# Specification: Cloud Blocked Matrix Modal Lightning Mapping

## Overview

The cloud preflight registry and unblock checklist now include Modal and
Lightning as fail-closed candidate backends. The active blocked-track matrix
classifier still mapped only Colab, HF Jobs, Azure, NGC, and Kaggle, so any
future blocked Modal or Lightning track would appear as `unknown` and would not
inherit the backend-specific blocker and operator commands.

## Goals

- Map track IDs or titles containing Modal to the `modal` backend.
- Map track IDs or titles containing Lightning to the `lightning` backend.
- Add regression tests for both mappings.
- Confirm the current blocked-track matrix remains valid.

## Acceptance Criteria

- Modal track names classify as `modal`.
- Lightning track names classify as `lightning`.
- Existing cloud blocker reports validate.
- No remote jobs, auth commands, or downloads are run.

## Out Of Scope

- Creating Modal or Lightning scorecard tracks.
- Submitting cloud jobs.
- Changing existing blocked-track statuses.
