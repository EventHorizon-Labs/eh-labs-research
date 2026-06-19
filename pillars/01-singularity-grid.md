# Pillar 1 — Singularity Grid

**Decentralized, confidential, OpenAI-compatible inference across attested TEE nodes.**

> Status: 🟢 **Live** · `grid.x402compute.cc`

---

## What it is

The Grid is the inference layer of the decentralized AI cluster. Independent operators run
**Trusted Execution Environment (TEE)** nodes — Apple Secure Enclave, Intel TDX/SGX, AMD
SEV-SNP, AWS Nitro — that serve language models confidentially. Requests are end-to-end
encrypted; the operator cannot see the prompt or the output. The grid routes each request to
an attested node, meters it per token, and settles in stablecoins.

It speaks the **OpenAI API**, so any existing client works by pointing `base_url` at the grid.

## Why it matters

- **Confidential:** your data is sealed to the enclave; the node operator sees ciphertext.
- **Decentralized:** no single datacenter; nodes join and leave permissionlessly.
- **Verifiable:** every node attests to the exact binary it runs before it can serve.
- **Economic:** pay-per-token in USDC (x402) or prepaid credits — no subscription.

## How it works

```
client ──(OpenAI /v1, encrypted)──▶ Grid router ──(sealed)──▶ attested TEE node ──▶ model
        ◀──(sealed tokens, usage.cost_usd)──────────────────────────────────────────┘
```

- **Auth:** `X-API-Key` (prepaid credits) or per-request x402 `X-Payment`.
- **Models:** served by whichever nodes are online; the live menu changes as operators come
  and go (a decentralized grid *breathes*).
- **Billing integrity:** when all nodes serving a model are at capacity, the grid returns a
  clean overload signal and **does not charge** — clients retry or fall back to another model.

## Open questions / research

- Capacity elasticity: incentivizing enough nodes (esp. GPU-class) to absorb bursty load.
- Per-model load visibility so clients can route intelligently.
- Latency-aware routing across geographically dispersed nodes.

## Related experiments

- **[SCN-001 · Ouroboros](../experiments/SCN-001-ouroboros/)** — uses the Grid to autonomously
  generate training data, including self-healing fallback across models under capacity pressure.
