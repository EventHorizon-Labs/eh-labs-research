# Ouroboros harness

`grid_selfchat.py` — orchestrates two autonomous personas (NOVA + ATLAS) in a self-directed
dialogue on the Singularity Grid, capturing a training-style corpus on decentralized inference.

## Requirements
Python 3.8+ standard library only (`urllib`, `json`, `threading`). No external dependencies.

## Run

```bash
export COMPUTE_API_KEY="x402c_..."          # Singularity Grid key (prepaid credits)
export OUTDIR=./run1
export MODELS="qwen-2.5-14b,llama-3.2-3b,gemma-2-2b"   # fallback chain (primary first)
export TARGET_USD=3.0                        # hard stop on cumulative spend
export MAX_TURNS=1000000                      # safety cap on turns
export MAX_TOKENS=3072                        # max tokens per response
export HISTORY_MSGS=12                        # recent messages replayed as context
export REQUEST_DELAY=3                        # polite pacing (seconds) between calls
export EXPERIMENT_ID="SCN-001" EXPERIMENT_NAME="Ouroboros"
python3 grid_selfchat.py
```

## What it does
- Self-chat via persona-swap over the OpenAI-compatible `/v1/chat/completions` endpoint.
- **Self-healing fallback:** tries each model in `MODELS` until one answers; absorbs grid
  capacity (`429` / `server_overloaded`) without stalling. Records which model produced each turn.
- **Cost-transparent:** accumulates `usage.cost_usd` from the grid; hard-stops at `TARGET_USD`.
- **Logged:** `transcript.jsonl` (one record/turn, with model + cost), `conversation_*.md`
  (readable), `state.json` (live totals).

## Notes
- The grid sits behind Cloudflare; the harness sends a normal `User-Agent` (the default
  `Python-urllib` UA is currently blocked — see the experiment's engineering notes).
- Honors `Retry-After` on `429` and backs off exponentially on transient errors.
