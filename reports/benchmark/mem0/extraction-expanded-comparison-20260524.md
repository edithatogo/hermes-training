# mem0 Extraction Expanded Comparison

Date: 2026-05-24

Suite: `benchmarks/mem0_extraction/smoke_suite.json`

## Result

| Model | Run ID | Pass | JSON valid | Expected extraction | Forbidden hit | Empty-case pass | p50 latency |
|---|---|---:|---:|---:|---:|---:|---:|
| `sam860/LFM2:2.6b` | `extraction-lfm2-2-6b-prompt-file-20260524` | 1.000 | 1.000 | 1.000 | 0.000 | 1.000 | 0.866s |
| `sam860/LFM2:2.6b` | `extraction-lfm2-2-6b-expanded-examples-20260524` | 1.000 | 1.000 | 1.000 | 0.000 | 1.000 | 1.847s |
| `hermes3:8b` | `extraction-hermes3-8b-expanded-examples-20260524` | 0.571 | 0.714 | 0.857 | 0.143 | 0.857 | 1.476s |

## Decision

Keep `sam860/LFM2:2.6b` as the mem0 rollback extractor. The versioned prompt at
`mem0/extraction/system_prompt.md` gives it a clean expanded-suite pass.
`hermes3:8b` remains useful as a comparison model, but it still misses JSON
validity and transient-noise gates.
