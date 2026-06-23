# Qwen3 v4 RULER Long-Context Runtime Attempt

Attempt ID: `qwen3-v4-peft-ruler-ctx4096-limit1-smoke-20260624`
Status: `blocked-runtime-fetch`
Suite: `ruler-long-context`
Run ID: `qwen3-v4-peft-ruler-long-context-20260616`
Candidate: `qwen3-4b-strict-toolcall-v4-targeted`

This is a runtime-attempt blocker only. It is not a RULER score and must not be used as benchmark evidence.

## Command

```bash
/Volumes/PortableSSD/hermes-training-envs/benchmarks-py312/bin/lm_eval run --model hf --model_args pretrained=Qwen/Qwen3-4B,peft=edithatogo/qwen3-4b-hermes-lora-peft-converted,trust_remote_code=True,dtype=float16,max_length=4096 --device mps --tasks niah_single_1 --limit 1 --batch_size 1 --metadata '{"max_seq_lengths":[4096]}' --output_path /Volumes/PortableSSD/hermes-evals/standard-benchmarks/ruler/qwen3-v4-peft-ruler-long-context-20260616/ctx4096-limit1-smoke-20260624
```

## Result

- Return code: `-15`
- Duration: `566.667 s`
- Timed out: `false`
- Output path: `/Volumes/PortableSSD/hermes-evals/standard-benchmarks/ruler/qwen3-v4-peft-ruler-long-context-20260616/ctx4096-limit1-smoke-20260624`

The local `lm_eval` RULER path reached model initialization on MPS but did not reach inference. The active shell is not authenticated with Hugging Face, the `Qwen/Qwen3-4B` cache is incomplete, and the PEFT-converted adapter repo is not present in the active HF cache.

The attempted download also used the internal Hugging Face cache path:

`/Users/doughnut/.cache/huggingface/hub/models--Qwen--Qwen3-4B`

That violates the project requirement to keep major model/cache files on `/Volumes/PortableSSD`.

## Next Action

Set the Hugging Face cache variables to SSD-backed paths, authenticate or provide `HF_TOKEN` for the PEFT-converted adapter, prefetch `Qwen/Qwen3-4B` and the adapter, then rerun the same smoke before launching the full ctx4096 RULER slice.

```bash
export HF_HOME=/Volumes/PortableSSD/huggingface
export HUGGINGFACE_HUB_CACHE=/Volumes/PortableSSD/huggingface/hub
export HF_XET_CACHE=/Volumes/PortableSSD/huggingface/xet
export TRANSFORMERS_CACHE=/Volumes/PortableSSD/huggingface/transformers
```
