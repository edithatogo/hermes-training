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

## Promotion Rule

Do not publish or package an adapter for Hermes unless it passes:

1. Structural readiness: `./.venv/bin/python scripts/validate_readiness.py`
2. Dataset audit recorded in docs or run notes
3. Base-vs-adapter comparison on the expanded eval set
4. Response-collapse gate on generated eval output
5. Standard benchmark gate appropriate to the release stage:
   - smoke: Hermes-local only
   - pilot: Hermes-local, IFEval, BFCL subset, HumanEval/MBPP, selected `lm-eval`
   - candidate: broader standardized suite from `STANDARD_BENCHMARKS.md`
6. Runtime smoke through MLX, then Ollama or LM Studio path
7. License check for base model and dataset

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
