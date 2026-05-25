# Specification: BGE-M3 Expanded Retrieval Benchmark

Expand the mem0 embedding benchmark beyond the original three-case smoke suite
before considering BGE-M3 for any live collection migration.

Acceptance criteria:

- Add an expanded embedding retrieval suite covering direct recall, recency
  conflicts, distractor resistance, storage policy, runtime status, and
  publication gates.
- Validate the suite structurally in tests.
- Run BGE-M3 from the SSD Hugging Face cache against the expanded suite.
- Compare the result against the existing nomic baseline and record whether a
  fresh nomic re-run was possible.
- Keep benchmark outputs on `/Volumes/PortableSSD/hermes-evals`.
- Do not promote BGE-M3 unless it clearly improves quality and runtime.

