# Hermes Training Hub — Codex Handoff

> Last updated: 2026-05-26
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

- `gemma4`: `d4d7078` (`github.com/edithatogo/hermes-gemma-lab`)
- `lfm2`: `40c4020` (`github.com/edithatogo/hermes-lfm2-lab`)
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
- Model radar includes Qwen3.6, Hermes 4, Gemma 4 A4B, LFM2.5, LFM2-ColBERT, Qwen3-Next, BitNet, BGE-M3, Jina embeddings, and watchlist entries for RWKV/Mamba-style families.
- Platform abstraction is now explicit: Mac/MLX is the local lane, Azure is the scale-out lane, retrieval is separate from chat SFT, and specialist runtimes require proof.
- Azure preflight exists at `scripts/azure_preflight.py`; it passes for `d.a.mordaunt@gmail.com` on `Azure for Students`. Modern GPU quota is zero across sampled regions, so the Azure track is fail-closed until quota is approved.
- Qwen3 v4 targeted is the current public/recommended strict Hermes tool-call adapter. It passes the held-out strict local tool-call suite at `1.000` with `/no_think` plus assistant prefill `<think>\n\n</think>\n\n`; publication evidence is in `reports/publication/qwen3-4b-strict-toolcall-v4-targeted/`.
- Qwen3 v5 pilot-polish is a documented non-promotion result. It improved the local BFCL-style pilot to `1.000`, but held-out strict pass regressed to `0.875`; keep v4 as the recommended/public adapter.
- V4/V5 pilot failure analysis is recorded in `reports/publication/qwen3-4b-strict-toolcall-v4-targeted/pilot-failure-analysis-20260526.md`. Any v6 attempt must start from V4 and keep held-out strict pass at `1.000`.
- The `ollama-pack` runtime packaging Conductor track is complete. It records current MLX, Ollama, GGUF/LM Studio, and blocked retest status without promoting unvalidated runtime surfaces.

Current gaps:

- Public dataset publication remains blocked pending explicit approval. A cleaned synthetic-only candidate has been materialized and audited under `/Volumes/PortableSSD/hermes-evals/datasets/qwen3-v4-synthetic-only-20260526`; the scope, run card, and draft dataset card are recorded in `reports/publication/qwen3-4b-strict-toolcall-v4-targeted/`.
- BGE-M3 is acquired and CPU/MPS-smoked from the SSD Hugging Face cache, but it is not promoted for mem0 defaults. On the expanded 12-case suite, BGE-M3 CPU reached top-1 `0.917` / recall@3 `1.000`; the current nomic default reached top-1 `0.833` / recall@3 `1.000` from the clean SSD Ollama root. The new `score_plus_created_at_rank_close_margin` reranker reached `1.000` on the BGE-derived suite and `0.917` on the nomic-derived suite, so the next mem0 improvement remains the read-only wrapper path, not a default embedder switch. See `reports/benchmark/mem0/bge-m3-expanded-retrieval-20260526.md` and `reports/benchmark/mem0/nomic-expanded-retrieval-20260526.md`.
- `Qwen/Qwen3-Reranker-0.6B` is now acquired in the SSD Hugging Face cache and benchmarked through the causal-LM yes/no scorer. It reached top-1, recall@3, MRR, and nDCG@3 of `1.000` on the fixed 6-case suite and both BGE/nomic expanded 12-case derived suites. The live read-only wrapper also passed against real `mem0 cmd search` output with one returned memory, `3.920s` mem0 search latency, `0.216s` Qwen3 scoring latency, and `12.093s` one-shot total latency. The warm helper reduced the second service-backed live request to `4.112s` total with `0.119s` Qwen scoring. Multi-result replay through the live-wrapper abstraction reached top-1 `1.000` for warm Qwen3 on fixed, BGE-derived expanded, and nomic-derived expanded suites; the close-margin heuristic stayed at `0.917` on nomic-derived replay. The isolated live fixture then returned 3-5 candidates per query and reversed the Qwen promotion case: close-margin reached top-1 `1.000`, while warm Qwen3 matched vector at `0.667` and missed a recency lane. The public `onnx-community/Qwen3-Reranker-0.6B-ONNX` candidate remains an ONNX/Transformers.js runtime bridge task; the source HF model is the validated Python scorer. See `reports/benchmark/mem0/mem0-live-fixture-qwen3-multiretrieval-rerank-20260526.md`, `reports/benchmark/mem0/mem0-rerank-replay-comparison-20260526.md`, `reports/benchmark/mem0/qwen3-0-6b-live-rerank-smoke-20260526.md`, `reports/benchmark/mem0/qwen3-0-6b-warm-service-rerank-smoke-20260526.md`, `reports/benchmark/mem0/run-cards/rerank-qwen3-0-6b-fixed-20260526.md`, `reports/benchmark/mem0/run-cards/qwen3-0-6b-nomic-expanded-rerank-20260526.md`, and `reports/benchmark/mem0/run-cards/qwen3-0-6b-bge-expanded-rerank-20260526.md`.
- The read-only mem0 wrapper now exposes `score_plus_created_at_rank_close_margin` and live search smoke passed from a clean SSD-backed Ollama root at `/Volumes/PortableSSD/Ollama/mem0-clean-models`. The stale Qdrant lock holder was stopped, `nomic-embed-text:latest` was re-pulled into the clean root, and the wrapper returned a live result in `2.873s`. `sam860/LFM2:2.6b` was also pulled into the clean root; bounded `/api/generate` returned exactly `ok`, and `extraction-lfm2-2-6b-clean-root-20260526` passed 7/7 mem0 extraction cases with JSON validity `1.000`, forbidden hit rate `0.000`, empty-case pass `1.000`, p50 latency `0.874s`, and p95 latency `0.988s`. No mem0 defaults were changed. See `reports/benchmark/mem0/mem0-margin-rerank-live-smoke-20260526.md` and `reports/benchmark/mem0/extraction-lfm2-2-6b-clean-root-20260526.md`.
- Live multi-result comparison is now covered by an isolated non-sensitive fixture store, not by the default mem0 store. The default store still returned singleton results for broad probes, but the fixture used `MEM0_CONFIG_PATH`, an output-local Qdrant path, and a unique collection. Close-margin passed this gate; Qwen3 did not. `scripts/mem0_read.py` is the guarded read-only entrypoint for agents; it defaults to close-margin, keeps vector as rollback, and makes Qwen3 explicit/experimental with optional vector fallback. A 5-query UX latency probe passed with p50 `2.897s` and p95 `3.729s`, all singleton live-store results, so use it as an explicit memory-read tool or cached/batched path rather than an automatic every-turn prelude. The opt-in cache path also passed a 10-case cold/warm benchmark with 5 cache hits, cold p50 `2.904s`, and cache-hit p50 `0.000s`. `scripts/hermes_mem0_tool.py` now provides the explicit Hermes-agent command contract; live smoke passed with first-read latency `3.999s` and second-read cache-hit latency `0.000s`. No mem0 defaults were changed. See `reports/benchmark/mem0/live-multiretrieval-readiness-20260526.md`, `reports/benchmark/mem0/mem0-live-fixture-qwen3-multiretrieval-rerank-20260526.md`, `reports/benchmark/mem0/mem0-read-ux-close-margin-20260526.md`, `reports/benchmark/mem0/mem0-read-cache-close-margin-20260526.md`, and `reports/benchmark/mem0/hermes-mem0-tool-smoke-20260526.md`.
- The Hermes user plugin shim is installed and enabled at `~/.hermes/plugins/hermes-mem0-read`, with the tracked template in `mem0/integration/hermes-mem0-read`. `HERMES_PLUGINS_DEBUG=1 hermes tools list` exposes the `hermes_mem0` plugin toolset, and direct handler smoke through close-margin returned one memory in `3.970s` while remaining read-only and non-mutating. See `reports/benchmark/mem0/hermes-mem0-plugin-smoke-20260526.md`.
- Dataset publication now has a non-publishing dry-run generator at `scripts/prepare_dataset_publication_dry_run.py`. The current dry run for the cleaned synthetic-only dataset produced `reports/publication/qwen3-4b-strict-toolcall-v4-targeted/dataset-publication-dry-run-20260526.md` and `.json`; it confirms 82 rows, 82 unique IDs, no held-out prompt overlap, and no publish actions. The remaining blocker is explicit approval of the exact cleaned dataset scope and HF repo ID.
- The next cheapest official benchmark lane is `lm-eval-selected`. The lm-eval smoke/candidate manifests now use the proven `local-chat-completions` endpoint shape from the IFEval pilot, with `arc_challenge,hellaswag,truthfulqa_mc2,gsm8k,winogrande`; the blocker is starting the `mlx_lm.server` adapter endpoint at `127.0.0.1:8080`.
- `lm-eval-selected` was attempted against the live Qwen3 v4 MLX endpoint on `127.0.0.1:8080` and is blocked before scoring. The selected ARC/HellaSwag/TruthfulQA/GSM8K/Winogrande tasks require loglikelihood; `local-chat-completions` raises `NotImplementedError`, and a `local-completions` probe fails because `mlx_lm.server` rejects the harness logprobs shape. Treat IFEval as the only official-harness pilot until a loglikelihood-compatible MLX shim or direct evaluator adapter exists. See `reports/benchmark/lm-eval/qwen3-4b-v4-targeted-lm-eval-selected-smoke-20260526.md`.
- The ONNX/Transformers.js bridge for `onnx-community/Qwen3-Reranker-0.6B-ONNX` was attempted and failed closed before promotion. Node/npm and the SSD tool root are present, no repo-local `node_modules` was created, the default `wasm` path was unsupported by the Node runtime, and the CPU retry with `max_length=512` timed out after `180.0s` before one fixed-suite case completed. See `reports/benchmark/mem0/qwen3-0-6b-onnx-transformersjs-bridge-20260526.md`.
- Standard benchmark coverage is now machine-checked for `qwen3-4b-strict-toolcall-v4-targeted`. The adapter remains local strict-gate ready with pilot-only benchmark positioning; public release is blocked, and full official BFCL, lm-eval, coding, safety, and RULER candidate suites are explicitly missing for broad benchmark claims. See `reports/benchmark/standard-coverage/qwen3-v4-targeted-standard-coverage-20260526.md`.
- Large MoE/frontier configs are runtime/teacher experiments only; do not treat them as safe defaults for local training.
- 2026-05-26 model radar refresh found no official Qwen3.7 open-weight lane. The only actionable delta was Qwen3.6 GGUF packaging with bundled MTP/self-speculative decoding heads: `mudler/Qwen3.6-35B-A3B-APEX-MTP-GGUF` and `localweights/Qwen3.6-35B-A3B-MTP-IQ4_XS-GGUF`. Keep them as runtime latency experiments behind the existing Qwen3.6 Q4_K_M proof, not local fine-tune targets.
- Azure student subscription login is complete. GPU-family quota/capacity still needs explicit Azure ML/portal confirmation before compute creation.
- LFM2.5 full-smoke training/evaluation is complete as a proof, but the adapter is not publishable. It trained for 200 iterations / 175,895 tokens with final validation loss 1.455 and peak memory 6.022 GB; evaluation on 100 prompts showed response collapse. See `lfm2/eval/lfm25-full-smoke-summary.md`.
- LFM2.5 1.2B Instruct smoke LoRA is now runtime-proven through `mlx_lm.server` using only SSD-cached artifacts. The server exposed the absolute snapshot path as the model ID, and the OpenAI-compatible smoke returned `{"ok": true}` in `378ms`. The direct `lfm2/scripts/evaluate.py` adapter load blocker is fixed in `lfm2` commit `3413720`, but a one-prompt direct eval still produced a non-compliant response, so this remains runtime/load proof only. See `reports/runtime/lfm25-1.2b-instruct-smoke-mlx-proof-20260526.md`.
- Qwen3 4B smoke training/evaluation is complete as a local MLX proof. It trained for 10 iterations / 2,889 tokens with final validation loss 2.386 and peak memory 3.944 GB; base and adapter both passed the response-collapse gate. See `gemma4/eval/qwen3-4b-smoke-summary.md`.
- Qwen3 4B MLX adapter runtime smoke passed through an OpenAI-compatible `mlx_lm.server` endpoint. See `ollama-pack/runtime-card.qwen3-4b-mlx-smoke.md`.
- Qwen3 4B fused safetensors export exists under `/Volumes/PortableSSD/hermes-exports/ollama/qwen3-4b-hermes-smoke`. Ollama experimental import succeeded into `/Volumes/PortableSSD/ollama-models`, but `/v1/chat/completions` failed with an Ollama MLX runner panic, so Ollama is not a validated runtime for this Qwen3 package yet.
- Qwen3 4B dequantized fused export and GGUF conversion are complete on the SSD:
  - `/Volumes/PortableSSD/hermes-exports/ollama/qwen3-4b-hermes-smoke/merged-dequantized`
  - `/Volumes/PortableSSD/hermes-exports/ollama/qwen3-4b-hermes-smoke/qwen3-4b-hermes-smoke-f16.gguf`
  - `/Volumes/PortableSSD/hermes-exports/ollama/qwen3-4b-hermes-smoke/qwen3-4b-hermes-smoke-q4_K_M.gguf`
- The Q4_K_M GGUF passed direct `llama-completion` validation and LM Studio smoke. Ollama GGUF import failed because the daemon dropped during model creation, so direct llama.cpp and LM Studio are the validated GGUF runtime paths for now.
- Populated publication/evidence bundles exist for Qwen3 smoke, failed Qwen3 attempts, Qwen3 v4 public adapter evidence, and Qwen3 v5 non-promotion evidence.
- Internal disk pressure has been reduced. `~/.gemini/antigravity/browser_recordings` was relocated to `/Volumes/PortableSSD/home-relocated/gemini-antigravity/browser_recordings` and symlinked back. Last check showed about 51 GiB free on `/` and about 660 GiB free on `/Volumes/PortableSSD`.

## Next Actions

1. Re-test Ollama only after upgrading or replacing the current crashing Qwen3 GGUF/import path.
2. Confirm Azure ML GPU quota/capacity before creating workspace compute or submitting benchmark jobs.
3. Run broader official benchmark score cards for the v4 adapter only if the claim needs to go beyond local strict Hermes tool-calling and repo-native pilots; the coverage gate lists missing official BFCL, lm-eval, coding, safety, and RULER candidate suites.
4. Publish no dataset until the cleaned synthetic-only dataset scope is explicitly approved and re-audited.
5. Use Hermes 4, Qwen3.6, Gemma 4, and LFM2-24B as runtime baselines/teachers before attempting local fine-tunes.
6. If wiring mem0 into Hermes-agent, use `scripts/hermes_mem0_tool.py` or the manifest at `mem0/integration/hermes_agent_mem0_read_tool.json`; keep it explicit/cached, not an every-turn prelude. Keep Qwen3 0.6B as a learned-reranker candidate only after prompt/metadata work fixes the isolated fixture recency miss and the ONNX/Transformers.js bridge has a bounded CPU/CoreML proof.
7. If running a Qwen3 v6 adapter attempt, add only narrow strict-compatible unsupported-tool refusal examples and stop if held-out strict pass drops below `1.000`.
8. Start any safer LFM2.5 recipe only with lower learning rate and an early empty-response gate.
9. Validate every new runtime through `ollama-pack/scripts/runtime_smoke.sh` or the LM Studio smoke helper before using it in Hermes.

## Key Files

| File | What to edit |
|---|---|
| `conductor/tracks.md` | Hub-level track registry |
| `conductor/tracks/*/spec.md` | Hub-level feature specifications |
| `conductor/tracks/*/plan.md` | Hub-level implementation plans |
| `MODEL_CANDIDATES.yaml` | Machine-readable model radar |
| `PLATFORM_LANES.md` | Purpose/platform abstraction and lane routing |
| `AZURE_SCALEOUT.md` | Azure preflight and cloud-lane policy |
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
