# Singularity Cloud Network — Experiment Log

## SCN-001 · "Ouroboros"

**Decentralized synthetic dataset generation on a confidential compute grid.**

| Field | Value |
|---|---|
| Experiment ID | `SCN-001` |
| Codename | Ouroboros |
| Date opened | 2026-06-19 |
| Status | Running |
| Grid | Singularity Cloud Network — SGL Grid (`grid.x402compute.cc`) |
| Compute substrate | Apple Secure Enclave TEE nodes (decentralized, confidential) |
| Models | `qwen-2.5-14b` → `llama-3.2-3b` → `gemma-2-2b` (self-healing fallback) |
| Interface | OpenAI-compatible `/v1/chat/completions` |
| Settlement | Per-token USDC (x402 credits) — `$0.01/M` in, `$0.02/M` out |
| Method | Two autonomous personas (NOVA + ATLAS) in self-chat, generating a training-style corpus on decentralized sharded inference |
| Artifacts | `run1/transcript.jsonl`, `run1/conversation_*.md`, `run1/state.json` |
| Harness | `grid_selfchat.py` |

### Hypothesis
A decentralized, confidential compute grid can autonomously generate a coherent,
domain-specific training corpus end-to-end — with no centralized datacenter, transparent
per-token economic settlement, and graceful self-healing across model nodes under capacity
pressure — as the first stage of a fully decentralized AI training pipeline on Singularity
DAI Comp.

### Why this is logged as an experiment
This is the first stage (dataset creation) of a planned end-to-end decentralized training
pipeline. Each stage gets its own SCN-### entry so results, costs, and limitations are
reproducible and citable.

### Naming
Future experiments: `SCN-002`, `SCN-003`, … Set `EXPERIMENT_ID` / `EXPERIMENT_NAME`
env vars when launching `grid_selfchat.py`.
