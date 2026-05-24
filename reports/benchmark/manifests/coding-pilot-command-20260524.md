# Coding Pilot Command Manifest

Date: 2026-05-24

## Purpose

Run a small coding sanity pilot for models that will be described as useful for Hermes development or code-oriented agent workflows.

## Gate

- Candidate must have a stable endpoint.
- Candidate must pass the local runtime smoke.
- Sandboxed execution must be enabled and recorded.
- Output root must be on `/Volumes/PortableSSD`.

## Command

```bash
source scripts/env.sh
RUN_ID=<model>-coding-pilot-<date>
MODEL_ID=<runtime_model_id>
BASE_URL=http://127.0.0.1:<port>/v1
OUT=/Volumes/PortableSSD/hermes-evals/standard-benchmarks/coding/${RUN_ID}
mkdir -p "$OUT"

python -m lm_eval \
  --model local-completions \
  --tasks humaneval,mbpp \
  --limit 10 \
  --batch_size 1 \
  --output_path "$OUT"
```

If code execution evaluation is unavailable locally, generate completions only and record the execution blocker. Do not report pass@k without executing tests.

## Result Card Schema

```json
{
  "run_id": "<model>-coding-pilot-<date>",
  "suite": "coding-pilot",
  "model": "<runtime_model_id>",
  "base_url": "http://127.0.0.1:<port>/v1",
  "tasks": ["humaneval", "mbpp"],
  "limit": 10,
  "raw_output": "/Volumes/PortableSSD/hermes-evals/standard-benchmarks/coding/<run-id>",
  "execution_enabled": false,
  "pass_at_1": null,
  "compile_error_rate": null,
  "timeout_rate": null,
  "publish_decision": "pilot-only"
}
```

## Publication Boundary

Public coding claims require executed tests, pass@k methodology, sandbox configuration, and raw generated solutions.

## Current Local Pilot Evidence

Because `lm_eval` is not installed in the active environment, the repo-native endpoint pilot was run first:

- Script: `scripts/run_endpoint_pilot_benchmark.py`
- Suite: `benchmarks/endpoint_pilots/coding_pilot.json`
- Report: `reports/benchmark/endpoint-pilots/qwen3-q4km-llamacpp-pilots-20260524.md`
- Raw output: `/Volumes/PortableSSD/hermes-evals/standard-benchmarks/endpoint-pilots/qwen3-q4km-llamacpp-coding-pilot-nothink-20260524`
- Result: `1.000`
