# Free Container Account Probe - 2026-06-13

This probe checked candidate free-tier or credit-backed container backends
without launching jobs, creating resources, uploading artifacts, or using paid
compute.

## Modal

- CLI: installed (`modal client version: 1.5.0`).
- Auth state: authenticated. The browser-assisted `modal token new` flow
  completed on 2026-06-13 and connected the CLI to the `d-a-mordaunt`
  workspace. Token details are intentionally not recorded in this repo.
- Remaining gates:
  - confirm free credits, academic grant, or other zero-cost allowance;
  - record non-secret GPU policy evidence;
  - add a fail-closed Modal scorecard submitter with result persistence.
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
- Remaining gates:
  - resolve quota visibility: `kaggle quota` currently fails with a CLI parsing
    error before reporting weekly accelerator quota;
  - review dataset terms and avoid private data uploads;
  - push/run the staged kernel only after explicit confirmation.
- Next step:

```bash
kaggle quota
kaggle kernels list --mine --page-size 1
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

Kaggle is now the strongest prepared no-cost GPU path if quota and dataset terms
pass. Modal is the best custom-container candidate once free credit/grant and
GPU policy evidence are confirmed.
Lightning is promising because the account is logged in and GPU machine types
are visible, but it cannot list or run Studio/Job resources until the Teamspace
owner is fixed.
