# Track mkadrlik-hermes-qwen35-4b-sft-v7-strict-suffix-completion_20260614 Context

- [Specification](./spec.md)
- [Implementation Plan](./plan.md)
- [Metadata](./metadata.json)
- [Hub Requirements](../../requirements.md)
- [Hub Design](../../design.md)
- [Hub Contracts](../../contracts.md)

## Summary

The queued `strict-suffix-copy-exact` endpoint repair for
`mkadrlik/Hermes-Qwen3.5-4B-SFT-v7` was run against the SSD-backed Q8_0 GGUF
through `llama-server` on Metal. It scored `1/3` on the strict BFCL pilot and
is not promotable.

## Evidence

- Report: `reports/benchmark/endpoint-pilots/mkadrlik-hermes-qwen35-4b-sft-v7-strict-suffix-copy-exact-repair-20260614.md`
- Source summary: `/Volumes/PortableSSD/hermes-evals/standard-benchmarks/endpoint-pilots/mkadrlik-hermes-qwen3-5-4b-sft-v7-strict-suffix-copy-exact-20260614-030449/summary.json`
