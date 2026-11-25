"""Benchmark on the minimal example for every ER partition, k in {2, 3, 4} and system.

Counting questions use COUNT(DISTINCT gid); the count from the retrieved text is kept only for comparison.
"""
import json
from pathlib import Path

import pandas as pd

from dataset import PARTIZIONI
from rag import (Encoder, Indice, SISTEMI, FUNZIONI, USA_ER, leggi_entity, leggi_multihop,
                 leggi_conteggio, recall_at_k, precision_at_k, completezza, costo)

ROOT = Path(__file__).resolve().parent.parent
K_VALORI = [2, 3, 4]


def conteggio_esatto(docs, p, farmaco):
    """Exact COUNT(DISTINCT gid) on the metadata."""
    return len({d["metadata"][p] for d in docs if d["metadata"]["farmaco"] == farmaco})


def valuta(docs, domande, enc):
    righe = []
    for p in PARTIZIONI:
        ix = Indice(docs, p, enc, nome=f"mini_{p}")
        for q in domande:
            gt = q["ground_truth"][p]
            for k in K_VALORI:
                for s in SISTEMI:
                    ret = FUNZIONI[s](ix, q["query"], k, seed=q["seed"], gold=gt["gold_docs"])
                    if ret is None:
                        continue
                    er = USA_ER[s]
                    r = {"partizione": p, "qid": q["qid"], "tipo": q["tipo"], "k": k, "sistema": s,
                         "recuperati": " ".join(ret),
                         "recall": recall_at_k(ret, gt["gold_docs"]),
                         "precision": precision_at_k(ret, gt["gold_docs"])}
                    r["n_doc"], r["n_token"] = costo(ix, ret)
                    if q["tipo"] == "entity-centric":
                        risp = leggi_entity(ix, ret, q["seed"], er)
                        r["completezza"] = completezza(ix, ret, gt["gold_docs"], gt["risposta"])
                        r["accuracy"] = float(risp == gt["risposta"])
                    elif q["tipo"] == "multi-hop":
                        f1, f2 = "Insulina", "Aspirina"
                        risp = leggi_multihop(ix, ret, f1, f2, er)
                        pertinenti = [d for d in ret if d in set(gt["gold_docs"])]
                        r["completezza"] = float(leggi_multihop(ix, pertinenti, f1, f2, True) == gt["risposta"])
                        r["accuracy"] = float(risp == gt["risposta"])
                    elif q["tipo"] == "counting":
                        farmaco = q["query"].split("eventi di ")[1].rstrip("?")
                        risp = leggi_conteggio(ix, ret, farmaco, er)
                        r["conteggio_rag"] = risp
                        r["conteggio_esatto"] = conteggio_esatto(docs, p, farmaco)
                        r["accuracy"] = float(r["conteggio_esatto"] == gt["risposta"])
                        r["accuracy_rag"] = float(risp == gt["risposta"])
                    else:
                        risp = [d for d in ret if ix.meta(d)["farmaco"] == "Paracetamolo"]
                        r["accuracy"] = float(risp == [])
                    r["risposta"] = str(risp)
                    righe.append(r)
    return pd.DataFrame(righe)


def controlli(df):
    """Checks that hold by construction."""
    o = df[(df.sistema == "ORACLE") & (df.tipo != "negativa")]
    assert (o[o.k >= 4].recall == 1).all()
    a = df[(df.partizione == "gid_0") & (df.sistema == "ER+seed")].set_index(["qid", "k"]).recuperati
    b = df[(df.partizione == "gid_0") & (df.sistema == "BASE+seed")].set_index(["qid", "k"]).recuperati
    assert (a == b).all()
    assert (df[df.tipo == "counting"].accuracy == 1).all()


if __name__ == "__main__":
    docs = json.loads((ROOT / "data" / "documents.json").read_text(encoding="utf-8"))
    domande = json.loads((ROOT / "data" / "questions.json").read_text(encoding="utf-8"))
    df = valuta(docs, domande, Encoder())
    controlli(df)
    (ROOT / "results").mkdir(exist_ok=True)
    df.to_csv(ROOT / "results" / "minimal_benchmark.csv", index=False)

    pd.set_option("display.width", 200)
    sel = df[(df.partizione == "gid_1") & (df.k == 3)]
    print("=== GID_1, k = 3: documenti recuperati ===")
    print(sel.pivot(index="qid", columns="sistema", values="recuperati").reindex(columns=SISTEMI).fillna("-"))
    for m in ["recall", "precision", "completezza", "accuracy"]:
        print(f"\n=== GID_1, k = 3: {m} ===")
        print(sel.pivot(index="qid", columns="sistema", values=m).reindex(columns=SISTEMI).round(2).fillna("-"))
    print("\n=== Conteggi (GID_1, k = 3): esatto vs 'alla RAG' ===")
    print(sel[sel.tipo == "counting"][["qid", "sistema", "conteggio_esatto", "conteggio_rag"]].to_string(index=False))
    for tipo in ["entity-centric", "multi-hop"]:
        t = df[df.tipo == tipo]
        for m in ["recall", "accuracy"]:
            print(f"\n=== {tipo}: {m} media, per partizione e k ===")
            print(t.pivot_table(index=["partizione", "k"], columns="sistema", values=m)
                  .reindex(columns=[s for s in SISTEMI if s in set(t.sistema)]).round(2))
    print("\nControlli superati. Salvato results/minimal_benchmark.csv")
