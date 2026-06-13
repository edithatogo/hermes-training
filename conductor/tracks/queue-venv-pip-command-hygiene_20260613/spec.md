# Specification: Queue Venv Pip Command Hygiene

## Overview

Generated proof queues should use the same Python environment for optional
dependency installation and benchmark execution. The runtime proof action queue
and mem0 candidate queue previously emitted `python -m pip install ...` for
some optional dependencies while immediately running benchmarks through
`./.venv/bin/python`. That can install into the wrong interpreter on macOS and
make a queued proof fail or mutate the wrong environment.

## Goals

- Pin runtime proof support-model dependency installs to `./.venv/bin/python -m pip`.
- Pin mem0 reranker optional dependency installs to `./.venv/bin/python -m pip`.
- Regenerate both queue artifacts.
- Keep the change limited to generated command hygiene, with no new benchmark or promotion claims.

## Acceptance Criteria

- Runtime proof support-model command tests reject bare `python -m pip install`.
- mem0 cross-encoder reranker command tests reject bare `python -m pip install`.
- `reports/benchmark/coverage/runtime-proof-action-queue-20260613.*` is regenerated.
- `reports/model-radar/mem0-candidate-queue.md` is regenerated.
- Runtime proof and mem0 queue validators pass.

## Out Of Scope

- Installing dependencies.
- Running new model benchmarks.
- Changing candidate priorities or default model choices.
