from __future__ import annotations

import json
import tempfile
import unittest
from pathlib import Path

from scripts.build_blocked_track_matrix import backend_for_track, build_rows


class BuildBlockedTrackMatrixTests(unittest.TestCase):
    def test_build_rows_maps_blocked_track_to_backend(self) -> None:
        with tempfile.TemporaryDirectory() as tmpdir:
            root = Path(tmpdir)
            tracks_dir = root / "conductor" / "tracks"
            track_dir = tracks_dir / "example-hf-jobs_20260613"
            track_dir.mkdir(parents=True)
            (root / "conductor").mkdir(exist_ok=True)
            registry = root / "conductor" / "tracks.md"
            registry.write_text(
                "## [~] Track: Example HF Jobs\n"
                "*Link: [./tracks/example-hf-jobs_20260613/](./tracks/example-hf-jobs_20260613/)*\n",
                encoding="utf-8",
            )
            (track_dir / "metadata.json").write_text(
                json.dumps({"track_id": "example-hf-jobs_20260613", "status": "blocked"}) + "\n",
                encoding="utf-8",
            )
            (track_dir / "plan.md").write_text("- [ ] Task: Submit job\n", encoding="utf-8")
            checklist = root / "checklist.json"
            checklist.write_text(
                json.dumps(
                    {
                        "items": [
                            {
                                "backend": "hf_jobs",
                                "status": "blocked-insufficient-hf-credits",
                                "blocker": "credits",
                                "commands": ["hf jobs ps"],
                            }
                        ]
                    }
                )
                + "\n",
                encoding="utf-8",
            )

            rows = build_rows(registry, checklist)

        self.assertEqual(len(rows), 1)
        self.assertEqual(rows[0]["backend"], "hf_jobs")
        self.assertEqual(rows[0]["backend_status"], "blocked-insufficient-hf-credits")
        self.assertEqual(rows[0]["next_task"], "Submit job")

    def test_backend_for_track_maps_modal_and_lightning(self) -> None:
        self.assertEqual(
            backend_for_track("qwen3-v4-peft-modal-scorecard_20260613", "Qwen3 v4 PEFT Modal scorecard"),
            "modal",
        )
        self.assertEqual(
            backend_for_track(
                "qwen3-v4-peft-lightning-scorecard_20260613",
                "Qwen3 v4 PEFT Lightning scorecard",
            ),
            "lightning",
        )


if __name__ == "__main__":
    unittest.main()
