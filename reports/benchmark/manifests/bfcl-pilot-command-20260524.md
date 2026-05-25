# BFCL Pilot Command Manifest

Date: 2026-05-24

## Purpose

Run a small Berkeley Function Calling Leaderboard-style pilot for candidate Hermes agent models after the local strict tool-call held-out suite is stable enough to justify broader comparison.

## Gate

- Candidate must have a working OpenAI-compatible endpoint.
- Candidate must have a local strict tool-call report under `reports/benchmark/endpoint-tool-call/`.
- Output root must be on `/Volumes/PortableSSD`.
- Full BFCL runs remain deferred until the pilot schema is reviewed.

## Command

```bash
source scripts/env.sh
RUN_ID=<model>-bfcl-pilot-<date>
MODEL_ID=<bfcl_registered_model_name>
BASE_URL=http://127.0.0.1:<port>/v1
OUT=/Volumes/PortableSSD/hermes-evals/standard-benchmarks/bfcl/${RUN_ID}
mkdir -p "$OUT"

LOCAL_SERVER_ENDPOINT="$BASE_URL" \
LOCAL_SERVER_PORT="<port>" \
/Volumes/PortableSSD/hermes-training-envs/bfcl-py312/bin/bfcl generate \
  --model "$MODEL_ID" \
  --test-category simple_python,multiple,parallel \
  --temperature 0 \
  --skip-server-setup \
  --result-dir "$OUT/results" \
  --include-input-log

/Volumes/PortableSSD/hermes-training-envs/bfcl-py312/bin/bfcl evaluate \
  --model "$MODEL_ID" \
  --test-category simple_python,multiple,parallel \
  --result-dir "$OUT/results" \
  --score-dir "$OUT/scores" \
  --partial-eval
```

The installed BFCL package exposes a `bfcl` CLI with `generate` and `evaluate`
subcommands. Keep the endpoint variables in the run card because `--skip-server-setup`
uses `LOCAL_SERVER_ENDPOINT` and `LOCAL_SERVER_PORT` rather than a `--base-url`
flag.

## Result Card Schema

```json
{
  "run_id": "<model>-bfcl-pilot-<date>",
  "suite": "bfcl-pilot",
  "model": "<runtime_model_id>",
  "base_url": "http://127.0.0.1:<port>/v1",
  "categories": ["simple_python", "multiple", "parallel"],
  "temperature": 0,
  "raw_output": "/Volumes/PortableSSD/hermes-evals/standard-benchmarks/bfcl/<run-id>/results",
  "normalized_summary": "/Volumes/PortableSSD/hermes-evals/standard-benchmarks/bfcl/<run-id>/scores",
  "accuracy": null,
  "invalid_json_rate": null,
  "schema_error_rate": null,
  "publish_decision": "pilot-only"
}
```

## Publication Boundary

Pilot results are engineering evidence only. Public claims require full BFCL execution, raw outputs, normalized summaries, and reviewer sign-off.

## Current Local Pilot Evidence

Because `bfcl_eval` is not installed in the active environment, the repo-native endpoint pilot was run first:

- Script: `scripts/run_endpoint_pilot_benchmark.py`
- Suite: `benchmarks/endpoint_pilots/bfcl_pilot.json`
- Report: `reports/benchmark/endpoint-pilots/qwen3-q4km-llamacpp-pilots-20260524.md`
- Raw output: `/Volumes/PortableSSD/hermes-evals/standard-benchmarks/endpoint-pilots/qwen3-q4km-llamacpp-bfcl-pilot-nothink-20260524`
- Result: `0.333`
