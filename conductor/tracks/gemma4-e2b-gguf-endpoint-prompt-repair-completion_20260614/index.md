# Gemma 4 E2B GGUF Endpoint Prompt Repair Completion

- [Specification](./spec.md)
- [Implementation Plan](./plan.md)
- [Metadata](./metadata.json)
- [Hub Requirements](../../requirements.md)
- [Hub Design](../../design.md)
- [Hub Contracts](../../contracts.md)

## Summary

The queued `strict-suffix-copy-exact` endpoint repair for
`google/gemma-4-E2B-it-qat-q4_0-gguf` was run against the SSD-backed GGUF
through `llama-server` on Metal. It scored `1/3` by passing only the
invalid-tool refusal, so it is not promotable.

## Evidence

- Report: `reports/benchmark/endpoint-pilots/gemma4-e2b-gguf-strict-suffix-copy-exact-repair-20260614.md`
- Source summary: `/Volumes/PortableSSD/hermes-evals/standard-benchmarks/endpoint-pilots/google-gemma-4-e2b-it-qat-q4-0-gguf-strict-suffix-copy-exact-20260614-023301/summary.json`
