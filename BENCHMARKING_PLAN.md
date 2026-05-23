# Benchmarking Plan

This project must distinguish pipeline proof from quality proof.

Use [STANDARD_BENCHMARKS.md](./STANDARD_BENCHMARKS.md) for the broader standardized suite that should accompany GitHub and Hugging Face publication. Use [AZURE_SCALEOUT.md](./AZURE_SCALEOUT.md) when benchmark breadth or teacher/evaluator runs should move to Azure.
Use [RETRIEVAL_MEMORY.md](./RETRIEVAL_MEMORY.md) for the retrieval-specific lane decisions, serving shape, and publication rules.

## Current Result

The completed `LiquidAI/LFM2.5-1.2B-Instruct` run is a smoke test:

- Config: `lfm2/scripts/train_config.lfm25-1.2b-instruct.smoke.yaml`
- Iterations: 10
- Effective trained tokens logged by MLX: 5,462
- Peak memory: about 3.6 GB
- Output: `lfm2/experiments/lfm25-1.2b-instruct-smoke/lora_adapter`

This proves that model loading, dataset processing, LoRA injection, training, and adapter saving work on the M1 Max. It is not enough training to claim improved Hermes behavior.

The completed `Qwen/Qwen3-4B-MLX-4bit` candidate run is a larger local proof:

- Config: `gemma4/scripts/train_config.qwen3-4b.candidate.yaml`
- Iterations: 60
- Effective trained tokens logged by MLX: 25,094
- Peak memory: 3.962 GB
- Output: `gemma4/experiments/qwen3-4b-candidate/lora_adapter`
- Hermes-local response gate: passed on 100 prompts
- Tool-call benchmark: failed strict local tool-call shape at 1/6 cases

This proves the Qwen3 local MLX lane can scale beyond the first smoke run without response collapse. It does not yet prove Hermes tool-calling quality; the next dataset needs explicit strict tool-call targets.

The completed `Qwen/Qwen3-4B-MLX-4bit` tool-call repair proof is a targeted negative/diagnostic result:

- Config: `gemma4/scripts/train_config.qwen3-4b.toolcall-repair.yaml`
- Iterations: 40
- Effective trained tokens logged by MLX: 10,603
- Peak memory: 3.417 GB
- Output: `gemma4/experiments/qwen3-4b-toolcall-repair/lora_adapter`
- Strict tool-call benchmark: still failed at 1/6 cases
- Diagnostic empty-think-stripped rescore: 5/6 cases

This proves the adapter learned most tool arguments, but Qwen's empty `<think></think>` wrapper and one malformed multi-call output still block publication. The next implementation should add runtime normalization for empty leading thinking wrappers, retrain on the richer `gemma4/data/strict_tool_call` lane, and evaluate on `benchmarks/tool_call_local/heldout_suite.json`, which does not overlap the benchmark-mirrored training seed.

The completed `qwen3-4b-strict-toolcall` run is a held-out promotion failure:

- Config: `gemma4/scripts/train_config.qwen3-4b.strict-toolcall.yaml`
- Iterations: 80
- Effective trained tokens logged by MLX: 28,020
- Peak memory: 3.785 GB
- Output: `gemma4/experiments/qwen3-4b-strict-toolcall/lora_adapter`
- Mirrored regression suite: strict 0.167, diagnostic empty-think-stripped 1.000
- Held-out publication gate: strict 0.250, diagnostic empty-think-stripped 0.750

This proves the current strict seed is too small for publication-quality generalization. Keep publication blocked and expand strict data before another promotion attempt.

The completed `Qwen/Qwen3-4B-MLX-4bit` strict tool-call expanded-data retrain is another held-out promotion failure:

- Config: `gemma4/scripts/train_config.qwen3-4b.strict-toolcall-expanded.yaml`
- Training data: expanded and audited `gemma4/data/strict_tool_call/expanded_splits_v1`
- Iterations: 120
- Effective trained tokens logged by MLX: 33,133
- Peak memory: 3.785 GB
- Output: `gemma4/experiments/qwen3-4b-strict-toolcall-expanded/lora_adapter`
- Mirrored regression suite: strict 0.167, diagnostic empty-think-stripped 0.833
- Held-out publication gate: strict 0.250, diagnostic empty-think-stripped 0.750
- Strict JSON validity: 0.000
- Multi-turn repair: 0.000
- Publication scaffold: `reports/publication/qwen3-4b-strict-toolcall-expanded/`

This proves expanded coverage improved the documented evidence base but did not solve strict output formatting. Keep Hugging Face publication blocked and do not substitute mirrored-suite results, diagnostic empty-think-stripped scores, non-heldout local checks, or unaudited expanded data for the held-out gate.

Dataset-token evidence for this run is now recorded at `reports/publication/qwen3-4b-strict-toolcall-expanded/dataset-token-audit.json`. Runtime normalization of empty leading `<think></think>` wrappers is documented separately at `reports/runtime/qwen3-runtime-normalization/run-card.md`; it is a Hermes integration aid, not a benchmark promotion rule.

The completed v2/v3 strict format-guard attempts are negative but useful evidence:

- V2 config: `gemma4/scripts/train_config.qwen3-4b.strict-toolcall-v2.yaml`
- V2 data: audited `gemma4/data/strict_tool_call/expanded_splits_v2`
- V2 held-out publication gate: strict `0.250`, diagnostic empty-think-stripped `0.625`
- V3 config: `gemma4/scripts/train_config.qwen3-4b.strict-toolcall-v3-no-think.yaml`
- V3 data: audited `gemma4/data/strict_tool_call/expanded_splits_v3_no_think`
- V3 held-out publication gate: strict `0.250`, diagnostic empty-think-stripped `0.875`
- V3 residual after empty-think stripping: one semantic argument mismatch in `heldout-argument-correctness-lab-order`
- Publication scaffold: `reports/publication/qwen3-4b-strict-toolcall-v2-v3/`

This proves that prompt-shape augmentation improved recoverable tool-call behavior but did not satisfy strict Hermes output requirements. Keep Hugging Face publication blocked and prioritize either a runtime that can suppress Qwen thinking wrappers before Hermes sees them, or a base model that obeys no-thinking mode without wrapper leakage.

A first-class runtime-normalized report for the V3 held-out scorecard is now generated under `/Volumes/PortableSSD/hermes-evals/runtime-normalized-tool-call/qwen3-4b-strict-toolcall-v3-heldout-20260524/`. It reports strict `0.250` and runtime-normalized `0.875`. This is Hermes integration evidence only; it does not satisfy the held-out publication gate.

## Dataset Audit

Run:

```bash
source scripts/env.sh
HF_HUB_OFFLINE=1 ./.venv/bin/python scripts/dataset_token_audit.py \
  --model LiquidAI/LFM2.5-1.2B-Instruct \
  --data lfm2/data/splits
```

Current LFM2.5 split audit:

| Split | Rows | Tokens | Avg | P50 | P95 | Max |
|---|---:|---:|---:|---:|---:|---:|
| train | 461 | 219,354 | 475.8 | 331 | 1,260 | 2,225 |
| valid | 57 | 22,693 | 398.1 | 278 | 951 | 1,759 |
| test | 59 | 25,081 | 425.1 | 267 | 1,159 | 1,784 |

## Training Gates

Use increasing gates rather than jumping straight to large runs.

| Gate | Purpose | Target Tokens | Pass Criteria |
|---|---|---:|---|
| smoke | Pipeline proof | 5k-25k | Completes, saves adapter, no memory or dataset errors |
| full-smoke-data | Fit current checked-in data | 200k-500k | Stable train/validation loss, no obvious eval regression |
| pilot | First behavior signal | 2M-10M | Wins or ties base on Hermes eval set and tool-call checks |
| candidate | Publishable adapter candidate | 25M-100M+ | Beats base and prior adapter across automated and manual evals |

The SSD capacity removes the artifact/cache limit, but it does not make the current checked-in dataset optimal. The limiting factor is data quality and coverage, not disk space.

## Evaluation Set

The current `eval/prompts.jsonl` is a seed set only. Expand it to at least 100 prompts before judging quality:

- 25 tool-use and JSON/function-call formatting prompts
- 20 coding/debugging prompts
- 15 long-context instruction-following prompts
- 15 reasoning/planning prompts
- 10 refusal/safety boundary prompts
- 10 concise factual/procedural prompts
- 5 adversarial formatting prompts

Audit coverage with:

```bash
source scripts/env.sh
./.venv/bin/python scripts/eval_prompt_audit.py \
  lfm2/eval/prompts.jsonl \
  gemma4/eval/prompts.jsonl
```

Use `--strict` in release checks so a sub-100 prompt set fails before publication.

After every generated-result run, apply the response-collapse gate:

```bash
source scripts/env.sh
./.venv/bin/python scripts/eval_response_gate.py \
  lfm2/eval/lfm25-full-smoke-adapter-results.jsonl \
  --strict
```

The full-smoke LFM2.5 adapter currently fails this gate because it emits empty or near-empty responses. Treat that as a valid negative benchmark result, not a publication candidate.

For retrieval and Hermes memory work, use a separate scenario set that covers:

- grounded fact recall from prior memory
- document-grounded QA with citations
- multi-hop retrieval across two or more sources
- preference updates and recency conflicts
- source attribution and distractor resistance
- tool-state recall when memory is mediated by a retriever

## Metrics

Record these for base model, smoke adapter, and each promoted adapter:

- Exact JSON/tool-call validity rate
- Instruction-following pass/fail
- Code execution pass/fail where applicable
- Human preference: base vs adapter
- Response length and verbosity drift
- Latency, tokens/sec, peak memory
- Validation loss on held-out split
- Local tool-call benchmark scorecard: JSON validity, argument correctness, invalid-tool handling, and multi-turn repair
- Diagnostic empty-think-stripped tool-call score for Qwen-family models; this is informational only and never replaces the strict pass gate

## Promotion Rule

Do not publish or package an adapter for Hermes unless it passes:

1. Structural readiness: `./.venv/bin/python scripts/validate_readiness.py`
2. Dataset audit recorded in docs or run notes
3. Base-vs-adapter comparison on the expanded eval set
4. Response-collapse gate on generated eval output
5. Strict local held-out tool-call gate: `benchmarks/tool_call_local/heldout_suite.json` must pass at `1.000`
6. Standard benchmark gate appropriate to the release stage:
   - smoke: Hermes-local only
   - pilot: Hermes-local, IFEval, BFCL subset, HumanEval/MBPP, selected `lm-eval`
   - candidate: broader standardized suite from `STANDARD_BENCHMARKS.md`
7. Runtime smoke through MLX, then Ollama or LM Studio path
8. License check for base model and dataset

For local Hermes engineering checks, the tool-call benchmark runner may be executed against `benchmarks/tool_call_local/suite.json`, but that suite overlaps the strict training seed and is not held-out evidence. For publication checks, run the held-out suite:

```bash
source scripts/env.sh
./.venv/bin/python scripts/run_tool_call_benchmark.py \
  --model <model_id_or_path> \
  --adapter <optional_adapter_path> \
  --suite benchmarks/tool_call_local/heldout_suite.json \
  --user-prefix /no_think
```

The output directory should remain under `$HERMES_EVAL_ROOT/tool-call-benchmark/<run-id>`.

For the Qwen3 strict-tool-call expanded-data retrain track, the run card, model card, and publish-readiness checklist must quote the exact heldout pass rate from this command shape. Any value below `1.000` keeps Hugging Face publication blocked.

Publication-quality benchmark claims should also retain exact command lines, model revisions, harness versions, prompt-set revisions or hashes, and raw output locations for every score that appears in a model card or run card.

## Platform-Lane Benchmark Routing

| Lane | Benchmark Use |
|---|---|
| Mac/MLX | smoke, full-smoke-data, local Hermes eval, latency/memory |
| Mac/Ollama/LM Studio | endpoint smoke, JSON/tool-call checks, daily runtime latency |
| Azure/CUDA | broader `lm-eval`, coding suites, BFCL, teacher/evaluator judging, larger-model comparisons |
| Retrieval | MTEB, ColBERT/retrieval tests, Hermes memory/RAG scenarios |
| Specialist runtime | runtime proof, long-context/RULER, architecture-specific stability checks |

Azure benchmark outputs must be synced back to SSD-backed report roots before model-card or run-card publication.

Retrieval runs should record the exact benchmark command shape, model revision, index hash, and corpus digest. The canonical CLI shape is:

```bash
source scripts/env.sh
mteb run \
  -m <model_id_or_path> \
  -t "<retrieval_task_or_benchmark>" \
  --output-folder "$HERMES_EVAL_ROOT/mteb/<run-id>"
```
