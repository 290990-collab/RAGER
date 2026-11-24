"""Grafici aggregati con intervalli di variabilita' (traccia Sez. 13).

Fascia colorata = media +/- deviazione standard fra i 5 seed (media prima sulle query di ogni seed).
Colori: palette categoriale validata (slot fissi per sistema); marcatori e tratteggi come seconda codifica.
Titolo = il risultato che il grafico mostra; sottotitolo = le condizioni dell'esperimento.
I valori numerici corrispondenti sono in results/tables.md.
Output: results/plots/*.png (italiano, per la relazione) e results/plots/en/*.png (inglese, per il README).
"""
from pathlib import Path

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import pandas as pd

ROOT = Path(__file__).resolve().parent.parent
R = ROOT / "results"
COLORE = {"BASE": "#2a78d6", "BASE+seed": "#eb6834", "ER+seed": "#1baf7a", "ER-pool": "#eda100", "ORACLE": "#e87ba4"}
MARK = {"BASE": "o", "BASE+seed": "s", "ER+seed": "^", "ER-pool": "D", "ORACLE": "v"}
SERIE = ["#2a78d6", "#eb6834", "#1baf7a", "#eda100"]          # per serie non legate ai sistemi
MARK_S = ["o", "s", "^", "D"]
SFONDO, INCHIOSTRO, MUTO = "#fcfcfb", "#0b0b0b", "#6b6a66"

plt.rcParams.update({"figure.facecolor": SFONDO, "axes.facecolor": SFONDO, "axes.edgecolor": "#c3c2b7",
                     "axes.labelcolor": "#52514e", "xtick.color": "#52514e", "ytick.color": "#52514e",
                     "text.color": INCHIOSTRO, "axes.grid": True, "axes.grid.axis": "y", "grid.color": "#e6e5e0",
                     "grid.linewidth": 0.7, "axes.spines.top": False, "axes.spines.right": False,
                     "axes.spines.left": False, "ytick.left": False, "font.size": 10.5, "lines.linewidth": 2,
                     "lines.markersize": 7, "legend.frameon": False, "axes.titlesize": 10.5,
                     "axes.titleweight": "bold", "axes.titlelocation": "left"})

# Testi dei grafici nelle due lingue. Chiave: (grafico, elemento).
T = {
    "it": {
        "sd": "Fascia = ± 1 deviazione standard fra 5 seed.",
        "G1": ("Con le evidenze divise fra due fonti, solo il linkage resta a 1",
               "Query multi-source, k = 4, ω > 0.",
               "α = quota di entità condivise con farmaci diversi nelle due fonti", "Accuratezza della risposta"),
        "G2": ("Il guadagno del linkage segue α, non ω",
               "ER+seed meno BASE+seed, query multi-source, k = 4.",
               "ω = sovrapposizione delle identità fra le fonti", "Guadagno di accuratezza"),
        "G3": ("I quasi-duplicati consumano un budget piccolo",
               "ER+seed, query multi-source, ε = quota di eventi con un quasi-duplicato, N = 500, ω = α = 0,5.",
               "Budget k (documenti nel contesto)", "Completezza delle evidenze"),
        "G4": ("Il retriever denso raramente trova la persona indicata da un ID locale",
               "BASE: quota di query con l'entità del seed nei top-k.",
               "Budget k (documenti nel contesto)", "Quota di query"),
        "G5": ("Contare sul contesto recuperato sbaglia di circa il 90 %",
               "Errore relativo rispetto a COUNT(DISTINCT gid), BASE, k = 8, media su 5 seed.",
               "ω = sovrapposizione delle identità fra le fonti", "Errore relativo"),
        "G6": ("Link sbagliati: i falsi positivi tolgono accuratezza, i falsi negativi la riducono gradualmente",
               "k = 4, N = 500, ω = α = 0,5.",
               "Quota di falsi positivi", "Quota di falsi negativi", "Accuratezza della risposta",
               "Query single-source", "Query multi-source"),
        "eps": "ε = {v}", "N": "N = {v}", "alpha": "α = {v}",
        "g5": ["Somma dei conteggi locali (per farmaco)", "γ − 1 sul totale (teorico)",
               "Conteggio sul contesto (RAG)"],
        "nomi": {},
    },
    "en": {
        "sd": "Bands: spread over 5 seeds.",
        "G1": ("Split records: only linking answers correctly",
               "Questions about one patient, answered from 4 retrieved records.",
               "Share of patients whose hospital and pharmacy list different drugs", "Correct answers"),
        "G2": ("Linking helps as much as the evidence is split, whatever the overlap",
               "Correct answers with linking minus those with the patient ID alone.",
               "Share of patients present in both sources", "Gain from linking"),
        "G3": ("Duplicate records crowd out evidence when the context is small",
               "Patient ID + linking. Each line is a share of records that have a near-copy.",
               "Records in the context", "Evidence found"),
        "G4": ("Semantic search rarely finds the patient named by an ID",
               "Share of questions whose top results include the patient that was asked about.",
               "Records in the context", "Questions"),
        "G5": ("Counting patients from retrieved text is off by about 90 %",
               "Error against the exact count of distinct patients, semantic search, 8 records.",
               "Share of patients present in both sources", "Error"),
        "G6": ("Wrong links cost accuracy, missing links erode it slowly",
               "Linking with errors, against the patient ID alone, 4 records.",
               "Share of wrong links", "Share of missing links", "Correct answers",
               "Answer in one source", "Answer split across two sources"),
        "eps": "{v:.0%} copies", "N": "{v} patients per source", "alpha": "{v:.0%} of patients split",
        "g5": ["Sum of per-source counts", "Overcount from overlap (theory)", "Count from retrieved text"],
        "nomi": {"BASE": "Semantic search", "BASE+seed": "Patient ID only", "ER+seed": "Patient ID + linking",
                 "ER-pool": "Linking every hit", "ORACLE": "Perfect retrieval"},
    },
}


def media_std(df, x, gruppo, metrica):
    s = df.groupby([gruppo, x, "seed"])[metrica].mean()
    return s.groupby([gruppo, x]).agg(["mean", "std"]).reset_index()


def etichette(ax, finali, xmax, dx, gap):
    """Etichette dirette a destra della linea; quelle troppo vicine si uniscono o si scostano."""
    finali = sorted(finali, key=lambda t: t[0])
    gruppi = []
    for y, testo, c in finali:
        if gruppi and abs(y - gruppi[-1][0]) < 0.005:       # stesse coordinate: un'unica etichetta
            gruppi[-1][1].append(testo)
            continue
        gruppi.append([y, [testo], c])
    pos = []
    for y, _, _ in gruppi:
        pos.append(max(y, pos[-1] + gap) if pos else y)
    for (y, testi, c), p in zip(gruppi, pos):
        ax.annotate(", ".join(testi), (xmax, y), xytext=(xmax + dx, p), color=INCHIOSTRO, fontsize=9.5,
                    va="center", ha="left", annotation_clip=False,
                    arrowprops=None if abs(p - y) < 1e-9 else dict(arrowstyle="-", color=c, lw=0.8))


def linee(ax, t, x, gruppo, ordine, colori, marcatori, fmt=str, gap=0.06, sinistra=False):
    finali, xs = [], []
    for i, g in enumerate(ordine):
        d = t[t[gruppo] == g].sort_values(x)
        if d.empty:
            continue
        c = colori[g] if isinstance(colori, dict) else colori[i]
        m = marcatori[g] if isinstance(marcatori, dict) else marcatori[i]
        sd = d["std"].fillna(0)
        ax.fill_between(d[x], d["mean"] - sd, d["mean"] + sd, color=c, alpha=0.16, linewidth=0, zorder=1)
        # ORACLE tratteggiato e sopra: spesso coincide con ER+seed (accuracy 1) e lo coprirebbe
        ax.plot(d[x], d["mean"], color=c, marker=m, markeredgecolor=SFONDO, markeredgewidth=1.5,
                linestyle=(0, (4, 2.5)) if g == "ORACLE" else "-", zorder=3 if g == "ORACLE" else 2, label=fmt(g))
        finali.append((d["mean"].iloc[0 if sinistra else -1], fmt(g), c))
        xs.extend(d[x].tolist())
    lo, hi = min(xs), max(xs)
    ax.set_xlim(lo - 0.04 * (hi - lo), hi + 0.04 * (hi - lo))
    if sinistra:                       # etichette sotto il primo punto, dentro l'area del grafico
        for y, testo, c in finali:
            ax.annotate(testo, (lo, y), xytext=(10, -13), textcoords="offset points", fontsize=9.5,
                        color=INCHIOSTRO, ha="left", va="center")
    else:
        etichette(ax, finali, hi, 0.06 * (hi - lo), gap)


def percento(ax, lingua, x=False, y=False):
    """[MIO] Nella versione inglese (README) le quote si leggono in percentuale."""
    if lingua != "en":
        return
    f = matplotlib.ticker.PercentFormatter(1.0, decimals=0)
    if x:
        ax.xaxis.set_major_formatter(f)
    if y:
        ax.yaxis.set_major_formatter(f)


def figura(w=7.6, h=4.4, **kw):
    return plt.subplots(figsize=(w, h), **kw)


def salva(fig, cartella, nome, titolo, sottotitolo, nota):
    fig.text(0.015, 0.975, titolo, ha="left", va="top", fontsize=12.5, fontweight="bold")
    fig.text(0.015, 0.915, f"{sottotitolo} {nota}" if nota else sottotitolo, ha="left", va="top",
             fontsize=9.5, color=MUTO)
    fig.tight_layout(rect=(0, 0, 1, 0.87))
    fig.savefig(cartella / nome, dpi=200)
    plt.close(fig)


def grafici(lingua, q, e, c):
    L = T[lingua]
    out = R / "plots" if lingua == "it" else R / "plots" / "en"
    out.mkdir(parents=True, exist_ok=True)
    sist = list(COLORE)
    nome = lambda g: L["nomi"].get(g, g)

    # G1 (H1, H2): accuracy multi-source al variare di alpha
    m = q[(q.k == 4) & (q.omega > 0) & (q.tipo == "multi-source")]
    tit, sub, xl, yl = L["G1"]
    fig, ax = figura()
    linee(ax, media_std(m, "alpha", "sistema", "accuracy"), "alpha", "sistema", sist, COLORE, MARK, fmt=nome)
    ax.set(xlabel=xl, ylabel=yl, ylim=(-0.05, 1.08), xticks=[0, 0.5, 1])
    percento(ax, lingua, x=True, y=True)
    fig.subplots_adjust(right=0.8)
    salva(fig, out, "G1_accuracy_alpha.png", tit, sub, L["sd"])

    # G2 (H4): guadagno del linkage per omega, una linea per alpha
    a = m[m.sistema == "ER+seed"].groupby(["alpha", "omega", "seed"]).accuracy.mean()
    b = m[m.sistema == "BASE+seed"].groupby(["alpha", "omega", "seed"]).accuracy.mean()
    g = (a - b).groupby(["alpha", "omega"]).agg(["mean", "std"]).reset_index()
    tit, sub, xl, yl = L["G2"]
    fig, ax = figura()
    linee(ax, g, "omega", "alpha", [0, 0.5, 1], SERIE, MARK_S, fmt=lambda v: L["alpha"].format(v=v))
    ax.set(xlabel=xl, ylabel=yl, ylim=(-0.05, 1.08), xticks=[0.25, 0.5, 0.75])
    percento(ax, lingua, x=True, y=True)
    salva(fig, out, "G2_gain_omega.png", tit, sub, L["sd"])

    # G3 (H3): completezza di ER+seed al variare di k con quasi-duplicati
    d = e[(e.studio == "duplicati") & (e.tipo == "multi-source") & (e.sistema == "ER+seed")]
    tit, sub, xl, yl = L["G3"]
    fig, ax = figura()
    linee(ax, media_std(d, "k", "x", "completezza"), "k", "x", [0, 0.25, 0.5], SERIE, MARK_S,
          fmt=lambda v: L["eps"].format(v=v), gap=0.03, sinistra=True)
    ax.set(xlabel=xl, ylabel=yl, ylim=(0.6, 1.03), xticks=[2, 4, 8])
    percento(ax, lingua, y=True)
    salva(fig, out, "G3_duplicates_budget.png", tit, sub, "")

    # G4: disambiguazione di BASE per N e k
    b = q[q.sistema == "BASE"]
    tit, sub, xl, yl = L["G4"]
    fig, ax = figura()
    linee(ax, media_std(b, "k", "N", "disambiguazione"), "k", "N", [100, 500, 1000], SERIE, MARK_S,
          fmt=lambda v: L["N"].format(v=v), gap=0.04)
    ax.set(xlabel=xl, ylabel=yl, ylim=(0, 1), xticks=[2, 4, 8])
    ax.yaxis.set_major_formatter(matplotlib.ticker.PercentFormatter(1.0))
    salva(fig, out, "G4_disambiguation.png", tit, sub, L["sd"])

    # G5: conteggi, errore relativo per omega
    c8 = c[(c.k == 8) & (c.sistema == "BASE")].copy()
    c8["locale"] = (c8.somma_locale - c8.esatto) / c8.esatto
    c8["rag"] = (c8.rag - c8.esatto).abs() / c8.esatto
    t = c8.groupby("omega")[["locale", "rag"]].mean()
    t["gamma"] = [2 / (2 - w) - 1 for w in t.index]
    tit, sub, xl, yl = L["G5"]
    fig, ax = figura()
    finali = []
    for i, (col, stile) in enumerate([("locale", "-"), ("gamma", (0, (4, 2.5))), ("rag", "-")]):
        ax.plot(t.index, t[col], color=SERIE[i], marker=MARK_S[i], markeredgecolor=SFONDO, markeredgewidth=1.5,
                linestyle=stile, label=L["g5"][i])
        finali.append((t[col].iloc[-1], L["g5"][i], SERIE[i]))
    ax.set(xlabel=xl, ylabel=yl, ylim=(0, 1.05), xticks=[0, 0.25, 0.5, 0.75], xlim=(-0.03, 0.78))
    percento(ax, lingua, x=True)
    ax.yaxis.set_major_formatter(matplotlib.ticker.PercentFormatter(1.0))
    etichette(ax, finali, 0.75, 0.04, 0.06)
    fig.subplots_adjust(right=0.7)
    salva(fig, out, "G5_counts.png", tit, sub, "")

    # G6: falsi match (ER+seed) - falsi positivi su single-source, falsi negativi su multi-source
    f = e[(e.studio == "falsi") & (e.k == 4)]
    tit, sub, xfp, xfn, yl, t1, t2 = L["G6"]
    fig, (a1, a2) = figura(9.6, 4.2, ncols=2, sharey=True)
    for ax, tipo, x, fisso, lab, tt in [(a1, "single-source", "y", "x", xfp, t1),
                                        (a2, "multi-source", "x", "y", xfn, t2)]:
        s = f[(f.tipo == tipo) & (f[fisso] == 0)]
        linee(ax, media_std(s, x, "sistema", "accuracy"), x, "sistema", ["BASE+seed", "ER+seed"], COLORE, MARK,
              fmt=nome)
        ax.set(xlabel=lab, title=tt, ylim=(0.4, 1.05))
        percento(ax, lingua, x=True, y=True)
    a1.set_ylabel(yl)
    salva(fig, out, "G6_false_matches.png", tit, sub, L["sd"])
    print("Grafici salvati in", out)


def main():
    q = pd.read_csv(R / "experiment_queries.csv")
    e = pd.read_csv(R / "extension_queries.csv")
    c = pd.read_csv(R / "experiment_counts.csv")
    for lingua in ("it", "en"):
        grafici(lingua, q, e, c)


if __name__ == "__main__":
    main()
