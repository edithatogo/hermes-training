# Qwen3 V4 PEFT Kaggle Notebook Contract

Status: `pass`
Staging dir: `/Volumes/PortableSSD/GitHub/hermes-training/reports/cloud/kaggle-qwen3-v4-peft-scorecard-20260613`
Dry-run report: `/Volumes/PortableSSD/GitHub/hermes-training/reports/cloud/qwen3-v4-peft-kaggle-submit-dry-run-20260613.json`
Preflight report: `/Volumes/PortableSSD/GitHub/hermes-training/reports/cloud/backend-preflight-20260613.json`

## Dataset And Execution Contract

- Private data upload: `False`
- Public inputs: `edithatogo/qwen3-4b-hermes-lora-peft-converted`, `Qwen/Qwen3-4B`, lm-eval selected public benchmark tasks
- Internet is required for public dependency/model downloads inside Kaggle.
- No Kaggle kernel push without `--execute --confirm-kaggle-run` and explicit operator approval.
- P100 compatibility policy: `p100-cu118`; 4-bit/bitsandbytes is disabled for this path.

## Checks

| Check | Result | Detail |
|---|---|---|
| `metadata_kernel_id` | `pass` | edithatogo/qwen3-v4-peft-lm-eval-selected-full |
| `metadata_script_kernel` | `pass` | script |
| `metadata_python` | `pass` | python |
| `metadata_gpu_enabled` | `pass` | True |
| `metadata_internet_enabled` | `pass` | True |
| `metadata_public_kernel` | `pass` | False |
| `metadata_license` | `pass` | apache-2.0 |
| `config_adapter_public_repo` | `pass` | edithatogo/qwen3-4b-hermes-lora-peft-converted |
| `config_no_limit` | `pass` | None |
| `config_selected_tasks` | `pass` | arc_challenge,hellaswag,truthfulqa_mc2,gsm8k,winogrande |
| `config_timeout_bounded` | `pass` | 21600 |
| `config_p100_torch_policy` | `pass` | p100-cu118 |
| `config_disables_4bit_for_p100` | `pass` | False |
| `dry_run_status` | `pass` | dry-run |
| `dry_run_no_execute` | `pass` | False |
| `dry_run_no_confirmation` | `pass` | False |
| `dry_run_no_blockers` | `pass` | [] |
| `preflight_kaggle_prepared` | `pass` | prepared-needs-notebook-contract |
| `preflight_quota_visible` | `pass` | 0 |
| `runner_downloads_public_adapter` | `pass` | adapter repo is configurable and defaults to the public PEFT repo |
| `runner_writes_kaggle_working_artifacts` | `pass` | runner writes summary and lm-eval outputs under Kaggle working directory |
| `runner_records_claim_boundary` | `pass` | claim boundary is embedded in runner output |
| `runner_installs_p100_compatible_torch` | `pass` | runner has a configurable P100-compatible PyTorch install policy |
