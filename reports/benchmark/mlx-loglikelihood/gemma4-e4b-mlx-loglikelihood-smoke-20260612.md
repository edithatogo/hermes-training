# Gemma 4 E4B MLX Direct Loglikelihood Smoke - 2026-06-12

## Summary

`mlx-community/gemma-4-E4B-it-qat-4bit` was acquired to the SSD-backed
Hugging Face cache and load-proven through the direct MLX loglikelihood harness.

This is runtime evidence only. The one-case smoke returned a weak score on the
simple continuation probe, and the follow-on BFCL-style local pilot scored
`0.000`.

## Artifact

- Repo: `mlx-community/gemma-4-E4B-it-qat-4bit`
- Snapshot:
  `/Volumes/PortableSSD/huggingface/hub/models--mlx-community--gemma-4-E4B-it-qat-4bit/snapshots/0f35c6f6d386f7f74e628bd7c6526ce531212300`
- Cache footprint: `6.4G`
- Storage: external SSD cache under `/Volumes/PortableSSD/huggingface/hub`

## Loglikelihood Smoke

Command:

```bash
./.venv/bin/python scripts/run_mlx_loglikelihood_smoke.py \
  --model /Volumes/PortableSSD/huggingface/hub/models--mlx-community--gemma-4-E4B-it-qat-4bit/snapshots/0f35c6f6d386f7f74e628bd7c6526ce531212300 \
  --suite benchmarks/lm_loglikelihood/smoke.jsonl \
  --run-id gemma4-e4b-mlx-loglikelihood-smoke-20260612 \
  --max-cases 1 \
  --max-length 1024
```

Result:

| Metric | Value |
|---|---:|
| Cases | 1 |
| Mean avg logprob | -13.000000 |
| Greedy match rate | 0.000 |
| Load latency seconds | 14.149 |
| Score latency seconds | 0.970 |

SSD output:

`/Volumes/PortableSSD/hermes-evals/standard-benchmarks/mlx-loglikelihood/gemma4-e4b-mlx-loglikelihood-smoke-20260612`

## BFCL-Style Local Pilot

Command:

```bash
./.venv/bin/python scripts/run_local_pilot_benchmark.py \
  --suite benchmarks/endpoint_pilots/bfcl_pilot.json \
  --model /Volumes/PortableSSD/huggingface/hub/models--mlx-community--gemma-4-E4B-it-qat-4bit/snapshots/0f35c6f6d386f7f74e628bd7c6526ce531212300 \
  --run-id gemma4-e4b-mlx-local-bfcl-pilot-20260612 \
  --max-tokens 96
```

Result:

| Category | Cases | Pass rate |
|---|---:|---:|
| `tool_call_exact` | 2 | 0.000 |
| `contains_excludes` | 1 | 0.000 |

Observed failure mode:

- The model emitted Gemma-style `<|channel>thought` reasoning and partial
  `<tool_call>` fragments rather than strict Hermes JSON tool calls.
- The invalid-tool case reasoned that the requested function was absent, but
  still included the forbidden `delete_customer_record` string, so the exclude
  gate failed.

SSD output:

`/Volumes/PortableSSD/hermes-evals/standard-benchmarks/local-pilots/gemma4-e4b-mlx-local-bfcl-pilot-20260612`

## Score-Only Gemma Native Normalizer

A follow-up analysis run used:

```text
--score-normalizer gemma-native-tool-call
```

This preserved raw responses and converted only Gemma native
`{"function": ...}` fragments into Hermes `<tool_call>` JSON for scoring.

Result: `1/3` cases passed (`0.333`). Only the simple customer lookup case was
rescued. The parallel call remained incomplete, and the invalid-tool case still
failed because the raw response contained `delete_customer_record`.

Report:

`reports/benchmark/local-pilots/gemma4-e4b-native-normalized-pilot-20260612.md`

## Decision

- Status: `completed-runtime-proof; tool-call-blocked`
- Do not promote to Hermes default, training, or publication.
- Next gate: a Gemma-specific prompt/profile repair may be useful, but only if
  the target role is helper/extraction or Gemma comparison. Do not scale Gemma
  local training until strict-format behavior improves.
