# Pillar 3 — SGL Pouches

**Decentralized, confidential data & storage — verifiable datasets and embeddings.**

> Status: 🔵 **Designing**

---

## What it is

SGL Pouches are the **data layer** of the decentralized AI cluster — think "SQL pouches": small,
portable, confidential, verifiable stores for the structured data, datasets, and embeddings that
feed training and inference. Where the Grid does compute, Pouches hold state.

A Pouch is a unit of data that is:

- **Confidential** — encrypted; access controlled cryptographically, not by a trusted host.
- **Verifiable** — content-addressed and provenance-tracked, so a dataset's lineage is provable
  (critical when data is generated *by* the network — see [Ouroboros](../experiments/SCN-001-ouroboros/)).
- **Portable** — moves with the workload across the decentralized grid.
- **Queryable** — structured access (relational / vector) without surrendering the data to a
  central server.

## Why it matters

Decentralized training and inference are only as trustworthy as their data. If a model is
trained on grid-generated data, you need to prove *what* data, generated *how*, with *what*
lineage. Pouches make datasets first-class, confidential, and auditable — the connective tissue
between data creation (Grid), curation, and training (DiComp).

## Research questions

- Confidential query execution (compute over encrypted data / inside TEEs).
- Dataset provenance and tamper-evidence for synthetic, network-generated corpora.
- Vector storage and retrieval for embeddings, decentralized and confidential.
- Replication and durability across untrusted nodes.

## Where it sits

```
Grid (generate data) ──▶ SGL Pouches (store, verify, version) ──▶ DiComp (train)
```
