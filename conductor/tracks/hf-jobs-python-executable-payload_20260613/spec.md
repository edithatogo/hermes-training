# Specification: HF Jobs Python Executable Payload

## Overview

The guarded HF Jobs scorecard submitter builds a remote `bash -lc` payload that
installs evaluation dependencies and then runs the downloaded scorecard script.
The payload previously hard-coded `python` in both places. That is usually fine
for the selected PyTorch image, but making the interpreter explicit in the
submitter contract lets future images use `python3` or another interpreter
without hand-editing the shell payload.

## Goals

- Add a `python_executable` field to the HF Jobs scorecard spec.
- Use the selected interpreter for both dependency installation and script execution.
- Expose `--python-executable` on the dry-run submitter CLI.
- Record the chosen interpreter in the dry-run JSON.

## Acceptance Criteria

- Unit tests prove a custom interpreter is reflected in the remote payload.
- The default dry-run still uses `python`.
- The dry-run JSON records `python_executable`.
- No HF Jobs job is submitted.

## Out Of Scope

- Running HF Jobs.
- Changing the default container image.
- Changing paid-compute or credit-blocker gates.
