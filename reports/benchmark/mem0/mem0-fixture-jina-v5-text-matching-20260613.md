# mem0 Isolated Fixture: Jina v5 Text-Matching MLX

Date: 2026-06-12T14:16:58.973608+00:00
Run ID: `mem0-fixture-jina-v5-text-matching-20260613`
Embedder: `jinaai/jina-embeddings-v5-omni-small-text-matching-mlx`
Embedder runtime: local MLX server exposed as OpenAI-compatible `/v1/embeddings`
Embedding dims: 1024
Fixture collection: `mem0_fixture_mem0_fixture_jina_v5_text_matching_20260613`
Raw output: `/Volumes/PortableSSD/hermes-evals/mem0-isolated-fixture-rerank/mem0-fixture-jina-v5-text-matching-20260613`
Run card: `reports/benchmark/mem0/run-cards/mem0-fixture-jina-v5-text-matching-20260613.md`

## Result

| Strategy | Pass | Top-1 | Recall@3 | MRR | nDCG@3 | Recency conflict | Distractor resistance | p50 rerank |
|---|---:|---:|---:|---:|---:|---:|---:|---:|
| `vector` | 0.600 | 0.600 | 1.000 | 0.800 | 0.852 | 0.500 | 1.000 | 0.000s |
| `score_plus_created_at_rank_close_margin` | 0.800 | 0.800 | 1.000 | 0.900 | 0.926 | 1.000 | 1.000 | 0.000s |

| Metric | Value |
|---|---:|
| Add latency p50 | 3.039s |
| Add latency p95 | 3.504s |
| Search latency p50 | 2.978s |
| Search latency p95 | 3.030s |
| Added memories | 11 |
| Input count range | 2-5 |

## Failure Mode

The isolated config and local embedding endpoint worked, and the run used an
output-local Qdrant path through `MEM0_CONFIG_PATH`. It did not edit
`~/.mem0/config.json` or `mem0_nomic_768`.

The remaining failure was `tool-state-current-collection`: both vector and
close-margin reranking placed the older `mem0_legacy_1024` memory above the
current `mem0_nomic_768` memory. This means the Jina text-matching embedder is
not ready to replace the current default despite its 1.000 offline expanded
embedding score.

## Decision

Keep as a benchmarked candidate only. Do not promote to the default mem0
embedder or collection. The current daily path remains `nomic-embed-text:latest`
with guarded close-margin reads, because this live add/search fixture did not
clear the top-1 tool-state gate.

## Commands

Start the local Jina MLX embedding endpoint:

```bash
source scripts/env.sh
./.venv/bin/python scripts/jina_mlx_embedding_server.py \
  --model jinaai/jina-embeddings-v5-omni-small-text-matching-mlx \
  --task-type text-matching \
  --repo-dir /Volumes/PortableSSD/huggingface/hub/jina-mlx/jina-mlx-text-matching-smoke-20260612b \
  --local-files-only \
  --host 127.0.0.1 \
  --port 8094
```

Run the isolated mem0 fixture:

```bash
source scripts/env.sh
./.venv/bin/python scripts/run_mem0_isolated_fixture_rerank.py \
  --suite benchmarks/mem0_memory/recency_suite.json \
  --run-id mem0-fixture-jina-v5-text-matching-20260613 \
  --embedder-provider openai \
  --embedder-model jinaai/jina-embeddings-v5-omni-small-text-matching-mlx \
  --embedder-base-url http://127.0.0.1:8094/v1 \
  --embedding-dims 1024 \
  --skip-qwen3 \
  --timeout-s 120
```
