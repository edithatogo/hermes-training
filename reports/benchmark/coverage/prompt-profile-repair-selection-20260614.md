# Prompt/Profile Repair Selection

- Status: `dry-run`
- Candidate: `LiquidAI/LFM2.5-8B-A1B-GGUF`
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
./.venv/bin/python scripts/run_endpoint_pilot_benchmark.py --model liquidai-lfm2-5-8b-a1b-gguf --base-url 'http://127.0.0.1:<port>/v1' --suite benchmarks/endpoint_pilots/bfcl_pilot.json --max-tokens 512 --require-no-extra-tool-text --run-id liquidai-lfm2-5-8b-a1b-gguf-strict-suffix-copy-exact-${RUN_STAMP} --system-suffix ' Return only valid Hermes <tool_call> blocks when a listed tool satisfies the request. If no listed tool can satisfy the request, reply exactly: I cannot perform the action because the requested tool is not available. Copy argument values exactly from the user request; do not expand, summarize, or paraphrase string arguments.'
```
