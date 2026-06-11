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

## 2026-05-26 Candidate-Scorecard Refresh

Another live Hugging Face API spot check was run while the larger direct MLX
`lm_eval` scorecard was executing.

- `Qwen3.7`: no Hugging Face model results were returned. Keep Qwen3.7
  watchlist-only until official open weights or a supported hosted workflow
  exists.
- `Qwen/Qwen3.6-35B-A3B`: the official repository remains the canonical
  frontier Qwen runtime/teacher candidate. Current community packaging is active,
  including `unsloth/Qwen3.6-35B-A3B-MTP-GGUF`, `byteshape/Qwen3.6-35B-A3B-MTP-GGUF`,
  and `mudler/Qwen3.6-35B-A3B-APEX-MTP-GGUF`; treat these as latency/runtime
  experiments only.
- `NousResearch/Hermes-4-14B`: the official Hermes 4 14B repository remains the
  smaller Hermes-aligned baseline. ONNX/GGUF/MLX variants are packaging
  candidates, not new fine-tune bases.
- `LiquidAI/LFM2-24B-A2B`: official GGUF, ONNX, and MLX quantized packages
  remain visible. Continue treating LFM2-24B as an efficient runtime/teacher
  lane rather than a local M1 fine-tune target.

## 2026-06-11 Refresh

Two weeks after the 2026-05-26 radar pass, the live Hugging Face/API and web
refresh changes the local priority order but does not change the Qwen3.7
guardrail.

### Decisions

- Keep `Qwen3.7` out of local runtime, training, Azure, GitHub, and Hugging Face
  publication lanes. Hugging Face API search returned one non-official
  `RscriptSQwen/Qwen3.7-plus` result with zero downloads, and no official
  `Qwen/Qwen3.7*` or `Qwen3.7-Max` open-weight model was verified. Web results
  still describe Qwen3.7/Qwen3.7-Max as closed or not-yet-open-weight.
- Promote `LiquidAI/LFM2.5-8B-A1B` to the next high-priority Mac-local runtime
  proof candidate. Liquid describes it as an 8B-total / 1B-active edge model for
  fast tool calling, with 128K context, day-one llama.cpp, MLX, vLLM, SGLang,
  ONNX, and LEAP support, and sub-6 GB laptop-class inference in Liquid's own
  testing. This is a runtime/baseline candidate first, not an immediate local
  fine-tune target until a Hermes prompt smoke and quality gate pass.
- Add Gemma 4 26B-A4B QAT/GGUF as a stronger local runtime proof candidate than
  the previous generic Gemma 4 GGUF watch item. Google published QAT Q4_0 GGUF
  packaging for Gemma 4, and Unsloth/Ollama packages are now visible. Treat this
  as LM Studio/Ollama/llama.cpp proof work, not a Mac M1 fine-tune.
- Add `Qwen/Qwen3-Coder-Next` as a cloud/specialist coding-agent baseline. It is
  open weight and architecturally relevant: 80B total / 3B active, hybrid
  Gated-DeltaNet, attention, and MoE, 256K context, and tool-call parser support
  through SGLang/vLLM. It is not a 32GB Mac fine-tune target.
- Add `Qwen/Qwen3-VL-8B-Instruct-GGUF` as the smaller Qwen multimodal runtime
  candidate for GUI/screenshot Hermes-agent experiments. Keep it after the text
  and mem0 lanes unless multimodal local tool use becomes the priority.
- Keep `Hermes-4-14B` and `Hermes-4.3-36B` in their previous roles. New June
  results are packaging updates, not a new Hermes base generation.
- Keep BitNet, Mamba-3, RWKV7, MiMo V2 Flash, and Qwen3-Next as specialist
  runtime lanes. Current results are interesting, but none should displace the
  immediate local LFM2.5/Gemma QAT/Qwen3.6/Hermes baseline queue without a
  runtime harness proof.

### Actionable Queue

| Priority | Candidate | First proof | Why now |
|---:|---|---|---|
| 1 | `LiquidAI/LFM2.5-8B-A1B` / `LiquidAI/LFM2.5-8B-A1B-GGUF` | MLX or llama.cpp smoke, then Hermes prompt smoke | New official edge-agent release; best fit for Mac-local tool-calling latency. |
| 2 | `google/gemma-4-26B-A4B-it-qat-q4_0-gguf` or `unsloth/gemma-4-26B-A4B-it-qat-GGUF` | LM Studio/Ollama/llama.cpp smoke | New QAT packaging may make the 26B-A4B lane more practical locally. |
| 3 | `Qwen/Qwen3-Coder-Next` | Azure/specialist runtime smoke | Strong open-weight coding-agent baseline with only 3B active parameters, but too large for Mac fine-tune. |
| 4 | `Qwen/Qwen3-VL-8B-Instruct-GGUF` | multimodal local runtime smoke | Smaller Qwen VL option for GUI/screenshot agent tasks. |
| 5 | `nvidia/Qwen3.6-35B-A3B-NVFP4` | Azure/NVIDIA runtime proof only | Newer NVIDIA packaging, not useful for M1 local execution. |

### Live API Highlights

- `LiquidAI/LFM2.5-8B-A1B`: modified `2026-06-10`; `LiquidAI/LFM2.5-Audio-1.5B-JP`
  modified `2026-06-11`; `LiquidAI/LFM2.5-8B-A1B-GGUF` modified `2026-05-29`.
- `google/gemma-4-26B-A4B-it`: modified `2026-06-03`;
  `google/gemma-4-26B-A4B-it-qat-q4_0-gguf` modified `2026-06-05`;
  `unsloth/gemma-4-26B-A4B-it-qat-GGUF` modified `2026-06-10`.
- `Qwen/Qwen3-Coder-Next`: remains the relevant Qwen subquadratic/hybrid coding
  candidate; `Qwen/Qwen3.6-35B-A3B` remains the canonical open Qwen frontier
  runtime/teacher lane, with `nvidia/Qwen3.6-35B-A3B-NVFP4` now visible as a
  cloud/NVIDIA packaging option.
- `Qwen/Qwen3-Embedding-0.6B`, `Qwen/Qwen3-Embedding-4B`,
  `Qwen/Qwen3-Embedding-8B`, `Qwen/Qwen3-Reranker-0.6B`,
  `Qwen/Qwen3-Reranker-4B`, and `Qwen/Qwen3-VL-*` embedding/reranker variants
  remain visible. The current mem0 lane should finish reranker prompt/latency
  work before acquiring more large retrieval models.

### 2026-06-11 Artificial Analysis Follow-Up

The Artificial Analysis small and tiny open-source leaderboards add several
missing candidates to the repo radar:

- Gemma 4 has more relevant sizes than the first June pass captured. Artificial
  Analysis ranks Gemma 4 31B, 26B A4B, 12B, E4B, and E2B among small/tiny open
  models. Hugging Face confirms official Google QAT GGUF packages for 31B, 26B
  A4B, 12B, E4B, and E2B, plus active Unsloth QAT GGUF mirrors. For this Mac,
  proof order should be E4B or 12B first, then 26B A4B, then 31B only if the
  QAT GGUF runtime is stable and memory headroom is acceptable.
- NVIDIA candidates are more prominent than the earlier model radar reflected.
  Artificial Analysis lists Nemotron Cascade 2 30B A3B, Nemotron 3 Nano 30B A3B,
  Nemotron 3 Nano Omni 30B A3B, Nemotron Nano 12B v2 VL, and Nemotron Nano 9B
  v2. Hugging Face confirms NVIDIA NVFP4/FP8/BF16 packages for the 30B A3B and
  VL families. These should be Azure/NVIDIA or specialist-runtime proofs first;
  community GGUF variants can be local experiments only after local Gemma/LFM
  priorities are clear.
- MiniCPM should be added as a real tiny local lane. Artificial Analysis ranks
  MiniCPM5-1B at the top of its tiny open-source board, and Hugging Face confirms
  `openbmb/MiniCPM5-1B`, official GGUF, official MLX, and SFT packages. This is
  a good low-risk Mac-local smoke candidate for fast Hermes utility prompts, but
  not a likely replacement for the current Qwen3 v4 strict tool-call adapter.
- The 1-bit lane remains BitNet-first. Hugging Face confirms
  `microsoft/bitnet-b1.58-2B-4T-gguf`, BF16, and base packages, plus a small MLX
  community conversion. Keep this as a specialist runtime/efficiency lane until
  the BitNet runtime proves actual local throughput and Hermes prompt stability.
- The combined Artificial Analysis tiny/small leaderboard is useful as a
  discovery page but not sufficient evidence for local open weights by itself.
  It surfaced current API-only rows such as Qwen3.7 Max/Plus alongside open
  rows, so every local track still needs a verified primary model repository or
  supported runtime package before promotion.

### Revised Local Proof Order

| Priority | Candidate | First proof | Reason |
|---:|---|---|---|
| 1 | `LiquidAI/LFM2.5-8B-A1B` / GGUF | MLX or llama.cpp smoke | Best new edge-agent fit. |
| 2 | `google/gemma-4-E4B-it-qat-q4_0-gguf` | llama.cpp / LM Studio / Ollama smoke | Smallest practical Gemma 4 QAT local proof. |
| 3 | `google/gemma-4-12B-it-qat-q4_0-gguf` | llama.cpp / LM Studio / Ollama smoke | Stronger Gemma 4 local baseline before 26B/31B. |
| 4 | `openbmb/MiniCPM5-1B` / GGUF / MLX | MLX or GGUF smoke | Fast tiny utility/runtime lane. |
| 5 | `google/gemma-4-26B-A4B-it-qat-q4_0-gguf` | llama.cpp / LM Studio smoke | Larger MoE/A4B Gemma candidate after smaller QAT proofs. |
| 6 | `microsoft/bitnet-b1.58-2B-4T-gguf` | BitNet/llama.cpp specialist smoke | 1-bit efficiency experiment. |
| 7 | `nvidia/NVIDIA-Nemotron-3-Nano-30B-A3B-NVFP4` | Azure/NVIDIA smoke | Cloud/specialist baseline; not a Mac-first lane. |

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
- Live Hugging Face API spot check on 2026-05-26 for `Qwen3.7`, `Qwen3.6-35B-A3B`, `Hermes-4-14B`, and `LFM2-24B-A2B`
- Live Hugging Face API searches on 2026-06-11 for `Qwen3.7`, `Qwen3.7-Max`, `Qwen4`, `Qwen3.6-35B-A3B`, `Qwen3-Next`, `Qwen3-Coder-Next`, `Hermes-4.3`, `Hermes-4.4`, `Hermes-5`, `Hermes-4-14B`, `Gemma 4 26B A4B`, `LFM2.5`, `LFM2-24B-A2B`, `LFM3`, `LFM2 ColBERT`, `RWKV7`, `Mamba-3`, `BitNet b1.58`, `MiMo V2 Flash`, `Qwen3 Embedding`, `Qwen3 Reranker`, and `jina embeddings v5 mlx`
- Live Hugging Face API searches on 2026-06-11 follow-up for `Gemma 4 31B`, `Gemma 4 12B`, `Gemma 4 E4B`, `Gemma 4 E2B`, `NVIDIA Nemotron 3 Nano 30B A3B`, `NVIDIA Nemotron Nano 9B V2`, `NVIDIA Nemotron Nano 12B v2 VL`, `MiniCPM5-1B`, `MiniCPM-V 4.6 1.3B`, `OpenBMB MiniCPM5`, `1bit LLM`, `1-bit LLM`, `BitNet 1.58`, and `BitNet b1.58`
- Web pages checked on 2026-06-11: Liquid AI LFM2.5-8B-A1B release blog, `LiquidAI/LFM2.5-8B-A1B`, Google Gemma 4 QAT release, `google/gemma-4-26B-A4B-it-qat-q4_0-gguf`, `Qwen/Qwen3-Coder-Next`, and `Qwen/Qwen3-VL-8B-Instruct-GGUF`
- Web pages checked on 2026-06-11 follow-up: Artificial Analysis small open-source leaderboard, Artificial Analysis tiny open-source leaderboard, Artificial Analysis combined tiny/small leaderboard, `google/gemma-4-31B-it-qat-q4_0-gguf`, `google/gemma-4-12B-it-qat-q4_0-gguf`, `google/gemma-4-E4B-it-qat-q4_0-gguf`, `openbmb/MiniCPM5-1B`, `nvidia/NVIDIA-Nemotron-3-Nano-30B-A3B-NVFP4`, and `microsoft/bitnet-b1.58-2B-4T-gguf`
- Qwen3.7-Max web refresh: TechNode, GIGAZINE, VentureBeat, BenchLM, and related coverage describe a proprietary/API-preview model, not an open-weight local artifact.
- Hugging Face pages checked on 2026-05-24: `SandLogicTechnologies/Hermes-4-14B-GGUF`, `mradermacher/Hermes-4-14B-GGUF`, `XiaomiMiMo/MiMo-V2-Flash`, `LiquidAI/LFM2-8B-A1B-GGUF`, and Hugging Face model search results for `Qwen3.7`.
