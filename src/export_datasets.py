"""Consegnabile Sez. 13: esporta i dataset sintetici dell'esperimento parametrico.

Rigenera con gli stessi seed di experiment.py (dataset: seed; domande: 1000+seed) i 180 dataset
N x omega x alpha x seed e li salva in un formato unico:
  data/parametric/documents.csv  dataset_id, document_id, source, local_id, gid, testo, farmaco, quantita, coorte
  data/parametric/questions.json   dataset_id, qid, tipologia, domanda, seed (ID locale), ground truth
Le domande entity-centric sono nello stesso ordine usato in experiment.py (qid = posizione);
le domande di conteggio hanno come ground truth COUNT(DISTINCT gid).
Controllo: il numero di domande per dataset coincide con le righe di results/experiment_queries.csv.
Uso: python src/export_datasets.py
"""
import json
from itertools import product
from pathlib import Path

import numpy as np
import pandas as pd

from experiment import N_VAL, OMEGA, ALPHA, SEEDS, K_VAL
from generator import genera, domande, controlli, FARMACI
from rag import SISTEMI

ROOT = Path(__file__).resolve().parent.parent

if __name__ == "__main__":
    out = ROOT / "data" / "parametric"
    out.mkdir(parents=True, exist_ok=True)
    righe_doc, righe_q, n_entity = [], [], {}
    for N, omega, alpha, seed in product(N_VAL, OMEGA, ALPHA, SEEDS):
        ds = f"N{N}_w{omega}_a{alpha}_s{seed}"
        docs, info, locali, coorte, compl = genera(N, omega, alpha, seed)
        controlli(docs, info)
        for d in docs:
            m = d["metadata"]
            righe_doc.append({"dataset_id": ds, "N": N, "omega": omega, "alpha": alpha, "seed": seed,
                              "document_id": d["doc_id"], "source": m["source"], "local_id": m["local_id"],
                              "gid": m["gid"], "testo": d["text"], "farmaco": m["farmaco"],
                              "quantita": m["quantita"], "coorte": m["coorte"]})
        qs = domande(docs, locali, coorte, compl, np.random.default_rng(1000 + seed))
        n_entity[(N, omega, alpha, seed)] = len(qs)
        for i, q in enumerate(qs):
            righe_q.append({"dataset_id": ds, "qid": f"q{i}", "tipologia": q["tipo"],
                            "complementare": q["complementare"], "domanda": q["query"],
                            "seed_locale": q["seed"], "gold_docs": q["gold_docs"], "risposta": q["risposta"]})
        for j, f in enumerate(FARMACI):
            esatto = len({d["metadata"]["gid"] for d in docs if d["metadata"]["farmaco"] == f})
            righe_q.append({"dataset_id": ds, "qid": f"c{j}", "tipologia": "counting", "complementare": None,
                            "domanda": f"Quanti pazienti distinti hanno eventi di {f}?", "seed_locale": None,
                            "gold_docs": None, "risposta": esatto})

    # Controllo di coerenza con i risultati gia' calcolati
    rq = pd.read_csv(ROOT / "results" / "experiment_queries.csv")
    attese = rq.groupby(["N", "omega", "alpha", "seed"]).size() // (len(K_VAL) * len(SISTEMI))
    for key, n in n_entity.items():
        assert attese.loc[key] == n, f"domande diverse per {key}: {attese.loc[key]} vs {n}"

    pd.DataFrame(righe_doc).to_csv(out / "documents.csv", index=False)
    with open(out / "questions.json", "w", encoding="utf-8") as fh:
        json.dump(righe_q, fh, ensure_ascii=False, indent=1)
    print(f"{len(n_entity)} dataset, {len(righe_doc)} documenti, {len(righe_q)} domande -> {out}")
    print("Controllo superato: domande coerenti con results/experiment_queries.csv")
