"""Minimal-example questions, with ground truth from the GID metadata for each partition GID_0..GID_3."""
import json
from pathlib import Path

from dataset import PARTIZIONI

DATA = Path(__file__).resolve().parent.parent / "data"


def entity_centric(docs, p, seed):
    """Documents of the seed's entity."""
    gid = next(d["metadata"][p] for d in docs if d["metadata"]["local_id"] == seed)
    gold = [d for d in docs if d["metadata"][p] == gid]
    return {"gold_docs": [d["doc_id"] for d in gold],
            "risposta": sorted({d["metadata"]["farmaco"] for d in gold})}


def multi_hop(docs, p, f1, f2):
    """Entities with drug f1 and drug f2 in different sources."""
    entita, gold = [], []
    for g in sorted({d["metadata"][p] for d in docs}):
        ev = [d for d in docs if d["metadata"][p] == g and d["metadata"]["farmaco"] in (f1, f2)]
        s1 = {d["metadata"]["source"] for d in ev if d["metadata"]["farmaco"] == f1}
        s2 = {d["metadata"]["source"] for d in ev if d["metadata"]["farmaco"] == f2}
        if any(a != b for a in s1 for b in s2):
            entita.append(g)
            gold += [d["doc_id"] for d in ev]
    return {"gold_docs": gold, "risposta": entita}


def counting(docs, p, farmaco):
    """COUNT(DISTINCT gid) over the drug's documents."""
    gold = [d for d in docs if d["metadata"]["farmaco"] == farmaco]
    return {"gold_docs": [d["doc_id"] for d in gold],
            "risposta": len({d["metadata"][p] for d in gold}),
            "record_locali": len({d["metadata"]["local_id"] for d in gold})}


def negativa(docs, p, farmaco):
    return {"gold_docs": [], "risposta": []}


# (id, type, query, seed, function, arguments)
DOMANDE = [
    ("Q1", "entity-centric", "Quali farmaci risultano per H:3 in tutte le sorgenti?", "H:3", entity_centric, ("H:3",)),
    ("Q2", "entity-centric", "Quali farmaci risultano per P:2 in tutte le sorgenti?", "P:2", entity_centric, ("P:2",)),
    ("Q3", "entity-centric", "Quali farmaci risultano per H:2 in tutte le sorgenti?", "H:2", entity_centric, ("H:2",)),
    ("Q4", "multi-hop", "Chi ha eventi di Insulina e Aspirina su fonti distinte?", None, multi_hop, ("Insulina", "Aspirina")),
    ("Q5a", "counting", "Quanti pazienti distinti hanno eventi di Metformina?", None, counting, ("Metformina",)),
    ("Q5b", "counting", "Quanti pazienti distinti hanno eventi di Insulina?", None, counting, ("Insulina",)),
    ("Q5c", "counting", "Quanti pazienti distinti hanno eventi di Aspirina?", None, counting, ("Aspirina",)),
    ("Q6", "negativa", "Quali pazienti ricevono Paracetamolo?", None, negativa, ("Paracetamolo",)),
]


def costruisci(docs):
    out = []
    for qid, tipo, testo, seed, fn, args in DOMANDE:
        gt = {p: fn(docs, p, *args) for p in PARTIZIONI}
        out.append({"qid": qid, "tipo": tipo, "query": testo, "seed": seed, "ground_truth": gt})
    return out


def controlli(dom):
    """Checks against values derived by hand from the paper."""
    gt = {q["qid"]: q["ground_truth"] for q in dom}
    assert gt["Q1"]["gid_1"] == {"gold_docs": ["d3", "d4", "d5"], "risposta": ["Aspirina", "Insulina"]}
    assert gt["Q2"]["gid_1"]["gold_docs"] == ["d6"]
    assert gt["Q3"]["gid_1"] == {"gold_docs": ["d2", "d7"], "risposta": ["Metformina"]}
    assert gt["Q4"]["gid_1"]["risposta"] == ["HP3"]
    for q, persone, schede in (("Q5a", 2, 3), ("Q5b", 2, 3), ("Q5c", 2, 2)):
        assert gt[q]["gid_1"]["risposta"] == persone and gt[q]["gid_1"]["record_locali"] == schede
    for q in ("Q5a", "Q5b", "Q5c"):
        assert gt[q]["gid_0"]["risposta"] == gt[q]["gid_0"]["record_locali"]
    assert gt["Q4"]["gid_0"]["risposta"] == []
    assert gt["Q1"]["gid_0"]["risposta"] == ["Insulina"]
    assert all(gt["Q6"][p]["gold_docs"] == [] for p in PARTIZIONI)


if __name__ == "__main__":
    docs = json.loads((DATA / "documents.json").read_text(encoding="utf-8"))
    dom = costruisci(docs)
    controlli(dom)
    (DATA / "questions.json").write_text(json.dumps(dom, ensure_ascii=False, indent=2), encoding="utf-8")

    for q in dom:
        print(f"\n{q['qid']} [{q['tipo']}] {q['query']}")
        for p in PARTIZIONI:
            g = q["ground_truth"][p]
            print(f"   {p}: risposta={g['risposta']}  documenti={g['gold_docs']}")
    print("\nTutti i controlli superati. Salvato in questions.json")
