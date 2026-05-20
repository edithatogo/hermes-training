# Spec: Azure Scale-Out Preflight and Benchmark Lane

## Goal

Use the Azure Students hours on `d.a.mordaunt@gmail.com` to accelerate Hermes-agent benchmark and teacher/evaluator workflows without creating uncontrolled cloud spend.

## Requirements

- Azure is a scale-out lane for benchmarks, teacher/evaluator runs, dataset review, and selected larger LoRA/QLoRA experiments.
- No compute creation or job submission may happen until account, subscription, Azure ML extension, region, quota, and cost policy pass preflight.
- Default cost policy is Spot/low-priority, `min_instances: 0`, `max_instances: 1`, and one GPU job at a time.
- Local artifacts synced from Azure must land under `/Volumes/PortableSSD`.
- Initial cloud use is benchmark and teacher/evaluator work, not broad training sweeps.
- Health target: `>= 9.5 / 10`.

## Acceptance Criteria

- Azure preflight command exists and is documented.
- Preflight can identify when the active CLI account is not the Gmail student account.
- Azure ML CLI extension missing state is surfaced.
- Track plan includes quota, job-template, benchmark, and run-card phases.
- Readiness validation passes.
