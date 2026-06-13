# mem0 Model Lab

This lane is for improving the local mem0 stack that backs cross-agent memory on this machine.

It is deliberately separate from the Hermes chat/tool-call lane:

- Hermes models are judged on assistant behavior, tool calls, JSON shape, and runtime integration.
- mem0 extraction models are judged on whether useful memories are written, deduplicated, updated, and retrieved.
- embedding and retriever models are judged on semantic recall, recency conflict handling, latency, and index compatibility.

The current working setup is:

| Component | Current value |
|---|---|
| Memory CLI | `mem0` |
| Vector store | local Qdrant |
| Collection | `mem0_nomic_768` |
| Embedder | `nomic-embed-text:latest` through Ollama |
| Extraction / LLM | `sam860/LFM2:2.6b` through Ollama |
| Storage | `~/.mem0`, with the validated mem0 Ollama root at `/Volumes/PortableSSD/Ollama/mem0-clean-models` |

Do not replace the working setup just to test a candidate. New candidates should be added behind a run card and a benchmark result first.
The leading 768-dimension challenger is now `lmstudio-community/embeddinggemma-300m-qat-GGUF` served through the resilient llama.cpp embedding proxy. It outperforms the current default on isolated retrieval and passes the output-local live mem0 fixture with raw vector and query-guarded strategies at top-1 `1.000` / recall@3 `1.000`. A copied live-store replay then reached default-top recall `1.000` but top-1 match only `0.200`, so it remains opt-in rather than the default.

## Structure

```
mem0/
├── README.md                  -> lane overview and current state
├── BENCHMARKS.md              -> mem0-specific benchmark plan
├── MODEL_CANDIDATES.yaml      -> candidate extraction, embedding, reranker, and store models
├── RUNTIME_TARGETS.md         -> Ollama, llama.cpp, LM Studio, MLX, and Metal rules
├── data/                      -> contrastive memory/retrieval seed data
├── extraction/                -> extractor prompt and gate evidence
├── retrieval/                 -> late-interaction and retriever service plans
├── reranking/                 -> post-retrieval ranking experiments
├── training/                  -> future fine-tuning recipes for embedders/retrievers/rerankers
└── embeddings/
    └── README.md              -> embedding adaptation lane
```

Shared benchmark fixtures live under `benchmarks/mem0_memory/`.

Shared scripts live under `scripts/`, starting with:

```bash
source scripts/env.sh
./.venv/bin/python scripts/run_mem0_memory_benchmark.py --dry-run
```

The current candidate execution queue is generated from
`mem0/MODEL_CANDIDATES.yaml`:

```bash
source scripts/env.sh
./.venv/bin/python scripts/build_mem0_candidate_queue.py
```

Output: `reports/model-radar/mem0-candidate-queue.md`.

For heavier embedding, reranker, or training sweeps that should move off the
Mac, use the hub Colab lane in [COLAB_SCALEOUT.md](../COLAB_SCALEOUT.md). The
supported pattern is `scripts/colab_preflight.py` followed by
`scripts/colab_dispatch.py`, with GPU-first ordering and TPU only for
JAX/PyTorch-XLA-compatible jobs.

## Promotion Gates

Read-wrapper integration is not the same as default mem0 config promotion. A
guarded read wrapper such as `scripts/mem0_read.py` may be used by agents if it
is read-only, rollback is raw `mem0 cmd search`, and current latency plus
fixture evidence are recorded. Changing `~/.mem0/config.json`, the default
collection, embedder, or extractor still requires the full default-promotion
gates below.

For Hermes-agent integration, use the explicit command contract in
[`HERMES_AGENT_TOOL.md`](./HERMES_AGENT_TOOL.md). It wraps the same guarded read
path and keeps memory lookup intentional rather than adding a memory prelude to
every turn.

Every mem0 candidate must pass these gates before becoming the default:

| Gate | Purpose | Required evidence |
|---|---|---|
| config-smoke | mem0 can start with the candidate | `mem0 status` plus exact config diff |
| add-search-smoke | memories can be written and retrieved | `scripts/run_mem0_memory_benchmark.py` summary |
| recency-conflict | newer memory beats older memory | dedicated benchmark cases |
| distractor-resistance | irrelevant memories do not dominate | dedicated benchmark cases |
| latency | local use remains responsive | p50 and p95 add/search latency |
| rollback | old working config can be restored | saved config path and collection name |

Use a new Qdrant collection when embedding dimensions change. Never mix 768, 1024, 1536, or late-interaction indexes in one collection.

## Default-Switch Policy

Do not switch the mem0 default embedder or reranker unless the challenger has:

| Criterion | Minimum bar |
|---|---|
| Retrieval quality | Top-1 and Recall@3 at least match the current default on the same fixture class |
| Recency handling | Recency-conflict pass rate is 1.000 on the replay suite |
| Distractor handling | Distractor-resistance pass rate is 1.000 on the replay suite |
| Latency | p50/p95 stay within the current daily-use budget for the same hardware path |
| Footprint | The model fits the target index/runtime without swapping or unsupported runtime hacks |
| Reproducibility | Run card, exact model ID, collection name, and rollback command are recorded |
| Rollback | `nomic-embed-text:latest` and `mem0_nomic_768` remain intact and restorable |

Migration plan if a challenger wins:

1. Create a separate collection for the new embedding dimensions or index shape.
2. Replay the smoke and recency/distractor suites against both old and new paths.
3. Stage the new default behind an explicit config diff and run card.
4. Keep the old collection and config available until a full rollback smoke passes.
5. Restore the previous config with `mem0 cmd search` if the new path regresses.

EmbeddingGemma has the same 768-dimensional vector shape as the current nomic
default, but it must still use a separate candidate collection for promotion
testing:

```text
mem0_embeddinggemma_300m_768
```

Render the opt-in profile without editing `~/.mem0/config.json`:

```bash
source scripts/env.sh
./.venv/bin/python scripts/render_mem0_embeddinggemma_config.py
```

Use the printed config path with `MEM0_CONFIG_PATH` only after starting the
resilient llama.cpp embedding proxy. Rollback remains the unmodified default:
unset `MEM0_CONFIG_PATH`, use `nomic-embed-text:latest`, and read/write
`mem0_nomic_768`.

Copied live-store replay evidence is recorded at
[`reports/benchmark/mem0/embeddinggemma-live-store-replay-20260613.md`](../reports/benchmark/mem0/embeddinggemma-live-store-replay-20260613.md).
It copied a bounded `default_user` / `codex` sample into a run-scoped
EmbeddingGemma collection, wrote private raw artifacts under
`/Volumes/PortableSSD/hermes-evals/mem0-live-store-replay/`, and committed only
redacted hashes and aggregate metrics. Result: default top memory was present in
candidate results for every comparable query, but the rank order differed
enough to block default promotion.

## Candidate Roles

mem0 needs several model roles, not just a chat model:

- `extractor`: turns raw turns into compact memory records.
- `embedder`: encodes memory records and queries for vector search.
- `reranker`: reorders retrieved memory candidates.
- `retriever`: handles multi-vector or ColBERT-style retrieval.
- `summarizer`: compresses older or duplicated memory entries.

The default daily path should remain simple: Ollama embedder, local Qdrant, and a small local extraction model. Experimental retrieval stacks belong in separate collections or indexes until they beat the default.

## Fine-Tuning Direction

Embedding and retriever fine-tuning starts from contrastive triplets, not chat conversations:

```bash
./.venv/bin/python scripts/validate_mem0_triplets.py mem0/data/contrastive_seed.jsonl
```

The seed data is only a schema lock. A real training pass needs a larger, safe corpus with source/license notes and a held-out retrieval set.
