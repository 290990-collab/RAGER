"""Punto E - Estensioni eseguite (traccia Sez. 12, nota Sez. 4; Paper 3.2).

Configurazione fissa [MIO]: N = 500, omega = 0.5, alpha = 0.5, seed 0..4, k in {2, 4, 8}.
Quattro studi, ognuno varia un solo fattore:
  dirty      D_H = D_P = round(delta*N), delta in {0, 0.1, 0.25}            (Dirty ER)
  falsi      falsi negativi fn in {0, .25, .5} x falsi positivi fp in {0, .1, .25}  (qualita' del linkage)
  duplicati  quota eps in {0, .25, .5} di eventi con un quasi-duplicato        (rumore, H3: spreco di budget)
  errori_id  quota eps in {0, .1, .25} di documenti con l'ID locale sbagliato nel testo (rumore)
Output: results/extension_queries.csv, results/extension_aggregate.csv
"""
import time
from pathlib import Path

import numpy as np
import pandas as pd

from experiment import valuta_dataset, aggrega
from generator import genera, domande, controlli
from rag import Encoder

ROOT = Path(__file__).resolve().parent.parent
N, OMEGA, ALPHA, SEEDS = 500, 0.5, 0.5, [0, 1, 2, 3, 4]


def falsi_match(docs, coorte, fn, fp, rng):
    """Mappa ER imperfetta `gid_er`. fn: quota di entita' condivise spezzate (il lato P riceve un GID nuovo);
    fp: quota di entita' esclusive di H fuse con un'esclusiva di P. Ritorna precision/recall del linkage."""
    cond = [e for e, c in enumerate(coorte) if c == "condivisa"]
    sh = [e for e, c in enumerate(coorte) if c == "solo_H"]
    sp = [e for e, c in enumerate(coorte) if c == "solo_P"]
    spezzate = set(rng.choice(cond, size=round(fn * len(cond)), replace=False).tolist()) if cond else set()
    n_fp = round(fp * len(sh))
    fusioni = dict(zip(rng.choice(sp, size=n_fp, replace=False).tolist(),
                       rng.choice(sh, size=n_fp, replace=False).tolist()))   # P-esclusiva -> H-esclusiva
    for d in docs:
        m = d["metadata"]
        e = int(m["gid"][1:])
        if e in spezzate and m["source"] == "P":
            m["gid_er"] = f"G{e}_P"
        elif e in fusioni:
            m["gid_er"] = f"G{fusioni[e]}"
        else:
            m["gid_er"] = m["gid"]
    tp, pred = len(cond) - len(spezzate), len(cond) - len(spezzate) + n_fp
    return {"linkage_precision": tp / pred if pred else 1.0, "linkage_recall": tp / len(cond) if cond else 1.0}


def quasi_duplicati(docs, eps, rng):
    """Per una quota eps di eventi aggiunge un quasi-duplicato (stessa entita', testo quasi uguale)."""
    scelti = rng.choice(len(docs), size=round(eps * len(docs)), replace=False).tolist()
    nuovi = []
    for j, i in enumerate(scelti):
        d = docs[i]
        nuovi.append({"doc_id": f"x{j + 1}", "text": d["text"].replace("ha ricevuto", "risulta aver ricevuto"),
                      "metadata": dict(d["metadata"])})
    return docs + nuovi


def errori_id(docs, eps, rng):
    """Per una quota eps di documenti l'ID locale scritto nel testo e' sbagliato (altro ID della stessa
    sorgente); i metadati restano corretti. Nessun nuovo documento."""
    per_src = {}
    for d in docs:
        per_src.setdefault(d["metadata"]["source"], set()).add(d["metadata"]["local_id"])
    per_src = {s: sorted(v) for s, v in per_src.items()}
    for i in rng.choice(len(docs), size=round(eps * len(docs)), replace=False).tolist():
        m = docs[i]["metadata"]
        altro = m["local_id"]
        while altro == m["local_id"]:
            altro = per_src[m["source"]][int(rng.integers(len(per_src[m["source"]])))]
        docs[i]["text"] = docs[i]["text"].replace(m["local_id"] + " ", altro + " ", 1)
        m["lid_testo"] = altro
    return docs


def gold_aggiornato(qs, docs):
    """Ricalcola la ground truth dopo l'aggiunta di documenti (sempre dal GID vero)."""
    per_gid = {}
    for d in docs:
        per_gid.setdefault(d["metadata"]["gid"], []).append(d)
    for q in qs:
        g = next(d["metadata"]["gid"] for d in docs if d["metadata"]["local_id"] == q["seed"])
        q["gold_docs"] = [d["doc_id"] for d in per_gid[g]]
        q["risposta"] = sorted({d["metadata"]["farmaco"] for d in per_gid[g]})
    return qs


if __name__ == "__main__":
    enc, righe, t0 = Encoder(), [], time.time()
    configurazioni = ([("dirty", x, None) for x in (0, 0.1, 0.25)]
                      + [("falsi", fn, fp) for fn in (0, 0.25, 0.5) for fp in (0, 0.1, 0.25)]
                      + [("duplicati", x, None) for x in (0, 0.25, 0.5)]
                      + [("errori_id", x, None) for x in (0, 0.1, 0.25)])
    for studio, x, y in configurazioni:
        for seed in SEEDS:
            rng = np.random.default_rng(2000 + seed)
            D = round(x * N) if studio == "dirty" else 0
            docs, info, locali, coorte, compl = genera(N, OMEGA, ALPHA, seed, D_H=D, D_P=D)
            controlli(docs, info)
            qs = domande(docs, locali, coorte, compl, np.random.default_rng(1000 + seed))
            extra, partizione = {}, "gid"
            if studio == "falsi":
                extra = falsi_match(docs, coorte, x, y, rng)
                partizione = "gid_er"
            elif studio == "duplicati":
                docs = quasi_duplicati(docs, x, rng)
                qs = gold_aggiornato(qs, docs)
            elif studio == "errori_id":
                docs = errori_id(docs, x, rng)
            info = {**info, "studio": studio, "x": x, "y": y if y is not None else 0, **extra}
            r, _ = valuta_dataset(docs, info, qs, enc, partizione=partizione, nome="est")
            righe += r
        print(f"{studio} x={x} y={y} [{time.time() - t0:.0f}s]", flush=True)

    df = pd.DataFrame(righe)
    out = ROOT / "results"
    df.to_csv(out / "extension_queries.csv", index=False)
    aggrega(df, ["studio", "x", "y", "k", "tipo", "sistema"]).to_csv(out / "extension_aggregate.csv", index=False)
    # Controlli: senza perturbazione i quattro studi coincidono con la stessa configurazione di base
    base = df[(df.x == 0) & (df.y == 0)]
    acc = base.groupby(["studio", "sistema", "k", "tipo"]).accuracy.mean().unstack("studio")
    assert np.allclose(acc.to_numpy(), acc.iloc[:, [0]].to_numpy()), "le configurazioni di controllo differiscono"
    print(f"Controlli superati. Tempo totale {time.time() - t0:.0f}s")
