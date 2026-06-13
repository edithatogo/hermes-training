# Qwen3 V4 PEFT Colab lm-eval Selected Pilot

Run ID: `qwen3-v4-peft-lm-eval-selected-limit5-20260613`

## Summary

Status: `scored`

The converted Qwen3 v4 PEFT candidate was evaluated through
`lm_eval[hf]` on a Google Colab T4 session with the selected task set at
`--limit 5`. This is a bounded route pilot only. It is not a full no-limit
candidate scorecard and must not be used as a leaderboard-style benchmark
claim.

## Runtime

| Field | Value |
| --- | --- |
| Backend | Google Colab CLI |
| Accelerator | `Tesla T4` |
| Python | `3.12.13` |
| Torch | `2.11.0+cu128` |
| Base model | `Qwen/Qwen3-4B` |
| Adapter | `/content/qwen3-v4-peft-conversion-20260613` |
| Adapter source | `/Volumes/PortableSSD/hermes-evals/adapters/qwen3-v4-peft-conversion-20260613` |
| Harness | `lm_eval[hf]` |
| Transformers pin | `transformers>=4.56,<5` |
| Quantization | `load_in_4bit=True`, `bnb_4bit_compute_dtype=float16` |
| Batch size | `1` |
| Limit | `5` |
| Evaluation duration | `406.180s` |

## Scores

| Task | Metric | Value | Stderr | Samples |
| --- | --- | ---: | ---: | ---: |
| `arc_challenge` | `acc` | 0.0000 | 0.0000 | 5 |
| `arc_challenge` | `acc_norm` | 0.2000 | 0.2000 | 5 |
| `hellaswag` | `acc` | 0.4000 | 0.2449 | 5 |
| `hellaswag` | `acc_norm` | 0.6000 | 0.2449 | 5 |
| `truthfulqa_mc2` | `acc` | 0.5166 | 0.2090 | 5 |
| `gsm8k` | `exact_match,strict-match` | 0.8000 | 0.2000 | 5 |
| `gsm8k` | `exact_match,flexible-extract` | 0.8000 | 0.2000 | 5 |
| `winogrande` | `acc` | 0.4000 | 0.2449 | 5 |

## Evidence

- Script: `scripts/colab_peft_lm_eval_selected.py`
- Run JSON: `/Volumes/PortableSSD/hermes-evals/colab/qwen3-v4-peft-lm-eval-selected-limit5-20260613/qwen3-v4-peft-lm-eval-selected-limit5.json`
- Harness result: `/Volumes/PortableSSD/hermes-evals/colab/qwen3-v4-peft-lm-eval-selected-limit5-20260613/lm-eval-results/results_2026-06-13T02-49-14.059270.json`
- Colab log: `/Volumes/PortableSSD/hermes-evals/colab/qwen3-v4-peft-lm-eval-selected-limit5-20260613/colab-exec-nodeps-pin4bit.log`
- Cleanup: `colab sessions` reported no active sessions after the run.

## Reconciliation Notes

Two blockers were preserved from earlier attempts:

- `qwen3-v4-peft-lm-eval-selected-limit5-quant-blocked.json`: unpinned
  Transformers 5.x rejected `load_in_4bit` as passed by `lm_eval`.
- `qwen3-v4-peft-lm-eval-selected-limit5-pin4bit-torchvision-blocked.json`:
  `accelerate --ignore-installed` replaced Colab's Torch build and broke
  torchvision import registration.

The working path is to preserve Colab's Torch/CUDA stack, install `accelerate`
with `--no-deps`, pin Transformers below 5, and use the harness HF adapter with
4-bit loading.

## Next Step

Promote this route to a full selected-task scorecard track with no `--limit`.
The expected bottleneck is wall-clock time for full task generation and
loglikelihood batches, not route compatibility.
