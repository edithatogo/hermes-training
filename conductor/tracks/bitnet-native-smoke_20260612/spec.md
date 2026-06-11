# Specification: BitNet Native Runtime Smoke

Prove whether the local specialist-runtime lane can run a BitNet b1.58 model
through the native BitNet checkout on the Mac without downloading new artifacts.

Acceptance criteria:

- Refresh the no-download specialist-runtime preflight so repo-local runtimes
  are detected.
- Confirm the native BitNet runtime and SSD-backed model file exist.
- Run a bounded BitNet prompt with a small context and token cap.
- Store raw logs under `/Volumes/PortableSSD/hermes-evals`.
- Track a markdown report under `reports/runtime`.
- Update queue and candidate notes without claiming Hermes readiness if prompt
  compliance fails.
- Validation passes.
