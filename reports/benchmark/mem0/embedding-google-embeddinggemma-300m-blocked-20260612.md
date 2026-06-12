# EmbeddingGemma Benchmark Attempt: blocked

Date: 2026-06-12
Model: `google/embeddinggemma-300m`
Runtime: `sentence-transformers`
Device requested: `cpu`
Cache root: `/Volumes/PortableSSD/huggingface`

## Result

The direct mem0 embedding benchmark did not start because Hugging Face returned a gated repository error for `google/embeddinggemma-300m`.

Blocked request:

```text
https://huggingface.co/google/embeddinggemma-300m/resolve/main/config.json
```

Error class:

```text
GatedRepoError: Access to model google/embeddinggemma-300m is restricted and you are not in the authorized list.
```

## Decision

Keep EmbeddingGemma in the candidate queue as an access-gated baseline. It cannot be compared fairly until the Hugging Face account has access or an equivalent open artifact is selected.
