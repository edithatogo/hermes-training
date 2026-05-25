# Specification: Qwen3 V4 Pilot Failure Analysis

Analyze the Qwen3 v4 and v5 local pilot failures and define the next safe
adapter-improvement plan without training a new adapter.

Acceptance criteria:

- Record exact residual BFCL-style and IFEval-style pilot failures.
- Compare v4, strict-compatible v5, and superseded mixed-draft v5 behavior.
- Preserve v4 as the public adapter and v5 as a non-promotion result.
- Define guardrails for any future v6 attempt so held-out strict quality is not
  traded away for pilot polish.
- Validation passes.
