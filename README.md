<div align="center">

# Event Horizon Labs · Research

**Building decentralized, verifiable, confidential, and agentic cloud infrastructure.**

*Research toward a fully decentralized AI cluster — where data, training, and inference*
*all run on trustless, attested hardware owned by no one and verifiable by everyone.*

</div>

---

## Why we exist

Modern AI is centralized at every layer: data is curated inside a few companies, training
runs in single datacenters on tightly-coupled clusters, and inference is served from walled
gardens. Each layer concentrates control, cost, and trust.

Event Horizon Labs is building the opposite — an end-to-end stack where **every stage of the
AI lifecycle runs on a decentralized grid of independent, confidential (TEE) machines**,
coordinated over the open internet and settled in stablecoins. This repository is our public
research record: the experiments, results, and honest engineering notes on the road there.

We publish like a research lab — including what doesn't work yet.

---

## The four pillars

| # | Pillar | What it is | Status |
|---|--------|------------|--------|
| 1 | **[Singularity Grid](pillars/01-singularity-grid.md)** | Decentralized, confidential, OpenAI-compatible **inference** across attested TEE nodes | 🟢 Live |
| 2 | **[Singularity DiComp](pillars/02-singularity-dicomp.md)** | Decentralized **training** for AI models across distributed compute | 🟡 Building |
| 3 | **[SGL Pouches](pillars/03-sgl-pouches.md)** | Decentralized, confidential **data & storage** — verifiable datasets and embeddings | 🔵 Designing |
| 4 | **[Singularity Hive Mind](pillars/04-singularity-hive-mind.md)** | One **large model sharded across many device clusters** over the internet, no speed drop | 🔵 Designing |

Underpinning all four: **tokenized compute markets** — stake `$SGL`, bring a TEE machine
online, earn for the work it does. Compute becomes a permissionless, liquid commodity.

→ See the **[Roadmap](ROADMAP.md)** for how the pillars compose into a fully decentralized AI cluster.

---

## Experiments

We log each study as `SCN-###` (Singularity Cloud Network). Every experiment is reproducible,
cost-transparent, and honest about scope.

| ID | Codename | Pillar(s) | Question | Status |
|----|----------|-----------|----------|--------|
| [SCN-001](experiments/SCN-001-ouroboros/) | **Ouroboros** | Grid → DiComp | Can the grid autonomously generate its own training data, end-to-end, with no datacenter? | 🟢 Running |

→ Browse all in **[experiments/](experiments/)**. New studies start from the **[template](experiments/_TEMPLATE/)**.

---

## How to read this repo

```
eh-labs-research/
├── README.md            ← you are here (lab index)
├── ROADMAP.md           ← the phased path to a fully decentralized AI cluster
├── pillars/             ← what we're building (one doc per pillar)
├── experiments/         ← what we've tested (SCN-### studies, reproducible)
│   ├── _TEMPLATE/       ← start a new experiment here
│   └── SCN-001-ouroboros/
└── web/                 ← source for the public experiments page (eventhorizon labs site)
```

---

<div align="center">

*Confidential by construction. Decentralized by design. Verifiable by everyone.*

**`$SGL` secures the grid.**

</div>
