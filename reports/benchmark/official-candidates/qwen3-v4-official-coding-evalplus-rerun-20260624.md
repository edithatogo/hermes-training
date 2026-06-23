# Qwen3 v4 Official Coding EvalPlus Rerun

Status: `scored-artifact-present`
Suite: `official-coding`
Run ID: `qwen3-v4-peft-official-coding-rerun-20260624`
Candidate: `qwen3-4b-strict-toolcall-v4-targeted`
Dataset: `humaneval`

This rerun generated all 164 HumanEval samples into a fresh SSD-backed output
directory and scored them with EvalPlus. It is coding benchmark evidence for
this candidate, but it is not a broad model quality claim by itself.

## Scores

| Suite | pass@1 |
|---|---:|
| HumanEval base tests | `0.518` |
| HumanEval+ base + extra tests | `0.482` |

Detailed result JSON contains `164` task entries. The raw status counts from
that JSON are `85/164` base passes and `80/164` plus passes.

## Artifacts

- Output root: `/Volumes/PortableSSD/hermes-evals/standard-benchmarks/coding/qwen3-v4-peft-official-coding-rerun-20260624`
- Generated samples: `/Volumes/PortableSSD/hermes-evals/standard-benchmarks/coding/qwen3-v4-peft-official-coding-rerun-20260624/generated.jsonl`
- EvalPlus results: `/Volumes/PortableSSD/hermes-evals/standard-benchmarks/coding/qwen3-v4-peft-official-coding-rerun-20260624/generated_eval_results.json`
- EvalPlus log: `/Volumes/PortableSSD/hermes-evals/standard-benchmarks/coding/qwen3-v4-peft-official-coding-rerun-20260624/evalplus-humaneval-no-memlimit.log`
- Generation summary: `/Volumes/PortableSSD/hermes-evals/standard-benchmarks/coding/qwen3-v4-peft-official-coding-rerun-20260624/generation-summary.json`

## Generation

Rows generated: `164`
Unique task IDs: `164`
Prompt mode: `completion`
Max tokens: `256`
Generation duration: `779.928s`

The generation shell returned nonzero because an initial `tee` target was
missing before the output directory existed. The generator itself completed and
the JSONL was validated before scoring.

## Scoring Command

```bash
source scripts/env.sh && EVALPLUS_MAX_MEMORY_BYTES=-1 \
/Volumes/PortableSSD/hermes-training-envs/benchmarks-py312/bin/python \
  -m evalplus.evaluate humaneval \
  --samples /Volumes/PortableSSD/hermes-evals/standard-benchmarks/coding/qwen3-v4-peft-official-coding-rerun-20260624/generated.jsonl \
  --test-details \
  --parallel 8 \
  --i-just-wanna-run
```

`EVALPLUS_MAX_MEMORY_BYTES=-1` was used on this macOS host to avoid the
EvalPlus memory guard issue observed in prior runs.
