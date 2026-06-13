# Track mungert-nanbeige41-3b-gguf-strict-suffix-completion_20260614 Context

- [Specification](./spec.md)
- [Implementation Plan](./plan.md)
- [Metadata](./metadata.json)
- [Hub Requirements](../../requirements.md)
- [Hub Design](../../design.md)
- [Hub Contracts](../../contracts.md)

## Summary

The queued `strict-suffix-copy-exact` endpoint repair for
`Mungert/Nanbeige4.1-3B-GGUF` was run against the SSD-backed Q4_K_M GGUF
through `llama-server` on Metal. It scored `1/3` on the strict BFCL pilot and
is not promotable.

## Evidence

- Report: `reports/benchmark/endpoint-pilots/mungert-nanbeige41-3b-gguf-strict-suffix-copy-exact-repair-20260614.md`
- Source summary: `/Volumes/PortableSSD/hermes-evals/standard-benchmarks/endpoint-pilots/mungert-nanbeige4-1-3b-gguf-strict-suffix-copy-exact-20260614-025949/summary.json`
