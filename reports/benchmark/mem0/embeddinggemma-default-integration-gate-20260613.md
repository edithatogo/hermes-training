# EmbeddingGemma mem0 Default Integration Gate - 2026-06-13

## Decision

EmbeddingGemma GGUF is now an opt-in mem0/Hermes read profile, not the default.
The default remains the existing `nomic-embed-text:latest` profile and
`mem0_nomic_768` collection until a later promotion commit deliberately changes
both write and read behavior.

The opt-in profile uses:

| Surface | Value |
|---|---|
| Read mode | `embeddinggemma-proxy` |
| Rerank policy | `query_terms_guarded` |
| Config selection | explicit `--mem0-config-path` or `MEM0_CONFIG_PATH` |
| Embedder endpoint | OpenAI-compatible embeddings endpoint, usually the resilient llama.cpp proxy |
| Collection | `mem0_embeddinggemma_300m_768` for promotion proof |
| Default mutation | none |

## Why It Is Opt-In

The direct differentiation suite and fresh isolated mem0 fixture both reached
top-1 `1.000` / recall@3 `1.000` with EmbeddingGemma GGUF. That is strong
enough to expose an explicit Hermes read mode. It is not enough to silently
replace the user's default memory store, because the default collection has
existing data, operational habits, and rollback expectations tied to
`mem0_nomic_768`.

## Runtime Profile

Render an SSD-local mem0 config:

```bash
source scripts/env.sh
./.venv/bin/python scripts/render_mem0_embeddinggemma_config.py \
  --base-config ~/.mem0/config.json \
  --output /Volumes/PortableSSD/hermes-evals/mem0-profiles/embeddinggemma-300m-qat-gguf/config.json \
  --collection-name mem0_embeddinggemma_300m_768 \
  --qdrant-path /Volumes/PortableSSD/hermes-evals/mem0-profiles/embeddinggemma-300m-qat-gguf/qdrant \
  --history-db-path /Volumes/PortableSSD/hermes-evals/mem0-profiles/embeddinggemma-300m-qat-gguf/history.db \
  --base-url http://127.0.0.1:8105/v1 \
  --model embeddinggemma-300m-qat-Q4_0.gguf \
  --embedding-dims 768
```

Run a read through the explicit profile after the embedding endpoint is up:

```bash
source scripts/env.sh
./.venv/bin/python scripts/mem0_read.py "active collection" \
  --mode embeddinggemma-proxy \
  --mem0-config-path /Volumes/PortableSSD/hermes-evals/mem0-profiles/embeddinggemma-300m-qat-gguf/config.json \
  --cache-ttl-s 0
```

Hermes-agent should call the stable tool wrapper with the same explicit profile:

```bash
source scripts/env.sh
printf '%s\n' '{"query":"active collection","mode":"embeddinggemma-proxy","mem0_config_path":"/Volumes/PortableSSD/hermes-evals/mem0-profiles/embeddinggemma-300m-qat-gguf/config.json","cache_ttl_s":0}' \
  | ./.venv/bin/python scripts/hermes_mem0_tool.py
```

For fixture or benchmark runs, keep using
`scripts/run_resilient_llama_cpp_embedding_proxy.py` around the command so the
llama.cpp embedding backend is stopped after the command exits.

## Rollback

Rollback is selecting the existing default profile:

```bash
unset MEM0_CONFIG_PATH
./.venv/bin/python scripts/mem0_read.py "active collection" --mode close-margin
```

No migration is required to roll back from the opt-in profile because
`embeddinggemma-proxy` only uses a supplied config path. It does not edit
`~/.mem0/config.json`, does not rename collections, and reports
`mutates_mem0_config: false`.

## Collection Rule

`nomic-embed-text:latest` and EmbeddingGemma GGUF both produce 768-dimensional
dense vectors in the current evidence, so the dimensions do not force a new
collection. The promotion rule is still to use a new collection,
`mem0_embeddinggemma_300m_768`, until a migration run proves that existing
memories have been re-embedded with the same model and distance metric.

Do not mix old `nomic-embed-text:latest` vectors and new EmbeddingGemma vectors
inside `mem0_nomic_768`; identical dimensions do not imply identical vector
space semantics.

## Evidence

- `mem0-live-fixture-embeddinggemma-query-guard-pathfix-20260613`: live isolated
  fixture, top-1 `1.000`, recall@3 `1.000`, MRR `1.000`, nDCG@3 `1.000`.
- `embeddinggemma-default-profile-smoke-pass-20260613`: opt-in profile add/search
  smoke through the resilient llama.cpp proxy, required collection text found,
  total latency `0.910s`, search latency `0.016s`, and SSD-local Qdrant/history
  paths.
- `embeddinggemma-hermes-tool-profile-smoke-20260613`: Hermes wrapper contract
  smoke passed with `read_only: true`, `mutates_mem0_config: false`, and the
  explicit `mem0_config_path` preserved. It returned no memories through the
  shell CLI path, so it is wrapper-contract evidence rather than retrieval
  quality evidence.
- `embeddinggemma-fixture-replay-query-guard-20260613`: replayed captured
  candidates, top-1 `1.000`, recall@3 `1.000`.
- `embeddinggemma-proxy-read-mode-smoke-20260613`: `scripts/mem0_read.py`
  smoke through the new `embeddinggemma-proxy` mode. It used the populated
  fixture config, returned `Qwen3 v4 targeted` as the top memory, reported
  `read_only: true` / `mutates_mem0_config: false`, and wrote logs under
  `/Volumes/PortableSSD/hermes-evals/server-logs/embeddinggemma-proxy-read-mode-smoke-20260613`.
- `embeddinggemma-proxy-hermes-tool-smoke-20260613`:
  `scripts/hermes_mem0_tool.py` contract smoke through the same proxy. It
  returned `nomic-embed-text:latest` as the top memory for the default rollback
  query and wrote logs under
  `/Volumes/PortableSSD/hermes-evals/server-logs/embeddinggemma-proxy-hermes-tool-smoke-20260613`.
- Focused unit tests cover the fail-closed config requirement and Hermes wrapper
  contract for `embeddinggemma-proxy`.

## Promotion Checklist

- Run the opt-in profile against the user's real representative mem0 workload
  with SSD-local output and no global config mutation.
- Backfill/re-embed a copy of the live store into
  `mem0_embeddinggemma_300m_768`.
- Compare against the current default on the differentiation suite plus a
  user-history replay.
- Keep a rollback command in the release note.
- Only then change defaults in a separate promotion commit.
