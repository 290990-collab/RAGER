"""Phase 2a: entity resolution computed from a registry instead of given.

Same setting as followups.py (N = 500, omega = alpha = 0.5, seeds 0..4, k in {2, 4, 8}).
  Registry    one record per local ID: name, birth year, town. The pharmacy (P) record of a shared person
              has a typo in the name (30 %), a year off by one (10 %) or another town (10 %).
  Blocking    only H-P pairs whose birth years differ by at most one are compared.
  Score       Fellegi-Sunter: sum over fields of log2(m/u) for the observed agreement level.
              m and u are counted on a separate training dataset (seed 100) where the truth is known.
  Linking     one-to-one, highest score first, while score >= t. Gives the metadata key gid_er.
  Thresholds  t* = best F1 on the training dataset; review zone [t_low, t_high] = recall >= 99 % and
              precision >= 99 % on the training dataset.
  RAG         BASE+seed, ER+seed and ER-pool with gid_er, for a grid of t, against ideal ER (true gid).
  IDs         BM25 on the typo texts of phase 1, with and without a rule that rewrites "H-37" as "H:37".
Output: results/er_real_thresholds.csv, er_real_linkage.csv, er_real_queries.csv, er_real_ids.csv
Usage: python src/er_real.py [--rapido]
"""
import re
import sys
import time
from difflib import SequenceMatcher
from pathlib import Path

import numpy as np
import pandas as pd

from followups import NOMI, COGNOMI, SISTEMI, valuta
from generator import genera, domande, controlli, FARMACI
from rag import Encoder, FUNZIONI
from robustness_text import refuso_parola, riscrivi

ROOT = Path(__file__).resolve().parent.parent
N, OMEGA, ALPHA, SEEDS, SEED_TRAIN = 500, 0.5, 0.5, [0, 1, 2, 3, 4], 100
P_NOME, P_ANNO, P_COMUNE = 0.3, 0.1, 0.1
COMUNI = ["Roma", "Milano", "Napoli", "Torino", "Palermo", "Genova", "Bologna", "Firenze", "Bari", "Catania",
          "Venezia", "Verona", "Messina", "Padova", "Trieste", "Brescia", "Parma", "Prato", "Modena", "Lecce"]
LIVELLI = {"nome": ["uguale", "simile", "diverso"], "anno": ["uguale", "vicino"], "comune": ["uguale", "diverso"]}
SISTEMI_ER = {s: (FUNZIONI[s], s != "BASE+seed") for s in ("BASE+seed", "ER+seed", "ER-pool")}
NORMA_ID = re.compile(r"\b([HP])[-\s]?(\d+)\b")


# ---------------------------------------------------------------- registry and comparison
def anagrafe(locali, coorte, rng):
    """One record per local ID. Names are drawn with replacement, so homonyms occur as in real data."""
    righe = []
    for e in range(len(coorte)):
        nome = f"{NOMI[int(rng.integers(len(NOMI)))]} {COGNOMI[int(rng.integers(len(COGNOMI)))]}"
        anno, comune = int(rng.integers(1940, 2006)), COMUNI[int(rng.integers(len(COMUNI)))]
        for src, lids in sorted(locali[e].items()):
            r = {"local_id": lids[0], "source": src, "gid": f"G{e}", "nome": nome, "anno": anno, "comune": comune}
            if src == "P" and coorte[e] == "condivisa":
                if rng.random() < P_NOME:
                    n, c = nome.split(" ", 1)
                    r["nome"] = f"{refuso_parola(n, rng)} {c}" if rng.random() < 0.5 else f"{n} {refuso_parola(c, rng)}"
                if rng.random() < P_ANNO:
                    r["anno"] = anno + (1 if rng.random() < 0.5 else -1)
                if rng.random() < P_COMUNE:
                    r["comune"] = COMUNI[(COMUNI.index(comune) + 1 + int(rng.integers(len(COMUNI) - 1))) % len(COMUNI)]
            righe.append(r)
    return pd.DataFrame(righe)


def livello_nome(a, b):
    if a == b:
        return "uguale"
    return "simile" if SequenceMatcher(None, a, b).ratio() >= 0.85 else "diverso"


def coppie(reg):
    """Blocking on birth year +/- 1, then the agreement level of each field."""
    H, P = reg[reg.source == "H"], reg[reg.source == "P"]
    per_anno = {a: g for a, g in P.groupby("anno")}
    righe = []
    for h in H.itertuples():
        for a in (h.anno - 1, h.anno, h.anno + 1):
            for p in per_anno.get(a, P.iloc[:0]).itertuples():
                righe.append({"h": h.local_id, "p": p.local_id, "vera": h.gid == p.gid,
                              "nome": livello_nome(h.nome, p.nome), "anno": "uguale" if h.anno == p.anno else "vicino",
                              "comune": "uguale" if h.comune == p.comune else "diverso"})
    return pd.DataFrame(righe)


def pesi(cp):
    """log2(m/u) per field and level, from labelled pairs, with add-one smoothing."""
    w = {}
    for campo, livelli in LIVELLI.items():
        for vera, nome in ((True, "m"), (False, "u")):
            c = cp[cp.vera == vera][campo].value_counts()
            tot = c.sum() + len(livelli)
            for l in livelli:
                w[(campo, l, nome)] = (c.get(l, 0) + 1) / tot
    return {(campo, l): float(np.log2(w[(campo, l, "m")] / w[(campo, l, "u")]))
            for campo, livelli in LIVELLI.items() for l in livelli}


def punteggi(cp, w):
    cp = cp.copy()
    cp["score"] = sum(cp[c].map(lambda l, c=c: w[(c, l)]) for c in LIVELLI)
    return cp.sort_values(["score", "h", "p"], ascending=[False, True, True]).reset_index(drop=True)


def collega(cp, t):
    """One-to-one links, highest score first. cp must be sorted by punteggi()."""
    usati_h, usati_p, link = set(), set(), []
    for r in cp[cp.score >= t].itertuples():
        if r.h not in usati_h and r.p not in usati_p:
            usati_h.add(r.h)
            usati_p.add(r.p)
            link.append((r.h, r.p, r.vera))
    return link


def qualita(link, n_vere):
    tp = sum(v for *_, v in link)
    return {"linkage_precision": tp / len(link) if link else 1.0, "linkage_recall": tp / n_vere if n_vere else 1.0,
            "n_link": len(link)}


def applica(docs, link):
    """gid_er: the H local ID names the group; linked P IDs join it, unlinked P IDs stay alone."""
    a = {p: h for h, p, _ in link}
    for d in docs:
        lid = d["metadata"]["local_id"]
        d["metadata"]["gid_er"] = "E" + a.get(lid, lid)
    return docs


def conteggio_er(docs):
    """Relative error of COUNT(DISTINCT gid_er) against COUNT(DISTINCT gid), averaged over drugs."""
    err = []
    for f in FARMACI:
        dd = [d["metadata"] for d in docs if d["metadata"]["farmaco"] == f]
        vero = len({m["gid"] for m in dd})
        err.append((len({m["gid_er"] for m in dd}) - vero) / vero)
    return float(np.mean(err))


def dataset(seed):
    docs, info, locali, coorte, compl = genera(N, OMEGA, ALPHA, seed)
    controlli(docs, info)
    qs = domande(docs, locali, coorte, compl, np.random.default_rng(1000 + seed))
    reg = anagrafe(locali, coorte, np.random.default_rng(5000 + seed))
    return docs, info, qs, reg, sum(c == "condivisa" for c in coorte)


# ---------------------------------------------------------------- thresholds from the training dataset
def soglie(cp, n_vere):
    curva = []
    for t in np.unique(cp.score):
        curva.append({"t": float(t), **qualita(collega(cp, t), n_vere)})
    c = pd.DataFrame(curva)
    c["f1"] = 2 * c.linkage_precision * c.linkage_recall / (c.linkage_precision + c.linkage_recall)
    t_star = float(c.loc[c.f1.idxmax(), "t"])
    t_basso = float(c[c.linkage_recall >= 0.99].t.max())
    t_alto = float(c[c.linkage_precision >= 0.99].t.min())
    return t_star, t_basso, t_alto


if __name__ == "__main__":
    rapido = "--rapido" in sys.argv
    seeds, suff = ([0], "_quick") if rapido else (SEEDS, "")
    t0 = time.time()

    _, _, _, reg, n_vere = dataset(SEED_TRAIN)
    cp_train = coppie(reg)
    w = pesi(cp_train)
    cp_train = punteggi(cp_train, w)
    t_star, t_basso, t_alto = soglie(cp_train, n_vere)
    print("pesi:", {f"{c}={l}": round(v, 2) for (c, l), v in w.items()})
    print(f"t* = {t_star:.2f}, zona di revisione [{t_basso:.2f}, {t_alto:.2f}]")
    griglia = sorted({round(x, 2) for x in np.arange(np.floor(cp_train.score.min()), np.ceil(cp_train.score.max()) + 1, 2)}
                     | {round(t_star, 2), round(t_basso, 2), round(t_alto, 2)})

    enc, lk, righe = Encoder(), [], []
    for seed in seeds:
        docs, info, qs, reg, n_vere = dataset(seed)
        cp = punteggi(coppie(reg), w)
        n_tutte = (reg.source == "H").sum() * (reg.source == "P").sum()
        base = {"seed": seed, "coppie_confrontate": len(cp), "riduzione_blocking": 1 - len(cp) / n_tutte,
                "recall_blocking": cp.vera.sum() / n_vere}
        zona = cp[(cp.score >= t_basso) & (cp.score < t_alto)]
        rev = collega(cp[(cp.score >= t_alto) | ((cp.score >= t_basso) & cp.vera)], t_basso)
        lk.append({**base, "t": "revisione", **qualita(rev, n_vere), "coppie_da_rivedere": len(zona),
                   "errore_conteggio": conteggio_er(applica(docs, rev))})
        for t in griglia:
            link = collega(cp, t)
            lk.append({**base, "t": t, **qualita(link, n_vere), "errore_conteggio": conteggio_er(applica(docs, link))})
            r, _, _ = valuta(docs, {**info, "er": "calcolata", "t": t}, qs, enc, SISTEMI_ER, "gid_er")
            righe += r
        r, _, _ = valuta(docs, {**info, "er": "ideale", "t": np.nan}, qs, enc, SISTEMI_ER, "gid")
        righe += r
        print(f"seed {seed}: {len(cp)} coppie dopo il blocking [{time.time() - t0:.0f}s]", flush=True)

    # ID normalization for BM25, on the typo texts of phase 1 (BM25 does not use the embedding model)
    ids = []
    bm = {s: SISTEMI["ibrido"][s] for s in ("BM25", "BM25 + ER")}
    for seed in seeds:
        docs, info, qs, _, _ = dataset(seed)
        docs, qs = riscrivi(docs, qs, "refusi", np.random.default_rng(4000 + seed))
        for norma in (False, True):
            if norma:
                docs = [{**d, "text": NORMA_ID.sub(r"\1:\2", d["text"])} for d in docs]
                qs = [{**q, "query": NORMA_ID.sub(r"\1:\2", q["query"])} for q in qs]
            r, _, _ = valuta(docs, {**info, "normalizzazione": norma}, qs, enc, bm)
            ids += r
    print(f"normalizzazione ID fatta [{time.time() - t0:.0f}s]")

    df, lk, ids = pd.DataFrame(righe), pd.DataFrame(lk), pd.DataFrame(ids)
    # Ideal ER is the reference of phase 0; without ER links the seed systems read only the local ID
    assert (df[(df.er == "ideale") & (df.sistema == "ER+seed")].accuracy == 1).all()
    assert (lk.recall_blocking == 1).all(), "blocking on year +/- 1 should keep every true pair"
    out = ROOT / "results"
    pd.DataFrame([{"t_star": t_star, "t_basso": t_basso, "t_alto": t_alto, **{f"w_{c}_{l}": v for (c, l), v in w.items()}}]
                 ).to_csv(out / f"er_real_thresholds{suff}.csv", index=False)
    lk.to_csv(out / f"er_real_linkage{suff}.csv", index=False)
    df.to_csv(out / f"er_real_queries{suff}.csv", index=False)
    ids.to_csv(out / f"er_real_ids{suff}.csv", index=False)
    pd.set_option("display.width", 200)
    print(lk.groupby("t", sort=False)[["linkage_precision", "linkage_recall", "n_link", "errore_conteggio"]]
          .mean().round(3).to_string())
    k4 = df[df.k == 4]
    print(k4.groupby(["er", "t", "tipo", "sistema"], dropna=False).accuracy.mean().unstack(["tipo", "sistema"])
          .round(3).to_string())
    print(ids[ids.k == 4].groupby(["normalizzazione", "sistema", "tipo"]).trova_paziente.mean().unstack().round(3))
    print(f"Total {time.time() - t0:.0f}s")
