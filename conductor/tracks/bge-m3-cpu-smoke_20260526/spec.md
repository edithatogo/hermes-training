# Specification: BGE-M3 CPU Smoke

Complete the BGE-M3 acquisition check by verifying whether the model can load
from the SSD-backed Hugging Face cache and run the local memory retrieval suite.

Acceptance criteria:

- Confirm BGE-M3 loads from `/Volumes/PortableSSD/huggingface`.
- Run a CPU sentence-transformers embedding benchmark.
- Record the result against the current `nomic-embed-text:latest` baseline.
- Preserve `mem0_nomic_768` as the default unless BGE-M3 clearly improves.
- Document any teardown or cache caveats.
- Validation passes.
