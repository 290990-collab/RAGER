"""Summary tables (hypotheses H1-H4, counting, robustness) written to results/tables.md.

Values are mean ± std over 5 seeds of the per-seed query means.
"""
from pathlib import Path

import pandas as pd

ROOT = Path(__file__).resolve().parent.parent
R = ROOT / "results"
SIST = ["BASE", "BASE+seed", "ER+seed", "ER-pool", "ORACLE"]


def md(t):
    """DataFrame or Series as a Markdown table."""
    t = t.to_frame() if isinstance(t, pd.Series) else t
    idx = [str(n) for n in t.index.names]
    cols = [" ".join(map(str, c)) if isinstance(c, tuple) else str(c) for c in t.columns]
    righe = ["| " + " | ".join(idx + cols) + " |", "|" + "---|" * (len(idx) + len(cols))]
    for i, r in zip(t.index, t.itertuples(index=False)):
        i = i if isinstance(i, tuple) else (i,)
        righe.append("| " + " | ".join(map(str, list(i) + list(r))) + " |")
    return "\n".join(righe)


def ms(serie_per_seed, chiavi):
    """Mean ± std over seeds."""
    g = serie_per_seed.groupby(chiavi)
    return g.mean().round(2).astype(str) + " ± " + g.std().fillna(0).round(2).astype(str)


def per_seed(df, chiavi, metrica):
    return df.groupby(chiavi + ["seed"])[metrica].mean()


def tab(serie, colonne):
    t = serie.unstack(colonne)
    if colonne == "sistema":
        t = t.reindex(columns=[s for s in SIST if s in t.columns])
    return md(t)


def main():
    out = []
    q = pd.read_csv(R / "experiment_queries.csv")
    c = pd.read_csv(R / "experiment_counts.csv")
    k4 = q[q.k == 4]
    x = k4[k4.omega > 0]
    m = x[x.tipo == "multi-source"]

    out.append("# Tabelle dei risultati\n\nValori: media ± deviazione standard fra 5 seed. "
               "Accuracy = lettore deterministico senza LLM.\n")

    out.append("## T1 (H1) - Accuracy per tipo di query e sistema, k = 4, omega > 0\n")
    out.append(tab(ms(per_seed(x, ["tipo", "sistema"], "accuracy"), ["tipo", "sistema"]), "sistema"))
    out.append("\n## T2 (H1) - Recall@k per tipo di query e sistema, k = 4, omega > 0\n")
    out.append(tab(ms(per_seed(x, ["tipo", "sistema"], "recall"), ["tipo", "sistema"]), "sistema"))

    out.append("\n## T3 (H2) - Query multi-source: accuracy per alpha (complementarità), k = 4, omega > 0\n")
    out.append(tab(ms(per_seed(m, ["alpha", "sistema"], "accuracy"), ["alpha", "sistema"]), "sistema"))

    out.append("\n## T4 (H2, H4) - Guadagno del linkage = accuracy(ER+seed) - accuracy(BASE+seed), "
               "query multi-source, k = 4\n")
    a = per_seed(m[m.sistema == "ER+seed"], ["omega", "alpha"], "accuracy")
    b = per_seed(m[m.sistema == "BASE+seed"], ["omega", "alpha"], "accuracy")
    out.append(tab(ms(a - b, ["omega", "alpha"]), "alpha"))

    out.append("\n## T5 (H4) - Guadagno di ER-pool su BASE (accuracy), per omega e tipo, k = 4\n")
    a = per_seed(k4[k4.sistema == "ER-pool"], ["omega", "tipo"], "accuracy")
    b = per_seed(k4[k4.sistema == "BASE"], ["omega", "tipo"], "accuracy")
    out.append(tab(ms(a - b, ["omega", "tipo"]), "tipo"))

    out.append("\n## T6 (H3) - Budget k: accuracy, precision e costo (token) per sistema, query multi-source\n")
    mm = q[q.tipo == "multi-source"]
    for met in ["accuracy", "precision", "n_token"]:
        out.append(f"\n**{met}**\n")
        out.append(tab(ms(per_seed(mm, ["k", "sistema"], met), ["k", "sistema"]), "sistema"))

    out.append("\n## T7 - Disambiguazione (Sez. 12): quota di query in cui i top-k di BASE contengono "
               "l'entità del seed\n")
    d = q[q.sistema == "BASE"]
    out.append(tab(ms(per_seed(d, ["N", "k"], "disambiguazione"), ["N", "k"]), "k"))

    out.append("\n## T8 - Conteggi: errore relativo medio rispetto a COUNT(DISTINCT gid), k = 8\n")
    c8 = c[(c.k == 8) & (c.sistema == "BASE")].copy()
    c8["err_somma_locale"] = (c8.somma_locale - c8.esatto) / c8.esatto
    c8["err_rag"] = (c8.rag - c8.esatto).abs() / c8.esatto
    t = c8.groupby(["N", "omega"])[["err_somma_locale", "err_rag"]].mean().round(3)
    t["gamma_teorico - 1"] = [round(2 * n / (2 * n - round(w * n)) - 1, 3) for n, w in t.index]
    out.append(md(t))

    e = R / "extension_queries.csv"
    if e.exists():
        e4 = pd.read_csv(e)
        e4 = e4[e4.k == 4]
        for studio, titolo in [("dirty", "Dirty ER, delta = D/N"), ("duplicati", "Quasi-duplicati, quota eps"),
                               ("errori_id", "Errori sugli ID nel testo, quota eps")]:
            s = e4[e4.studio == studio]
            for tipo in ["single-source", "multi-source"]:
                out.append(f"\n## E - {titolo}: accuracy, query {tipo}, k = 4\n")
                out.append(tab(ms(per_seed(s[s.tipo == tipo], ["x", "sistema"], "accuracy"), ["x", "sistema"]),
                               "sistema"))
        f = e4[e4.studio == "falsi"]
        out.append("\n## E - Falsi match: qualità del linkage e accuracy, k = 4 "
                   "(x = quota falsi negativi, y = quota falsi positivi)\n")
        lk = f.groupby(["x", "y"])[["linkage_precision", "linkage_recall"]].mean().round(3)
        for s, tipo in [("ER+seed", "single-source"), ("ER+seed", "multi-source"), ("BASE+seed", "multi-source")]:
            lk[f"{s} {tipo}"] = ms(per_seed(f[(f.sistema == s) & (f.tipo == tipo)], ["x", "y"], "accuracy"),
                                   ["x", "y"])
        out.append(md(lk))

    fu = R / "followup_queries.csv"
    if fu.exists():
        fq = pd.read_csv(fu)

        def blocco(studio, titolo, metrica, ordine, k=None, chiavi=("x",)):
            s = fq[fq.studio == studio] if k is None else fq[(fq.studio == studio) & (fq.k == k)]
            for tipo in ["single-source", "multi-source"]:
                t = ms(per_seed(s[s.tipo == tipo], list(chiavi) + ["sistema"], metrica), list(chiavi) + ["sistema"])
                t = t.unstack("sistema").reindex(columns=[c for c in ordine if c in set(s.sistema)])
                out.append(f"\n## F - {titolo}: {metrica}, query {tipo}\n")
                out.append(md(t))

        blocco("omonimi", "Omonimi (x = quota di persone con un omonimo), k = 4; ER ideale vs ER per nome",
               "accuracy", ["BASE", "BASE+seed", "ER+seed", "ER-pool"], k=4, chiavi=("x", "er"))
        blocco("indici", "Un indice per fonte, k = 4", "accuracy",
               ["BASE", "BASE split, merged", "BASE split, k/2 each", "ER-pool", "ER-pool split, k/2 each"], k=4)
        blocco("diversita", "Quasi-duplicati e reranking con varietà, k = 2 (x = quota eps)", "completezza",
               ["BASE+seed", "ER+seed", "ER+seed, source variety", "ER+seed, MMR"], k=2)
        ib = ["BASE", "BM25", "BM25 + ER", "Hybrid", "Hybrid + ER", "ER+seed"]
        blocco("ibrido", "Retriever lessicale e ibrido, per k", "accuracy", ib, chiavi=("k",))
        blocco("ibrido", "Retriever lessicale e ibrido, per k", "trova_paziente", ib, chiavi=("k",))

    (R / "tables.md").write_text("\n".join(out) + "\n", encoding="utf-8")
    print("\n".join(out))


if __name__ == "__main__":
    main()
