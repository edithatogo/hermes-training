import unittest

from scripts.check_mem0_model_candidates import validate_candidate


def candidate_with_status(status: str) -> dict[str, object]:
    return {
        "id": "example/model",
        "role": "reranker",
        "family": "example",
        "runtime": ["local-python"],
        "embedding_dims": None,
        "status": status,
        "first_gate": "smoke",
        "notes": "test candidate",
    }


class CheckMem0ModelCandidatesTests(unittest.TestCase):
    def test_validates_evidence_statuses(self) -> None:
        for status in (
            "benchmarked-cpu-mps-not-promoted",
            "live-read-wrapper-smoked",
            "working-default-clean-root-smoked",
        ):
            with self.subTest(status=status):
                self.assertEqual(validate_candidate(candidate_with_status(status)), [])

    def test_rejects_unknown_status(self) -> None:
        errors = validate_candidate(candidate_with_status("unknown-new-status"))

        self.assertIn("example/model: invalid status unknown-new-status", errors)


if __name__ == "__main__":
    unittest.main()
