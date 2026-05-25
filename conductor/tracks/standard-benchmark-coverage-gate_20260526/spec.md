# Specification: Standard Benchmark Coverage Gate

Close the immediate documentation and readiness gaps around official benchmark
coverage without starting long-running benchmark jobs, downloading large model
or dataset artifacts, or spending cloud budget.

Acceptance criteria:

- Formalize the follow-on benchmark coverage work in Conductor so the gap is
  no longer represented by an empty orphan track directory.
- Keep the `lm-eval-selected` lane explicit: it is attempted but blocked until
  the local MLX/OpenAI-compatible path can satisfy loglikelihood requests.
- Update the OpenAI normalizing proxy with the narrow compatibility behavior
  needed by `lm_eval --model local-completions` against `mlx_lm.server`:
  completions passthrough and integer-to-boolean `logprobs` coercion.
- Align the BFCL command manifest with the installed `bfcl` CLI rather than
  stale `python -m bfcl_eval` invocation shapes.
- Add lightweight validation so official benchmark manifests fail closed when
  they drift from the installed harness interfaces.
- Correct stale model-radar wording for runtime-proven LFM lanes and mem0
  reranker packaging/source-model distinctions.
- Keep all generated benchmark outputs on `/Volumes/PortableSSD`; this track
  may add only lightweight code, tests, reports, and manifests to Git.
