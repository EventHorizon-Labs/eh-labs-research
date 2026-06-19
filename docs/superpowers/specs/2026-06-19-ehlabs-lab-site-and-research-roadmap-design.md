# Design Spec — EHLabs Lab Site + Internal Research Roadmap

*Date: 2026-06-19 · Status: For review*

## 1. Goal & positioning

**EHLabs is a web3 + AI research lab — positioned like Anthropic.** It exists to build, and prove out, **the unified infrastructure layer for cross-species homo-agentic commerce**: a stack where data, training, inference, payments, and commerce all run on decentralized, verifiable, confidential, agentic infrastructure.

The site has **two pillars, Anthropic-style: Research and Products.** Everything lives under one or the other.

- **Research** is the moat: a visible, disciplined research *program* (not random experiments) on a decentralized-AI stack nobody else has end-to-end. Experiments + papers prove EHLabs is ahead.
- **Products** is the proof it's real: the full Singularity stack, shipping.

Two coordinated outputs in this spec:
- **(A)** the public **EHLabs site** (this is the bulk of the build), and
- **(B)** the internal **research-practices roadmap** in the `eh-labs-research` repo — the fixed path that makes experiments connect.

## 2. Site information architecture

Top nav (persistent, styled like the existing research-page top bar): **Home · Research · Products** (Company/About deferred).

```
/                              HOME — the vision & why
                               - Hero: "The unified infra layer for cross-species homo-agentic commerce"
                               - The thesis / why everything is being built
                               - "Connected map": how Research → Products → the endgame fit
                               - Two doors: Research and Products
                               - CLASSIFIED teaser: the unnamed endgame ("final product on Singularity infra")

/research                      RESEARCH — the lab
                               - Research mission & thesis
                               - Research tracks (mapped to the stack)
                               - How we work (methodology summary; links to repo)
                               - Experiments (link) + Papers (index)

/research/experiments          EXPERIMENTS tab — SCN-### index (cards: codename, question, status)
/research/experiments/[id]     Individual experiment page — SCN-001 "Ouroboros" (proof-of-concept) first

/products                      PRODUCTS — hub; cards for every division w/ status → dedicated pages
/products/[slug]               Dedicated division pages:
                                 singularity-studio · agent-skills · payments · enterprise ·
                                 agentic-fundraisers · staking-engine · erc-8004 · slayer · marketplace
/products/cloud-network        CLOUD NETWORK — sub-hub (its own landing) linking to sub-product pages
/products/cloud-network/[slug]   grid · machines · processors · dai-comp · vault · pouches · clusters · hivemind

(existing /brand-kit /contact /privacy /terms retained; footer updated)
```

## 3. Canonical taxonomy (verbatim from source — do NOT paraphrase loosely)

Source of truth: `SGLCompute_Frontend/src/app/page.tsx` and `ivaavimusic/docs` (docs.json).

**Top-level divisions (Products):**
- **Singularity Studio** — build & deploy monetized x402 endpoints; marketplace presence.
- **Agent Skills** — portable agent skills (the `singularity` / `x402-compute` skill family).
- **Singularity Payments** — x402 + MPP stablecoin payments (USDC/USDm) across chains.
- **Singularity Enterprise** — white-label commerce, revenue splits, off-chain-first.
- **Agentic Fundraisers** — agent-run fundraising campaigns (off-chain escrow now).
- **Staking Engine ($SGL)** — staking that secures the grid / validators / registry.
- **ERC-8004** — agent identity & on-chain reputation registry (multi-chain).
- **Slayer** — agentic product (per docs "Slayer Agent").
- **Marketplace** — discovery/commerce for endpoints & agents.

**Singularity Cloud Network (umbrella) sub-products** — exact descriptions:
| Slug | Name | Description (verbatim) | Status |
|---|---|---|---|
| grid | SGL Grid | Decentralized, confidential, OpenAI-compatible inference across attested TEE nodes | Live |
| machines | SGL Machines | GPU/VPS provisioning (Cloud Compute, High Performance, Dedicated, GPU) | Live |
| processors | Processors | "Serverless TEE functions. Deploy a function; it runs confidentially, on demand, and settles per call." | Soon |
| dai-comp | DAI Comp | "Confidential, decentralized training & fine-tuning. Run jobs across attested GPU nodes with your data sealed end-to-end." | Soon |
| vault | Vault | "Encrypted persistent storage. Only attested enclaves can decrypt your state." | Soon |
| pouches | Pouches | "Lightweight encrypted SQLite pouches. Spin up tiny, on-demand databases per agent or workload, sealed inside the enclave." | Soon |
| clusters | Clusters | "Spin up your own branded slice of the grid. Recruit nodes, route inference, and earn on every request." | Soon |
| hivemind | Hivemind | "Shard one giant model across many grid nodes. Pooled VRAM runs models too large for any single machine to hold." | Roadmap |

**The endgame (agent factories):** referenced ONLY as a CLASSIFIED teaser — "the final product, running on Singularity infra." Never named.

## 4. Content model (single source of truth)

To prevent drift, division/sub-product/experiment copy lives in **typed data modules** in the EHLabs repo:
- `src/data/products.ts` — divisions + cloud-network sub-products (name, slug, tagline, description, status, links).
- `src/data/research.ts` — research tracks, experiments (SCN-### metadata), papers.

Pages render from these modules. The repo `eh-labs-research` remains the canonical *narrative* record; the site data mirrors it. (No CMS/MDX yet — YAGNI.)

## 5. Components (reuse existing CRT/TVA "intense" theme)

Extract/add to `src/components/`:
- `ui/SectionHeading`, `ui/CornerMarkers` (extract from the current research page), `ui/StatusBadge`, `ui/ClassifiedTeaser`.
- `nav/TopNav` — persistent header (Home · Research · Products), CRT-styled.
- `cards/DivisionCard`, `cards/ExperimentCard`.
Reuse `ScrambledText`, scanline overlay, corner markers, orange `lab(57.341% 57.7263 58.8116)`, sharp corners, monospace fonts. Enforce dark + `intense` theme on each page (as the home page does).

## 6. Internal research-practices roadmap (repo: `eh-labs-research`)

- **`RESEARCH.md`** (new) — the fixed path: **mission → thesis → research tracks (mapped to the stack) → methodology (experiment lifecycle: hypothesis → design → run → document → conclude → feed papers/products) → SCN-### discipline (naming, reproducibility, honest scope, definition-of-done) → cadence → how findings graduate into papers & products.** Explicitly answers "when is an experiment done, when do we open the next SCN."
- **`ROADMAP.md`** (existing) — re-scope header to clarify it's the *product/phase* roadmap; `RESEARCH.md` is the *practices* roadmap. Cross-link.
- **`papers/`** (new) — `README.md` index + `_TEMPLATE.md` for future research papers.
- Align `experiments/_TEMPLATE/` with the `RESEARCH.md` methodology.
- **SCN-001 stays a proof-of-concept** (no further extension); its writeup already states scope honestly.

## 7. Build phasing (one branch → PR on `ivaavimusic/EHLabs`)

- **P1 (this iteration):** TopNav · Home (vision) · Products hub · Cloud Network sub-hub · Research · Experiments index · SCN-001 experiment page · data modules · `RESEARCH.md` + `papers/` in the repo.
- **P2:** Dedicated division pages (`/products/[slug]`).
- **P3:** Cloud Network sub-product pages (`/products/cloud-network/[slug]`) + Papers section fill-out.

Each phase: `npm run build` must pass; ship as PR (don't push to `main`).

## 8. Scope / non-goals (YAGNI)

- No CMS, no MDX pipeline, no blog engine yet — typed data + the existing page patterns.
- No live data wiring to the cloud platform (explicitly out of scope; EHLabs site is static/marketing).
- No new design system — strictly reuse the established CRT/TVA theme.
- The endgame is never named.

## 9. Success criteria

- A visitor immediately understands EHLabs's thesis and sees a credible, Anthropic-style split of **Research** and **Products**.
- Every real division & Cloud Network sub-product is represented with accurate, source-true copy and a status.
- The Research section shows a *disciplined program* (methodology + SCN-### + papers), with SCN-001 as the featured proof-of-concept — the moat is legible.
- Internal `RESEARCH.md` gives a fixed path so future experiments connect rather than scatter.
