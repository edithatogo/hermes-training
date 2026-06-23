# Qwen3 v4 BFCL Endpoint Smoke HF Artifact

HF dataset repo: `edithatogo/hermes-training-artifacts`
Visibility target: `private`
Status: `blocked-auth`
Path prefix target: `qwen3-v4-bfcl-endpoint-smoke-20260624/`

The raw BFCL smoke evidence was staged locally at
`/tmp/qwen3-v4-bfcl-endpoint-smoke-20260624`, but the upload could not be
completed because the active shell is not authenticated with Hugging Face.

## Upload Attempt

```bash
hf upload edithatogo/hermes-training-artifacts \
  /tmp/qwen3-v4-bfcl-endpoint-smoke-20260624 \
  qwen3-v4-bfcl-endpoint-smoke-20260624 \
  --repo-type dataset \
  --private \
  --commit-message 'Add Qwen3 v4 BFCL endpoint smoke evidence' \
  --json
```

Result: `401 Unauthorized`.

`hf auth whoami` returned `Not logged in`, and no `HF_TOKEN`,
`HUGGINGFACE_HUB_TOKEN`, or `HUGGING_FACE_HUB_TOKEN` environment variable was
present.

## Staged Files

- `report.json`
- `report.md`
- `test_case_ids_to_generate.json`
- `logs/generate.log`
- `logs/evaluate.log`
- `proxy_probe_headers.txt`
- `proxy_probe_body.json`
- `results/Qwen_Qwen3-4B-Instruct-2507-FC/non_live/*.json`
- `scores/Qwen_Qwen3-4B-Instruct-2507-FC/non_live/*.json`
- `scores/data_*.csv`

This is evidence-only material. It records a three-case partial BFCL smoke and
must not be described as a full official BFCL score.
