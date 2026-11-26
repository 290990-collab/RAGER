"""Core: encoder, federated ChromaDB index, retrieval systems, deterministic readers, metrics.

Systems (each returns at most k documents):
  BASE       semantic top-k
  BASE+seed  documents of the seed's local ID, reranked
  ER+seed    documents of the seed's GID, reranked
  ER-pool    BASE top-k, expanded entity by entity through their GIDs
  ORACLE     ground-truth evidence, reranked
"""
import numpy as np
import chromadb
from sentence_transformers import SentenceTransformer

MODELLO = "sentence-transformers/paraphrase-multilingual-MiniLM-L12-v2"
SISTEMI = ["BASE", "BASE+seed", "ER+seed", "ER-pool", "ORACLE"]


class Encoder:
    """Normalized embeddings, cached by text."""

    def __init__(self, modello=MODELLO, prefissi=("", "")):
        """prefissi = (query, document): some models, such as E5, expect a role prefix."""
        self.m = SentenceTransformer(modello, device="cpu")
        self.pq, self.pd = prefissi
        self.cache, self.tok = {}, {}

    def encode(self, texts, prefisso=None):
        p = self.pd if prefisso is None else prefisso
        texts = [p + t for t in texts]
        nuovi = [t for t in dict.fromkeys(texts) if t not in self.cache]
        if nuovi:
            E = self.m.encode(nuovi, batch_size=256, normalize_embeddings=True, show_progress_bar=False)
            self.cache.update(zip(nuovi, E))
        return np.stack([self.cache[t] for t in texts])

    def encode_query(self, query):
        return self.encode([query], self.pq)[0]

    def n_token(self, text):
        if text not in self.tok:
            self.tok[text] = len(self.m.tokenizer(text)["input_ids"])
        return self.tok[text]


_client = chromadb.EphemeralClient()


class Indice:
    """One index over all sources; `partizione` is the metadata key used as the ER map."""

    def __init__(self, docs, partizione, enc, nome="rag"):
        self.docs = {d["doc_id"]: d for d in docs}
        self.p, self.enc = partizione, enc
        try:
            _client.delete_collection(nome)
        except Exception:
            pass
        # Single-threaded HNSW with a wide search: deterministic and equal to exact search
        self.col = _client.create_collection(nome, configuration={
            "hnsw": {"num_threads": 1, "ef_search": 2000, "ef_construction": 400}})
        ids = [d["doc_id"] for d in docs]
        E = enc.encode([d["text"] for d in docs])
        self.E = dict(zip(ids, E))
        metas = [{"source": d["metadata"]["source"], "local_id": d["metadata"]["local_id"],
                  "farmaco": d["metadata"]["farmaco"], "gid": d["metadata"][partizione]} for d in docs]
        for i in range(0, len(ids), 4000):
            self.col.add(ids=ids[i:i + 4000], documents=[d["text"] for d in docs[i:i + 4000]],
                         embeddings=E[i:i + 4000].tolist(), metadatas=metas[i:i + 4000])
        self.mappa_er = {d["metadata"]["local_id"]: d["metadata"][partizione] for d in docs}
        self._where, self._q = {}, {}

    def meta(self, doc_id):
        return self.docs[doc_id]["metadata"]

    def gid(self, doc_id):
        return self.docs[doc_id]["metadata"][self.p]

    def qvec(self, query):
        if query not in self._q:
            self._q[query] = self.enc.encode_query(query)
        return self._q[query]

    def cerca(self, query, n):
        """Semantic search."""
        r = self.col.query(query_embeddings=[self.qvec(query).tolist()], n_results=min(n, len(self.docs)))
        return r["ids"][0]

    def where(self, chiave, valore):
        if (chiave, valore) not in self._where:
            self._where[(chiave, valore)] = self.col.get(where={chiave: valore}, include=[])["ids"]
        return self._where[(chiave, valore)]

    def rerank(self, query, ids, k):
        """Reranks by cosine similarity to the query, ties by doc_id."""
        q = self.qvec(query)
        return sorted(ids, key=lambda i: (-float(self.E[i] @ q), i))[:k]


# ---------------------------------------------------------------- systems
def sys_base(ix, query, k, seed=None, gold=None):
    return ix.cerca(query, k)


def sys_base_seed(ix, query, k, seed=None, gold=None):
    if seed is None:
        return None
    return ix.rerank(query, ix.where("local_id", seed), k)


def sys_er_seed(ix, query, k, seed=None, gold=None):
    if seed is None:
        return None
    return ix.rerank(query, ix.where("gid", ix.mappa_er[seed]), k)


def sys_er_pool(ix, query, k, seed=None, gold=None):
    """BASE top-k, then the entities found, in order of their best rank, fill the budget with their documents."""
    out = []
    for doc in ix.cerca(query, k):
        for m in ix.rerank(query, ix.where("gid", ix.gid(doc)), k):
            if len(out) < k and m not in out:
                out.append(m)
    return out


def sys_oracle(ix, query, k, seed=None, gold=None):
    return ix.rerank(query, list(gold), k)


FUNZIONI = dict(zip(SISTEMI, [sys_base, sys_base_seed, sys_er_seed, sys_er_pool, sys_oracle]))
USA_ER = {"BASE": False, "BASE+seed": False, "ER+seed": True, "ER-pool": True, "ORACLE": True}


# ---------------------------------------------------------------- deterministic readers
# Without ER a document belongs to the seed if its text names the local ID; with ER the GID decides.
def leggi_entity(ix, ret, seed, er):
    if er:
        g = ix.mappa_er[seed]
        att = [d for d in ret if ix.gid(d) == g]
    else:
        att = [d for d in ret if ix.meta(d).get("lid_testo", ix.meta(d)["local_id"]) == seed]
    return sorted({ix.meta(d)["farmaco"] for d in att})


def leggi_multihop(ix, ret, f1, f2, er):
    """Entities with f1 and f2 in different sources among the retrieved documents."""
    gruppi = {}
    for d in ret:
        m = ix.meta(d)
        g = ix.gid(d) if er else m["local_id"]
        gruppi.setdefault(g, []).append((m["farmaco"], m["source"]))
    out = []
    for g, ev in gruppi.items():
        s1 = {s for f, s in ev if f == f1}
        s2 = {s for f, s in ev if f == f2}
        if any(a != b for a in s1 for b in s2):
            out.append(g)
    return sorted(out)


def leggi_conteggio(ix, ret, farmaco, er):
    """Distinct patients counted from the retrieved text, as a RAG would."""
    return len({(ix.gid(d) if er else ix.meta(d)["local_id"]) for d in ret if ix.meta(d)["farmaco"] == farmaco})


# ---------------------------------------------------------------- metrics
def recall_at_k(ret, rel):
    rel = set(rel)
    if not rel:
        return 1.0 if not ret else 0.0
    return len(set(ret) & rel) / len(rel)


def precision_at_k(ret, rel):
    if not ret:
        return 1.0 if not rel else 0.0
    return len(set(ret) & set(rel)) / len(ret)


def completezza(ix, ret, gold, farmaci_attesi):
    """Every drug of the answer is covered by at least one relevant document."""
    coperti = {ix.meta(d)["farmaco"] for d in ret if d in set(gold)}
    return float(set(farmaci_attesi) <= coperti)


def costo(ix, ret):
    return len(ret), sum(ix.enc.n_token(ix.docs[d]["text"]) for d in ret)
