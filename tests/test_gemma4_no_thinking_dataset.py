from __future__ import annotations

import json
import tempfile
import unittest
from pathlib import Path

import yaml

from scripts.materialize_gemma4_no_thinking_dataset import (
    EMPTY_THOUGHT_CHANNEL,
    materialize_dataset,
)
from scripts.validate_gemma4_no_thinking_dataset import validate_config, validate_dataset


def write_jsonl(path: Path, rows: list[dict]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text("".join(json.dumps(row) + "\n" for row in rows), encoding="utf-8")


class Gemma4NoThinkingDatasetTests(unittest.TestCase):
    def test_materializer_prefixes_assistant_turns_and_is_idempotent(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            source = root / "source"
            target = root / "target"
            write_jsonl(
                source / "train.jsonl",
                [
                    {
                        "id": "one",
                        "messages": [
                            {"role": "user", "content": "Call a tool."},
                            {"role": "assistant", "content": "<tool_call>{}</tool_call>"},
                        ],
                    },
                    {
                        "id": "two",
                        "messages": [
                            {"role": "user", "content": "Call again."},
                            {
                                "role": "assistant",
                                "content": f"{EMPTY_THOUGHT_CHANNEL}<tool_call>{{}}</tool_call>",
                            },
                        ],
                    },
                ],
            )

            summary = materialize_dataset(source, target)

            self.assertEqual(summary["train"]["rows"], 2)
            self.assertEqual(summary["train"]["assistant_messages_prefixed"], 1)
            rows = [json.loads(line) for line in (target / "train.jsonl").read_text().splitlines()]
            self.assertTrue(rows[0]["messages"][1]["content"].startswith(EMPTY_THOUGHT_CHANNEL))
            self.assertEqual(rows[1]["messages"][1]["content"].count(EMPTY_THOUGHT_CHANNEL), 1)

    def test_validator_rejects_missing_empty_channel_for_gemma4_config(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            data = root / "data"
            write_jsonl(
                data / "train.jsonl",
                [
                    {
                        "id": "bad",
                        "messages": [
                            {"role": "user", "content": "Call a tool."},
                            {"role": "assistant", "content": "<tool_call>{}</tool_call>"},
                        ],
                    }
                ],
            )
            config = root / "gemma4" / "scripts" / "train_config.yaml"
            config.parent.mkdir(parents=True, exist_ok=True)
            config.write_text(
                yaml.safe_dump(
                    {
                        "model": "google/gemma-4-26B-A4B-it",
                        "data": str(data),
                        "gemma4_no_thinking_empty_channel": True,
                    }
                ),
                encoding="utf-8",
            )

            errors = validate_config(config)

            self.assertTrue(any("missing Gemma 4 empty thought channel" in error for error in errors))

    def test_validator_accepts_materialized_dataset_and_metadata_flag(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            source = root / "source"
            target = root / "target"
            write_jsonl(
                source / "train.jsonl",
                [
                    {
                        "id": "ok",
                        "messages": [
                            {"role": "user", "content": "Call a tool."},
                            {"role": "assistant", "content": "<tool_call>{}</tool_call>"},
                        ],
                    }
                ],
            )
            materialize_dataset(source, target)

            self.assertEqual(validate_dataset(target), [])


if __name__ == "__main__":
    unittest.main()
