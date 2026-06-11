# Specification: North Mini Code GGUF Smoke

Prove whether the SSD-backed Mac runtime lane can acquire and load the
`unsloth/North-Mini-Code-1.0-GGUF` Q4_K_M artifact for use as a Hermes
code-specialist candidate.

Acceptance criteria:

- Acquire the GGUF through the SSD-backed Hugging Face cache.
- Run a bounded local `llama-cli` smoke with a tiny code prompt.
- Store raw logs under `/Volumes/PortableSSD/hermes-evals`.
- Track a markdown report under `reports/runtime`.
- Update the runtime proof queue and model candidate notes with the exact
  pass/blocker status.
- Do not promote the model unless a real runtime load and smoke response pass.
- Validation passes.
