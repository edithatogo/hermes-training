# Live mem0 Multi-Result Comparison Readiness

Date: 2026-05-26

## Purpose

Check whether the current live mem0 store can support a meaningful comparison
between vector ordering, `score_plus_created_at_rank_close_margin`, and the
warm `Qwen/Qwen3-Reranker-0.6B` wrapper.

## Probe

Ollama was started against the clean SSD-backed root:

```bash
OLLAMA_MODELS=/Volumes/PortableSSD/Ollama/mem0-clean-models \
OLLAMA_HOST=127.0.0.1:11434 \
/opt/homebrew/bin/ollama serve
```

The following live `mem0 cmd search` probes were run:

| Query | Returned results |
|---|---:|
| `mem0` | 1 |
| `Ollama` | 1 |
| `Qwen` | 1 |
| `PortableSSD` | 1 |
| `What models are configured?` | 1 |
| `What is the active mem0 Qdrant collection?` | 1 |

Each probe returned the same setup note about the active local mem0/Ollama
configuration.

## Decision

Do not claim a live multi-result reranker comparison yet. The current live mem0
store is too small; all tested queries returned a singleton result, so reranking
cannot change rank order or reveal distractor behavior.

The next valid comparison needs either:

- a deliberate, non-sensitive local fixture memory set added to a test agent or
  isolated test collection, or
- a replay harness that uses captured multi-result candidate suites without
  writing to the live default memory.

The existing offline expanded suites remain the valid evidence for reranker
quality until a live multi-result store exists.
