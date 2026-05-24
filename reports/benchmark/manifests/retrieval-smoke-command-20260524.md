# Retrieval Smoke Command Manifest

Date: 2026-05-24

## Purpose

Run retrieval-only candidates through MTEB-style smoke without confusing retrieval quality with chat-model quality.

## Command

```bash
source scripts/env.sh
mteb run \
  -m <model_id_or_path> \
  -t "<retrieval_task_or_benchmark>" \
  --output-folder "$HERMES_EVAL_ROOT/mteb/<run-id>"
```

## Artifact Root

```text
$HERMES_EVAL_ROOT/mteb/<run-id>
```

## Boundary

Retriever scores can support Hermes memory/RAG claims only. They do not support chat SFT or adapter publication claims.
