"""Phase 1: do the measured results survive varied wording and a second embedding model?

Same setting as followups.py (N = 500, omega = alpha = 0.5, seeds 0..4, k in {2, 4, 8}). Four text conditions:
  fisso    the original template and question
  variato  3 document templates per source and 5 question paraphrases
  refusi   variato, plus typos: 20 % of documents write the ID as "H-37", "H 37" or "H37",
           20 % misspell the drug
  nome     variato with the patient's name in the text; the question names the patient instead of the ID
Two embedding models: MiniLM (the main one) and multilingual E5-small (trained for retrieval).
Metadata never change, so seed-based systems and the reader are unaffected; only retrieval sees the text.
Output: results/robustness_text_queries.csv, results/robustness_text_aggregate.csv
Usage: python src/robustness_text.py [--rapido]
"""
import sys
import time
from pathlib import Path

import numpy as np
import pandas as pd

from followups import NOMI, COGNOMI, SISTEMI, valuta, aggrega
from generator import genera, domande, controlli
from rag import Encoder, FUNZIONI, MODELLO

ROOT = Path(__file__).resolve().parent.parent
N, OMEGA, ALPHA, SEEDS = 500, 0.5, 0.5, [0, 1, 2, 3, 4]
CONDIZIONI = ["fisso", "variato", "refusi", "nome"]
MODELLI = {"MiniLM": (MODELLO, ("", "")),
           "E5-small": ("intfloat/multilingual-e5-small", ("query: ", "passage: "))}
P_REFUSO = 0.2

DOC = {"H": ["{p} ha ricevuto {f}, quantità {q}.",
             "Al paziente {p} è stato somministrato {f} ({q} unità).",
             "Ricovero di {p}: terapia con {f}, dose {q}."],
       "P": ["{p} ha ritirato {f}, quantità {q}.",
             "Farmacia: dispensato {f} a {p}, confezioni {q}.",
             "Ricetta di {p}: {f}, {q} confezioni."]}
DOMANDE = ["Quali farmaci risultano per {p} in tutte le sorgenti?",
           "Che terapie ha avuto {p}?",
           "Elenca tutti i farmaci registrati per {p}.",
           "{p}: quali medicinali gli sono stati dati?",
           "Dimmi i farmaci di {p} in ospedale e in farmacia."]
SISTEMI_T = {**SISTEMI["ibrido"], "BASE+seed": (FUNZIONI["BASE+seed"], False),
             "ER-pool": (FUNZIONI["ER-pool"], True)}


def refuso_id(lid, rng):
    src, num = lid.split(":")
    return [f"{src}-{num}", f"{src} {num}", f"{src}{num}"][int(rng.integers(3))]


def refuso_parola(w, rng):
    i = int(rng.integers(1, len(w) - 1))
    return w[:i] + w[i] + w[i:] if rng.random() < 0.5 else w[:i - 1] + w[i] + w[i - 1] + w[i + 1:]


def riscrivi(docs, qs, cond, rng):
    """Rewrites document texts and questions for a condition; metadata stay as they are."""
    if cond == "fisso":
        return docs, qs
    gids = sorted({d["metadata"]["gid"] for d in docs}, key=lambda g: int(g[1:]))
    combo = [f"{n} {c}" for n in NOMI for c in COGNOMI]
    nome = dict(zip(gids, (combo[i] for i in rng.permutation(len(combo))[:len(gids)])))
    nuovi = []
    for d in docs:
        m = d["metadata"]
        p, f = m["local_id"], m["farmaco"]
        if cond == "refusi":
            if rng.random() < P_REFUSO:
                p = refuso_id(p, rng)
            if rng.random() < P_REFUSO:
                f = refuso_parola(f, rng)
        if cond == "nome":
            p = f"{p} ({nome[m['gid']]})"
        t = DOC[m["source"]][int(rng.integers(3))].format(p=p, f=f, q=m["quantita"])
        nuovi.append({**d, "text": t})
    gid_di = {d["metadata"]["local_id"]: d["metadata"]["gid"] for d in docs}
    qs = [{**q, "query": DOMANDE[int(rng.integers(len(DOMANDE)))].format(
        p=nome[gid_di[q["seed"]]] if cond == "nome" else q["seed"])} for q in qs]
    return nuovi, qs


if __name__ == "__main__":
    rapido = "--rapido" in sys.argv
    seeds, suff = ([0], "_quick") if rapido else (SEEDS, "")
    righe, t0 = [], time.time()
    for modello, (nome_m, prefissi) in MODELLI.items():
        enc = Encoder(nome_m, prefissi)
        for cond in CONDIZIONI:
            for seed in seeds:
                docs, info, locali, coorte, compl = genera(N, OMEGA, ALPHA, seed)
                controlli(docs, info)
                qs = domande(docs, locali, coorte, compl, np.random.default_rng(1000 + seed))
                docs, qs = riscrivi(docs, qs, cond, np.random.default_rng(4000 + seed))
                for d in docs:
                    assert d["metadata"]["gid"] not in d["text"]
                info = {**info, "modello": modello, "condizione": cond}
                r, _, _ = valuta(docs, info, qs, enc, SISTEMI_T)
                righe += r
            print(f"{modello} {cond} [{time.time() - t0:.0f}s]", flush=True)

    df = pd.DataFrame(righe)
    # Seed-based systems read metadata only: wording cannot change them
    s = df[df.sistema == "ER+seed"]
    assert (s.accuracy == 1).all(), "ER+seed should not depend on the text"
    out = ROOT / "results"
    df.to_csv(out / f"robustness_text_queries{suff}.csv", index=False)
    aggrega(df, ["modello", "condizione", "k", "tipo", "sistema"]).to_csv(
        out / f"robustness_text_aggregate{suff}.csv", index=False)
    print(f"Total {time.time() - t0:.0f}s")
