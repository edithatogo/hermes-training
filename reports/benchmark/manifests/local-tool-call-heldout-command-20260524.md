# Local Tool-Call Held-Out Command Manifest

Date: 2026-05-24

## Purpose

Run the strict Hermes local held-out gate for any agent-positioned candidate.

## Command

```bash
source scripts/env.sh
./.venv/bin/python scripts/run_tool_call_benchmark.py \
  --model <model_id_or_path> \
  --adapter <optional_adapter_path> \
  --suite benchmarks/tool_call_local/heldout_suite.json \
  --user-prefix /no_think \
  --run-id <model>-heldout-<date>
```

## Artifact Root

```text
$HERMES_EVAL_ROOT/tool-call-benchmark/<run-id>
```

## Publication Gate

Adapter/model publication as a Hermes agent requires strict pass rate `1.000`. Runtime-normalized diagnostic scores may be reported as integration notes only.
