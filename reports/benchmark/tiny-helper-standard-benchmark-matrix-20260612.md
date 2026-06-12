# Tiny Helper Standard Benchmark Matrix - 2026-06-12

## Summary

The tiny helper lane is now explicit in `RUNTIME_PROMPT_PROFILES.yaml` via
`tiny-helper-no-prefill`. This report maps that lane to the repo's standard
benchmark contract and records the current publication status.

The relevant candidates are:

- `Qwen/Qwen3.5-0.8B`
- `Qwen/Qwen3.5-2B`
- `openbmb/MiniCPM5-1B-MLX`

`LGAI-EXAONE/EXAONE-4.0-1.2B-GGUF` remains a comparison lane only.

## Evidence Already In Hand

| Candidate | Hermes-local evidence | BFCL-style evidence | Runtime status |
|---|---|---|---|
| `Qwen/Qwen3.5-0.8B` | One-case MLX loglikelihood smoke passed; helper role still blocked by strict formatting | Raw 3-case tiny BFCL-style pilot failed at `0.000` | MLX-load-proven |
| `Qwen/Qwen3.5-2B` | One-case MLX loglikelihood smoke passed; helper role still blocked by strict formatting | Raw 3-case tiny BFCL-style pilot failed at `0.000` | MLX-load-proven |
| `openbmb/MiniCPM5-1B-MLX` | One-case MLX loglikelihood smoke passed; helper role still blocked by strict formatting | Raw 3-case tiny BFCL-style pilot failed at `0.000` | MLX-load-proven |
| `LGAI-EXAONE/EXAONE-4.0-1.2B-GGUF` | Runtime proof only; repeated-brace output is not a strict Hermes candidate | Not promoted | GGUF runtime-proven |

## Prompt Coverage Check

The repo's standard prompt sets already satisfy the documented coverage target.

| Prompt set | Total | Coverage result |
|---|---:|---|
| `gemma4/eval/prompts.jsonl` | 100 | Pass |
| `lfm2/eval/prompts.jsonl` | 100 | Pass |

The audited category mix matches the repo plan:

- tool_use: 25
- code: 20
- long_context: 15
- reasoning: 15
- safety: 10
- factual: 10
- formatting: 5

## Standard Benchmark Matrix

| Area | Primary benchmark | Current status for tiny-helper lane |
|---|---|---|
| Hermes-local | Expanded local prompt set, tool-call validator | 100-prompt pass recorded for Qwen3.5 0.8B/2B and MiniCPM5 1B MLX; strict tool-call shape still fails |
| Instruction following | IFEval + expanded Hermes-local eval | Tiny Qwen helper IFEval pilot ran and failed at `0.000` |
| Function/tool calling | BFCL subset + held-out strict local suite | Local tiny BFCL-style gate failed; held-out gate not yet justified |
| Coding | HumanEval / MBPP | Tiny Qwen helper coding pilot ran and failed at `0.000` |
| Safety/refusal | XSTest / SimpleSafetyTests / HarmBench subset | Not yet run for this lane |
| Long context | RULER | Not applicable to these tiny helper lanes |
| Retrieval/embedding | MTEB / retrieval eval | Not applicable unless the lane is repurposed as an embedder |

## Publication Status

The tiny helper lane is **not** a publication candidate.

Reasons:

1. Strict tool-call formatting is not yet proven.
2. Standardized benchmark evidence is incomplete.
3. The lane is currently useful as a helper/extraction comparison surface, not
   as a public Hermes adapter.

## Recommended Next Gate

Run only the lightweight, lane-appropriate tests first:

1. Hermes-local expanded prompt set
2. IFEval subset
3. BFCL subset
4. HumanEval/MBPP subset if the candidate is also being considered for code
   assistance

Keep standard benchmark claims blocked until the reports exist and are tied to
exact commands and raw artifacts.
