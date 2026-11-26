"""Figures 1-9, each one question and its answer, in Italian (results/plots/) and English (results/plots/en/).

Lines are means over 5 seeds; light bands show the spread between seeds; bars carry 95 % intervals.
"""
from pathlib import Path

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from matplotlib.ticker import PercentFormatter

ROOT = Path(__file__).resolve().parent.parent
R = ROOT / "results"
SFONDO, INCHIOSTRO, MUTO, GRIGIO = "#fcfcfb", "#0b0b0b", "#6b6a66", "#8f8e86"
C = {"sem": "#2a78d6", "id": "#eb6834", "link": "#1baf7a", "pool": "#eda100", "parole": "#e87ba4"}

plt.rcParams.update({"figure.facecolor": SFONDO, "axes.facecolor": SFONDO, "axes.edgecolor": "#c3c2b7",
                     "axes.labelcolor": "#52514e", "xtick.color": "#52514e", "ytick.color": "#52514e",
                     "text.color": INCHIOSTRO, "axes.grid": True, "axes.grid.axis": "y", "grid.color": "#e6e5e0",
                     "grid.linewidth": 0.7, "axes.spines.top": False, "axes.spines.right": False,
                     "axes.spines.left": False, "ytick.left": False, "font.size": 10.5, "lines.linewidth": 2.2,
                     "lines.markersize": 7, "legend.frameon": False, "axes.titlesize": 10.5,
                     "axes.titleweight": "bold", "axes.titlelocation": "left"})

T = {
    "it": {
        "piede": "Media su 5 ripetizioni con dati diversi; la fascia chiara mostra quanto variano.",
        "piede_barre": "Barre: media su 5 ripetizioni; tratto nero = intervallo al 95 %.",
        "sem": "Ricerca semantica", "id": "Solo ID del paziente", "link": "ID + collegamento (ER)",
        "pool": "Ricerca semantica + collegare tutto", "parole": "Ricerca per parole (BM25)",
        "parole_link": "Parole + collegamento", "ibrido": "Ibrido (parole + semantica)",
        "ibrido_link": "Ibrido + collegamento", "nome": "ID + collegamento, ER per nome",
        "varieta": "+ prima un documento per fonte", "mmr": "+ scarta i documenti troppo simili (MMR)",
        "f1": ("Quando serve collegare i record delle due fonti?",
               "Quando ospedale e farmacia riportano farmaci diversi: lì il collegamento è l'unico a rispondere.",
               "Pazienti condivisi con farmaci diversi nelle due fonti", ["nessuno", "metà", "tutti"],
               "Risposte corrette", "+{v:.0f} punti", "Domande su pazienti presenti in entrambe le fonti, "
               "4 documenti nel contesto."),
        "f2": ("Conta quanti pazienti hanno in comune le due fonti?",
               "No: il guadagno dipende da quanti hanno dati diversi, non da quanti sono in comune.",
               "Pazienti presenti in entrambe le fonti", "Punti guadagnati collegando",
               ["Nessun paziente con dati diversi", "Metà con dati diversi", "Tutti con dati diversi"],
               "Risposte corrette con il collegamento meno quelle con il solo ID."),
        "f3": ("La ricerca semantica trova il paziente nominato nella domanda?",
               "Quasi mai: lo trova in 1 domanda su 4–7. La ricerca per parole esatte lo trova sempre.",
               "Documenti nel contesto", "Paziente trovato",
               "La domanda contiene l'ID locale del paziente (es. «H:3»). Embedding MiniLM; con un altro modello "
               "cambia: figura 9."),
        "f4": ("Se il sistema riceve solo la domanda, quale strategia risponde?",
               "Cercare l'ID per parole e poi collegare: 100 %, come se l'ID fosse già noto.",
               "Risposte corrette", "con l'ID già noto", "Domande su pazienti in entrambe le fonti, "
               "4 documenti nel contesto."),
        "f5": ("Cosa succede se l'Entity Resolution sbaglia?",
               "Un collegamento sbagliato fa peggio che non collegare; uno mancante toglie solo parte del vantaggio.",
               "Pazienti fusi per errore con un altro", "Pazienti non collegati fra le fonti", "Risposte corrette",
               "Paziente in una sola fonte", "Paziente in entrambe le fonti", "peggio che\nnon collegare",
               "4 documenti nel contesto."),
        "f6": ("E se l'ER collega i pazienti per nome?",
               "Ogni omonimo diventa un collegamento sbagliato: con un quarto di omonimi si scende al 76 %.",
               "Pazienti che hanno un omonimo", "Risposte corrette",
               "Domande su pazienti in entrambe le fonti, 4 documenti nel contesto."),
        "f7": ("I doppioni occupano i posti nel contesto: si può evitare?",
               "Sì: scartare i documenti troppo simili a quelli già scelti riporta tutto al 100 %.",
               "Prove complete", "Paziente in una sola fonte", "Paziente in entrambe le fonti",
               "Metà dei documenti ha una quasi-copia; solo 2 documenti nel contesto (con 4 o più il problema "
               "sparisce)."),
        "f8": ("Si può chiedere al RAG quanti pazienti hanno preso un farmaco?",
               "No: contando dai documenti trovati si sbaglia di circa il 90 %. Contare i GID distinti è esatto.",
               "Pazienti presenti in entrambe le fonti", "Errore sul numero di pazienti",
               ["Contare dai documenti trovati (RAG)", "Sommare i conteggi delle due fonti",
                "Contare i GID distinti (esatto)"],
               "8 documenti nel contesto. La somma delle fonti sbaglia esattamente del sovraconteggio previsto "
               "dal paper."),
        "f9": ("Questi risultati dipendono dalle frasi e dal modello?",
               "Con frasi variate la semantica perde l'ID anche con E5; le parole reggono, tranne sui refusi.",
               "Paziente trovato", ["Frase\nfissa", "Frasi\nvariate", "Con\nrefusi", "Per\nnome"],
               "Domande su pazienti in entrambe le fonti, 4 documenti nel contesto. Refusi: ID scritto «H-37» "
               "o «H37» nel 20 % dei documenti."),
    },
    "en": {
        "piede": "Mean over 5 runs with different data; the light band shows how much they vary.",
        "piede_barre": "Bars: mean over 5 runs; black tick = 95 % interval.",
        "sem": "Semantic search", "id": "Patient ID only", "link": "Patient ID + linking (ER)",
        "pool": "Semantic search + link every hit", "parole": "Keyword search (BM25)",
        "parole_link": "Keywords + linking", "ibrido": "Hybrid (keywords + semantic)",
        "ibrido_link": "Hybrid + linking", "nome": "Patient ID + linking, ER by name",
        "varieta": "+ one record per source first", "mmr": "+ drop records too similar (MMR)",
        "f1": ("When does linking the two sources pay off?",
               "When hospital and pharmacy list different drugs: there, only linking answers.",
               "Shared patients with different drugs in the two sources", ["none", "half", "all"],
               "Correct answers", "+{v:.0f} points", "Questions about patients in both sources, 4 records in "
               "the context."),
        "f2": ("Does it matter how many patients the sources share?",
               "No: the gain depends on how many have different records, not on how many are shared.",
               "Patients present in both sources", "Points gained by linking",
               ["No patient with different records", "Half with different records", "All with different records"],
               "Correct answers with linking minus those with the patient ID alone."),
        "f3": ("Does semantic search find the patient named in the question?",
               "Rarely: in 1 question out of 4 to 7. Keyword search always finds it.",
               "Records in the context", "Patient found",
               "The question names the patient's local ID (e.g. \"H:3\"). MiniLM embeddings; another model "
               "changes this: figure 9."),
        "f4": ("Given only the question, which strategy answers?",
               "Find the ID by keywords, then link: 100 %, as if the ID were known.",
               "Correct answers", "with the ID known", "Questions about patients in both sources, 4 records "
               "in the context."),
        "f5": ("What happens when Entity Resolution makes mistakes?",
               "A wrong link is worse than no link; a missing link only takes away part of the gain.",
               "Patients wrongly merged with someone else", "Patients not linked across sources",
               "Correct answers", "Patient in one source", "Patient in both sources", "worse than\nno linking",
               "4 records in the context."),
        "f6": ("What if ER links patients by name?",
               "Every namesake becomes a wrong link: with a quarter of namesakes, accuracy drops to 76 %.",
               "Patients who have a namesake", "Correct answers",
               "Questions about patients in both sources, 4 records in the context."),
        "f7": ("Duplicates take up slots in the context: can it be avoided?",
               "Yes: dropping records too similar to those already chosen brings it back to 100 %.",
               "Complete evidence", "Patient in one source", "Patient in both sources",
               "Half of the records have a near-copy; only 2 records in the context (with 4 or more the problem "
               "disappears)."),
        "f8": ("Can RAG count how many patients received a drug?",
               "No: counting from the retrieved records is off by about 90 %. Counting distinct GIDs is exact.",
               "Patients present in both sources", "Error on the number of patients",
               ["Count from retrieved records (RAG)", "Add up the two sources' counts",
                "Count distinct GIDs (exact)"],
               "8 records in the context. Adding up the sources overcounts exactly as the paper predicts."),
        "f9": ("Do these results depend on the wording and the model?",
               "With varied sentences, semantic search loses the ID even with E5; keywords hold, except on typos.",
               "Patient found", ["Fixed\nsentence", "Varied\nsentences", "With\ntypos", "By\nname"],
               "Questions about patients in both sources, 4 records in the context. Typos: ID written \"H-37\" "
               "or \"H37\" in 20 % of the records."),
    },
}


# ---------------------------------------------------------------- helpers
def per_seed(df, x, metrica):
    s = df.groupby([x, "seed"])[metrica].mean()
    return s.groupby(x).agg(["mean", "std"]).reset_index()


def linea(ax, t, x, colore, testo, stile="-", marcatore="o"):
    sd = t["std"].fillna(0)
    ax.fill_between(t[x], t["mean"] - sd, t["mean"] + sd, color=colore, alpha=0.15, linewidth=0, zorder=1)
    ax.plot(t[x], t["mean"], color=colore, linestyle=stile, marker=marcatore, markeredgecolor=SFONDO,
            markeredgewidth=1.5, zorder=3)
    return (float(t["mean"].iloc[-1]), testo, colore)


def etichette(ax, finali, gap=0.07):
    """Labels right of the last point, nudged apart when they would overlap."""
    x0, x1 = ax.get_xlim()
    x1 += 0.012 * (x1 - x0)
    finali = sorted(finali, key=lambda f: f[0])
    pos = []
    for y, _, _ in finali:
        pos.append(max(y, pos[-1] + gap) if pos else y)
    for (y, testo, c), p in zip(finali, pos):
        ax.annotate(testo, (x1, y), xytext=(x1, p), xycoords="data", color=c, fontsize=9.5, fontweight="bold",
                    va="center", ha="left", annotation_clip=False)


def percento(ax, x=False):
    ax.yaxis.set_major_formatter(PercentFormatter(1.0, decimals=0))
    if x:
        ax.xaxis.set_major_formatter(PercentFormatter(1.0, decimals=0))


def figura(w=8.2, h=4.8, **kw):
    return plt.subplots(figsize=(w, h), **kw)


def salva(fig, cartella, nome, titolo, risposta, nota, piede, destra=0.74, basso=0.09):
    fig.text(0.02, 0.975, titolo, ha="left", va="top", fontsize=13.5, fontweight="bold")
    fig.text(0.02, 0.915, risposta, ha="left", va="top", fontsize=10.5, color=INCHIOSTRO)
    fig.text(0.02, 0.02, nota + "\n" + piede, ha="left", va="bottom", fontsize=8.5, color=MUTO, linespacing=1.4)
    fig.tight_layout(rect=(0, basso, destra, 0.86))
    fig.savefig(cartella / nome, dpi=200)
    plt.close(fig)


def ic95(x):
    p, n = x.mean(), len(x)
    return p, 1.96 * np.sqrt(p * (1 - p) / n) if n else 0


# ---------------------------------------------------------------- figures
def grafici(lingua, q, e, c, f, t=None):
    L = T[lingua]
    out = R / "plots" if lingua == "it" else R / "plots" / "en"
    out.mkdir(parents=True, exist_ok=True)
    for vecchio in out.glob("*.png"):
        vecchio.unlink()

    # 1. When does linking pay off
    m = q[(q.k == 4) & (q.omega > 0) & (q.tipo == "multi-source")]
    tit, ris, xl, xt, yl, gain, nota = L["f1"]
    fig, ax = figura()
    fin = [linea(ax, per_seed(m[m.sistema == s], "alpha", "accuracy"), "alpha", C[k], L[k])
           for s, k in [("BASE", "sem"), ("BASE+seed", "id"), ("ER+seed", "link")]]
    ax.set(xlabel=xl, ylabel=yl, ylim=(-0.04, 1.08), xticks=[0, 0.5, 1], xticklabels=xt, xlim=(-0.06, 1.06))
    a = m[(m.alpha == 0.5) & (m.sistema == "BASE+seed")].accuracy.mean()
    b = m[(m.alpha == 0.5) & (m.sistema == "ER+seed")].accuracy.mean()
    ax.annotate("", (0.5, b - 0.02), (0.5, a + 0.02), arrowprops=dict(arrowstyle="<->", color=INCHIOSTRO, lw=1.2))
    ax.text(0.52, (a + b) / 2, gain.format(v=100 * (b - a)), va="center", fontsize=10, fontweight="bold")
    percento(ax)
    etichette(ax, fin)
    salva(fig, out, "fig1_when_linking_helps.png", tit, ris, nota, L["piede"])

    # 2. Overlap does not matter
    tit, ris, xl, yl, nomi, nota = L["f2"]
    fig, ax = figura()
    fin = []
    for alpha, col, nm in zip([0, 0.5, 1], [GRIGIO, C["link"], "#0d6b4a"], nomi):
        A = m[(m.alpha == alpha) & (m.sistema == "ER+seed")].groupby(["omega", "seed"]).accuracy.mean()
        Bq = m[(m.alpha == alpha) & (m.sistema == "BASE+seed")].groupby(["omega", "seed"]).accuracy.mean()
        g = (A - Bq).groupby("omega").agg(["mean", "std"]).reset_index()
        fin.append(linea(ax, g, "omega", col, nm))
    ax.set(xlabel=xl, ylabel=yl, ylim=(-0.04, 1.08), xticks=[0.25, 0.5, 0.75], xlim=(0.2, 0.8))
    ax.yaxis.set_major_formatter(matplotlib.ticker.FuncFormatter(lambda v, _: f"+{100 * v:.0f}" if v else "0"))
    ax.xaxis.set_major_formatter(PercentFormatter(1.0, decimals=0))
    etichette(ax, fin)
    salva(fig, out, "fig2_overlap_does_not_matter.png", tit, ris, nota, L["piede"])

    # 3. Semantic search does not find IDs
    ib = f[f.studio == "ibrido"]
    tit, ris, xl, yl, nota = L["f3"]
    fig, ax = figura()
    fin = [linea(ax, per_seed(ib[ib.sistema == s], "k", "trova_paziente"), "k", C[k], L[k])
           for s, k in [("BASE", "sem"), ("BM25", "parole")]]
    ax.set(xlabel=xl, ylabel=yl, ylim=(0, 1.08), xticks=[2, 4, 8], xlim=(1.6, 8.4))
    percento(ax)
    etichette(ax, fin)
    salva(fig, out, "fig3_semantic_search_misses_ids.png", tit, ris, nota, L["piede"])

    # 4. Strategies given only the question
    tit, ris, xl, rif, nota = L["f4"]
    ms = f[(f.k == 4) & (f.tipo == "multi-source")]
    voci = [("ibrido", "BASE", "sem"), ("indici", "ER-pool", "pool"), ("ibrido", "BM25", "parole"),
            ("ibrido", "BM25 + ER", "parole_link")]
    fig, ax = figura(8.2, 4.6)
    for i, (st, s, k) in enumerate(voci):
        p, h = ic95(ms[(ms.studio == st) & (ms.sistema == s)].accuracy)
        col = C["link"] if k == "parole_link" else GRIGIO
        ax.barh(i, p, color=col, height=0.62, zorder=2)
        ax.errorbar(p, i, xerr=h, color=INCHIOSTRO, capsize=0, lw=1.4, zorder=3)
        ax.text(p + h + 0.015, i, f"{100 * p:.0f} %", va="center", fontsize=10,
                fontweight="bold" if k == "parole_link" else "normal")
    ax.axvline(1, color=INCHIOSTRO, lw=1, ls=(0, (3, 3)), zorder=1)
    ax.text(1.0, len(voci) - 0.35, rif, ha="right", va="bottom", fontsize=9, color=MUTO)
    ax.set(yticks=range(len(voci)), yticklabels=[L[k] for _, _, k in voci], xlim=(0, 1.12), xlabel=xl)
    ax.grid(axis="y", visible=False)
    ax.grid(axis="x", visible=True)
    ax.xaxis.set_major_formatter(PercentFormatter(1.0, decimals=0))
    salva(fig, out, "fig4_strategies_without_id.png", tit, ris, nota, L["piede_barre"], destra=1)

    # 5. ER mistakes
    tit, ris, xfp, xfn, yl, t1, t2, peggio, nota = L["f5"]
    fz = e[(e.studio == "falsi") & (e.k == 4)]
    fig, (a1, a2) = figura(9.8, 4.8, ncols=2, sharey=True)
    for ax, tipo, x, fisso, lab, tt in [(a1, "single-source", "y", "x", xfp, t1), (a2, "multi-source", "x", "y", xfn, t2)]:
        s = fz[(fz.tipo == tipo) & (fz[fisso] == 0)]
        base = s[s.sistema == "BASE+seed"].accuracy.mean()
        fin = [linea(ax, per_seed(s[s.sistema == "BASE+seed"], x, "accuracy"), x, C["id"], L["id"]),
               linea(ax, per_seed(s[s.sistema == "ER+seed"], x, "accuracy"), x, C["link"], L["link"])]
        xs = sorted(s[x].unique())
        ax.set(xlabel=lab, title=tt, ylim=(0.4, 1.06), xticks=xs, xlim=(xs[0] - 0.03 * xs[-1], xs[-1] * 1.03))
        percento(ax, x=True)
        if tipo == "single-source":
            ax.fill_between([xs[0], xs[-1]], 0.4, base, color=C["id"], alpha=0.06, zorder=0)
            ax.text(xs[-1] * 0.5, 0.5, peggio, ha="center", va="center", fontsize=9.5, color=C["id"])
        etichette(ax, fin, gap=0.08)
    a1.set_ylabel(yl)
    salva(fig, out, "fig5_er_mistakes.png", tit, ris, nota, L["piede"], destra=0.83)

    # 6. Homonyms
    tit, ris, xl, yl, nota = L["f6"]
    om = f[(f.studio == "omonimi") & (f.k == 4) & (f.tipo == "multi-source")]
    fig, ax = figura()
    fin = [linea(ax, per_seed(om[(om.sistema == "BASE+seed") & (om.er == "ideal")], "x", "accuracy"), "x", C["id"], L["id"]),
           linea(ax, per_seed(om[(om.sistema == "ER+seed") & (om.er == "ideal")], "x", "accuracy"), "x", C["link"], L["link"]),
           linea(ax, per_seed(om[(om.sistema == "ER+seed") & (om.er == "names")], "x", "accuracy"), "x", C["link"],
                 L["nome"], stile=(0, (4, 2.5)), marcatore="s")]
    ax.set(xlabel=xl, ylabel=yl, ylim=(0.4, 1.06), xticks=[0, 0.1, 0.25], xlim=(-0.01, 0.26))
    percento(ax, x=True)
    etichette(ax, fin)
    salva(fig, out, "fig6_homonyms.png", tit, ris, nota, L["piede"], destra=0.7)

    # 7. Duplicates and diversity
    tit, ris, yl, t1, t2, nota = L["f7"]
    dv = f[(f.studio == "diversita") & (f.k == 2) & (f.x == 0.5)]
    varianti = [("ER+seed", "link", C["link"]), ("ER+seed, source variety", "varieta", C["sem"]),
                ("ER+seed, MMR", "mmr", C["parole"])]
    fig, ax = figura(8.2, 4.8)
    w = 0.26
    for j, (s, k, col) in enumerate(varianti):
        for i, tipo in enumerate(["single-source", "multi-source"]):
            p, h = ic95(dv[(dv.tipo == tipo) & (dv.sistema == s)].completezza)
            x = i + (j - 1) * w
            ax.bar(x, p, width=w * 0.9, color=col, zorder=2, label=L[k] if i == 0 else None)
            ax.errorbar(x, p, yerr=h, color=INCHIOSTRO, lw=1.4, zorder=3)
            ax.text(x, p + h + 0.02, f"{100 * p:.0f} %", ha="center", fontsize=10)
    ax.set(xticks=[0, 1], xticklabels=[t1, t2], ylabel=yl, ylim=(0, 1.15))
    ax.legend(loc="upper center", bbox_to_anchor=(0.5, -0.1), ncol=1, fontsize=9.5)
    percento(ax)
    salva(fig, out, "fig7_duplicates.png", tit, ris, nota, L["piede_barre"], destra=1)

    # 8. Counting
    tit, ris, xl, yl, nomi, nota = L["f8"]
    c8 = c[(c.k == 8) & (c.sistema == "BASE")].copy()
    c8["rag"] = (c8.rag - c8.esatto).abs() / c8.esatto
    c8["locale"] = (c8.somma_locale - c8.esatto) / c8.esatto
    c8["gid"] = 0.0
    fig, ax = figura()
    fin = []
    for col, colore, nm, mk in zip(["rag", "locale", "gid"], [C["sem"], C["id"], C["link"]], nomi, "osD"):
        fin.append(linea(ax, per_seed(c8, "omega", col), "omega", colore, nm, marcatore=mk))
    ax.set(xlabel=xl, ylabel=yl, ylim=(-0.03, 1.05), xticks=[0, 0.25, 0.5, 0.75], xlim=(-0.03, 0.78))
    percento(ax, x=True)
    etichette(ax, fin, gap=0.08)
    salva(fig, out, "fig8_counting.png", tit, ris, nota, L["piede"], destra=0.7)

    # 9. Wording and embedding model
    if t is not None:
        tit, ris, yl, condizioni, nota = L["f9"]
        tm = t[(t.k == 4) & (t.tipo == "multi-source")]
        sistemi = [("BASE", "sem", C["sem"]), ("BM25", "parole", C["parole"])]
        fig, assi = figura(10.4, 5.0, ncols=2, sharey=True)
        w = 0.34
        for ax, modello in zip(assi, ["MiniLM", "E5-small"]):
            for j, (s, k, col) in enumerate(sistemi):
                for i, cond in enumerate(["fisso", "variato", "refusi", "nome"]):
                    p, h = ic95(tm[(tm.modello == modello) & (tm.condizione == cond) & (tm.sistema == s)].trova_paziente)
                    x = i + (j - 0.5) * w
                    ax.bar(x, p, width=w * 0.9, color=col, zorder=2, label=L[k] if i == 0 else None)
                    ax.errorbar(x, p, yerr=h, color=INCHIOSTRO, lw=1.2, zorder=3)
                    ax.text(x, p + h + 0.02, f"{100 * p:.0f}", ha="center", fontsize=8.5)
            ax.set(xticks=range(4), xticklabels=condizioni, ylim=(0, 1.15), title=f"Embedding: {modello}")
            percento(ax)
        assi[0].set_ylabel(yl)
        h, lab = assi[0].get_legend_handles_labels()
        fig.legend(h, lab, loc="lower center", bbox_to_anchor=(0.5, 0.1), ncol=2, fontsize=9.5)
        salva(fig, out, "fig9_wording_and_model.png", tit, ris, nota, L["piede_barre"], destra=1, basso=0.15)
    print("Grafici salvati in", out)


def main():
    q = pd.read_csv(R / "experiment_queries.csv")
    e = pd.read_csv(R / "extension_queries.csv")
    c = pd.read_csv(R / "experiment_counts.csv")
    f = pd.read_csv(R / "followup_queries.csv")
    rt = R / "robustness_text_queries.csv"
    t = pd.read_csv(rt) if rt.exists() else None
    for lingua in ("it", "en"):
        grafici(lingua, q, e, c, f, t)


if __name__ == "__main__":
    main()
