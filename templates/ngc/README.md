# NGC Scorecard Container Templates

These templates prepare the Qwen3 v4 PEFT selected-task `lm_eval[hf]`
scorecard for NVIDIA NGC Cloud Function tasks. They are build recipes only; do
not push or run them until NGC auth, org/team, registry access, GPU quota, and
result persistence are verified.

## Qwen3 v4 PEFT Scorecard

Build from the repository root so the runner copy path resolves:

```bash
docker build -f templates/ngc/qwen3-v4-peft-scorecard.Containerfile \
  -t <ngc-registry-image> .
```

After NGC registry auth and quota are proven, use the guarded submitter:

```bash
./.venv/bin/python scripts/submit_ngc_cloud_function_scorecard.py \
  --container-image <ngc-registry-image> \
  --gpu-specification <gpu-spec> \
  --execute \
  --confirm-ngc-run
```

The container expects public adapter access through `PEFT_ADAPTER_REPO`, and can
upload recovered artifacts to a Hugging Face dataset only when `HF_TOKEN` and
`HF_RESULTS_REPO` are supplied by the execution environment.
