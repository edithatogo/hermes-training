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
MODEL_ID=<runtime_model_id>
BASE_URL=http://127.0.0.1:<port>/v1
OUT=/Volumes/PortableSSD/hermes-evals/standard-benchmarks/bfcl/${RUN_ID}
mkdir -p "$OUT"

python -m bfcl_eval \
  --model "$MODEL_ID" \
  --base-url "$BASE_URL" \
  --category simple,multiple,parallel \
  --limit 25 \
  --temperature 0 \
  --output "$OUT/results.jsonl"
```

If the installed BFCL package exposes a different CLI name, record the resolved command in the run card before execution.

## Result Card Schema

```json
{
  "run_id": "<model>-bfcl-pilot-<date>",
  "suite": "bfcl-pilot",
  "model": "<runtime_model_id>",
  "base_url": "http://127.0.0.1:<port>/v1",
  "categories": ["simple", "multiple", "parallel"],
  "limit": 25,
  "temperature": 0,
  "raw_output": "/Volumes/PortableSSD/hermes-evals/standard-benchmarks/bfcl/<run-id>/results.jsonl",
  "normalized_summary": "/Volumes/PortableSSD/hermes-evals/standard-benchmarks/bfcl/<run-id>/summary.json",
  "accuracy": null,
  "invalid_json_rate": null,
  "schema_error_rate": null,
  "publish_decision": "pilot-only"
}
```

## Publication Boundary

Pilot results are engineering evidence only. Public claims require full BFCL execution, raw outputs, normalized summaries, and reviewer sign-off.
