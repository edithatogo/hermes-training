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
- The runner embeds `LM_EVAL_USE_4BIT=0` as its default because Kaggle did not expose the JSON sidecar beside the executed script in the live rerun.
- The dependency install omits `--upgrade` while the P100 torch policy is active, so `lm_eval[hf]` cannot overwrite `torch==2.2.2+cu118` with a newer unsupported CUDA build.
- The runner pins `numpy<2` because the P100-compatible Torch 2.2 wheel is not compatible with Kaggle's NumPy 2 default.
- The runner pins `transformers==4.57.6` and `tokenizers==0.22.2`; wheel inspection confirmed Qwen3 class availability while keeping Torch 2.2 compatibility.
- The runner disables TensorFlow/Flax discovery and records a direct Qwen3 import probe before invoking lm-eval.
- The runner uninstalls Kaggle's preinstalled `torchao` on the non-4-bit P100 path because that package expects newer Torch internals than `torch==2.2.2+cu118` exposes.

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
| `runner_defaults_no_4bit_without_sidecar_config` | `pass` | Kaggle may not expose the JSON sidecar next to the script; embedded default must be P100-safe |
| `runner_keeps_p100_torch_after_dependency_install` | `pass` | dependency install only upgrades when no P100 torch policy is active |
| `runner_pins_numpy_for_p100_torch` | `pass` | torch==2.2.2+cu118 is not compatible with Kaggle's NumPy 2 default |
| `runner_pins_qwen3_transformers` | `pass` | wheel inspection confirmed transformers 4.57.6 exposes Qwen3ForCausalLM while supporting torch>=2.2 |
| `runner_applies_p100_torch_policy_last` | `pass` | P100 torch policy must be applied after the general dependency install |
| `runner_records_qwen3_import_probe` | `pass` | runner must expose direct Qwen3 import diagnostics before lm-eval |
| `runner_disables_tf_flax_for_transformers` | `pass` | runner disables TensorFlow/Flax discovery before importing transformers |
| `runner_removes_incompatible_torchao` | `pass` | runner removes preinstalled torchao because Kaggle's version requires newer torch APIs than torch 2.2.2 |
