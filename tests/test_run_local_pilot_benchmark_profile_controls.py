from __future__ import annotations

import unittest
from pathlib import Path
import sys

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "scripts"))

from scripts.run_endpoint_pilot_benchmark import apply_system_affixes


class RunLocalPilotBenchmarkProfileControlsTests(unittest.TestCase):
    def test_system_affixes_update_existing_system_message(self) -> None:
        messages = [
            {"role": "system", "content": "Return tool calls."},
            {"role": "user", "content": "Do the task."},
        ]

        updated = apply_system_affixes(messages, "Prefix. ", " Suffix.")

        self.assertEqual(updated[0]["content"], "Prefix. Return tool calls. Suffix.")
        self.assertEqual(messages[0]["content"], "Return tool calls.")

    def test_system_affixes_insert_system_message_when_missing(self) -> None:
        updated = apply_system_affixes([{"role": "user", "content": "Do the task."}], "Prefix", "Suffix")

        self.assertEqual(updated[0], {"role": "system", "content": "PrefixSuffix"})


if __name__ == "__main__":
    unittest.main()
