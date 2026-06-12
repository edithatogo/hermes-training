# Jina Embeddings v4 Benchmark Attempt: runtime blocked

Date: 2026-06-12
Model: `jinaai/jina-embeddings-v4`
Runtime: `sentence-transformers`
Device requested: `cpu`
Cache root: `/Volumes/PortableSSD/huggingface`

## Attempts

The first load without remote code failed because the model requires custom Sentence Transformers modules.

The second load used `--trust-remote-code`. It exposed additional local prerequisites, so `pillow` and `peft` were installed into the project virtual environment and added to `requirements-mem0-embeddings.txt`.

The benchmark still did not start because the remote Jina code imports a cache utility that is not present in the current Transformers stack:

```text
ImportError: cannot import name 'SlidingWindowCache' from 'transformers.cache_utils'
```

## Decision

Keep `jinaai/jina-embeddings-v4` as runtime-blocked. Do not change the shared Transformers stack just to satisfy this model until that upgrade is tested against PyLate, Qwen3 reranking, MLX candidates, and the existing benchmark scripts.
