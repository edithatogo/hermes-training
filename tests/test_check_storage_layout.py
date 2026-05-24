from __future__ import annotations

import tempfile
import unittest
from pathlib import Path

from scripts.check_storage_layout import EXPECTED_ROOT_DIRS, check_layout


def make_valid_layout(root: Path) -> None:
    for name in EXPECTED_ROOT_DIRS:
        (root / name).mkdir(parents=True, exist_ok=True)

    canonical = root / "GitHub/llama.cpp-convert-tool"
    canonical.mkdir(parents=True)
    (canonical / ".git").mkdir()
    (canonical / "convert_hf_to_gguf.py").write_text("# converter\n", encoding="utf-8")

    legacy_parent = root / "hermes-tools"
    legacy_parent.mkdir()
    (legacy_parent / "llama.cpp").symlink_to(canonical, target_is_directory=True)


class CheckStorageLayoutTests(unittest.TestCase):
    def test_valid_layout_passes(self) -> None:
        with tempfile.TemporaryDirectory() as temp_dir:
            root = Path(temp_dir)
            make_valid_layout(root)

            errors, notes = check_layout(root, max_depth=4)

        self.assertEqual(errors, [])
        self.assertIn("ok: canonical llama.cpp checkout at GitHub/llama.cpp-convert-tool", notes)
        self.assertIn("ok: no git checkouts outside GitHub within depth 4", notes)

    def test_wrong_legacy_symlink_fails(self) -> None:
        with tempfile.TemporaryDirectory() as temp_dir:
            root = Path(temp_dir)
            make_valid_layout(root)
            wrong = root / "GitHub/wrong-llama"
            wrong.mkdir()
            legacy = root / "hermes-tools/llama.cpp"
            legacy.unlink()
            legacy.symlink_to(wrong, target_is_directory=True)

            errors, _ = check_layout(root, max_depth=4)

        self.assertTrue(any("legacy llama.cpp symlink points to" in error for error in errors))

    def test_stray_git_checkout_outside_github_fails(self) -> None:
        with tempfile.TemporaryDirectory() as temp_dir:
            root = Path(temp_dir)
            make_valid_layout(root)
            stray = root / "misplaced-project"
            stray.mkdir()
            (stray / ".git").mkdir()

            errors, _ = check_layout(root, max_depth=4)

        self.assertIn("git checkout outside GitHub: misplaced-project", errors)

    def test_missing_converter_fails(self) -> None:
        with tempfile.TemporaryDirectory() as temp_dir:
            root = Path(temp_dir)
            make_valid_layout(root)
            (root / "GitHub/llama.cpp-convert-tool/convert_hf_to_gguf.py").unlink()

            errors, _ = check_layout(root, max_depth=4)

        self.assertTrue(any("missing llama.cpp converter" in error for error in errors))


if __name__ == "__main__":
    unittest.main()
