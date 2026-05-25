from __future__ import annotations

import json
import tempfile
import unittest
from pathlib import Path

from scripts.materialize_publication_dataset import materialize


def write_jsonl(path: Path, rows: list[dict]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text("\n".join(json.dumps(row) for row in rows) + "\n", encoding="utf-8")


class MaterializePublicationDatasetTests(unittest.TestCase):
    def test_filters_to_allowed_sources_and_renames_validation_split(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            input_dir = root / "input"
            output_dir = root / "output"
            for split in ("train", "val", "test"):
                write_jsonl(
                    input_dir / f"{split}.jsonl",
                    [
                        {"id": f"{split}-seed", "source": "strict_tool_call_seed", "messages": []},
                        {"id": f"{split}-synthetic", "source": "strict_tool_call_expansion_v1", "messages": []},
                        {
                            "id": f"{split}-synthetic-nothink",
                            "source": "strict_tool_call_expansion_v4_targeted+no_think_prompt",
                            "messages": [],
                        },
                    ],
                )

            summary = materialize(
                input_dir,
                output_dir,
                allowed_sources={"strict_tool_call_expansion_v1", "strict_tool_call_expansion_v4_targeted"},
                split_map={"train": "train", "val": "validation", "test": "test"},
            )

            self.assertEqual(summary["rows"], 6)
            self.assertEqual(summary["duplicate_id_count"], 0)
            self.assertEqual(summary["splits"]["validation"]["rows"], 2)
            self.assertTrue((output_dir / "validation.jsonl").exists())
            train_rows = [json.loads(line) for line in (output_dir / "train.jsonl").read_text().splitlines()]
            self.assertEqual([row["id"] for row in train_rows], ["train-synthetic", "train-synthetic-nothink"])


if __name__ == "__main__":
    unittest.main()
