from __future__ import annotations

import json
import tempfile
import unittest
from pathlib import Path

from scripts.prepare_dataset_publication_dry_run import (
    build_plan,
    collect_dataset_manifest,
    render_approval_artifact,
)


class DatasetPublicationDryRunTests(unittest.TestCase):
    def _write_dataset(self, root: Path) -> None:
        row = {
            "id": "synthetic-1",
            "source": "strict_tool_call_expansion_v1",
            "messages": [{"role": "user", "content": "Create a safe synthetic task."}],
        }
        (root / "train.jsonl").write_text(json.dumps(row) + "\n", encoding="utf-8")

    def _write_bundle(self, root: Path, dataset_dir: Path) -> None:
        root.mkdir(parents=True, exist_ok=True)
        source_audit = {
            "public_dataset_release": "blocked_pending_human_scope_approval",
            "unknown_sources": [],
        }
        overlap_audit = {
            "error_count": 0,
            "overlap": {"heldout_suite": {"user_prompt_overlap_count": 0}},
        }
        token_audit = {"model": "Qwen/Qwen3-4B-MLX-4bit", "data": str(dataset_dir)}
        (root / "cleaned-synthetic-source-audit.json").write_text(json.dumps(source_audit), encoding="utf-8")
        (root / "cleaned-synthetic-overlap-audit.json").write_text(json.dumps(overlap_audit), encoding="utf-8")
        (root / "cleaned-synthetic-token-audit.json").write_text(json.dumps(token_audit), encoding="utf-8")
        (root / "hf-dataset-card-draft.md").write_text("# Dataset Card\n", encoding="utf-8")
        (root / "dataset-publication-scope.md").write_text(
            "Public dataset publication remains blocked.\nExplicit human approval is required.\n",
            encoding="utf-8",
        )

    def test_collect_dataset_manifest_counts_rows(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            dataset_dir = Path(tmp)
            self._write_dataset(dataset_dir)

            manifest = collect_dataset_manifest(dataset_dir)

            self.assertEqual(manifest["rows"], 1)
            self.assertEqual(manifest["unique_ids"], 1)
            self.assertEqual(manifest["source_counts"]["strict_tool_call_expansion_v1"], 1)

    def test_plan_remains_dry_run_and_blocked(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            dataset_dir = root / "dataset"
            bundle_dir = root / "bundle"
            dataset_dir.mkdir()
            self._write_dataset(dataset_dir)
            self._write_bundle(bundle_dir, dataset_dir)

            plan = build_plan(dataset_dir, bundle_dir, "owner/dataset", "dry-run-test")

            self.assertEqual(plan["status"], "dry-run-only")
            self.assertFalse(plan["publish_actions_performed"])
            self.assertIn("explicit human approval", " ".join(plan["blockers"]))
            self.assertIn("owner/dataset", plan["approval_phrase"])

    def test_render_artifact_names_no_publish_commands(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            dataset_dir = root / "dataset"
            bundle_dir = root / "bundle"
            dataset_dir.mkdir()
            self._write_dataset(dataset_dir)
            self._write_bundle(bundle_dir, dataset_dir)
            plan = build_plan(dataset_dir, bundle_dir, "owner/dataset", "dry-run-test")

            artifact = render_approval_artifact(plan)

            self.assertIn("Publish actions performed: `false`", artifact)
            self.assertIn("hf repo create", artifact)
            self.assertIn("owner/dataset", artifact)


if __name__ == "__main__":
    unittest.main()
