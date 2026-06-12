# Hermes Agent mem0 Tool Contract

`scripts/hermes_mem0_tool.py` is the explicit Hermes-agent command surface for
local mem0 reads. It wraps `scripts/mem0_read.py`, keeps the close-margin
reranker as the default, and leaves mem0 defaults unchanged.

## Command

```bash
source scripts/env.sh
./.venv/bin/python scripts/hermes_mem0_tool.py \
  --query "What is the active mem0 Qdrant collection?"
```

Stdin JSON is also supported:

```bash
printf '{"query":"What is the active mem0 Qdrant collection?","cache_ttl_s":300}\n' \
  | ./.venv/bin/python scripts/hermes_mem0_tool.py
```

The checked-in manifest is
`mem0/integration/hermes_agent_mem0_read_tool.json`.

## Hermes Plugin Shim

Hermes Agent loads tools through plugins rather than raw JSON manifests. The
safe local wiring path is the user plugin at:

`~/.hermes/plugins/hermes-mem0-read`

The tracked plugin template is `mem0/integration/hermes-mem0-read`. It reads
the checked-in JSON manifest, registers `hermes_mem0_read` under the
`hermes_mem0` toolset, and invokes the command with stdin JSON. This keeps the
dirty `/Volumes/PortableSSD/GitHub/hermes-agent` checkout untouched while still
making the mem0 read wrapper available to Hermes.

Enable or verify it with:

```bash
hermes plugins enable hermes-mem0-read
HERMES_PLUGINS_DEBUG=1 hermes tools list
```

## Contract

- Read-only: true.
- Mutates `~/.mem0/config.json`: false.
- Default mode: `close-margin`.
- Rollback mode: `vector`.
- Experimental mode: `qwen3` with optional `fallback_to_vector`.
- Experimental service mode: `colbert` reranks normal mem0 CLI results through
  the local ColBERT retriever service.
- Experimental fixture mode: `colbert-qwen3` retrieves from an explicit JSON
  document fixture through the ColBERT service and then reranks with Qwen3.
- Cache: opt-in TTL, default `300s` for this command wrapper.

Use `refresh_cache: true` after memory writes or when validating a changed
store. Do not wire this as an automatic every-turn prelude; use it as an
explicit or cached memory-read tool.

## ColBERT + Qwen3 Fixture Mode

Use this only when the local ColBERT service is already running. It is useful
for integration checks and controlled fixtures, not live default mem0 reads:

```bash
source scripts/env.sh
./.venv/bin/python scripts/hermes_mem0_tool.py \
  --query "Which collection stores the current mem0 vectors?" \
  --mode colbert-qwen3 \
  --document-fixture benchmarks/embeddings/memory_retrieval_expanded_suite.json \
  --retriever-service-url http://127.0.0.1:8765 \
  --retriever-top-k 8 \
  --qwen3-device cpu \
  --qwen3-max-length 1024 \
  --qwen3-local-files-only
```

The 2026-06-12 fixture smoke passed and is recorded in
`reports/benchmark/mem0/hermes-tool-colbert-qwen3-fixture-smoke-20260612.md`.
Keep this mode opt-in until live mem0 indexing, service lifecycle, and rollback
behavior are proven.

## ColBERT Live Wrapper Lifecycle Smoke

Use this before considering `colbert` as a daily Hermes memory-read mode:

```bash
source scripts/env.sh
./.venv/bin/python scripts/run_colbert_read_stack_smoke.py \
  --local-files-only \
  --run-id-prefix mem0-colbert-stack-$(date +%Y%m%d-%H%M%S)
```

The smoke starts `scripts/lfm2_colbert_service.py`, waits for `/health`, probes
`scripts/mem0_read.py --mode colbert --fallback-to-vector`, stops the service,
and verifies that the wrapper falls back to vector ordering when the service is
down. Keep this path opt-in unless a live probe has multiple returned mem0
candidates, ranks the right memory first, and has acceptable p50/p95 latency.

2026-06-12 lifecycle smoke evidence:
`reports/benchmark/mem0/mem0-colbert-stack-20260612-read-stack-smoke.md`.
It passed service-up and service-down fallback checks, but the live mem0
queries returned singleton candidate sets, so it is not default-promotion
evidence.

2026-06-12 multi-result fixture evidence:
`reports/benchmark/mem0/mem0-live-fixture-colbert-rerank-20260612.md`.
ColBERT completed the six-case isolated mem0 fixture with 3-5 candidates per
query and reached pass/top-1 `0.833`, improving over raw vector ordering
`0.667` but trailing the default close-margin guarded read at `1.000`.
