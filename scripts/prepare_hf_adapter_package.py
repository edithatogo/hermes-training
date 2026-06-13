#!/usr/bin/env python3
"""Prepare a local Hugging Face adapter upload package without publishing."""
from __future__ import annotations

import argparse
import json
import shutil
from datetime import UTC, datetime
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]


def copy_file(src: Path, dst: Path) -> dict[str, object]:
    if not src.exists():
        raise FileNotFoundError(src)
    dst.parent.mkdir(parents=True, exist_ok=True)
    shutil.copy2(src, dst, follow_symlinks=True)
    return {
        "source": str(src),
        "target": str(dst),
        "bytes": dst.stat().st_size,
        "source_is_symlink": src.is_symlink(),
        "resolved_source": str(src.resolve()),
    }


def prepare_package(
    adapter_dir: Path,
    model_card: Path,
    output_dir: Path,
    *,
    repo_id: str,
    publication_bundle: Path,
    extra_files: list[Path],
) -> dict[str, object]:
    output_dir.mkdir(parents=True, exist_ok=True)
    copied: list[dict[str, object]] = []
    copied.append(copy_file(adapter_dir / "adapters.safetensors", output_dir / "adapters.safetensors"))
    copied.append(copy_file(adapter_dir / "adapter_config.json", output_dir / "adapter_config.json"))
    copied.append(copy_file(model_card, output_dir / "README.md"))

    for extra in extra_files:
        copied.append(copy_file(extra, output_dir / "evidence" / extra.name))

    manifest = {
        "created_at": datetime.now(UTC).isoformat(),
        "repo_id": repo_id,
        "adapter_dir": str(adapter_dir),
        "adapter_dir_resolved": str(adapter_dir.resolve()),
        "model_card": str(model_card),
        "publication_bundle": str(publication_bundle),
        "output_dir": str(output_dir),
        "publish_action_performed": False,
        "copied_files": copied,
        "upload_command": f"hf upload {repo_id} {output_dir} . --repo-type model",
        "approval_phrase": f"I approve publishing HF adapter package {output_dir} to Hugging Face model repo {repo_id}.",
        "blocked_until": [
            "Hugging Face model card finalized",
            "Human publication approval recorded",
            "Standard benchmark stage target explicitly accepted or kept pilot-only",
        ],
    }
    (output_dir / "package-manifest.json").write_text(json.dumps(manifest, indent=2) + "\n", encoding="utf-8")
    return manifest


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--adapter-dir", type=Path, required=True)
    parser.add_argument("--model-card", type=Path, required=True)
    parser.add_argument("--publication-bundle", type=Path, required=True)
    parser.add_argument("--output-dir", type=Path, required=True)
    parser.add_argument("--repo-id", required=True)
    parser.add_argument("--extra-file", type=Path, action="append", default=[])
    args = parser.parse_args()

    manifest = prepare_package(
        args.adapter_dir,
        args.model_card,
        args.output_dir,
        repo_id=args.repo_id,
        publication_bundle=args.publication_bundle,
        extra_files=args.extra_file,
    )
    print(json.dumps(manifest, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
