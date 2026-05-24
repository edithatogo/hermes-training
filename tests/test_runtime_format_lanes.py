from __future__ import annotations

import tempfile
import unittest
from pathlib import Path

from scripts.create_runtime_format_lane_card import load_lanes, render_card
from scripts.create_runtime_format_proof_queue import load_queue, output_path_for, validate_queue
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

    def test_proof_queue_matches_known_lanes(self) -> None:
        lanes = load_lanes()
        queue = load_queue()

        self.assertEqual(validate_queue(queue, set(lanes)), [])
        self.assertGreaterEqual(len(queue["proofs"]), len(lanes))

    def test_queue_output_path_uses_lane_and_proof_id(self) -> None:
        queue = load_queue()
        output = output_path_for(queue["proofs"][0], Path("/tmp/runtime-format-lanes"))

        self.assertIn(queue["proofs"][0]["lane_id"], output.parts)
        self.assertIn(queue["proofs"][0]["id"], output.parts)


if __name__ == "__main__":
    unittest.main()
