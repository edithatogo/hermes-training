#!/usr/bin/env python3
"""Convert an MLX LoRA adapter directory to a PEFT-style adapter directory."""
from __future__ import annotations

import argparse
import json
import re
from pathlib import Path
from typing import Any

import torch
from safetensors.torch import load_file, save_file


KEY_RE = re.compile(r"^model\.layers\.(\d+)\.(.+)\.lora_([ab])$")
DEFAULT_TARGET_MODULES = ["q_proj", "k_proj", "v_proj", "o_proj", "gate_proj", "up_proj", "down_proj"]


def load_config(path: Path) -> dict[str, Any]:
    return json.loads(path.read_text(encoding="utf-8"))


def convert_key(key: str) -> str:
    match = KEY_RE.match(key)
    if not match:
        raise ValueError(f"Unsupported MLX LoRA key: {key}")
    layer = int(match.group(1))
    module_path = match.group(2)
    side = match.group(3)
    peft_side = "A" if side == "a" else "B"
    return f"base_model.model.model.layers.{layer}.{module_path}.lora_{peft_side}.weight"


def convert_state(input_file: Path) -> tuple[dict[str, torch.Tensor], list[int], list[str]]:
    source = load_file(str(input_file))
    converted: dict[str, torch.Tensor] = {}
    layers: set[int] = set()
    modules: set[str] = set()
    for key, tensor in source.items():
        match = KEY_RE.match(key)
        if not match:
            raise ValueError(f"Unsupported MLX LoRA key: {key}")
        layer = int(match.group(1))
        module_path = match.group(2)
        side = match.group(3)
        module_name = module_path.rsplit(".", 1)[-1]
        converted[convert_key(key)] = tensor.T.contiguous()
        layers.add(layer)
        modules.add(module_name)
    ordered_modules = [module for module in DEFAULT_TARGET_MODULES if module in modules]
    ordered_modules.extend(sorted(modules.difference(ordered_modules)))
    return converted, sorted(layers), ordered_modules


def build_peft_config(
    mlx_config: dict[str, Any],
    base_model: str,
    target_modules: list[str] | None = None,
    layers: list[int] | None = None,
) -> dict[str, Any]:
    rank = int(mlx_config.get("lora_rank") or mlx_config.get("lora_parameters", {}).get("rank", 8))
    alpha = float(mlx_config.get("lora_scale") or mlx_config.get("lora_parameters", {}).get("scale", rank))
    dropout = float(mlx_config.get("lora_dropout") or mlx_config.get("lora_parameters", {}).get("dropout", 0.0))
    return {
        "alpha_pattern": {},
        "auto_mapping": None,
        "base_model_name_or_path": base_model,
        "bias": "none",
        "corda_config": None,
        "eva_config": None,
        "exclude_modules": None,
        "fan_in_fan_out": False,
        "inference_mode": True,
        "init_lora_weights": True,
        "layer_replication": None,
        "layers_pattern": "layers",
        "layers_to_transform": layers or [],
        "loftq_config": {},
        "lora_alpha": alpha,
        "lora_bias": False,
        "lora_dropout": dropout,
        "megatron_config": None,
        "megatron_core": "megatron.core",
        "modules_to_save": None,
        "peft_type": "LORA",
        "qalora_group_size": 16,
        "r": rank,
        "rank_pattern": {},
        "revision": None,
        "target_modules": target_modules or DEFAULT_TARGET_MODULES,
        "target_parameters": None,
        "task_type": "CAUSAL_LM",
        "trainable_token_indices": None,
        "use_dora": False,
        "use_qalora": False,
        "use_rslora": False,
    }


def convert_adapter(adapter: Path, output: Path, base_model: str, dry_run: bool = False) -> dict[str, Any]:
    input_file = adapter / "adapters.safetensors"
    input_config = adapter / "adapter_config.json"
    if not input_file.exists():
        raise FileNotFoundError(input_file)
    if not input_config.exists():
        raise FileNotFoundError(input_config)

    mlx_config = load_config(input_config)
    state, layers, target_modules = convert_state(input_file)
    peft_config = build_peft_config(mlx_config, base_model, target_modules, layers)
    report = {
        "status": "planned" if dry_run else "converted",
        "source_adapter": str(adapter.resolve()),
        "source_model": mlx_config.get("model"),
        "base_model_name_or_path": base_model,
        "output_dir": str(output),
        "input_weight_file": str(input_file.resolve()),
        "input_key_count": len(load_file(str(input_file))),
        "output_key_count": len(state),
        "layers": layers,
        "rank": peft_config["r"],
        "lora_alpha": peft_config["lora_alpha"],
        "target_modules": target_modules,
        "claim_boundary": "Experimental format conversion only; requires PEFT load and behavior smoke before benchmark use.",
    }
    if dry_run:
        return report

    output.mkdir(parents=True, exist_ok=True)
    save_file(state, str(output / "adapter_model.safetensors"))
    (output / "adapter_config.json").write_text(json.dumps(peft_config, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    (output / "conversion-manifest.json").write_text(json.dumps(report, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    return report


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--input", type=Path, required=True, help="MLX adapter directory containing adapters.safetensors")
    parser.add_argument("--output", type=Path, required=True, help="Output PEFT adapter directory")
    parser.add_argument("--base-model", default="Qwen/Qwen3-4B")
    parser.add_argument("--readme", type=Path, help="Optional README/model card to copy into the PEFT directory")
    parser.add_argument("--json-output", type=Path)
    parser.add_argument("--markdown-output", type=Path)
    parser.add_argument("--dry-run", action="store_true")
    args = parser.parse_args()

    report = convert_adapter(args.input, args.output, base_model=args.base_model, dry_run=args.dry_run)
    if args.readme and not args.dry_run:
        (args.output / "README.md").write_text(args.readme.read_text(encoding="utf-8"), encoding="utf-8")
    rendered = json.dumps(report, indent=2, ensure_ascii=False)
    if args.json_output:
        args.json_output.parent.mkdir(parents=True, exist_ok=True)
        args.json_output.write_text(rendered + "\n", encoding="utf-8")
    if args.markdown_output:
        args.markdown_output.parent.mkdir(parents=True, exist_ok=True)
        args.markdown_output.write_text(
            "\n".join(
                [
                    "# MLX LoRA To PEFT Conversion",
                    "",
                    "Status: `" + str(report["status"]) + "`",
                    f"Source adapter: `{report['source_adapter']}`",
                    f"Source model: `{report['source_model']}`",
                    f"PEFT base model: `{report['base_model_name_or_path']}`",
                    f"Output: `{report['output_dir']}`",
                    "",
                    "| Field | Value |",
                    "|---|---:|",
                    f"| Input keys | {report['input_key_count']} |",
                    f"| Output keys | {report['output_key_count']} |",
                    f"| LoRA rank | {report['rank']} |",
                    f"| LoRA alpha | {report['lora_alpha']} |",
                    f"| Layers | {', '.join(str(layer) for layer in report['layers'])} |",
                    "",
                    "## Claim Boundary",
                    "",
                    str(report["claim_boundary"]),
                    "",
                ]
            ),
            encoding="utf-8",
        )
    print(rendered)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
