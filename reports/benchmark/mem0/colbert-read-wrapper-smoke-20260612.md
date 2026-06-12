# ColBERT Read Wrapper Smoke - 2026-06-12

## Scope

This smoke verifies the new opt-in `colbert` read mode without touching the live
mem0 database. The test used synthetic mem0-style result rows and the local
`LiquidAI/LFM2-ColBERT-350M` retriever service on `http://127.0.0.1:8765`.

## Command

```bash
source scripts/env.sh
HF_HOME=/Volumes/PortableSSD/huggingface HF_HUB_CACHE=/Volumes/PortableSSD/huggingface/hub \
  ./.venv/bin/python scripts/lfm2_colbert_service.py \
    --host 127.0.0.1 \
    --port 8765 \
    --model LiquidAI/LFM2-ColBERT-350M \
    --device auto \
    --local-files-only \
    --quiet

source scripts/env.sh
./.venv/bin/python - <<'PY'
from scripts.mem0_rerank_search import rerank_search_results

results = [
    {"id": "old", "memory": "Old preference: use Hermes3 as the extractor.", "score": 0.91},
    {"id": "target", "memory": "Current rollback extractor is sam860/LFM2:2.6b for mem0 memory extraction.", "score": 0.88},
    {"id": "noise", "memory": "Benchmark outputs must be stored on the external SSD.", "score": 0.70},
]
ranked, latency = rerank_search_results(
    "Which extractor should remain the rollback extractor?",
    results,
    "retriever_service",
    0.2,
    None,
    "cpu",
    1024,
    "Retrieve memories that answer the query for a local Hermes agent.",
    False,
    None,
    1024,
    "http://127.0.0.1:8765",
    120.0,
)
print({"top_id": ranked[0]["id"], "latency_s": round(latency, 3), "count": len(ranked)})
PY
```

## Result

```json
{"top_id": "target", "latency_s": 0.445, "count": 3}
```

## Decision

`scripts/mem0_read.py --mode colbert` and `scripts/hermes_mem0_tool.py --mode colbert`
are now available as explicit, read-only, retriever-service backed modes. Keep
the mode opt-in until the live wrapper has broader cold/warm latency probes and
a documented fallback path for when the ColBERT service is not running.
