# Qwen3 v4 RULER ctx8192 Runtime Blocker - 2026-06-24

Candidate: `qwen3-4b-strict-toolcall-v4-targeted`

Suite: `ruler-long-context`

Task: `niah_single_1`

Context: `8192`

Limit: `20`

Status: `blocked-runtime-generation-stall`

## Result

No ctx8192 score was produced.

The local MPS runtime successfully:

- loaded `Qwen/Qwen3-4B` with PEFT adapter
  `edithatogo/qwen3-4b-hermes-lora-peft-converted`
- generated 500 synthetic ctx8192 RULER samples
- built the 20 limited evaluation contexts
- entered `generate_until`

Generation stayed at `0/20` until manual termination after approximately
524 seconds. This is a runtime-duration blocker, not a failed score.

## Evidence

- Output root: `/Volumes/PortableSSD/hermes-evals/standard-benchmarks/ruler/qwen3-v4-peft-ruler-long-context-20260616/ctx8192-limit20-20260624`
- Stdout log: `/Volumes/PortableSSD/hermes-evals/standard-benchmarks/ruler/qwen3-v4-peft-ruler-long-context-20260616/ctx8192-limit20-20260624/stdout.log`
- Stderr log: `/Volumes/PortableSSD/hermes-evals/standard-benchmarks/ruler/qwen3-v4-peft-ruler-long-context-20260616/ctx8192-limit20-20260624/stderr.log`

Command:

```bash
HF_HOME=/Volumes/PortableSSD/huggingface HUGGINGFACE_HUB_CACHE=/Volumes/PortableSSD/huggingface/hub HF_XET_CACHE=/Volumes/PortableSSD/huggingface/xet TRANSFORMERS_CACHE=/Volumes/PortableSSD/huggingface/transformers HF_HUB_ENABLE_HF_TRANSFER=0 /Volumes/PortableSSD/hermes-training-envs/benchmarks-py312/bin/lm_eval run --model hf --model_args pretrained=Qwen/Qwen3-4B,peft=edithatogo/qwen3-4b-hermes-lora-peft-converted,trust_remote_code=True,dtype=float16,max_length=8192 --device mps --tasks niah_single_1 --batch_size 1 --limit 20 --metadata '{"max_seq_lengths":[8192]}' --output_path /Volumes/PortableSSD/hermes-evals/standard-benchmarks/ruler/qwen3-v4-peft-ruler-long-context-20260616/ctx8192-limit20-20260624
```

## Claim Boundary

This is a runtime-blocker artifact, not a RULER score.

The only scored long-context evidence remains:

- ctx4096 `niah_single_1 = 1.000` over 500 samples

Do not claim broader long-context capability until ctx8192+ scored artifacts
exist.

## Next Action

Do not run a full ctx8192 MPS slice in the current local path. Try one of:

- a lower-overhead runtime
- smaller `max_gen_toks`
- cloud/offloaded evaluation
- a model/runtime with better 8k attention performance

Then rerun ctx8192 before attempting ctx16384.
