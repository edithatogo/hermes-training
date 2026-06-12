# OpenAI Memory Extraction Benchmark: extraction-hermes4-14b-q4-smoke-20260613

Date: 2026-06-12T14:07:01.331669+00:00
Model: `hermes-4-14b-q4`
Endpoint: `http://127.0.0.1:8092/v1`
Runtime: `llama.cpp`
Artifact: `/Volumes/PortableSSD/hermes-models/frontier-gguf/hermes-4-14b-q4/Hermes-4-14B_Q4_k_m.gguf`
Raw output: `/Volumes/PortableSSD/hermes-evals/mem0-extraction-benchmark/extraction-hermes4-14b-q4-smoke-20260613`
Run card: `reports/benchmark/mem0/run-cards/extraction-hermes4-14b-q4-smoke-20260613.md`

## Result

| Metric | Value |
|---|---:|
| Cases | 7 |
| Pass rate | 0.286 |
| JSON validity rate | 0.286 |
| Expected extraction rate | 0.714 |
| Forbidden hit rate | 0.000 |
| Empty-case pass rate | 1.000 |
| Latency p50 | 0.355s |
| Latency p95 | 2.204s |

## Cases

| Case | Category | Pass | JSON valid | Memories |
|---|---|---:|---:|---:|
| durable-project-preference | preference | False | False | 0 |
| transient-noise | ignore_transient | False | False | 0 |
| tool-state | tool_state | False | False | 0 |
| secret-rejection | secret_rejection | False | False | 0 |
| runtime-endpoint-preference | tool_state | True | True | 1 |
| rollback-extractor-update | preference_update | True | True | 1 |
| status-update-noise | ignore_transient | False | False | 0 |

## Failure Mode

Hermes 4 mostly followed the user-facing instruction instead of the extraction
contract. Five of seven responses were conversational text rather than the
required JSON object with a `memories` array. The model avoided forbidden secret
retention, but it missed durable preference/tool-state extraction and failed the
JSON validity gate.

## Decision

Reject for mem0 default extraction. Keep `sam860/LFM2:2.6b` as the default and
rollback extractor because the clean-root LFM2 smoke passed 7/7 with JSON
validity 1.000. Hermes 4 remains useful as a Hermes-aligned runtime baseline or
teacher candidate, but not as the current mem0 extraction model without a prompt
or chat-template change followed by a fresh benchmark.

## Command

```bash
source scripts/env.sh
./.venv/bin/python scripts/run_openai_memory_extraction_benchmark.py \
  --model hermes-4-14b-q4 \
  --base-url http://127.0.0.1:8092/v1 \
  --suite benchmarks/mem0_extraction/smoke_suite.json \
  --run-id extraction-hermes4-14b-q4-smoke-20260613
```
