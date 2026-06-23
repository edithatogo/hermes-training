# Qwen3 v4 RULER ctx4096 Limit-1 Smoke

Status: `passed-limit1-smoke`
Task: `niah_single_1`
Context length: `4096`
Limit: `1`
Device: `mps`
Base model: `Qwen/Qwen3-4B`
Adapter: `edithatogo/qwen3-4b-hermes-lora-peft-converted`

This is a RULER launch smoke with `--limit 1`. It proves the ctx4096 path can
load and score one `niah_single_1` example on MPS, but it is not a full official
RULER benchmark result.

## Result

| Task | Metric | Value | Stderr |
|---|---:|---:|---:|
| `niah_single_1` | `4096` | `1.0` | `N/A` |

Total evaluation time: `111.41076754103415` seconds.

## Artifacts

- Output root: `/Volumes/PortableSSD/hermes-evals/standard-benchmarks/ruler/qwen3-v4-peft-ruler-long-context-20260616/ctx4096-limit1-smoke-20260624-envpinned`
- Raw result JSON: `/Volumes/PortableSSD/hermes-evals/standard-benchmarks/ruler/qwen3-v4-peft-ruler-long-context-20260616/ctx4096-limit1-smoke-20260624-envpinned/edithatogo__qwen3-4b-hermes-lora-peft-converted/results_2026-06-24T03-44-26.349752.json`
- Model SHA: `1cfa9a7208912126459214e8b04321603b3df60c`
- PEFT SHA: `97c969fdcc92e7b25eb79f57e12d87a5da1761ee`

## Runtime Notes

- The initial direct run reached model download but hit repeated Hugging Face
  read timeouts before evaluation.
- `Qwen/Qwen3-4B` was then pre-downloaded into the PortableSSD HF cache with
  `HF_HUB_DOWNLOAD_TIMEOUT=300` and a single-worker `snapshot_download`.
- RULER task construction initially failed because `wonderwords` was missing.
  `wonderwords` was installed into
  `/Volumes/PortableSSD/hermes-training-envs/benchmarks-py312`; `nltk` was
  already present.

## Command

```bash
source scripts/env.sh && HF_HUB_DOWNLOAD_TIMEOUT=300 HF_HUB_ETAG_TIMEOUT=60 /Volumes/PortableSSD/hermes-training-envs/benchmarks-py312/bin/lm_eval run --model hf --model_args pretrained=Qwen/Qwen3-4B,peft=edithatogo/qwen3-4b-hermes-lora-peft-converted,trust_remote_code=True,dtype=float16,max_length=4096 --device mps --tasks niah_single_1 --limit 1 --batch_size 1 --metadata '{"max_seq_lengths":[4096],"smoke_limit":1,"rerun":"env-pinned-after-ruler-extras"}' --output_path /Volumes/PortableSSD/hermes-evals/standard-benchmarks/ruler/qwen3-v4-peft-ruler-long-context-20260616/ctx4096-limit1-smoke-20260624-envpinned
```
