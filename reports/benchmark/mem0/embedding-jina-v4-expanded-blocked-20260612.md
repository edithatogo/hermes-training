# Jina v4 Expanded Embedding Benchmark Blocked - 2026-06-12

Candidate: `jinaai/jina-embeddings-v4`

Status: blocked before scoring

Command:

```bash
source scripts/env.sh
./.venv/bin/python scripts/run_sentence_transformers_embedding_benchmark.py \
  --model jinaai/jina-embeddings-v4 \
  --device mps \
  --trust-remote-code \
  --suite benchmarks/embeddings/memory_retrieval_expanded_suite.json \
  --run-id embedding-jina-v4-expanded-20260612 \
  --force-exit-after-write
```

Result:

The run downloaded the model's custom code but failed before producing any
embedding rows.

Primary error:

```text
ImportError: cannot import name 'SlidingWindowCache' from 'transformers.cache_utils'
```

Interpretation:

This is not a retrieval-quality failure. It is a local runtime compatibility
failure between the candidate's custom Qwen2.5-VL-backed code path and the
currently installed `transformers` package.

Decision:

Keep `jinaai/jina-embeddings-v4` blocked for local mem0 benchmarking until one
of these is true:

- the benchmark environment is updated to a compatible `transformers` version
- a pinned model revision with compatible custom code is selected
- the run is offloaded to a clean cloud environment with a compatible stack

The smaller MLX lanes remain the practical local Jina candidates because they
already have local retrieval smoke evidence.
