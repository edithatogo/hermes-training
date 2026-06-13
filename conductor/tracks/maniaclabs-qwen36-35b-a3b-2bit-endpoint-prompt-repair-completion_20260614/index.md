# Track maniaclabs-qwen36-35b-a3b-2bit-endpoint-prompt-repair-completion_20260614 Context

- [Specification](./spec.md)
- [Implementation Plan](./plan.md)
- [Metadata](./metadata.json)
- [Hub Requirements](../../requirements.md)
- [Hub Design](../../design.md)
- [Hub Contracts](../../contracts.md)

## Summary

The queued `strict-suffix-copy-exact` endpoint repair for
`ManiacLabs/Qwen3.6-35B-A3B-2bit` was run against the SSD-backed 2-bit GGUF
through `llama-server` on Metal. It scored `1/3` on the strict BFCL pilot and
is not promotable.

## Evidence

- Report: `reports/benchmark/endpoint-pilots/maniaclabs-qwen36-35b-a3b-2bit-strict-suffix-copy-exact-repair-20260614.md`
- Source summary: `/Volumes/PortableSSD/hermes-evals/standard-benchmarks/endpoint-pilots/maniaclabs-qwen3-6-35b-a3b-2bit-strict-suffix-copy-exact-20260614-024948/summary.json`
