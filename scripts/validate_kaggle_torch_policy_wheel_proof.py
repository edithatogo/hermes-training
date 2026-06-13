#!/usr/bin/env python3
"""Validate the Kaggle P100 torch compatibility wheel proof."""
from __future__ import annotations

import argparse
import json
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[1]
DEFAULT_JSON = ROOT / "reports/cloud/kaggle-p100-torch-policy-wheel-proof-20260614.json"
DEFAULT_MD = ROOT / "reports/cloud/kaggle-p100-torch-policy-wheel-proof-20260614.md"
EXPECTED_WHEELS = {
    "torch": "torch-2.2.2+cu118-cp312-cp312-linux_x86_64.whl",
    "torchvision": "torchvision-0.17.2+cu118-cp312-cp312-linux_x86_64.whl",
    "torchaudio": "torchaudio-2.2.2+cu118-cp312-cp312-linux_x86_64.whl",
}


def display_path(path: Path) -> str:
    try:
        return str(path.relative_to(ROOT))
    except ValueError:
        return str(path)


def load_json(path: Path) -> dict[str, Any]:
    data = json.loads(path.read_text(encoding="utf-8"))
    if not isinstance(data, dict):
        raise ValueError(f"{path}: expected JSON object")
    return data


def validate_report(json_path: Path = DEFAULT_JSON, markdown_path: Path = DEFAULT_MD) -> list[str]:
    failures: list[str] = []
    if not json_path.exists():
        return [f"missing {display_path(json_path)}"]
    if not markdown_path.exists():
        failures.append(f"missing {display_path(markdown_path)}")
    data = load_json(json_path)
    if data.get("policy") != "p100-cu118":
        failures.append("wheel proof must target p100-cu118")
    if data.get("python_abi") != "cp312-cp312":
        failures.append("wheel proof must target Kaggle CPython 3.12 ABI")
    if data.get("platform") != "linux_x86_64":
        failures.append("wheel proof must target Linux x86_64")
    if data.get("index_url") != "https://download.pytorch.org/whl/cu118":
        failures.append("wheel proof must use the CUDA 11.8 PyTorch index")
    boundary = str(data.get("claim_boundary", ""))
    if "does not prove Kaggle runtime scoring" not in boundary:
        failures.append("wheel proof must preserve the non-scoring claim boundary")

    wheels = data.get("wheels", [])
    by_package = {row.get("package"): row for row in wheels if isinstance(row, dict)}
    for package, wheel in EXPECTED_WHEELS.items():
        row = by_package.get(package)
        if row is None:
            failures.append(f"missing wheel proof for {package}")
            continue
        if row.get("wheel") != wheel:
            failures.append(f"{package} wheel mismatch: {row.get('wheel')}")
        if row.get("present") is not True:
            failures.append(f"{package} wheel must be present")
    bulk = data.get("bulk_download_attempt", {})
    if isinstance(bulk, dict) and bulk.get("status") == "completed":
        failures.append("wheel proof should not imply a full bulk download is required")
    return failures


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--json-report", type=Path, default=DEFAULT_JSON)
    parser.add_argument("--markdown-report", type=Path, default=DEFAULT_MD)
    args = parser.parse_args()

    failures = validate_report(args.json_report, args.markdown_report)
    if failures:
        print("not ready: Kaggle P100 torch policy wheel proof")
        for failure in failures:
            print(f"- {failure}")
        return 1
    print("ready: Kaggle P100 torch policy wheel proof is current")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
