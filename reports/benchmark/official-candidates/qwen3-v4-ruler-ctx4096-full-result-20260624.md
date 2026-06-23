# Qwen3 v4 RULER ctx4096 Full Result

Candidate: `qwen3-4b-strict-toolcall-v4-targeted`
Base model: `Qwen/Qwen3-4B`
Adapter: `edithatogo/qwen3-4b-hermes-lora-peft-converted`
Suite: `ruler-long-context`
Run ID: `qwen3-v4-peft-ruler-long-context-20260616`
Status: `scored-artifact-present`

## Result

| Task | Context | Samples | Score | Stderr |
|---|---:|---:|---:|---|
| `niah_single_1` | 4096 | 500 | 1.000 | N/A |

This is a full `niah_single_1` ctx4096 RULER slice. It supports ctx4096 needle-retrieval evidence only; do not describe it as broader long-context performance without additional RULER tasks and longer context lengths.

## Runtime

- Device: `mps`
- Dtype: `float16`
- Batch size: `1`
- Limit: none
- Total evaluation time: `18898.908290124964` seconds
- Started: `2026-06-24T03:45:20+10:00`
- Finished: `2026-06-24T09:00:26+10:00`
- Model SHA: `1cfa9a7208912126459214e8b04321603b3df60c`
- PEFT SHA: `97c969fdcc92e7b25eb79f57e12d87a5da1761ee`

## Artifacts

- Raw result JSON: `/Volumes/PortableSSD/hermes-evals/standard-benchmarks/ruler/qwen3-v4-peft-ruler-long-context-20260616/ctx4096/edithatogo__qwen3-4b-hermes-lora-peft-converted/results_2026-06-24T09-00-21.623907.json`
- Stdout log: `/Volumes/PortableSSD/hermes-evals/standard-benchmarks/ruler/qwen3-v4-peft-ruler-long-context-20260616/ctx4096/stdout.log`
- Stderr log: `/Volumes/PortableSSD/hermes-evals/standard-benchmarks/ruler/qwen3-v4-peft-ruler-long-context-20260616/ctx4096/stderr.log`

## Command

```bash
HF_HOME=/Volumes/PortableSSD/huggingface HUGGINGFACE_HUB_CACHE=/Volumes/PortableSSD/huggingface/hub HF_XET_CACHE=/Volumes/PortableSSD/huggingface/xet TRANSFORMERS_CACHE=/Volumes/PortableSSD/huggingface/transformers HF_HUB_ENABLE_HF_TRANSFER=0 /Volumes/PortableSSD/hermes-training-envs/benchmarks-py312/bin/lm_eval run --model hf --model_args pretrained=Qwen/Qwen3-4B,peft=edithatogo/qwen3-4b-hermes-lora-peft-converted,trust_remote_code=True,dtype=float16,max_length=4096 --device mps --tasks niah_single_1 --batch_size 1 --metadata '{"max_seq_lengths":[4096]}' --output_path /Volumes/PortableSSD/hermes-evals/standard-benchmarks/ruler/qwen3-v4-peft-ruler-long-context-20260616/ctx4096
```
