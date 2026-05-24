# mem0 Extraction Smoke

Date: 2026-05-24

## Commands

```bash
source scripts/env.sh
./.venv/bin/python scripts/run_ollama_memory_extraction_benchmark.py \
  --model 'sam860/LFM2:2.6b' \
  --suite benchmarks/mem0_extraction/smoke_suite.json \
  --run-id extraction-lfm2-2-6b-smoke-20260524

./.venv/bin/python scripts/run_ollama_memory_extraction_benchmark.py \
  --model 'hermes3:8b' \
  --suite benchmarks/mem0_extraction/smoke_suite.json \
  --run-id extraction-hermes3-8b-smoke-20260524
```

## Results

| Model | Pass rate | JSON validity | Expected extraction | Forbidden hit rate | Empty-case pass | Latency p50 | Latency p95 |
|---|---:|---:|---:|---:|---:|---:|---:|
| `sam860/LFM2:2.6b` | 0.333 | 0.667 | 0.667 | 0.333 | 0.000 | 0.786s | 3.634s |
| `hermes3:8b` | 0.333 | 0.333 | 0.667 | 0.000 | 1.000 | 1.031s | 26.531s |

Raw output:

- `/Volumes/PortableSSD/hermes-evals/mem0-extraction-benchmark/extraction-lfm2-2-6b-smoke-20260524/summary.md`
- `/Volumes/PortableSSD/hermes-evals/mem0-extraction-benchmark/extraction-hermes3-8b-smoke-20260524/summary.md`

## Findings

`sam860/LFM2:2.6b` is the better latency baseline and successfully extracted the tool-state path. It failed the preference case because it returned a list of objects instead of a list of strings, and it incorrectly stored a transient progress-spinner update.

`hermes3:8b` extracted the rollback preference cleanly and ignored the transient noise semantically, but it failed JSON validity on two cases and had one slow response around 29 seconds.

## Decision

Keep `sam860/LFM2:2.6b` as the current working extractor because it is already wired into mem0 and has better latency. Do not promote `hermes3:8b` as the extractor. The next extractor work should focus on:

1. stricter JSON-mode prompting or a repair parser for LFM2 outputs
2. transient/noise rejection examples
3. a larger extraction suite before changing the mem0 default
4. testing Hermes 4 only after a local runtime artifact exists

