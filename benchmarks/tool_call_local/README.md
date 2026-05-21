# Local Tool-Call Benchmark

This directory holds the small deterministic Hermes-local tool-call benchmark suite.

## Scope

The suite is designed to exercise four local regression categories:

1. JSON validity
2. Argument correctness
3. Invalid-tool handling
4. Multi-turn repair

Two benchmark files are checked in:

- [`suite.json`](./suite.json): mirrored by the tiny strict training seed; use for regression and shape-repair experiments only.
- [`heldout_suite.json`](./heldout_suite.json): publication gate suite; these examples intentionally do not overlap the benchmark-mirrored training seed.

The runner is [`scripts/run_tool_call_benchmark.py`](../../scripts/run_tool_call_benchmark.py).

## Running

```bash
source scripts/env.sh
./.venv/bin/python scripts/run_tool_call_benchmark.py \
  --model <model_id_or_path> \
  --adapter <optional_adapter_path> \
  --suite benchmarks/tool_call_local/suite.json \
  --user-prefix /no_think
```

For publication gating, run the held-out suite instead:

```bash
source scripts/env.sh
./.venv/bin/python scripts/run_tool_call_benchmark.py \
  --model <model_id_or_path> \
  --adapter <optional_adapter_path> \
  --suite benchmarks/tool_call_local/heldout_suite.json \
  --user-prefix /no_think
```

Validate either suite without loading a model:

```bash
./.venv/bin/python scripts/run_tool_call_benchmark.py \
  --suite benchmarks/tool_call_local/heldout_suite.json \
  --dry-run
```

The runner writes all real outputs under `$HERMES_EVAL_ROOT/tool-call-benchmark/<run-id>` unless `--output-dir` is set explicitly. Keep benchmark artifacts on the SSD-backed eval root and out of Git.

## Outputs

- `responses.jsonl` for generation runs
- `results.jsonl` for scored rows
- `summary.json` for machine-readable metrics
- `summary.md` for a short human-readable report

## Notes

- Both suites are intentionally small and deterministic.
- `suite.json` overlaps the strict training seed and must not be cited as held-out evidence.
- `heldout_suite.json` is the strict local publication gate and must pass at `1.000` before a model card or publish-readiness checklist is marked ready.
- Tool-call outputs are scored against the exact JSON tool-call schema in each case.
- The invalid-tool case should return plain text and avoid hallucinating a tool call.
- The repair case includes a prior malformed assistant turn so the next assistant turn must repair the call.
