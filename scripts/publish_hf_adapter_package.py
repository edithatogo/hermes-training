#!/usr/bin/env python3
"""Validate and optionally publish a prepared Hugging Face adapter package."""
from __future__ import annotations

import argparse
import json
import shutil
import subprocess
from dataclasses import dataclass
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[1]
DEFAULT_EXPORT_ROOT = Path("/Volumes/PortableSSD/hermes-exports")
REQUIRED_PACKAGE_FILES = ("adapters.safetensors", "adapter_config.json", "README.md", "package-manifest.json")


@dataclass(frozen=True)
class PublicationCheck:
    ok: bool
    message: str


def load_json(path: Path) -> dict[str, Any]:
    return json.loads(path.read_text(encoding="utf-8"))


def approval_phrase(package_dir: Path, repo_id: str) -> str:
    return f"I approve publishing HF adapter package {package_dir} to Hugging Face model repo {repo_id}."


def check_package(package_dir: Path, repo_id: str, *, export_root: Path) -> list[PublicationCheck]:
    checks: list[PublicationCheck] = []
    resolved_package = package_dir.resolve()
    resolved_export = export_root.resolve()
    checks.append(PublicationCheck(package_dir.exists(), f"package directory exists: {package_dir}"))
    try:
        resolved_package.relative_to(resolved_export)
        checks.append(PublicationCheck(True, f"package is under SSD export root: {resolved_export}"))
    except ValueError:
        checks.append(PublicationCheck(False, f"package is not under SSD export root: {resolved_export}"))

    for name in REQUIRED_PACKAGE_FILES:
        checks.append(PublicationCheck((package_dir / name).is_file(), f"required file present: {name}"))

    manifest_path = package_dir / "package-manifest.json"
    if not manifest_path.is_file():
        return checks

    manifest = load_json(manifest_path)
    checks.append(PublicationCheck(manifest.get("repo_id") == repo_id, f"manifest repo_id matches target: {repo_id}"))
    checks.append(PublicationCheck(manifest.get("publish_action_performed") is False, "manifest records dry-run package"))

    copied_files = manifest.get("copied_files") or []
    if not isinstance(copied_files, list):
        checks.append(PublicationCheck(False, "manifest copied_files is a list"))
    else:
        missing = []
        for entry in copied_files:
            target = Path(str(entry.get("target", "")))
            if not target.is_file():
                missing.append(str(target))
        checks.append(PublicationCheck(not missing, "manifest copied files exist in package"))

    blocked_until = manifest.get("blocked_until") or []
    checks.append(PublicationCheck(not blocked_until, "manifest has no remaining publication blockers"))
    return checks


def check_approval(approval_file: Path | None, phrase: str) -> list[PublicationCheck]:
    if approval_file is None:
        return [PublicationCheck(False, "approval file was provided")]
    if not approval_file.is_file():
        return [PublicationCheck(False, f"approval file exists: {approval_file}")]
    text = approval_file.read_text(encoding="utf-8")
    return [
        PublicationCheck(True, f"approval file exists: {approval_file}"),
        PublicationCheck(phrase in text, "approval file contains exact approval phrase"),
    ]


def run_hf_publish(package_dir: Path, repo_id: str, *, visibility: str) -> None:
    hf = shutil.which("hf")
    if hf is None:
        raise RuntimeError("Missing hf CLI on PATH")

    create_cmd = [hf, "repo", "create", repo_id, "--type", "model", "--exist-ok"]
    if visibility == "private":
        create_cmd.append("--private")
    subprocess.run(create_cmd, check=True)
    subprocess.run(
        [hf, "upload", repo_id, str(package_dir), ".", "--repo-type", "model"],
        check=True,
    )


def summarize(checks: list[PublicationCheck]) -> dict[str, Any]:
    return {
        "ok": all(check.ok for check in checks),
        "checks": [{"ok": check.ok, "message": check.message} for check in checks],
    }


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--package-dir", type=Path, required=True)
    parser.add_argument("--repo-id", required=True)
    parser.add_argument("--approval-file", type=Path)
    parser.add_argument("--export-root", type=Path, default=DEFAULT_EXPORT_ROOT)
    parser.add_argument("--visibility", choices=("private", "public"), default="private")
    parser.add_argument("--publish", action="store_true", help="Create/upload the HF repo after all gates pass.")
    parser.add_argument("--json", action="store_true", help="Print machine-readable preflight output.")
    args = parser.parse_args()

    package_dir = args.package_dir.resolve()
    phrase = approval_phrase(package_dir, args.repo_id)
    checks = check_package(package_dir, args.repo_id, export_root=args.export_root)
    if args.publish:
        checks.extend(check_approval(args.approval_file, phrase))

    result = summarize(checks)
    result.update(
        {
            "publish_requested": args.publish,
            "publish_action_performed": False,
            "repo_id": args.repo_id,
            "package_dir": str(package_dir),
            "required_approval_phrase": phrase,
            "visibility": args.visibility,
        }
    )

    if args.publish and result["ok"]:
        run_hf_publish(package_dir, args.repo_id, visibility=args.visibility)
        result["publish_action_performed"] = True

    if args.json:
        print(json.dumps(result, indent=2))
    else:
        print(f"Package: {package_dir}")
        print(f"Repo: {args.repo_id}")
        print(f"Publish requested: {str(args.publish).lower()}")
        for check in result["checks"]:
            prefix = "ok" if check["ok"] else "blocked"
            print(f"{prefix}: {check['message']}")
        print("\nRequired approval phrase:")
        print(phrase)

    return 0 if result["ok"] or not args.publish else 2


if __name__ == "__main__":
    raise SystemExit(main())
