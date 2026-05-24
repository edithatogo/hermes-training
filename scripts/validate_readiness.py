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
        ROOT / "scripts/build_tool_call_training_data.py",
        ROOT / "scripts/normalize_tool_response.py",
        ROOT / "ollama-pack/scripts/normalize_runtime_json.py",
        ROOT / "scripts/run_benchmark.py",
        ROOT / "scripts/run_teacher_evaluator.py",
        ROOT / "scripts/check_storage_layout.py",
        ROOT / "scripts/validate_readiness.py",
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


def main() -> int:
    failures: list[str] = []
    check_imports(failures)
    for track in TRAINING_TRACKS:
        check_training_track(track, failures)
    check_ollama_pack(failures)
    check_endpoint_pilots(failures)
    check_conductor(failures)
    check_shell_syntax(failures)
    check_storage_layout(failures)

    if failures:
        print("\nnot ready:")
        for item in failures:
            print(f"- {item}")
        return 1

    print("\nready: all structural readiness checks passed")
    return 0


if __name__ == "__main__":
    sys.exit(main())
