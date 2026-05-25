# Parallel Roadmap

Updated: 2026-05-25

This roadmap defines the remaining work as parallel Conductor lanes. It is intentionally broader than the completed Qwen3 4B experiments: the goal is to reach publishable Hermes-agent evidence, not to keep iterating on one weak candidate.

## Execution Model

- Work proceeds by lane whenever dependencies permit.
- Every lane writes generated artifacts, logs, run cards, and benchmark outputs under `/Volumes/PortableSSD`.
- Git tracks plans, manifests, small reports, cards, and decisions only.
- Hugging Face publication remains blocked until the relevant strict benchmark, standardized benchmark, runtime, license, and documentation gates pass.
- Runtime-normalized output may support local Hermes integration but must not replace raw strict benchmark scoring.

## Lanes

| Lane | Track | Can Run In Parallel With | Hard Dependencies | Completion Gate |
|---|---|---|---|---|
| Model candidate evaluation | `conductor/tracks/model-candidate-evaluation_20260524/` | Runtime proof, Azure readiness, benchmark setup | Current model scan, license/source check | Candidate matrix with reject/watchlist/runtime-proof/benchmark/publish decisions |
| Runtime proof completion | `conductor/tracks/runtime-proof-completion_20260524/` | Model evaluation, benchmark setup | Existing local artifact or active endpoint | Qwen3 GGUF LM Studio proof plus Hermes 4/Qwen3.6 proof or documented no-download blockers |
| Azure execution readiness | `conductor/tracks/azure-execution-readiness_20260524/` | Local runtime/model work | Azure identity, quota, no-spend gates | Dry-run-ready Azure benchmark/teacher lane with fail-closed controls |
| Standard benchmark execution | `conductor/tracks/standard-benchmark-execution_20260524/` | Candidate/runtime setup until live runs | Benchmark candidate and artifact roots | IFEval/BFCL/coding/lm-eval evidence pack or explicit exclusions |
| Publication readiness | Part of standard benchmark execution | After benchmark evidence exists | Strict held-out pass, standard benchmarks, license | GitHub/Hugging Face go/no-go decision and model-card-ready evidence |

## Current High-Priority Work

1. Qwen3 v4 targeted is the current public/recommended strict Hermes tool-call adapter. It passes the local held-out strict gate at `1.000` with the recorded Qwen runtime prefill and has ready publication evidence.
2. Qwen3 v5 pilot-polish is a non-promotion result. It improved the BFCL-style pilot but regressed held-out strict pass to `0.875`, so it must not replace v4.
3. Candidate matrix is recorded at `reports/model-radar/candidate-matrix-20260524.md`; next action is to attach runtime proof evidence for frontier/runtime candidates, not to train them immediately.
4. Runtime packaging is complete as a lane. Remaining runtime work is live LM Studio GGUF smoke for Qwen3 and a future Ollama retest after the Qwen3 import/runtime instability changes.
5. Azure account preflight passed and is recorded at `reports/azure/execution-readiness-20260524.md`; live cloud execution remains blocked until specific useful GPU quota is confirmed.
6. Standardized benchmark manifest is recorded at `reports/benchmark/manifests/standard-benchmark-manifest-20260524.md`; official BFCL/IFEval/lm-eval expansion remains future work if broader public claims are needed.
7. Dataset publication remains separate from adapter publication and blocked pending dataset-scope approval.

## Current Model Scan Notes

The 2026-05-24 search did not find an official Qwen3.7 open-weight lane. Relevant newly surfaced or refreshed candidates include:

- `Qwen/Qwen3.6-27B`
- `Qwen/Qwen3.6-35B-A3B`
- `unsloth/Qwen3.6-27B-UD-MLX-4bit`
- `unsloth/Qwen3.6-27B-MTP-GGUF`
- `unsloth/Qwen3.6-35B-A3B-MTP-GGUF`
- `google/gemma-4-26B-A4B-it`
- `unsloth/gemma-4-26B-A4B-it-GGUF`
- `nvidia/Gemma-4-26B-A4B-NVFP4`
- `NousResearch/Hermes-4-14B`
- `NousResearch/Hermes-4.3-36B`
- `NousResearch/Hermes-4.3-36B-GGUF`
- `RWKV/RWKV7-Goose-World3-2.9B-HF`

These are candidates for runtime proof or watchlist triage, not automatic training targets.

## Stop Conditions

- Do not download large artifacts unless a specific track calls for it and SSD/cost gates pass.
- Do not run paid Azure jobs until quota and no-spend controls are recorded.
- Do not publish adapters or datasets until license and benchmark gates pass.
- Do not treat runtime-normalized output as strict benchmark success.
