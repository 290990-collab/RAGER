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
