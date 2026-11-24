"""Grafici aggregati con intervalli di variabilita' (traccia Sez. 13).

Barre di errore = deviazione standard fra i 5 seed (media prima sulle query di ogni seed).
Colori: palette categoriale validata (slot fissi per sistema); marcatori diversi come seconda codifica.
I valori numerici corrispondenti sono in results/tables.md.
Output: results/plots/*.png
"""
from pathlib import Path

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import pandas as pd

ROOT = Path(__file__).resolve().parent.parent
R, OUT = ROOT / "results", ROOT / "results" / "plots"
COLORE = {"BASE": "#2a78d6", "BASE+seed": "#eb6834", "ER+seed": "#1baf7a", "ER-pool": "#eda100", "ORACLE": "#e87ba4"}
MARK = {"BASE": "o", "BASE+seed": "s", "ER+seed": "^", "ER-pool": "D", "ORACLE": "v"}
SERIE = ["#2a78d6", "#eb6834", "#1baf7a", "#eda100"]          # per serie non legate ai sistemi
MARK_S = ["o", "s", "^", "D"]

plt.rcParams.update({"figure.facecolor": "#fcfcfb", "axes.facecolor": "#fcfcfb", "axes.edgecolor": "#c3c2b7",
                     "axes.labelcolor": "#52514e", "xtick.color": "#52514e", "ytick.color": "#52514e",
                     "text.color": "#0b0b0b", "axes.grid": True, "grid.color": "#e6e5e0", "grid.linewidth": 0.6,
                     "axes.spines.top": False, "axes.spines.right": False, "font.size": 10, "lines.linewidth": 2,
                     "lines.markersize": 7, "legend.frameon": False})


def media_std(df, x, gruppo, metrica):
    s = df.groupby([gruppo, x, "seed"])[metrica].mean()
    return s.groupby([gruppo, x]).agg(["mean", "std"]).reset_index()


def linee(ax, t, x, gruppo, ordine, colori, marcatori, fmt=str):
    for i, g in enumerate(ordine):
        d = t[t[gruppo] == g]
        if d.empty:
            continue
        c = colori[g] if isinstance(colori, dict) else colori[i]
        m = marcatori[g] if isinstance(marcatori, dict) else marcatori[i]
        # ORACLE tratteggiato: spesso coincide con ER+seed (accuracy 1) e lo coprirebbe
        ax.errorbar(d[x], d["mean"], yerr=d["std"].fillna(0), color=c, marker=m, capsize=3,
                    markeredgecolor="#fcfcfb", markeredgewidth=1.5, label=fmt(g),
                    linestyle="--" if g == "ORACLE" else "-", zorder=3 if g == "ORACLE" else 2)


def salva(fig, nome, titolo):
    fig.suptitle(titolo, x=0.02, ha="left", fontsize=11)
    fig.tight_layout()
    fig.savefig(OUT / nome, dpi=150)
    plt.close(fig)


def main():
    OUT.mkdir(parents=True, exist_ok=True)
    q = pd.read_csv(R / "experiment_queries.csv")
    e = pd.read_csv(R / "extension_queries.csv")
    c = pd.read_csv(R / "experiment_counts.csv")
    sist = list(COLORE)

    # G1 (H1, H2): accuracy multi-source al variare di alpha
    m = q[(q.k == 4) & (q.omega > 0) & (q.tipo == "multi-source")]
    fig, ax = plt.subplots(figsize=(6.4, 4))
    linee(ax, media_std(m, "alpha", "sistema", "accuracy"), "alpha", "sistema", sist, COLORE, MARK)
    ax.set(xlabel="α (quota di entità condivise con evidenze complementari)", ylabel="Answer accuracy",
           ylim=(-0.05, 1.05), xticks=[0, 0.5, 1])
    ax.legend(loc="center left", bbox_to_anchor=(1, 0.5))
    salva(fig, "G1_accuracy_alpha.png", "H1–H2: query multi-source, k = 4, ω > 0")

    # G2 (H4): guadagno del linkage per omega, una linea per alpha
    a = m[m.sistema == "ER+seed"].groupby(["alpha", "omega", "seed"]).accuracy.mean()
    b = m[m.sistema == "BASE+seed"].groupby(["alpha", "omega", "seed"]).accuracy.mean()
    g = (a - b).groupby(["alpha", "omega"]).agg(["mean", "std"]).reset_index()
    fig, ax = plt.subplots(figsize=(6.4, 4))
    linee(ax, g, "omega", "alpha", [0, 0.5, 1], SERIE, MARK_S, fmt=lambda v: f"α = {v}")
    ax.set(xlabel="ω (sovrapposizione delle identità)", ylabel="accuracy(ER+seed) − accuracy(BASE+seed)",
           ylim=(-0.05, 1.05), xticks=[0.25, 0.5, 0.75])
    ax.legend(loc="center left", bbox_to_anchor=(1, 0.5))
    salva(fig, "G2_gain_omega.png", "H4: il guadagno per query dipende da α, non da ω (k = 4)")

    # G3 (H3): completezza di ER+seed al variare di k con quasi-duplicati
    d = e[(e.studio == "duplicati") & (e.tipo == "multi-source") & (e.sistema == "ER+seed")]
    fig, ax = plt.subplots(figsize=(6.4, 4))
    linee(ax, media_std(d, "k", "x", "completezza"), "k", "x", [0, 0.25, 0.5], SERIE, MARK_S,
          fmt=lambda v: f"ε = {v}")
    ax.set(xlabel="budget k (documenti)", ylabel="Completezza delle evidenze", ylim=(0.5, 1.05), xticks=[2, 4, 8])
    ax.legend(loc="center left", bbox_to_anchor=(1, 0.5))
    salva(fig, "G3_duplicates_budget.png", "H3: i quasi-duplicati consumano il budget (ER+seed, multi-source)")

    # G4: disambiguazione di BASE per N e k
    b = q[q.sistema == "BASE"]
    fig, ax = plt.subplots(figsize=(6.4, 4))
    linee(ax, media_std(b, "k", "N", "disambiguazione"), "k", "N", [100, 500, 1000], SERIE, MARK_S,
          fmt=lambda v: f"N = {v}")
    ax.set(xlabel="budget k (documenti)", ylabel="Quota di query con l'entità nei top-k", ylim=(0, 1),
           xticks=[2, 4, 8])
    ax.legend(loc="center left", bbox_to_anchor=(1, 0.5))
    salva(fig, "G4_disambiguation.png", "Disambiguazione: il retriever denso non riconosce gli ID locali")

    # G5: conteggi, errore relativo per omega
    c8 = c[(c.k == 8) & (c.sistema == "BASE")].copy()
    c8["somma_locale"] = (c8.somma_locale - c8.esatto) / c8.esatto
    c8["conteggio sul contesto"] = (c8.rag - c8.esatto).abs() / c8.esatto
    t = c8.groupby("omega")[["somma_locale", "conteggio sul contesto"]].mean()
    t["γ − 1 sul totale"] = [2 / (2 - w) - 1 for w in t.index]
    fig, ax = plt.subplots(figsize=(9, 4))
    for i, col in enumerate(["somma_locale", "γ − 1 sul totale", "conteggio sul contesto"]):
        ax.plot(t.index, t[col], color=SERIE[i], marker=MARK_S[i], markeredgecolor="#fcfcfb",
                label={"somma_locale": "somma dei conteggi locali (per farmaco)"}.get(col, col))
    ax.set(xlabel="ω", ylabel="Errore relativo rispetto a COUNT(DISTINCT gid)", ylim=(0, 1.05),
           xticks=[0, 0.25, 0.5, 0.75])
    ax.legend(loc="center left", bbox_to_anchor=(1, 0.5))
    salva(fig, "G5_counts.png", "Conteggi: γ dipende dalla cella; il conteggio via RAG non è affidabile (k = 8)")

    # G6: falsi match (ER+seed) - falsi positivi su single-source, falsi negativi su multi-source
    f = e[(e.studio == "falsi") & (e.k == 4)]
    fig, (a1, a2) = plt.subplots(1, 2, figsize=(9, 3.8), sharey=True)
    for ax, tipo, x, fisso, lab in [(a1, "single-source", "y", "x", "quota di falsi positivi"),
                                    (a2, "multi-source", "x", "y", "quota di falsi negativi")]:
        s = f[(f.tipo == tipo) & (f[fisso] == 0)]
        linee(ax, media_std(s, x, "sistema", "accuracy"), x, "sistema", ["BASE+seed", "ER+seed"], COLORE, MARK)
        ax.set(xlabel=lab, title=f"query {tipo}", ylim=(0.4, 1.05))
    a1.set_ylabel("Answer accuracy")
    a2.legend(loc="center left", bbox_to_anchor=(1, 0.5))
    salva(fig, "G6_false_matches.png", "Falsi match del linkage (k = 4, N = 500, ω = 0,5, α = 0,5)")
    print("Grafici salvati in", OUT)


if __name__ == "__main__":
    main()
