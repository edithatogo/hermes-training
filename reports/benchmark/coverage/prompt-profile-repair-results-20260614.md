# Prompt/Profile Repair Results

Run ID: `prompt-profile-repair-results-20260614`
Created: `2026-06-14T03:20:00+00:00`

Purpose: append real prompt/profile repair benchmark outcomes without treating failed repairs as promotion evidence.

## Results

| Candidate | Variant | Runner | Status | Pass rate | Report |
|---|---|---|---|---:|---|
| `Qwen/Qwen3.5-0.8B` | `strict-suffix-copy-exact` | `local` | `completed-no-promotion` | 0.000 | `reports/benchmark/local-pilots/qwen35-08b-strict-suffix-copy-exact-repair-20260614.md` |
| `Qwen/Qwen3.5-0.8B` | `qwen-no-think-prefill` | `local` | `completed-no-promotion` | 0.333 | `reports/benchmark/local-pilots/qwen35-08b-qwen-no-think-prefill-repair-20260614.md` |

## Decision Boundary

- A completed repair run is only evidence for the tested prompt/profile variant.
- Failed repair evidence must keep the candidate out of promotion and feed the next variant choice.
- Promotion still requires raw strict outputs plus held-out tool-call, local pilot, official benchmark, latency, rollback, and publication gates.
