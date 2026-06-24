# Qwen3 v4 RULER ctx8192 Runtime Blocker HF Artifact

- Dataset: `edithatogo/hermes-training-artifacts`
- Path: `qwen3-v4-ruler-ctx8192-runtime-blocker-20260624`
- Revision: `641d7f3641ef688371a34c3754ece854a5de84e1`
- URL: <https://huggingface.co/datasets/edithatogo/hermes-training-artifacts/tree/641d7f3641ef688371a34c3754ece854a5de84e1/qwen3-v4-ruler-ctx8192-runtime-blocker-20260624>

This is an evidence-only private artifact. It records a ctx8192 local MPS
runtime blocker and must not be described as a RULER score.

## Gate Summary

| Slice | Task | Samples | Score | Status | Claim scope |
| --- | --- | ---: | ---: | --- | --- |
| ctx4096 | `niah_single_1` | 500 | 1.000 | scored | ctx4096 needle retrieval only |
| ctx8192 | `niah_single_1` | limit 20 attempted | N/A | blocked at generation `0/20` | no long-context claim |

The ctx8192 attempt loaded the model and built contexts but did not complete the
first generation before termination after approximately 524 seconds.
