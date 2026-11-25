"""Parametric grid: N x omega x alpha x 5 seeds, k in {2, 4, 8}.

Output: results/experiment_queries.csv, experiment_counts.csv, experiment_aggregate.csv
Usage: python src/experiment.py [--rapido]
"""
import sys
import time
from itertools import product
from pathlib import Path

import numpy as np
import pandas as pd

from generator import genera, domande, controlli, FARMACI
from rag import (Encoder, Indice, SISTEMI, FUNZIONI, USA_ER, leggi_entity, leggi_conteggio,
                 recall_at_k, precision_at_k, completezza, costo)

ROOT = Path(__file__).resolve().parent.parent
N_VAL, OMEGA, ALPHA, K_VAL, SEEDS = [100, 500, 1000], [0, 0.25, 0.5, 0.75], [0, 0.5, 1], [2, 4, 8], [0, 1, 2, 3, 4]


def valuta_dataset(docs, info, qs, enc, partizione="gid", gid_vero="gid", nome="esp"):
    """Evaluates every system on one dataset: `partizione` is the ER map used for retrieval,
    `gid_vero` the one used for the ground truth."""
    ix = Indice(docs, partizione, enc, nome=nome)
    righe = []
    for q, k, s in product(qs, K_VAL, SISTEMI):
        ret = FUNZIONI[s](ix, q["query"], k, seed=q["seed"], gold=q["gold_docs"])
        g_seed = ix.mappa_er[q["seed"]]
        disamb = float(any(ix.gid(d) == g_seed for d in ix.cerca(q["query"], k)))
        n_doc, n_tok = costo(ix, ret)
        risp = leggi_entity(ix, ret, q["seed"], USA_ER[s])
        righe.append({**info, "tipo": q["tipo"], "complementare": q["complementare"], "k": k, "sistema": s,
                      "recall": recall_at_k(ret, q["gold_docs"]),
                      "precision": precision_at_k(ret, q["gold_docs"]),
                      "completezza": completezza(ix, ret, q["gold_docs"], q["risposta"]),
                      "accuracy": float(risp == q["risposta"]), "n_doc": n_doc, "n_token": n_tok,
                      "disambiguazione": disamb})
    conti = []
    for f, k in product(FARMACI, K_VAL):
        query = f"Quanti pazienti distinti hanno eventi di {f}?"
        del_f = [d for d in docs if d["metadata"]["farmaco"] == f]
        esatto = len({d["metadata"][gid_vero] for d in del_f})                  # COUNT(DISTINCT gid)
        somma_locale = sum(len({d["metadata"]["local_id"] for d in del_f if d["metadata"]["source"] == src})
                           for src in ("H", "P"))
        for s in ("BASE", "ER-pool"):
            ret = FUNZIONI[s](ix, query, k)
            conti.append({**info, "farmaco": f, "k": k, "sistema": s, "esatto": esatto,
                          "somma_locale": somma_locale, "rag": leggi_conteggio(ix, ret, f, USA_ER[s])})
    return righe, conti


def aggrega(df, chiavi):
    m = ["recall", "precision", "completezza", "accuracy", "n_doc", "n_token", "disambiguazione"]
    per_seed = df.groupby(chiavi + ["seed"])[m].mean().reset_index()
    agg = per_seed.groupby(chiavi)[m].agg(["mean", "std"])
    agg.columns = [f"{a}_{b}" for a, b in agg.columns]
    return agg.reset_index()


if __name__ == "__main__":
    rapido = "--rapido" in sys.argv
    n_val, seeds = ([100], [0, 1]) if rapido else (N_VAL, SEEDS)
    enc = Encoder()
    righe, conti, t0 = [], [], time.time()
    for N, omega, alpha, seed in product(n_val, OMEGA, ALPHA, seeds):
        docs, info, locali, coorte, compl = genera(N, omega, alpha, seed)
        controlli(docs, info)
        qs = domande(docs, locali, coorte, compl, np.random.default_rng(1000 + seed))
        r, c = valuta_dataset(docs, info, qs, enc)
        righe += r
        conti += c
        print(f"N={N} omega={omega} alpha={alpha} seed={seed}: {len(docs)} doc, {len(qs)} query "
              f"[{time.time() - t0:.0f}s]", flush=True)

    df, dc = pd.DataFrame(righe), pd.DataFrame(conti)
    # Sanity checks
    ss = df[df.tipo == "single-source"]
    a = ss[ss.sistema == "ER+seed"].recall.to_numpy()
    b = ss[ss.sistema == "BASE+seed"].recall.to_numpy()
    assert np.array_equal(a, b), "controllo negativo fallito"
    assert (dc.somma_locale >= dc.esatto).all()

    out = ROOT / "results"
    out.mkdir(exist_ok=True)
    suff = "_quick" if rapido else ""
    df.to_csv(out / f"experiment_queries{suff}.csv", index=False)
    dc.to_csv(out / f"experiment_counts{suff}.csv", index=False)
    aggrega(df, ["N", "omega", "alpha", "k", "tipo", "sistema"]).to_csv(
        out / f"experiment_aggregate{suff}.csv", index=False)
    print(f"Controlli superati. Tempo totale {time.time() - t0:.0f}s")
