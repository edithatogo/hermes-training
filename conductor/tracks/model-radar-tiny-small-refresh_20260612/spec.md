# Specification: Model Radar Tiny/Small Refresh

Refresh the model radar and mem0 candidate queue with the current tiny/small
open-weight frontier while keeping all new candidates behind runtime-proof,
license, and benchmark gates.

Acceptance criteria:

- Record the current small-model shortlist from live model sources and the
  Artificial Analysis tiny/small open leaderboard.
- Add verified Hugging Face IDs for Qwen3.5, Gemma 3n/4, Phi-4 mini, Granite
  4.1, EXAONE 4.0, LFM2.5, and North Mini Code candidates where they exist.
- Keep new candidates as runtime-smoke or local-finetune candidates only; do
  not promote them to defaults.
- Wire Jina v5 omni MLX embedding candidates into the mem0 queue with a
  dedicated MLX benchmark command and collection boundary.
- Ensure runtime proof queue, candidate queue generation, model-candidate
  schema checks, unit tests, and readiness validation pass.

