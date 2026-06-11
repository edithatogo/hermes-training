# Specification: Jina v5 Text-Matching MLX Proof

Prove the Jina v5 omni small text-matching MLX embedding lane on Apple Silicon
using SSD-backed model artifacts and the local mem0 retrieval smoke suite.

Acceptance criteria:

- Add direct Jina MLX model loading support for repos that ship `model.py`,
  `config.json`, `tokenizer.json`, and `model.safetensors` without `utils.py`.
- Run a bounded text-matching smoke over the 3-case mem0 embedding suite from
  SSD-backed artifacts.
- Record summary, run card, and mem0 index evidence without promoting Jina as
  the default embedder.
- Update runtime proof queue and mem0 candidate notes to reflect the proof.
- Validation passes.

