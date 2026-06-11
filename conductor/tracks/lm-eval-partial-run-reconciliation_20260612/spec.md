# Specification: lm-eval Partial Run Reconciliation

Reconcile the full selected-task MLX lm-eval attempt that stopped after one of
five tasks, so the repository records useful evidence without overstating the
benchmark result.

Acceptance criteria:

- Convert the untracked full-run report from `running` to a clear partial /
  interrupted attempt.
- Preserve the completed ARC Challenge metric while making the four missing
  tasks explicit.
- Keep `lm-eval-selected` marked missing for full candidate claims.
- Update the standard benchmark coverage notes to reference the partial full
  attempt without promoting it.
- Validation passes.

