# Qwen3 v4 Official Coding Failure Analysis HF Artifact

- Dataset: `edithatogo/hermes-training-artifacts`
- Path: `qwen3-v4-official-coding-failure-analysis-20260624`
- Revision: `a6b40d3f61cbe80b18b861884d72ee5d578492e4`
- URL: <https://huggingface.co/datasets/edithatogo/hermes-training-artifacts/tree/a6b40d3f61cbe80b18b861884d72ee5d578492e4/qwen3-v4-official-coding-failure-analysis-20260624>

This is an evidence-only private artifact. It records diagnostic failure
analysis for the scored EvalPlus rerun and is not a new coding score.

## Summary

| Metric | Value |
| --- | ---: |
| HumanEval base pass@1 | 0.518 |
| HumanEval+ pass@1 | 0.482 |
| Pass both | 79 |
| Base fail | 79 |
| Plus-only fail | 6 |
| Empty completions | 23 |
| Syntax/pre-test failures | 13 |

Decision: targeted coding repair is worthwhile, but the first step should be a
generation/protocol repair pass rather than immediate broad fine-tuning.
