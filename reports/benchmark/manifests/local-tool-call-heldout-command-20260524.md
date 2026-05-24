# Local Tool-Call Held-Out Command Manifest

Date: 2026-05-24

## Purpose

Run the strict Hermes local held-out gate for any agent-positioned candidate.

## Command

MLX/local model path:

```bash
source scripts/env.sh
./.venv/bin/python scripts/run_tool_call_benchmark.py \
  --model <model_id_or_path> \
  --adapter <optional_adapter_path> \
  --suite benchmarks/tool_call_local/heldout_suite.json \
  --user-prefix /no_think \
  --run-id <model>-heldout-<date>
```

OpenAI-compatible endpoint path:

```bash
source scripts/env.sh
./.venv/bin/python scripts/run_endpoint_tool_call_benchmark.py \
  --base-url http://127.0.0.1:11434/v1 \
  --model <runtime_model_id> \
  --suite benchmarks/tool_call_local/heldout_suite.json \
  --user-prefix /no_think \
  --run-id <model>-endpoint-heldout-<date>
```

## Artifact Root

```text
$HERMES_EVAL_ROOT/tool-call-benchmark/<run-id>
```

## Publication Gate

Adapter/model publication as a Hermes agent requires strict pass rate `1.000`. Runtime-normalized diagnostic scores may be reported as integration notes only.
