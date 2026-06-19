# Roadmap — Toward a Fully Decentralized AI Cluster

The goal: a complete AI lifecycle — **data → training → model → inference** — running on a
single decentralized, confidential, verifiable substrate. No datacenter. No single owner.
Every step attested in a TEE and settled in stablecoins.

We get there in phases. Each phase is anchored by experiments (`SCN-###`) that prove the next
link in the chain actually holds before we build on it.

---

## The end-to-end pipeline

```
   [1] DATA              [2] TRAINING            [3] MODEL              [4] INFERENCE
   creation &       →    decentralized      →    sharded across   →    confidential,
   curation              distributed             device clusters       OpenAI-compatible
   on the grid           training                (Hive Mind)           serving

   SGL Grid +            Singularity             Singularity           Singularity Grid
   SGL Pouches           DiComp                  Hive Mind             (live today)
```

A model whose data, training weights, and serving all live on the same trustless grid —
contributed to by anyone who stakes `$SGL` and brings a TEE machine online.

---

## Phases

### Phase 0 — Confidential inference (✅ shipped)
- **Singularity Grid** live: decentralized, confidential, OpenAI-compatible inference on
  attested TEE nodes; per-token USDC settlement; end-to-end encryption.
- Tokenized access: pay with x402 (USDC/USDm) or prepaid credits.

### Phase 1 — Decentralized data (🟢 in progress)
- Prove the grid can **generate** domain-specific training data autonomously. → **SCN-001 (Ouroboros)**
- Next: on-grid **curation & verification** (multi-node cross-checking, dedup, diversity). → SCN-002 (planned)
- Storage & provenance via **SGL Pouches** (confidential, verifiable datasets).

### Phase 2 — Decentralized training (🟡 building)
- **Singularity DiComp**: distributed training across independent nodes — gradient exchange
  over the WAN, fault tolerance, verifiable contribution accounting.
- Close the loop: fine-tune on a curated Ouroboros corpus and beat a centralized baseline on
  the target domain.

### Phase 3 — Sharded serving at scale (🔵 designing)
- **Singularity Hive Mind**: serve one large model split across many device clusters over the
  public internet with no perceptible speed drop (pipeline/tensor/expert parallelism + latency
  hiding). Fittingly, this is the exact topic SCN-001's agents are generating data about.

### Phase 4 — The autonomous cluster (🔭 vision)
- Agents that **provision, train, serve, and pay** for compute without humans in the loop.
- Tokenized compute markets clear supply and demand automatically.
- The network maintains, funds, and improves itself.

---

## Experiment ledger

| Phase | Experiment | Proves |
|-------|------------|--------|
| 1 | **SCN-001 · Ouroboros** | Grid can autonomously generate its own training corpus, end-to-end, self-healing, for fractions of a cent |
| 1 | SCN-002 · *(planned)* | On-grid decentralized curation/verification of generated data |
| 2 | SCN-003 · *(planned)* | First decentralized fine-tune on DiComp; baseline comparison |
| 3 | SCN-004 · *(planned)* | Single large model sharded across clusters with bounded latency |

---

*Each phase ships in the open. We report results — and limitations — as research, not marketing.*
