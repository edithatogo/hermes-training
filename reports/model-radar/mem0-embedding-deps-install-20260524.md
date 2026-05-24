# mem0 Embedding Dependency Install Attempt

Date: 2026-05-24

## Purpose

Prepare the repo venv to run Hugging Face embedding candidates such as
`BAAI/bge-m3` through `scripts/run_sentence_transformers_embedding_benchmark.py`.

## Command

```bash
source scripts/env.sh
./.venv/bin/python -m pip install -r requirements-mem0-embeddings.txt
```

## Result

First attempt stopped manually after the install spent several minutes
downloading the PyTorch macOS arm64 wheel:

```text
torch-2.12.0-cp314-cp314-macosx_14_0_arm64.whl
14.9/88.0 MB
ERROR: Operation cancelled by user
```

After splitting `FlagEmbedding` into `requirements-mem0-rerankers.txt`, a
second leaner attempt ran:

```bash
source scripts/env.sh
./.venv/bin/python -m pip install --progress-bar off -r requirements-mem0-embeddings.txt
```

It again stalled silently on the same `torch-2.12.0` wheel for more than six
minutes and was stopped. Post-check:

```text
sentence_transformers NO ModuleNotFoundError
torch NO ModuleNotFoundError
FlagEmbedding NO ModuleNotFoundError
```

The benchmark harness itself compiled and dry-ran, but live BGE-M3, Jina, Qwen
embedding, and CrossEncoder reranker runs were blocked until `torch` and the
relevant optional package finished installing.

## Successful Retry

A longer focused retry completed:

```bash
source scripts/env.sh
./.venv/bin/python -m pip install torch
./.venv/bin/python -m pip install sentence-transformers
```

Installed:

```text
torch OK 2.12.0
sentence_transformers OK 5.5.1
```

## Model Acquisition Blockers

After dependencies installed:

- `BAAI/bge-m3` reached Hugging Face checkpoint download/load but did not reach
  the first benchmark case after several minutes, so the run was stopped.
- `Qwen/Qwen3-Reranker-4B` reached model fetch for the first fixed reranking
  case, stayed at `Fetching 2 files: 0/2` for several minutes, and was stopped.

The remaining blocker is model acquisition/load time for large Hugging Face
artifacts, not the local Python dependency stack.

## Follow-Up

- Keep `requirements-mem0-embeddings.txt` limited to `sentence-transformers`
  and `torch`.
- Keep `FlagEmbedding` in `requirements-mem0-rerankers.txt` because it pulls
  extra retrieval-evaluation dependencies and source builds.
- Retry during a better network window, or install wheels through a faster
  package mirror/cache before running BGE-M3.
