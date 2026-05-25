from __future__ import annotations

import json
import tempfile
import unittest
from pathlib import Path

from scripts.check_conductor_track_consistency import parse_registry, validate


def write_track(root: Path, track_id: str, status: str, plan: str = "- [x] Task: Done\n") -> None:
    path = root / "conductor" / "tracks" / track_id
    path.mkdir(parents=True, exist_ok=True)
    (path / "metadata.json").write_text(json.dumps({"status": status}) + "\n", encoding="utf-8")
    (path / "plan.md").write_text(plan, encoding="utf-8")


class ConductorTrackConsistencyTests(unittest.TestCase):
    def test_completed_registry_requires_terminal_metadata_and_checked_plan(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            (root / "conductor").mkdir()
            (root / "conductor" / "tracks.md").write_text(
                "# Tracks\n\n"
                "## [x] Track: Demo\n"
                "*Link: [./tracks/demo/](./tracks/demo/)*\n",
                encoding="utf-8",
            )
            write_track(root, "demo", "implemented", "- [x] Task: Done\n- [ ] Follow-up\n")

            failures = validate(root)

            self.assertTrue(any("metadata status is implemented" in failure for failure in failures))
            self.assertTrue(any("unchecked item" in failure for failure in failures))

    def test_complete_or_completed_statuses_pass_for_completed_registry(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            (root / "conductor").mkdir()
            (root / "conductor" / "tracks.md").write_text(
                "# Tracks\n\n"
                "## [x] Track: One\n"
                "*Link: [./tracks/one/](./tracks/one/)*\n\n"
                "## [x] Track: Two\n"
                "*Link: [./tracks/two/](./tracks/two/)*\n",
                encoding="utf-8",
            )
            write_track(root, "one", "complete")
            write_track(root, "two", "completed")

            self.assertEqual(validate(root), [])

    def test_registry_parser_reads_track_links(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            (root / "conductor").mkdir()
            (root / "conductor" / "tracks.md").write_text(
                "# Tracks\n\n"
                "## [~] Track: Active Track\n"
                "*Link: [./tracks/active/](./tracks/active/)*\n",
                encoding="utf-8",
            )

            tracks = parse_registry(root)

            self.assertEqual(len(tracks), 1)
            self.assertEqual(tracks[0].title, "Active Track")
            self.assertFalse(tracks[0].completed)


if __name__ == "__main__":
    unittest.main()
