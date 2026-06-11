# Specialist Frontier Current Release Scan - 2026-06-12

## Summary

This scan focuses on newly published agentic teacher models and specialist
runtime candidates that are useful for Hermes comparisons, distillation, or
future runtime experiments.

## Verified Candidates

| Family | Verified release | Why it matters |
|---|---|---|
| Cohere | `CohereLabs/command-a-plus-05-2026-w4a4` | Large agentic multimodal teacher with 25B active / 218B total parameters and a W4A4 runtime path. |
| StepFun | `stepfun-ai/Step-3.7-Flash` | Large sparse MoE vision-language teacher with agentic workflow emphasis and long context. |
| Nex-AGI | `nex-agi/Nex-N2-mini` | Smaller agentic model with community MLX conversions already published, making it a plausible Mac/Colab runtime candidate. |

## Watchlist / Special Cases

- `nvidia/Nemotron-3.5-Content-Safety` is useful as a safety moderator, not as
  a Hermes text-generation candidate.
- `nvidia/nemotron-3.5-asr-streaming-0.6b` is a specialist ASR model and
  belongs in the multimodal/speech lane, not the Hermes tool-call lane.

## Decision

- Add the verified Command A+, Step 3.7 Flash, and Nex-N2-mini entries to the
  machine-readable radar.
- Keep Nemotron safety and ASR variants as adjacent specialist watchlist
  references.
- Do not promote any of these to local fine-tune defaults without runtime
  proof.
