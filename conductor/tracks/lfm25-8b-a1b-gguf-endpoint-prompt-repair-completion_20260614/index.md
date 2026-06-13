# Track lfm25-8b-a1b-gguf-endpoint-prompt-repair-completion_20260614 Context

- [Specification](./spec.md)
- [Implementation Plan](./plan.md)
- [Metadata](./metadata.json)
- [Hub Requirements](../../requirements.md)
- [Hub Design](../../design.md)
- [Hub Contracts](../../contracts.md)

## Summary

The queued `strict-suffix-copy-exact` endpoint repair for
`LiquidAI/LFM2.5-8B-A1B-GGUF` was run against the SSD-backed Q4_K_M GGUF
through `llama-server` on Metal. It scored `0/3` on the strict BFCL pilot and is
not promotable.

## Evidence

- Report: `reports/benchmark/endpoint-pilots/lfm25-8b-a1b-gguf-strict-suffix-copy-exact-repair-20260614.md`
- Source summary: `/Volumes/PortableSSD/hermes-evals/standard-benchmarks/endpoint-pilots/liquidai-lfm2-5-8b-a1b-gguf-strict-suffix-copy-exact-20260614-024103/summary.json`
