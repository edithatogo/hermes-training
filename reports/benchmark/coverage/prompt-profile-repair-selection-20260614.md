# Prompt/Profile Repair Selection

- Status: `dry-run`
- Candidate: `Qwen/Qwen3.5-0.8B`
- Variant: `strict-suffix-copy-exact`
- Runner: `local`
- Raw-output promotion allowed: `True`
- Goal: tighten raw Hermes tool-call formatting and exact argument copying
- Boundary: A selected repair run is not promotion evidence until raw strict outputs and downstream held-out, pilot, official benchmark, latency, and rollback gates pass.

## Command

```bash
source scripts/env.sh
RUN_STAMP=$(date +%Y%m%d-%H%M%S)
# No download here: run only against the existing SSD-backed artifact or local endpoint.
./.venv/bin/python scripts/run_local_pilot_benchmark.py --model Qwen/Qwen3.5-0.8B --suite benchmarks/endpoint_pilots/bfcl_pilot.json --max-tokens 512 --require-no-extra-tool-text --run-id qwen-qwen3-5-0-8b-strict-suffix-copy-exact-${RUN_STAMP} --system-suffix ' Return only valid Hermes <tool_call> blocks when a listed tool satisfies the request. If no listed tool can satisfy the request, reply exactly: I cannot perform the action because the requested tool is not available. Copy argument values exactly from the user request; do not expand, summarize, or paraphrase string arguments.'
```
