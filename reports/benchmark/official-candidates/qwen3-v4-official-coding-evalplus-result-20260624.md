# Qwen3 v4 Official Coding EvalPlus Result

Status: `scored-artifact-present`
Suite: `official-coding`
Run ID: `qwen3-v4-peft-official-coding-20260616`
Candidate: `qwen3-4b-strict-toolcall-v4-targeted`
Dataset: `humaneval`

This run generated all 164 HumanEval samples and scored them with EvalPlus.
It is coding benchmark evidence for this candidate, but it is not a broad model
quality claim by itself.

## Scores

| Suite | pass@1 |
|---|---:|
| HumanEval base tests | `0.518` |
| HumanEval+ base + extra tests | `0.482` |

Detailed result JSON contains `164` task entries. The raw status counts from
that JSON are `85/164` base passes and `80/164` plus passes.

## Artifacts

- Output root: `/Volumes/PortableSSD/hermes-evals/standard-benchmarks/coding/qwen3-v4-peft-official-coding-20260616`
- Generated samples: `/Volumes/PortableSSD/hermes-evals/standard-benchmarks/coding/qwen3-v4-peft-official-coding-20260616/generated.jsonl`
- EvalPlus results: `/Volumes/PortableSSD/hermes-evals/standard-benchmarks/coding/qwen3-v4-peft-official-coding-20260616/generated_eval_results.json`
- EvalPlus log: `/Volumes/PortableSSD/hermes-evals/standard-benchmarks/coding/qwen3-v4-peft-official-coding-20260616/evalplus-humaneval-no-memlimit.log`
- Generation summary: `/Volumes/PortableSSD/hermes-evals/standard-benchmarks/coding/qwen3-v4-peft-official-coding-20260616/generation-summary.json`

## Generation

The initial generator prompt appended natural-language instructions and caused
prose completions. The generator was updated to use raw HumanEval completion
prompts by default, preserve function-body indentation, trim generated test
scaffolding, and normalize already-written JSONL rows.

Rows generated: `164`
Unique task IDs: `164`
Prompt mode: `completion`
Max tokens: `256`

## Scoring Command

```bash
source scripts/env.sh && EVALPLUS_MAX_MEMORY_BYTES=-1 \
/Volumes/PortableSSD/hermes-training-envs/benchmarks-py312/bin/python \
  -m evalplus.evaluate humaneval \
  --samples /Volumes/PortableSSD/hermes-evals/standard-benchmarks/coding/qwen3-v4-peft-official-coding-20260616/generated.jsonl \
  --test-details \
  --parallel 8 \
  --i-just-wanna-run
```

`EVALPLUS_MAX_MEMORY_BYTES=-1` was required on this macOS host because the
default EvalPlus memory guard hit `ValueError: current limit exceeds maximum
limit` in `resource.setrlimit`.
