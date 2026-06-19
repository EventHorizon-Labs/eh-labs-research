# Pillar 4 — Singularity Hive Mind

**One large model, sharded across many device clusters over the internet — no speed drop.**

> Status: 🔵 **Designing**

---

## What it is

Hive Mind runs a **single large model** (e.g. 70B+) that is too big for any one machine by
**splitting it into chunks across multiple clusters of independent devices** connected over the
public internet — and serving it as if it were one model in one datacenter, with no perceptible
latency penalty.

Where the [Grid](01-singularity-grid.md) serves models that fit on a node, Hive Mind serves
models that *don't* — by making many small/consumer machines behave as one large accelerator.

## The core challenge

Splitting a model across geographically dispersed machines normally tanks performance: every
layer boundary becomes a network round-trip (20–80 ms RTT, variable bandwidth). "No speed drop"
means keeping latency and throughput within a small margin of a centralized baseline despite
that.

Approaches under study:

- **Pipeline parallelism** — partition layers into stages across clusters; keep stages busy so
  network time hides behind compute.
- **Tensor / expert parallelism** — split within layers or route to expert shards.
- **Latency hiding** — speculative execution, asynchronous communication, activation
  prefetching, micro-batching.
- **Topology-aware placement** — co-locate chatty stages; budget the WAN deliberately.
- **Trust** — TEE attestation between shards so no single device can poison the forward pass.

> Fittingly, **this is the exact problem the agents in [SCN-001 · Ouroboros](../experiments/SCN-001-ouroboros/)
> are generating a training dataset about** — the network reasoning about how to become one mind.

## Where it sits

```
DiComp (train large model) ──▶ weights sharded ──▶ Hive Mind (serve across clusters)
```

## Related experiments

- **SCN-004 · *(planned)*** — serve one large model sharded across clusters with bounded,
  measured latency vs. a single-node baseline.
