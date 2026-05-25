# Runtime Inventory

Date: 2026-05-24

## Existing Local Evidence

| Runtime | Evidence | Status |
|---|---|---|
| Ollama installed models | `reports/runtime/ollama-installed-models-smoke/run-card.md`; live `/v1/models` check on 2026-05-24 | passed for `hermes3:8b` and `sam860/LFM2:2.6b`; `nomic-embed-text:latest` also visible |
| OpenAI normalizing proxy | `reports/runtime/openai-normalizing-proxy-ollama-smoke/run-card.md` | passed in front of Ollama with `hermes3:8b` |
| Qwen3 4B MLX server | `ollama-pack/runtime-card.qwen3-4b-mlx-smoke.md` | passed earlier on port `8088` |
| Qwen3 Q4_K_M GGUF direct llama.cpp | `RUNTIME_TARGETS.md`; `reports/runtime/llamacpp-qwen3-q4km-server-smoke-20260524.md` | passed direct validation and OpenAI-compatible `llama-server` smoke |
| Qwen3 Q4_K_M GGUF in LM Studio | `reports/runtime/lmstudio-qwen3-q4km-server-smoke-20260524.md` | passed with symbolic link to SSD artifact |
| Hermes 4 14B Q4_K_M GGUF direct llama.cpp | `reports/runtime/hermes4-14b-q4-llamacpp-smoke-20260524.md` | passed OpenAI-compatible `llama-server` smoke on port `8092` |
| Qwen3 4B MLX native current proof | `reports/runtime/qwen3-4b-mlx-native-proof-20260524.md` | passed OpenAI-compatible `mlx_lm.server` smoke on port `8094`; held-out strict pass `0.250`, so runtime proof only |
| Qwen3.6 35B-A3B Q4_K_M GGUF | `reports/runtime/qwen36-35b-a3b-q4-llamacpp-proof-20260525.md` | passed OpenAI-compatible `llama-server` smoke on port `8093`; held-out strict pass `0.000`, so runtime proof only |
| MLX server previous endpoint | live endpoint check on 2026-05-24 | old port `127.0.0.1:8088` not listening; current proof used `127.0.0.1:8094` |
| Qwen3 GGUF in Ollama | `ollama-pack/runtime-card.qwen3-4b-mlx-smoke.md`; `reports/runtime/ollama-qwen3-retest-gate-20260524.md` | blocked by unchanged Ollama `0.24.0` runtime after prior import/runtime instability |

Initial `lms` checks failed, but LM Studio `0.4.14+4` is now installed and `/opt/homebrew/bin/lms` points at the app-bundled CLI.

`llama-server` was built on 2026-05-24 from `/Volumes/PortableSSD/GitHub/llama.cpp`. The build required a local `<unordered_map>` include patch in `tools/server/server-http.h`; that external repo already had unrelated local changes and was not committed here.

## Existing SSD Artifacts

| Artifact | Path | Next Use |
|---|---|---|
| Qwen3 F16 GGUF | `/Volumes/PortableSSD/hermes-exports/ollama/qwen3-4b-hermes-smoke/qwen3-4b-hermes-smoke-f16.gguf` | fallback runtime proof |
| Qwen3 Q4_K_M GGUF | `/Volumes/PortableSSD/hermes-exports/ollama/qwen3-4b-hermes-smoke/qwen3-4b-hermes-smoke-q4_K_M.gguf` | LM Studio proof |
| Qwen3 merged dequantized export | `/Volumes/PortableSSD/hermes-exports/ollama/qwen3-4b-hermes-smoke/merged-dequantized` | export provenance only |

## Frontier Runtime Status

The original no-download scan on 2026-05-24 found no runnable Qwen3.6, Hermes 4,
Hermes 4.3, or Gemma 4 26B A4B chat artifact. That blocker has since been
partially closed through explicit SSD-backed acquisition and proof:

- Hermes 4 14B Q4_K_M is complete and runtime-proven.
- Qwen3.6 35B-A3B Q4_K_M is complete and runtime-proven, but failed the strict
  Hermes tool-call gate.
- LFM2 24B-A2B Q4_K_M is complete and runtime-proven, but remains below the
  Hermes-agent promotion gate.

Remaining frontier blockers:

- Hermes 4.3 36B remains acquisition/proof work.
- Gemma 4 26B A4B remains paused/resumable.
- Qwen3.7 remains watchlist-only because no official open-weight local artifact
  has been verified.

Exact GGUF acquisition targets and resumable SSD commands are recorded in
`reports/runtime/frontier-gguf-acquisition-20260524.md`.

## Frontier Artifact Acquisition

Artifact acquisition has now started under SSD-backed paths. Current status is tracked in `reports/runtime/frontier-artifact-acquisition-20260524.md`.

Hermes 4 14B Q4_K_M GGUF under `/Volumes/PortableSSD/hermes-models/frontier-gguf/hermes-4-14b-q4` is complete and runtime-proven. Qwen3.6 Q4_K_M under `/Volumes/PortableSSD/hermes-models/frontier-gguf/qwen3.6-35b-a3b-q4` is also complete and runtime-proven, but failed the strict Hermes-agent tool-call gate. LFM2 24B-A2B Q4_K_M under `/Volumes/PortableSSD/hermes-models/frontier-gguf/lfm2-24b-a2b-q4` is complete and runtime-proven with strict held-out pass `0.375`, so it remains a comparison/runtime lane rather than a Hermes-agent promotion candidate. Gemma 4 remains paused/resumable.
