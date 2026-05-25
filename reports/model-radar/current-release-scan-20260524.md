# Current Release Scan

Date: 2026-05-24

## Summary

The scan found refreshed Qwen3.6, Gemma 4, Hermes 4, Unsloth, MiMo V2 Flash, LFM2, and RWKV runtime candidates. It did not find an official Qwen3.7 open-weight local model lane.

Live refresh during implementation also found no Hugging Face model results for `Qwen3.7` or `Qwen3.7-Max`. It did find API listings and news coverage for `Qwen3.7-Max`, but not open local weights. It also found additional downloadable Qwen3.6 IQ4_XS, MiMo V2 Flash, Hermes 4 14B, and LFM2 candidates, including LFM2-24B-A2B GGUF, ONNX, and MLX-bf16 variants. These should be treated as secondary runtime experiments after the primary Qwen3.6 Q4_K_M and Gemma 4 Q3_K_M proofs.

## Relevant Findings

| Candidate | Evidence | Track Treatment |
|---|---|---|
| `Qwen/Qwen3.6-27B` | Listed in current Hugging Face Qwen search results. | Runtime proof candidate. |
| `Qwen/Qwen3.6-35B-A3B` | Listed in current Hugging Face Qwen search results. | Frontier runtime/teacher candidate. |
| `unsloth/Qwen3.6-27B-UD-MLX-4bit` | Model card exposes MLX usage and Hermes Agent setup instructions. | Mac-local runtime proof candidate; size is still tight for 32GB. |
| `unsloth/Qwen3.6-27B-MTP-GGUF` and `unsloth/Qwen3.6-35B-A3B-MTP-GGUF` | Recent Unsloth GGUF listings. | LM Studio/Ollama runtime proof candidates. |
| `localweights/Qwen3.6-35B-A3B-MTP-IMAT-IQ4_XS-Q8nextn-GGUF` | Hugging Face API search result updated `2026-05-16`. | Secondary lower-memory Qwen3.6 runtime candidate after the canonical Q4_K_M proof. |
| `localweights/Qwen3.6-35B-A3B-MTP-IQ4_XS-GGUF` | Hugging Face API search result updated `2026-05-07`. | Secondary lower-memory Qwen3.6 runtime candidate; review quant quality and license before use. |
| `google/gemma-4-26B-A4B-it` | Current official Gemma 4 listing. | Multimodal MoE runtime/teacher candidate. |
| `unsloth/gemma-4-26B-A4B-it-GGUF` | Recent Unsloth GGUF listing. | LM Studio/Ollama runtime proof candidate. |
| `nvidia/Gemma-4-26B-A4B-NVFP4` | Quantized Gemma 4 listing. | Cloud/specialist runtime candidate. |
| `NousResearch/Hermes-4-14B` | Current NousResearch listing. | Primary Hermes baseline/runtime target. |
| `NousResearch/Hermes-4.3-36B` and GGUF variants | Current NousResearch listings. | Newer Hermes baseline; likely cloud or quantized runtime target. |
| `SandLogicTechnologies/Hermes-4-14B-GGUF` and `mradermacher/Hermes-4-14B-GGUF` | Hugging Face model cards expose Q4/Q5 or broader GGUF variants. | Alternate Hermes 4 quant sources; the current local SandLogic Q4_K_M artifact is already runtime-proven. |
| `unsloth/MiMo-V2-Flash-GGUF` and `mradermacher/MiMo-V2-Flash-i1-GGUF` | Hugging Face API search found GGUF variants for the recursive/reasoning MiMo V2 Flash lane. | Research runtime proof candidate after Mac-local Qwen3.6/Gemma priorities. |
| `XiaomiMiMo/MiMo-V2-Flash` | Model card describes a 309B-total, 15B-active MoE with hybrid attention and multi-token prediction. | Too large for this Mac as a first local target; keep as Azure/specialist or heavily quantized GGUF research lane. |
| `LiquidAI/LFM2-8B-A1B-GGUF` | Hugging Face model card reports GGUF availability for an 8B-total, 1B-active LFM2 MoE-style candidate. | Stronger LFM-family runtime candidate than the 2.6B helper if the GGUF fits and serves locally. |
| `LiquidAI/LFM2-24B-A2B`, `LiquidAI/LFM2-24B-A2B-GGUF`, `LiquidAI/LFM2-24B-A2B-ONNX`, `LiquidAI/LFM2-24B-A2B-MLX-bf16`, and `NexaAI/LFM2-24B-A2B-GGUF` | Live Hugging Face API refresh found multiple official and community runtime packages. | High-priority LFM runtime experiment; not a first 32GB Mac fine-tune target until artifact-size and endpoint proofs pass. |
| `RWKV/RWKV7-Goose-World3-2.9B-HF` | Current RWKV listing. | Research runtime proof candidate. |

## Qwen3.7 Guardrail

No official `Qwen/Qwen3.7-*` open-weight model or official Qwen repository result was verified. Keep Qwen3.7 out of local runtime, training, Azure, GitHub, and Hugging Face publication lanes until an official model card or repository exists. Treat `Qwen3.7-Max` as API-only/watchlist for now, not as a Mac-local model.

## 2026-05-25 Refresh

Live Hugging Face search was refreshed on 2026-05-25 for `Qwen3.7`,
`Qwen3.6`, `Hermes-4.3`, `LFM2-24B-A2B`, `BitNet`, and `RWKV-7`.

- `Qwen3.7`: no Hugging Face model results were returned. Keep the guardrail.
- `Qwen3.6`: community GGUF/merged variants remain active; the local project
  already has the Qwen3.6 35B-A3B Q4_K_M runtime proof and should not add a
  second Qwen3.6 download unless it closes a specific benchmark gap.
- `Hermes-4.3`: newer 36B GGUF/MLX variants are visible, including MLX 5-bit
  and Q4/Q5 GGUF variants. This remains a cloud or carefully selected local
  runtime-proof candidate, not an M1 fine-tune target.
- `LFM2-24B-A2B`: additional terminal-SFT, MXFP4-MoE, OpenVINO int4, and GGUF
  variants are visible. The current LFM2-24B-A2B Q4 acquisition should finish
  and prove before adding another LFM2 variant.
- `BitNet`: small and experimental variants are visible, but no current result
  changes the existing watchlist-only posture.
- `RWKV-7`: `rwkv7-g1` and 7.2B/13.3B GGUF variants are visible. These remain
  research-runtime lanes until a Hermes prompt harness exists.

## 2026-05-26 Refresh

Live search was refreshed on 2026-05-26 for `Qwen3.7`, Qwen3.6 GGUF/MLX,
Hermes 4.3, and LFM2-24B-A2B.

- `Qwen3.7`: no official open-weight Hugging Face model was verified. Search
  surfaced `qwen3.7-max` trace datasets, but those are generated traces rather
  than redistributable local weights. Keep Qwen3.7 watchlist-only for local
  runtime, training, Azure, GitHub, and Hugging Face publication lanes.
- `Qwen3.6`: additional GGUF and MLX variants are visible, including
  `batiai/Qwen3.6-35B-A3B-GGUF`, `opensota/Qwen3.6-35B-A3B-GGUF`, and
  `Brooooooklyn/Qwen3.6-35B-A3B-UD-Q6_K_XL-mlx`. The project already has a
  complete Qwen3.6 35B-A3B Q4_K_M llama.cpp runtime proof, so new Qwen3.6
  downloads should be justified by a specific benchmark or runtime gap.
- `Hermes-4.3`: official and community GGUF/MLX paths remain visible, including
  `NousResearch/Hermes-4.3-36B-GGUF`, `bartowski/NousResearch_Hermes-4.3-36B-GGUF`,
  and `NexVeridian/Hermes-4.3-36B-4bit`. Treat 36B as a runtime/teacher
  candidate, not a Mac-local fine-tune target.
- `LFM2-24B-A2B`: official and community quantized variants remain broad,
  including GGUF, ONNX, MLX 4/5/6/8-bit, and MXFP4-MoE variants. The local
  Q4_K_M proof is complete, so prefer benchmarking/alignment decisions over
  acquiring another LFM2 variant.

## 2026-05-26 mem0 Retrieval Refresh

Live Hugging Face API search was also refreshed for mem0-specific embedding,
reranking, and Apple Silicon paths.

- `BAAI/bge-m3` remains the validated stronger local embedding baseline. It has
  CPU/MPS smokes and a side-by-side mem0 config; it is still not the default.
- `jinaai/jina-embeddings-v5-omni-small-mlx` and related Jina v5 omni MLX
  variants appeared in current MLX embedding results. Add them as Mac-first
  acquisition/load-proof candidates after the BGE-M3/nomic comparison.
- `Qwen/Qwen3-Embedding-4B` remains the next high-quality dense embedding
  candidate, but its download and memory footprint are materially larger than
  BGE-M3.
- Smaller Qwen3 reranker packages are visible, including ONNX and GGUF
  `Qwen3-Reranker-0.6B` variants. These should be tested before the 4B reranker
  if the target is live mem0 latency.
- `flaglow/BAAI-bge-reranker-v2-m3-mlx-fp16` and
  `flaglow/BAAI-bge-reranker-v2-m3-mlx-mxfp8-8bit` appeared as fresh MLX
  reranker builds. They are good Apple Silicon reranker candidates for the
  expanded mem0 suite.
- `LiquidAI/LFM2-ColBERT-350M` remains the primary late-interaction retrieval
  candidate, but it requires a separate ColBERT index path rather than reuse of
  the dense Qdrant collections.

## 2026-05-26 Qwen3.6 MTP Packaging Delta

A follow-up refresh found one actionable delta after the prior radar cutoff:
Qwen3.6 GGUF packages with bundled MTP/self-speculative-decoding heads.

| Candidate | Delta | Action |
|---|---|---|
| `mudler/Qwen3.6-35B-A3B-APEX-MTP-GGUF` | APEX GGUF packaging bundles the MTP head and describes `--draft-mtp` support with a recent/patched llama.cpp runtime. | Add as a runtime latency experiment only. |
| `localweights/Qwen3.6-35B-A3B-MTP-IQ4_XS-GGUF` | IQ4_XS GGUF bundles the trunk plus NextN/MTP head and is positioned for 24GB-class inference with patched llama.cpp. | Add as a lower-memory runtime experiment only. |
| `byteshape/Qwen3.6-35B-A3B-MTP-GGUF` | ByteShape GGUF packaging describes ShapeLearn quantization with the MTP head bundled and `--spec-type draft-mtp` guidance. | Add as a runtime latency experiment only; do not treat as a fine-tune target. |

No official Qwen3.7 open-weight local model lane was verified in the same
refresh.

## 2026-05-26 Late Parallel Web Refresh

A late parallel web/Hugging Face refresh again found no official `Qwen3.7`
open-weight model lane suitable for local Mac training or publication.

Actionable additions:

- `mlx-community/Qwen3-VL-32B-Instruct-4bit` is a current MLX vision-language
  runtime candidate. The model card describes an MLX conversion from
  `Qwen/Qwen3-VL-32B-Instruct`, MLX/VLM usage, Hermes Agent local-server
  instructions, Apache-2.0 licensing, and a 19.6 GB 4-bit footprint. Treat it
  as a multimodal runtime smoke candidate only; do not fine-tune it locally on
  the 32 GB M1 Max lane.
- LiquidAI's Hugging Face organization continues to show active LFM2/LFM2.5
  releases, including small MLX/VL/ColBERT and audio candidates. These remain
  strong edge-runtime and retrieval/audio watchlist items, but they do not
  replace the current LFM2.5 1.2B local fine-tune lane without separate smoke
  and quality gates.
- `NousResearch/eval-Hermes-4-14B-reasoning` is useful as Hermes 4 evidence
  context, but it is a dataset/eval artifact rather than a local runtime model
  to acquire.

Decision: add no Qwen3.7 track. Keep Qwen3-VL 32B MLX as a future multimodal
runtime proof candidate after the current text/tool-call and mem0 gates are
stable.

## Sources

- Hugging Face Qwen model search: `https://huggingface.co/models?search=Qwen%2FQwen3`
- Hugging Face Unsloth organization model search: `https://huggingface.co/unsloth/models`
- Hugging Face Gemma 4 model search: `https://huggingface.co/models?search=google%2Fgemma-4-26B-A4B`
- Hugging Face NousResearch organization: `https://huggingface.co/NousResearch`
- Hugging Face RWKV organization: `https://huggingface.co/RWKV/models`
- Live Hugging Face API searches on 2026-05-24 for `Qwen3.7`, `Qwen3.7-Max`, `Qwen3.6-35B-A3B`, `LFM2-24B-A2B`, `Hermes-4-14B`, and `MiMo-V2-Flash GGUF`
- Live Hugging Face API searches on 2026-05-25 for `Qwen3.7`, `Qwen3.6`, `Hermes-4.3`, `LFM2-24B-A2B`, `BitNet`, and `RWKV-7`
- Live web/Hugging Face searches on 2026-05-26 for `Qwen3.7`, `Qwen3.6`, `Hermes-4.3`, and `LFM2-24B-A2B`
- Live Hugging Face API searches on 2026-05-26 for `Hermes 4 GGUF`, `Qwen3.6 GGUF`, `Qwen3 Embedding`, `Qwen3 Reranker`, `LFM2 GGUF`, `LFM2 ColBERT`, `embedding mlx`, and `reranker mlx`
- Hugging Face pages checked on 2026-05-26: `mudler/Qwen3.6-35B-A3B-APEX-MTP-GGUF` and `localweights/Qwen3.6-35B-A3B-MTP-IQ4_XS-GGUF`
- Hugging Face pages checked on 2026-05-26 late refresh: `mlx-community/Qwen3-VL-32B-Instruct-4bit`, `LiquidAI` organization models, `LiquidAI/LFM2.5-Audio-1.5B`, and `NousResearch/eval-Hermes-4-14B-reasoning`
- Qwen3.7-Max web refresh: TechNode, GIGAZINE, VentureBeat, BenchLM, and related coverage describe a proprietary/API-preview model, not an open-weight local artifact.
- Hugging Face pages checked on 2026-05-24: `SandLogicTechnologies/Hermes-4-14B-GGUF`, `mradermacher/Hermes-4-14B-GGUF`, `XiaomiMiMo/MiMo-V2-Flash`, `LiquidAI/LFM2-8B-A1B-GGUF`, and Hugging Face model search results for `Qwen3.7`.
