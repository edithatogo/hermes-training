# Hermes Training Hub Product Definition

## Product

Hermes Training Hub is a bleeding-edge model research and engineering workspace for adapting, benchmarking, packaging, and publishing Hermes-agent models across local and cloud-assisted platforms.

The MacBook Pro M1 Max/MLX setup is the first local lane. Azure GPU, Hugging Face/Transformers, Ollama, LM Studio, GGUF, KTransformers, and model-family runtimes are platform lanes used when they are the right fit for a Hermes-agent model goal.

## Users

- The project owner running local models on a MacBook Pro M1 Max with 32GB unified memory and cloud-assisted experiments where useful.
- AI agents and coding assistants that need a structured, reproducible training/evaluation workflow.
- Future GitHub and Hugging Face consumers who need clear model cards, benchmark evidence, and runtime instructions.

## Goals

- Fine-tune practical local adapters where training is realistic on Apple Silicon.
- Use Azure and other non-Mac platforms to scale benchmarks, teacher/evaluator runs, and larger experiments when quota and cost controls pass.
- Use frontier models as baselines, teachers, evaluators, and runtime comparisons before attempting risky local fine-tunes.
- Keep all large caches, downloads, temp files, and benchmark artifacts on the external SSD.
- Promote adapters only after benchmark gates and documentation requirements are satisfied.
- Support MLX, Ollama, LM Studio, and other runtimes when they are technically justified.

## Non-Goals

- Publishing unbenchmarked smoke adapters as quality improvements.
- Treating every frontier model as a local fine-tune target.
- Treating Mac/MLX as the product boundary rather than a constrained implementation lane.
- Creating cloud compute before account, quota, region, and spend guardrails pass.
- Storing large model artifacts or benchmark outputs in Git.
- Merging chat SFT, retrieval training, and runtime packaging into one untracked workflow.

## Current Proof

`LiquidAI/LFM2.5-1.2B-Instruct` has completed a 10-iteration MLX LoRA smoke run and saved a local adapter. This proves the local pipeline but not model quality.
