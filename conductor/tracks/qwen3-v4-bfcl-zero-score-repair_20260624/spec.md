# Specification: Qwen3 v4 BFCL Zero-Score Repair

## Overview

The v4 official BFCL blocker has moved from endpoint/config reachability to a
scored failure. The selected BFCL categories generated/evaluated, but the
selected-slice score is `0.000`, so no BFCL capability claim is allowed.

## Source Evidence

- Result report:
  `reports/benchmark/official-candidates/qwen3-v4-official-bfcl-result-20260624.json`
- Generate log:
  `reports/benchmark/official-candidates/logs/qwen3-v4-official-bfcl-generate-20260624.log`
- Evaluate log:
  `reports/benchmark/official-candidates/logs/qwen3-v4-official-bfcl-evaluate-20260624.log`
- Raw BFCL root:
  `/Volumes/PortableSSD/hermes-evals/standard-benchmarks/bfcl/qwen3-v4-peft-official-bfcl-20260616`

## Goals

- Treat the selected-slice `0.000` BFCL score as a repair target, not a
  publication result.
- Inspect raw BFCL outputs for formatting, routing, model-id, and proxy
  normalization failures.
- Decide whether the fix belongs in the runtime/profile path, the adapter data,
  or the BFCL invocation/model mapping.
- Keep BFCL publication claims blocked until a rerun has nonzero and
  interpretable selected-slice evidence, followed by a separate full-scope
  decision.

## Acceptance Criteria

- Preserve the selected-slice score report and logs in Git.
- Add a failure analysis report that identifies why the BFCL scorer marked all
  selected categories `0.000`.
- Produce one repair recommendation with the minimal next rerun scope.
- Rerun selected categories only after the failure analysis identifies a
  concrete fix.

## Target Gates

- Selected-slice BFCL score improves above `0.000`.
- Raw BFCL outputs match the expected BFCL format for the selected categories.
- Publication boundary remains selected-slice only unless a full BFCL run is
  separately executed and reviewed.

## Out Of Scope

- Claiming full official BFCL leaderboard performance.
- Publishing v4 weights based on a selected-slice BFCL result.
- Mixing BFCL repair decisions into the v9 safety/refusal track.
