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
- [x] Task: Conductor - Automated Review and Checkpoint 'Phase 1 - Shared Benchmark Doctrine And SSD Policy' (Protocol in workflow.md)

## Phase 2 - Lane A Local Hermes Strict Tool-Call

- [ ] Task: Define local strict tool-call tiers.
    - [x] Specify smoke, heldout, and full tiers with expected runtime, dataset path, prompts, parser settings, and output schema.
    - [x] Distinguish raw strict scores from runtime-normalized scores.
    - [x] Define minimum evidence for runtime proof versus publication-ready benchmark evidence.
- [ ] Task: Define local runtime matrix.
    - [x] Include Hermes-compatible local runtime, OpenAI-compatible endpoint, normalization wrapper, prompt format, context length, and sampling settings.
    - [x] Record command manifests and environment variables without launching expensive runs.
    - [x] Require SSD output roots for raw completions, normalized completions, parser diagnostics, and scorecards.
    - [x] Record first endpoint baselines for Ollama Hermes3, Ollama LFM2, and llama.cpp Qwen3 Q4_K_M.
- [ ] Task: Define local pass/fail gates.
    - [x] Fail publication if strict tool-call behavior is materially broken for an agent-positioned model.
    - [x] Require failure examples and parser diagnostics for any residual failures.
    - [x] Require reviewer sign-off before local results are used in model-card claims.
- [x] Task: Conductor - Automated Review and Checkpoint 'Phase 2 - Lane A Local Hermes Strict Tool-Call' (Protocol in workflow.md)

## Phase 3 - Lane B IFEval, BFCL, Coding, And lm-eval

- [ ] Task: Define standardized suite manifests.
    - [x] Create manifest expectations for IFEval, BFCL, coding benchmarks, and lm-eval tasks.
    - [x] Capture dataset version, task subset, prompt format, scoring command, output schema, and expected artifacts for each suite.
    - [x] Mark full execution as a future gated action, not a setup action.
- [ ] Task: Define cheap per-suite readiness checks.
    - [x] IFEval: validate config, prompt template, output schema, and score parser availability.
    - [x] BFCL: validate tool schema sources, generation format, parser expectations, and result-card schema.
    - [x] Coding: validate task source, sandbox assumptions, timeout policy, and result normalization fields.
    - [x] lm-eval: validate task list, model adapter invocation, batch-size policy, and output path.
- [ ] Task: Define score normalization and comparability rules.
    - [x] Preserve raw suite outputs alongside normalized summaries.
    - [x] Record benchmark harness version and repository commit for every future run.
    - [x] Require rerun notes when local and Azure results are compared.
- [x] Task: Conductor - Automated Review and Checkpoint 'Phase 3 - Lane B IFEval, BFCL, Coding, And lm-eval' (Protocol in workflow.md)

## Phase 4 - Lane C Azure Scale-Out

- [x] Task: Define Azure fail-closed gates.
    - [x] Require active account, subscription, region, quota, budget, workspace, compute, storage, and output path confirmation before live jobs.
    - [x] Block paid jobs, persistent GPU resources, and non-Spot compute unless explicitly approved.
    - [x] Reuse the Azure execution readiness doctrine instead of duplicating cloud setup details.
- [x] Task: Define Azure benchmark job manifests.
    - [x] Include benchmark suite, image/environment, command, inputs, outputs, compute target, timeout, max cost expectation, and SSD sync destination.
    - [x] Require dry-run command generation before any job submission.
    - [x] Require run logs and result artifacts to sync back under `/Volumes/PortableSSD`.
- [x] Task: Define cloud-to-local evidence reconciliation.
    - [x] Compare Azure outputs with local manifests and normalized schemas.
    - [x] Record job ID, logs, artifact path, checksum or integrity note, and any failed shards.
    - [x] Prevent report updates until cloud artifacts are present locally on SSD.
- [x] Task: Conductor - Automated Review and Checkpoint 'Phase 4 - Lane C Azure Scale-Out' (Protocol in workflow.md)

## Phase 5 - Lane D Report And Model-Card Publishing

- [x] Task: Define benchmark report template.
    - [x] Include executive summary, model/runtime identity, benchmark methodology, raw artifact paths, normalized metrics, known limitations, and reproducibility commands.
    - [x] Separate draft internal reports from publication-ready reports.
    - [x] Require links to SSD artifact roots rather than embedding large outputs in the repository.
- [x] Task: Define model-card benchmark sections.
    - [x] Cover intended use, evaluation suites, hardware/runtime, dataset versions, metrics, failure cases, license, and provenance.
    - [x] Require clear labeling for smoke, partial, full, local, and Azure results.
    - [x] Prohibit unsupported comparative claims or leaderboard-style claims without complete evidence.
- [x] Task: Define evidence-pack checklist.
    - [x] Include manifests, raw outputs, normalized summaries, logs, environment capture, checksums, report draft, and review decisions.
    - [x] Track unresolved blockers and explicit no-publish reasons.
    - [x] Require sign-off before model-card or report changes become public.
- [x] Task: Conductor - Automated Review and Checkpoint 'Phase 5 - Lane D Report And Model-Card Publishing' (Protocol in workflow.md)

## Phase 6 - Lane E Hugging Face And GitHub Release Gates

- [x] Task: Define Hugging Face release gate.
    - [x] Require license compatibility, model-card readiness, artifact provenance, file-size review, repository target, visibility decision, and explicit user approval.
    - [x] Block uploads when benchmark evidence is incomplete or artifacts are outside the declared SSD root.
    - [x] Require dry-run or staged release notes before public publication.
- [x] Task: Define GitHub release gate.
    - [x] Require clean scoped diff, benchmark report review, release notes, tag naming, artifact policy review, and explicit user approval.
    - [x] Block tags or releases while benchmark lanes remain unreviewed or publication claims are unresolved.
    - [x] Keep generated large artifacts out of Git history.
- [x] Task: Define final go/no-go checklist.
    - [x] Confirm local strict tool-call evidence.
    - [x] Confirm IFEval/BFCL/coding/lm-eval evidence or clearly labeled exclusions.
    - [x] Confirm Azure evidence if cloud execution was used.
    - [x] Confirm report and model-card review.
    - [x] Confirm Hugging Face and GitHub publication approvals.
- [x] Task: Conductor - Automated Review and Checkpoint 'Phase 6 - Lane E Hugging Face And GitHub Release Gates' (Protocol in workflow.md)

## Phase 7 - Final Synthesis And Handoff

- [x] Task: Produce a lane status summary.
    - [x] List ready, blocked, deferred, and explicitly out-of-scope benchmark work.
    - [x] Link each lane to manifests, artifact roots, and remaining blockers.
    - [x] Identify which future tasks can be run in parallel and which require release-gate sequencing.
- [x] Task: Validate setup-only scope.
    - [x] Confirm no expensive benchmarks were run.
    - [x] Confirm no Azure jobs or paid resources were created.
    - [x] Confirm no large artifacts were written into the Git working tree.
    - [x] Confirm all planned artifact roots point under `/Volumes/PortableSSD`.
- [x] Task: Update registry status only when the track is reviewed and ready for execution.
- [x] Task: Conductor - Automated Review and Checkpoint 'Phase 7 - Final Synthesis And Handoff' (Protocol in workflow.md)

## Health Check

- Target: >= 9.5 / 10
- Current estimate: 9.6 / 10
- Evidence: `reports/benchmark/manifests/standard-benchmark-manifest-20260524.md` defines suite tiers, SSD roots, required run records, no-run guardrails, suite-specific pilot manifests, and the current endpoint benchmark evidence.
- Additional evidence: local held-out, lm-eval smoke, and retrieval smoke command manifests now exist under `reports/benchmark/manifests/`.
- Endpoint harness: `scripts/run_endpoint_tool_call_benchmark.py` now allows the same strict suite to run against Ollama, LM Studio, MLX server, or the normalizing proxy through OpenAI-compatible endpoints.
- Endpoint baselines: `reports/benchmark/endpoint-tool-call/hermes3-8b-ollama-heldout-20260524.md` records `hermes3:8b` via Ollama at strict held-out `0.250`; `reports/benchmark/endpoint-tool-call/lfm2-2-6b-ollama-heldout-20260524.md` records `sam860/LFM2:2.6b` via Ollama at `0.250`; `reports/benchmark/endpoint-tool-call/qwen3-q4km-llamacpp-heldout-20260524.md` records the SSD-backed Qwen3 Q4_K_M GGUF via llama.cpp at `0.375`.
- Endpoint pilots: `reports/benchmark/endpoint-pilots/qwen3-q4km-llamacpp-pilots-20260524.md` records BFCL-style `0.333`, IFEval-style `0.667`, and coding sanity `1.000` for the Qwen3 Q4_K_M llama.cpp endpoint with `/no_think`.
- Publication gate: `reports/benchmark/publication-readiness-gate-20260524.md` records the evidence-pack requirement, current local scores, and no-publish decision.
- Remaining gap: full execution remains gated on runtime stability, local/SSD artifacts, useful Azure quota, and explicit approval for any paid or long-running jobs. The setup plan itself clears the 9.5 health target.
