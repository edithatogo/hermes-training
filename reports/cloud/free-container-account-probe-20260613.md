# Free Container Account Probe - 2026-06-13

This probe checked candidate free-tier or credit-backed container backends
without launching jobs, creating resources, uploading artifacts, or using paid
compute.

## Modal

- CLI: installed (`modal client version: 1.5.0`).
- Auth state: authenticated. The browser-assisted `modal token new` flow
  completed on 2026-06-13 and connected the CLI to the `d-a-mordaunt`
  workspace. Token details are intentionally not recorded in this repo.
- Billing probe: `modal billing report --for "this month" --json` returned an
  empty JSON array. This confirms no current-month billable usage was visible
  through the CLI, but it does not prove free GPU credits or grant allowance.
- Submitter state: a guarded dry-run submitter now exists at
  `scripts/submit_modal_peft_scorecard.py`, with evidence in
  `reports/cloud/qwen3-v4-peft-modal-submit-dry-run-20260614.json`. It does not
  launch work unless explicit run and zero-cost-compute confirmations are both
  supplied.
- Remaining gates:
  - confirm free credits, academic grant, or other zero-cost allowance;
  - record non-secret GPU policy evidence;
  - execute only after explicit approval and recover result artifacts.
- Next step:

```bash
modal profile list
modal billing
```

Do not launch GPU work until the credit/grant and GPU policy gates are proven.

## Kaggle

- CLI: installed (`Kaggle CLI 2.2.1`).
- Auth state: authenticated. The browser-assisted OAuth flow completed on
  2026-06-13 and the CLI reports the local account as `edithatogo`.
- Quota state: visible through the authenticated SDK fallback. GPU quota is
  `108000s` total / `0s` used; TPU quota is `72000s` total / `0s` used; refresh
  is `2026-06-20T00:00:00Z`. The public `kaggle quota` command still fails with
  a CLI parsing error, so use the preflight report as the quota proof.
- Remaining gates:
  - push/run the staged kernel only after explicit confirmation.
- Notebook contract: passed in
  `reports/cloud/qwen3-v4-peft-kaggle-contract-20260614.md` with public inputs
  only, no private data upload, no `--limit`, and the explicit
  `--execute --confirm-kaggle-run` boundary.
- Next step:

```bash
./.venv/bin/python scripts/cloud_backend_preflight.py
./.venv/bin/python scripts/submit_kaggle_peft_scorecard.py
```

## Lightning AI

- CLI: installed (`Lightning CLI version 2026.06.08post0`).
- Login state: `lightning login` reports the current account as `damordaunt`.
- Machine catalog: visible, including `T4`, `L4`, `L40S`, `A100`, `H100`,
  `H200`, and multi-GPU variants.
- Blocker: default teamspace is `None/None`. `lightning studio list`,
  `lightning studio list --all`, `lightning job list --all`, and a trial
  `--teamspace damordaunt/default` override all still fail with a Teamspace
  owner error.
- Next user-assisted step:

```bash
lightning config set teamspace <owner>/<teamspace>
lightning studio list --teamspace <owner>/<teamspace>
lightning job list --teamspace <owner>/<teamspace>
```

After a valid teamspace is configured, confirm free monthly credits/GPU hours
and choose a low-cost machine type such as `T4` or `L4` before adding a guarded
Lightning scorecard submitter.

## Current Decision

Kaggle is now the strongest prepared no-cost GPU path if dataset terms and the
notebook execution contract pass. Modal is the best custom-container candidate
once free credit/grant and GPU policy evidence are confirmed.
Lightning is promising because the account is logged in and GPU machine types
are visible, but it cannot list or run Studio/Job resources until the Teamspace
owner is fixed.
