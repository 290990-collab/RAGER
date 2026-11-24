"""Nucleo del prototipo: indice ChromaDB, sistemi di retrieval, lettori deterministici, metriche.

Riferimenti: traccia Sez. 3 (indice federato unico), 7 (baseline), 8 (espansione per GID),
9 (metriche), 12 (seed leakage e budget).

Sistemi (tutti restituiscono al massimo k documenti: stesso budget, Sez. 12):
  BASE       ricerca semantica top-k (Sez. 7)
  BASE+seed  [MIO] documenti dell'ID locale del seed, riordinati: contrappeso equo di ER+seed
  ER+seed    documenti del GID del seed, riordinati (Sez. 8)
  ER-pool    [MIO] top-k di BASE -> GID dei documenti trovati -> espansione e reranking per entita'
  ORACLE     evidenze della ground truth, riordinate (Abstract)
"""
import numpy as np
import chromadb
from sentence_transformers import SentenceTransformer

MODELLO = "sentence-transformers/paraphrase-multilingual-MiniLM-L12-v2"
SISTEMI = ["BASE", "BASE+seed", "ER+seed", "ER-pool", "ORACLE"]


class Encoder:
    """Embedding normalizzati con cache sul testo (stesso testo -> stesso vettore)."""

    def __init__(self):
        self.m = SentenceTransformer(MODELLO, device="cpu")
        self.cache, self.tok = {}, {}

    def encode(self, texts):
        nuovi = [t for t in dict.fromkeys(texts) if t not in self.cache]
        if nuovi:
            E = self.m.encode(nuovi, batch_size=256, normalize_embeddings=True, show_progress_bar=False)
            self.cache.update(zip(nuovi, E))
        return np.stack([self.cache[t] for t in texts])

    def n_token(self, text):
        if text not in self.tok:
            self.tok[text] = len(self.m.tokenizer(text)["input_ids"])
        return self.tok[text]


_client = chromadb.EphemeralClient()


class Indice:
    """Indice federato unico (Sez. 3): il campo `source` conserva la provenienza,
    il GID sta solo nei metadati (chiave `gid`), mai nel testo.

    partizione = chiave dei metadati usata come mappa ER (es. "gid_1", oppure "gid_er" con falsi match).
    """

    def __init__(self, docs, partizione, enc, nome="rag"):
        self.docs = {d["doc_id"]: d for d in docs}
        self.p, self.enc = partizione, enc
        try:
            _client.delete_collection(nome)
        except Exception:
            pass
        # [MIO] HNSW costruito con un solo thread e ricerca ampia: con i valori predefiniti ChromaDB
        # restituiva top-k diversi ricostruendo lo stesso indice (3 query su 80); cosi' e' deterministico
        # e coincide con la ricerca esatta (verificato su N = 1000).
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
        # Mappa ER: identita' locale -> GID (nota per costruzione, Sez. 8)
        self.mappa_er = {d["metadata"]["local_id"]: d["metadata"][partizione] for d in docs}
        self._where, self._q = {}, {}

    def meta(self, doc_id):
        return self.docs[doc_id]["metadata"]

    def gid(self, doc_id):
        return self.docs[doc_id]["metadata"][self.p]

    def qvec(self, query):
        if query not in self._q:
            self._q[query] = self.enc.encode([query])[0]
        return self._q[query]

    def cerca(self, query, n):
        """Ricerca semantica (embedding normalizzati: ordine L2 = ordine coseno)."""
        r = self.col.query(query_embeddings=[self.qvec(query).tolist()], n_results=min(n, len(self.docs)))
        return r["ids"][0]

    def where(self, chiave, valore):
        if (chiave, valore) not in self._where:
            self._where[(chiave, valore)] = self.col.get(where={chiave: valore}, include=[])["ids"]
        return self._where[(chiave, valore)]

    def rerank(self, query, ids, k):
        """Riordino per similarita' coseno con la query (Sez. 8); a parita', per doc_id."""
        q = self.qvec(query)
        return sorted(ids, key=lambda i: (-float(self.E[i] @ q), i))[:k]


# ---------------------------------------------------------------- sistemi
def sys_base(ix, query, k, seed=None, gold=None):
    return ix.cerca(query, k)


def sys_base_seed(ix, query, k, seed=None, gold=None):
    if seed is None:
        return None                      # non applicabile senza seed
    return ix.rerank(query, ix.where("local_id", seed), k)


def sys_er_seed(ix, query, k, seed=None, gold=None):
    if seed is None:
        return None
    return ix.rerank(query, ix.where("gid", ix.mappa_er[seed]), k)


def sys_er_pool(ix, query, k, seed=None, gold=None):
    """[MIO] Stesso accesso di BASE (solo la query): candidati = top-k di BASE.
    Le entita' sono ordinate per il miglior rango di un loro documento fra i candidati;
    il budget k si riempie entita' per entita' con i loro documenti riordinati."""
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


# ---------------------------------------------------------------- lettori deterministici [MIO]
# Simulano un lettore ideale senza LLM (Sez. 9: valutazione senza generazione).
# Senza ER un documento si attribuisce al seed solo se ne riporta l'ID locale;
# con ER si usa la mappa ER (GID nei metadati).
def leggi_entity(ix, ret, seed, er):
    if er:
        g = ix.mappa_er[seed]
        att = [d for d in ret if ix.gid(d) == g]
    else:
        # senza ER si legge l'ID scritto nel testo (diverso dal vero solo con errori sugli ID, punto E)
        att = [d for d in ret if ix.meta(d).get("lid_testo", ix.meta(d)["local_id"]) == seed]
    return sorted({ix.meta(d)["farmaco"] for d in att})


def leggi_multihop(ix, ret, f1, f2, er):
    """Entita' con f1 e f2 su fonti distinte fra i documenti recuperati."""
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
    """Conteggio 'alla RAG' (quello che farebbe un LLM sul contesto): NON e' il metodo corretto."""
    return len({(ix.gid(d) if er else ix.meta(d)["local_id"]) for d in ret if ix.meta(d)["farmaco"] == farmaco})


# ---------------------------------------------------------------- metriche (Sez. 9)
def recall_at_k(ret, rel):
    rel = set(rel)
    if not rel:
        return 1.0 if not ret else 0.0      # definizione della traccia, Sez. 9
    return len(set(ret) & rel) / len(rel)


def precision_at_k(ret, rel):
    if not ret:
        return 1.0 if not rel else 0.0
    return len(set(ret) & set(rel)) / len(ret)


def completezza(ix, ret, gold, farmaci_attesi):
    """Evidenze obbligatorie: almeno un documento pertinente per ogni farmaco della risposta."""
    coperti = {ix.meta(d)["farmaco"] for d in ret if d in set(gold)}
    return float(set(farmaci_attesi) <= coperti)


def costo(ix, ret):
    return len(ret), sum(ix.enc.n_token(ix.docs[d]["text"]) for d in ret)
