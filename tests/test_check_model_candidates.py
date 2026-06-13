import unittest

from scripts.check_model_candidates import validate_entry


def valid_candidate(**overrides: object) -> dict[str, object]:
    candidate: dict[str, object] = {
        "id": "example/model",
        "family": "example",
        "tier": "test",
        "role": "local-runtime",
        "environment": "mac-mlx",
        "feasibility": "needs-runtime-proof",
        "parameters": "1B",
        "architecture": "decoder",
        "license": "unknown",
        "first_runtime": "mlx",
        "first_finetune": "none",
        "notes": "test candidate",
    }
    candidate.update(overrides)
    return candidate


class CheckModelCandidatesTests(unittest.TestCase):
    def test_accepts_valid_candidate(self) -> None:
        self.assertEqual(validate_entry(valid_candidate()), [])

    def test_rejects_invalid_role(self) -> None:
        errors = validate_entry(valid_candidate(role="unsupported"))

        self.assertIn("example/model: invalid role unsupported", errors)

    def test_requires_retrieval_role_for_retrieval_environment(self) -> None:
        errors = validate_entry(valid_candidate(environment="retrieval"))

        self.assertIn("example/model: retrieval environment requires retrieval role", errors)


if __name__ == "__main__":
    unittest.main()
