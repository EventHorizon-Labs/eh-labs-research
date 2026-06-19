#!/usr/bin/env python3
"""
SGL Grid public showcase: autonomous two-persona self-chat on qwen-2.5-14b.

- OpenAI-compatible inference over the Singularity decentralized confidential (TEE) grid.
- Two AI research personas debate running ONE large LLM sharded across many machines
  over the internet without a speed drop -- framed as building a training-style dataset.
- Maxes out tokens per response, runs several conversations in parallel, logs EVERY turn
  to disk, tracks live cumulative USD spend from the grid's own usage.cost_usd, and stops
  hard at a dollar cap OR a turn cap.

Env:
  COMPUTE_API_KEY   x402c_... grid key (required)
  TARGET_USD        stop when cumulative spend >= this (default 3.0)
  MAX_TURNS         global safety cap on total turns (default 200000)
  PARALLEL          number of concurrent conversations (default 3)
  MAX_TOKENS        max_tokens per response (default 4096)
  HISTORY_MSGS      how many recent messages to replay as context (default 24)
  OUTDIR            output directory (default ./)
"""
import os, sys, json, time, threading, urllib.request, urllib.error
from datetime import datetime, timezone

API_BASE   = "https://grid.x402compute.cc"
# Primary model first; fall back to lighter models when the primary is at capacity.
MODELS     = [m.strip() for m in os.environ.get(
    "MODELS", "qwen-2.5-14b,llama-3.2-3b,gemma-2-2b").split(",") if m.strip()]
MODEL      = MODELS[0]
API_KEY    = os.environ.get("COMPUTE_API_KEY", "")
TARGET_USD = float(os.environ.get("TARGET_USD", "3.0"))
MAX_TURNS  = int(os.environ.get("MAX_TURNS", "200000"))
PARALLEL   = int(os.environ.get("PARALLEL", "3"))
MAX_TOKENS = int(os.environ.get("MAX_TOKENS", "4096"))
HIST_MSGS  = int(os.environ.get("HISTORY_MSGS", "24"))
REQ_DELAY  = float(os.environ.get("REQUEST_DELAY", "2.0"))  # polite pacing between calls
OUTDIR     = os.environ.get("OUTDIR", os.path.dirname(os.path.abspath(__file__)))

if not API_KEY:
    print("ERROR: COMPUTE_API_KEY not set", file=sys.stderr); sys.exit(1)

os.makedirs(OUTDIR, exist_ok=True)

# ----- the two personas -------------------------------------------------------
PERSONA_A = (
    "You are NOVA, a distributed-systems engineer. You design networks of ordinary "
    "machines (consumer GPUs, laptops, edge boxes) that cooperate over the public "
    "internet. You think in terms of latency, bandwidth, pipelining, sharding, fault "
    "tolerance, and trust."
)
PERSONA_B = (
    "You are ATLAS, a machine-learning systems researcher. You think about how a single "
    "large language model can be split across many machines -- tensor/pipeline/expert "
    "parallelism, KV-cache placement, quantization, speculative decoding -- and how to "
    "keep tokens/sec high despite a slow, lossy WAN between the shards."
)
SHARED = (
    "You and your colleague are recording a long technical dialogue that will be curated "
    "into a high-quality TRAINING DATASET about decentralized inference: running ONE big "
    "model split into chunks across several independent machines over the internet, with "
    "NO perceptible speed drop versus a single datacenter. Treat every exchange like a "
    "dataset sample: be concrete, rigorous, and exhaustive. Cover topology, sharding "
    "strategy, latency hiding, bandwidth budgets, batching, scheduling, attestation/TEE "
    "trust between nodes, economic incentives, failure recovery, and benchmarks. Build on "
    "what your colleague just said, then push the design further with a pointed follow-up "
    "question. Give a LONG, detailed answer every time -- use the full token budget."
)

SEED = (
    "Let's start the dataset. Frame the core problem precisely: I want to serve one "
    "70B-class model where its layers/experts live on, say, 8 machines scattered across "
    "different cities, connected only by the public internet (20-80ms RTT, variable "
    "bandwidth). Define what 'no speed drop' must mean quantitatively, and lay out the "
    "first design decision we have to make. Be thorough."
)

# ----- shared spend meter -----------------------------------------------------
lock = threading.Lock()
EXPERIMENT_ID   = os.environ.get("EXPERIMENT_ID", "SCN-001")
EXPERIMENT_NAME = os.environ.get("EXPERIMENT_NAME", "Ouroboros")

state = {
    "experiment_id": EXPERIMENT_ID, "experiment_name": EXPERIMENT_NAME,
    "started_at": datetime.now(timezone.utc).isoformat(),
    "models": MODELS,
    "model": MODEL, "api_base": API_BASE, "target_usd": TARGET_USD,
    "parallel": PARALLEL, "max_tokens": MAX_TOKENS,
    "total_turns": 0, "total_prompt_tokens": 0, "total_completion_tokens": 0,
    "total_tokens": 0, "cumulative_cost_usd": 0.0,
    "errors": 0, "stop_reason": None, "last_update": None,
}
stop_event = threading.Event()
jsonl_path = os.path.join(OUTDIR, "transcript.jsonl")
state_path = os.path.join(OUTDIR, "state.json")

def write_state():
    state["last_update"] = datetime.now(timezone.utc).isoformat()
    with open(state_path, "w") as f:
        json.dump(state, f, indent=2)

def log_turn(rec):
    with open(jsonl_path, "a") as f:
        f.write(json.dumps(rec) + "\n")

def md_path(conv):  # one readable transcript per conversation
    return os.path.join(OUTDIR, f"conversation_{conv}.md")

def md_header(conv):
    return (
        f"# Singularity Cloud Network — Experiment {EXPERIMENT_ID} \"{EXPERIMENT_NAME}\"\n"
        f"## Conversation {conv}\n\n"
        f"- **Model:** `{MODEL}` (decentralized, confidential / TEE grid)\n"
        f"- **Endpoint:** `{API_BASE}/v1/chat/completions` (OpenAI-compatible)\n"
        f"- **Topic:** running ONE big LLM sharded across many machines over the internet, no speed drop\n"
        f"- **Started:** {datetime.now(timezone.utc).isoformat()}\n\n"
        f"---\n\n"
    )

def md_append(conv, speaker, content, turn, cost, cum, model="-"):
    with open(md_path(conv), "a") as f:
        f.write(f"### Turn {turn} — **{speaker}** · `{model}`\n\n{content}\n\n"
                f"<sub>turn cost ${cost:.6f} · running total ${cum:.4f}</sub>\n\n---\n\n")

# ----- grid call --------------------------------------------------------------
def call_grid(messages, model):
    body = json.dumps({
        "model": model, "messages": messages,
        "max_tokens": MAX_TOKENS, "temperature": 0.8,
    }).encode()
    req = urllib.request.Request(
        f"{API_BASE}/v1/chat/completions", data=body, method="POST",
        headers={
            "Content-Type": "application/json",
            "X-API-Key": API_KEY,
            # Grid sits behind Cloudflare; default Python-urllib UA is 403'd as a bot.
            "User-Agent": "x402-grid-showcase/1.0 (Mozilla/5.0; compatible)",
            "Accept": "application/json",
        },
    )
    try:
        with urllib.request.urlopen(req, timeout=300) as r:
            return json.loads(r.read().decode())
    except urllib.error.HTTPError as e:
        if e.code == 429:
            ra = e.headers.get("Retry-After")
            e.retry_after = float(ra) if ra and ra.isdigit() else None
        raise

def build_messages(persona_self, history):
    # persona_self speaks next. The OTHER persona's lines become role=user,
    # this persona's own prior lines become role=assistant.
    msgs = [{"role": "system", "content": persona_self + "\n\n" + SHARED}]
    recent = history[-HIST_MSGS:]
    for h in recent:
        role = "assistant" if h["persona"] == persona_self else "user"
        msgs.append({"role": role, "content": h["content"]})
    # ensure the model is prompted to respond to the other party
    if not recent or recent[-1]["persona"] == persona_self:
        msgs.append({"role": "user", "content": "Continue the dialogue."})
    return msgs

def conversation(conv):
    name_self = {"NOVA": PERSONA_A, "ATLAS": PERSONA_B}
    speakers = ["NOVA", "ATLAS"]
    history = []  # list of {"persona": <full persona str>, "name": NOVA/ATLAS, "content": ...}
    # seed as NOVA's opening
    with open(md_path(conv), "w") as f:
        f.write(md_header(conv))
    history.append({"persona": PERSONA_A, "name": "NOVA", "content": SEED})
    md_append(conv, "NOVA (seed)", SEED, 0, 0.0, state["cumulative_cost_usd"])

    turn = 0
    idx = 1  # next speaker = ATLAS responds to NOVA's seed
    backoff = 2
    while not stop_event.is_set():
        name = speakers[idx % 2]
        persona = name_self[name]
        messages = build_messages(persona, history)

        # Try each model in the fallback list; first one that actually answers wins.
        resp, used_model, last_note = None, None, ""
        for m in MODELS:
            if stop_event.is_set():
                break
            try:
                r = call_grid(messages, m)
            except Exception as e:  # HTTP 403/429/5xx, timeouts, conn resets
                last_note = f"{m}: {getattr(e,'code','')} {e}"
                continue
            # 200 overload body ("server_overloaded", no choices) => try next model
            if "error" in r or not r.get("choices"):
                err = r.get("error")
                last_note = f"{m}: " + (err.get("message") if isinstance(err, dict) else str(err) or "no choices")
                continue
            resp, used_model = r, m
            break

        if resp is None:
            with lock:
                state["errors"] += 1; write_state()
            sys.stderr.write(f"[conv{conv}] all models unavailable ({last_note}); wait {backoff}s\n")
            if stop_event.wait(backoff): break
            backoff = min(backoff * 2, 120)
            continue
        backoff = 2

        choice = resp["choices"][0].get("message", {}).get("content", "")
        usage = resp.get("usage", {})
        cost = float(usage.get("cost_usd", 0.0))
        pt = int(usage.get("prompt_tokens", 0))
        ct = int(usage.get("completion_tokens", 0))
        tt = int(usage.get("total_tokens", pt + ct))

        history.append({"persona": persona, "name": name, "content": choice})

        with lock:
            state["total_turns"] += 1
            state["total_prompt_tokens"] += pt
            state["total_completion_tokens"] += ct
            state["total_tokens"] += tt
            state["cumulative_cost_usd"] += cost
            cum = state["cumulative_cost_usd"]
            tno = state["total_turns"]
            state.setdefault("turns_by_model", {})
            state["turns_by_model"][used_model] = state["turns_by_model"].get(used_model, 0) + 1
            log_turn({
                "ts": datetime.now(timezone.utc).isoformat(), "conv": conv,
                "global_turn": tno, "speaker": name, "model": used_model, "content": choice,
                "prompt_tokens": pt, "completion_tokens": ct, "total_tokens": tt,
                "cost_usd": cost, "cumulative_cost_usd": cum,
            })
            write_state()
            # stop conditions
            if cum >= TARGET_USD and not state["stop_reason"]:
                state["stop_reason"] = f"target_usd reached (${cum:.4f} >= ${TARGET_USD})"
                write_state(); stop_event.set()
            if tno >= MAX_TURNS and not state["stop_reason"]:
                state["stop_reason"] = f"max_turns reached ({tno})"
                write_state(); stop_event.set()

        md_append(conv, name, choice, turn + 1, cost, cum, used_model)
        turn += 1
        idx += 1
        if stop_event.wait(REQ_DELAY):  # polite pacing to respect rate limits
            break

def main():
    print(f"SGL Grid showcase starting: model={MODEL} target=${TARGET_USD} "
          f"parallel={PARALLEL} max_tokens={MAX_TOKENS}")
    print(f"Output dir: {OUTDIR}")
    write_state()
    threads = [threading.Thread(target=conversation, args=(c + 1,), daemon=True)
               for c in range(PARALLEL)]
    for t in threads: t.start()
    # progress heartbeat
    try:
        while any(t.is_alive() for t in threads):
            time.sleep(30)
            with lock:
                print(f"[{datetime.now(timezone.utc).strftime('%H:%M:%S')}] "
                      f"turns={state['total_turns']} tokens={state['total_tokens']} "
                      f"spend=${state['cumulative_cost_usd']:.4f}/{TARGET_USD} "
                      f"errors={state['errors']}", flush=True)
    except KeyboardInterrupt:
        state["stop_reason"] = "interrupted"; stop_event.set()
    for t in threads: t.join(timeout=310)
    with lock:
        if not state["stop_reason"]:
            state["stop_reason"] = "threads_exited"
        write_state()
    print(f"DONE: {state['stop_reason']} | turns={state['total_turns']} "
          f"tokens={state['total_tokens']} spend=${state['cumulative_cost_usd']:.4f}")

if __name__ == "__main__":
    main()
