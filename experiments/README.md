# Experiments

Studies are logged as `SCN-###` (Singularity Cloud Network), in order. Each is reproducible,
cost-transparent, and explicit about what it does and does not prove.

| ID | Codename | Pillar(s) | Question | Status |
|----|----------|-----------|----------|--------|
| [SCN-001](SCN-001-ouroboros/) | **Ouroboros** | [Grid](../pillars/01-singularity-grid.md) → [DiComp](../pillars/02-singularity-dicomp.md) | Can the grid autonomously generate its own training data, end-to-end, with no datacenter? | 🟢 Running |
| SCN-002 | *(planned)* | Grid + [Pouches](../pillars/03-sgl-pouches.md) | Decentralized on-grid curation & verification of generated data | ◻ Planned |
| SCN-003 | *(planned)* | [DiComp](../pillars/02-singularity-dicomp.md) | First decentralized fine-tune; vs. centralized baseline | ◻ Planned |
| SCN-004 | *(planned)* | [Hive Mind](../pillars/04-singularity-hive-mind.md) | Single large model sharded across clusters, bounded latency | ◻ Planned |

## Starting a new experiment

Copy [`_TEMPLATE/`](_TEMPLATE/) to `SCN-00X-codename/` and fill it in. Conventions:

- **ID:** next free `SCN-###`.
- **Codename:** one evocative word.
- **Reproducible:** include the harness, parameters, and raw artifacts (transcript / logs).
- **Honest:** a "What this is / is not" section is mandatory.
