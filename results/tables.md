# Tabelle dei risultati

Valori: media ± deviazione standard fra 5 seed. Accuracy = lettore deterministico senza LLM.

## T1 (H1) - Accuracy per tipo di query e sistema, k = 4, omega > 0

| tipo | BASE | BASE+seed | ER+seed | ER-pool | ORACLE |
|---|---|---|---|---|---|
| multi-source | 0.09 ± 0.0 | 0.5 ± 0.01 | 1.0 ± 0.0 | 0.11 ± 0.01 | 1.0 ± 0.0 |
| single-source | 0.03 ± 0.01 | 1.0 ± 0.0 | 1.0 ± 0.0 | 0.21 ± 0.02 | 1.0 ± 0.0 |

## T2 (H1) - Recall@k per tipo di query e sistema, k = 4, omega > 0

| tipo | BASE | BASE+seed | ER+seed | ER-pool | ORACLE |
|---|---|---|---|---|---|
| multi-source | 0.08 ± 0.01 | 0.5 ± 0.0 | 1.0 ± 0.0 | 0.11 ± 0.01 | 1.0 ± 0.0 |
| single-source | 0.16 ± 0.01 | 1.0 ± 0.0 | 1.0 ± 0.0 | 0.21 ± 0.02 | 1.0 ± 0.0 |

## T3 (H2) - Query multi-source: accuracy per alpha (complementarità), k = 4, omega > 0

| alpha | BASE | BASE+seed | ER+seed | ER-pool | ORACLE |
|---|---|---|---|---|---|
| 0.0 | 0.17 ± 0.02 | 1.0 ± 0.0 | 1.0 ± 0.0 | 0.12 ± 0.02 | 1.0 ± 0.0 |
| 0.5 | 0.09 ± 0.01 | 0.49 ± 0.02 | 1.0 ± 0.0 | 0.11 ± 0.01 | 1.0 ± 0.0 |
| 1.0 | 0.0 ± 0.0 | 0.0 ± 0.0 | 1.0 ± 0.0 | 0.12 ± 0.01 | 1.0 ± 0.0 |

## T4 (H2, H4) - Guadagno del linkage = accuracy(ER+seed) - accuracy(BASE+seed), query multi-source, k = 4

| omega | 0.0 | 0.5 | 1.0 |
|---|---|---|---|
| 0.25 | 0.0 ± 0.0 | 0.47 ± 0.05 | 1.0 ± 0.0 |
| 0.5 | 0.0 ± 0.0 | 0.51 ± 0.04 | 1.0 ± 0.0 |
| 0.75 | 0.0 ± 0.0 | 0.55 ± 0.03 | 1.0 ± 0.0 |

## T5 (H4) - Guadagno di ER-pool su BASE (accuracy), per omega e tipo, k = 4

| omega | multi-source | single-source |
|---|---|---|
| 0.0 | nan | 0.15 ± 0.04 |
| 0.25 | 0.03 ± 0.01 | 0.17 ± 0.02 |
| 0.5 | 0.03 ± 0.02 | 0.17 ± 0.03 |
| 0.75 | 0.03 ± 0.01 | 0.18 ± 0.03 |

## T6 (H3) - Budget k: accuracy, precision e costo (token) per sistema, query multi-source


**accuracy**

| k | BASE | BASE+seed | ER+seed | ER-pool | ORACLE |
|---|---|---|---|---|---|
| 2 | 0.06 ± 0.01 | 0.5 ± 0.01 | 1.0 ± 0.0 | 0.08 ± 0.01 | 1.0 ± 0.0 |
| 4 | 0.09 ± 0.0 | 0.5 ± 0.01 | 1.0 ± 0.0 | 0.11 ± 0.01 | 1.0 ± 0.0 |
| 8 | 0.11 ± 0.01 | 0.5 ± 0.01 | 1.0 ± 0.0 | 0.17 ± 0.01 | 1.0 ± 0.0 |

**precision**

| k | BASE | BASE+seed | ER+seed | ER-pool | ORACLE |
|---|---|---|---|---|---|
| 2 | 0.06 ± 0.0 | 1.0 ± 0.0 | 1.0 ± 0.0 | 0.08 ± 0.01 | 1.0 ± 0.0 |
| 4 | 0.04 ± 0.0 | 1.0 ± 0.0 | 1.0 ± 0.0 | 0.06 ± 0.01 | 1.0 ± 0.0 |
| 8 | 0.03 ± 0.0 | 1.0 ± 0.0 | 1.0 ± 0.0 | 0.04 ± 0.0 | 1.0 ± 0.0 |

**n_token**

| k | BASE | BASE+seed | ER+seed | ER-pool | ORACLE |
|---|---|---|---|---|---|
| 2 | 26.69 ± 0.07 | 13.54 ± 0.01 | 27.09 ± 0.04 | 26.86 ± 0.06 | 27.09 ± 0.04 |
| 4 | 53.42 ± 0.14 | 13.54 ± 0.01 | 27.09 ± 0.04 | 53.73 ± 0.1 | 27.09 ± 0.04 |
| 8 | 107.02 ± 0.25 | 13.54 ± 0.01 | 27.09 ± 0.04 | 107.52 ± 0.2 | 27.09 ± 0.04 |

## T7 - Disambiguazione (Sez. 12): quota di query in cui i top-k di BASE contengono l'entità del seed

| N | 2 | 4 | 8 |
|---|---|---|---|
| 100 | 0.23 ± 0.01 | 0.33 ± 0.02 | 0.46 ± 0.02 |
| 500 | 0.15 ± 0.01 | 0.21 ± 0.02 | 0.28 ± 0.01 |
| 1000 | 0.11 ± 0.01 | 0.15 ± 0.01 | 0.2 ± 0.01 |

## T8 - Conteggi: errore relativo medio rispetto a COUNT(DISTINCT gid), k = 8

| N | omega | err_somma_locale | err_rag | gamma_teorico - 1 |
|---|---|---|---|---|
| 100 | 0.0 | 0.0 | 0.878 | 0.0 |
| 100 | 0.25 | 0.038 | 0.856 | 0.143 |
| 100 | 0.5 | 0.096 | 0.822 | 0.333 |
| 100 | 0.75 | 0.198 | 0.764 | 0.6 |
| 500 | 0.0 | 0.0 | 0.976 | 0.0 |
| 500 | 0.25 | 0.038 | 0.971 | 0.143 |
| 500 | 0.5 | 0.097 | 0.965 | 0.333 |
| 500 | 0.75 | 0.201 | 0.954 | 0.6 |
| 1000 | 0.0 | 0.0 | 0.988 | 0.0 |
| 1000 | 0.25 | 0.038 | 0.986 | 0.143 |
| 1000 | 0.5 | 0.097 | 0.982 | 0.333 |
| 1000 | 0.75 | 0.202 | 0.977 | 0.6 |

## E - Dirty ER, delta = D/N: accuracy, query single-source, k = 4

| x | BASE | BASE+seed | ER+seed | ER-pool | ORACLE |
|---|---|---|---|---|---|
| 0.0 | 0.02 ± 0.03 | 1.0 ± 0.0 | 1.0 ± 0.0 | 0.18 ± 0.07 | 1.0 ± 0.0 |
| 0.1 | 0.02 ± 0.02 | 0.95 ± 0.02 | 1.0 ± 0.0 | 0.18 ± 0.06 | 1.0 ± 0.0 |
| 0.25 | 0.02 ± 0.02 | 0.87 ± 0.04 | 1.0 ± 0.0 | 0.14 ± 0.05 | 1.0 ± 0.0 |

## E - Dirty ER, delta = D/N: accuracy, query multi-source, k = 4

| x | BASE | BASE+seed | ER+seed | ER-pool | ORACLE |
|---|---|---|---|---|---|
| 0.0 | 0.08 ± 0.04 | 0.54 ± 0.06 | 1.0 ± 0.0 | 0.11 ± 0.03 | 1.0 ± 0.0 |
| 0.1 | 0.05 ± 0.05 | 0.48 ± 0.05 | 1.0 ± 0.0 | 0.08 ± 0.04 | 1.0 ± 0.0 |
| 0.25 | 0.06 ± 0.03 | 0.38 ± 0.05 | 1.0 ± 0.0 | 0.11 ± 0.06 | 1.0 ± 0.0 |

## E - Quasi-duplicati, quota eps: accuracy, query single-source, k = 4

| x | BASE | BASE+seed | ER+seed | ER-pool | ORACLE |
|---|---|---|---|---|---|
| 0.0 | 0.02 ± 0.03 | 1.0 ± 0.0 | 1.0 ± 0.0 | 0.18 ± 0.07 | 1.0 ± 0.0 |
| 0.25 | 0.02 ± 0.01 | 1.0 ± 0.0 | 1.0 ± 0.0 | 0.13 ± 0.05 | 1.0 ± 0.0 |
| 0.5 | 0.02 ± 0.02 | 1.0 ± 0.0 | 1.0 ± 0.0 | 0.12 ± 0.06 | 1.0 ± 0.0 |

## E - Quasi-duplicati, quota eps: accuracy, query multi-source, k = 4

| x | BASE | BASE+seed | ER+seed | ER-pool | ORACLE |
|---|---|---|---|---|---|
| 0.0 | 0.08 ± 0.04 | 0.54 ± 0.06 | 1.0 ± 0.0 | 0.11 ± 0.03 | 1.0 ± 0.0 |
| 0.25 | 0.08 ± 0.03 | 0.54 ± 0.06 | 1.0 ± 0.0 | 0.07 ± 0.04 | 1.0 ± 0.0 |
| 0.5 | 0.07 ± 0.02 | 0.54 ± 0.06 | 1.0 ± 0.0 | 0.08 ± 0.03 | 1.0 ± 0.0 |

## E - Errori sugli ID nel testo, quota eps: accuracy, query single-source, k = 4

| x | BASE | BASE+seed | ER+seed | ER-pool | ORACLE |
|---|---|---|---|---|---|
| 0.0 | 0.02 ± 0.03 | 1.0 ± 0.0 | 1.0 ± 0.0 | 0.18 ± 0.07 | 1.0 ± 0.0 |
| 0.1 | 0.02 ± 0.02 | 0.82 ± 0.06 | 1.0 ± 0.0 | 0.16 ± 0.07 | 1.0 ± 0.0 |
| 0.25 | 0.02 ± 0.01 | 0.57 ± 0.04 | 1.0 ± 0.0 | 0.15 ± 0.07 | 1.0 ± 0.0 |

## E - Errori sugli ID nel testo, quota eps: accuracy, query multi-source, k = 4

| x | BASE | BASE+seed | ER+seed | ER-pool | ORACLE |
|---|---|---|---|---|---|
| 0.0 | 0.08 ± 0.04 | 0.54 ± 0.06 | 1.0 ± 0.0 | 0.11 ± 0.03 | 1.0 ± 0.0 |
| 0.1 | 0.08 ± 0.03 | 0.46 ± 0.09 | 1.0 ± 0.0 | 0.1 ± 0.02 | 1.0 ± 0.0 |
| 0.25 | 0.05 ± 0.02 | 0.45 ± 0.07 | 1.0 ± 0.0 | 0.08 ± 0.03 | 1.0 ± 0.0 |

## E - Falsi match: qualità del linkage e accuracy, k = 4 (x = quota falsi negativi, y = quota falsi positivi)

| x | y | linkage_precision | linkage_recall | ER+seed single-source | ER+seed multi-source | BASE+seed multi-source |
|---|---|---|---|---|---|---|
| 0.0 | 0.0 | 1.0 | 1.0 | 1.0 ± 0.0 | 1.0 ± 0.0 | 0.54 ± 0.06 |
| 0.0 | 0.1 | 0.909 | 1.0 | 0.9 ± 0.02 | 1.0 ± 0.0 | 0.54 ± 0.06 |
| 0.0 | 0.25 | 0.801 | 1.0 | 0.78 ± 0.06 | 1.0 ± 0.0 | 0.54 ± 0.06 |
| 0.25 | 0.0 | 1.0 | 0.752 | 1.0 ± 0.0 | 0.89 ± 0.04 | 0.54 ± 0.06 |
| 0.25 | 0.1 | 0.883 | 0.752 | 0.9 ± 0.05 | 0.89 ± 0.04 | 0.54 ± 0.06 |
| 0.25 | 0.25 | 0.752 | 0.752 | 0.76 ± 0.05 | 0.89 ± 0.04 | 0.54 ± 0.06 |
| 0.5 | 0.0 | 1.0 | 0.5 | 1.0 ± 0.0 | 0.73 ± 0.04 | 0.54 ± 0.06 |
| 0.5 | 0.1 | 0.833 | 0.5 | 0.9 ± 0.05 | 0.73 ± 0.04 | 0.54 ± 0.06 |
| 0.5 | 0.25 | 0.668 | 0.5 | 0.8 ± 0.04 | 0.73 ± 0.04 | 0.54 ± 0.06 |

## F - Omonimi (x = quota di persone con un omonimo), k = 4; ER ideale vs ER per nome: accuracy, query single-source

| x | er | BASE | BASE+seed | ER+seed | ER-pool |
|---|---|---|---|---|---|
| 0.0 | ideal | 0.0 ± 0.01 | 1.0 ± 0.0 | 1.0 ± 0.0 | 0.07 ± 0.02 |
| 0.0 | names | 0.0 ± 0.01 | 1.0 ± 0.0 | 1.0 ± 0.0 | 0.07 ± 0.02 |
| 0.1 | ideal | 0.0 ± 0.01 | 1.0 ± 0.0 | 1.0 ± 0.0 | 0.06 ± 0.03 |
| 0.1 | names | 0.0 ± 0.01 | 1.0 ± 0.0 | 0.92 ± 0.05 | 0.06 ± 0.02 |
| 0.25 | ideal | 0.0 ± 0.01 | 1.0 ± 0.0 | 1.0 ± 0.0 | 0.06 ± 0.01 |
| 0.25 | names | 0.0 ± 0.01 | 1.0 ± 0.0 | 0.76 ± 0.09 | 0.05 ± 0.02 |

## F - Omonimi (x = quota di persone con un omonimo), k = 4; ER ideale vs ER per nome: accuracy, query multi-source

| x | er | BASE | BASE+seed | ER+seed | ER-pool |
|---|---|---|---|---|---|
| 0.0 | ideal | 0.03 ± 0.01 | 0.54 ± 0.06 | 1.0 ± 0.0 | 0.04 ± 0.01 |
| 0.0 | names | 0.03 ± 0.01 | 0.54 ± 0.06 | 1.0 ± 0.0 | 0.04 ± 0.01 |
| 0.1 | ideal | 0.03 ± 0.01 | 0.54 ± 0.06 | 1.0 ± 0.0 | 0.03 ± 0.01 |
| 0.1 | names | 0.03 ± 0.01 | 0.54 ± 0.06 | 0.9 ± 0.05 | 0.03 ± 0.01 |
| 0.25 | ideal | 0.03 ± 0.01 | 0.54 ± 0.06 | 1.0 ± 0.0 | 0.03 ± 0.02 |
| 0.25 | names | 0.03 ± 0.01 | 0.54 ± 0.06 | 0.76 ± 0.07 | 0.02 ± 0.02 |

## F - Un indice per fonte, k = 4: accuracy, query single-source

| x | BASE | BASE split, merged | BASE split, k/2 each | ER-pool | ER-pool split, k/2 each |
|---|---|---|---|---|---|
| 0.0 | 0.02 ± 0.03 | 0.02 ± 0.03 | 0.0 ± 0.01 | 0.18 ± 0.07 | 0.08 ± 0.06 |

## F - Un indice per fonte, k = 4: accuracy, query multi-source

| x | BASE | BASE split, merged | BASE split, k/2 each | ER-pool | ER-pool split, k/2 each |
|---|---|---|---|---|---|
| 0.0 | 0.08 ± 0.04 | 0.08 ± 0.04 | 0.06 ± 0.04 | 0.11 ± 0.03 | 0.04 ± 0.03 |

## F - Quasi-duplicati e reranking con varietà, k = 2 (x = quota eps): completezza, query single-source

| x | BASE+seed | ER+seed | ER+seed, source variety | ER+seed, MMR |
|---|---|---|---|---|
| 0.0 | 1.0 ± 0.0 | 1.0 ± 0.0 | 1.0 ± 0.0 | 1.0 ± 0.0 |
| 0.25 | 0.77 ± 0.07 | 0.77 ± 0.07 | 0.77 ± 0.07 | 1.0 ± 0.0 |
| 0.5 | 0.61 ± 0.11 | 0.61 ± 0.11 | 0.61 ± 0.11 | 1.0 ± 0.0 |

## F - Quasi-duplicati e reranking con varietà, k = 2 (x = quota eps): completezza, query multi-source

| x | BASE+seed | ER+seed | ER+seed, source variety | ER+seed, MMR |
|---|---|---|---|---|
| 0.0 | 0.54 ± 0.06 | 1.0 ± 0.0 | 1.0 ± 0.0 | 1.0 ± 0.0 |
| 0.25 | 0.54 ± 0.06 | 0.88 ± 0.02 | 1.0 ± 0.0 | 1.0 ± 0.0 |
| 0.5 | 0.54 ± 0.06 | 0.76 ± 0.05 | 1.0 ± 0.0 | 1.0 ± 0.0 |

## F - Retriever lessicale e ibrido, per k: accuracy, query single-source

| k | BASE | BM25 | BM25 + ER | Hybrid | Hybrid + ER | ER+seed |
|---|---|---|---|---|---|---|
| 2 | 0.0 ± 0.01 | 1.0 ± 0.0 | 1.0 ± 0.0 | 0.32 ± 0.09 | 0.8 ± 0.04 | 1.0 ± 0.0 |
| 4 | 0.02 ± 0.03 | 1.0 ± 0.0 | 1.0 ± 0.0 | 0.53 ± 0.04 | 0.92 ± 0.04 | 1.0 ± 0.0 |
| 8 | 0.05 ± 0.03 | 1.0 ± 0.0 | 1.0 ± 0.0 | 0.76 ± 0.07 | 0.97 ± 0.02 | 1.0 ± 0.0 |

## F - Retriever lessicale e ibrido, per k: accuracy, query multi-source

| k | BASE | BM25 | BM25 + ER | Hybrid | Hybrid + ER | ER+seed |
|---|---|---|---|---|---|---|
| 2 | 0.06 ± 0.04 | 0.54 ± 0.06 | 1.0 ± 0.0 | 0.32 ± 0.05 | 0.5 ± 0.05 | 1.0 ± 0.0 |
| 4 | 0.08 ± 0.04 | 0.54 ± 0.06 | 1.0 ± 0.0 | 0.43 ± 0.05 | 0.6 ± 0.03 | 1.0 ± 0.0 |
| 8 | 0.1 ± 0.04 | 0.54 ± 0.06 | 1.0 ± 0.0 | 0.46 ± 0.06 | 0.78 ± 0.02 | 1.0 ± 0.0 |

## F - Retriever lessicale e ibrido, per k: trova_paziente, query single-source

| k | BASE | BM25 | BM25 + ER | Hybrid | Hybrid + ER | ER+seed |
|---|---|---|---|---|---|---|
| 2 | 0.18 ± 0.07 | 1.0 ± 0.0 | 1.0 ± 0.0 | 0.92 ± 0.04 | 0.8 ± 0.04 | 1.0 ± 0.0 |
| 4 | 0.26 ± 0.07 | 1.0 ± 0.0 | 1.0 ± 0.0 | 0.97 ± 0.03 | 0.92 ± 0.04 | 1.0 ± 0.0 |
| 8 | 0.35 ± 0.07 | 1.0 ± 0.0 | 1.0 ± 0.0 | 0.99 ± 0.01 | 0.97 ± 0.02 | 1.0 ± 0.0 |

## F - Retriever lessicale e ibrido, per k: trova_paziente, query multi-source

| k | BASE | BM25 | BM25 + ER | Hybrid | Hybrid + ER | ER+seed |
|---|---|---|---|---|---|---|
| 2 | 0.11 ± 0.03 | 1.0 ± 0.0 | 1.0 ± 0.0 | 0.6 ± 0.03 | 0.5 ± 0.05 | 1.0 ± 0.0 |
| 4 | 0.14 ± 0.05 | 1.0 ± 0.0 | 1.0 ± 0.0 | 0.78 ± 0.02 | 0.6 ± 0.03 | 1.0 ± 0.0 |
| 8 | 0.19 ± 0.03 | 1.0 ± 0.0 | 1.0 ± 0.0 | 0.86 ± 0.04 | 0.78 ± 0.02 | 1.0 ± 0.0 |

## G - Testi variati e secondo embedding, k = 4: trova_paziente, query single-source

| modello | condizione | BASE | ER-pool | BM25 | BM25 + ER | Hybrid | Hybrid + ER | BASE+seed | ER+seed |
|---|---|---|---|---|---|---|---|---|---|
| MiniLM | fisso | 0.26 ± 0.07 | 0.18 ± 0.07 | 1.0 ± 0.0 | 1.0 ± 0.0 | 0.97 ± 0.03 | 0.92 ± 0.04 | 1.0 ± 0.0 | 1.0 ± 0.0 |
| MiniLM | variato | 0.17 ± 0.02 | 0.12 ± 0.03 | 1.0 ± 0.0 | 1.0 ± 0.0 | 0.71 ± 0.11 | 0.6 ± 0.11 | 1.0 ± 0.0 | 1.0 ± 0.0 |
| MiniLM | refusi | 0.08 ± 0.03 | 0.06 ± 0.02 | 0.96 ± 0.05 | 0.96 ± 0.05 | 0.61 ± 0.07 | 0.53 ± 0.06 | 1.0 ± 0.0 | 1.0 ± 0.0 |
| MiniLM | nome | 0.25 ± 0.06 | 0.18 ± 0.05 | 1.0 ± 0.0 | 1.0 ± 0.0 | 0.6 ± 0.06 | 0.54 ± 0.09 | 1.0 ± 0.0 | 1.0 ± 0.0 |
| E5-small | fisso | 0.96 ± 0.02 | 0.88 ± 0.03 | 1.0 ± 0.0 | 1.0 ± 0.0 | 1.0 ± 0.0 | 1.0 ± 0.0 | 1.0 ± 0.0 | 1.0 ± 0.0 |
| E5-small | variato | 0.62 ± 0.06 | 0.52 ± 0.05 | 1.0 ± 0.0 | 1.0 ± 0.0 | 0.98 ± 0.02 | 0.95 ± 0.05 | 1.0 ± 0.0 | 1.0 ± 0.0 |
| E5-small | refusi | 0.63 ± 0.03 | 0.54 ± 0.06 | 0.96 ± 0.05 | 0.96 ± 0.05 | 0.92 ± 0.08 | 0.9 ± 0.09 | 1.0 ± 0.0 | 1.0 ± 0.0 |
| E5-small | nome | 0.6 ± 0.1 | 0.5 ± 0.08 | 1.0 ± 0.0 | 1.0 ± 0.0 | 0.91 ± 0.07 | 0.86 ± 0.06 | 1.0 ± 0.0 | 1.0 ± 0.0 |

## G - Testi variati e secondo embedding, k = 4: trova_paziente, query multi-source

| modello | condizione | BASE | ER-pool | BM25 | BM25 + ER | Hybrid | Hybrid + ER | BASE+seed | ER+seed |
|---|---|---|---|---|---|---|---|---|---|
| MiniLM | fisso | 0.14 ± 0.05 | 0.11 ± 0.03 | 1.0 ± 0.0 | 1.0 ± 0.0 | 0.78 ± 0.02 | 0.6 ± 0.03 | 1.0 ± 0.0 | 1.0 ± 0.0 |
| MiniLM | variato | 0.08 ± 0.03 | 0.06 ± 0.02 | 1.0 ± 0.0 | 1.0 ± 0.0 | 0.5 ± 0.1 | 0.42 ± 0.1 | 1.0 ± 0.0 | 1.0 ± 0.0 |
| MiniLM | refusi | 0.08 ± 0.05 | 0.06 ± 0.05 | 0.8 ± 0.07 | 0.8 ± 0.07 | 0.41 ± 0.06 | 0.36 ± 0.04 | 1.0 ± 0.0 | 1.0 ± 0.0 |
| MiniLM | nome | 0.26 ± 0.1 | 0.21 ± 0.09 | 1.0 ± 0.0 | 1.0 ± 0.0 | 0.58 ± 0.11 | 0.54 ± 0.1 | 1.0 ± 0.0 | 1.0 ± 0.0 |
| E5-small | fisso | 0.82 ± 0.1 | 0.72 ± 0.09 | 1.0 ± 0.0 | 1.0 ± 0.0 | 1.0 ± 0.0 | 0.99 ± 0.01 | 1.0 ± 0.0 | 1.0 ± 0.0 |
| E5-small | variato | 0.37 ± 0.04 | 0.3 ± 0.06 | 1.0 ± 0.0 | 1.0 ± 0.0 | 0.9 ± 0.05 | 0.84 ± 0.03 | 1.0 ± 0.0 | 1.0 ± 0.0 |
| E5-small | refusi | 0.4 ± 0.07 | 0.34 ± 0.05 | 0.8 ± 0.07 | 0.8 ± 0.07 | 0.72 ± 0.1 | 0.66 ± 0.1 | 1.0 ± 0.0 | 1.0 ± 0.0 |
| E5-small | nome | 0.65 ± 0.06 | 0.51 ± 0.07 | 1.0 ± 0.0 | 1.0 ± 0.0 | 0.92 ± 0.04 | 0.88 ± 0.02 | 1.0 ± 0.0 | 1.0 ± 0.0 |

## G - Testi variati e secondo embedding, k = 4: accuracy, query single-source

| modello | condizione | BASE | ER-pool | BM25 | BM25 + ER | Hybrid | Hybrid + ER | BASE+seed | ER+seed |
|---|---|---|---|---|---|---|---|---|---|
| MiniLM | fisso | 0.02 ± 0.03 | 0.18 ± 0.07 | 1.0 ± 0.0 | 1.0 ± 0.0 | 0.53 ± 0.04 | 0.92 ± 0.04 | 1.0 ± 0.0 | 1.0 ± 0.0 |
| MiniLM | variato | 0.0 ± 0.0 | 0.12 ± 0.03 | 1.0 ± 0.0 | 1.0 ± 0.0 | 0.33 ± 0.09 | 0.6 ± 0.11 | 1.0 ± 0.0 | 1.0 ± 0.0 |
| MiniLM | refusi | 0.0 ± 0.01 | 0.06 ± 0.02 | 0.63 ± 0.04 | 0.96 ± 0.05 | 0.23 ± 0.03 | 0.53 ± 0.06 | 1.0 ± 0.0 | 1.0 ± 0.0 |
| MiniLM | nome | 0.06 ± 0.01 | 0.18 ± 0.05 | 1.0 ± 0.0 | 1.0 ± 0.0 | 0.28 ± 0.03 | 0.54 ± 0.09 | 1.0 ± 0.0 | 1.0 ± 0.0 |
| E5-small | fisso | 0.69 ± 0.06 | 0.88 ± 0.03 | 1.0 ± 0.0 | 1.0 ± 0.0 | 1.0 ± 0.0 | 1.0 ± 0.0 | 1.0 ± 0.0 | 1.0 ± 0.0 |
| E5-small | variato | 0.22 ± 0.08 | 0.52 ± 0.05 | 1.0 ± 0.0 | 1.0 ± 0.0 | 0.84 ± 0.06 | 0.95 ± 0.05 | 1.0 ± 0.0 | 1.0 ± 0.0 |
| E5-small | refusi | 0.14 ± 0.07 | 0.54 ± 0.06 | 0.63 ± 0.04 | 0.96 ± 0.05 | 0.57 ± 0.07 | 0.9 ± 0.09 | 1.0 ± 0.0 | 1.0 ± 0.0 |
| E5-small | nome | 0.23 ± 0.04 | 0.5 ± 0.08 | 1.0 ± 0.0 | 1.0 ± 0.0 | 0.62 ± 0.05 | 0.86 ± 0.06 | 1.0 ± 0.0 | 1.0 ± 0.0 |

## G - Testi variati e secondo embedding, k = 4: accuracy, query multi-source

| modello | condizione | BASE | ER-pool | BM25 | BM25 + ER | Hybrid | Hybrid + ER | BASE+seed | ER+seed |
|---|---|---|---|---|---|---|---|---|---|
| MiniLM | fisso | 0.08 ± 0.04 | 0.11 ± 0.03 | 0.54 ± 0.06 | 1.0 ± 0.0 | 0.43 ± 0.05 | 0.6 ± 0.03 | 0.54 ± 0.06 | 1.0 ± 0.0 |
| MiniLM | variato | 0.03 ± 0.03 | 0.06 ± 0.02 | 0.54 ± 0.06 | 1.0 ± 0.0 | 0.29 ± 0.05 | 0.42 ± 0.1 | 0.54 ± 0.06 | 1.0 ± 0.0 |
| MiniLM | refusi | 0.04 ± 0.03 | 0.06 ± 0.05 | 0.43 ± 0.04 | 0.8 ± 0.07 | 0.22 ± 0.06 | 0.36 ± 0.04 | 0.54 ± 0.06 | 1.0 ± 0.0 |
| MiniLM | nome | 0.06 ± 0.04 | 0.21 ± 0.09 | 0.54 ± 0.06 | 1.0 ± 0.0 | 0.22 ± 0.03 | 0.54 ± 0.1 | 0.54 ± 0.06 | 1.0 ± 0.0 |
| E5-small | fisso | 0.42 ± 0.09 | 0.72 ± 0.09 | 0.54 ± 0.06 | 1.0 ± 0.0 | 0.54 ± 0.06 | 0.99 ± 0.01 | 0.54 ± 0.06 | 1.0 ± 0.0 |
| E5-small | variato | 0.18 ± 0.08 | 0.3 ± 0.06 | 0.54 ± 0.06 | 1.0 ± 0.0 | 0.5 ± 0.05 | 0.84 ± 0.03 | 0.54 ± 0.06 | 1.0 ± 0.0 |
| E5-small | refusi | 0.2 ± 0.05 | 0.34 ± 0.05 | 0.43 ± 0.04 | 0.8 ± 0.07 | 0.37 ± 0.06 | 0.66 ± 0.1 | 0.54 ± 0.06 | 1.0 ± 0.0 |
| E5-small | nome | 0.18 ± 0.1 | 0.51 ± 0.07 | 0.54 ± 0.06 | 1.0 ± 0.0 | 0.38 ± 0.09 | 0.88 ± 0.02 | 0.54 ± 0.06 | 1.0 ± 0.0 |

## H - ER calcolata dall'anagrafe (Fellegi–Sunter), k = 4

Soglie dal dataset di addestramento (seed 100): t* = 2.38 (F1 massimo), zona di revisione [4.31, 8.17].

| t | linkage_precision | linkage_recall | n_link | errore_conteggio |
|---|---|---|---|---|
| revisione | 0.992 | 0.994 | 250.4 | -0.0 |
| -14.0 | 0.541 | 0.998 | 461.8 | -0.1 |
| -12.0 | 0.571 | 0.998 | 436.8 | -0.088 |
| -10.0 | 0.571 | 0.998 | 436.8 | -0.088 |
| -8.0 | 0.726 | 0.998 | 343.6 | -0.041 |
| -6.0 | 0.844 | 0.998 | 295.6 | -0.02 |
| -4.0 | 0.844 | 0.998 | 295.6 | -0.02 |
| -2.0 | 0.972 | 0.998 | 256.8 | -0.003 |
| 0.0 | 0.972 | 0.998 | 256.8 | -0.003 |
| 2.0 | 0.972 | 0.998 | 256.8 | -0.003 |
| 2.38 | 0.972 | 0.998 | 256.8 | -0.003 |
| 4.0 | 0.976 | 0.994 | 254.4 | -0.002 |
| 4.31 | 0.976 | 0.994 | 254.4 | -0.002 |
| 6.0 | 0.987 | 0.986 | 249.6 | 0.001 |
| 8.0 | 0.992 | 0.97 | 244.4 | 0.003 |
| 8.17 | 0.996 | 0.897 | 225.2 | 0.009 |
| 10.0 | 0.995 | 0.868 | 218.0 | 0.013 |
| 12.0 | 1.0 | 0.816 | 204.0 | 0.018 |
| 14.0 | 1.0 | 0.575 | 143.8 | 0.04 |
| 16.0 | 1.0 | 0.0 | 0.0 | 0.091 |

Blocking (anno ± 1): 11548 coppie confrontate, 95.4 % in meno del confronto completo, recall del blocking 1.000. Zona di revisione: 19.4 coppie da rivedere in media.


## H - Accuracy per soglia t, query single-source (t = ideale: ER vera)

| t | BASE+seed | ER+seed | ER-pool |
|---|---|---|---|
| -14.0 | 1.0 ± 0.0 | 0.18 ± 0.09 | 0.04 ± 0.03 |
| -12.0 | 1.0 ± 0.0 | 0.28 ± 0.06 | 0.05 ± 0.04 |
| -10.0 | 1.0 ± 0.0 | 0.28 ± 0.06 | 0.05 ± 0.04 |
| -8.0 | 1.0 ± 0.0 | 0.61 ± 0.08 | 0.1 ± 0.04 |
| -6.0 | 1.0 ± 0.0 | 0.82 ± 0.07 | 0.15 ± 0.07 |
| -4.0 | 1.0 ± 0.0 | 0.82 ± 0.07 | 0.15 ± 0.07 |
| -2.0 | 1.0 ± 0.0 | 0.98 ± 0.03 | 0.18 ± 0.08 |
| 0.0 | 1.0 ± 0.0 | 0.98 ± 0.03 | 0.18 ± 0.08 |
| 2.0 | 1.0 ± 0.0 | 0.98 ± 0.03 | 0.18 ± 0.08 |
| 2.38 | 1.0 ± 0.0 | 0.98 ± 0.03 | 0.18 ± 0.08 |
| 4.0 | 1.0 ± 0.0 | 0.98 ± 0.03 | 0.18 ± 0.08 |
| 4.31 | 1.0 ± 0.0 | 0.98 ± 0.03 | 0.18 ± 0.08 |
| 6.0 | 1.0 ± 0.0 | 0.99 ± 0.01 | 0.18 ± 0.08 |
| 8.0 | 1.0 ± 0.0 | 0.99 ± 0.01 | 0.18 ± 0.08 |
| 8.17 | 1.0 ± 0.0 | 0.99 ± 0.01 | 0.18 ± 0.07 |
| 10.0 | 1.0 ± 0.0 | 0.99 ± 0.01 | 0.18 ± 0.07 |
| 12.0 | 1.0 ± 0.0 | 1.0 ± 0.0 | 0.18 ± 0.07 |
| 14.0 | 1.0 ± 0.0 | 1.0 ± 0.0 | 0.18 ± 0.07 |
| 16.0 | 1.0 ± 0.0 | 1.0 ± 0.0 | 0.19 ± 0.07 |
| ideale | 1.0 ± 0.0 | 1.0 ± 0.0 | 0.18 ± 0.07 |

## H - Accuracy per soglia t, query multi-source (t = ideale: ER vera)

| t | BASE+seed | ER+seed | ER-pool |
|---|---|---|---|
| -14.0 | 0.54 ± 0.06 | 0.99 ± 0.01 | 0.09 ± 0.01 |
| -12.0 | 0.54 ± 0.06 | 0.99 ± 0.01 | 0.1 ± 0.02 |
| -10.0 | 0.54 ± 0.06 | 0.99 ± 0.01 | 0.1 ± 0.02 |
| -8.0 | 0.54 ± 0.06 | 0.99 ± 0.01 | 0.11 ± 0.03 |
| -6.0 | 0.54 ± 0.06 | 0.99 ± 0.01 | 0.11 ± 0.03 |
| -4.0 | 0.54 ± 0.06 | 0.99 ± 0.01 | 0.11 ± 0.03 |
| -2.0 | 0.54 ± 0.06 | 1.0 ± 0.0 | 0.11 ± 0.03 |
| 0.0 | 0.54 ± 0.06 | 1.0 ± 0.0 | 0.11 ± 0.03 |
| 2.0 | 0.54 ± 0.06 | 1.0 ± 0.0 | 0.11 ± 0.03 |
| 2.38 | 0.54 ± 0.06 | 1.0 ± 0.0 | 0.11 ± 0.03 |
| 4.0 | 0.54 ± 0.06 | 0.99 ± 0.01 | 0.11 ± 0.03 |
| 4.31 | 0.54 ± 0.06 | 0.99 ± 0.01 | 0.11 ± 0.03 |
| 6.0 | 0.54 ± 0.06 | 0.99 ± 0.01 | 0.11 ± 0.03 |
| 8.0 | 0.54 ± 0.06 | 0.99 ± 0.01 | 0.11 ± 0.03 |
| 8.17 | 0.54 ± 0.06 | 0.94 ± 0.05 | 0.1 ± 0.04 |
| 10.0 | 0.54 ± 0.06 | 0.93 ± 0.06 | 0.1 ± 0.04 |
| 12.0 | 0.54 ± 0.06 | 0.9 ± 0.05 | 0.1 ± 0.04 |
| 14.0 | 0.54 ± 0.06 | 0.81 ± 0.04 | 0.08 ± 0.03 |
| 16.0 | 0.54 ± 0.06 | 0.54 ± 0.06 | 0.06 ± 0.04 |
| ideale | 0.54 ± 0.06 | 1.0 ± 0.0 | 0.11 ± 0.03 |

## H - Normalizzazione degli ID («H-37» → «H:37») sui testi con refusi: paziente trovato, k = 4

| normalizzazione | tipo | BM25 | BM25 + ER |
|---|---|---|---|
| False | multi-source | 0.8 ± 0.07 | 0.8 ± 0.07 |
| False | single-source | 0.96 ± 0.05 | 0.96 ± 0.05 |
| True | multi-source | 1.0 ± 0.0 | 1.0 ± 0.0 |
| True | single-source | 1.0 ± 0.0 | 1.0 ± 0.0 |

## L - LLM e lettore deterministico sulle stesse domande (N = 500, omega = 0.5, k = 4, 5 seed)

Accordo = quota di domande in cui l'LLM e il lettore deterministico danno lo stesso esito.

- qwen3.6: accordo 98.6 % su 2250 risposte.
- qwen3.8: accordo 96.7 % su 2250 risposte.

| tipo | alpha | sistema | qwen3.6 | qwen3.6 accordo | qwen3.8 | qwen3.8 accordo | lettore |
|---|---|---|---|---|---|---|---|
| multi-source | 0.0 | BASE | 0.18 | 1.0 | 0.18 | 1.0 | 0.18 |
| multi-source | 0.0 | BASE+seed | 1.0 | 1.0 | 0.64 | 0.64 | 1.0 |
| multi-source | 0.0 | ER+seed | 0.99 | 0.99 | 1.0 | 1.0 | 1.0 |
| multi-source | 0.0 | ER-pool | 0.13 | 1.0 | 0.09 | 0.96 | 0.13 |
| multi-source | 0.0 | ORACLE | 0.99 | 0.99 | 1.0 | 1.0 | 1.0 |
| multi-source | 0.5 | BASE | 0.06 | 1.0 | 0.06 | 1.0 | 0.06 |
| multi-source | 0.5 | BASE+seed | 0.51 | 1.0 | 0.4 | 0.89 | 0.51 |
| multi-source | 0.5 | ER+seed | 0.93 | 0.93 | 0.97 | 0.97 | 1.0 |
| multi-source | 0.5 | ER-pool | 0.07 | 0.95 | 0.06 | 0.94 | 0.12 |
| multi-source | 0.5 | ORACLE | 0.93 | 0.93 | 0.97 | 0.97 | 1.0 |
| multi-source | 1.0 | BASE | 0.0 | 1.0 | 0.0 | 1.0 | 0.0 |
| multi-source | 1.0 | BASE+seed | 0.0 | 1.0 | 0.0 | 1.0 | 0.0 |
| multi-source | 1.0 | ER+seed | 0.99 | 0.99 | 0.96 | 0.96 | 1.0 |
| multi-source | 1.0 | ER-pool | 0.04 | 0.93 | 0.07 | 0.96 | 0.11 |
| multi-source | 1.0 | ORACLE | 0.99 | 0.99 | 0.96 | 0.96 | 1.0 |
| single-source | 0.0 | BASE | 0.02 | 1.0 | 0.02 | 1.0 | 0.02 |
| single-source | 0.0 | BASE+seed | 1.0 | 1.0 | 1.0 | 1.0 | 1.0 |
| single-source | 0.0 | ER+seed | 1.0 | 1.0 | 1.0 | 1.0 | 1.0 |
| single-source | 0.0 | ER-pool | 0.18 | 1.0 | 0.18 | 1.0 | 0.18 |
| single-source | 0.0 | ORACLE | 1.0 | 1.0 | 1.0 | 1.0 | 1.0 |
| single-source | 0.5 | BASE | 0.02 | 1.0 | 0.02 | 1.0 | 0.02 |
| single-source | 0.5 | BASE+seed | 0.98 | 0.98 | 1.0 | 1.0 | 1.0 |
| single-source | 0.5 | ER+seed | 1.0 | 1.0 | 1.0 | 1.0 | 1.0 |
| single-source | 0.5 | ER-pool | 0.22 | 1.0 | 0.22 | 1.0 | 0.22 |
| single-source | 0.5 | ORACLE | 1.0 | 1.0 | 1.0 | 1.0 | 1.0 |
| single-source | 1.0 | BASE | 0.06 | 1.0 | 0.06 | 1.0 | 0.06 |
| single-source | 1.0 | BASE+seed | 1.0 | 1.0 | 1.0 | 1.0 | 1.0 |
| single-source | 1.0 | ER+seed | 1.0 | 1.0 | 1.0 | 1.0 | 1.0 |
| single-source | 1.0 | ER-pool | 0.3 | 1.0 | 0.3 | 1.0 | 0.3 |
| single-source | 1.0 | ORACLE | 1.0 | 1.0 | 1.0 | 1.0 | 1.0 |

## S - Confronti appaiati: differenza (B - A), intervallo al 95 % (bootstrap) e test di McNemar

Stesse domande nelle due condizioni. "reale" = intervallo che esclude lo zero e p < 0,05.

| gruppo | confronto A → B | metrica | A | B | B - A | IC 95 % | p | esito |
|---|---|---|---|---|---|---|---|---|
| Griglia, k = 4 | multi-source, alpha = 0: BASE+seed → ER+seed | accuracy | 1.0 | 1.0 | 0.0 | [0.0, 0.0] | 1.000 | non distinguibile |
| Griglia, k = 4 | multi-source, alpha = 0.5: BASE+seed → ER+seed | accuracy | 0.488 | 1.0 | 0.512 | [0.489, 0.536] | < 0,001 | reale |
| Griglia, k = 4 | multi-source, alpha = 1: BASE+seed → ER+seed | accuracy | 0.0 | 1.0 | 1.0 | [1.0, 1.0] | < 0,001 | reale |
| Griglia, k = 4 | single-source: BASE → ER-pool | accuracy | 0.033 | 0.208 | 0.175 | [0.165, 0.185] | < 0,001 | reale |
| Griglia, k = 4 | single-source: ER-pool → ER+seed | accuracy | 0.208 | 1.0 | 0.792 | [0.781, 0.802] | < 0,001 | reale |
| Griglia, k = 4 | multi-source: BASE → ER-pool | accuracy | 0.085 | 0.115 | 0.03 | [0.023, 0.037] | < 0,001 | reale |
| Griglia, k = 4 | multi-source: ER-pool → ER+seed | accuracy | 0.115 | 1.0 | 0.885 | [0.876, 0.893] | < 0,001 | reale |
| Falsi match, ER+seed, k = 4 | single-source: ER corretta → 25 % falsi positivi | accuracy | 1.0 | 0.785 | -0.215 | [-0.27, -0.16] | < 0,001 | reale |
| Falsi match, ER+seed, k = 4 | multi-source: ER corretta → 25 % falsi negativi | accuracy | 1.0 | 0.89 | -0.11 | [-0.155, -0.07] | < 0,001 | reale |
| Falsi match, ER+seed, k = 4 | multi-source: ER corretta → 50 % falsi negativi | accuracy | 1.0 | 0.73 | -0.27 | [-0.335, -0.21] | < 0,001 | reale |
| Quasi-duplicati, ER+seed, k = 2 | multi-source: nessun doppione → 50 % doppioni | completezza | 1.0 | 0.76 | -0.24 | [-0.305, -0.18] | < 0,001 | reale |
| Omonimi 25 %, ER+seed, k = 4 | single-source: ER ideale → ER per nome | accuracy | 1.0 | 0.765 | -0.235 | [-0.295, -0.18] | < 0,001 | reale |
| Omonimi 25 %, ER+seed, k = 4 | multi-source: ER ideale → ER per nome | accuracy | 1.0 | 0.765 | -0.235 | [-0.295, -0.18] | < 0,001 | reale |
| Indice per fonte, k = 4 | single-source: BASE → BASE split, merged | accuracy | 0.025 | 0.025 | 0.0 | [0.0, 0.0] | 1.000 | non distinguibile |
| Indice per fonte, k = 4 | single-source: BASE → BASE split, k/2 each | accuracy | 0.025 | 0.005 | -0.02 | [-0.04, -0.005] | 0.125 | non distinguibile |
| Indice per fonte, k = 4 | single-source: ER-pool → ER-pool split, k/2 each | accuracy | 0.18 | 0.075 | -0.105 | [-0.15, -0.065] | < 0,001 | reale |
| Indice per fonte, k = 4 | multi-source: BASE → BASE split, merged | accuracy | 0.075 | 0.075 | 0.0 | [0.0, 0.0] | 1.000 | non distinguibile |
| Indice per fonte, k = 4 | multi-source: BASE → BASE split, k/2 each | accuracy | 0.075 | 0.065 | -0.01 | [-0.025, 0.0] | 0.500 | non distinguibile |
| Indice per fonte, k = 4 | multi-source: ER-pool → ER-pool split, k/2 each | accuracy | 0.105 | 0.04 | -0.065 | [-0.105, -0.03] | < 0,001 | reale |
| Doppioni 50 %, k = 2 | single-source: ER+seed → ER+seed, source variety | completezza | 0.61 | 0.61 | 0.0 | [0.0, 0.0] | 1.000 | non distinguibile |
| Doppioni 50 %, k = 2 | single-source: ER+seed → ER+seed, MMR | completezza | 0.61 | 1.0 | 0.39 | [0.325, 0.455] | < 0,001 | reale |
| Doppioni 50 %, k = 2 | multi-source: ER+seed → ER+seed, source variety | completezza | 0.76 | 1.0 | 0.24 | [0.18, 0.295] | < 0,001 | reale |
| Doppioni 50 %, k = 2 | multi-source: ER+seed → ER+seed, MMR | completezza | 0.76 | 1.0 | 0.24 | [0.18, 0.3] | < 0,001 | reale |
| Ricerca per parole e ibrida, k = 4 | single-source: BASE → BM25 | accuracy | 0.025 | 1.0 | 0.975 | [0.95, 0.995] | < 0,001 | reale |
| Ricerca per parole e ibrida, k = 4 | single-source: BM25 → BM25 + ER | accuracy | 1.0 | 1.0 | 0.0 | [0.0, 0.0] | 1.000 | non distinguibile |
| Ricerca per parole e ibrida, k = 4 | single-source: BM25 + ER → ER+seed | accuracy | 1.0 | 1.0 | 0.0 | [0.0, 0.0] | 1.000 | non distinguibile |
| Ricerca per parole e ibrida, k = 4 | single-source: BM25 → Hybrid | accuracy | 1.0 | 0.535 | -0.465 | [-0.535, -0.395] | < 0,001 | reale |
| Ricerca per parole e ibrida, k = 4 | single-source: Hybrid → Hybrid + ER | accuracy | 0.535 | 0.915 | 0.38 | [0.315, 0.45] | < 0,001 | reale |
| Ricerca per parole e ibrida, k = 4 | multi-source: BASE → BM25 | accuracy | 0.075 | 0.54 | 0.465 | [0.395, 0.53] | < 0,001 | reale |
| Ricerca per parole e ibrida, k = 4 | multi-source: BM25 → BM25 + ER | accuracy | 0.54 | 1.0 | 0.46 | [0.39, 0.53] | < 0,001 | reale |
| Ricerca per parole e ibrida, k = 4 | multi-source: BM25 + ER → ER+seed | accuracy | 1.0 | 1.0 | 0.0 | [0.0, 0.0] | 1.000 | non distinguibile |
| Ricerca per parole e ibrida, k = 4 | multi-source: BM25 → Hybrid | accuracy | 0.54 | 0.43 | -0.11 | [-0.155, -0.07] | < 0,001 | reale |
| Ricerca per parole e ibrida, k = 4 | multi-source: Hybrid → Hybrid + ER | accuracy | 0.43 | 0.595 | 0.165 | [0.085, 0.245] | < 0,001 | reale |
| Testi variati e secondo embedding, k = 4 | single-source, testo fisso, semantica: MiniLM → E5-small | trova_paziente | 0.26 | 0.96 | 0.7 | [0.635, 0.76] | < 0,001 | reale |
| Testi variati e secondo embedding, k = 4 | multi-source, testo fisso, semantica: MiniLM → E5-small | trova_paziente | 0.135 | 0.825 | 0.69 | [0.625, 0.755] | < 0,001 | reale |
| Testi variati e secondo embedding, k = 4 | multi-source, semantica MiniLM: testo fisso → variato | trova_paziente | 0.135 | 0.075 | -0.06 | [-0.115, -0.005] | 0.058 | non distinguibile |
| Testi variati e secondo embedding, k = 4 | multi-source, semantica MiniLM: testo variato → nome | trova_paziente | 0.075 | 0.26 | 0.185 | [0.12, 0.25] | < 0,001 | reale |
| Testi variati e secondo embedding, k = 4 | multi-source, semantica E5-small: testo fisso → variato | trova_paziente | 0.825 | 0.37 | -0.455 | [-0.535, -0.38] | < 0,001 | reale |
| Testi variati e secondo embedding, k = 4 | multi-source, semantica E5-small: testo variato → nome | trova_paziente | 0.37 | 0.65 | 0.28 | [0.205, 0.36] | < 0,001 | reale |
| Testi variati e secondo embedding, k = 4 | multi-source, BM25: testo variato → refusi | trova_paziente | 1.0 | 0.8 | -0.2 | [-0.255, -0.145] | < 0,001 | reale |
| Testi variati e secondo embedding, k = 4 | multi-source, refusi, MiniLM: BM25 → Hybrid | trova_paziente | 0.8 | 0.405 | -0.395 | [-0.46, -0.325] | < 0,001 | reale |
| Testi variati e secondo embedding, k = 4 | multi-source, refusi, E5-small: BM25 → Hybrid | trova_paziente | 0.8 | 0.72 | -0.08 | [-0.13, -0.03] | 0.004 | reale |
| Testi variati e secondo embedding, k = 4 | multi-source, testo fisso, ER-pool: MiniLM → E5-small | accuracy | 0.105 | 0.725 | 0.62 | [0.55, 0.69] | < 0,001 | reale |
| ER calcolata dall'anagrafe, ER+seed, k = 4 | single-source: ER ideale → t* (scelta) | accuracy | 1.0 | 0.98 | -0.02 | [-0.04, -0.005] | 0.125 | non distinguibile |
| ER calcolata dall'anagrafe, ER+seed, k = 4 | multi-source: ER ideale → t* (scelta) | accuracy | 1.0 | 1.0 | 0.0 | [0.0, 0.0] | 1.000 | non distinguibile |
| ER calcolata dall'anagrafe, ER+seed, k = 4 | single-source: ER ideale → t = -8 (bassa) | accuracy | 1.0 | 0.61 | -0.39 | [-0.46, -0.325] | < 0,001 | reale |
| ER calcolata dall'anagrafe, ER+seed, k = 4 | multi-source: ER ideale → t = 12 (alta) | accuracy | 1.0 | 0.9 | -0.1 | [-0.145, -0.06] | < 0,001 | reale |
| ER calcolata dall'anagrafe, BM25, k = 4 | multi-source, testi con refusi: ID così come sono → normalizzati | trova_paziente | 0.8 | 1.0 | 0.2 | [0.145, 0.255] | < 0,001 | reale |
