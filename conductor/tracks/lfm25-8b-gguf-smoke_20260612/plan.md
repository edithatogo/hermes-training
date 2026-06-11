# Plan: LFM2.5 8B A1B GGUF Runtime Smoke

## Phase 1: Acquisition

- [x] Task: verify `LiquidAI/LFM2.5-8B-A1B` and
  `LiquidAI/LFM2.5-8B-A1B-GGUF` with the Hugging Face API.
- [x] Task: acquire `LFM2.5-8B-A1B-Q4_K_M.gguf` to the SSD-backed Hugging Face
  cache.

## Phase 2: Runtime Smoke

- [x] Task: run bounded `llama-cli` attempts and identify that conversation mode
  is not the correct batch path.
- [x] Task: run bounded `llama-completion` generation smoke with
  `--no-conversation`.
- [x] Task: record load, generation, memory, and prompt-compliance behavior.

## Phase 3: Documentation And Validation

- [x] Task: update `MODEL_CANDIDATES.yaml`, `RUNTIME_FORMAT_PROOF_QUEUE.yaml`,
  `FUTURE_MODELS.md`, `HANDOFF.md`, and the hub track registry.
- [x] Task: run candidate, queue, unit, readiness, and whitespace checks.

## Health Check

- Target: >= 9.5 / 10
- Current estimate: 9.7 / 10
- Evidence: the Q4_K_M GGUF loads and generates through `llama-completion`
  from SSD-backed artifacts in a bounded run.
- Gaps: the response is not valid JSON for the Hermes prompt, so this is a
  runtime proof only and not a tool-call readiness claim.
