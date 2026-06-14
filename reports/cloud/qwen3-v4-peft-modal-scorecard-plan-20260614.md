# Qwen3 V4 PEFT Modal Scorecard Plan

Status: `prepared-needs-credit-and-gpu-policy-check`

## Rationale

Modal is authenticated for the `d-a-mordaunt` workspace and can provide a
custom-container route if free credit/grant and GPU policy gates are confirmed.
It is useful as a fallback to Colab pruning and HF Jobs credit limits, but it
must stay fail-closed until zero-cost compute is proven.

## Prepared Artifact

Modal app:

```text
scripts/modal_peft_lm_eval_selected.py
```

Guarded submitter:

```text
scripts/submit_modal_peft_scorecard.py
```

Dry-run submission artifact:

```text
reports/cloud/qwen3-v4-peft-modal-submit-dry-run-20260614.json
```

Policy gate artifact:

```text
reports/cloud/modal-policy-gate-20260614.md
```

Staged config folder:

```text
reports/cloud/modal-qwen3-v4-peft-scorecard-20260614
```

## Current Blocker

`modal profile list` confirms the authenticated workspace and
`modal billing report --for "this month" --json` returned an empty JSON array,
but that is only no-current-month-usage evidence. It does not prove free GPU
credits, grant allowance, or accepted GPU policy. No Modal job was submitted.
The policy gate report now records this fail-closed boundary and keeps
`execution_allowed=false`.

## Stop Conditions

- No Modal run without `--execute --confirm-modal-run --confirm-zero-cost-compute`.
- No Modal run while `reports/cloud/modal-policy-gate-20260614.json` has
  `execution_allowed=false`, unless a deliberate post-verification override is
  recorded.
- No no-limit benchmark claim until every configured task completes without
  `--limit` and artifacts are recovered locally.
- No private data upload; the Modal app uses the public PEFT adapter and public
  benchmark tasks.
