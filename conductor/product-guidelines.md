# Product Guidelines

## Operating Principles

- Be evidence-first: benchmark results must distinguish pipeline proof from model-quality claims.
- Prefer reproducibility over convenience: every promoted run needs a config, dataset audit, run note, and evaluation record.
- Keep storage explicit: all model, dataset, temp, and benchmark caches should resolve to the external SSD by default.
- Keep runtime choice pragmatic: MLX is the Apple Silicon default, Ollama is the Hermes launcher path, LM Studio/GGUF is a compatibility fallback.
- Keep claims scoped: adapter cards should say exactly what was trained, on what data, and how it performed.

## Documentation Style

- Use concise engineering prose.
- Put status, blockers, commands, and file paths near the top.
- Prefer tables for model comparisons, benchmark matrices, and promotion gates.
- Avoid marketing claims unless backed by benchmark outputs.

## Release Standard

A release is not ready unless:

- the base model and adapter paths are documented
- dataset sources and token counts are documented
- benchmark results are recorded
- runtime instructions are tested
- license and redistribution status are stated
