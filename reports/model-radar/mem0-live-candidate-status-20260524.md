# mem0 Live Candidate Status

Date: 2026-05-24

## Completed

| Lane | Result |
|---|---|
| Expanded reranking suite | `benchmarks/mem0_reranking/fixed_candidate_suite.json` now has 6 cases. |
| No-download reranker comparison | `score_plus_created_at_rank` passed 6/6; vector baseline failed recency; lexical failed one recency case. |
| Expanded extraction suite | `benchmarks/mem0_extraction/smoke_suite.json` now has 7 cases and stricter all-required checks. |
| LFM2 extractor prompt | `sam860/LFM2:2.6b` passed the expanded extraction suite at `1.000` using `mem0/extraction/system_prompt.md`. |
| Hermes3 extractor comparison | `hermes3:8b` improved to `0.571` but still fails JSON/transient gates. |
| OpenAI-compatible embedding endpoint | Ollama `/v1/embeddings` path is proven for `nomic-embed-text:latest`. |
| Optional embedding deps | `torch 2.12.0` and `sentence-transformers 5.5.1` are installed in the repo venv. |
| ColBERT service boundary | `mem0/retrieval/COLBERT_SERVICE_PLAN.md` and `scripts/run_retriever_service_benchmark.py` define the first retriever gate. |

## Blocked

| Candidate | Blocker | Evidence |
|---|---|---|
| `BAAI/bge-m3` | Model checkpoint acquisition/load did not reach first benchmark case in the available window. | `reports/model-radar/mem0-embedding-deps-install-20260524.md` |
| `jinaai/jina-embeddings-v4` | Needs first model acquisition/load proof now that deps are installed. | `requirements-mem0-embeddings.txt` |
| `Qwen/Qwen3-Embedding-4B` | Needs first model acquisition/load proof plus likely memory-footprint proof. | `reports/model-radar/mem0-candidate-queue.md` |
| `Qwen/Qwen3-Reranker-4B` | Reached Hugging Face model fetch but did not complete in the available window. | `scripts/run_fixed_reranking_benchmark.py` |
| `LiquidAI/LFM2-ColBERT-350M` | Needs separate late-interaction index/service. | `mem0/RUNTIME_TARGETS.md` |

## Decision

- Keep `nomic-embed-text:latest` and `mem0_nomic_768` as the embedding/vector rollback path.
- Keep `sam860/LFM2:2.6b` as the mem0 extraction rollback path; it now has a clean expanded-suite pass.
- Keep `score_plus_created_at_rank` as the leading no-download reranker candidate, but do not wire it as the default live behavior until a learned reranker comparison runs or the suite grows further.
- Treat Hugging Face candidate model acquisition as a separate prefetch task before benchmark timing.
