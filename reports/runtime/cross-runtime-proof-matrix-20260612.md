# Cross-Runtime Proof Matrix - 2026-06-12

This report is the current execution checkpoint for `cross-runtime-proof-matrix_20260612`. It reconciles the active candidate radar, runtime format lanes, proof queue, local tool availability, and cloud/offload preflight state.

## Backend Preflight

| Backend | Current state | Evidence | Decision |
|---|---|---|---|
| MLX / MLX-LM | Available | `validate_readiness.py` imported `mlx` and `mlx_lm`; existing MLX proofs are recorded in `RUNTIME_FORMAT_PROOF_QUEUE.yaml`. | Preferred Mac/Metal lane for Qwen3 4B, Qwen3.5 helper models, Gemma E4B, MiniCPM5, Jina MLX, and other MLX-packaged candidates. |
| llama.cpp | Available | `llama-cli` and `llama-completion` are on PATH. Existing GGUF proofs cover Qwen3, Hermes 4 14B, Qwen3.6 35B, LFM2/LFM2.5, Gemma E2B, EXAONE, and BitNet/native-adjacent lanes. | Preferred direct GGUF proof path before Ollama/LM Studio packaging claims. |
| Ollama | Available | `ollama list` shows `hermes3:8b`, `sam860/LFM2:2.6b`, `nomic-embed-text:latest`, and `microsoft-bitnet-b1.58:2b`. | Stable daily mem0/extraction/embedder runtime; use for operational smoke, not as universal proof. |
| LM Studio | Available | `lms ls` shows `qwen3-4b-hermes-smoke` and `text-embedding-nomic-embed-text-v1.5`. | Useful desktop/OpenAI-compatible parity lane for Qwen3 Hermes and embedding endpoint checks. |
| Transformers / sentence-transformers | Available | `validate_readiness.py` imported `transformers`; mem0 evidence includes sentence-transformers BGE-M3 runs. | Use for embedding/reranker baselines and candidates without MLX/GGUF endpoint support. |
| ONNX / Transformers.js | Not promoted | Existing Qwen3 0.6B ONNX bridge evidence failed closed due unsupported wasm path and CPU timeout. | Keep ONNX/CoreML as follow-up only after bounded proof passes. |
| Colab CLI | Available and authenticated enough for session listing | `colab sessions` succeeded and reported no active sessions; CLI update available from 0.5.9 to 0.5.11. | First offload route for bounded, sanitized benchmark jobs; keep raw private fixtures local. |
| Azure | Installed but blocked | `az account show` reports `Please run 'az login' to setup account.` | No Azure GPU work until login, subscription, region, quota, and cost gates pass. |
| NVIDIA / NGC | Installed but unconfigured | `ngc config current` exposes only the default `format_type` table and no API-key/org/team state. | No NGC work until API key, entitlement, container/model availability, and license gates pass. |
| Kaggle | Not available on PATH | No `kaggle` executable was found in the PATH preflight. | Keep out of the active execution matrix until CLI/auth are installed and verified. |
| Hugging Face CLI | Available as `hf` | `hf` is on PATH; the deprecated `huggingface-cli` path should be avoided in new benchmark code. | Prefer `hf download` for future scripted acquisition. |

## Candidate Runtime Routing

| Candidate group | Primary route | Secondary route | State |
|---|---|---|---|
| `Qwen/Qwen3-4B-MLX-4bit` and strict Qwen3 adapter lane | MLX server / MLX direct | GGUF through llama.cpp, LM Studio, or Ollama after packaging | Main Mac/Metal adapter target remains runtime-proven; strict promotion depends on the documented prompt profile and benchmark gate. |
| Qwen3.5 tiny/helper lane (`0.8B`, `2B`) | MLX direct/loglikelihood | Colab for broader benchmark sweeps; GGUF/LM Studio only if packaging is acquired | Runtime proof exists, but strict BFCL/Hermes formatting remains failed; helper/extraction only. |
| `openbmb/MiniCPM5-1B-MLX` | MLX direct/loglikelihood | GGUF through llama.cpp after artifact acquisition | Runtime proof exists; strict Hermes formatting remains failed; helper/extraction only. |
| Hermes 4 / Harmonic / Hermes-Qwen3.5 GGUF lanes | llama.cpp or LM Studio | Colab/Azure for larger teacher comparisons after gates | Hermes 4 14B is runtime-proven; Hermes 4.3 and Harmonic/Hermes-Qwen3.5 GGUF lanes remain acquisition/proof follow-ups. |
| Qwen3.6 27B/35B and related MoE lanes | llama.cpp GGUF or MLX quant where explicitly acquired | Colab/Azure for large benchmark or teacher runs after auth/quota gates | Qwen3.6 35B Q4 GGUF is runtime-proven but failed strict Hermes; newer 27B/35B packaging remains proof work. |
| Gemma 4 E2B/E4B/12B/31B lanes | MLX where packaged; llama.cpp for GGUF | Colab/Azure/NGC for large or NVFP4 lanes after gates | E2B GGUF and E4B MLX have runtime proof; outputs are not strict Hermes-compliant yet. Larger Gemma/NVFP4 lanes remain gated. |
| LFM/LFM2.5 lanes | MLX and llama.cpp/GGUF | Liquid/LEAP only after native runtime proof | LFM2.5 1.2B MLX and LFM2.5 8B/LFM2 24B GGUF proofs exist; not promoted as strict Hermes defaults. |
| mem0 embedding/reranker lanes | Ollama, sentence-transformers, MLX | Colab only with sanitized fixtures | Nomic, BGE-M3, Jina MLX, Qwen3 0.6B reranker, and MLX BGE reranker evidence exists; default switch remains gated by mem0 migration policy. |
| Qwen3-VL / multimodal retrieval lanes | MLX/Transformers where available | Colab for sanitized multimodal fixtures | Candidate proof only; do not mix with text-only Hermes promotion gates. |
| NVIDIA Nemotron / NVFP4 support lanes | NGC/NVIDIA stack after API-key and entitlement proof | Azure only if license and quota allow | Current state is gated; no NGC execution should start from the local repo yet. |
| DeepSeek V4 Pro teacher/reference | Hosted API or specialist CUDA runtime | Colab only for sanitized comparison fixtures | Cloud-teacher lane only; do not attempt local fitting on the 32GB Mac. |
| NVIDIA LocateAnything-3B / Phi-4 multimodal helper lanes | Transformers or specialist multimodal runtime | Colab for sanitized visual helper fixtures | Support lanes for screenshot, GUI localization, and speech/image comparison, not Hermes chat targets. |
| Qwen3 ASR / TTS support lanes | Transformers, specialist speech runtime, or MLX where packaged | Colab for sanitized audio fixtures | Speech plumbing and voice-agent support only; keep outputs out of Hermes chat promotion claims. |
| Qwen3 Omni and multimodal support lanes | Transformers or specialist multimodal runtime | Colab for sanitized multimodal fixtures | Broad text/image/audio/video support lanes; benchmark as helpers or teachers, not chat defaults. |
| Jina v5 omni multimodal retrieval lanes | sentence-transformers / Transformers / MLX / browser WebGPU | Colab for sanitized cross-modal retrieval fixtures | Retrieval-first support lane for screenshots, documents, video, and audio search. |
| MiniCPM-o / MiniCPM-V support lanes | MLX, GGUF, or specialist multimodal runtime where packaged | Colab for sanitized multimodal fixtures | Local helper/runtime comparison lanes, useful for OCR and voice workflows. |
| Specialist research lanes: BitNet, RWKV, Mamba, RLM | Native runtime only | Colab/Azure only for isolated research benchmarks | BitNet native runtime proof exists; other specialist lanes remain blocked or watchlist until native runtime/artifacts are present. |

## Duplicate and Obsolete Queue Notes

- `qwen36-ktransformers-moe-proof` is not a duplicate of the completed Qwen3.6 GGUF proof. It remains blocked because GGUF/llama.cpp evidence does not prove KTransformers support.
- `lfm2-8b-a1b-leap-lfm-proof` is not replaced by MLX/GGUF LFM evidence. LEAP remains a separate blocked runtime lane.
- `qwen37-max-hosted-teacher-proof` remains API-only/watchlist because no verified open local weights are present.
- `north-mini-code-gguf-proof` remains blocked until llama.cpp or another runtime supports the `cohere2moe` GGUF architecture.
- ONNX Qwen3 0.6B reranker evidence remains failed closed; do not promote ONNX/CoreML until a bounded non-timeout proof exists.

## Execution Policy

1. Prefer Mac/Metal proofs for day-to-day local candidates when MLX or GGUF artifacts already exist.
2. Use Colab first for sanitized, bounded benchmark sweeps that are too expensive locally.
3. Use Azure only after `az login`, subscription, region, quota, and cost checks pass.
4. Use NVIDIA/NGC only after API-key, org/team, entitlement, and model/container checks pass.
5. Keep private mem0 fixtures, secrets, and restricted data out of cloud notebooks.
6. Treat runtime load success as runtime evidence only; promotion still requires task-specific benchmark gates.

## Health Check

- Target: >= 9.5 / 10
- Current estimate: 9.6 / 10
- Evidence: readiness validation passed; candidate checker passed; local backend preflights are documented; Colab/Azure/NGC gates are fail-closed; existing proof queue covers 20 runtime proof states.
- Gaps: Azure and NGC are still unavailable for execution; Kaggle is not installed; some candidate families remain proof work rather than completed runtime coverage.
- Decision: complete this matrix track as an operator-ready routing and proof-state artifact. Follow-on execution belongs in the candidate-specific and cloud orchestration tracks.
