# Qwen3 V4 PEFT Modal Scorecard Contract

Status: `pass`
Staging dir: `/Volumes/PortableSSD/GitHub/hermes-training/reports/cloud/modal-qwen3-v4-peft-scorecard-20260614`
Dry-run report: `/Volumes/PortableSSD/GitHub/hermes-training/reports/cloud/qwen3-v4-peft-modal-submit-dry-run-20260614.json`
App: `/Volumes/PortableSSD/GitHub/hermes-training/scripts/modal_peft_lm_eval_selected.py`

## Execution Contract

- Dry-run only: `execute=false`
- Remote execution requires `--execute --confirm-modal-run --confirm-zero-cost-compute`.
- Cost or zero-cost policy evidence is required before execution.
- Post-run result ingest validation is required before benchmark claims.

## Checks

| Check | Result | Detail |
|---|---|---|
| `dry_run_status` | `pass` | dry-run |
| `dry_run_no_execute` | `pass` | False |
| `dry_run_no_confirmation` | `pass` | False |
| `dry_run_no_zero_cost_confirmation` | `pass` | False |
| `dry_run_no_blockers` | `pass` | [] |
| `command_uses_modal_run` | `pass` | modal run --name qwen3-v4-peft-modal-lm-eval-selected-full-20260614 --write-result /Volumes/PortableSSD/GitHub/hermes-training/reports/cloud/modal-qwen3-v4-peft-scorecard-20260614/modal-result.json /Volumes/PortableSSD/GitHub/hermes-trainin |
| `command_targets_scorecard` | `pass` | modal run --name qwen3-v4-peft-modal-lm-eval-selected-full-20260614 --write-result /Volumes/PortableSSD/GitHub/hermes-training/reports/cloud/modal-qwen3-v4-peft-scorecard-20260614/modal-result.json /Volumes/PortableSSD/GitHub/hermes-trainin |
| `command_writes_local_result` | `pass` | modal run --name qwen3-v4-peft-modal-lm-eval-selected-full-20260614 --write-result /Volumes/PortableSSD/GitHub/hermes-training/reports/cloud/modal-qwen3-v4-peft-scorecard-20260614/modal-result.json /Volumes/PortableSSD/GitHub/hermes-trainin |
| `config_adapter_public_repo` | `pass` | edithatogo/qwen3-4b-hermes-lora-peft-converted |
| `config_base_model` | `pass` | Qwen/Qwen3-4B |
| `config_no_limit` | `pass` | None |
| `config_selected_tasks` | `pass` | arc_challenge,hellaswag,truthfulqa_mc2,gsm8k,winogrande |
| `config_timeout_bounded` | `pass` | 21600 |
| `config_volume_output` | `pass` | /results/qwen3-v4-peft-modal-lm-eval-selected-full-20260614/lm-eval-output |
| `config_volume_summary` | `pass` | /results/qwen3-v4-peft-modal-lm-eval-selected-full-20260614/summary.json |
| `app_declares_t4_gpu` | `pass` | Modal function uses T4 GPU |
| `app_uses_results_volume` | `pass` | Modal volume mounted at /results |
| `app_commits_volume` | `pass` | Modal result volume commit is attempted |
| `app_embeds_claim_boundary` | `pass` | claim boundary is embedded |
