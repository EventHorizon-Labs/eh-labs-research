# Pillar 2 — Singularity DiComp

**Decentralized training for AI models across distributed, confidential compute.**

> Status: 🟡 **Building** · *(also referred to as DAI Comp — Distributed AI Compute)*

---

## What it is

DiComp is the **training** layer: a way to train and fine-tune models across many independent
machines that don't trust each other and are connected only by the public internet. Where the
Grid serves models, DiComp *creates* them — on the same decentralized, attested substrate.

## Why it matters

Training is the most centralized part of AI today — it demands tightly-coupled GPU clusters in
a single datacenter. DiComp's goal is to break that requirement: pool heterogeneous compute
from independent operators, coordinate it over a slow/lossy WAN, and still converge — with
**verifiable contribution accounting** so honest work is provably rewarded and tampering is
detectable.

## Core problems we're researching

- **Communication over the WAN:** gradient/activation exchange when nodes are 20–80 ms apart
  with variable bandwidth (overlap, compression, async, local steps).
- **Fault tolerance:** nodes drop mid-run; training must survive and resume.
- **Verifiable compute:** prove a node did the work it claims (TEE attestation +
  spot-checking) before paying it.
- **Heterogeneity:** mixed hardware, mixed speeds, fair scheduling.
- **Economics:** `$SGL`-staked operators earn for training work; slashing for proven cheating.

## Where it sits in the pipeline

```
SGL Pouches (data) ──▶ DiComp (training) ──▶ model weights ──▶ Grid / Hive Mind (serving)
```

## Related experiments

- **SCN-003 · *(planned)*** — first decentralized fine-tune on a curated [Ouroboros](../experiments/SCN-001-ouroboros/)
  corpus; measure decentralized-data → decentralized-training vs. a centralized baseline.
