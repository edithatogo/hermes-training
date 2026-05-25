# BGE-M3 Embedding Acquisition Check

Date: 2026-05-25

## Candidate

- Model: `BAAI/bge-m3`
- Role: mem0 dense embedding candidate
- Intended collection: `mem0_bge_m3_1024`
- Intended runtime: `sentence-transformers`, then optional server/runtime export if it wins
- Source: https://huggingface.co/BAAI/bge-m3

## Why It Remains In The Queue

The model card identifies BGE-M3 as a multilingual embedding model with dense,
sparse, and ColBERT-style modes. The card lists the dense embedding dimension
as `1024`, sequence length as `8192`, and license as MIT.

This keeps it relevant as the first practical replacement candidate for the
current `nomic-embed-text:latest` mem0 baseline, but it must use a separate
Qdrant collection because `mem0_nomic_768` is dimensioned for 768-dimensional
nomic vectors.

## Local Attempt

Command attempted on MPS:

```bash
HF_HOME=/Volumes/PortableSSD/huggingface \
TRANSFORMERS_CACHE=/Volumes/PortableSSD/huggingface/transformers \
/Volumes/PortableSSD/hermes-training-envs/benchmarks-py312/bin/python \
  scripts/run_sentence_transformers_embedding_benchmark.py \
  --model BAAI/bge-m3 \
  --device mps \
  --suite benchmarks/embeddings/memory_retrieval_suite.json \
  --run-id embedding-bge-m3-mps-smoke-20260525
```

Result: no case progress after more than two minutes; process was killed.

Command attempted on CPU:

```bash
HF_HOME=/Volumes/PortableSSD/huggingface \
TRANSFORMERS_CACHE=/Volumes/PortableSSD/huggingface/transformers \
/Volumes/PortableSSD/hermes-training-envs/benchmarks-py312/bin/python \
  scripts/run_sentence_transformers_embedding_benchmark.py \
  --model BAAI/bge-m3 \
  --device cpu \
  --suite benchmarks/embeddings/memory_retrieval_suite.json \
  --run-id embedding-bge-m3-cpu-smoke-20260525
```

Result: no case progress after roughly two minutes; process was killed.

Follow-up on 2026-05-26:

- `~/.mem0/mem0_wrapper.py` now honors `MEM0_CONFIG_PATH`, so BGE-M3 can be
  tested without overwriting the stable `mem0_nomic_768` setup.
- `~/.mem0/config.bge-m3.json` was created for side-by-side testing with
  collection `mem0_bge_m3_1024`, embedder `BAAI/bge-m3`, embedding dimensions
  `1024`, and the existing extractor `sam860/LFM2:2.6b`.
- The first full `hf download BAAI/bge-m3` attempt was stopped because it was
  also downloading the ONNX weight shard. The resumed acquisition uses only
  PyTorch / sentence-transformers files:

```bash
HF_HOME=/Volumes/PortableSSD/huggingface \
HF_HUB_CACHE=/Volumes/PortableSSD/huggingface/hub \
HF_HUB_DISABLE_XET=1 \
/Volumes/PortableSSD/hermes-training-envs/benchmarks-py312/bin/hf download \
  BAAI/bge-m3 \
  --include '*.json' \
  --include '*.pt' \
  --include '*.bin' \
  --include 'sentencepiece.bpe.model' \
  --include '1_Pooling/config.json' \
  --exclude 'onnx/*' \
  --exclude 'imgs/*' \
  --max-workers 2
```

Local cache inspection showed that the model weights are not acquired:

```text
/Volumes/PortableSSD/huggingface/hub/models--BAAI--bge-m3
```

The directory was only `36K` and contained a zero-byte incomplete blob:

```text
blobs/b5e0ce3470abf5ef3831aa1bd5553b486803e83251590ab7ff35a117cf6aad38.incomplete
```

## Decision

No benchmark score is recorded for BGE-M3 yet. The failure mode is incomplete
model acquisition, not retrieval quality.

Next action:

1. Acquire the full BGE-M3 weights into the SSD Hugging Face cache.
2. Re-run the CPU smoke first to verify functionality.
3. Re-run MPS only after CPU completes, because the first MPS attempt was not
   informative while the weights were incomplete.
4. If BGE-M3 passes, create the `mem0_bge_m3_1024` collection and run the live
   mem0 add/search and recency suites against that collection.
