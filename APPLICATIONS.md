# Applications and Use Cases

The project should produce more than one chatbot. Different model families should be used where their architecture is strongest.

## Primary Applications

| Application | Best initial model path | Why |
|---|---|---|
| Local Hermes assistant | LFM2.5 1.2B, Qwen3 4B | Fits MacBook Pro M1 Max, can run privately, fast iteration |
| Tool-calling assistant | Qwen3 4B, Hermes 4 baseline, LFM2.5 helper | Needs reliable JSON/function-call formatting |
| Local coding helper | Qwen3 4B, Hermes 4 14B runtime, Qwen3.6 teacher | Better coding/reasoning baseline than tiny models |
| Background summarizer | LFM2.5 1.2B | Low memory and latency |
| Retrieval/memory layer | LFM2-ColBERT, BGE-M3, Jina embeddings, Qwen embedding/reranker candidates | Better suited to retrieval than chat SFT; train with contrastive data and retrieval metrics |
| Long-context research assistant | Qwen3-Next, recursive/linear-attention models | Use only after RULER and runtime memory proof |
| Teacher/evaluator model | Hermes 4 14B, Qwen3.6 35B-A3B, Gemma4 A4B | Larger models can label, critique, and score local adapters |
| Runtime benchmark target | Ollama, LM Studio, MLX server | Ensures Hermes can use whichever runtime is practical |
| Cloud benchmark accelerator | Azure GPU lane | Runs broader standardized benchmarks and teacher checks without forcing all work onto the Mac |

## Secondary Applications

- Dataset curation assistant for Hermes-style conversations.
- Tool-call validator and repair model.
- Local agent router that chooses between a small fast model and a larger teacher.
- Private document summarization and RAG over local files.
- Offline coding support for small repositories.
- Evaluation judge for local benchmark outputs, subject to human spot checks.
- Model comparison harness for Apple Silicon runtime experiments.

## Architecture Patterns

### Small-Fast Plus Teacher

Use LFM2.5 or Qwen3 4B for routine local work. Use Hermes 4 or Qwen3.6 as an occasional teacher/evaluator for:

- synthetic data review
- tool-call correction
- benchmark judging
- difficult coding/reasoning prompts

### Retrieval-Augmented Hermes

Use a retrieval model such as LFM2-ColBERT to build a local memory layer. Keep chat SFT separate from retrieval tuning:

- chat adapters: supervised fine-tuning and tool-call benchmarks
- retrievers: contrastive training, Hermes memory/RAG scenarios, and MTEB/retrieval benchmarks
- local serving: separate retriever API or tool call, not a chat adapter shim

See [RETRIEVAL_MEMORY.md](./RETRIEVAL_MEMORY.md) for the retrieval lane contract details.

### Runtime Flexibility

Do not assume one runtime wins. Track all viable paths:

- MLX: best native Apple Silicon path
- Ollama: easiest Hermes launcher path
- LM Studio: useful GGUF/manual runtime fallback
- KTransformers/experimental engines: evaluate only for large MoE or special architectures

### Platform-Lane Selection

Choose the lane from the model goal:

- use Mac/MLX for achievable local training and rapid iteration
- use Ollama or LM Studio when the task is daily Hermes serving
- use Azure when the task is benchmark breadth, teacher/evaluator quality, or a larger experiment
- use retrieval tooling when the task is memory/RAG, not chat generation
- use specialist runtimes only after the model has verified weights, license, and endpoint proof
- publish retriever cards with index hashes, corpus provenance, and retrieval metrics; keep raw corpora and embeddings out of source control

## Improvement Opportunities

1. Expand the Hermes-local benchmark before quality claims.
2. Add BFCL-style tool-call validation and JSON schema scoring.
3. Add a run-card generator so every training/eval run leaves a structured record.
4. Add a model-prefetch command that uses `scripts/env.sh` and verifies SSD cache location.
5. Add a local judge workflow using Hermes 4 or Qwen3.6, with human review for sampled outputs.
6. Split chat SFT, retrieval, and runtime packaging into separate promotion gates.
7. Add long-context benchmarks before promoting recursive/subquadratic model claims.
8. Add Azure benchmark and teacher/evaluator run cards once the student subscription preflight passes.
9. Keep speculative bleeding-edge releases in the watchlist until verified by model card, weights, license, and runtime smoke.

## Publication Guidance

For GitHub:

- publish code, configs, benchmark definitions, run cards, and small summary reports
- keep heavy artifacts out of source control

For Hugging Face:

- publish datasets with dataset cards and split/token audits
- publish adapter repos only after benchmark gates pass
- include runtime instructions for MLX/Ollama/LM Studio
- include standardized benchmark tables and limitations
