#!/usr/bin/env python3
"""Check the PortableSSD source/artifact layout used by Hermes work."""
from __future__ import annotations

import argparse
import os
from pathlib import Path


DEFAULT_ROOT = Path(os.environ.get("HERMES_STORAGE_ROOT", "/Volumes/PortableSSD"))
CANONICAL_LLAMA_REL = Path("GitHub/llama.cpp-convert-tool")
LEGACY_LLAMA_REL = Path("hermes-tools/llama.cpp")

EXPECTED_ROOT_DIRS = {
    "GitHub": "source repositories",
    "hermes-evals": "benchmark outputs",
    "hermes-exports": "model exports",
    "hermes-models": "model artifacts",
    "huggingface": "Hugging Face cache",
    "Ollama": "Ollama runtime state",
    "ollama-models": "Ollama model store",
}

SKIP_NAMES = {
    ".DocumentRevisions-V100",
    ".Spotlight-V100",
    ".TemporaryItems",
    ".Trashes",
    ".fseventsd",
    ".pnpm-store",
    "GitHub",
    "Movies",
    "OneDrive",
    "Ollama",
    "appdata",
    "cache",
    "homebrew-cache",
    "huggingface",
    "models",
    "ollama-models",
    "pip-cache",
    "toolchains",
    "uv-cache",
}


def rel(path: Path, root: Path) -> str:
    try:
        return str(path.relative_to(root))
    except ValueError:
        return str(path)


def find_git_dirs_outside_github(root: Path, max_depth: int) -> list[Path]:
    findings: list[Path] = []
    root_depth = len(root.parts)
    for current, dirs, _files in os.walk(root):
        current_path = Path(current)
        depth = len(current_path.parts) - root_depth
        if depth >= max_depth:
            dirs[:] = []
            continue
        dirs[:] = [
            name
            for name in dirs
            if name not in SKIP_NAMES and not (current_path == root and name == "GitHub")
        ]
        if ".git" in dirs:
            findings.append(current_path / ".git")
            dirs.remove(".git")
    return findings


def check_layout(root: Path, max_depth: int) -> tuple[list[str], list[str]]:
    errors: list[str] = []
    notes: list[str] = []

    if not root.exists():
        return [f"storage root does not exist: {root}"], notes

    for name, purpose in sorted(EXPECTED_ROOT_DIRS.items()):
        path = root / name
        if path.exists():
            notes.append(f"ok: {rel(path, root)} ({purpose})")
        else:
            errors.append(f"missing expected root: {rel(path, root)} ({purpose})")

    canonical = root / CANONICAL_LLAMA_REL
    legacy = root / LEGACY_LLAMA_REL
    converter = canonical / "convert_hf_to_gguf.py"

    if not (canonical / ".git").is_dir():
        errors.append(f"missing canonical llama.cpp git checkout: {canonical}")
    else:
        notes.append(f"ok: canonical llama.cpp checkout at {rel(canonical, root)}")

    if not converter.is_file():
        errors.append(f"missing llama.cpp converter: {converter}")
    else:
        notes.append(f"ok: llama.cpp converter at {rel(converter, root)}")

    if not legacy.is_symlink():
        errors.append(f"legacy llama.cpp path is not a symlink: {legacy}")
    elif legacy.resolve() != canonical.resolve():
        errors.append(f"legacy llama.cpp symlink points to {legacy.resolve()}, expected {canonical}")
    else:
        notes.append(f"ok: legacy llama.cpp symlink points to {rel(canonical, root)}")

    stray_git_dirs = find_git_dirs_outside_github(root, max_depth=max_depth)
    if stray_git_dirs:
        for git_dir in stray_git_dirs:
            errors.append(f"git checkout outside GitHub: {rel(git_dir.parent, root)}")
    else:
        notes.append(f"ok: no git checkouts outside GitHub within depth {max_depth}")

    return errors, notes


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--root", type=Path, default=DEFAULT_ROOT)
    parser.add_argument("--max-depth", type=int, default=4)
    args = parser.parse_args()

    errors, notes = check_layout(args.root.resolve(), args.max_depth)
    for note in notes:
        print(note)
    for error in errors:
        print(f"error: {error}")
    return 1 if errors else 0


if __name__ == "__main__":
    raise SystemExit(main())
