# Endpoint Pilot Suites

These suites are lightweight local pilots for endpoint readiness. They are not replacements for full BFCL, IFEval, coding, or lm-evaluation-harness runs.

Use them when external benchmark packages are not installed or when a model needs a quick, SSD-backed sanity check before spending time or cloud budget.

Outputs must be written under `/Volumes/PortableSSD/hermes-evals/standard-benchmarks/endpoint-pilots/` for endpoints or `/Volumes/PortableSSD/hermes-evals/standard-benchmarks/local-pilots/` for local MLX runs.

Local MLX adapter example:

```bash
source scripts/env.sh
PYTHONPATH=scripts ./.venv/bin/python scripts/run_local_pilot_benchmark.py \
  --suite benchmarks/endpoint_pilots/bfcl_pilot.json \
  --model Qwen/Qwen3-4B-MLX-4bit \
  --adapter gemma4/experiments/qwen3-4b-strict-toolcall-v4-targeted/lora_adapter \
  --user-prefix /no_think \
  --assistant-prefill $'<think>\n\n</think>\n\n'
```
