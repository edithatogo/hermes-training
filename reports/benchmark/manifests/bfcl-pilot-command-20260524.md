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
MODEL_ID=Qwen/Qwen3-4B-Instruct-2507-FC
BASE_URL=http://127.0.0.1:<port>/v1
OUT=/Volumes/PortableSSD/hermes-evals/standard-benchmarks/bfcl/${RUN_ID}
mkdir -p "$OUT"

REMOTE_OPENAI_BASE_URL="$BASE_URL" \
REMOTE_OPENAI_API_KEY=EMPTY \
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
subcommands. Keep `REMOTE_OPENAI_BASE_URL` and `REMOTE_OPENAI_API_KEY` in the
run card because the generic self-hosted OpenAI-compatible handlers use those
environment variables rather than a `--base-url` flag.

BFCL model-name boundary: local OpenAI-compatible endpoints should use a BFCL
self-hosted model config such as `Qwen/Qwen3-4B-Instruct-2507-FC`. The shorter
`qwen3-4b` / `qwen3-4b-FC` names are wired to hosted Qwen API handlers in the
installed BFCL package and are not equivalent to a local MLX/llama.cpp endpoint.

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

The repo-native endpoint pilot below predates the isolated official BFCL env
and remains separate from it. The official BFCL package is now installed and
smoked in `/Volumes/PortableSSD/hermes-training-envs/bfcl-py312`, but no
official BFCL model execution is recorded yet.

- Script: `scripts/run_endpoint_pilot_benchmark.py`
- Suite: `benchmarks/endpoint_pilots/bfcl_pilot.json`
- Report: `reports/benchmark/endpoint-pilots/qwen3-q4km-llamacpp-pilots-20260524.md`
- Raw output: `/Volumes/PortableSSD/hermes-evals/standard-benchmarks/endpoint-pilots/qwen3-q4km-llamacpp-bfcl-pilot-nothink-20260524`
- Result: `0.333`
