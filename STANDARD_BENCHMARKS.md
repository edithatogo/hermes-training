# Standard Benchmark Plan

The repo needs two benchmark layers:

1. **Hermes-local benchmark**: proves the adapter works for the actual Hermes use case: concise assistant behavior, tool calls, local runtime compatibility, and Mac latency.
2. **Standardized benchmark suite**: makes results comparable on GitHub and Hugging Face.

Do not use one layer as a substitute for the other. A model can improve on Hermes tool formatting while getting worse at broad reasoning, and the reverse can also happen.

## Recommended Suites

| Area | Primary benchmark | Why include it | Run location |
|---|---|---|---|
| General knowledge and reasoning | `lm-evaluation-harness`: MMLU, ARC-Challenge, HellaSwag, TruthfulQA, Winogrande, GSM8K | Common comparable baselines across open models | Local for small/quantized models; cloud optional for large MoE |
| Instruction following | IFEval plus the expanded Hermes-local eval | Measures prompt constraint following and format obedience | Local |
| Function/tool calling | Berkeley Function Calling Leaderboard (BFCL V3 where possible) plus Hermes-local tool-call validator | Hermes depends on reliable tool calls; BFCL covers AST/execution, relevance detection, multiple and parallel calls | Local subset first; full run if tooling is stable |
| Coding | HumanEval/MBPP for quick regression; BigCodeBench and LiveCodeBench for stronger claims | HumanEval is quick but saturated; BigCodeBench and LiveCodeBench are better for modern code models | Local subset first; full run may be slow |
| Software-engineering agents | SWE-bench Verified/Lite only after a real agent harness exists | Measures repository-level issue resolution, not plain chat completion | Usually cloud or remote runner |
| Long context | RULER | Important for recursive/subquadratic/long-context claims | Local at staged context sizes |
| Safety and refusal | XSTest, SimpleSafetyTests, HarmBench subset | Prevents Hermes adaptation from damaging refusal boundaries | Local subset |
| Retrieval/embedding | MTEB for embedding models; ColBERT-specific retrieval eval for LFM2-ColBERT | Applies to LFM2-ColBERT, BGE-M3, Jina embeddings, and Qwen embedding/reranker tracks, not chat SFT adapters | Local |

## Benchmark Gates

| Gate | Required benchmarks | Purpose |
|---|---|---|
| Smoke | Hermes-local 10-100 prompt set; generation works with adapter loaded | Pipeline proof |
| Full-smoke-data | Hermes-local expanded 100+ prompts; validation loss; latency/memory | Detect obvious regressions after training on current data |
| Pilot | Hermes-local, IFEval, BFCL subset, HumanEval/MBPP, selected lm-eval tasks | First meaningful behavior comparison |
| Candidate | Full Hermes-local, broader lm-eval suite, BFCL, coding suite, safety suite, RULER where relevant | Publishable adapter decision |
| Frontier/runtime-only | Latency/memory, Hermes-local, BFCL subset, selected lm-eval tasks | Compare large MoE/recursive/subquadratic models used as baselines or teachers |

## Platform Execution Rules

For local Mac work, always start with:

```bash
source scripts/env.sh
```

This moves caches and outputs to the SSD:

- Hugging Face model cache: `$HF_HUB_CACHE`
- Hugging Face dataset cache: `$HF_DATASETS_CACHE`
- `lm-evaluation-harness` cache: `$LM_HARNESS_CACHE_PATH`
- HELM workspace: `$HELM_HOME`
- OpenCompass cache and datasets: `$OPENCOMPASS_CACHE_DIR`, `$OPENCOMPASS_DATASETS`
- Project eval outputs: `$HERMES_EVAL_ROOT`
- temp files: `$TMPDIR`

For Azure work, run `scripts/azure_preflight.py` first and keep the default policy of Spot/low-priority, `min_instances: 0`, `max_instances: 1`, and one GPU job at a time until a track explicitly changes it.

## lm-evaluation-harness Starter

Use `lm-eval` for common academic baselines. Record the exact command, task names, model args, seeds, and harness commit/version.

Example shape:

```bash
source scripts/env.sh
lm-eval run \
  --model hf \
  --model_args pretrained=<model>,dtype=float16 \
  --tasks arc_challenge,hellaswag,truthfulqa_mc2,gsm8k \
  --device mps \
  --batch_size 1 \
  --output_path "$HERMES_EVAL_ROOT/lm-eval/<run-id>" \
  --log_samples
```

Use limited samples only for engineering tests. Do not publish limited-sample numbers as benchmark scores.

## Tool-Calling Benchmark

The Hermes benchmark must include both local tool-call tests and BFCL-style standardized tests.

Track at minimum:

- exact JSON/tool-call parse rate
- correct function name
- required argument coverage
- hallucinated argument rate
- relevance detection when no tool is appropriate
- multiple and parallel tool calls
- latency and retry rate

Run the local schema/tool-call benchmark with:

```bash
source scripts/env.sh
./.venv/bin/python scripts/run_tool_call_benchmark.py \
  --model <model_id_or_path> \
  --adapter <optional_adapter_path> \
  --suite benchmarks/tool_call_local/suite.json \
  --user-prefix /no_think
```

The runner writes raw outputs, scorecards, and summaries to `$HERMES_EVAL_ROOT/tool-call-benchmark/<run-id>`. Use the checked-in suite as the local BFCL-style subset for engineering runs; keep those outputs off Git and on the SSD-backed eval root.

This local harness is not a substitute for the full BFCL suite. It is the fast Hermes-specific gate that should run before the broader BFCL subset.

## Retrieval Benchmark

Retrieval publication claims need the retrieval lane metrics, not chat metrics.

Track at minimum:

- Recall@k
- nDCG@10
- MRR@10
- latency per query
- index hash and corpus digest
- scenario coverage for Hermes memory/RAG cases

Use the MTEB CLI shape for standard embedding runs:

```bash
source scripts/env.sh
mteb run \
  -m <model_id_or_path> \
  -t "<retrieval_task_or_benchmark>" \
  --output-folder "$HERMES_EVAL_ROOT/mteb/<run-id>"
```

ColBERT or other late-interaction retrievers may use their own benchmark wrapper, but the report must still include the same metric family and the same corpus/index provenance fields.

## Coding Benchmark

Use tiers:

1. HumanEval/MBPP: fast regression checks.
2. BigCodeBench: stronger practical code-generation signal with library/function-call use.
3. LiveCodeBench: stronger contamination-resistant coding signal.
4. SWE-bench Lite/Verified: only for models wired into an agent capable of editing repos and running tests.

## Long-Context Benchmark

Use RULER for Qwen3-Next, recursive models, RWKV/Mamba-style models, and any model where long-context claims matter. Run staged context sizes rather than one maximal run:

- 4k
- 8k
- 16k
- 32k if the runtime stays stable

Record memory, latency, and accuracy at every size.

## Reporting Table

Every published adapter/model card should include:

| Model | Adapter | Dataset tokens | Hermes-local | IFEval | BFCL subset | Coding | lm-eval suite | RULER | Peak memory | Decision |
|---|---|---:|---:|---:|---:|---:|---:|---:|---:|---|
| `<base>` | `<adapter>` | `<tokens>` | `<score>` | `<score>` | `<score>` | `<score>` | `<score>` | `<score>` | `<GB>` | promote / hold / reject |

Retriever cards should use a similar table, replacing chat columns with retrieval columns such as Recall@k, nDCG@10, MRR@10, latency, index hash, and corpus digest.

Any published score should be traceable back to the exact command, model revision, harness or evaluator version, and prompt-set or corpus revision used to produce it.

## References

- EleutherAI `lm-evaluation-harness`: https://github.com/EleutherAI/lm-evaluation-harness
- Berkeley Function Calling Leaderboard: https://gorilla.cs.berkeley.edu/blogs/8_berkeley_function_calling_leaderboard.html
- SWE-bench: https://github.com/swe-bench
- OpenCompass: https://github.com/open-compass/opencompass
- RULER: https://github.com/NVIDIA/RULER
- BigCodeBench: https://github.com/bigcode-project/bigcodebench
- LiveCodeBench: https://github.com/LiveCodeBench/LiveCodeBench
