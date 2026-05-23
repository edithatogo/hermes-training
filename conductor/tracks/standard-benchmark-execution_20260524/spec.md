# Specification: Standardized Benchmark Execution And Publication Readiness

## Overview

Create an execution-ready Conductor track for running standardized Hermes benchmark suites and preparing publishable evidence without performing expensive benchmark execution during track setup. The track decomposes the work into parallel lanes for local strict tool-call validation, standard benchmark suites, Azure scale-out execution, report and model-card preparation, and final Hugging Face/GitHub release gates.

This is a planning and readiness track. It should make future benchmark runs reproducible, comparable, and publication-safe while keeping all large artifacts, caches, logs, and reports on SSD-backed storage.

## Goals

- Define a single benchmark execution doctrine that agents can follow consistently across local and Azure lanes.
- Split work into parallelizable lanes so local Hermes strict tool-call checks, IFEval/BFCL/coding/lm-eval suites, Azure scale-out, reporting, and release gating can progress independently.
- Require benchmark manifests, environment capture, result cards, and raw artifacts before any public benchmark claim.
- Preserve SSD artifact policy for all large files and generated benchmark outputs.
- Prevent accidental spend, oversized local writes, or premature Hugging Face/GitHub publication.

## Parallel Execution Lanes

### Lane A - Local Hermes Strict Tool-Call

- Own local strict tool-call execution readiness for Hermes-compatible runtimes and OpenAI-compatible serving paths.
- Define small smoke and full strict-tool-call tiers with explicit prompts, datasets, runtime normalization, pass/fail thresholds, and output locations.
- Require raw outputs, normalized outputs, parser diagnostics, scorecards, runtime metadata, and command manifests for any future run.
- Treat local smoke results as runtime proof only until full strict tool-call evidence is produced and reviewed.

### Lane B - IFEval, BFCL, Coding, And lm-eval

- Own standardized benchmark harness readiness for IFEval, BFCL, coding benchmarks, and lm-eval tasks.
- Define per-suite configuration files, dataset versions, prompt templates, sampling settings, scoring scripts, expected result schemas, and comparison baselines.
- Separate cheap dry-runs and schema checks from full benchmark execution.
- Require result normalization so scores from local, Azure, and future reruns are comparable.

### Lane C - Azure Scale-Out

- Own cloud execution readiness for benchmark jobs that exceed local runtime limits.
- Keep quota, budget, account, region, workspace, compute, storage, and fail-closed checks ahead of any live run.
- Require job manifests, dry-run command validation, SSD-backed input/output sync plans, and post-run artifact download instructions.
- Block paid or persistent resources unless explicit quota, budget, and user approval gates are satisfied.

### Lane D - Report And Model-Card Publishing

- Own benchmark report, model-card, and evidence-pack preparation.
- Define report templates that include model/runtime identity, dataset versions, commands, environment, raw artifact locations, normalized metrics, limitations, and reproducibility notes.
- Prepare model-card sections for intended use, evaluation methodology, benchmark results, known failures, license, hardware, and artifact provenance.
- Keep draft publication materials local until release gates pass.

### Lane E - Hugging Face And GitHub Release Gates

- Own final public release readiness checks for Hugging Face and GitHub.
- Require explicit license compatibility, benchmark evidence, artifact review, model-card review, repository cleanliness, tag/release notes, and user approval before publication.
- Block public model, adapter, score, or report publication when evidence is incomplete, artifacts are off-SSD, scores are not reproducible, or benchmark runs were not normalized.

## SSD Artifact Policy

- All large generated artifacts, benchmark outputs, model caches, raw predictions, Azure synced outputs, reports, and temporary run directories must live under `/Volumes/PortableSSD`.
- Repository commits may include only lightweight manifests, templates, documentation, checksums, score summaries, and links or paths to SSD artifacts.
- No benchmark lane may write large outputs into the Git working tree unless the file is intentionally lightweight and reviewed for publication.
- Every future benchmark run must record the exact SSD root, relative artifact path, command manifest, environment metadata, and checksum or integrity note where practical.
- A run is not publication-ready if its raw evidence cannot be found under the declared SSD-backed artifact root.

## Requirements

- Create a readiness plan with independent lanes for local Hermes strict tool-call, IFEval/BFCL/coding/lm-eval, Azure scale-out, report/model-card publishing, and final Hugging Face/GitHub release gates.
- Include cheap validation steps such as syntax checks, configuration dry-runs, dataset presence checks, output-schema validation, and command-manifest review.
- Explicitly mark full benchmark execution, paid Azure jobs, large downloads, and public publication as out of scope for setup.
- Define handoff artifacts for each lane: checklist, manifest, expected outputs, evidence paths, blockers, and promotion gates.
- Preserve compatibility with existing repository doctrine in `requirements.md`, `design.md`, `contracts.md`, `STANDARD_BENCHMARKS.md`, `REPO_MAINTENANCE.md`, and `HANDOFF.md` where applicable.
- Keep track setup edits scoped to this track directory and the tracks registry unless a minimal documentation pointer is necessary.

## Acceptance Criteria

- The track contains `spec.md`, `plan.md`, `metadata.json`, and `index.md`.
- `conductor/tracks.md` contains an unchecked registry entry pointing to this track.
- The plan decomposes future work into the five required lanes and a final synthesis/checkpoint phase.
- The plan includes SSD artifact policy, no-expensive-benchmark guardrails, publication gates, and Azure fail-closed requirements.
- No expensive benchmarks, paid Azure jobs, model downloads, large artifact generation, Hugging Face publication, or GitHub release actions are run during setup.

## Out Of Scope

- Running full IFEval, BFCL, coding, lm-eval, or Hermes strict tool-call benchmark suites during setup.
- Creating Azure resources, submitting paid cloud jobs, or syncing large benchmark outputs during setup.
- Downloading models, datasets, or benchmark caches beyond cheap presence checks.
- Publishing model cards, adapters, benchmark reports, Hugging Face repositories, GitHub releases, or tags.
- Refactoring benchmark harness code unless a future implementation phase explicitly scopes it.
