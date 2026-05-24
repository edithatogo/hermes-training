# Plan: Standardized Benchmark Execution And Publication Readiness

## Phase 1 - Shared Benchmark Doctrine And SSD Policy

- [x] Task: Define the benchmark execution manifest.
    - [x] Include model identity, runtime, commit, environment, benchmark suite, dataset version, prompt template, sampling settings, command, output schema, artifact root, and reviewer.
    - [x] Require every future run to declare an SSD-backed artifact path under `/Volumes/PortableSSD`.
    - [x] Separate lightweight repo-tracked manifests from large SSD-only outputs.
- [x] Task: Define global no-run and no-publish guardrails.
    - [x] Block expensive benchmark execution during setup.
    - [x] Block large model, dataset, cache, or result writes into the Git working tree.
    - [x] Block public claims without raw outputs, normalized scores, environment capture, and review.
    - [x] Block publication when artifact evidence is missing from the declared SSD root.
- [x] Task: Define cheap readiness validation.
    - [x] Prefer syntax checks, manifest linting, dry-run command generation, dataset path presence checks, and output-schema validation.
    - [x] Record skipped expensive commands with reason and future owner.
    - [x] Keep validation reproducible from documented commands.
- [ ] Task: Conductor - Automated Review and Checkpoint 'Phase 1 - Shared Benchmark Doctrine And SSD Policy' (Protocol in workflow.md)

## Phase 2 - Lane A Local Hermes Strict Tool-Call

- [ ] Task: Define local strict tool-call tiers.
    - [ ] Specify smoke, heldout, and full tiers with expected runtime, dataset path, prompts, parser settings, and output schema.
    - [ ] Distinguish raw strict scores from runtime-normalized scores.
    - [ ] Define minimum evidence for runtime proof versus publication-ready benchmark evidence.
- [ ] Task: Define local runtime matrix.
    - [ ] Include Hermes-compatible local runtime, OpenAI-compatible endpoint, normalization wrapper, prompt format, context length, and sampling settings.
    - [ ] Record command manifests and environment variables without launching expensive runs.
    - [ ] Require SSD output roots for raw completions, normalized completions, parser diagnostics, and scorecards.
- [ ] Task: Define local pass/fail gates.
    - [ ] Fail publication if strict tool-call behavior is materially broken for an agent-positioned model.
    - [ ] Require failure examples and parser diagnostics for any residual failures.
    - [ ] Require reviewer sign-off before local results are used in model-card claims.
- [ ] Task: Conductor - Automated Review and Checkpoint 'Phase 2 - Lane A Local Hermes Strict Tool-Call' (Protocol in workflow.md)

## Phase 3 - Lane B IFEval, BFCL, Coding, And lm-eval

- [ ] Task: Define standardized suite manifests.
    - [ ] Create manifest expectations for IFEval, BFCL, coding benchmarks, and lm-eval tasks.
    - [ ] Capture dataset version, task subset, prompt format, scoring command, output schema, and expected artifacts for each suite.
    - [ ] Mark full execution as a future gated action, not a setup action.
- [ ] Task: Define cheap per-suite readiness checks.
    - [ ] IFEval: validate config, prompt template, output schema, and score parser availability.
    - [ ] BFCL: validate tool schema sources, generation format, parser expectations, and result-card schema.
    - [ ] Coding: validate task source, sandbox assumptions, timeout policy, and result normalization fields.
    - [ ] lm-eval: validate task list, model adapter invocation, batch-size policy, and output path.
- [ ] Task: Define score normalization and comparability rules.
    - [ ] Preserve raw suite outputs alongside normalized summaries.
    - [ ] Record benchmark harness version and repository commit for every future run.
    - [ ] Require rerun notes when local and Azure results are compared.
- [ ] Task: Conductor - Automated Review and Checkpoint 'Phase 3 - Lane B IFEval, BFCL, Coding, And lm-eval' (Protocol in workflow.md)

## Phase 4 - Lane C Azure Scale-Out

- [ ] Task: Define Azure fail-closed gates.
    - [ ] Require active account, subscription, region, quota, budget, workspace, compute, storage, and output path confirmation before live jobs.
    - [ ] Block paid jobs, persistent GPU resources, and non-Spot compute unless explicitly approved.
    - [ ] Reuse the Azure execution readiness doctrine instead of duplicating cloud setup details.
- [ ] Task: Define Azure benchmark job manifests.
    - [ ] Include benchmark suite, image/environment, command, inputs, outputs, compute target, timeout, max cost expectation, and SSD sync destination.
    - [ ] Require dry-run command generation before any job submission.
    - [ ] Require run logs and result artifacts to sync back under `/Volumes/PortableSSD`.
- [ ] Task: Define cloud-to-local evidence reconciliation.
    - [ ] Compare Azure outputs with local manifests and normalized schemas.
    - [ ] Record job ID, logs, artifact path, checksum or integrity note, and any failed shards.
    - [ ] Prevent report updates until cloud artifacts are present locally on SSD.
- [ ] Task: Conductor - Automated Review and Checkpoint 'Phase 4 - Lane C Azure Scale-Out' (Protocol in workflow.md)

## Phase 5 - Lane D Report And Model-Card Publishing

- [ ] Task: Define benchmark report template.
    - [ ] Include executive summary, model/runtime identity, benchmark methodology, raw artifact paths, normalized metrics, known limitations, and reproducibility commands.
    - [ ] Separate draft internal reports from publication-ready reports.
    - [ ] Require links to SSD artifact roots rather than embedding large outputs in the repository.
- [ ] Task: Define model-card benchmark sections.
    - [ ] Cover intended use, evaluation suites, hardware/runtime, dataset versions, metrics, failure cases, license, and provenance.
    - [ ] Require clear labeling for smoke, partial, full, local, and Azure results.
    - [ ] Prohibit unsupported comparative claims or leaderboard-style claims without complete evidence.
- [ ] Task: Define evidence-pack checklist.
    - [ ] Include manifests, raw outputs, normalized summaries, logs, environment capture, checksums, report draft, and review decisions.
    - [ ] Track unresolved blockers and explicit no-publish reasons.
    - [ ] Require sign-off before model-card or report changes become public.
- [ ] Task: Conductor - Automated Review and Checkpoint 'Phase 5 - Lane D Report And Model-Card Publishing' (Protocol in workflow.md)

## Phase 6 - Lane E Hugging Face And GitHub Release Gates

- [ ] Task: Define Hugging Face release gate.
    - [ ] Require license compatibility, model-card readiness, artifact provenance, file-size review, repository target, visibility decision, and explicit user approval.
    - [ ] Block uploads when benchmark evidence is incomplete or artifacts are outside the declared SSD root.
    - [ ] Require dry-run or staged release notes before public publication.
- [ ] Task: Define GitHub release gate.
    - [ ] Require clean scoped diff, benchmark report review, release notes, tag naming, artifact policy review, and explicit user approval.
    - [ ] Block tags or releases while benchmark lanes remain unreviewed or publication claims are unresolved.
    - [ ] Keep generated large artifacts out of Git history.
- [ ] Task: Define final go/no-go checklist.
    - [ ] Confirm local strict tool-call evidence.
    - [ ] Confirm IFEval/BFCL/coding/lm-eval evidence or clearly labeled exclusions.
    - [ ] Confirm Azure evidence if cloud execution was used.
    - [ ] Confirm report and model-card review.
    - [ ] Confirm Hugging Face and GitHub publication approvals.
- [ ] Task: Conductor - Automated Review and Checkpoint 'Phase 6 - Lane E Hugging Face And GitHub Release Gates' (Protocol in workflow.md)

## Phase 7 - Final Synthesis And Handoff

- [ ] Task: Produce a lane status summary.
    - [ ] List ready, blocked, deferred, and explicitly out-of-scope benchmark work.
    - [ ] Link each lane to manifests, artifact roots, and remaining blockers.
    - [ ] Identify which future tasks can be run in parallel and which require release-gate sequencing.
- [ ] Task: Validate setup-only scope.
    - [ ] Confirm no expensive benchmarks were run.
    - [ ] Confirm no Azure jobs or paid resources were created.
    - [ ] Confirm no large artifacts were written into the Git working tree.
    - [ ] Confirm all planned artifact roots point under `/Volumes/PortableSSD`.
- [ ] Task: Update registry status only when the track is reviewed and ready for execution.
- [ ] Task: Conductor - Automated Review and Checkpoint 'Phase 7 - Final Synthesis And Handoff' (Protocol in workflow.md)

## Health Check

- Target: >= 9.5 / 10
- Current estimate: 9.1 / 10
- Evidence: `reports/benchmark/manifests/standard-benchmark-manifest-20260524.md` defines suite tiers, SSD roots, required run records, and no-run guardrails. Health remains below completion threshold until suite-specific manifests and real benchmark evidence are produced.
- Additional evidence: local held-out, lm-eval smoke, and retrieval smoke command manifests now exist under `reports/benchmark/manifests/`.
- Endpoint harness: `scripts/run_endpoint_tool_call_benchmark.py` now allows the same strict suite to run against Ollama, LM Studio, MLX server, or the normalizing proxy through OpenAI-compatible endpoints.
- First endpoint baseline: `reports/benchmark/endpoint-tool-call/hermes3-8b-ollama-heldout-20260524.md` records `hermes3:8b` via Ollama at strict held-out `0.250`.
