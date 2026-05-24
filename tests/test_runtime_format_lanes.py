from __future__ import annotations

import tempfile
import unittest
from pathlib import Path

from scripts.create_runtime_format_lane_card import load_lanes, render_card
from scripts.validate_runtime_format_lanes import main as validate_lanes


class RuntimeFormatLaneTests(unittest.TestCase):
    def test_lanes_validate(self) -> None:
        self.assertEqual(validate_lanes(), 0)

    def test_render_card_includes_lane_contract(self) -> None:
        lane = load_lanes()["mlx-native"]

        with tempfile.TemporaryDirectory() as temp_dir:
            output_root = Path(temp_dir)
            card = render_card(
                lane,
                "Qwen/Qwen3-4B-MLX-4bit",
                "mlx-smoke",
                "mlx_lm.server --model Qwen/Qwen3-4B-MLX-4bit",
                "",
                "http://127.0.0.1:8080/v1",
                "test",
                "2026-05-24",
                output_root,
            )

        self.assertIn("Format lane: `mlx-native`", card)
        self.assertIn("MLX load or dry-run", card)
        self.assertIn("http://127.0.0.1:8080/v1", card)


if __name__ == "__main__":
    unittest.main()
