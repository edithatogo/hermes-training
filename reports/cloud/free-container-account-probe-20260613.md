# Free Container Account Probe - 2026-06-13

This probe checked candidate free-tier or credit-backed container backends
without launching jobs, creating resources, uploading artifacts, or using paid
compute.

## Modal

- CLI: installed (`modal client version: 1.5.0`).
- Auth state: blocked. `modal token info` reports that no token is configured.
- Attempted unblock: `modal token new` opened a browser token flow, but the
  terminal flow did not complete before it was interrupted.
- Next user-assisted step:

```bash
modal token new
modal token info
modal profile list
```

After a token is configured, confirm free credits or an academic grant before
adding any GPU submitter.

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

Kaggle remains the strongest already-prepared no-cost GPU path once
authenticated. Modal is the best custom-container candidate after token setup.
Lightning is promising because the account is logged in and GPU machine types
are visible, but it cannot list or run Studio/Job resources until the Teamspace
owner is fixed.
