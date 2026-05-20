# Tech Stack

## Languages and Tools

- Python 3.14 virtual environment for local scripts.
- Bash for launchers, runtime setup, and packaging scripts.
- YAML for model/training configuration.
- JSONL for datasets and benchmark prompts.
- Markdown for specs, plans, run cards, and model documentation.

## ML Stack

- MLX and MLX-LM for Apple Silicon LoRA training and serving.
- Hugging Face Hub for models, datasets, adapter publication, and model cards.
- Transformers/Datasets/Safetensors for compatibility and artifact handling.
- Ollama for local Hermes runtime integration.
- LM Studio/GGUF for broad local serving fallback.
- Azure CLI and Azure ML CLI v2 for cloud-assisted benchmark, teacher, and larger experiment lanes.
- CUDA-oriented frameworks such as Unsloth/TRL/PEFT are cloud-lane tools unless a Mac-native backend is proven.
- Specialist runtimes such as KTransformers, RWKV-LM, BitNet, and Mamba-family runtimes require runtime proof before promotion.

## Benchmark Stack

- Hermes-local benchmark harness in each model track.
- Standard benchmarks documented in `STANDARD_BENCHMARKS.md`.
- Future integration targets: `lm-evaluation-harness`, BFCL, IFEval, coding benchmarks, RULER, MTEB for embedding tracks.

## Storage Stack

- Project code: `/Volumes/PortableSSD/GitHub/hermes-training`, symlinked from `/Users/doughnut/GitHub/hermes-training`.
- Shared environment helper: `scripts/env.sh`.
- Model cache: `/Volumes/PortableSSD/huggingface`.
- Benchmark/output roots: `/Volumes/PortableSSD/hermes-evals`, `/Volumes/PortableSSD/lm-eval`, `/Volumes/PortableSSD/opencompass`, `/Volumes/PortableSSD/helm`.
- Cloud job manifests, downloaded reports, and synced artifacts must also land under SSD-backed roots.

## Platform Lanes

| Lane | Purpose | Guardrail |
|---|---|---|
| Mac/MLX | Practical local fine-tunes and fast Hermes runtime proof | 32GB memory budget, SSD caches, small/efficient models first |
| Mac/Ollama/LM Studio | Daily Hermes serving and runtime packaging | OpenAI-compatible endpoint smoke before promotion |
| Azure/CUDA | Benchmarks, teacher/evaluator runs, and larger experiments | Preflight, quota check, Spot/low-priority, max one GPU job |
| Retrieval | Hermes memory/RAG with embedding/reranker models | Contrastive/retrieval evals, not chat SFT gates |
| Research runtime | Recursive, subquadratic, RWKV, BitNet, Mamba-family exploration | Verify weights, license, runtime, and endpoint before track promotion |
