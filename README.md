<p align="center">
  <picture>
    <source media="(prefers-color-scheme: dark)" srcset="assets/hero-dark.svg">
    <img src="assets/hero-light.svg" width="960" alt="Entity Resolution links H:3 at the hospital and P:1 at the pharmacy to the same person, so the retrieved context holds both sources and the answer becomes complete">
  </picture>
</p>

<h1 align="center">RAGER</h1>

<p align="center"><b>Same patient, two IDs, half an answer.</b><br>
A benchmark that measures when Entity Resolution makes RAG over federated sources answer correctly,
at the same context budget.</p>

<p align="center">
  <img src="https://img.shields.io/badge/python-3.12-3776ab" alt="Python 3.12">
  <img src="https://img.shields.io/badge/vector%20index-ChromaDB-1baf7a" alt="ChromaDB">
  <img src="https://img.shields.io/badge/embeddings-Sentence%20Transformers-eb6834" alt="Sentence Transformers">
  <img src="https://img.shields.io/badge/data-100%25%20synthetic-6b6a66" alt="Synthetic data">
  <a href="LICENSE"><img src="https://img.shields.io/badge/license-MIT-2a78d6" alt="MIT license"></a>
</p>

A hospital knows a patient as `H:3`. A pharmacy knows the same patient as `P:1`. Ask a RAG system which drugs
`H:3` received, and it reads the hospital record, answers "Insulin" and never sees the Aspirin on the
pharmacy side. Entity Resolution (ER) is the step that recognises `H:3` and `P:1` as one person and gives
them a shared global ID (GID). RAGER measures what that link is worth to retrieval, on 180 synthetic datasets
where the right answer is known.

## Results at a glance

Share of correct answers with 4 records in the context, mean over 5 seeds ([all tables](results/tables.md)):

| Question | Semantic search | Patient ID only | **Patient ID + linking** | Linking every hit | Perfect retrieval |
|---|---|---|---|---|---|
| Answer split across two sources | 9 % | 50 % | **100 %** | 11 % | 100 % |
| Answer in one source | 3 % | 100 % | **100 %** | 21 % | 100 % |

- **Linking pays exactly where the answer is split.** When no patient's records differ between sources,
  linking adds nothing; when half do, it adds 50 points; when all do, 100. How many patients the two
  sources share barely changes it.
- **Linking everything wastes the context.** Expanding every patient that search turns up fills the 4 slots
  with the wrong people: 11 % against 100 % for linking the patient that was asked about.
- **Never let RAG count.** Counting distinct patients from the retrieved text misses by 76–99 %.
  A `COUNT(DISTINCT gid)` on the metadata is exact.
- **Semantic search is unreliable on IDs.** With MiniLM it puts the asked-about patient in its top results
  for only 11–46 % of questions. A retrieval-trained model (E5) does better on identical sentences, 82 %,
  but falls to 37 % once the wording varies. Keyword search (BM25) finds the ID every time.
- **Computed ER works across a wide band of thresholds.** Linking from a noisy registry (name, birth year,
  town; Fellegi–Sunter with blocking) answers as well as perfect ER at the chosen threshold. Too low a
  threshold breaks single-source answers (61 %), too high breaks multi-source ones (90 %).
- **An LLM agrees.** Two local Qwen models reproduce these verdicts in 97–99 % of 2,250 grid answers
  over 5 seeds.

![When does linking the two sources pay off?](results/plots/en/fig1_when_linking_helps.png)

## Quick start

Python 3.12, CPU only. The embedding model (about 470 MB) downloads on first run.

```powershell
python -m venv .venv
.venv\Scripts\python -m pip install -r requirements.txt
.venv\Scripts\python src\minimal_benchmark.py      # seconds: the hospital/pharmacy example
.venv\Scripts\python src\experiment.py --rapido     # under a minute: reduced grid
```

On Linux or macOS use `.venv/bin/python`. Every command runs from the repository root.

| Command | Output | Time |
|---|---|---|
| `python src/dataset.py` | `data/documents.*` | seconds |
| `python src/questions.py` | `data/questions.json` | seconds |
| `python src/minimal_benchmark.py` | `results/minimal_benchmark.csv` | seconds |
| `python src/experiment.py` | `results/experiment_*.csv` (full grid) | about 20 min |
| `python src/extensions.py` | `results/extension_*.csv` | minutes |
| `python src/export_datasets.py` | `data/parametric/` | about a minute |
| `python src/analysis.py` | `results/tables.md` | seconds |
| `python src/plots.py` | `results/plots/` (Italian) and `results/plots/en/` | seconds |

Every script checks itself with `assert` and stops on failure: the generator against the paper's formulas,
the GID never in the text, ER+seed equal to BASE+seed when all evidence sits in one source.

## How it works

```
synthetic sources → documents (local_id, source, GID in metadata) → embeddings → one federated vector index
→ semantic search → [GID expansion + rerank] → context (k documents) → reader → evaluation
```

- **Embeddings**: `sentence-transformers/paraphrase-multilingual-MiniLM-L12-v2`, 384 dimensions, normalized.
- **Vector index**: one in-memory ChromaDB collection for all sources. HNSW runs single-threaded with
  `ef_search = 2000`, so top-k is deterministic and equal to exact search.
- **The GID lives in metadata only.** In the text, the embedding would do the linkage for free.
- **ER is a parameter, not an algorithm.** The GID is known by construction. The minimal example has four
  alternative partitions; imperfect ER is simulated with false-negative and false-positive links, then
  computed from a synthetic registry with a Fellegi–Sunter score and a threshold.

### Systems

All of them return at most k documents.

| In the figures | Code name | Document selection |
|---|---|---|
| Semantic search | `BASE` | semantic top-k |
| Patient ID only | `BASE+seed` | documents of the local ID named in the query, reranked; the fair baseline |
| Patient ID + linking | `ER+seed` | documents of the seed's GID, reranked |
| Linking every hit | `ER-pool` | BASE top-k, then every document of the GIDs found, entity by entity |
| Perfect retrieval | `ORACLE` | ground-truth evidence, reranked (upper bound) |

### Readers

- **Deterministic reader** (main measure): collects the attributes of the documents that belong to the
  queried entity, by local ID without ER and by GID with ER. It isolates retrieval from generation.
- **LLM reader** (optional): same prompt, model, temperature 0, seed 0 and 400-token limit for every system.
  With ER, each document in the context carries its entity label.

### Metrics

| Metric | Definition |
|---|---|
| Recall@k | relevant documents retrieved / relevant documents |
| Precision@k | relevant documents retrieved / documents retrieved |
| Completeness | 1 if every required piece of evidence is covered |
| Accuracy | 1 if the reader's answer equals the ground truth exactly |
| Cost | documents and tokens in the context |
| Disambiguation | BASE's top-k contains the seed's entity |

Means are taken over the queries of a seed, then reported as mean ± standard deviation over 5 seeds.

## Experiments

| Study | Setup |
|---|---|
| Minimal example | 8 clinical events, 2 sources, 4 ER partitions; entity-centric, multi-hop, counting and negative queries |
| Parametric grid | N ∈ {100, 500, 1000} × ω ∈ {0, .25, .5, .75} × α ∈ {0, .5, 1} × 5 seeds = 180 datasets; k ∈ {2, 4, 8}; 40 single-source, 40 multi-source and 6 counting queries per dataset |
| Robustness (N = 500, ω = α = 0.5) | dirty ER (several local IDs per person), false matches, near-duplicates, wrong IDs in text |
| Wording and model (same setting) | 3 sentence forms per source, 5 question paraphrases, typos in 20 % of records, patient named by name; MiniLM and multilingual E5-small |
| Computed ER (same setting) | registry with typos, blocking on birth year ± 1, Fellegi–Sunter weights from a separate training set, one-to-one links above a threshold t swept from −14 to 16; ID normalization for BM25 |
| LLM generation | minimal example plus a sample of the grid, two local models |

Generator: two sources with N local identities each, S = round(ωN) shared entities, V = 2N − S global
entities and overcount factor γ = 2N / (2N − S). Each entity has two events; for a share α of the shared
entities the two sources report different drugs, so a complete answer needs both.

| Hypothesis | Evidence |
|---|---|
| H1. ER improves recall of evidence spread over sources for the same entity | T1, T2, G1 |
| H2. The benefit grows with complementarity and with queries that need several sources | T3, T4, G1, G2 |
| H3. Indiscriminate GID expansion wastes the budget | T6, robustness, G3 |
| H4. The improvement does not depend on overlap ω alone | T4, T5, G2 |

<table>
  <tr>
    <td><img src="results/plots/en/fig2_overlap_does_not_matter.png" alt="Does it matter how many patients the sources share?"></td>
    <td><img src="results/plots/en/fig4_strategies_without_id.png" alt="Given only the question, which strategy answers?"></td>
  </tr>
  <tr>
    <td><img src="results/plots/en/fig3_semantic_search_misses_ids.png" alt="Does semantic search find the patient named in the question?"></td>
    <td><img src="results/plots/en/fig5_er_mistakes.png" alt="What happens when Entity Resolution makes mistakes?"></td>
  </tr>
</table>

<table>
  <tr>
    <td><img src="results/plots/en/fig6_homonyms.png" alt="What if ER links patients by name?"></td>
    <td><img src="results/plots/en/fig7_duplicates.png" alt="Duplicates take up slots in the context: can it be avoided?"></td>
  </tr>
</table>

![Can RAG count how many patients received a drug?](results/plots/en/fig8_counting.png)

![Do these results depend on the wording and the model?](results/plots/en/fig9_wording_and_model.png)

![What if the links must be computed from the registry, with a threshold?](results/plots/en/fig10_er_threshold.png)

## Optional: LLM generation

Any OpenAI-compatible endpoint works (`/v1/chat/completions`), for example a local llama.cpp server.

| Variable | Meaning |
|---|---|
| `LLM_URL` | endpoint, default `http://127.0.0.1:8080/v1` |
| `LLM_MODEL` | model id as listed by `GET /v1/models` |
| `LLM_KEY_FILE` | optional file holding the API key; the key never goes in code |
| `LLM_TAG` | suffix of the output files |

```powershell
$env:LLM_MODEL = "<model id>"; $env:LLM_TAG = "mymodel"
python src/llm.py tutto        # or: minimo | parametrico
```

Responses are cached in `results/llm_cache.jsonl`, keyed by model, parameters and prompt. With the committed
cache, a rerun reproduces the published LLM results without calling a model.

## Repository layout

```
src/
  rag.py                 core: encoder, index, systems, readers, metrics
  dataset.py             minimal example documents
  questions.py           minimal example questions and ground truth
  minimal_benchmark.py   benchmark on the minimal example
  generator.py           parametric generator (N, ω, α, dirty records)
  experiment.py          parametric grid
  extensions.py          robustness studies
  export_datasets.py     exports the 180 generated datasets
  analysis.py            summary tables
  plots.py               figures 1–10
  followups.py           follow-up studies (homonyms, per-source indices, diversity, keyword search)
  stats.py               paired tests and 95 % intervals
  robustness_text.py     varied wording, typos, names, second embedding model
  er_real.py             ER computed from a registry: blocking, Fellegi–Sunter, threshold
  llm.py                 optional LLM generation
data/
  documents.{json,csv}   minimal example
  questions.json         minimal example questions
  parametric/            180 datasets: documents.csv, questions.json
results/
  *.csv                  per-query and aggregated metrics
  tables.md              summary tables T1–T8 and robustness tables
  plots/                 figures 1–10 (Italian), plots/en/ (English)
  llm_cache.jsonl        cached LLM responses
assets/                  README banner and its generator
```

| Field | Meaning |
|---|---|
| `document_id` / `doc_id` | one document = one event |
| `source` | data owner (`H` hospital, `P` pharmacy) |
| `local_id` | person ID inside its source |
| `gid` | global entity ID (metadata only) |
| `farmaco`, `quantita` | drug and quantity of the event |
| `tipologia` / `tipo` | query type: single-source, multi-source, counting |

Column names and identifiers are in Italian; comments are in English.

## Reproducibility

- Seeds: datasets use `s ∈ {0,…,4}`, question sampling `1000 + s`, robustness perturbations `2000 + s`.
- Library versions are pinned in [`requirements.txt`](requirements.txt).
- Deterministic HNSW search; LLM at temperature 0, seed 0.
- Every comparison uses the same queries, the same budget k and the same model.

## Scope

RAGER isolates one question: what a correct link between local IDs is worth to retrieval. It uses simple
text templates, one embedding model and two sources, and starts from ideal ER; false positives are drawn
between non-shared entities, and homonyms appear only as equal local numbers in different sources. A shared
stable GID is not privacy-preserving record linkage and can reveal that a person appears in several sources,
which is why every record here is synthetic.

## License

[MIT](LICENSE). Developed as a Business Intelligence course project.
