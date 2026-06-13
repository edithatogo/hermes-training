# Roadmap Regression and Publication Gate - 2026-06-12

## Scope

This gate reconciles the public-facing model roadmap after the 2026-06-12 model-radar, runtime-proof, mem0, and cloud/offload tracks.

Checked sources:

- `FUTURE_MODELS.md`
- `MODEL_CANDIDATES.yaml`
- `mem0/MODEL_CANDIDATES.yaml`
- `RUNTIME_FORMAT_PROOF_QUEUE.yaml`
- `HANDOFF.md`
- `reports/model-radar/*20260612.md`
- `reports/benchmark/**`
- `reports/runtime/**`
- `reports/publication/**`

## Source-of-Truth Contract

| Artifact | Authority | Publication rule |
|---|---|---|
| Benchmark and runtime reports | Execution evidence | Use as the source for measured claims only. Failed runs stay recorded as evidence. |
| `MODEL_CANDIDATES.yaml` | Structured Hermes candidate state | Candidate status, role, environment, license notes, and first gate must match the roadmap summary. |
| `FUTURE_MODELS.md` | Operator roadmap synthesis | Can summarize and prioritize, but cannot promote a model beyond evidence in reports and YAML. |
| `mem0/MODEL_CANDIDATES.yaml` | Structured mem0 candidate state | Retrieval/extraction defaults and challengers stay separate from chat/SFT lanes. |
| `RUNTIME_FORMAT_PROOF_QUEUE.yaml` | Runtime proof queue | Local, cloud, GGUF, MLX, specialist, and hosted lanes must stay distinguishable. |
| `HANDOFF.md` | Next-action operator summary | Must identify the immediate lane, blockers, and no-publish boundaries. |

## Consistency Result

The current roadmap and candidate metadata agree at the role level:

- Hermes local adapter target remains `Qwen/Qwen3-4B-MLX-4bit`.
- Qwen3.5 0.8B/2B and MiniCPM5 1B remain helper/extraction candidates, not strict Hermes promotions.
- Hermes 4.3, Harmonic/Harmonic-Hermes, Qwen3.6, Gemma 4, Nemotron, DeepSeek, Step, Command A+, and other large/specialist additions remain runtime, teacher, or specialist lanes.
- mem0 defaults remain unchanged: `nomic-embed-text:latest` for embeddings, Qdrant for vector storage, and the explicit read wrapper for reranking experiments.
- BGE-M3, Jina v5 omni MLX, EmbeddingGemma, Qwen3 embedding/reranker, and MLX BGE reranking are candidate lanes that require side-by-side benchmark and migration evidence before default promotion.
- Runtime proof is not fine-tune proof, and cloud/offload proof is not Mac-local compatibility proof.

No roadmap-level edit was required for `FUTURE_MODELS.md` or root `MODEL_CANDIDATES.yaml` in this gate. Existing in-progress mem0 edits add EmbeddingGemma to the mem0 candidate radar and are intentionally left in their owning track.

## Publication Gate

GitHub code, documentation, and run cards may be pushed when validation passes and the commit does not include unreviewed generated artifacts.

Do not publish any Hugging Face model, adapter, dataset, GGUF, merged weight, or benchmark claim unless all of the following are true:

- The base model and derivative license permits the planned artifact.
- The exact artifact scope is recorded in a run card or publication report.
- Dataset scope has been explicitly approved by the user when dataset rows are involved.
- Benchmark claims cite concrete local or cloud evidence and do not exceed the measured gate.
- Private data, secrets, local caches, and large generated artifacts remain untracked.

Current public-safe claim boundary:

- The repo can claim local/runtime/benchmark evidence where reports exist.
- The Qwen3 v4 strict-targeted adapter remains the recommended local strict-tool-call adapter by current evidence.
- mem0 integration can be described as an explicit read-only wrapper/tool path, not a default memory replacement.
- Jina, EmbeddingGemma, Qwen retrieval, and MLX BGE remain candidate or opt-in lanes until broader benchmarks and migration plans pass.

## Cloud and Offload Provenance

Cloud/offload evidence must be tagged by provider and treated as separate from local Mac proof.

Current operator state:

- Colab CLI is installed and usable enough to inspect sessions; no active session is currently running.
- Azure remains a scale-out lane, but compute work requires current login/quota/capacity confirmation before job submission.
- NVIDIA NGC is present as a potential artifact/runtime lane, but configuration and credentials must be proven before use.
- Kaggle remains a possible offload path, but no benchmark evidence in this repo currently depends on Kaggle execution.

## Open Blockers

- `mem0-embedding-reranker-promotion_20260612`,
  `frontier-support-evaluation_20260612`, and
  `cloud-dynamic-benchmark-orchestration_20260612` are archived as complete in
  the Conductor registry. Follow-on work is now candidate-specific rather than
  a blocker on this publication gate.
- Dataset publication is no longer blocked. The approved cleaned synthetic-only
  dataset was published to
  `https://huggingface.co/datasets/edithatogo/qwen3-hermes-strict-toolcall-synthetic-v4`
  at remote SHA `727e7e4ecd781aca2f7506d4a8fc6d910f521d6d`.
- Remaining publication caution: keep the Qwen3 v4 adapter positioned as an
  experimental local strict Hermes tool-call LoRA with pilot-only broader
  benchmark evidence. Do not promote broader BFCL/IFEval/coding claims without
  full benchmark evidence.

## Validation

Passed on 2026-06-12:

```bash
source scripts/env.sh && ./.venv/bin/python scripts/validate_readiness.py
source scripts/env.sh && ./.venv/bin/python scripts/check_model_candidates.py
```

Track health: 9.8/10.

The remaining risk is claim scope rather than publication mechanics: the
dataset is public, but broader model-capability claims still need full benchmark
evidence before they are advertised.
