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

## Smoke Result

2026-06-12: the local `LiquidAI/LFM2-ColBERT-350M` service completed the
memory retrieval smoke suite on MPS with:

- Top-1 accuracy: 1.000
- Recall@3: 1.000
- MRR: 1.000
- nDCG@3: 1.000
- Query latency p50: 0.149s
- Query latency p95: 0.200s

That satisfies the first service gate, but not the larger replay and rollback
comparison needed for default promotion.

## Hermes Tool Fixture Smoke

2026-06-12: `scripts/hermes_mem0_tool.py --mode colbert-qwen3` successfully
called the local ColBERT service against
`benchmarks/embeddings/memory_retrieval_expanded_suite.json`, then reranked the
eight returned candidates with `Qwen/Qwen3-Reranker-0.6B`. The query "Which
collection stores the current mem0 vectors?" returned `target-collection` as
the top memory with no mem0 config mutation.

Evidence:
`reports/benchmark/mem0/hermes-tool-colbert-qwen3-fixture-smoke-20260612.md`

This proves the Hermes command surface can call the candidate stack. It does
not yet prove live mem0 default integration because the document source is an
explicit fixture rather than the live memory store.
