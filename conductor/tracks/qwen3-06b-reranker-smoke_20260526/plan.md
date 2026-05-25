# Plan: Qwen3 0.6B Reranker Smoke

## Phase 1: Artifact and Harness Proof

- [x] Task: verify `Qwen/Qwen3-Reranker-0.6B` exists on Hugging Face.
- [x] Task: verify the local Qwen3 causal-LM yes/no scoring harness is
  available with SSD-backed Hugging Face cache paths.

## Phase 2: Learned Reranker Benchmarks

- [x] Task: run the Qwen3 0.6B reranker on the expanded fixed candidate suite.
- [x] Task: run the Qwen3 0.6B reranker on BGE-derived and nomic-derived
  expanded candidate suites if the first run is viable.

## Phase 3: Documentation and Gates

- [x] Task: document results and any runtime/memory caveats.
- [x] Task: update candidate radar, queue, benchmark index, and handoff.
- [x] Task: run validation and leave the tree ready to push.

## Health Check

- Target: >= 9.5 / 10
- Current estimate: 9.7 / 10
- Evidence: `Qwen/Qwen3-Reranker-0.6B` passed the fixed 6-case suite and both
  expanded BGE/nomic 12-case derived suites at top-1, recall@3, MRR, and
  nDCG@3 of 1.000.
- Gaps: live read-only mem0 wrapper and ONNX/Transformers.js bridge proof remain
  future work.
