# Track minicpm5-1b-gguf-endpoint-repair-completion_20260614 Context

- [Specification](./spec.md)
- [Implementation Plan](./plan.md)
- [Metadata](./metadata.json)
- [Hub Requirements](../../requirements.md)
- [Hub Design](../../design.md)
- [Hub Contracts](../../contracts.md)

## Summary

The queued `strict-suffix-copy-exact` and `minicpm-empty-tag-repair` endpoint
repairs for `openbmb/MiniCPM5-1B-GGUF` were run against the SSD-backed Q4_K_M
GGUF through `llama-server` on Metal. The strict suffix scored `0/3`; the
MiniCPM empty-tag repair scored `1/3`, passing only the unavailable-tool
refusal. The candidate is not promotable.

## Evidence

- Strict report: `reports/benchmark/endpoint-pilots/minicpm5-1b-gguf-strict-suffix-copy-exact-repair-20260614.md`
- Empty-tag report: `reports/benchmark/endpoint-pilots/minicpm5-1b-gguf-empty-tag-repair-20260614.md`
- Strict source summary: `/Volumes/PortableSSD/hermes-evals/standard-benchmarks/endpoint-pilots/openbmb-minicpm5-1b-gguf-strict-suffix-copy-exact-20260614-032828/summary.json`
- Empty-tag source summary: `/Volumes/PortableSSD/hermes-evals/standard-benchmarks/endpoint-pilots/openbmb-minicpm5-1b-gguf-minicpm-empty-tag-repair-20260614-032828/summary.json`
