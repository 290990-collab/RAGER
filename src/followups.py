"""Follow-up studies at N = 500, omega = alpha = 0.5, seeds 0..4, k in {2, 4, 8}.

  omonimi    patient names in the text; a share h in {0, .1, .25} of people share their name with someone else.
             Ideal ER against ER that links by name.
  indici     one index per source, results fused by score or with k/2 slots per source.
  diversita  near-duplicates (eps in {0, .25, .5}); rerank for source variety or with MMR.
  ibrido     lexical BM25 and dense search fused with RRF, with and without GID expansion.
Output: results/followup_queries.csv, results/followup_aggregate.csv
Usage: python src/followups.py [--rapido]
"""
import re
import sys
import time
from collections import Counter
from pathlib import Path

import numpy as np
import pandas as pd

from extensions import quasi_duplicati, gold_aggiornato
from generator import genera, domande, controlli
from rag import (Encoder, Indice, FUNZIONI, leggi_entity, recall_at_k, precision_at_k, completezza, costo)

ROOT = Path(__file__).resolve().parent.parent
N, OMEGA, ALPHA, SEEDS, K_VAL = 500, 0.5, 0.5, [0, 1, 2, 3, 4], [2, 4, 8]
NOMI = ["Marco", "Giulia", "Luca", "Sara", "Paolo", "Anna", "Giorgio", "Elena", "Franco", "Laura", "Matteo",
        "Chiara", "Davide", "Marta", "Stefano", "Silvia", "Andrea", "Paola", "Roberto", "Federica", "Simone",
        "Valeria", "Alberto", "Irene", "Claudio", "Monica", "Fabio", "Alessia", "Enzo", "Rita"]
COGNOMI = ["Rossi", "Russo", "Ferrari", "Esposito", "Bianchi", "Romano", "Colombo", "Ricci", "Marino", "Greco",
           "Bruno", "Gallo", "Conti", "De Luca", "Mancini", "Costa", "Giordano", "Rizzo", "Lombardi", "Moretti",
           "Barbieri", "Fontana", "Santoro", "Mariani", "Rinaldi", "Caruso", "Ferrara", "Galli", "Martini", "Leone"]


# ---------------------------------------------------------------- data variants
def con_nomi(docs, coorte, h, rng):
    """Writes each person's name in the text; a share h of people get the name of someone else."""
    V = len(coorte)
    combo = [f"{n} {c}" for n in NOMI for c in COGNOMI]
    nome = {e: combo[i] for e, i in enumerate(rng.permutation(len(combo))[:V].tolist())}
    coppie = rng.permutation(V)[:2 * round(h * V / 2)].reshape(-1, 2)
    for a, b in coppie.tolist():
        nome[b] = nome[a]
    for d in docs:
        m = d["metadata"]
        m["nome"] = nome[int(m["gid"][1:])]
        m["gid_nome"] = "N:" + m["nome"]
        d["text"] = d["text"].replace(m["local_id"] + " ", f"{m['local_id']} ({m['nome']}) ", 1)
    omonimi = sum(c > 1 for c in Counter(nome.values()).values())
    return {"persone_con_omonimo": 2 * len(coppie) / V, "nomi_condivisi": omonimi}


# ---------------------------------------------------------------- extra retrieval
TOKEN = re.compile(r"[a-z]+:\d+|\w+")


class Extra:
    """Exact dense scores, per-source search and BM25 over the documents of an index."""

    def __init__(self, ix, k1=1.5, b=0.75):
        self.ix = ix
        self.ids = list(ix.docs)
        self.pos = {d: j for j, d in enumerate(self.ids)}
        self.E = np.stack([ix.E[i] for i in self.ids])
        self.src = np.array([ix.meta(i)["source"] for i in self.ids])
        toks = [TOKEN.findall(ix.docs[i]["text"].lower()) for i in self.ids]
        lun = np.array([len(t) for t in toks], dtype=float)
        df = Counter(w for t in toks for w in set(t))
        n = len(self.ids)
        self.idf = {w: np.log(1 + (n - c + 0.5) / (c + 0.5)) for w, c in df.items()}
        self.post = {}
        for j, t in enumerate(toks):
            for w, tf in Counter(t).items():
                self.post.setdefault(w, []).append((j, tf * (k1 + 1) / (tf + k1 * (1 - b + b * lun[j] / lun.mean()))))

    def ordina(self, punteggi, mask=None):
        idx = np.arange(len(self.ids)) if mask is None else np.flatnonzero(mask)
        return [self.ids[j] for j in sorted(idx, key=lambda j: (-punteggi[j], self.ids[j]))]

    def denso(self, query):
        return self.E @ self.ix.qvec(query)

    def bm25(self, query):
        s = np.zeros(len(self.ids))
        for w in TOKEN.findall(query.lower()):
            for j, v in self.post.get(w, []):
                s[j] += self.idf[w] * v
        return s

    def rrf(self, query, c=60):
        s = np.zeros(len(self.ids))
        for punteggi in (self.denso(query), self.bm25(query)):
            for r, d in enumerate(self.ordina(punteggi)):
                s[self.pos[d]] += 1 / (c + r + 1)
        return s


def espandi(ix, query, candidati, k):
    """ER-pool expansion of any candidate list."""
    out = []
    for doc in candidati:
        for m in ix.rerank(query, ix.where("gid", ix.gid(doc)), k):
            if len(out) < k and m not in out:
                out.append(m)
    return out


def per_fonte(x, query, k, quota):
    s = x.denso(query)
    liste = {src: x.ordina(s, x.src == src)[:k] for src in ("H", "P")}
    if quota:
        return liste["H"][:k // 2] + liste["P"][:k // 2]
    return sorted(liste["H"] + liste["P"], key=lambda d: (-float(s[x.pos[d]]), d))[:k]


def diversita_fonte(ix, query, ids, k):
    """Best document of each source first, then the next best of each, and so on."""
    ordine = ix.rerank(query, ids, len(ids))
    code = {}
    for d in ordine:
        code.setdefault(ix.meta(d)["source"], []).append(d)
    out = []
    while len(out) < k and any(code.values()):
        for src in sorted(code, key=lambda s: ordine.index(code[s][0]) if code[s] else 1e9):
            if code[src] and len(out) < k:
                out.append(code[src].pop(0))
    return out


def mmr(ix, query, ids, k, lam=0.5):
    q, out, resto = ix.qvec(query), [], sorted(ids)
    while resto and len(out) < k:
        def valore(d):
            ridondanza = max((float(ix.E[d] @ ix.E[s]) for s in out), default=0.0)
            return lam * float(ix.E[d] @ q) - (1 - lam) * ridondanza
        best = max(resto, key=valore)
        out.append(best)
        resto.remove(best)
    return out


def seed_gid(ix, q):
    return ix.where("gid", ix.mappa_er[q["seed"]])


SISTEMI = {
    "omonimi": {"BASE": (FUNZIONI["BASE"], False), "BASE+seed": (FUNZIONI["BASE+seed"], False),
                "ER+seed": (FUNZIONI["ER+seed"], True), "ER-pool": (FUNZIONI["ER-pool"], True)},
    "indici": {"BASE": (FUNZIONI["BASE"], False),
               "BASE split, merged": (lambda ix, x, q, k: per_fonte(x, q["query"], k, False), False),
               "BASE split, k/2 each": (lambda ix, x, q, k: per_fonte(x, q["query"], k, True), False),
               "ER-pool": (FUNZIONI["ER-pool"], True),
               "ER-pool split, k/2 each": (lambda ix, x, q, k: espandi(ix, q["query"], per_fonte(x, q["query"], k, True), k), True)},
    "diversita": {"BASE+seed": (FUNZIONI["BASE+seed"], False), "ER+seed": (FUNZIONI["ER+seed"], True),
                  "ER+seed, source variety": (lambda ix, x, q, k: diversita_fonte(ix, q["query"], seed_gid(ix, q), k), True),
                  "ER+seed, MMR": (lambda ix, x, q, k: mmr(ix, q["query"], seed_gid(ix, q), k), True)},
    "ibrido": {"BASE": (FUNZIONI["BASE"], False),
               "BM25": (lambda ix, x, q, k: x.ordina(x.bm25(q["query"]))[:k], False),
               "BM25 + ER": (lambda ix, x, q, k: espandi(ix, q["query"], x.ordina(x.bm25(q["query"]))[:k], k), True),
               "Hybrid": (lambda ix, x, q, k: x.ordina(x.rrf(q["query"]))[:k], False),
               "Hybrid + ER": (lambda ix, x, q, k: espandi(ix, q["query"], x.ordina(x.rrf(q["query"]))[:k], k), True),
               "ER+seed": (FUNZIONI["ER+seed"], True)},
}


def valuta(docs, info, qs, enc, sistemi, partizione="gid"):
    ix = Indice(docs, partizione, enc, nome="followup")
    x = Extra(ix)
    righe = []
    for q in qs:
        g_vero = ix.meta(q["gold_docs"][0])["gid"]
        for k in K_VAL:
            for nome, (f, er) in sistemi.items():
                if f in FUNZIONI.values():
                    ret = f(ix, q["query"], k, seed=q["seed"], gold=q["gold_docs"])
                else:
                    ret = f(ix, x, q, k)
                n_doc, n_tok = costo(ix, ret)
                righe.append({**info, "tipo": q["tipo"], "k": k, "sistema": nome,
                              "recall": recall_at_k(ret, q["gold_docs"]),
                              "precision": precision_at_k(ret, q["gold_docs"]),
                              "completezza": completezza(ix, ret, q["gold_docs"], q["risposta"]),
                              "accuracy": float(leggi_entity(ix, ret, q["seed"], er) == q["risposta"]),
                              "trova_paziente": float(any(ix.meta(d)["gid"] == g_vero for d in ret)),
                              "n_doc": n_doc, "n_token": n_tok})
    return righe, ix, x


def aggrega(df, chiavi):
    m = ["recall", "precision", "completezza", "accuracy", "trova_paziente", "n_doc", "n_token"]
    per_seed = df.groupby(chiavi + ["seed"])[m].mean().reset_index()
    agg = per_seed.groupby(chiavi)[m].agg(["mean", "std"])
    agg.columns = [f"{a}_{b}" for a, b in agg.columns]
    return agg.reset_index()


if __name__ == "__main__":
    rapido = "--rapido" in sys.argv
    seeds, suff = ([0], "_quick") if rapido else (SEEDS, "")
    enc, righe, t0 = Encoder(), [], time.time()
    uguali = []
    configurazioni = ([("omonimi", h, er) for h in (0, 0.1, 0.25) for er in ("ideal", "names")]
                      + [("indici", 0, "ideal"), ("ibrido", 0, "ideal")]
                      + [("diversita", e, "ideal") for e in (0, 0.25, 0.5)])
    for studio, x_val, er in configurazioni:
        for seed in seeds:
            rng = np.random.default_rng(3000 + seed)
            docs, info, locali, coorte, compl = genera(N, OMEGA, ALPHA, seed)
            controlli(docs, info)
            qs = domande(docs, locali, coorte, compl, np.random.default_rng(1000 + seed))
            extra = {}
            if studio == "omonimi":
                extra = con_nomi(docs, coorte, x_val, rng)
            elif studio == "diversita":
                docs = quasi_duplicati(docs, x_val, np.random.default_rng(2000 + seed))
                qs = gold_aggiornato(qs, docs)
            info = {**info, "studio": studio, "x": x_val, "er": er, **extra}
            r, ix, x = valuta(docs, info, qs, enc, SISTEMI[studio], "gid_nome" if er == "names" else "gid")
            righe += r
            if studio == "indici":
                for q in qs:
                    for k in K_VAL:
                        uguali.append(set(per_fonte(x, q["query"], k, False)) == set(ix.cerca(q["query"], k)))
        print(f"{studio} x={x_val} er={er} [{time.time() - t0:.0f}s]", flush=True)

    df = pd.DataFrame(righe)
    # Ideal ER is unaffected by names and homonyms; split indices merged by score equal one index
    o = df[(df.studio == "omonimi") & (df.er == "ideal") & (df.sistema == "ER+seed")]
    assert (o.accuracy == 1).all(), "ideal ER should not depend on homonyms"
    assert np.mean(uguali) >= 0.99, f"split and merged differs from one index in {1 - np.mean(uguali):.1%}"
    out = ROOT / "results"
    df.to_csv(out / f"followup_queries{suff}.csv", index=False)
    aggrega(df, ["studio", "x", "er", "k", "tipo", "sistema"]).to_csv(out / f"followup_aggregate{suff}.csv", index=False)
    print(f"split = one index in {np.mean(uguali):.2%} of queries. Total {time.time() - t0:.0f}s")
