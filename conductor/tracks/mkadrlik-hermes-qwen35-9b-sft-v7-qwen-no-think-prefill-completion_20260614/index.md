# Track mkadrlik-hermes-qwen35-9b-sft-v7-qwen-no-think-prefill-completion_20260614 Context

- [Specification](./spec.md)
- [Implementation Plan](./plan.md)
- [Metadata](./metadata.json)
- [Hub Requirements](../../requirements.md)
- [Hub Design](../../design.md)
- [Hub Contracts](../../contracts.md)

## Summary

The queued `qwen-no-think-prefill` endpoint repair for
`mkadrlik/Hermes-Qwen3.5-9B-SFT-v7` was run against the SSD-backed Q4_K_M GGUF
through `llama-server` on Metal. It scored `0/3` on the strict BFCL pilot and
is not promotable.

## Evidence

- Report: `reports/benchmark/endpoint-pilots/mkadrlik-hermes-qwen35-9b-sft-v7-qwen-no-think-prefill-repair-20260614.md`
- Source summary: `/Volumes/PortableSSD/hermes-evals/standard-benchmarks/endpoint-pilots/mkadrlik-hermes-qwen3-5-9b-sft-v7-qwen-no-think-prefill-20260614-031117/summary.json`
