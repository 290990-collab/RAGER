"""Optional LLM reader over any OpenAI-compatible endpoint.

Same model, prompt, temperature 0, seed 0 and token limit for every system; counting never goes to the LLM.
With ER, each document in the context carries its entity label. Responses are cached in results/llm_cache.jsonl.
Usage: python src/llm.py [minimo|parametrico|tutto]   (LLM_SEEDS=0,1,2,3,4 for more grid seeds)
       python src/llm.py unisci <responses.jsonl>    (adds remote responses to the cache)
"""
import hashlib
import json
import os
import re
import sys
import time
from pathlib import Path

import httpx
import numpy as np
import pandas as pd

from dataset import PARTIZIONI
from generator import genera, domande as gen_domande, FARMACI
from rag import Encoder, Indice, FUNZIONI, USA_ER

ROOT = Path(__file__).resolve().parent.parent
URL = os.environ.get("LLM_URL", "http://127.0.0.1:8080/v1")
MODEL = os.environ.get("LLM_MODEL", "qwen3.8-flash-next-iq3_xxs")
KEY_FILE = os.environ.get("LLM_KEY_FILE", "")
TAG = os.environ.get("LLM_TAG", "qwen3.8")
RACCOGLI = os.environ.get("LLM_RACCOGLI") == "1"     # 1 = collect prompts without calling the model
CACHE = ROOT / "results" / "llm_cache.jsonl"
DA_FARE = ROOT / "results" / os.environ.get("LLM_TODO", "llm_todo.jsonl")
SEEDS = [int(s) for s in os.environ.get("LLM_SEEDS", "0").split(",")]
PARAMS = {"temperature": 0, "seed": 0, "max_tokens": 400,
          "chat_template_kwargs": {"enable_thinking": False}}
TUTTI_FARMACI = FARMACI + ["Paracetamolo"]

TEMPLATE = """Rispondi solo in base al contesto.
Se il contesto non basta, dichiaralo esplicitamente.
Cita gli identificativi dei documenti usati.
{nota}
Contesto:
{context}

Domanda: {question}
Termina con una riga nel formato "RISPOSTA: ..." con l'elenco dei farmaci o dei pazienti richiesti, oppure "RISPOSTA: nessuno".
Risposta:"""
NOTA_ER = ("Secondo l'Entity Resolution, i documenti con la stessa etichetta \"entità\" riguardano la stessa persona, "
           "anche se riportano identificativi locali diversi: tutto ciò che riportano vale per quella persona.\n")


def chiave():
    if not KEY_FILE:
        return ""
    return next(l.strip() for l in open(KEY_FILE, encoding="utf-8") if l.strip() and not l.startswith("#"))


class LLM:
    def __init__(self):
        k = "" if RACCOGLI else chiave()
        self.h = {"Authorization": f"Bearer {k}"} if k else {}
        self.da_fare = {}
        self.cache = {}
        if CACHE.exists():
            for riga in CACHE.read_text(encoding="utf-8").splitlines():
                r = json.loads(riga)
                self.cache[r["h"]] = r["out"]
        self.n_nuove = 0

    def __call__(self, prompt):
        h = hashlib.sha256(json.dumps([MODEL, PARAMS, prompt], ensure_ascii=False).encode()).hexdigest()
        if h not in self.cache:
            body = {"model": MODEL, "messages": [{"role": "user", "content": prompt}], **PARAMS}
            if RACCOGLI:
                self.da_fare[h] = body
                return {"text": "", "usage": {}}
            for tentativo in range(3):
                try:
                    r = httpx.post(f"{URL}/chat/completions", headers=self.h, json=body, timeout=900)
                    r.raise_for_status()
                    break
                except httpx.HTTPError:
                    if tentativo == 2:
                        raise
                    time.sleep(30)
            j = r.json()
            out = {"text": j["choices"][0]["message"]["content"], "usage": j.get("usage", {})}
            self.cache[h] = out
            with open(CACHE, "a", encoding="utf-8") as f:
                f.write(json.dumps({"h": h, "out": out}, ensure_ascii=False) + "\n")
            self.n_nuove += 1
        return self.cache[h]


def contesto(ix, ret, etichetta):
    righe = [f"[{d} | entità {ix.gid(d)}] {ix.docs[d]['text']}" if etichetta else f"[{d}] {ix.docs[d]['text']}"
             for d in ret]
    return "\n".join(righe) if righe else "(nessun documento)"


def leggi_risposta(testo):
    """Parses the last 'RISPOSTA:' line into (drugs, patients, none, well_formed)."""
    m = re.findall(r"RISPOSTA:\s*(.*)", testo, flags=re.IGNORECASE)
    if not m:
        return set(), set(), False, False
    r = m[-1]
    farm = {f for f in TUTTI_FARMACI if re.search(rf"\b{f}\b", r, re.IGNORECASE)}
    paz = set(re.findall(r"\b[HP]:\d+\b", r))
    nessuno = bool(re.search(r"\bnessun[oa]?\b", r, re.IGNORECASE)) and not farm and not paz
    return farm, paz, nessuno, True


def valuta(testo, tipo, gt_risposta, ret, locali_gold):
    farm, paz, nessuno, ok = leggi_risposta(testo)
    citati = set(re.findall(r"\b[dx]\d+\b", testo))
    if tipo in ("entity-centric", "single-source", "multi-source"):
        acc = float(farm == set(gt_risposta))
    elif tipo == "multi-hop":
        riga = (re.findall(r"RISPOSTA:\s*(.*)", testo, flags=re.IGNORECASE) or [""])[-1]
        etich = any(re.search(rf"\b{re.escape(g)}\b", riga) for g in gt_risposta)
        acc = float(nessuno) if not gt_risposta else float((bool(paz) or etich) and paz <= locali_gold)
    else:
        acc = float(nessuno)
    return {"accuracy_llm": acc, "formato_ok": float(ok),
            "citazioni_valide": float(citati <= set(ret)) if citati else np.nan,
            "insufficiente": float(bool(re.search(r"non (basta|è sufficiente|sufficiente)|insufficient", testo,
                                                  re.IGNORECASE)))}


def run_minimo(llm, enc):
    docs = json.loads((ROOT / "data" / "documents.json").read_text(encoding="utf-8"))
    dom = [q for q in json.loads((ROOT / "data" / "questions.json").read_text(encoding="utf-8"))
           if q["tipo"] != "counting"]
    righe = []
    for p in PARTIZIONI:
        ix = Indice(docs, p, enc, nome=f"llm_{p}")
        for q in dom:
            gt = q["ground_truth"][p]
            gold_loc = {ix.meta(d)["local_id"] for d in gt["gold_docs"]} if q["tipo"] == "multi-hop" else set()
            for k in (2, 3, 4):
                for s in FUNZIONI:
                    ret = FUNZIONI[s](ix, q["query"], k, seed=q["seed"], gold=gt["gold_docs"])
                    if ret is None:
                        continue
                    varianti = [(s, USA_ER[s])] + ([(s + " nolabel", False)] if USA_ER[s] else [])
                    for nome, etich in varianti:
                        pr = TEMPLATE.format(nota=NOTA_ER if etich else "", context=contesto(ix, ret, etich),
                                             question=q["query"])
                        out = llm(pr)
                        righe.append({"partizione": p, "qid": q["qid"], "tipo": q["tipo"], "k": k, "sistema": nome,
                                      "recuperati": " ".join(ret), "risposta_llm": out["text"],
                                      **valuta(out["text"], q["tipo"], gt["risposta"], ret, gold_loc)})
        print(f"minimo {p}: {len(righe)} righe, {llm.n_nuove} richieste nuove", flush=True)
    return pd.DataFrame(righe)


def run_parametrico(llm, enc, N=500, omega=0.5, k=4, n_multi=20, n_single=10):
    """Grid sample: N = 500, omega = 0.5, alpha in {0, 0.5, 1}, seeds SEEDS, k = 4."""
    righe = []
    for seed, alpha in [(s, a) for s in SEEDS for a in (0, 0.5, 1)]:
        docs, info, locali, coorte, compl = genera(N, omega, alpha, seed)
        qs = gen_domande(docs, locali, coorte, compl, np.random.default_rng(1000 + seed))
        qs = [q for q in qs if q["tipo"] == "multi-source"][:n_multi] + \
             [q for q in qs if q["tipo"] == "single-source"][:n_single]
        ix = Indice(docs, "gid", enc, nome="llm_par")
        for q in qs:
            for s in FUNZIONI:
                ret = FUNZIONI[s](ix, q["query"], k, seed=q["seed"], gold=q["gold_docs"])
                pr = TEMPLATE.format(nota=NOTA_ER if USA_ER[s] else "", context=contesto(ix, ret, USA_ER[s]),
                                     question=q["query"])
                out = llm(pr)
                righe.append({**info, "tipo": q["tipo"], "k": k, "sistema": s, "risposta_llm": out["text"],
                              **valuta(out["text"], q["tipo"], q["risposta"], ret, set())})
        print(f"parametrico seed={seed} alpha={alpha}: {len(righe)} righe, {llm.n_nuove} richieste nuove", flush=True)
    return pd.DataFrame(righe)


if __name__ == "__main__":
    fase = sys.argv[1] if len(sys.argv) > 1 else "tutto"
    if fase == "unisci":
        noti = {json.loads(r)["h"] for r in CACHE.read_text(encoding="utf-8").splitlines()} if CACHE.exists() else set()
        nuove = [r for r in Path(sys.argv[2]).read_text(encoding="utf-8").splitlines() if json.loads(r)["h"] not in noti]
        with open(CACHE, "a", encoding="utf-8") as f:
            f.writelines(r + "\n" for r in nuove)
        print(f"{len(nuove)} risposte aggiunte alla cache")
        sys.exit()
    CACHE.parent.mkdir(exist_ok=True)
    enc, llm, t0 = Encoder(), LLM(), time.time()
    print(f"Modello {MODEL} @ {URL}", flush=True)
    pd.set_option("display.width", 200)
    if fase in ("minimo", "tutto"):
        df = run_minimo(llm, enc)
        df.to_csv(ROOT / "results" / f"llm_minimal_{TAG}.csv", index=False)
        print(df[df.partizione == "gid_1"].pivot_table(index=["tipo", "k"], columns="sistema",
                                                       values="accuracy_llm").round(2))
    if fase in ("parametrico", "tutto"):
        dp = run_parametrico(llm, enc)
        suff = "" if SEEDS == [0] else "_seeds"
        dp.to_csv(ROOT / "results" / f"llm_parametric_{TAG}{suff}.csv", index=False)
        print(dp.pivot_table(index=["tipo", "alpha"], columns="sistema", values="accuracy_llm").round(2))
    if RACCOGLI:
        with open(DA_FARE, "w", encoding="utf-8") as f:
            for h, body in llm.da_fare.items():
                f.write(json.dumps({"h": h, "body": body}, ensure_ascii=False) + "\n")
        print(f"Raccolte {len(llm.da_fare)} richieste in {DA_FARE.name} (nessuna chiamata al modello)")
    print(f"Fatto in {time.time() - t0:.0f}s; richieste nuove: {llm.n_nuove}")
