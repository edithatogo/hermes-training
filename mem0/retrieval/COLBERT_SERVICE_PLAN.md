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

## Lifecycle Smoke

Use the service lifecycle smoke before any default-integration decision. It
starts the local ColBERT service with SSD-backed caches, waits for `/health`,
runs the opt-in `mem0_read.py --mode colbert` wrapper, stops the service, and
then verifies `--fallback-to-vector`.

```bash
source scripts/env.sh
./.venv/bin/python scripts/run_colbert_read_stack_smoke.py \
  --local-files-only \
  --run-id-prefix mem0-colbert-stack-$(date +%Y%m%d-%H%M%S)
```

The generated report is written under `reports/benchmark/mem0/`. Raw probe
outputs stay on the external SSD under
`/Volumes/PortableSSD/hermes-evals/mem0-read-latency/`, and service logs stay
under `/Volumes/PortableSSD/hermes-evals/service-logs/`.

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

## Default Promotion Rule

Keep ColBERT opt-in unless all of these are true:

- the lifecycle smoke passes service-up and service-down fallback checks;
- at least one live mem0 probe returns multiple candidates and ranks the target
  correctly through the retriever service;
- p50/p95 total read latency is acceptable for a Hermes memory-read tool;
- fallback returns useful vector-ordered results when the service is absent;
- the service lifecycle is supervised outside the agent process.

## Lifecycle Smoke Result

2026-06-12: `scripts/run_colbert_read_stack_smoke.py` passed a bounded
two-query lifecycle smoke with local files only:

- service health: `LiquidAI/LFM2-ColBERT-350M` on MPS;
- service-up reads: success `2`, fallback `0`, p50 total `3.099s`, retriever
  latency `0.238s`;
- service-down fallback: success `1`, fallback `1`, p50 total `2.898s`;
- raw outputs: `/Volumes/PortableSSD/hermes-evals/mem0-read-latency/`;
- report:
  `reports/benchmark/mem0/mem0-colbert-stack-20260612-read-stack-smoke.md`.

This is lifecycle evidence only because the live mem0 queries returned
singleton candidate sets. It does not satisfy the multi-result
default-promotion rule.
