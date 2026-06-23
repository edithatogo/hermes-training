# Qwen3 v4 Official Coding Generation Attempt

Attempt ID: `qwen3-v4-peft-official-coding-generation-smoke-20260624`
Status: `blocked-runtime-fetch`
Suite: `official-coding`
Run ID: `qwen3-v4-peft-official-coding-20260616`
Candidate: `qwen3-4b-strict-toolcall-v4-targeted`

This is a generation runtime-attempt blocker only. It is not an EvalPlus score and must not be used as benchmark evidence.

## Command

```bash
/Volumes/PortableSSD/hermes-training-envs/benchmarks-py312/bin/python scripts/generate_humaneval_mlx_solutions.py --limit 1 --output /Volumes/PortableSSD/hermes-evals/standard-benchmarks/coding/qwen3-v4-peft-official-coding-20260616/generation-smoke-20260624.jsonl --summary-output /Volumes/PortableSSD/hermes-evals/standard-benchmarks/coding/qwen3-v4-peft-official-coding-20260616/generation-smoke-20260624-summary.json --max-tokens 128
```

## Result

The MLX HumanEval generator is wired and HumanEval data is available, but model acquisition stalled before the local `Qwen/Qwen3-4B-MLX-4bit` runtime loaded. The run was stopped after it remained at `Fetching 7 files: 29%`; no EvalPlus-shaped generated sample was produced.

## Next Action

Set `HF_HOME`, `HUGGINGFACE_HUB_CACHE`, `HF_XET_CACHE`, and `TRANSFORMERS_CACHE` to `/Volumes/PortableSSD`-backed paths; authenticate or provide `HF_TOKEN`; prefetch `Qwen/Qwen3-4B-MLX-4bit` and the local adapter dependencies; rerun the one-problem generation smoke; then generate all 164 HumanEval rows before EvalPlus execution.
