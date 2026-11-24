"""Passo A2 - Dataset minimo di documenti (Paper, tabella 4; traccia Sez. 4).

Ogni riga della tabella 4 del paper e' un evento farmacologico e diventa un documento.
Tre identificativi distinti:
  - doc_id   = il documento (un evento)
  - local_id = la persona nella sua sorgente (es. "P:1")
  - gid_*    = l'entita' globale sotto una delle quattro ipotesi di ER (solo nei metadati)
"""
import json
from pathlib import Path

# Paper, tabella 4: (sito, person_id, farmaco, quantita, GID_0, GID_1, GID_2, GID_3, anno, luogo)
EVENTI = [
    ("H", "H:1", "Metformina", 30,  "H1", "H1",  "HP1", "HP13", 1980, "Modena"),
    ("H", "H:2", "Metformina", 30,  "H2", "HP2", "HP2", "HP2",  1950, "Bologna"),
    ("H", "H:3", "Insulina",   20,  "H3", "HP3", "HP3", "HP13", 1980, "Modena"),
    ("P", "P:1", "Aspirina",   100, "P1", "HP3", "HP3", "HP13", 1980, None),
    ("P", "P:1", "Insulina",   15,  "P1", "HP3", "HP3", "HP13", 1980, None),
    ("P", "P:2", "Aspirina",   50,  "P2", "P2",  "HP1", "P2",   1980, None),
    ("P", "P:3", "Metformina", 60,  "P3", "HP2", "HP2", "HP2",  1950, None),
    ("P", "P:4", "Insulina",   10,  "P4", "P4",  "P4",  "HP2",  1950, None),
]
PARTIZIONI = ["gid_0", "gid_1", "gid_2", "gid_3"]


def costruisci_documenti():
    docs = []
    for i, (src, lid, farm, q, g0, g1, g2, g3, anno, luogo) in enumerate(EVENTI, start=1):
        docs.append({
            "doc_id": f"d{i}",
            # Template del codice della traccia (Sez. 4): solo local_id, farmaco e quantita.
            "text": f"{lid} ha ricevuto {farm}, quantità {q}.",
            "metadata": {
                "source": src, "local_id": lid, "farmaco": farm, "quantita": q,
                "gid_0": g0, "gid_1": g1, "gid_2": g2, "gid_3": g3,
                "year_of_birth": anno, "location_id": luogo,
            },
        })
    return docs


def controlli(docs):
    """Verifiche automatiche contro i numeri del paper (Paper 2.2-2.4)."""
    assert len(docs) == 8, "8 eventi"
    identita_locali = {(d["metadata"]["source"], d["metadata"]["local_id"]) for d in docs}
    assert len(identita_locali) == 7, "7 schede: 3 in H, 4 in P (P:1 ha due eventi)"
    attese = {"gid_0": 7, "gid_1": 5, "gid_2": 4, "gid_3": 3}
    for p, v in attese.items():
        assert len({d["metadata"][p] for d in docs}) == v, f"{p}: attese {v} entita'"
    # Il GID non compare mai nel testo (regola del progetto).
    for d in docs:
        for p in PARTIZIONI:
            assert d["metadata"][p] not in d["text"].split(), f"GID nel testo di {d['doc_id']}"
    # Dentro ogni entita' gli attributi concordano (Paper 2.3: nessuna scelta di Data Fusion).
    for p in PARTIZIONI:
        anni = {}
        for d in docs:
            anni.setdefault(d["metadata"][p], set()).add(d["metadata"]["year_of_birth"])
        assert all(len(s) == 1 for s in anni.values()), f"{p}: anni discordi nella stessa entita'"


if __name__ == "__main__":
    docs = costruisci_documenti()
    controlli(docs)
    out = Path(__file__).resolve().parent.parent / "data" / "documents.json"
    out.parent.mkdir(exist_ok=True)
    out.write_text(json.dumps(docs, ensure_ascii=False, indent=2), encoding="utf-8")
    # Copia CSV (Sez. 13: dataset JSON/CSV)
    import csv
    with open(out.with_suffix(".csv"), "w", newline="", encoding="utf-8-sig") as f:  # BOM: Excel legge le lettere accentate
        w = csv.writer(f)
        w.writerow(["doc_id", "text"] + list(docs[0]["metadata"]))
        for d in docs:
            w.writerow([d["doc_id"], d["text"]] + list(d["metadata"].values()))

    print(f"{'doc':4} {'src':3} {'local':5} {'g0':3} {'g1':4} {'g2':4} {'g3':5} testo")
    for d in docs:
        m = d["metadata"]
        print(f"{d['doc_id']:4} {m['source']:3} {m['local_id']:5} {m['gid_0']:3} "
              f"{m['gid_1']:4} {m['gid_2']:4} {m['gid_3']:5} {d['text']}")
    for p in PARTIZIONI:
        print(f"{p}: {len({d['metadata'][p] for d in docs})} entità")
    print(f"Tutti i controlli superati. Salvato in {out.name}")
