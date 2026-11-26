"""Paired comparisons with 95 % bootstrap intervals and an exact McNemar test.

Each comparison pairs the same questions (same seed, k, type and question order) under two conditions.
The interval comes from 2000 resamples of the questions, stratified by seed.
Output: results/significance.csv and the "S" section of results/tables.md (via analysis.py).
Usage: python src/stats.py
"""
import sys
from pathlib import Path

import numpy as np
import pandas as pd
from scipy.stats import binomtest

ROOT = Path(__file__).resolve().parent.parent
R = ROOT / "results"
B, RNG = 2000, np.random.default_rng(4242)


def con_indice(df, chiavi):
    df = df.copy()
    df["q"] = df.groupby(chiavi + ["seed", "k", "tipo", "sistema"]).cumcount()
    return df


def confronta(df, a, b, metrica="accuracy"):
    """a, b: dicts of column filters. Returns mean difference b - a, 95 % CI, McNemar p and verdict."""
    def sel(f):
        m = np.ones(len(df), bool)
        for c, v in f.items():
            m &= (df[c] == v).to_numpy()
        return df[m].set_index(["seed", "k", "tipo", "q"])[metrica]
    xa, xb = sel(a), sel(b)
    xa, xb = xa.align(xb, join="inner")
    assert len(xa) > 0, (a, b)
    d = (xb - xa).to_numpy()
    seeds = xa.index.get_level_values("seed").to_numpy()
    gruppi = [np.flatnonzero(seeds == s) for s in np.unique(seeds)]
    boot = np.empty(B)
    for i in range(B):
        idx = np.concatenate([g[RNG.integers(len(g), size=len(g))] for g in gruppi])
        boot[i] = d[idx].mean()
    lo, hi = np.percentile(boot, [2.5, 97.5])
    vince_b, vince_a = int((d > 0).sum()), int((d < 0).sum())
    p = binomtest(vince_b, vince_b + vince_a, 0.5).pvalue if vince_a + vince_b else 1.0
    reale = (lo > 0 or hi < 0) and p < 0.05
    return {"n_coppie": len(d), "media_a": xa.mean(), "media_b": xb.mean(), "differenza": d.mean(),
            "ic95_basso": lo, "ic95_alto": hi, "b_meglio": vince_b, "a_meglio": vince_a, "p_mcnemar": p,
            "esito": "reale" if reale else "non distinguibile"}


def main():
    ex = pd.read_csv(R / "experiment_queries.csv")
    ex = con_indice(ex[(ex.k == 4) & (ex.omega > 0)], ["N", "omega", "alpha"])
    es = con_indice(pd.read_csv(R / "extension_queries.csv"), ["studio", "x", "y"])
    fu = con_indice(pd.read_csv(R / "followup_queries.csv"), ["studio", "x", "er"])

    confronti = []
    for alpha in (0, 0.5, 1):
        confronti.append(("Griglia, k = 4", f"multi-source, alpha = {alpha}: BASE+seed → ER+seed",
                          ex[ex.alpha == alpha], dict(sistema="BASE+seed", tipo="multi-source"),
                          dict(sistema="ER+seed", tipo="multi-source"), "accuracy", ["N", "omega"]))
    for tipo in ("single-source", "multi-source"):
        confronti.append(("Griglia, k = 4", f"{tipo}: BASE → ER-pool", ex, dict(sistema="BASE", tipo=tipo),
                          dict(sistema="ER-pool", tipo=tipo), "accuracy", ["N", "omega", "alpha"]))
        confronti.append(("Griglia, k = 4", f"{tipo}: ER-pool → ER+seed", ex, dict(sistema="ER-pool", tipo=tipo),
                          dict(sistema="ER+seed", tipo=tipo), "accuracy", ["N", "omega", "alpha"]))
    f4 = es[(es.studio == "falsi") & (es.k == 4) & (es.sistema == "ER+seed")]
    for tipo, x, y, nome in [("single-source", 0, 0.25, "25 % falsi positivi"),
                             ("multi-source", 0.25, 0, "25 % falsi negativi"),
                             ("multi-source", 0.5, 0, "50 % falsi negativi")]:
        confronti.append(("Falsi match, ER+seed, k = 4", f"{tipo}: ER corretta → {nome}", f4,
                          dict(x=0, y=0, tipo=tipo), dict(x=x, y=y, tipo=tipo), "accuracy", []))
    d2 = es[(es.studio == "duplicati") & (es.k == 2) & (es.sistema == "ER+seed")]
    confronti.append(("Quasi-duplicati, ER+seed, k = 2", "multi-source: nessun doppione → 50 % doppioni", d2,
                      dict(x=0, tipo="multi-source"), dict(x=0.5, tipo="multi-source"), "completezza", []))
    om = fu[(fu.studio == "omonimi") & (fu.k == 4) & (fu.sistema == "ER+seed") & (fu.x == 0.25)]
    for tipo in ("single-source", "multi-source"):
        confronti.append(("Omonimi 25 %, ER+seed, k = 4", f"{tipo}: ER ideale → ER per nome", om,
                          dict(er="ideal", tipo=tipo), dict(er="names", tipo=tipo), "accuracy", []))
    ind = fu[(fu.studio == "indici") & (fu.k == 4)]
    for tipo in ("single-source", "multi-source"):
        for a, b in [("BASE", "BASE split, merged"), ("BASE", "BASE split, k/2 each"),
                     ("ER-pool", "ER-pool split, k/2 each")]:
            confronti.append(("Indice per fonte, k = 4", f"{tipo}: {a} → {b}", ind, dict(sistema=a, tipo=tipo),
                              dict(sistema=b, tipo=tipo), "accuracy", []))
    dv = fu[(fu.studio == "diversita") & (fu.k == 2) & (fu.x == 0.5)]
    for tipo in ("single-source", "multi-source"):
        for b in ("ER+seed, source variety", "ER+seed, MMR"):
            confronti.append(("Doppioni 50 %, k = 2", f"{tipo}: ER+seed → {b}", dv, dict(sistema="ER+seed", tipo=tipo),
                              dict(sistema=b, tipo=tipo), "completezza", []))
    ib = fu[(fu.studio == "ibrido") & (fu.k == 4)]
    for tipo in ("single-source", "multi-source"):
        for a, b in [("BASE", "BM25"), ("BM25", "BM25 + ER"), ("BM25 + ER", "ER+seed"), ("BM25", "Hybrid"),
                     ("Hybrid", "Hybrid + ER")]:
            confronti.append(("Ricerca per parole e ibrida, k = 4", f"{tipo}: {a} → {b}", ib,
                              dict(sistema=a, tipo=tipo), dict(sistema=b, tipo=tipo), "accuracy", []))

    rt = R / "robustness_text_queries.csv"
    if rt.exists():
        tq = pd.read_csv(rt)
        tq = con_indice(tq[tq.k == 4], ["modello", "condizione"])
        g = "Testi variati e secondo embedding, k = 4"
        for tipo in ("single-source", "multi-source"):
            confronti.append((g, f"{tipo}, testo fisso, semantica: MiniLM → E5-small", tq,
                              dict(sistema="BASE", modello="MiniLM", condizione="fisso", tipo=tipo),
                              dict(sistema="BASE", modello="E5-small", condizione="fisso", tipo=tipo),
                              "trova_paziente", []))
        for modello in ("MiniLM", "E5-small"):
            for a, b in (("fisso", "variato"), ("variato", "nome")):
                confronti.append((g, f"multi-source, semantica {modello}: testo {a} → {b}", tq,
                                  dict(sistema="BASE", modello=modello, condizione=a, tipo="multi-source"),
                                  dict(sistema="BASE", modello=modello, condizione=b, tipo="multi-source"),
                                  "trova_paziente", []))
        confronti.append((g, "multi-source, BM25: testo variato → refusi", tq,
                          dict(sistema="BM25", modello="MiniLM", condizione="variato", tipo="multi-source"),
                          dict(sistema="BM25", modello="MiniLM", condizione="refusi", tipo="multi-source"),
                          "trova_paziente", []))
        for modello in ("MiniLM", "E5-small"):
            confronti.append((g, f"multi-source, refusi, {modello}: BM25 → Hybrid", tq,
                              dict(sistema="BM25", modello=modello, condizione="refusi", tipo="multi-source"),
                              dict(sistema="Hybrid", modello=modello, condizione="refusi", tipo="multi-source"),
                              "trova_paziente", []))
        confronti.append((g, "multi-source, testo fisso, ER-pool: MiniLM → E5-small", tq,
                          dict(sistema="ER-pool", modello="MiniLM", condizione="fisso", tipo="multi-source"),
                          dict(sistema="ER-pool", modello="E5-small", condizione="fisso", tipo="multi-source"),
                          "accuracy", []))

    er = R / "er_real_queries.csv"
    if er.exists():
        s = pd.read_csv(R / "er_real_thresholds.csv").iloc[0]
        eq = pd.read_csv(er)
        eq = con_indice(eq[(eq.k == 4) & (eq.sistema == "ER+seed")].assign(t=lambda d: d.t.fillna(-999)), ["er", "t"])
        g = "ER calcolata dall'anagrafe, ER+seed, k = 4"
        for tipo, t, nome in [("single-source", round(s.t_star, 2), "t* (scelta)"),
                              ("multi-source", round(s.t_star, 2), "t* (scelta)"),
                              ("single-source", -8.0, "t = -8 (bassa)"),
                              ("multi-source", 12.0, "t = 12 (alta)")]:
            confronti.append((g, f"{tipo}: ER ideale → {nome}", eq, dict(t=-999, tipo=tipo), dict(t=t, tipo=tipo),
                              "accuracy", []))
        ni = con_indice(pd.read_csv(R / "er_real_ids.csv").query("k == 4"), ["normalizzazione"])
        confronti.append((g.replace("ER+seed", "BM25"), "multi-source, testi con refusi: ID così come sono → normalizzati",
                          ni, dict(sistema="BM25", normalizzazione=False, tipo="multi-source"),
                          dict(sistema="BM25", normalizzazione=True, tipo="multi-source"), "trova_paziente", []))

    righe = []
    for gruppo, nome, df, a, b, metrica, extra in confronti:
        if extra:
            df = df.copy()
            df["seed"] = df["seed"].astype(str) + "|" + df[extra].astype(str).agg("|".join, axis=1)
        r = confronta(df, a, b, metrica)
        righe.append({"gruppo": gruppo, "confronto": nome, "metrica": metrica, **r})
    out = pd.DataFrame(righe)
    out.to_csv(R / "significance.csv", index=False)
    sys.stdout.reconfigure(encoding="utf-8")
    pd.set_option("display.width", 220)
    print(out[["gruppo", "confronto", "media_a", "media_b", "differenza", "ic95_basso", "ic95_alto",
               "p_mcnemar", "esito"]].round(3).to_string())


if __name__ == "__main__":
    main()
