from __future__ import annotations

import unittest
from unittest.mock import MagicMock, patch

from scripts.colab_adaptive_train_smoke import select_device


class ColabAdaptiveTrainSmokeTests(unittest.TestCase):
    def test_select_device_prefers_cuda(self) -> None:
        fake_torch = MagicMock()
        fake_torch.cuda.is_available.return_value = True
        fake_torch.cuda.get_device_name.return_value = "Tesla T4"
        fake_torch.device.side_effect = lambda name: name

        with patch.dict("sys.modules", {"torch": fake_torch}):
            selected = select_device()

        self.assertEqual(selected["backend"], "cuda")
        self.assertEqual(selected["device_name"], "Tesla T4")

    def test_select_device_falls_back_to_cpu_without_torch_xla(self) -> None:
        fake_torch = MagicMock()
        fake_torch.cuda.is_available.return_value = False
        fake_torch.device.side_effect = lambda name: name

        with patch.dict("sys.modules", {"torch": fake_torch, "torch_xla.core.xla_model": None}):
            selected = select_device()

        self.assertEqual(selected["backend"], "cpu")
        self.assertIn("torch_xla_error", selected)


if __name__ == "__main__":
    unittest.main()
