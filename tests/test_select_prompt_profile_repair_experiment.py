from __future__ import annotations

import unittest

from scripts.select_prompt_profile_repair_experiment import (
    ENDPOINT_PLACEHOLDER,
    build_selection,
    command_with_overrides,
    select_experiment,
)


def experiment(**overrides: object) -> dict[str, object]:
    data: dict[str, object] = {
        "candidate": "Qwen/Qwen3.5-0.8B",
        "variant": "strict-suffix-copy-exact",
        "runner": "local",
        "raw_output_promotion_allowed": True,
        "goal": "test",
        "promotion_boundary": "boundary",
        "command": "source scripts/env.sh\npython script.py",
    }
    data.update(overrides)
    return data


class SelectPromptProfileRepairExperimentTests(unittest.TestCase):
    def test_select_by_index_is_one_based(self) -> None:
        selected = select_experiment([experiment(candidate="a"), experiment(candidate="b")], None, None, 2)

        self.assertEqual(selected["candidate"], "b")

    def test_select_by_candidate_and_variant(self) -> None:
        selected = select_experiment(
            [experiment(candidate="a", variant="v1"), experiment(candidate="b", variant="v2")],
            "b",
            "v2",
            None,
        )

        self.assertEqual(selected["variant"], "v2")

    def test_endpoint_execute_blocks_without_base_url(self) -> None:
        item = experiment(runner="endpoint", command=f"run --base-url {ENDPOINT_PLACEHOLDER}")

        selection = build_selection(item, str(item["command"]), execute=True, confirm_local_run=True)

        self.assertEqual(selection["status"], "blocked")
        self.assertTrue(any("--base-url" in blocker for blocker in selection["blockers"]))

    def test_execute_requires_confirmation(self) -> None:
        selection = build_selection(experiment(), "python script.py", execute=True, confirm_local_run=False)

        self.assertEqual(selection["status"], "blocked")
        self.assertTrue(any("--confirm-local-run" in blocker for blocker in selection["blockers"]))

    def test_base_url_override_replaces_placeholder(self) -> None:
        command = command_with_overrides(f"run --base-url {ENDPOINT_PLACEHOLDER}", "http://127.0.0.1:8080/v1")

        self.assertIn("http://127.0.0.1:8080/v1", command)
        self.assertNotIn(ENDPOINT_PLACEHOLDER, command)


if __name__ == "__main__":
    unittest.main()
