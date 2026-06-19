# Ouroboros: A Network That Writes Its Own Training Data

### Singularity Cloud Network — Experiment SCN-001

*Singularity Research · June 19, 2026*

---

## Abstract

We report the first end-to-end demonstration of **decentralized synthetic dataset
generation** on the Singularity Cloud Network. Two autonomous language-model agents,
running entirely on a grid of **confidential Apple Secure Enclave (TEE) nodes** — no
centralized datacenter — held an extended, self-directed technical dialogue and, in doing
so, produced a structured corpus on the very problem the network is built to solve: running
a single large model split across many machines over the public internet without a speed
drop. Every exchange was settled per-token in USDC through an OpenAI-compatible API, and the
system **self-healed across models** (`qwen-2.5-14b → llama-3.2-3b → gemma-2-2b`) whenever a
node hit capacity. This is the first stage of a planned **fully decentralized training
pipeline** on Singularity DAI Comp, in which data creation, training, and inference all run
on the same trustless, attested substrate.

We are deliberately precise about what this is — a working pilot — and what it is not yet —
a frontier-scale training run. The result is small in compute and large in implication: the
pieces of a decentralized AI factory now compose.

---

## 1. Motivation

Modern AI is centralized at every layer. Datasets are scraped and curated inside a handful
of companies; training runs on tightly-coupled GPU clusters in single datacenters; inference
is served from the same walled gardens. Each layer concentrates control, cost, and trust.

Singularity's thesis is the opposite: **compute should be a decentralized, confidential,
permissionless commodity** — thousands of independent machines, each attesting to what it
runs inside a Trusted Execution Environment, coordinating over the open internet, settling
in stablecoins. We already serve confidential inference this way on the **SGL Grid**, and we
are building distributed training on **SGL DAI Comp** (Phase 2).

But a training pipeline is more than a trainer. It begins with **data**. If the grid can
*generate* high-quality, domain-specific data — autonomously, verifiably, and economically —
then the entire loop, from dataset to model to inference, can live on decentralized
infrastructure. That is the question SCN-001 set out to probe.

We named it **Ouroboros**: the network feeding itself.

---

## 2. What we built

A minimal but complete harness (`grid_selfchat.py`) that orchestrates two AI research
personas in an autonomous dialogue:

- **NOVA**, a distributed-systems engineer (latency, sharding, fault tolerance, trust).
- **ATLAS**, an ML-systems researcher (tensor/pipeline/expert parallelism, KV-cache
  placement, speculative decoding).

Each turn, the harness replays the running conversation to the grid as an OpenAI-compatible
chat request, relabeling roles so the model always speaks as the *next* persona. The personas
are instructed to treat every exchange as a **dataset sample**: concrete, rigorous,
exhaustive, always ending with a pointed follow-up that advances the design. The seed
question frames the core problem precisely:

> *Serve one 70B-class model whose layers live on 8 machines in different cities, connected
> only by the public internet (20–80 ms RTT, variable bandwidth). Define what "no speed drop"
> must mean quantitatively, and lay out the first design decision.*

### System architecture

```
        ┌──────────────────────────────────────────────────────┐
        │              Ouroboros harness (orchestrator)          │
        │   persona swap · context replay · cost meter · logs    │
        └───────────────┬────────────────────────────┬───────────┘
                        │ OpenAI-compatible /v1        │ usage.cost_usd
                        ▼                              ▲
        ┌──────────────────────────────────────────────────────┐
        │             SGL Grid  (grid.x402compute.cc)            │
        │     routing · attestation · per-token USDC billing     │
        └───────┬─────────────────┬─────────────────┬────────────┘
                ▼                 ▼                 ▼
          ┌──────────┐      ┌──────────┐      ┌──────────┐
          │ TEE node │      │ TEE node │      │ TEE node │   Apple Secure
          │ qwen-14b │      │ llama-3b │      │ gemma-2b │   Enclave nodes
          └──────────┘      └──────────┘      └──────────┘
             (confidential, attested, decentralized — no datacenter)
```

### Self-healing across models

The grid is real infrastructure under real load. When all nodes serving the primary model
are busy, it returns a clean `429` (or a `server_overloaded` body) **and does not charge**.
Rather than stall, Ouroboros walks a fallback chain:

```
qwen-2.5-14b   (preferred)  ──busy──▶  llama-3.2-3b  ──busy──▶  gemma-2-2b
```

The transcript records which model produced each line, so the dataset itself is a log of the
network routing around its own congestion.

---

## 3. Results (live pilot)

*Numbers below are a snapshot of an ongoing run; the corpus continues to grow.*

| Metric | Value (snapshot) |
|---|---|
| Completed dialogue turns | ~87 (growing) |
| Hard failures surfaced to caller | **0** (capacity absorbed by fallback) |
| Transient all-models-busy retries (auto-recovered) | 2 |
| Tokens generated | ~512,000 and climbing |
| Cost to date | **~$0.0026** |
| Cost per exchange | ~$0.00003 |
| Model mix | `llama-3.2-3b` carried the run while `qwen-2.5-14b` was at capacity |
| Substrate | 3 active Apple Secure Enclave TEE nodes |

*(Raw artifacts: [`data/state.snapshot.json`](data/state.snapshot.json),
[`data/transcript.jsonl`](data/transcript.jsonl). Harness: [`harness/grid_selfchat.py`](harness/grid_selfchat.py).)*

Two things stand out. First, **quality**: with no human in the loop, the agents independently
converged on a rigorous treatment — defining "no speed drop" as bounded time-to-first-token
and ≤10% throughput loss vs. a centralized baseline, then working through pipeline
parallelism, stage balancing, inter-stage activation transfer, latency budgets, speculative
execution, and asynchronous communication. This is usable, structured training data.

Second, **economics**: a full multi-turn technical exchange costs a *fraction of a cent*, with
the price of every token returned inline by the grid. The data-generation layer of an AI
pipeline, run on decentralized confidential hardware, is effectively too cheap to meter.

---

## 4. What we observed about the grid (honest engineering notes)

Running a real workload surfaced real findings, which we are fixing in the open:

- **Capacity is the binding constraint.** Only three TEE nodes currently serve the flagship
  model; under concurrent load they saturate and return `429 / server_overloaded` (correctly
  un-billed, with `Retry-After`). The fallback chain hid this from the experiment, but the
  lesson is clear: **decentralized scale needs more nodes online**, especially GPU-class
  operators. This is exactly what staking + node onboarding on DAI Comp is meant to solve.
- **Edge filtering can block legitimate SDK traffic.** Our edge layer was rejecting some
  programmatic User-Agents (including a popular SDK default) before they reached billing.
  Auth belongs on the API key, not the User-Agent; we're correcting it.
- **Billing integrity held.** Overloaded requests were never charged, and `usage.cost_usd`
  plus per-million pricing were returned on every successful call. Trustless metering works.

We consider transparent failure reporting part of the result. A decentralized network earns
trust by showing its seams.

---

## 5. What this is — and what it is not

**It is:** a working, reproducible demonstration that a decentralized confidential compute
grid can autonomously generate coherent, domain-specific, economically-metered training data,
end-to-end, with no centralized datacenter and graceful degradation under load.

**It is not (yet):** a frontier-scale dataset, a quality-filtered/deduplicated production
corpus, or evidence that a model *trained* on this data outperforms a baseline. Synthetic
self-chat can drift, repeat, or amplify a single model's biases; the data needs curation,
verification, and diversity before training. Scale here is tiny.

Calling it "groundbreaking" would be marketing. Calling it a **credible first step toward a
decentralized AI factory** is, we think, accurate — and that step has now been taken in the
open, on live infrastructure, for a fraction of a cent.

---

## 6. The bigger picture: an end-to-end decentralized pipeline

SCN-001 is stage one of four:

```
  [1] Dataset creation   →   [2] Curation & verification   →   [3] Training        →   [4] Inference
      SGL Grid (this)         multi-node cross-checking         SGL DAI Comp            SGL Grid
      ✅ pilot done            ◻ designing                       ◻ Phase 2 target        ✅ live today
```

The endgame: a model whose **data, training, and serving all run on the same trustless,
attested, stablecoin-settled grid** — owned by no one, verifiable by everyone, contributed to
by anyone who stakes $SGL and brings a TEE machine online. Ouroboros is the proof that the
first link in that chain holds.

---

## 7. Reproducibility

The harness, fallback logic, and full transcripts (Markdown + JSONL, with per-turn model and
cost) are logged under experiment `SCN-001`. Each run is parameterized by model chain, token
budget, pacing, and a hard USD/turn cap. Set `EXPERIMENT_ID` / `EXPERIMENT_NAME` to open a new
log.

---

## 8. Future work

- **SCN-002:** add a third *verifier* agent that scores and filters each exchange on-grid
  (decentralized curation).
- **Onboard GPU TEE nodes** (Intel TDX / AMD SEV-SNP / NVIDIA CC) to lift capacity and serve
  larger models without fallback.
- **Cross-model diversity:** rotate primary models per turn to reduce single-model bias in the
  corpus.
- **Close the loop:** fine-tune a small model on a curated Ouroboros corpus via DAI Comp and
  measure whether decentralized-data → decentralized-training → decentralized-inference beats a
  centralized baseline on the target domain.

---

*Built on the Singularity Cloud Network. Confidential by construction. Decentralized by design.*
*$SGL secures the grid. The network is learning to teach itself.*
