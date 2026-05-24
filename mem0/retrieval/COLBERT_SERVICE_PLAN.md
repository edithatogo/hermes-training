# ColBERT / Late-Interaction Retriever Service Plan

`LiquidAI/LFM2-ColBERT-350M` is not a dense-vector drop-in replacement for
`nomic-embed-text:latest`. It needs a separate late-interaction index and a
retriever service boundary.

## Service Contract

```http
GET /health
POST /index
POST /retrieve
```

`GET /health` should return:

```json
{
  "ok": true,
  "model_id": "LiquidAI/LFM2-ColBERT-350M",
  "index_id": "mem0_lfm2_colbert_350m",
  "device": "mps|cpu|metal|other"
}
```

`POST /index` should accept source records:

```json
{
  "index_id": "mem0_lfm2_colbert_350m",
  "documents": [
    {
      "doc_id": "memory-id",
      "text": "memory text",
      "metadata": {
        "created_at": "2026-05-24T00:00:00+00:00",
        "source": "mem0"
      }
    }
  ]
}
```

`POST /retrieve` should return ranked hits:

```json
{
  "query": "What is the current rollback extractor?",
  "results": [
    {
      "doc_id": "memory-id",
      "score": 0.0,
      "text": "memory text",
      "metadata": {
        "created_at": "2026-05-24T00:00:00+00:00",
        "model_id": "LiquidAI/LFM2-ColBERT-350M",
        "index_id": "mem0_lfm2_colbert_350m"
      }
    }
  ]
}
```

## Local Artifacts

Keep late-interaction artifacts outside Git:

| Artifact | Path |
|---|---|
| index root | `/Volumes/PortableSSD/hermes-indexes/mem0_lfm2_colbert_350m` |
| run outputs | `/Volumes/PortableSSD/hermes-evals/mem0-retriever-benchmark/<run-id>` |
| reports | `reports/benchmark/mem0/` |

## First Benchmark Gate

The first ColBERT gate should reuse the same memory retrieval facts as the dense
embedding suite, but through `POST /retrieve`.

```bash
source scripts/env.sh
./.venv/bin/python scripts/run_retriever_service_benchmark.py \
  --base-url http://127.0.0.1:8765 \
  --suite benchmarks/embeddings/memory_retrieval_suite.json \
  --run-id retriever-lfm2-colbert-$(date +%Y%m%d-%H%M%S)
```

Required metrics:

- Top-1 accuracy
- Recall@3
- MRR
- nDCG@3
- p50/p95 query latency
- index size
- device and peak memory notes

Do not wire this service into live mem0 until it beats or ties
`nomic-embed-text:latest` on recall and latency, and has a rollback path back
to `mem0_nomic_768`.
