# mem0 Extraction

This folder holds the prompt and gate evidence for local memory extraction.

## Current Default

| Field | Value |
|---|---|
| Extractor | `sam860/LFM2:2.6b` |
| Runtime | Ollama OpenAI-compatible `/v1/chat/completions` |
| Prompt | `mem0/extraction/system_prompt.md` |
| Current gate | `extraction-lfm2-2-6b-clean-root-20260526` |
| Expanded-suite pass | `1.000` |
| Clean SSD root | `/Volumes/PortableSSD/Ollama/mem0-clean-models` |

## Benchmark

```bash
source scripts/env.sh
./.venv/bin/python scripts/run_ollama_memory_extraction_benchmark.py \
  --model 'sam860/LFM2:2.6b' \
  --system-prompt-file mem0/extraction/system_prompt.md \
  --suite benchmarks/mem0_extraction/smoke_suite.json \
  --run-id extraction-lfm2-2-6b-$(date +%Y%m%d-%H%M%S)
```

The clean-root recovery run on 2026-05-26 keeps both
`nomic-embed-text:latest` and `sam860/LFM2:2.6b` in
`/Volumes/PortableSSD/Ollama/mem0-clean-models`, avoiding the older model roots
that had caused `ollama list` and model creation hangs.

## Promotion Rule

Keep `sam860/LFM2:2.6b` as the rollback extractor until another model passes
the expanded extraction suite with:

- pass rate `1.000`
- JSON validity `1.000`
- forbidden hit rate `0.000`
- empty-case pass rate `1.000`
