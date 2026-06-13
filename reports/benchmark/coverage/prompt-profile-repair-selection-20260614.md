# Prompt/Profile Repair Selection

- Status: `dry-run`
- Candidate: `ManiacLabs/Qwen3.6-35B-A3B-2bit`
- Variant: `strict-suffix-copy-exact`
- Runner: `endpoint`
- Raw-output promotion allowed: `True`
- Goal: tighten raw Hermes tool-call formatting and exact argument copying
- Boundary: A selected repair run is not promotion evidence until raw strict outputs and downstream held-out, pilot, official benchmark, latency, and rollback gates pass.

## Command

```bash
source scripts/env.sh
RUN_STAMP=$(date +%Y%m%d-%H%M%S)
# No download here: run only against the existing SSD-backed artifact or local endpoint.
./.venv/bin/python scripts/run_endpoint_pilot_benchmark.py --model maniaclabs-qwen3-6-35b-a3b-2bit --base-url 'http://127.0.0.1:<port>/v1' --suite benchmarks/endpoint_pilots/bfcl_pilot.json --max-tokens 512 --require-no-extra-tool-text --run-id maniaclabs-qwen3-6-35b-a3b-2bit-strict-suffix-copy-exact-${RUN_STAMP} --system-suffix ' Return only valid Hermes <tool_call> blocks when a listed tool satisfies the request. If no listed tool can satisfy the request, reply exactly: I cannot perform the action because the requested tool is not available. Copy argument values exactly from the user request; do not expand, summarize, or paraphrase string arguments.'
```
