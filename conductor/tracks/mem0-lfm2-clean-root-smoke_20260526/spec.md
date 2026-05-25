# Specification: mem0 LFM2 Clean-Root Extraction Smoke

Validate the current mem0 extractor model in the clean SSD-backed Ollama root
before treating LFM2 extraction as recovered for local Hermes-agent memory work.

Acceptance criteria:

- Pull `sam860/LFM2:2.6b` into
  `/Volumes/PortableSSD/Ollama/mem0-clean-models` without using the older
  hanging Ollama roots.
- Verify the model is visible through the clean-root Ollama daemon.
- Run a bounded generation smoke and the mem0 extraction benchmark.
- Store benchmark outputs under `/Volumes/PortableSSD/hermes-evals`.
- Record a repo-local report, benchmark index entry, candidate radar update,
  and handoff update.
- Keep `~/.mem0/config.json` unchanged.
