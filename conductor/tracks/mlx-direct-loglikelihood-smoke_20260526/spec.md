# Specification: MLX Direct Loglikelihood Smoke Harness

Create a valid next path for selected `lm-eval` tasks that require
loglikelihood scoring. The OpenAI-compatible `mlx_lm.server` bridge cannot
produce legacy echoed prompt `token_logprobs`, so the next path must score
prompt/continuation pairs directly from MLX logits.

Acceptance criteria:

- Add a prompt/continuation JSONL smoke suite.
- Add a direct MLX scoring script with no-download mock mode for schema tests.
- Add a direct `lm_eval` adapter scaffold for loglikelihood-only tasks.
- Write SSD-backed smoke artifacts and a tracked report.
- Reflect the diagnostic harness in the standard benchmark coverage report
  without claiming official `lm-eval` scores.
