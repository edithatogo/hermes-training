# Spec: Platform Abstraction and Lane Architecture

## Goal

Reframe Hermes Training Hub around bleeding-edge Hermes-agent models rather than a single local hardware environment.

## Requirements

- The product mission must identify Mac/MLX as one constrained local lane, not the project boundary.
- Every model and execution path must map to a platform lane before training, benchmarking, packaging, or publication.
- Local work must remain constrained to what is achievable on the M1 Max with 32GB RAM.
- Cloud and specialist runtimes must be used where they speed up benchmarks, teacher runs, or research exploration.
- Health target: `>= 9.5 / 10`.

## Lane Definitions

| Lane | Use |
|---|---|
| `mac-mlx` | local LoRA training and MLX serving for practical models |
| `mac-ollama` | local Hermes runtime through Ollama |
| `mac-lmstudio` | GGUF desktop serving and runtime fallback |
| `azure-cuda` | benchmarks, teacher/evaluator jobs, and larger experiments |
| `retrieval` | embedding, reranking, ColBERT, and Hermes memory models |
| `specialist-runtime` | RWKV, BitNet, Mamba/subquadratic, KTransformers, recursive wrappers |

## Acceptance Criteria

- Hub mission, requirements, design, contracts, and tech stack describe platform lanes.
- `MODEL_CANDIDATES.yaml` supports role, environment, and feasibility classification.
- Readiness validation passes.
- Health checkpoint is completed at `>= 9.5`.
