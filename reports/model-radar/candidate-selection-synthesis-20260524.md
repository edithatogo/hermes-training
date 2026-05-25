# Candidate Selection Synthesis

Date: 2026-05-24

## Decision States

| State | Meaning | Promotion Requirement |
|---|---|---|
| Reject | Do not spend more time unless the upstream changes materially. | New model release, new runtime, or corrected blocker. |
| Watchlist | Interesting but not actionable yet. | Verified source, license, runtime path, and SSD storage plan. |
| Runtime-proof only | Worth loading or serving locally, but not a benchmark or publication candidate. | Successful smoke plus reproducible endpoint/runtime card. |
| Benchmark candidate | Runtime is reproducible and comparable benchmarks are meaningful. | Held-out strict tool-call, suite manifests, raw artifacts, normalized summary. |
| Internal adapter candidate | Worth training or adapting privately. | Training plan, dataset card, license check, runtime proof, benchmark target. |
| Publish candidate | Suitable for GitHub/Hugging Face publication after explicit approval. | Full evidence pack, model/dataset card, license review, and user approval. |

## Lane Winners

| Lane | Current Lead | Why | Current Blocker |
|---|---|---|---|
| Mac-local runtime | Qwen3 4B Q4_K_M through LM Studio | Best local strict held-out endpoint evidence so far at `0.500`. | Still below strict Hermes-agent publication gate. |
| Hermes baseline | Hermes 4 14B Q4_K_M through llama.cpp | Local SSD artifact is acquired, served, smoked, and benchmarked. | Strict held-out pass is `0.250`; use as baseline/teacher, not publish proof. |
| Frontier MoE | Qwen3.6 35B-A3B Q4_K_M | Efficient MoE runtime baseline is complete and reproducible through llama.cpp. | Strict held-out tool-call pass is `0.000`; runtime/teacher only. |
| Frontier multimodal/MoE | Gemma 4 26B-A4B Q3_K_M | Next one-by-one GGUF proof target after Qwen3.6. | Paused until Qwen3.6 completes or is skipped. |
| Retrieval baseline | BGE-M3 and current `nomic-embed-text:latest` | Practical local retrieval evidence exists; mem0 recency rerank path improves pass rate. | Retrieval wins are separate from chat/tool-call publication. |
| Research runtime | MiMo V2 Flash, RWKV7, BitNet, LFM2/LFM2.5 | Relevant bleeding-edge/nonstandard architecture lanes; LFM2 24B-A2B Q4_K_M is now runtime-proven. | Keep non-proven families on watchlist until runtime proof and license checks exist. |
| Qwen3.7 | Watchlist only | Current refresh found proprietary/API-preview reporting, not verified open weights. | No official open-weight Hugging Face artifact verified. |

## Publish / No-Publish Decisions

| Candidate | Decision | Reason |
|---|---|---|
| Qwen3 4B v4 targeted adapter | Publish as narrow experimental adapter | Held-out strict local tool-call score is `1.000` with `/no_think` plus assistant prefill; broader benchmark claims remain pilot-only. |
| Qwen3 4B v5 pilot-polish adapter | No publish / do not promote | BFCL-style pilot improved, but held-out strict pass regressed to `0.875`. |
| Hermes 4 14B Q4_K_M | No publish as a Hermes-agent result | Runtime proof exists, but strict tool-call behavior is not publication-ready. |
| Qwen3.6 35B-A3B Q4_K_M | Runtime-proof only | Artifact and smoke proof are complete, but held-out strict tool-call pass is `0.000`. |
| Gemma 4 26B-A4B Q3_K_M | Watchlist/runtime-proof candidate | Artifact acquisition is paused. |
| mem0 reranking improvements | Internal evidence candidate | Useful benchmark evidence exists, but separate memory-lane review is still dirty/uncommitted. |

## Evidence Links

- Candidate matrix: `reports/model-radar/candidate-matrix-20260524.md`
- Current release scan: `reports/model-radar/current-release-scan-20260524.md`
- Qwen3.7/Qwen3.6/Hermes 4 check: `reports/model-radar/qwen37-qwen36-hermes4-check-20260524.md`
- Standard benchmark manifest: `reports/benchmark/manifests/standard-benchmark-manifest-20260524.md`
- Runtime inventory: `reports/runtime/runtime-inventory-20260524.md`
- Qwen3.6 runtime proof: `reports/runtime/qwen36-35b-a3b-q4-llamacpp-proof-20260525.md`
- LFM2 24B runtime proof: `reports/runtime/lfm2-24b-a2b-q4-llamacpp-proof-20260525.md`

## Next Parallel Work

1. Use Qwen3 v4 for narrow local strict Hermes tool-call publication; run official benchmarks only before broader claims.
2. Resume Gemma 4 Q3_K_M acquisition only if another frontier runtime baseline is worth the SSD/time cost after Qwen3.6, Hermes 4, and LFM2 evidence.
3. Keep Azure in dry-run/readiness mode until useful GPU quota exists.
4. Treat retrieval/mem0 evidence as a separate publication lane from chat SFT.
5. Keep Qwen3.7 off local training/publication tracks until official open weights exist.
