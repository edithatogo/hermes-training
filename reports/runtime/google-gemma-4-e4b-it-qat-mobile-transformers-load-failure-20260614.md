# Gemma 4 E4B IT QAT Mobile Transformers Load Failure - 2026-06-14

## Summary

`google/gemma-4-E4B-it-qat-mobile-transformers` was checked as the first item
in the runtime-proof action queue. The goal was a bounded Mac-local
Transformers BFCL pilot using the shared SSD-backed cache and the existing
Hermes benchmark harness.

The proof did not reach generation. The installed Transformers stack does not
recognize the checkpoint architecture `model_type: gemma4`, so the candidate
remains blocked by runtime support rather than benchmark quality.

## Command

```bash
source scripts/env.sh
./.venv/bin/python scripts/run_transformers_pilot_benchmark.py \
  --model google/gemma-4-E4B-it-qat-mobile-transformers \
  --suite benchmarks/endpoint_pilots/bfcl_pilot.json \
  --device auto \
  --dtype float16 \
  --require-no-extra-tool-text \
  --run-id google-gemma-4-e4b-it-qat-mobile-transformers-transformers-bfcl-pilot-20260614
```

## Result

```text
ValueError: The checkpoint you are trying to load has model type `gemma4` but Transformers does not recognize this architecture.
```

The tokenizer loaded, then `AutoModelForCausalLM.from_pretrained` failed during
configuration resolution before weights were loaded or any BFCL cases were
run.

## Decision

- Status: `runtime-support-blocked`
- Do not retry this candidate in the current shared environment.
- Next proof should be a separate Transformers-source or model-specific runtime
  support check, isolated from the stable benchmark environment.
