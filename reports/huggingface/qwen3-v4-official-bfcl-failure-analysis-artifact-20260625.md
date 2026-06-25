# Qwen3 v4 Official BFCL Failure Analysis HF Artifact

- Dataset: `edithatogo/hermes-training-artifacts`
- Path: `qwen3-v4-official-bfcl-failure-analysis-20260625`
- Revision: `1d3f724ea93e258fc821789605cbeff5c533e291`
- URL: <https://huggingface.co/datasets/edithatogo/hermes-training-artifacts/tree/1d3f724ea93e258fc821789605cbeff5c533e291/qwen3-v4-official-bfcl-failure-analysis-20260625>

This is an evidence-only private artifact. It records diagnostic BFCL failure
analysis for the scored selected-slice rerun and is not a new BFCL score.

## Summary

| Metric | Value |
| --- | ---: |
| Selected overall accuracy | 0.0065 |
| Non-live overall accuracy | 0.0646 |
| simple_python AST | 0.265 |
| multiple AST | 0.170 |
| parallel AST | 0.000 |
| Blank final results | 241 |
| Final answers without tool calls | 347 |
| Hidden reasoning tool calls not scored | 588 |
| Visible wrong-call-count rows | 61 |

Decision: targeted BFCL repair is worthwhile, but the first step should be a
runtime/proxy extraction and generation-contract repair pass rather than
immediate broad fine-tuning.
