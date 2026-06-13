from __future__ import annotations

import json
import tempfile
import unittest
from pathlib import Path

import torch
from safetensors.torch import save_file

from scripts.convert_mlx_lora_to_peft import build_peft_config, convert_adapter, convert_key


class ConvertMlxLoraToPeftTests(unittest.TestCase):
    def test_convert_key_maps_mlx_to_peft(self) -> None:
        key = "model.layers.28.self_attn.q_proj.lora_a"

        self.assertEqual(
            convert_key(key),
            "base_model.model.model.layers.28.self_attn.q_proj.lora_A.weight",
        )

    def test_build_peft_config_uses_mlx_rank_scale(self) -> None:
        config = build_peft_config({"lora_rank": 8, "lora_scale": 16.0, "lora_dropout": 0.1}, base_model="base")

        self.assertEqual(config["peft_type"], "LORA")
        self.assertEqual(config["r"], 8)
        self.assertEqual(config["lora_alpha"], 16.0)
        self.assertEqual(config["lora_dropout"], 0.1)
        self.assertIn("q_proj", config["target_modules"])

    def test_convert_adapter_transposes_weights(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            adapter = root / "adapter"
            output = root / "peft"
            adapter.mkdir()
            (adapter / "adapter_config.json").write_text(json.dumps({"model": "mlx", "lora_rank": 2, "lora_scale": 4.0}), encoding="utf-8")
            save_file(
                {
                    "model.layers.28.self_attn.q_proj.lora_a": torch.arange(6, dtype=torch.float32).reshape(3, 2),
                    "model.layers.28.self_attn.q_proj.lora_b": torch.arange(8, dtype=torch.float32).reshape(2, 4),
                },
                adapter / "adapters.safetensors",
            )

            report = convert_adapter(adapter, output, base_model="base", dry_run=False)

            self.assertEqual(report["status"], "converted")
            self.assertEqual(report["input_key_count"], 2)
            self.assertTrue((output / "adapter_model.safetensors").exists())
            self.assertTrue((output / "adapter_config.json").exists())
