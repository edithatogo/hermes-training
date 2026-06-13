from __future__ import annotations

import unittest

from scripts.colab_dispatch import extract_observed_runtime, parse_accelerators, slugify


class ColabDispatchTests(unittest.TestCase):
    def test_parse_accelerators_skips_tpu_without_opt_in(self) -> None:
        accelerators = parse_accelerators("gpu:T4,tpu:v5e1,gpu:L4", allow_tpu=False)

        self.assertEqual([(item.kind, item.name) for item in accelerators], [("gpu", "T4"), ("gpu", "L4")])

    def test_parse_accelerators_includes_tpu_with_opt_in(self) -> None:
        accelerators = parse_accelerators("gpu:T4,tpu:v5e1", allow_tpu=True)

        self.assertEqual([(item.kind, item.name) for item in accelerators], [("gpu", "T4"), ("tpu", "v5e1")])

    def test_extract_observed_runtime_from_colab_log(self) -> None:
        observed = extract_observed_runtime(
            '{"cuda_available": true, "cuda_device_name": "Tesla T4", "torch_xla_available": false, "backend": "cuda"}'
        )

        self.assertEqual(observed["cuda_available"], "true")
        self.assertEqual(observed["cuda_device_name"], "Tesla T4")
        self.assertEqual(observed["torch_xla_available"], "false")
        self.assertEqual(observed["training_backend"], "cuda")

    def test_extract_observed_runtime_reads_script_status(self) -> None:
        observed = extract_observed_runtime('{"status": "blocked", "decision": "MLX unavailable on CUDA"}')

        self.assertEqual(observed["script_status"], "blocked")
        self.assertEqual(observed["script_decision"], "MLX unavailable on CUDA")

    def test_slugify_keeps_run_id_filesystem_safe(self) -> None:
        self.assertEqual(slugify("Colab TPU/GPU smoke 2026"), "Colab-TPU-GPU-smoke-2026")


if __name__ == "__main__":
    unittest.main()
