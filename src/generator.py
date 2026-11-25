"""Parametric generator: sources H and P with N local IDs each and S = round(omega*N) shared entities.

Each entity has two events. A shared entity has one event per source, with different drugs for a share
alpha of them. Local ID numbers are shuffled per source, so equal numbers never mean the same person.
Dirty ER adds D_H and D_P extra local IDs to entities already in the same source.
"""
import numpy as np

FARMACI = ["Metformina", "Insulina", "Aspirina", "Atorvastatina", "Ramipril", "Omeprazolo"]
QUANTITA = [10, 20, 30]


def genera(N, omega, alpha, seed, D_H=0, D_P=0):
    rng = np.random.default_rng(seed)
    S = round(omega * N)
    V = 2 * N - S
    # Entities: 0..S-1 shared, S..N-1 only in H, N..V-1 only in P
    coorte = ["condivisa"] * S + ["solo_H"] * (N - S) + ["solo_P"] * (N - S)
    n_compl = round(alpha * S)
    compl = set(rng.choice(S, size=n_compl, replace=False).tolist()) if S else set()

    num_H = iter((rng.permutation(N) + 1).tolist())
    num_P = iter((rng.permutation(N) + 1).tolist())
    locali = {}
    for e in range(V):
        locali[e] = {}
        if coorte[e] in ("condivisa", "solo_H"):
            locali[e]["H"] = [f"H:{next(num_H)}"]
        if coorte[e] in ("condivisa", "solo_P"):
            locali[e]["P"] = [f"P:{next(num_P)}"]

    eventi = []
    for e in range(V):
        f1, f2 = rng.choice(FARMACI, size=2, replace=False).tolist()
        if coorte[e] == "condivisa":
            eventi.append((e, "H", locali[e]["H"][0], f1))
            eventi.append((e, "P", locali[e]["P"][0], f2 if e in compl else f1))
        else:
            src = "H" if coorte[e] == "solo_H" else "P"
            eventi += [(e, src, locali[e][src][0], f1), (e, src, locali[e][src][0], f2)]

    for src, D in (("H", D_H), ("P", D_P)):
        presenti = [e for e in range(V) if src in locali[e]]
        for j, e in enumerate(rng.choice(presenti, size=D, replace=False).tolist() if D else []):
            lid = f"{src}:{N + j + 1}"
            locali[e][src].append(lid)
            eventi.append((e, src, lid, rng.choice(FARMACI)))

    docs = []
    for i, (e, src, lid, f) in enumerate(eventi, start=1):
        q = int(rng.choice(QUANTITA))
        docs.append({"doc_id": f"d{i}", "text": f"{lid} ha ricevuto {f}, quantità {q}.",
                     "metadata": {"source": src, "local_id": lid, "farmaco": f, "quantita": q,
                                  "gid": f"G{e}", "coorte": coorte[e], "complementare": e in compl}})
    info = {"N": N, "omega": omega, "alpha": alpha, "seed": seed, "S": S, "V": V,
            "B": sum(len(v) for loc in locali.values() for v in loc.values()), "D_H": D_H, "D_P": D_P}
    return docs, info, locali, coorte, compl


def domande(docs, locali, coorte, compl, rng, n_per_tipo=40):
    """Entity-centric questions with a seed: single-source and multi-source."""
    per_gid = {}
    for d in docs:
        per_gid.setdefault(d["metadata"]["gid"], []).append(d)
    out = []
    escl = [e for e, c in enumerate(coorte) if c != "condivisa"]
    cond = [e for e, c in enumerate(coorte) if c == "condivisa"]
    for tipo, pool in (("single-source", escl), ("multi-source", cond)):
        scelte = rng.choice(pool, size=min(n_per_tipo, len(pool)), replace=False).tolist() if pool else []
        for e in scelte:
            srcs = sorted(locali[e])
            seed = locali[e][srcs[int(rng.integers(len(srcs)))]][0]
            gold = per_gid[f"G{e}"]
            out.append({"tipo": tipo, "seed": seed, "complementare": e in compl,
                        "query": f"Quali farmaci risultano per {seed} in tutte le sorgenti?",
                        "gold_docs": [d["doc_id"] for d in gold],
                        "risposta": sorted({d["metadata"]["farmaco"] for d in gold})})
    return out


def controlli(docs, info):
    """Paper identities: B = 2N + D, V = 2N - S, gamma = B / V."""
    N, S, V = info["N"], info["S"], info["V"]
    assert len({d["metadata"]["gid"] for d in docs}) == V
    assert info["B"] == 2 * N + info["D_H"] + info["D_P"]
    assert len({d["metadata"]["local_id"] for d in docs}) == info["B"]
    for d in docs:
        assert d["metadata"]["gid"] not in d["text"]
    if info["D_H"] == info["D_P"] == 0:
        assert abs(info["B"] / V - 2 * N / (2 * N - S)) < 1e-12


if __name__ == "__main__":
    for omega in (0, 0.25, 0.5, 0.75):
        docs, info, *_ = genera(100, omega, 0.5, seed=0)
        controlli(docs, info)
        print(f"omega={omega}: S={info['S']} V={info['V']} B={info['B']} gamma={info['B']/info['V']:.3f} "
              f"teorico={200/(200-info['S']):.3f} documenti={len(docs)}")
    docs, info, *_ = genera(100, 0.5, 0.5, seed=0, D_H=10, D_P=10)
    controlli(docs, info)
    print(f"Dirty D_H=D_P=10: B={info['B']} V={info['V']} gamma={info['B']/info['V']:.3f} "
          f"gamma_intra={(20)/info['V']:.3f}")
    print(docs[0]["text"], docs[0]["metadata"])
