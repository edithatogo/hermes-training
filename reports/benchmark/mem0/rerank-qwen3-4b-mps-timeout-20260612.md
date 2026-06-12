# Qwen3-Reranker-4B MPS Reranking Attempt Timed Out - 2026-06-12

Candidate: `Qwen/Qwen3-Reranker-4B`

Status: accelerated MPS path blocked

The CPU fixed-suite benchmark for this candidate is already recorded and passed:

```text
reports/benchmark/mem0/rerank-qwen3-4b-fixed-smoke-20260612.md
```

This follow-up attempted the same fixed reranking gate on MPS with a shorter
sequence length:

```bash
source scripts/env.sh
./.venv/bin/python scripts/run_fixed_reranking_benchmark.py \
  --strategy qwen3_causal_lm \
  --model Qwen/Qwen3-Reranker-4B \
  --qwen3-device mps \
  --qwen3-max-length 512 \
  --suite benchmarks/mem0_reranking/fixed_candidate_suite.json \
  --run-id rerank-qwen3-4b-fixed-20260612
```

Result:

```text
Timed out after 900 seconds before producing a scored case.
```

Interpretation:

This is not a quality failure because no cases were scored. The existing CPU
run remains the quality proof. The MPS path is not usable as the default local
reranker path until it can load and score within a bounded time window.

Decision:

Keep `Qwen/Qwen3-Reranker-4B` as a CPU-proven quality ceiling / teacher
comparison. Do not promote it for daily mem0 reads unless a faster runtime,
smaller quantized path, or cloud/offloaded service passes the live replay and
latency gates.
