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
| Storage | `~/.mem0`, with Ollama models SSD-backed under `/Volumes/PortableSSD/Ollama/models` |

Do not replace the working setup just to test a candidate. New candidates should be added behind a run card and a benchmark result first.

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

## Promotion Gates

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
