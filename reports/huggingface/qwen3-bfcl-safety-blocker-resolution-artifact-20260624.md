# Qwen3 BFCL + Safety Blocker Resolution HF Artifact

HF dataset repo: `edithatogo/hermes-training-artifacts`
Visibility: `private`
Revision: `11cc7396051091fb9213b872185ef86f166bbeab`
Commit: `https://huggingface.co/datasets/edithatogo/hermes-training-artifacts/commit/11cc7396051091fb9213b872185ef86f166bbeab`
Path prefix: `qwen3-bfcl-safety-blocker-resolution-20260624/`
GitHub source commit: `62af092d2d97b096ede4cfeaa9d416b9f5995453`

This is an evidence-only private artifact. It includes reports, Conductor
track state, checksummed manifests, and small scored outputs. It does not
include adapter weights, and it does not support public BFCL or safety/refusal
claims.

## Gate Outcomes

- BFCL: clean endpoint/proxy path cleared upstream errors, but the rerun hit
  the blank-output gate (`10/10` clean rows blank).
- v9 safety/refusal full140: strict pass `0.875`, JSON validity `1.000`,
  argument accuracy `1.000`, empty-think prefix cases `0`, residual failures
  `1`, refusal-marker echoes `1`, text-mode tool-call rows `0`.

Public v9 weights remain blocked until the pinned suite reaches strict pass
`1.000` with no residual failures or marker echoes, and a separate publication
review approves release.
