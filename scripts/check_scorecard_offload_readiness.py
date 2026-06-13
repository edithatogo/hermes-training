#!/usr/bin/env python3
"""Check whether a planned scorecard can be offloaded without changing model semantics."""
from __future__ import annotations

import argparse
import json
from datetime import UTC, datetime
from pathlib import Path
from typing import Any

import yaml


ROOT = Path(__file__).resolve().parents[1]
DEFAULT_PLAN = ROOT / "reports/benchmark/manifests/lm-eval-full-scorecard-plan-20260613.yaml"


def load_yaml(path: Path) -> dict[str, Any]:
    payload = yaml.safe_load(path.read_text(encoding="utf-8"))
    if not isinstance(payload, dict):
        raise ValueError(f"{path} must contain a mapping")
    return payload


def load_json(path: Path) -> dict[str, Any]:
    payload = json.loads(path.read_text(encoding="utf-8"))
    if not isinstance(payload, dict):
        raise ValueError(f"{path} must contain a JSON object")
    return payload


def classify_adapter(adapter_dir: Path, config: dict[str, Any]) -> dict[str, Any]:
    model_id = str(config.get("model", ""))
    files = sorted(path.name for path in adapter_dir.glob("*") if path.is_file())
    has_mlx_weights = "adapters.safetensors" in files
    has_peft_weights = "adapter_model.safetensors" in files
    has_peft_type = "peft_type" in config
    if has_peft_weights or has_peft_type:
        framework = "hf-peft"
    elif has_mlx_weights or "MLX" in model_id:
        framework = "mlx-native"
    else:
        framework = "unknown"
    return {
        "framework": framework,
        "model": model_id,
        "files": files,
        "has_mlx_weights": has_mlx_weights,
        "has_peft_weights": has_peft_weights,
        "has_peft_type": has_peft_type,
    }


def build_report(plan_path: Path, adapter_config_path: Path, created_at: str | None = None) -> dict[str, Any]:
    plan = load_yaml(plan_path)
    adapter_config = load_json(adapter_config_path)
    adapter_dir = adapter_config_path.parent
    adapter = classify_adapter(adapter_dir, adapter_config)
    cloud_backends = ("colab-cuda", "azure-cuda")
    exact_adapter_portable = adapter["framework"] == "hf-peft"
    status = "ready" if exact_adapter_portable else "blocked"
    blockers: list[str] = []
    if adapter["framework"] == "mlx-native":
        blockers.append("adapter is MLX-native; CUDA Colab/Azure cannot load it through standard Transformers/PEFT")
    elif adapter["framework"] == "unknown":
        blockers.append("adapter framework is unknown; exact offload semantics cannot be guaranteed")
    if plan.get("limit") is not None:
        blockers.append("scorecard plan is not a no-limit full selected-task run")
    if not str(plan.get("output_dir", "")).startswith("/Volumes/PortableSSD/hermes-evals/standard-benchmarks/lm-eval/"):
        blockers.append("scorecard output_dir is not SSD-backed")

    return {
        "created_at": created_at or datetime.now(UTC).isoformat(),
        "status": status if not blockers else "blocked",
        "plan": str(plan_path.relative_to(ROOT) if plan_path.is_relative_to(ROOT) else plan_path),
        "run_id": plan.get("run_id", ""),
        "candidate": plan.get("candidate", ""),
        "model": plan.get("model", ""),
        "adapter": str(adapter_config_path.parent.relative_to(ROOT) if adapter_config_path.parent.is_relative_to(ROOT) else adapter_config_path.parent),
        "adapter_classification": adapter,
        "cloud_backends": list(cloud_backends),
        "exact_adapter_portable": exact_adapter_portable,
        "blockers": blockers,
        "next_actions": (
            [
                "export or convert the MLX LoRA to a Hugging Face PEFT adapter with equivalent behavior",
                "or run the full scorecard on Apple Silicon with an explicit long-runtime window",
                "or benchmark only the base model/another portable candidate and label it separately",
            ]
            if blockers
            else ["dispatch the scorecard through Colab/Azure with the portable adapter package"]
        ),
        "claim_boundary": "No cloud scorecard claim until the exact adapter is portable or the report explicitly labels a different model.",
    }


def render_markdown(report: dict[str, Any]) -> str:
    blockers = report["blockers"] or ["none"]
    next_actions = report["next_actions"]
    lines = [
        f"# Scorecard Offload Readiness: {report['run_id']}",
        "",
        f"Date: {report['created_at']}",
        f"Status: `{report['status']}`",
        f"Candidate: `{report['candidate']}`",
        f"Model: `{report['model']}`",
        f"Adapter: `{report['adapter']}`",
        f"Adapter framework: `{report['adapter_classification']['framework']}`",
        f"Exact adapter portable: `{str(report['exact_adapter_portable']).lower()}`",
        "",
        "## Blockers",
        "",
    ]
    lines.extend(f"- {item}" for item in blockers)
    lines.extend(["", "## Next Actions", ""])
    lines.extend(f"- {item}" for item in next_actions)
    lines.extend(["", "## Claim Boundary", "", report["claim_boundary"], ""])
    return "\n".join(lines)


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--plan", type=Path, default=DEFAULT_PLAN)
    parser.add_argument(
        "--adapter-config",
        type=Path,
        default=ROOT / "gemma4/experiments/qwen3-4b-strict-toolcall-v4-targeted/lora_adapter/adapter_config.json",
    )
    parser.add_argument("--json-output", type=Path, default=ROOT / "reports/cloud/qwen3-v4-scorecard-offload-readiness-20260613.json")
    parser.add_argument("--markdown-output", type=Path, default=ROOT / "reports/cloud/qwen3-v4-scorecard-offload-readiness-20260613.md")
    parser.add_argument("--require-ready", action="store_true")
    parser.add_argument(
        "--created-at",
        help="Override the report timestamp for deterministic regeneration checks.",
    )
    args = parser.parse_args()

    report = build_report(args.plan, args.adapter_config, created_at=args.created_at)
    args.json_output.parent.mkdir(parents=True, exist_ok=True)
    args.markdown_output.parent.mkdir(parents=True, exist_ok=True)
    args.json_output.write_text(json.dumps(report, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    args.markdown_output.write_text(render_markdown(report), encoding="utf-8")
    print(json.dumps(report, indent=2, ensure_ascii=False))
    return 1 if args.require_ready and report["status"] != "ready" else 0


if __name__ == "__main__":
    raise SystemExit(main())
