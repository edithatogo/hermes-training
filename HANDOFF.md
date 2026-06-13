# Hermes Training Hub — Codex Handoff

> Last updated: 2026-06-13
> Pickup agent: Codex

## What Is Here

Canonical working root:

```text
/Volumes/PortableSSD/GitHub/hermes-training
```

| Repo | GitHub | Purpose |
|---|---|---|
| `gemma4/` | `github.com/edithatogo/hermes-gemma-lab` | Gemma/Qwen/Hermes 4 smoke configs and local fine-tune scripts |
| `lfm2/` | `github.com/edithatogo/hermes-lfm2-lab` | LFM/LFM2.5/LFM2/Ministral configs and local fine-tune scripts |
| `ollama-pack/` | `github.com/edithatogo/hermes-ollama-pack` | Ollama, experimental safetensors, GGUF, and Hermes runtime scripts |
| hub root | `github.com/edithatogo/hermes-training` | Platform lanes, model radar, requirements, runtime strategy, Azure scale-out, submodule map |

The hub root tracks the model repos as Git submodules. `.gitmodules` has been added to repair the previous gitlink-without-submodule metadata state.

Older notes may mention `/Users/doughnut/GitHub/hermes-training`; treat the SSD
path above as canonical for active work.

## 2026-05-24 Storage Layout Update

The SSD root migration pass found that most top-level `/Volumes/PortableSSD`
folders are intentional artifact, cache, runtime, app-state, or media roots and
should not be moved into `GitHub`.

The only misplaced Git checkout was migrated:

- canonical checkout: `/Volumes/PortableSSD/GitHub/llama.cpp-convert-tool`
- legacy compatibility path:
  `/Volumes/PortableSSD/hermes-tools/llama.cpp ->
  /Volumes/PortableSSD/GitHub/llama.cpp-convert-tool`

Keep the legacy symlink in place because older scripts and notes refer to
`hermes-tools/llama.cpp`.

Validation added:

- `scripts/check_storage_layout.py`
- `tests/test_check_storage_layout.py`
- `scripts/validate_readiness.py` now runs the storage check when the SSD root
  is present.
- `scripts/repo_status.sh` now prints a `== storage layout ==` section.

The nested `ollama-pack` checkout has one related local edit:
`ollama-pack/scripts/export_ollama.sh` now resolves llama.cpp in this order:

1. `HERMES_LLAMA_CPP`
2. `$HERMES_STORAGE_ROOT/GitHub/llama.cpp-convert-tool`
3. `$HERMES_STORAGE_ROOT/hermes-tools/llama.cpp`

Commit order if preserving this work:

1. Commit/push the nested `ollama-pack` change first.
2. Commit/push the hub root after the nested commit is available remotely.

Validation commands that passed:

```bash
scripts/repo_status.sh
./scripts/check_storage_layout.py --root /Volumes/PortableSSD
PYTHONPATH=. python3 -m unittest discover -s tests
./.venv/bin/python scripts/validate_readiness.py
```

The audit report is
`reports/storage/root-migration-audit-20260524.md`.

## Repo Hygiene Status

The nested repos are clean and pushed at the current submodule pointers:

- `gemma4`: `7b38e54` (`github.com/edithatogo/hermes-gemma-lab`)
- `lfm2`: `d6a3fc7` (`github.com/edithatogo/hermes-lfm2-lab`)
- `ollama-pack`: `c740e96` (`github.com/edithatogo/hermes-ollama-pack`)

Treat the current working tree as the source of truth and check status before
committing:

```bash
git status --short
git -C gemma4 status --short
git -C lfm2 status --short
git -C ollama-pack status --short
```

Do not modify nested repos just to clean the hub. Treat these as separate commit/push units and record pointer changes only after the nested commit exists on the remote.

## Current State

Complete:

- Proper Conductor structures now exist at the hub and nested track levels:
  - `conductor/`
  - `lfm2/conductor/`
  - `gemma4/conductor/`
  - `ollama-pack/conductor/`
- Repo scaffolding for current tracks.
- Real Hermes smoke dataset exists in the model tracks.
- Dataset pipeline writes train/val/test JSONL.
- MLX LoRA training script exists.
- Eval/comparison scripts exist.
- Hugging Face publishing scripts use the current `hf` CLI.
- Runtime docs cover Ollama launcher, experimental safetensors, GGUF, MLX, LM Studio, and specialist runtime handoff.
- Model radar includes Qwen3.5-27B, Qwen3.6-27B, Qwen3.6-35B-A3B, ManiacLabs Qwen3.6-35B 2-bit MLX packaging, Qwen3-4B-Instruct-2507, Qwen3-4B-Thinking-2507, Qwen3-Coder-Next / Qwen3-Coder-Next-GGUF, Qwen3-ASR-1.7B, Qwen3-TTS-12Hz-1.7B-VoiceDesign, Qwen3-Omni-30B-A3B-Instruct, Qwen3-Omni-30B-A3B-Captioner, Phi-4-multimodal-instruct, Qwen3-Embedding-0.6B, Qwen3-Reranker-0.6B, Qwen3-Embedding-4B, Qwen3-Reranker-4B, Harmonic-9B, Harmonic-Hermes-9B GGUF packaging plus mradermacher i1 GGUF, Hermes-Qwen3.5 SFT v7 packs, Hermes 4.3, Gemma 4 12B/26B/31B plus the Gemma 4 31B base repo, Gemma 4 12B Unsloth GGUF/QAT packaging plus community GGUF packagers, Gemma 4 QAT Mobile, MiniCPM-o 4.5, MiniCPM-V-4.6, MiniCPM-V-4.6-GPTQ, MiniCPM-V-4.6-Thinking, MiniCPM-V-4.6-BNB, MiniCPM-SALA, AgentCPM-Report, Nanbeige4.1-3B, DiffusionGemma plus NVIDIA/MLX packaging, Granite 4.1, Command A+, Step 3.7 Flash, DeepSeek-V4-Flash, Nemotron-Labs-Diffusion, Nex-N2-mini, Nemotron 3.5 safety/ASR support, Nemotron 3 Nano 4B with official GGUF and MLX packaging, the Nemotron frontier teacher/reward set, Nemotron 3 Ultra base/GenRM/speech checkpoints, NVIDIA physical-AI support lanes like `instant-nurec` and `omni-dreams-models`, LFM2.5, LFM2-ColBERT, Qwen3-Next, BitNet, BGE-M3, Jina embeddings, and watchlist entries for RWKV/Mamba-style families.
  The 2026-06-13 official-source addendum confirms Gemma 4 E2B/E4B/12B/26B-A4B/31B
  as real roadmap lanes, keeps Gemma 4 E4B/QAT in Mac-local prompt/profile repair,
  and records the empty thought channel requirement for Gemma 4 no-thinking
  fine-tune data. It also keeps Qwen3.7 watchlist-only because no official Qwen
  open-weight repository surfaced.
  The 2026-06-12 hybrid-packaging refresh adds `openbmb/MiniCPM-SALA`,
  `nvidia/Gemma-4-31B-IT-NVFP4`, and `deepseek-ai/DeepSeek-V4-Flash-Base` as
  specialist/runtime comparison lanes only; they are not default fine-tune
  targets.
- The packaging comparison lane also includes `bartowski/google_gemma-4-31B-it-GGUF`, which stays runtime-only until a real smoke proves it.
- Model radar now also includes the Qwen3-VL multimodal retrieval pair and the 2B/8B packaging lanes for screenshot, document-image, and video search workflows.
- Model radar now also includes the Jina v5 omni multimodal retrieval family plus MLX and ONNX browser/WebGPU packaging lanes.
- Gemma 4 no-thinking training prep is now enforced: nested `gemma4` commit
  `ba95083` materializes Gemma-specific empty-thought-channel datasets, retargets
  the Gemma 4 26B A4B experimental configs, and adds a nested Conductor track.
  The hub readiness gate validates the format through
  `scripts/validate_gemma4_no_thinking_dataset.py`.
- Colab accelerator routing is now explicit. `scripts/cloud_backend_preflight.py`
  and `reports/cloud/backend-unblock-checklist-20260613.md` expose the ladder
  `gpu:T4,gpu:L4,gpu:A100,tpu:v5e1`, but TPU remains opt-in and limited to
  adaptive scripts such as `scripts/colab_adaptive_train_smoke.py`; PEFT
  lm-eval, MLX scoring, and llama.cpp/GGUF endpoint pilots stay GPU or
  persistent-backend only.
- Runtime proof queue triage now separates known local runtime/converter support
  blockers into `runtime-support-upgrade`. Do not rerun those candidates until
  the relevant runtime, converter, or source package changes; use the
  `mac-runtime-proof` lane for candidates that can still produce new local
  evidence.
- Runtime proof queue priority now accounts for acquisition/storage footprint
  separately from MoE active parameters. An `80B total / 3B active` model can be
  inference-efficient but should not outrank smaller local artifacts for the
  next Mac proof.
- `hf-transformers` runtime proof queue entries now point to the bounded
  `scripts/run_transformers_pilot_benchmark.py` BFCL pilot with strict
  no-extra-tool-text scoring. This is an execution instruction only; it does not
  mean those candidates have passed.
- Runtime proof command generation now treats explicit environment as
  authoritative. `hf-transformers` candidates stay on the Transformers pilot
  path even when free-text runtime notes mention GGUF.
- mem0 embedding candidate command cards now select the broader
  `memory_retrieval_differentiation_suite.json` whenever the candidate gate or
  benchmarked status requires it. Baseline smoke candidates still use the
  smaller retrieval suite.
- mem0 `access-gated` and `runtime-blocked` candidates now render fail-closed
  unblock notes instead of known-failing benchmark commands. Recheck access or
  dependency/runtime changes before regenerating those command cards.
- Runtime proof endpoint command cards now use GGUF-specific acquisition text
  only for GGUF candidates. Non-GGUF endpoint candidates such as GPTQ packages
  receive runtime-neutral local-artifact instructions.
- Runtime proof endpoint command cards now include
  `--require-no-extra-tool-text` so queued endpoint proofs match the strict
  Hermes tool-call boundary instead of permissive parsed-tool scoring.
- Runtime proof MLX and prompt-profile repair command cards also include
  `--require-no-extra-tool-text`, so all generated local chat/tool-call proof
  commands now share the same strict scoring boundary.
- Jina MLX support-model proof command cards now rely on
  `scripts/run_jina_mlx_embedding_benchmark.py` to resolve the default
  SSD-backed repo directory, rather than emitting a literal `<repo-dir>`
  placeholder. Keep `--local-files-only` for queued proof runs after artifact
  acquisition; remove it only for a deliberate first acquisition after
  license/access checks.
- Runtime proof and mem0 candidate queue dependency-install command cards now
  use `./.venv/bin/python -m pip` instead of bare `python -m pip`, so optional
  embedding/reranker dependencies install into the same project virtualenv used
  by the benchmark scripts.
- Cloud offload preflight now includes Modal and Lightning as fail-closed
  candidate backends. Modal CLI auth is now complete for the `d-a-mordaunt`
  workspace, but Modal remains gated until free credit/grant proof, GPU policy,
  result persistence, and a guarded submitter exist. Lightning is blocked until
  login/teamspace, machine type, credits, and artifact recovery are proven. No
  remote jobs were submitted.
- HF Jobs scorecard dry-run payloads now expose `--python-executable`; the
  default remains `python`, and the tracked dry-run JSON records the interpreter
  while preserving the paid-compute and known-credit-blocker gates.
- Free-container account probe validation is now part of full readiness. It
  checks the Modal/Kaggle/Lightning sections, the no-job/no-resource/no-upload
  boundary, and obvious secret/execution-command leaks in
  `reports/cloud/free-container-account-probe-20260613.md`.
- Kaggle PEFT scorecard staging now has a tracked no-execution contract at
  `reports/cloud/qwen3-v4-peft-kaggle-contract-20260614.md`. Full readiness
  validates public inputs, dry-run/no-confirmation status, quota visibility,
  `/kaggle/working` output persistence, and the explicit operator approval
  boundary before any kernel push.
- Kaggle PEFT scorecard post-run ingestion now has a tracked fail-closed gate at
  `reports/cloud/qwen3-v4-peft-kaggle-result-ingest-20260614.md`. Full
  readiness accepts the current `pending_artifacts` state, but once a downloaded
  summary is provided it rejects limited, partial, timed-out, nonzero,
  missing-task, or non-SSD result artifacts before any benchmark claim.
- Cloud unblock reports now derive Kaggle's operator-facing status from the
  passed notebook contract and result-ingest gate. The active matrix shows
  Kaggle as `prepared-needs-run-approval` rather than still needing the notebook
  contract, while preserving the raw preflight report as account-state evidence.
- Active blocked-track matrix generation now maps future Modal and Lightning
  scorecard tracks to their backend-specific unblock checklist entries instead
  of `unknown`.
- Model radar now also includes the Gemma 4 31B QAT GGUF pack and the explicit MiniCPM-o 4.5 GGUF lane.
- Model radar now also includes the Unsloth and ggml-org Gemma 4 31B GGUF packs plus the official MiniCPM5-1B-GGUF lane.
- Hermes is now crystallized: `Qwen/Qwen3-4B-MLX-4bit` is the primary local adapter target, `Qwen/Qwen3.5-0.8B` and `Qwen/Qwen3.5-2B` are helper/extraction lanes, and `openbmb/MiniCPM5-1B` is the tiny support candidate. Hermes-4.3, Harmonic-9B, Harmonic-Hermes-9B, and Qwen3.6-27B remain teacher/runtime comparison lanes.
- The tiny helper/extraction lane is now explicitly codified as `tiny-helper-no-prefill` in `RUNTIME_PROMPT_PROFILES.yaml` for `Qwen/Qwen3.5-0.8B`, `Qwen/Qwen3.5-2B`, and `openbmb/MiniCPM5-1B-MLX`. Keep it raw and reproducible; do not treat it as Hermes-strict tool-call compliance.
- The tiny helper lane now has an explicit standard-benchmark matrix at `reports/benchmark/tiny-helper-standard-benchmark-matrix-20260612.md`. It is not a publication candidate yet because strict tool-call formatting and the broader standardized suite are still incomplete.
- The tiny helper execution track now has BFCL, IFEval, and coding pilot outputs for the smallest Qwen helper lane. Qwen3.5 0.8B remained at `0.000` on all three pilots, and the BFCL pilots for Qwen3.5 2B and MiniCPM5 1B MLX also stayed at `0.000`. Keep the lane blocked for promotion until the remaining blocked subsets are documented.
- The expanded Hermes-local 100-prompt pass is now recorded for `Qwen/Qwen3.5-0.8B`, `Qwen/Qwen3.5-2B`, and `openbmb/MiniCPM5-1B-MLX`. Qwen3.5 0.8B averaged `1.47s` and `78.09` words with `0.000` empty rate, Qwen3.5 2B averaged `2.32s` and `78.57` words with `0.000` empty rate, and MiniCPM5 1B MLX averaged `0.54s` and `74.30` words with `0.060` empty rate.
- mem0 and embedding are crystallized too: `BAAI/bge-m3` is the current retrieval baseline, `jinaai/jina-embeddings-v5-omni-small` and `jinaai/jina-embeddings-v5-omni-small-text-matching-mlx` are alternate lanes, `lmstudio-community/embeddinggemma-300m-qat-GGUF` is the leading 768-dim challenger but remains opt-in/non-default after copied live-store replay and rerank replay, and `Qwen/Qwen3-Embedding-4B` plus `Qwen/Qwen3-Reranker-4B` are follow-on candidates.
- Model radar now also includes `unsloth/North-Mini-Code-1.0-GGUF`; keep it as packaging evidence only until `cohere2moe` support lands in the runtime.
- Model radar now also includes `deepseek-ai/DeepSeek-V4-Pro`, `nvidia/LocateAnything-3B`, and `bosonai/higgs-audio-v3-tts-4b` as support-lane additions.
- Platform abstraction is now explicit: Mac/MLX is the local lane, Azure is the scale-out lane, retrieval is separate from chat SFT, and specialist runtimes require proof.
- Azure preflight exists at `scripts/azure_preflight.py`. It passed for
  `d.a.mordaunt@gmail.com` on `Azure for Students` on 2026-05-24, but the
  current 2026-06-13 refresh shows the CLI now needs `az login` before account
  and quota checks can be trusted again. Modern GPU quota was previously zero
  across sampled regions, so the Azure track remains fail-closed until login
  and quota are both resolved.
- Qwen3 v4 targeted is the current public/recommended strict Hermes tool-call adapter. It passes the held-out strict local tool-call suite at `1.000` with `/no_think` plus assistant prefill `<think>\n\n</think>\n\n`; publication evidence is in `reports/publication/qwen3-4b-strict-toolcall-v4-targeted/`.
- Qwen3 v5 pilot-polish is a documented non-promotion result. It improved the local BFCL-style pilot to `1.000`, but held-out strict pass regressed to `0.875`; keep v4 as the recommended/public adapter.
- V4/V5 pilot failure analysis is recorded in `reports/publication/qwen3-4b-strict-toolcall-v4-targeted/pilot-failure-analysis-20260526.md`. Any v6 attempt must start from V4 and keep held-out strict pass at `1.000`.
- The `ollama-pack` runtime packaging Conductor track is complete. It records current MLX, Ollama, GGUF/LM Studio, and blocked retest status without promoting unvalidated runtime surfaces.

Current gaps:

- Public dataset publication for the cleaned synthetic-only Qwen3 v4 strict
  tool-call dataset is complete. The approved local source at
  `/Volumes/PortableSSD/hermes-evals/datasets/qwen3-v4-synthetic-only-20260526`
  was published to
  `https://huggingface.co/datasets/edithatogo/qwen3-hermes-strict-toolcall-synthetic-v4`
  at remote SHA `727e7e4ecd781aca2f7506d4a8fc6d910f521d6d`. The live record is
  `reports/publication/qwen3-4b-strict-toolcall-v4-targeted/dataset-publication-live-20260612.md`.
- BGE-M3 is acquired and CPU/MPS-smoked from the SSD Hugging Face cache, but it is not promoted for mem0 defaults. On the expanded 12-case suite, BGE-M3 CPU reached top-1 `0.917` / recall@3 `1.000`; the current nomic default reached top-1 `0.833` / recall@3 `1.000` from the clean SSD Ollama root. The new `score_plus_created_at_rank_close_margin` reranker reached `1.000` on the BGE-derived suite and `0.917` on the nomic-derived suite, so the next mem0 improvement remains the read-only wrapper path, not a default embedder switch. See `reports/benchmark/mem0/bge-m3-expanded-retrieval-20260526.md` and `reports/benchmark/mem0/nomic-expanded-retrieval-20260526.md`.
- Jina v5 omni small MLX embedding candidates are now locally load-proven from SSD artifacts. The retrieval variant has a 1-case smoke, and the text-matching variant passed the 3-case mem0 embedding smoke at top-1 `1.000`, recall@3 `1.000`, MRR `1.000`, nDCG@3 `1.000`, 1024 dimensions, and p50 embedding latency `0.022s`. This is candidate evidence only; keep `nomic-embed-text:latest` as the default until a larger comparison and collection migration plan exists. See `reports/benchmark/mem0/run-cards/jina-mlx-text-matching-smoke-20260612c.md`.
- `Qwen/Qwen3.5-0.8B` is now SSD-acquired and MLX-load-proven on the Mac lane. The one-case direct loglikelihood smoke passed with greedy match `1.000`, score latency `1.037s`, and a 1.7G SSD cache footprint. Treat it as runtime/load evidence only; the next gate is deciding whether it is a Hermes helper, extractor, or prompt-format candidate before any training. See `reports/benchmark/mlx-loglikelihood/qwen35-08b-mlx-loglikelihood-smoke-20260612.md`.
- `Qwen/Qwen3.5-2B` is also SSD-acquired and MLX-load-proven. The same one-case direct loglikelihood smoke passed with greedy match `1.000`, score latency `0.769s`, and a 4.3G SSD cache footprint. Treat it as runtime/load evidence only; compare against 0.8B and the existing Qwen3 4B lane before training or promotion. See `reports/benchmark/mlx-loglikelihood/qwen35-2b-mlx-loglikelihood-smoke-20260612.md`.
- `openbmb/MiniCPM5-1B-MLX` is now SSD-acquired and MLX-load-proven. The one-case direct loglikelihood smoke passed with greedy match `1.000`, load latency `62.387s`, score latency `0.600s`, and a 592M SSD cache footprint. Its first 3-case BFCL-style local pilot scored `0.000`: the model reasoned about tools but did not emit strict Hermes tool-call JSON, and the invalid-tool case tried to call the forbidden deletion tool. Treat it as a tiny runtime/load candidate only; next gate is prompt-format repair or helper/extraction comparison against Qwen3.5 0.8B/2B. See `reports/benchmark/mlx-loglikelihood/minicpm5-1b-mlx-loglikelihood-smoke-20260612.md` and `reports/benchmark/local-pilots/minicpm5-1b-mlx-local-bfcl-pilot-20260612.md`.
- `ibm-granite/granite-4.1-3b` is now SSD-acquired and MLX-load-proven. The raw strict BFCL-style pilot scored `0.333`, then the opt-in `granite-native-tool-call` score-only normalizer raised the strict pilot to `0.667` without changing raw output. It is a useful helper/extraction comparison lane, not a strict Hermes default. See `reports/benchmark/local-pilots/granite4-1-3b-mlx-granite-native-normalized-strict-pilot-20260612.md`.
- Tiny MLX role-gate comparison is now fail-closed: MiniCPM5 1B MLX, Qwen3.5 0.8B, and Qwen3.5 2B all scored `0.000` on the raw 3-case BFCL-style local pilot. Qwen3.5 showed better invalid-tool refusal intent, but all three failed strict no-extra-text tool-call formatting. See `reports/benchmark/local-pilots/tiny-mlx-bfcl-role-gate-20260612.md`.
- The tiny helper/extraction lane is now codified as `tiny-helper-no-prefill` in `RUNTIME_PROMPT_PROFILES.yaml` for `Qwen/Qwen3.5-0.8B`, `Qwen/Qwen3.5-2B`, and `openbmb/MiniCPM5-1B-MLX`. The profile keeps the raw local endpoint untouched and records the lane as helper/extraction evidence only, not Hermes-strict tool-call compliance.
- Local pilot score wrappers now exist for prompt-repair experiments via `--score-prefix` and `--score-suffix`. A Qwen3.5 0.8B retry with `<tool_call>` prefill/wrapping still scored `0.000` and made the model echo tool metadata/function fragments, so simple prefill wrapping is not enough. See `reports/benchmark/local-pilots/qwen35-08b-local-bfcl-wrapper-pilot-20260612.md`.
- `CohereLabs/North-Mini-Code-1.0` has a completed blocked GGUF runtime proof. The 18G `unsloth/North-Mini-Code-1.0-GGUF` Q4_K_M artifact was acquired to `/Volumes/PortableSSD/huggingface/hub`, but Homebrew `llama.cpp` 9290 failed before generation with `unknown model architecture: 'cohere2moe'`. Do not retry the same path until the runtime explicitly supports `cohere2moe`; next options are a newer llama.cpp/LM Studio build or a safetensors/Transformers path. See `reports/runtime/north-mini-code-gguf-q4km-smoke-20260612.md`.
- `microsoft/bitnet-b1.58-2B-4T` now has a completed native runtime proof through `/Volumes/PortableSSD/GitHub/BitNet/bin/bitnet`. The SSD-backed 1.10 GiB I2_S model loaded and generated 16 tokens with exit code 0, 70.42s wall time, and 1.32 GB max RSS, but failed the JSON-only prompt-compliance smoke. A `-cnv` retry also produced non-compliant text and entered interactive mode, so it is not a batch benchmark path yet. Keep it as runtime evidence only until a non-interactive prompt wrapper and Hermes task smoke pass. See `reports/runtime/bitnet-b158-2b-native-smoke-20260612.md`.
- `LiquidAI/LFM2.5-8B-A1B-GGUF` now has a completed Mac GGUF runtime proof. The Q4_K_M artifact was acquired to the SSD-backed Hugging Face cache after a transient 429/backoff, and `llama-completion` build 9290 loaded and generated in a bounded run with exit code 0, load time `707.68 ms`, generation `109.59 tok/s`, and about `5.29 GB` max RSS. The output was not JSON-compliant, so keep it as an 8B LFM runtime baseline only. See `reports/runtime/lfm25-8b-a1b-q4km-llamacpp-smoke-20260612.md`.
- `google/gemma-4-E2B-it-qat-q4_0-gguf` now has a completed official small-Gemma GGUF runtime proof. The text GGUF was acquired to the SSD cache and `llama-completion` exited 0 in `2.703s` with about `3.53 GB` max RSS, but returned only end-of-text and emitted tool-response/EOG token warnings. Keep it runtime-only until a model-specific prompt profile or MLX package proof works. See `reports/runtime/gemma4-e2b-q4-llamacpp-smoke-20260612.md`.
- `google/gemma-4-E2B-it` now has official LiteRT and MLX packaging lanes in the live search. Use the base repo, LiteRT, and MLX packages as the smallest practical Gemma 4 helper/runtime comparison point, separate from the q4_0 GGUF proof.
- `google/embeddinggemma-300m` now has official LiteRT, MLX, and GGUF packaging lanes in the live search. Use it as the next Hermes memory/RAG comparison point rather than a chat lane.
- `mlx-community/gemma-4-E4B-it-qat-4bit` now has a completed MLX runtime and role-gate proof. The 6.4G SSD-cached package loaded through direct MLX scoring, but the one-case loglikelihood smoke had greedy match `0.000`, and the 3-case BFCL-style local pilot scored `0.000`. Outputs used Gemma-style thought/tool fragments rather than strict Hermes JSON; the invalid-tool case reasoned correctly but included the forbidden tool name. See `reports/benchmark/mlx-loglikelihood/gemma4-e4b-mlx-loglikelihood-smoke-20260612.md`.
- Local pilot scoring now has an opt-in Gemma native tool-call normalizer for runtime-adapter analysis only: `--score-normalizer gemma-native-tool-call`. It preserves raw responses and converts Gemma `{"function": ...}` fragments only for scoring. On Gemma 4 E4B it rescued 1/3 BFCL-style cases, improving score-only pass rate to `0.333`; this is not strict promotion evidence. See `reports/benchmark/local-pilots/gemma4-e4b-native-normalized-pilot-20260612.md`.
- Local and endpoint pilots now have `--require-no-extra-tool-text` for Hermes strict-format claims. Under a Gemma-specific profile, permissive parsed-tool scoring reached `0.333`, but no-extra-text scoring returned to `0.000` because the simple lookup still had Gemma thought text before the correct tool call. See `reports/benchmark/local-pilots/gemma4-e4b-strict-profile-no-extra-pilot-20260612.md`.
- `LGAI-EXAONE/EXAONE-4.0-1.2B-GGUF` now has a completed small-model GGUF runtime proof. The official Q4_K_M artifact was acquired to SSD after one resumable read timeout and `llama-completion` exited 0 in `2.039s` with about `0.94 GB` max RSS, but output repeated braces instead of JSON. The MLX 4-bit package is also acquired but blocked by a Transformers EXAONE4 config `ZeroDivisionError` during `mlx_lm.load`. See `reports/runtime/exaone4-12b-q4km-llamacpp-smoke-20260612.md`.
- `Qwen/Qwen3-Reranker-0.6B` is now acquired in the SSD Hugging Face cache and benchmarked through the causal-LM yes/no scorer. It reached top-1, recall@3, MRR, and nDCG@3 of `1.000` on the fixed 6-case suite and both BGE/nomic expanded 12-case derived suites. The live read-only wrapper also passed against real `mem0 cmd search` output with one returned memory, `3.920s` mem0 search latency, `0.216s` Qwen3 scoring latency, and `12.093s` one-shot total latency. The warm helper reduced the second service-backed live request to `4.112s` total with `0.119s` Qwen scoring. Multi-result replay through the live-wrapper abstraction reached top-1 `1.000` for warm Qwen3 on fixed, BGE-derived expanded, and nomic-derived expanded suites; the close-margin heuristic stayed at `0.917` on nomic-derived replay. The isolated live fixture then returned 3-5 candidates per query and reversed the Qwen promotion case: close-margin reached top-1 `1.000`, while warm Qwen3 matched vector at `0.667` and missed a recency lane. The public `onnx-community/Qwen3-Reranker-0.6B-ONNX` candidate remains an ONNX/Transformers.js runtime bridge task; the source HF model is the validated Python scorer. See `reports/benchmark/mem0/mem0-live-fixture-qwen3-multiretrieval-rerank-20260526.md`, `reports/benchmark/mem0/mem0-rerank-replay-comparison-20260526.md`, `reports/benchmark/mem0/qwen3-0-6b-live-rerank-smoke-20260526.md`, `reports/benchmark/mem0/qwen3-0-6b-warm-service-rerank-smoke-20260526.md`, `reports/benchmark/mem0/run-cards/rerank-qwen3-0-6b-fixed-20260526.md`, `reports/benchmark/mem0/run-cards/qwen3-0-6b-nomic-expanded-rerank-20260526.md`, and `reports/benchmark/mem0/run-cards/qwen3-0-6b-bge-expanded-rerank-20260526.md`.
- The read-only mem0 wrapper now exposes `score_plus_created_at_rank_close_margin` and live search smoke passed from a clean SSD-backed Ollama root at `/Volumes/PortableSSD/Ollama/mem0-clean-models`. The stale Qdrant lock holder was stopped, `nomic-embed-text:latest` was re-pulled into the clean root, and the wrapper returned a live result in `2.873s`. `sam860/LFM2:2.6b` was also pulled into the clean root; bounded `/api/generate` returned exactly `ok`, and `extraction-lfm2-2-6b-clean-root-20260526` passed 7/7 mem0 extraction cases with JSON validity `1.000`, forbidden hit rate `0.000`, empty-case pass `1.000`, p50 latency `0.874s`, and p95 latency `0.988s`. No mem0 defaults were changed. See `reports/benchmark/mem0/mem0-margin-rerank-live-smoke-20260526.md` and `reports/benchmark/mem0/extraction-lfm2-2-6b-clean-root-20260526.md`.
- Live multi-result comparison is now covered by an isolated non-sensitive fixture store, not by the default mem0 store. The default store still returned singleton results for broad probes, but the fixture used `MEM0_CONFIG_PATH`, an output-local Qdrant path, and a unique collection. Close-margin passed this gate; Qwen3 did not. `scripts/mem0_read.py` is the guarded read-only entrypoint for agents; it defaults to close-margin, keeps vector as rollback, and makes Qwen3 explicit/experimental with optional vector fallback. A 5-query UX latency probe passed with p50 `2.897s` and p95 `3.729s`, all singleton live-store results, so use it as an explicit memory-read tool or cached/batched path rather than an automatic every-turn prelude. The opt-in cache path also passed a 10-case cold/warm benchmark with 5 cache hits, cold p50 `2.904s`, and cache-hit p50 `0.000s`. `scripts/hermes_mem0_tool.py` now provides the explicit Hermes-agent command contract; live smoke passed with first-read latency `3.999s` and second-read cache-hit latency `0.000s`. No mem0 defaults were changed. See `reports/benchmark/mem0/live-multiretrieval-readiness-20260526.md`, `reports/benchmark/mem0/mem0-live-fixture-qwen3-multiretrieval-rerank-20260526.md`, `reports/benchmark/mem0/mem0-read-ux-close-margin-20260526.md`, `reports/benchmark/mem0/mem0-read-cache-close-margin-20260526.md`, and `reports/benchmark/mem0/hermes-mem0-tool-smoke-20260526.md`.
- The Hermes user plugin shim is installed and enabled at `~/.hermes/plugins/hermes-mem0-read`, with the tracked template in `mem0/integration/hermes-mem0-read`. `HERMES_PLUGINS_DEBUG=1 hermes tools list` exposes the `hermes_mem0` plugin toolset, and direct handler smoke through close-margin returned one memory in `3.970s` while remaining read-only and non-mutating. See `reports/benchmark/mem0/hermes-mem0-plugin-smoke-20260526.md`.
- MLX BGE reranking now has both the first bounded daily-use latency probe and
  a broader cold/warm subprocess probe. The original in-process `mlx-bge` probe
  stalled in artifact fetch/load for about seven minutes, so
  `scripts/run_mem0_read_latency_probe.py` supports `--subprocess-read` plus
  `--read-wall-timeout-s` to hard-bound model-load stalls. The broader
  2026-06-13 run completed 10/10 reads across five operational queries with no
  fallbacks, cold p50 `7.404s`, cache-hit p50 `4.552s`, and rerank p50
  `0.048s`; live results were singleton-only. Keep `mlx-bge` opt-in for
  deliberate Hermes/mem0 reads, not every-turn automatic preludes. See
  `reports/benchmark/mem0/mlx-bge-daily-use-latency-probe-20260526.md` and
  `reports/benchmark/mem0/mlx-bge-broader-cold-warm-latency-20260613.md`.
- Dataset publication also has a non-publishing dry-run generator at
  `scripts/prepare_dataset_publication_dry_run.py`. The dry run for the cleaned
  synthetic-only dataset produced
  `reports/publication/qwen3-4b-strict-toolcall-v4-targeted/dataset-publication-dry-run-20260526.md`
  and `.json`; the later live publication is recorded in
  `reports/publication/qwen3-4b-strict-toolcall-v4-targeted/dataset-publication-live-20260612.md`.
- `lm-eval-selected` was attempted against the live Qwen3 v4 MLX endpoint on `127.0.0.1:8080` and is blocked before scoring through that endpoint. The selected ARC/HellaSwag/TruthfulQA/GSM8K/Winogrande tasks require loglikelihood; `local-chat-completions` raises `NotImplementedError`, and a `local-completions` probe fails because `mlx_lm.server` returns logprobs in a shape that lacks legacy echoed `token_logprobs`. The direct MLX adapter in `scripts/run_mlx_lm_eval.py` subsequently scored both a selected-task `--limit 10` smoke and a larger `--limit 25` candidate-pilot scorecard. Treat the limit-25 run as bounded official-harness evidence, not a leaderboard or full selected-task score. The exact no-limit full-scorecard plan is now validator-enforced in `reports/benchmark/manifests/lm-eval-full-scorecard-plan-20260613.yaml` with a companion command card at `reports/benchmark/manifests/lm-eval-full-scorecard-plan-20260613.md`. See `reports/benchmark/lm-eval/qwen3-4b-v4-targeted-lm-eval-selected-smoke-20260526.md`, `reports/benchmark/lm-eval/qwen3-4b-v4-targeted-mlx-direct-lm-eval-selected-limit10-20260526.md`, and `reports/benchmark/lm-eval/qwen3-4b-v4-targeted-mlx-direct-lm-eval-selected-limit25-20260526.md`.
- The ONNX/Transformers.js bridge for `onnx-community/Qwen3-Reranker-0.6B-ONNX` was attempted and failed closed before promotion. Node/npm and the SSD tool root are present, no repo-local `node_modules` was created, the default `wasm` path was unsupported by the Node runtime, and the CPU retry with `max_length=512` timed out after `180.0s` before one fixed-suite case completed. See `reports/benchmark/mem0/qwen3-0-6b-onnx-transformersjs-bridge-20260526.md`.
- Standard benchmark coverage is now machine-checked for `qwen3-4b-strict-toolcall-v4-targeted`. The adapter remains local strict-gate ready with pilot-only benchmark positioning; public release is blocked. Official BFCL, full selected-task lm-eval, coding, safety, and RULER candidate suites are still missing for broad claims; the direct MLX lm-eval selected-task limit-10 smoke and limit-25 candidate-pilot scorecard are recorded separately as official-pilot evidence. See `reports/benchmark/standard-coverage/qwen3-v4-targeted-standard-coverage-20260526.md`.
- Large MoE/frontier configs are runtime/teacher experiments only; do not treat them as safe defaults for local training.
- The 2026-06-12 model radar refresh still found no verified open-weight Qwen3.7 lane. The major new actionable local candidates are `DJLougen/Harmonic-9B`, `DJLougen/Harmonic-Hermes-9B-GGUF`, `mradermacher/Harmonic-Hermes-9B-i1-GGUF`, `mkadrlik/Hermes-Qwen3.5-9B-SFT-v7`, `mkadrlik/Hermes-Qwen3.5-4B-SFT-v7`, `mkadrlik/hermes-Qwen3.5-2B-SFT-v7`, `mkadrlik/hermes-Qwen3.5-0.8B-SFT-v7-fresh`, `mkadrlik/Hermes-27B-SFT-v7`, `google/gemma-4-12B-it`, `google/gemma-4-12B`, `google/gemma-4-31B`, `unsloth/gemma-4-12b-it-GGUF`, `unsloth/gemma-4-12B-it-qat-GGUF`, `batiai/gemma-4-12B-it-GGUF`, `DuoNeural/OpenYourMind-Gemma4-12B-IT-Abliterated-GGUF`, `NousResearch/Hermes-4.3-36B`, `ManiacLabs/Qwen3.6-35B-A3B-2bit-maniac-nonstreaming`, `Qwen/Qwen3-4B-Instruct-2507`, `Qwen/Qwen3-4B-Thinking-2507`, `Qwen/Qwen3-Coder-Next`, `Qwen/Qwen3-Coder-Next-GGUF`, `Qwen/Qwen3-ASR-1.7B`, `Qwen/Qwen3-TTS-12Hz-1.7B-VoiceDesign`, `Qwen/Qwen3-Omni-30B-A3B-Instruct`, `Qwen/Qwen3-Omni-30B-A3B-Captioner`, `microsoft/Phi-4-multimodal-instruct`, `CohereLabs/cohere-transcribe-03-2026`, `nvidia/parakeet-tdt-0.6b-v3`, `Qwen/Qwen3-Embedding-0.6B`, `Qwen/Qwen3-Reranker-0.6B`, `Qwen/Qwen3-Embedding-4B`, `Qwen/Qwen3-Reranker-4B`, `Qwen/Qwen3.5-9B`, `nvidia/NVIDIA-Nemotron-3-Nano-4B-BF16`, `nvidia/NVIDIA-Nemotron-3-Nano-4B-GGUF`, `openbmb/MiniCPM-V-4.6-GPTQ`, `nvidia/NVIDIA-Nemotron-3-Ultra-550B-A55B-Base-BF16`, `nvidia/NVIDIA-Nemotron-3-Ultra-550B-A55B-GenRM`, `nvidia/nemotron-speech-streaming-en-0.6b`, `nvidia/instant-nurec`, and `nvidia/omni-dreams-models`. The new specialist-frontier additions are `CohereLabs/command-a-plus-05-2026-w4a4`, `stepfun-ai/Step-3.7-Flash`, `nex-agi/Nex-N2-mini`, and the Nemotron frontier teacher/reward set. The new support-lane additions are `nvidia/Nemotron-3.5-Content-Safety`, `nvidia/nemotron-3.5-asr-streaming-0.6b`, and the official Nemotron 3 Nano 4B GGUF/MLX packaging. The previously tracked `LiquidAI/LFM2.5-8B-A1B` / `LiquidAI/LFM2.5-8B-A1B-GGUF`, Gemma 4 QAT packaging from E2B/E4B through 31B, and `openbmb/MiniCPM5-1B` remain relevant. NVIDIA Nemotron 3 Nano / Nemotron Nano and `microsoft/bitnet-b1.58-2B-4T-gguf` are still explicit specialist runtime lanes. `Qwen/Qwen3-Coder-Next-GGUF` is now the strongest Qwen specialist runtime baseline for Hermes-agent workflows, while `Qwen/Qwen3-Embedding-0.6B` and `Qwen/Qwen3-Reranker-0.6B` are the current Qwen retrieval helpers for Hermes memory/RAG. `Harmonic-Hermes-9B` is now the most direct Hermes-style local runtime lane in the current search, and the Gemma 4 12B Unsloth GGUF/QAT lanes are now the freshest Mac-local packaging comparison points. They still belong in specialist runtime proof, not Mac-local fine-tune. See `reports/model-radar/current-release-scan-20260612.md`, `reports/model-radar/specialist-frontier-current-release-scan-20260612.md`, `reports/model-radar/nemotron-support-current-release-scan-20260612.md`, and `reports/model-radar/nemotron-frontier-current-release-scan-20260612.md`.
- Specialist runtime preflight is now explicit and no-download. KTransformers, LEAP, RWKV, and Mamba/SSM lanes remain blocked before smoke; BitNet has moved to completed native runtime proof only, with prompt-compliance failure still blocking Hermes use. Existing GGUF/MLX proofs do not count as specialist runtime proof for the remaining specialist lanes. See `reports/runtime/specialist-runtime-preflight-20260526.md` and `reports/runtime/bitnet-b158-2b-native-smoke-20260612.md`.
- Azure CLI is installed, but the current 2026-06-13 refresh shows
  `az account show` now requires `az login`. After login, rerun account,
  subscription, provider, workspace, and GPU quota checks before compute
  creation.
- Colab CLI is installed at `/Users/doughnut/.local/bin/colab` and upgraded to
  `0.5.11`; `colab sessions` currently reports no active sessions. Bounded
  PEFT pilots work, but no-limit Colab scorecard runs were pruned after a
  keepalive/session-permission failure, so they remain blocked for full
  benchmark coverage.
- LFM2.5 full-smoke training/evaluation is complete as a proof, but the adapter is not publishable. It trained for 200 iterations / 175,895 tokens with final validation loss 1.455 and peak memory 6.022 GB; evaluation on 100 prompts showed response collapse. See `lfm2/eval/lfm25-full-smoke-summary.md`.
- LFM2.5 1.2B Instruct smoke LoRA is now runtime-proven through `mlx_lm.server` using only SSD-cached artifacts. The server exposed the absolute snapshot path as the model ID, and the OpenAI-compatible smoke returned `{"ok": true}` in `378ms`. The direct `lfm2/scripts/evaluate.py` adapter load blocker is fixed in `lfm2` commit `3413720`, but a one-prompt direct eval still produced a non-compliant response, so this remains runtime/load proof only. See `reports/runtime/lfm25-1.2b-instruct-smoke-mlx-proof-20260526.md`.
- The OpenAI normalizing proxy now has a narrow `/v1/completions` passthrough and integer-to-boolean `logprobs` coercion for `mlx_lm.server`. A limited `lm_eval --model local-completions` rerun reached the endpoint but still failed before scoring because `mlx_lm.server` returns `logprobs.content` rather than legacy echoed `token_logprobs`; do not report lm-eval scores until a true loglikelihood evaluator exists. See `reports/benchmark/lm-eval/qwen3-4b-v4-targeted-lm-eval-selected-smoke-20260526.md`.
- Direct MLX prompt/continuation loglikelihood harnesses now exist at
  `scripts/run_mlx_loglikelihood_smoke.py` and `scripts/run_mlx_lm_eval.py`.
  The first no-download mock schema smoke produced SSD-backed artifacts under
  `/Volumes/PortableSSD/hermes-evals/standard-benchmarks/mlx-loglikelihood/mlx-loglikelihood-mock-smoke-20260526`.
  The `lm_eval` adapter scaffold self-test and dry-run pass. This is diagnostic
  plumbing. `scripts/run_mlx_lm_eval.py` now scores the selected lm-eval task
  documents from MLX logits directly; the first Qwen3 v4 run is a limit-10
  selected-task smoke, and the larger limit-25 run is a candidate-pilot
  scorecard rather than a full benchmark claim. See
  `reports/benchmark/lm-eval/mlx-loglikelihood-direct-smoke-20260526.md` and
  `reports/benchmark/lm-eval/qwen3-4b-v4-targeted-mlx-direct-lm-eval-selected-limit10-20260526.md` and
  `reports/benchmark/lm-eval/qwen3-4b-v4-targeted-mlx-direct-lm-eval-selected-limit25-20260526.md`.
- Qwen3 4B smoke training/evaluation is complete as a local MLX proof. It trained for 10 iterations / 2,889 tokens with final validation loss 2.386 and peak memory 3.944 GB; base and adapter both passed the response-collapse gate. See `gemma4/eval/qwen3-4b-smoke-summary.md`.
- Qwen3 4B MLX adapter runtime smoke passed through an OpenAI-compatible `mlx_lm.server` endpoint. See `ollama-pack/runtime-card.qwen3-4b-mlx-smoke.md`.
- Qwen3 4B fused safetensors export exists under `/Volumes/PortableSSD/hermes-exports/ollama/qwen3-4b-hermes-smoke`. Ollama experimental import succeeded into `/Volumes/PortableSSD/ollama-models`, but `/v1/chat/completions` failed with an Ollama MLX runner panic, so Ollama is not a validated runtime for this Qwen3 package yet.
- Qwen3 4B dequantized fused export and GGUF conversion are complete on the SSD:
  - `/Volumes/PortableSSD/hermes-exports/ollama/qwen3-4b-hermes-smoke/merged-dequantized`
  - `/Volumes/PortableSSD/hermes-exports/ollama/qwen3-4b-hermes-smoke/qwen3-4b-hermes-smoke-f16.gguf`
  - `/Volumes/PortableSSD/hermes-exports/ollama/qwen3-4b-hermes-smoke/qwen3-4b-hermes-smoke-q4_K_M.gguf`
- The Q4_K_M GGUF passed direct `llama-completion` validation and LM Studio smoke. Ollama GGUF import failed because the daemon dropped during model creation, so direct llama.cpp and LM Studio are the validated GGUF runtime paths for now.
- Populated publication/evidence bundles exist for Qwen3 smoke, failed Qwen3 attempts, Qwen3 v4 public adapter evidence, and Qwen3 v5 non-promotion evidence.
- Internal disk pressure has been reduced. `~/.gemini/antigravity/browser_recordings` was relocated to `/Volumes/PortableSSD/home-relocated/gemini-antigravity/browser_recordings` and symlinked back. Current 2026-06-12 check shows about 233 GiB free on `/` and about 252 GiB free on `/Volumes/PortableSSD`; keep model caches, benchmark outputs, and exports on the SSD.
- Roadmap regression and publication gate is reconciled in `reports/publication/roadmap-regression-publication-gate-20260612.md`. Treat benchmark/runtime reports as execution evidence, root and mem0 `MODEL_CANDIDATES.yaml` as structured state, `FUTURE_MODELS.md` as synthesis, and this handoff as the operator next-action summary. GitHub docs/code are publishable after validation, but Hugging Face datasets/models/adapters still require explicit artifact-scope and license approval.
- Cloud dynamic benchmark orchestration is now crystallized in
  `CLOUD_BENCHMARK_ORCHESTRATION.md` and `CLOUD_BENCHMARK_ORCHESTRATION.yaml`.
  `scripts/cloud_backend_preflight.py` records provider readiness without
  creating sessions or failing the run when a provider is blocked. Current
  2026-06-13 preflight: Colab ready with CLI `0.5.11` and no active sessions;
  HF Jobs authenticated but blocked by insufficient prepaid credits; Azure
  blocked until `az login` plus quota/cost checks; NGC installed but blocked
  until SSO/API key, org/team, Cloud Function GPU quota, registry access, and a
  benchmark container exist; Kaggle CLI `2.2.1` is authenticated as
  `edithatogo`, and read-only kernel listing works. The public `kaggle quota`
  command currently fails with a CLI parsing error, but the authenticated SDK
  fallback in `scripts/cloud_backend_preflight.py` returned GPU quota `108000s`
  total / `0s` used and TPU quota `72000s` total / `0s` used, resetting
  `2026-06-20T00:00:00Z`. The Kaggle notebook contract passed in
  `reports/cloud/qwen3-v4-peft-kaggle-contract-20260614.md`; it uses public
  inputs only, no private data upload, no `--limit`, and preserves the explicit
  `--execute --confirm-kaggle-run` operator boundary. The post-run ingest gate
  in `reports/cloud/qwen3-v4-peft-kaggle-result-ingest-20260614.md` is ready
  and currently `pending_artifacts`; after an approved run, download the
  `/kaggle/working` summary/results to the SSD and run
  `./.venv/bin/python scripts/validate_kaggle_result_ingest.py --summary-json <downloaded-summary> --no-allow-pending`
  before any benchmark claim. Kaggle still needs explicit run approval and
  artifact recovery. Modal is authenticated and now
  has a guarded dry-run submitter at `scripts/submit_modal_peft_scorecard.py`
  plus `reports/cloud/qwen3-v4-peft-modal-submit-dry-run-20260614.json`, but
  still needs free-credit/GPU-policy proof and explicit run approval. Lightning
  now has a guarded dry-run submitter at
  `scripts/submit_lightning_peft_scorecard.py` plus
  `reports/cloud/qwen3-v4-peft-lightning-submit-dry-run-20260614.json`, but
  remains blocked on login/teamspace, machine policy, zero-cost compute, and
  explicit run approval. Prepared reports and dry-runs are in
  `reports/cloud/backend-preflight-20260613.md`,
  `reports/cloud/qwen3-v4-peft-hf-jobs-scorecard-plan-20260613.md`,
  `reports/cloud/qwen3-v4-peft-kaggle-scorecard-plan-20260613.md`,
  `reports/cloud/qwen3-v4-peft-modal-scorecard-plan-20260614.md`,
  `reports/cloud/qwen3-v4-peft-lightning-scorecard-plan-20260614.md`, and
  `reports/cloud/qwen3-v4-peft-ngc-cloud-function-discovery-20260613.md`.
  A consolidated operator checklist is generated by
  `scripts/build_cloud_unblock_checklist.py` and tracked at
  `reports/cloud/backend-unblock-checklist-20260613.md`. The active blocked
  Conductor tracks are summarized by `scripts/build_blocked_track_matrix.py` in
  `reports/cloud/active-blocked-track-matrix-20260613.md`.
  Azure also has a Qwen3 v4 PEFT-specific guarded submitter and job template,
  recorded in `reports/cloud/qwen3-v4-peft-azure-scorecard-plan-20260613.md`;
  it remains blocked until login, quota, workspace, compute, environment, and
  cost gates pass.

## Next Actions

1. Re-test Ollama only after upgrading or replacing the current crashing Qwen3 GGUF/import path.
2. Use Colab first for sanitized bounded benchmark or smoke jobs via `scripts/colab_dispatch.py`; only attempt Azure after `az login`, `scripts/azure_preflight.py --check-quota`, and explicit cost approval pass.
3. Run broader official benchmark score cards for the v4 adapter only if the claim needs to go beyond local strict Hermes tool-calling and repo-native pilots; the coverage gate lists missing official BFCL, full selected-task lm-eval, coding, safety, and RULER candidate suites. The no-limit local MLX full selected-task attempt is recorded in `reports/benchmark/lm-eval/qwen3-4b-v4-targeted-mlx-direct-lm-eval-selected-full-20260613.md` and was stopped after 731.827 seconds with 0/5 tasks complete. A live T4 Colab portability probe is recorded in `reports/colab/qwen3-v4-colab-mlx-portability-20260613.md`; CUDA was available, but `mlx`/`mlx_lm` imports failed, so the exact MLX adapter cannot be scored on Colab as-is. The next full-scorecard step is a PEFT/Transformers adapter export or equivalent portable artifact, or an explicitly long Mac/MLX resume window. The proxy bridge alone is not enough for valid endpoint scores.
4. Publish no additional datasets until the exact artifact scope is explicitly approved and audited; the cleaned synthetic-only Qwen3 v4 dataset is already published and should not be republished unless its contents change.
5. Next local work should prioritize prompt/profile repair only for candidates with a concrete role: Gemma 4 E4B MLX, Gemma 4 31B-it, MiniCPM-o 4.5, MiniCPM-V-4.6, MiniCPM-V-4.6-Thinking, MiniCPM-SALA, AgentCPM-Report, Nanbeige4.1-3B, Granite 4.1 3B, LFM2.5 8B, MiniCPM5 1B, EXAONE 1.2B GGUF, Qwen3-4B-Instruct-2507, Qwen3-4B-Thinking-2507, Qwen3.5 0.8B/2B, Qwen3.5 9B, Qwen3.5 27B, and Qwen3.6-27B are all load-proven or verified candidates, but strict-format blocked or not yet proven. Gemma 4 E4B now has adapter-analysis evidence only: score-normalized BFCL pass is `0.333`, permissive parsed-tool profile pass is `0.333`, and no-extra-text Hermes-strict profile pass remains `0.000`. Granite 4.1 3B improved from `0.333` raw strict to `0.667` with the native score-only normalizer, but the parallel ticket-routing case still fails. MiniCPM5-1B should move only to prompt-format repair or helper/extraction comparison against Qwen3.5 0.8B/2B. LFM2.5 8B is GGUF load/generation proven but JSON-blocked. EXAONE 1.2B is GGUF runtime-proven but JSON-blocked, while MLX is config-blocked. Use Hermes 4.3, Qwen3-Coder-Next-GGUF, Qwen3.6-27B, Gemma 4 12B/31B, NVIDIA Gemma 4 31B NVFP4, OpenBMB AgentCPM-Report, NVIDIA Nemotron-Labs-Diffusion, Qwen3.6, LFM2-24B, NVIDIA Nemotron Ultra, DeepSeek-V4-Flash, DeepSeek-V4-Flash-Base, and BitNet as comparison/specialist baselines before attempting more local fine-tunes. For BitNet specifically, the next step is a non-interactive prompt wrapper plus Hermes extraction/tool-call smoke, not another raw `-cnv` run. For North Mini Code, wait for `cohere2moe` support in llama.cpp/LM Studio or switch to a safetensors/Transformers path. The follow-on execution lane is `conductor/tracks/tiny-helper-standard-benchmark-execution_20260612/`.
6. If wiring mem0 into Hermes-agent, use `scripts/hermes_mem0_tool.py` or the manifest at `mem0/integration/hermes_agent_mem0_read_tool.json`; keep it explicit/cached, not an every-turn prelude. `mlx-bge` is available only as an opt-in mode with vector fallback; the broader cold/warm proof passed safely but remains too slow and singleton-only for automatic preludes. Keep Qwen3 0.6B as a learned-reranker candidate only after prompt/metadata work fixes the isolated fixture recency miss and the ONNX/Transformers.js bridge has a bounded CPU/CoreML proof.
7. If running a Qwen3 v6 adapter attempt, add only narrow strict-compatible unsupported-tool refusal examples and stop if held-out strict pass drops below `1.000`.
8. Start any safer LFM2.5 recipe only with lower learning rate and an early empty-response gate.
9. Validate every new runtime through `ollama-pack/scripts/runtime_smoke.sh` or the LM Studio smoke helper before using it in Hermes.
10. Active incomplete Conductor tracks remain only where external execution is
    blocked: `qwen3-v4-peft-colab-full-scorecard_20260613`,
    `qwen3-v4-peft-colab-scorecard-shards_20260613`,
    `qwen3-v4-peft-hf-jobs-scorecard_20260613`,
    `qwen3-v4-peft-azure-scorecard_20260613`,
    `qwen3-v4-peft-kaggle-scorecard_20260613`,
    `qwen3-v4-peft-modal-scorecard_20260614`,
    `qwen3-v4-peft-lightning-scorecard_20260614`, and
    `qwen3-v4-peft-ngc-cloud-function-scorecard_20260613`. The next live
    execution step is whichever backend becomes unblocked first: HF credits,
    Kaggle run approval, Azure login/quota, NGC auth/container/quota,
    a stable Colab no-limit session, or Modal credit/GPU policy approval. The
    next new local track should be selected
    deliberately from remaining role gaps: prompt/profile repair for a specific
    local candidate or a fresh model-radar/runtime proof if a newly verified
    open-weight model appears.

## Key Files

| File | What to edit |
|---|---|
| `conductor/tracks.md` | Hub-level track registry |
| `conductor/tracks/*/spec.md` | Hub-level feature specifications |
| `conductor/tracks/*/plan.md` | Hub-level implementation plans |
| `MODEL_CANDIDATES.yaml` | Machine-readable model radar |
| `PLATFORM_LANES.md` | Purpose/platform abstraction and lane routing |
| `AZURE_SCALEOUT.md` | Azure preflight and cloud-lane policy |
| `CLOUD_BENCHMARK_ORCHESTRATION.md` | Dynamic local/Colab/Azure/NGC/Kaggle execution workflow |
| `CLOUD_BENCHMARK_ORCHESTRATION.yaml` | Machine-readable backend and job profile registry |
| `scripts/check_model_candidates.py` | HF existence/status verification |
| `FRAMEWORKS.md` | Framework and SDK choices |
| `RUNTIME_TARGETS.md` | Runtime/serving strategy |
| `scripts/train_config*.yaml` | Model ID, batch size, iterations |
| `modelfiles/*.Modelfile` | Chat template/runtime packaging |

## Read First

- `README.md`
- `BENCHMARKING_PLAN.md`
- `STANDARD_BENCHMARKS.md`
- `DOCUMENTATION_PLAN.md`
- `APPLICATIONS.md`
- `REQUIREMENTS.md`
- `FUTURE_MODELS.md`
- `FRAMEWORKS.md`
- `RUNTIME_TARGETS.md`
- `NEW_MODEL_WORKFLOW.md`
