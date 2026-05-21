# Local Tool-Call Benchmark

This directory holds the small deterministic Hermes-local tool-call benchmark suite.

## Scope

The suite is designed to exercise four local regression categories:

1. JSON validity
2. Argument correctness
3. Invalid-tool handling
4. Multi-turn repair

The benchmark suite is checked in at [`suite.json`](./suite.json). The runner is [`scripts/run_tool_call_benchmark.py`](../../scripts/run_tool_call_benchmark.py).

## Running

```bash
source scripts/env.sh
./.venv/bin/python scripts/run_tool_call_benchmark.py \
  --model <model_id_or_path> \
  --adapter <optional_adapter_path> \
  --suite benchmarks/tool_call_local/suite.json \
  --user-prefix /no_think
```

The runner writes all real outputs under `$HERMES_EVAL_ROOT/tool-call-benchmark/<run-id>` unless `--output-dir` is set explicitly. Keep benchmark artifacts on the SSD-backed eval root and out of Git.

## Outputs

- `responses.jsonl` for generation runs
- `results.jsonl` for scored rows
- `summary.json` for machine-readable metrics
- `summary.md` for a short human-readable report

## Notes

- The suite is intentionally small and deterministic.
- Tool-call outputs are scored against the exact JSON tool-call schema in each case.
- The invalid-tool case should return plain text and avoid hallucinating a tool call.
- The repair case includes a prior malformed assistant turn so the next assistant turn must repair the call.
