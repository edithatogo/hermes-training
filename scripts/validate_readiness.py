#!/usr/bin/env python3
"""Validate that Hermes training tracks are ready to start work.

This is intentionally lightweight: it checks local structure, Python imports,
YAML configs, JSONL split readability, and required scripts. It does not
download models or train.
"""
from __future__ import annotations

import importlib
import json
import os
import subprocess
import sys
from pathlib import Path

import yaml


ROOT = Path(__file__).resolve().parents[1]
STORAGE_ROOT = Path(os.environ.get("HERMES_STORAGE_ROOT", "/Volumes/PortableSSD"))
TRAINING_TRACKS = ("gemma4", "lfm2")
CONDUCTOR_ROOTS = (ROOT, ROOT / "gemma4", ROOT / "lfm2", ROOT / "ollama-pack")
REQUIRED_IMPORTS = (
    "mlx",
    "mlx_lm",
    "huggingface_hub",
    "yaml",
    "requests",
    "safetensors",
    "datasets",
    "transformers",
)


def ok(label: str) -> None:
    print(f"ok: {label}")


def fail(label: str, failures: list[str]) -> None:
    print(f"fail: {label}")
    failures.append(label)


def check_imports(failures: list[str]) -> None:
    for name in REQUIRED_IMPORTS:
        try:
            importlib.import_module(name)
        except Exception as exc:  # noqa: BLE001
            fail(f"import {name}: {type(exc).__name__}: {exc}", failures)
        else:
            ok(f"import {name}")


def check_jsonl(path: Path, failures: list[str]) -> None:
    if not path.exists():
        fail(f"missing {path}", failures)
        return

    count = 0
    with path.open() as handle:
        for count, line in enumerate(handle, 1):
            try:
                data = json.loads(line)
            except json.JSONDecodeError as exc:
                fail(f"invalid JSON in {path}:{count}: {exc}", failures)
                return
            messages = data.get("messages")
            if not isinstance(messages, list) or not messages:
                fail(f"missing messages in {path}:{count}", failures)
                return

    if count == 0:
        fail(f"empty split {path}", failures)
    else:
        ok(f"{path} ({count} rows)")


def check_training_track(track: str, failures: list[str]) -> None:
    root = ROOT / track
    for rel in (
        "README.md",
        "CONDUCTOR.md",
        "scripts/train.py",
        "scripts/build_dataset.py",
        "scripts/download_hermes_dataset.py",
        "scripts/evaluate.py",
        "scripts/compare.py",
        "scripts/push_to_hf.sh",
        "scripts/run_train.sh",
    ):
        path = root / rel
        if path.exists():
            ok(str(path.relative_to(ROOT)))
        else:
            fail(f"missing {path.relative_to(ROOT)}", failures)

    configs = sorted((root / "scripts").glob("train_config*.yaml"))
    if not configs:
        fail(f"no train configs in {track}", failures)
    for path in configs:
        with path.open() as handle:
            cfg = yaml.safe_load(handle)
        for key in ("model", "adapter_path", "data"):
            if key not in cfg:
                fail(f"{path.relative_to(ROOT)} missing {key}", failures)
                break
        else:
            ok(f"{path.relative_to(ROOT)} -> {cfg['model']}")

    for split in ("train", "val", "valid", "test"):
        check_jsonl(root / "data" / "splits" / f"{split}.jsonl", failures)


def check_ollama_pack(failures: list[str]) -> None:
    root = ROOT / "ollama-pack"
    for rel in (
        "README.md",
        "CONDUCTOR.md",
        "scripts/export_ollama.sh",
        "scripts/create_experimental_safetensors.sh",
        "scripts/runtime_smoke.sh",
        "scripts/runtime_smoke_lmstudio.sh",
    ):
        path = root / rel
        if path.exists():
            ok(str(path.relative_to(ROOT)))
        else:
            fail(f"missing {path.relative_to(ROOT)}", failures)

    modelfiles = sorted((root / "modelfiles").glob("*.Modelfile"))
    if not modelfiles:
        fail("no Ollama Modelfiles", failures)
    for path in modelfiles:
        ok(str(path.relative_to(ROOT)))


def check_endpoint_pilots(failures: list[str]) -> None:
    pilot_root = ROOT / "benchmarks" / "endpoint_pilots"
    for rel in ("README.md", "bfcl_pilot.json", "coding_pilot.json", "ifeval_pilot.json"):
        path = pilot_root / rel
        if not path.exists():
            fail(f"missing {path.relative_to(ROOT)}", failures)
            continue
        if path.suffix == ".json":
            try:
                suite = json.loads(path.read_text(encoding="utf-8"))
            except json.JSONDecodeError as exc:
                fail(f"invalid JSON in {path.relative_to(ROOT)}: {exc}", failures)
                continue
            if not isinstance(suite, list) or not suite:
                fail(f"{path.relative_to(ROOT)} must be a non-empty JSON array", failures)
                continue
            for index, case in enumerate(suite, 1):
                if not isinstance(case, dict) or not {"id", "category", "messages", "expected"} <= set(case):
                    fail(f"{path.relative_to(ROOT)} case {index} missing required keys", failures)
                    break
            else:
                ok(f"{path.relative_to(ROOT)} ({len(suite)} cases)")
        else:
            ok(str(path.relative_to(ROOT)))


def check_conductor(failures: list[str]) -> None:
    required = (
        "index.md",
        "product.md",
        "tech-stack.md",
        "workflow.md",
        "tracks.md",
        "requirements.md",
        "design.md",
        "contracts.md",
    )
    for base in CONDUCTOR_ROOTS:
        conductor = base / "conductor"
        label_base = base.relative_to(ROOT) if base != ROOT else Path(".")
        for rel in required:
            path = conductor / rel
            if path.exists():
                ok(str((label_base / "conductor" / rel).as_posix()))
            else:
                fail(f"missing {(label_base / 'conductor' / rel).as_posix()}", failures)

    hub_extra = ("product-guidelines.md", "health-score.md")
    for rel in hub_extra:
        path = ROOT / "conductor" / rel
        if path.exists():
            ok(str((Path(".") / "conductor" / rel).as_posix()))
        else:
            fail(f"missing {(Path('.') / 'conductor' / rel).as_posix()}", failures)

    result = subprocess.run(
        [sys.executable, str(ROOT / "scripts/check_conductor_track_consistency.py")],
        capture_output=True,
        text=True,
    )
    if result.returncode:
        fail(f"conductor track consistency: {result.stderr.strip() or result.stdout.strip()}", failures)
    else:
        ok(result.stdout.strip())


def check_shell_syntax(failures: list[str]) -> None:
    scripts = [
        ROOT / "gemma4/scripts/push_to_hf.sh",
        ROOT / "gemma4/scripts/run_train.sh",
        ROOT / "lfm2/scripts/push_to_hf.sh",
        ROOT / "lfm2/scripts/run_train.sh",
        ROOT / "ollama-pack/scripts/export_ollama.sh",
        ROOT / "ollama-pack/scripts/create_experimental_safetensors.sh",
        ROOT / "ollama-pack/scripts/runtime_smoke.sh",
        ROOT / "ollama-pack/scripts/runtime_smoke_lmstudio.sh",
        ROOT / "scripts/env.sh",
        ROOT / "scripts/repo_status.sh",
        ROOT / "scripts/run_qwen36_q4_runtime_proof.sh",
        ROOT / "templates/benchmark/lm-evaluation-harness-smoke.sh",
    ]
    result = subprocess.run(["bash", "-n", *map(str, scripts)], capture_output=True, text=True)
    if result.returncode:
        fail(f"shell syntax: {result.stderr.strip()}", failures)
    else:
        ok("shell syntax")

    py_scripts = [
        ROOT / "scripts/check_model_candidates.py",
        ROOT / "scripts/azure_preflight.py",
        ROOT / "scripts/azure_status.py",
        ROOT / "scripts/dataset_token_audit.py",
        ROOT / "scripts/eval_prompt_audit.py",
        ROOT / "scripts/eval_response_gate.py",
        ROOT / "scripts/run_tool_call_benchmark.py",
        ROOT / "scripts/run_endpoint_tool_call_benchmark.py",
        ROOT / "scripts/run_endpoint_pilot_benchmark.py",
        ROOT / "scripts/run_local_pilot_benchmark.py",
        ROOT / "scripts/run_transformers_pilot_benchmark.py",
        ROOT / "scripts/build_tool_call_training_data.py",
        ROOT / "scripts/normalize_tool_response.py",
        ROOT / "ollama-pack/scripts/normalize_runtime_json.py",
        ROOT / "scripts/run_benchmark.py",
        ROOT / "scripts/run_teacher_evaluator.py",
        ROOT / "scripts/create_runtime_format_lane_card.py",
        ROOT / "scripts/create_runtime_format_proof_queue.py",
        ROOT / "scripts/validate_runtime_prompt_profiles.py",
        ROOT / "scripts/validate_publication_bundle.py",
        ROOT / "scripts/check_standard_benchmark_coverage.py",
        ROOT / "scripts/validate_standard_benchmark_coverage_reports.py",
        ROOT / "scripts/prepare_hf_adapter_package.py",
        ROOT / "scripts/publish_hf_adapter_package.py",
        ROOT / "scripts/audit_publication_dataset_sources.py",
        ROOT / "scripts/check_storage_layout.py",
        ROOT / "scripts/smoke_official_benchmark_env.py",
        ROOT / "scripts/run_mlx_lm_eval.py",
        ROOT / "scripts/materialize_publication_dataset.py",
        ROOT / "scripts/materialize_gemma4_no_thinking_dataset.py",
        ROOT / "scripts/audit_tool_call_data.py",
        ROOT / "scripts/validate_gemma4_no_thinking_dataset.py",
        ROOT / "scripts/validate_runtime_format_lanes.py",
        ROOT / "scripts/validate_readiness.py",
        ROOT / "scripts/check_conductor_track_consistency.py",
        ROOT / "scripts/check_mem0_benchmark_evidence.py",
        ROOT / "scripts/validate_mem0_benchmark_evidence_report.py",
        ROOT / "scripts/summarize_mem0_benchmarks.py",
        ROOT / "scripts/validate_mem0_benchmark_index.py",
        ROOT / "scripts/validate_mem0_run_cards.py",
        ROOT / "scripts/build_mem0_candidate_queue.py",
        ROOT / "scripts/validate_mem0_candidate_queue.py",
        ROOT / "scripts/check_specialist_runtime_preflight.py",
        ROOT / "scripts/validate_specialist_runtime_preflight_report.py",
        ROOT / "scripts/validate_official_benchmark_manifests.py",
        ROOT / "scripts/build_official_candidate_suite_queue.py",
        ROOT / "scripts/validate_official_candidate_suite_queue.py",
        ROOT / "scripts/check_official_bfcl_preflight.py",
        ROOT / "scripts/validate_official_bfcl_preflight.py",
        ROOT / "scripts/check_official_coding_preflight.py",
        ROOT / "scripts/validate_official_coding_preflight.py",
        ROOT / "scripts/materialize_safety_refusal_suite.py",
        ROOT / "scripts/validate_safety_refusal_suite.py",
        ROOT / "scripts/build_safety_refusal_result_report.py",
        ROOT / "scripts/validate_safety_refusal_result_report.py",
        ROOT / "scripts/build_safety_refusal_repair_queue.py",
        ROOT / "scripts/validate_safety_refusal_repair_queue.py",
        ROOT / "scripts/validate_safety_refusal_repair_dataset.py",
        ROOT / "scripts/check_ruler_long_context_preflight.py",
        ROOT / "scripts/validate_ruler_long_context_preflight.py",
        ROOT / "scripts/build_official_candidate_execution_matrix.py",
        ROOT / "scripts/validate_official_candidate_execution_matrix.py",
        ROOT / "scripts/check_scorecard_offload_readiness.py",
        ROOT / "scripts/validate_scorecard_offload_readiness.py",
        ROOT / "scripts/build_all_candidate_benchmark_coverage.py",
        ROOT / "scripts/validate_all_candidate_benchmark_coverage.py",
        ROOT / "scripts/build_runtime_proof_action_queue.py",
        ROOT / "scripts/validate_runtime_proof_action_queue.py",
        ROOT / "scripts/build_prompt_profile_repair_queue.py",
        ROOT / "scripts/validate_prompt_profile_repair_queue.py",
        ROOT / "scripts/build_prompt_profile_repair_experiments.py",
        ROOT / "scripts/validate_prompt_profile_repair_experiments.py",
        ROOT / "scripts/build_prompt_profile_repair_ledger.py",
        ROOT / "scripts/validate_prompt_profile_repair_ledger.py",
        ROOT / "scripts/validate_prompt_profile_repair_results.py",
        ROOT / "scripts/build_constrained_envelope_repair_plan.py",
        ROOT / "scripts/validate_constrained_envelope_repair_plan.py",
        ROOT / "scripts/run_constrained_envelope_diagnostic.py",
        ROOT / "scripts/validate_constrained_envelope_diagnostic_report.py",
        ROOT / "scripts/validate_nanbeige_heldout_envelope_report.py",
        ROOT / "scripts/select_prompt_profile_repair_experiment.py",
        ROOT / "scripts/validate_prompt_profile_repair_selection.py",
        ROOT / "scripts/convert_mlx_lora_to_peft.py",
        ROOT / "scripts/colab_mlx_adapter_portability_probe.py",
        ROOT / "scripts/colab_peft_adapter_load_smoke.py",
        ROOT / "scripts/colab_peft_lm_eval_selected.py",
        ROOT / "scripts/hf_jobs_peft_lm_eval_selected.py",
        ROOT / "scripts/submit_hf_jobs_peft_scorecard.py",
        ROOT / "scripts/submit_azure_peft_scorecard.py",
        ROOT / "scripts/kaggle_peft_lm_eval_selected.py",
        ROOT / "scripts/submit_kaggle_peft_scorecard.py",
        ROOT / "scripts/modal_peft_lm_eval_selected.py",
        ROOT / "scripts/submit_modal_peft_scorecard.py",
        ROOT / "scripts/validate_modal_scorecard_contract.py",
        ROOT / "scripts/validate_modal_policy_gate.py",
        ROOT / "scripts/submit_lightning_peft_scorecard.py",
        ROOT / "scripts/submit_ngc_cloud_function_scorecard.py",
        ROOT / "scripts/build_cloud_unblock_checklist.py",
        ROOT / "scripts/build_cloud_operator_gates.py",
        ROOT / "scripts/build_blocked_track_matrix.py",
        ROOT / "scripts/select_scorecard_backend.py",
        ROOT / "scripts/validate_cloud_blocker_reports.py",
        ROOT / "scripts/validate_cloud_operator_gates.py",
        ROOT / "scripts/validate_scorecard_backend_selection.py",
        ROOT / "scripts/validate_kaggle_kernel_contract.py",
        ROOT / "scripts/validate_kaggle_torch_policy_wheel_proof.py",
        ROOT / "scripts/validate_kaggle_rerun_submit_report.py",
        ROOT / "scripts/sync_kaggle_rerun_status.py",
        ROOT / "scripts/validate_kaggle_result_ingest.py",
        ROOT / "scripts/validate_modal_result_ingest.py",
        ROOT / "scripts/validate_free_container_account_probe.py",
        ROOT / "scripts/colab_benchmark_env_smoke.py",
        ROOT / "scripts/run_jina_mlx_embedding_benchmark.py",
        ROOT / "scripts/run_colbert_read_stack_smoke.py",
        ROOT / "scripts/colab_lm_eval_shard.py",
        ROOT / "gemma4/data/strict_tool_call/tools/materialize_free_text_copy_splits_v6.py",
        ROOT / "gemma4/data/strict_tool_call/tools/materialize_safety_refusal_repair_splits_v7.py",
    ]
    result = subprocess.run(
        [sys.executable, "-m", "py_compile", *map(str, py_scripts)],
        capture_output=True,
        text=True,
    )
    if result.returncode:
        fail(f"python syntax: {result.stderr.strip()}", failures)
    else:
        ok("python syntax")


def check_storage_layout(failures: list[str]) -> None:
    if not STORAGE_ROOT.exists():
        ok(f"storage layout skipped: {STORAGE_ROOT} not present")
        return

    result = subprocess.run(
        [
            sys.executable,
            str(ROOT / "scripts/check_storage_layout.py"),
            "--root",
            str(STORAGE_ROOT),
        ],
        capture_output=True,
        text=True,
    )
    if result.returncode:
        fail(f"storage layout: {result.stdout.strip()} {result.stderr.strip()}".strip(), failures)
    else:
        ok("storage layout")


def check_mem0_benchmark_evidence(failures: list[str]) -> None:
    eval_root = STORAGE_ROOT / "hermes-evals"
    if not eval_root.exists():
        ok(f"mem0 benchmark evidence skipped: {eval_root} not present")
        return

    result = subprocess.run(
        [
            sys.executable,
            str(ROOT / "scripts/check_mem0_benchmark_evidence.py"),
            "--eval-root",
            str(eval_root),
            "--no-write",
        ],
        capture_output=True,
        text=True,
    )
    if result.returncode:
        fail(f"mem0 benchmark evidence: {result.stdout.strip()} {result.stderr.strip()}".strip(), failures)
    else:
        ok("mem0 benchmark evidence")


def check_mem0_benchmark_evidence_report(failures: list[str]) -> None:
    eval_root = STORAGE_ROOT / "hermes-evals"
    result = subprocess.run(
        [
            sys.executable,
            str(ROOT / "scripts/validate_mem0_benchmark_evidence_report.py"),
            "--eval-root",
            str(eval_root),
        ],
        capture_output=True,
        text=True,
    )
    if result.returncode:
        fail(f"mem0 benchmark evidence report: {result.stdout.strip()} {result.stderr.strip()}".strip(), failures)
    else:
        ok("mem0 benchmark evidence report")


def check_mem0_benchmark_index(failures: list[str]) -> None:
    eval_root = STORAGE_ROOT / "hermes-evals"
    result = subprocess.run(
        [
            sys.executable,
            str(ROOT / "scripts/validate_mem0_benchmark_index.py"),
            "--eval-root",
            str(eval_root),
        ],
        capture_output=True,
        text=True,
    )
    if result.returncode:
        fail(f"mem0 benchmark index: {result.stdout.strip()} {result.stderr.strip()}".strip(), failures)
    else:
        ok("mem0 benchmark index")


def check_mem0_run_cards(failures: list[str]) -> None:
    result = subprocess.run(
        [
            sys.executable,
            str(ROOT / "scripts/validate_mem0_run_cards.py"),
        ],
        capture_output=True,
        text=True,
    )
    if result.returncode:
        fail(f"mem0 run cards: {result.stdout.strip()} {result.stderr.strip()}".strip(), failures)
    else:
        ok("mem0 run cards")


def check_candidate_registries(failures: list[str]) -> None:
    checks = (
        ("root model candidates", [sys.executable, str(ROOT / "scripts/check_model_candidates.py"), "--schema-only"]),
        ("mem0 model candidates", [sys.executable, str(ROOT / "scripts/check_mem0_model_candidates.py")]),
    )
    for label, command in checks:
        result = subprocess.run(command, capture_output=True, text=True)
        if result.returncode:
            fail(f"{label}: {result.stdout.strip()} {result.stderr.strip()}".strip(), failures)
        else:
            ok(label)


def check_candidate_benchmark_coverage(failures: list[str]) -> None:
    result = subprocess.run(
        [
            sys.executable,
            str(ROOT / "scripts/validate_all_candidate_benchmark_coverage.py"),
        ],
        capture_output=True,
        text=True,
    )
    if result.returncode:
        fail(f"all-candidate benchmark coverage: {result.stdout.strip()} {result.stderr.strip()}".strip(), failures)
    else:
        ok("all-candidate benchmark coverage")


def check_runtime_proof_action_queue(failures: list[str]) -> None:
    result = subprocess.run(
        [
            sys.executable,
            str(ROOT / "scripts/validate_runtime_proof_action_queue.py"),
        ],
        capture_output=True,
        text=True,
    )
    if result.returncode:
        fail(f"runtime-proof action queue: {result.stdout.strip()} {result.stderr.strip()}".strip(), failures)
    else:
        ok("runtime-proof action queue")


def check_scorecard_offload_readiness(failures: list[str]) -> None:
    result = subprocess.run(
        [
            sys.executable,
            str(ROOT / "scripts/validate_scorecard_offload_readiness.py"),
        ],
        capture_output=True,
        text=True,
    )
    if result.returncode:
        fail(f"scorecard offload readiness: {result.stdout.strip()} {result.stderr.strip()}".strip(), failures)
    else:
        ok("scorecard offload readiness")


def check_standard_benchmark_coverage_reports(failures: list[str]) -> None:
    result = subprocess.run(
        [
            sys.executable,
            str(ROOT / "scripts/validate_standard_benchmark_coverage_reports.py"),
        ],
        capture_output=True,
        text=True,
    )
    if result.returncode:
        fail(f"standard benchmark coverage reports: {result.stdout.strip()} {result.stderr.strip()}".strip(), failures)
    else:
        ok("standard benchmark coverage reports")


def check_mem0_candidate_queue(failures: list[str]) -> None:
    result = subprocess.run(
        [
            sys.executable,
            str(ROOT / "scripts/validate_mem0_candidate_queue.py"),
        ],
        capture_output=True,
        text=True,
    )
    if result.returncode:
        fail(f"mem0 candidate queue: {result.stdout.strip()} {result.stderr.strip()}".strip(), failures)
    else:
        ok("mem0 candidate queue")


def check_specialist_runtime_preflight_report(failures: list[str]) -> None:
    result = subprocess.run(
        [
            sys.executable,
            str(ROOT / "scripts/validate_specialist_runtime_preflight_report.py"),
        ],
        capture_output=True,
        text=True,
    )
    if result.returncode:
        fail(f"specialist runtime preflight report: {result.stdout.strip()} {result.stderr.strip()}".strip(), failures)
    else:
        ok("specialist runtime preflight report")


def check_cloud_blocker_reports(failures: list[str]) -> None:
    result = subprocess.run(
        [
            sys.executable,
            str(ROOT / "scripts/validate_cloud_blocker_reports.py"),
        ],
        capture_output=True,
        text=True,
    )
    if result.returncode:
        fail(f"cloud blocker reports: {result.stdout.strip()} {result.stderr.strip()}".strip(), failures)
    else:
        ok("cloud blocker reports")


def check_cloud_operator_gates(failures: list[str]) -> None:
    result = subprocess.run(
        [
            sys.executable,
            str(ROOT / "scripts/validate_cloud_operator_gates.py"),
        ],
        capture_output=True,
        text=True,
    )
    if result.returncode:
        fail(f"cloud operator gates: {result.stdout.strip()} {result.stderr.strip()}".strip(), failures)
    else:
        ok("cloud operator gates")


def check_scorecard_backend_selection(failures: list[str]) -> None:
    result = subprocess.run(
        [
            sys.executable,
            str(ROOT / "scripts/validate_scorecard_backend_selection.py"),
        ],
        capture_output=True,
        text=True,
    )
    if result.returncode:
        fail(f"scorecard backend selection: {result.stdout.strip()} {result.stderr.strip()}".strip(), failures)
    else:
        ok("scorecard backend selection")


def check_kaggle_kernel_contract(failures: list[str]) -> None:
    result = subprocess.run(
        [
            sys.executable,
            str(ROOT / "scripts/validate_kaggle_kernel_contract.py"),
        ],
        capture_output=True,
        text=True,
    )
    if result.returncode:
        fail(f"kaggle kernel contract: {result.stdout.strip()} {result.stderr.strip()}".strip(), failures)
    else:
        ok("kaggle kernel contract")


def check_kaggle_torch_policy_wheel_proof(failures: list[str]) -> None:
    result = subprocess.run(
        [
            sys.executable,
            str(ROOT / "scripts/validate_kaggle_torch_policy_wheel_proof.py"),
        ],
        capture_output=True,
        text=True,
    )
    if result.returncode:
        fail(f"kaggle torch policy wheel proof: {result.stdout.strip()} {result.stderr.strip()}".strip(), failures)
    else:
        ok("kaggle torch policy wheel proof")


def check_kaggle_rerun_submit_report(failures: list[str]) -> None:
    result = subprocess.run(
        [
            sys.executable,
            str(ROOT / "scripts/validate_kaggle_rerun_submit_report.py"),
        ],
        capture_output=True,
        text=True,
    )
    if result.returncode:
        fail(f"kaggle P100 rerun submit report: {result.stdout.strip()} {result.stderr.strip()}".strip(), failures)
    else:
        ok("kaggle P100 rerun submit report")


def check_kaggle_result_ingest(failures: list[str]) -> None:
    result = subprocess.run(
        [
            sys.executable,
            str(ROOT / "scripts/validate_kaggle_result_ingest.py"),
        ],
        capture_output=True,
        text=True,
    )
    if result.returncode:
        fail(f"kaggle result ingest: {result.stdout.strip()} {result.stderr.strip()}".strip(), failures)
    else:
        ok("kaggle result ingest")


def check_modal_result_ingest(failures: list[str]) -> None:
    result = subprocess.run(
        [
            sys.executable,
            str(ROOT / "scripts/validate_modal_result_ingest.py"),
        ],
        capture_output=True,
        text=True,
    )
    if result.returncode:
        fail(f"modal result ingest: {result.stdout.strip()} {result.stderr.strip()}".strip(), failures)
    else:
        ok("modal result ingest")


def check_modal_scorecard_contract(failures: list[str]) -> None:
    result = subprocess.run(
        [
            sys.executable,
            str(ROOT / "scripts/validate_modal_scorecard_contract.py"),
        ],
        capture_output=True,
        text=True,
    )
    if result.returncode:
        fail(f"modal scorecard contract: {result.stdout.strip()} {result.stderr.strip()}".strip(), failures)
    else:
        ok("modal scorecard contract")


def check_modal_policy_gate(failures: list[str]) -> None:
    result = subprocess.run(
        [
            sys.executable,
            str(ROOT / "scripts/validate_modal_policy_gate.py"),
        ],
        capture_output=True,
        text=True,
    )
    if result.returncode:
        fail(f"modal policy gate: {result.stdout.strip()} {result.stderr.strip()}".strip(), failures)
    else:
        ok("modal policy gate")


def check_free_container_account_probe(failures: list[str]) -> None:
    result = subprocess.run(
        [
            sys.executable,
            str(ROOT / "scripts/validate_free_container_account_probe.py"),
        ],
        capture_output=True,
        text=True,
    )
    if result.returncode:
        fail(f"free-container account probe: {result.stdout.strip()} {result.stderr.strip()}".strip(), failures)
    else:
        ok("free-container account probe")


def check_prompt_profile_repair_queue(failures: list[str]) -> None:
    result = subprocess.run(
        [
            sys.executable,
            str(ROOT / "scripts/validate_prompt_profile_repair_queue.py"),
        ],
        capture_output=True,
        text=True,
    )
    if result.returncode:
        fail(f"prompt/profile repair queue: {result.stdout.strip()} {result.stderr.strip()}".strip(), failures)
    else:
        ok("prompt/profile repair queue")


def check_prompt_profile_repair_experiments(failures: list[str]) -> None:
    result = subprocess.run(
        [
            sys.executable,
            str(ROOT / "scripts/validate_prompt_profile_repair_experiments.py"),
        ],
        capture_output=True,
        text=True,
    )
    if result.returncode:
        fail(f"prompt/profile repair experiments: {result.stdout.strip()} {result.stderr.strip()}".strip(), failures)
    else:
        ok("prompt/profile repair experiments")


def check_prompt_profile_repair_ledger(failures: list[str]) -> None:
    result = subprocess.run(
        [
            sys.executable,
            str(ROOT / "scripts/validate_prompt_profile_repair_ledger.py"),
        ],
        capture_output=True,
        text=True,
    )
    if result.returncode:
        fail(f"prompt/profile repair ledger: {result.stdout.strip()} {result.stderr.strip()}".strip(), failures)
    else:
        ok("prompt/profile repair ledger")


def check_prompt_profile_repair_results(failures: list[str]) -> None:
    result = subprocess.run(
        [
            sys.executable,
            str(ROOT / "scripts/validate_prompt_profile_repair_results.py"),
        ],
        capture_output=True,
        text=True,
    )
    if result.returncode:
        fail(f"prompt/profile repair results: {result.stdout.strip()} {result.stderr.strip()}".strip(), failures)
    else:
        ok("prompt/profile repair results")


def check_constrained_envelope_repair_plan(failures: list[str]) -> None:
    result = subprocess.run(
        [
            sys.executable,
            str(ROOT / "scripts/validate_constrained_envelope_repair_plan.py"),
        ],
        capture_output=True,
        text=True,
    )
    if result.returncode:
        fail(f"constrained-envelope repair plan: {result.stdout.strip()} {result.stderr.strip()}".strip(), failures)
    else:
        ok("constrained-envelope repair plan")


def check_constrained_envelope_diagnostic_report(failures: list[str]) -> None:
    result = subprocess.run(
        [
            sys.executable,
            str(ROOT / "scripts/validate_constrained_envelope_diagnostic_report.py"),
        ],
        capture_output=True,
        text=True,
    )
    if result.returncode:
        fail(
            f"constrained-envelope diagnostic report: {result.stdout.strip()} {result.stderr.strip()}".strip(),
            failures,
        )
    else:
        ok("constrained-envelope diagnostic report")


def check_nanbeige_heldout_envelope_report(failures: list[str]) -> None:
    result = subprocess.run(
        [
            sys.executable,
            str(ROOT / "scripts/validate_nanbeige_heldout_envelope_report.py"),
        ],
        capture_output=True,
        text=True,
    )
    if result.returncode:
        fail(f"Nanbeige held-out envelope report: {result.stdout.strip()} {result.stderr.strip()}".strip(), failures)
    else:
        ok("Nanbeige held-out envelope report")


def check_prompt_profile_repair_selection(failures: list[str]) -> None:
    result = subprocess.run(
        [
            sys.executable,
            str(ROOT / "scripts/validate_prompt_profile_repair_selection.py"),
        ],
        capture_output=True,
        text=True,
    )
    if result.returncode:
        fail(f"prompt/profile repair selection: {result.stdout.strip()} {result.stderr.strip()}".strip(), failures)
    else:
        ok("prompt/profile repair selection")


def check_publication_bundles(failures: list[str]) -> None:
    bundle = ROOT / "reports/publication/qwen3-4b-strict-toolcall-v4-targeted"
    result = subprocess.run(
        [
            sys.executable,
            str(ROOT / "scripts/validate_publication_bundle.py"),
            str(bundle),
            "--require-ready",
        ],
        capture_output=True,
        text=True,
    )
    if result.returncode:
        fail(f"publication bundle: {result.stdout.strip()} {result.stderr.strip()}".strip(), failures)
    else:
        ok("publication bundle qwen3-4b-strict-toolcall-v4-targeted")

    bundle = ROOT / "reports/publication/qwen3-4b-strict-toolcall-v6-free-text-copy"
    coverage = ROOT / "reports/benchmark/standard-coverage/qwen3-v6-free-text-copy-standard-coverage-20260613.json"
    result = subprocess.run(
        [
            sys.executable,
            str(ROOT / "scripts/validate_publication_bundle.py"),
            str(bundle),
            "--expect-blocked",
            "--coverage-report",
            str(coverage),
        ],
        capture_output=True,
        text=True,
    )
    if result.returncode:
        fail(f"publication bundle v6: {result.stdout.strip()} {result.stderr.strip()}".strip(), failures)
    else:
        ok("publication bundle qwen3-4b-strict-toolcall-v6-free-text-copy blocked")


def check_official_benchmark_manifests(failures: list[str]) -> None:
    result = subprocess.run(
        [sys.executable, str(ROOT / "scripts/validate_official_benchmark_manifests.py")],
        capture_output=True,
        text=True,
    )
    if result.returncode:
        fail(f"official benchmark manifests: {result.stdout.strip()} {result.stderr.strip()}".strip(), failures)
    else:
        ok("official benchmark manifests")


def check_official_candidate_suite_queue(failures: list[str]) -> None:
    result = subprocess.run(
        [sys.executable, str(ROOT / "scripts/validate_official_candidate_suite_queue.py")],
        capture_output=True,
        text=True,
    )
    if result.returncode:
        fail(f"official candidate suite queue: {result.stdout.strip()} {result.stderr.strip()}".strip(), failures)
    else:
        ok("official candidate suite queue")


def check_official_bfcl_preflight(failures: list[str]) -> None:
    result = subprocess.run(
        [sys.executable, str(ROOT / "scripts/validate_official_bfcl_preflight.py")],
        capture_output=True,
        text=True,
    )
    if result.returncode:
        fail(f"official BFCL preflight: {result.stdout.strip()} {result.stderr.strip()}".strip(), failures)
    else:
        ok("official BFCL preflight")


def check_official_coding_preflight(failures: list[str]) -> None:
    result = subprocess.run(
        [sys.executable, str(ROOT / "scripts/validate_official_coding_preflight.py")],
        capture_output=True,
        text=True,
    )
    if result.returncode:
        fail(f"official coding preflight: {result.stdout.strip()} {result.stderr.strip()}".strip(), failures)
    else:
        ok("official coding preflight")


def check_safety_refusal_suite(failures: list[str]) -> None:
    result = subprocess.run(
        [sys.executable, str(ROOT / "scripts/validate_safety_refusal_suite.py")],
        capture_output=True,
        text=True,
    )
    if result.returncode:
        fail(f"safety/refusal suite: {result.stdout.strip()} {result.stderr.strip()}".strip(), failures)
    else:
        ok("safety/refusal suite")


def check_safety_refusal_result_report(failures: list[str]) -> None:
    result = subprocess.run(
        [sys.executable, str(ROOT / "scripts/validate_safety_refusal_result_report.py")],
        capture_output=True,
        text=True,
    )
    if result.returncode:
        fail(f"safety/refusal result report: {result.stdout.strip()} {result.stderr.strip()}".strip(), failures)
    else:
        ok("safety/refusal result report")


def check_safety_refusal_repair_queue(failures: list[str]) -> None:
    result = subprocess.run(
        [sys.executable, str(ROOT / "scripts/validate_safety_refusal_repair_queue.py")],
        capture_output=True,
        text=True,
    )
    if result.returncode:
        fail(f"safety/refusal repair queue: {result.stdout.strip()} {result.stderr.strip()}".strip(), failures)
    else:
        ok("safety/refusal repair queue")


def check_safety_refusal_repair_dataset(failures: list[str]) -> None:
    result = subprocess.run(
        [sys.executable, str(ROOT / "scripts/validate_safety_refusal_repair_dataset.py")],
        capture_output=True,
        text=True,
    )
    if result.returncode:
        fail(f"safety/refusal repair dataset: {result.stdout.strip()} {result.stderr.strip()}".strip(), failures)
    else:
        ok("safety/refusal repair dataset")


def check_ruler_long_context_preflight(failures: list[str]) -> None:
    result = subprocess.run(
        [sys.executable, str(ROOT / "scripts/validate_ruler_long_context_preflight.py")],
        capture_output=True,
        text=True,
    )
    if result.returncode:
        fail(f"RULER long-context preflight: {result.stdout.strip()} {result.stderr.strip()}".strip(), failures)
    else:
        ok("RULER long-context preflight")


def check_official_candidate_execution_matrix(failures: list[str]) -> None:
    result = subprocess.run(
        [sys.executable, str(ROOT / "scripts/validate_official_candidate_execution_matrix.py")],
        capture_output=True,
        text=True,
    )
    if result.returncode:
        fail(f"official candidate execution matrix: {result.stdout.strip()} {result.stderr.strip()}".strip(), failures)
    else:
        ok("official candidate execution matrix")


def check_gemma4_no_thinking_dataset(failures: list[str]) -> None:
    result = subprocess.run(
        [sys.executable, str(ROOT / "scripts/validate_gemma4_no_thinking_dataset.py")],
        capture_output=True,
        text=True,
    )
    if result.returncode:
        fail(f"Gemma 4 no-thinking dataset: {result.stdout.strip()} {result.stderr.strip()}".strip(), failures)
    else:
        ok(result.stdout.strip())


def check_runtime_templates(failures: list[str]) -> None:
    for rel in (
        "templates/runtime/runtime-card.md",
        "templates/runtime/format-lane-proof-card.md",
        "templates/ngc/README.md",
        "templates/ngc/qwen3-v4-peft-scorecard.Containerfile",
        "RUNTIME_FORMAT_LANES.yaml",
        "RUNTIME_FORMAT_PROOF_QUEUE.yaml",
        "RUNTIME_PROMPT_PROFILES.yaml",
    ):
        path = ROOT / rel
        if path.exists():
            ok(rel)
        else:
            fail(f"missing {rel}", failures)


def check_runtime_format_lanes(failures: list[str]) -> None:
    result = subprocess.run(
        [sys.executable, str(ROOT / "scripts/validate_runtime_format_lanes.py")],
        capture_output=True,
        text=True,
    )
    if result.returncode:
        fail(f"runtime format lanes: {result.stderr.strip() or result.stdout.strip()}", failures)
    else:
        ok(result.stdout.strip())

    result = subprocess.run(
        [sys.executable, str(ROOT / "scripts/create_runtime_format_proof_queue.py"), "--check"],
        capture_output=True,
        text=True,
    )
    if result.returncode:
        fail(f"runtime format proof queue: {result.stdout.strip()} {result.stderr.strip()}".strip(), failures)
    else:
        ok(result.stdout.strip())

    result = subprocess.run(
        [sys.executable, str(ROOT / "scripts/validate_runtime_prompt_profiles.py")],
        capture_output=True,
        text=True,
    )
    if result.returncode:
        fail(f"runtime prompt profiles: {result.stderr.strip() or result.stdout.strip()}", failures)
    else:
        ok(result.stdout.strip())


def main() -> int:
    failures: list[str] = []
    check_imports(failures)
    for track in TRAINING_TRACKS:
        check_training_track(track, failures)
    check_ollama_pack(failures)
    check_endpoint_pilots(failures)
    check_conductor(failures)
    check_shell_syntax(failures)
    check_runtime_templates(failures)
    check_runtime_format_lanes(failures)
    check_publication_bundles(failures)
    check_official_benchmark_manifests(failures)
    check_official_candidate_suite_queue(failures)
    check_official_bfcl_preflight(failures)
    check_official_coding_preflight(failures)
    check_safety_refusal_suite(failures)
    check_safety_refusal_result_report(failures)
    check_safety_refusal_repair_queue(failures)
    check_safety_refusal_repair_dataset(failures)
    check_ruler_long_context_preflight(failures)
    check_official_candidate_execution_matrix(failures)
    check_gemma4_no_thinking_dataset(failures)
    check_storage_layout(failures)
    check_mem0_benchmark_evidence(failures)
    check_mem0_benchmark_evidence_report(failures)
    check_mem0_benchmark_index(failures)
    check_mem0_run_cards(failures)
    check_candidate_registries(failures)
    check_candidate_benchmark_coverage(failures)
    check_runtime_proof_action_queue(failures)
    check_scorecard_offload_readiness(failures)
    check_standard_benchmark_coverage_reports(failures)
    check_mem0_candidate_queue(failures)
    check_specialist_runtime_preflight_report(failures)
    check_cloud_blocker_reports(failures)
    check_cloud_operator_gates(failures)
    check_scorecard_backend_selection(failures)
    check_kaggle_kernel_contract(failures)
    check_kaggle_torch_policy_wheel_proof(failures)
    check_kaggle_rerun_submit_report(failures)
    check_kaggle_result_ingest(failures)
    check_modal_scorecard_contract(failures)
    check_modal_policy_gate(failures)
    check_modal_result_ingest(failures)
    check_free_container_account_probe(failures)
    check_prompt_profile_repair_queue(failures)
    check_prompt_profile_repair_experiments(failures)
    check_prompt_profile_repair_ledger(failures)
    check_prompt_profile_repair_results(failures)
    check_constrained_envelope_repair_plan(failures)
    check_constrained_envelope_diagnostic_report(failures)
    check_nanbeige_heldout_envelope_report(failures)
    check_prompt_profile_repair_selection(failures)

    if failures:
        print("\nnot ready:")
        for item in failures:
            print(f"- {item}")
        return 1

    print("\nready: all structural readiness checks passed")
    return 0


if __name__ == "__main__":
    sys.exit(main())
