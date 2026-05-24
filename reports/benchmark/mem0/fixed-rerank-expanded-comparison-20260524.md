# mem0 Fixed Reranking Expanded Comparison

Date: 2026-05-24

Suite: `benchmarks/mem0_reranking/fixed_candidate_suite.json`

## Result

| Strategy | Run ID | Top-1 | Recall@3 | MRR | nDCG@3 | Recency conflict | Distractor resistance |
|---|---|---:|---:|---:|---:|---:|---:|
| `vector` | `fixed-rerank-vector-expanded-20260524` | 0.667 | 1.000 | 0.833 | 0.877 | 0.000 | 1.000 |
| `score_plus_created_at_rank` | `fixed-rerank-created-at-rank-expanded-20260524` | 1.000 | 1.000 | 1.000 | 1.000 | 1.000 | 1.000 |
| `lexical_overlap` | `fixed-rerank-lexical-overlap-expanded-20260524` | 0.833 | 1.000 | 0.917 | 0.938 | 0.500 | 1.000 |

## Decision

Keep `score_plus_created_at_rank` as the strongest no-download reranker
candidate. It fixes the current recency failures without breaking the expanded
distractor cases. Do not promote it into default live behavior until the suite
is larger and the learned reranker comparison has run.
