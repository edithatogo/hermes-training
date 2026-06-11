# Gemma 4 E4B Strict Profile No-Extra Pilot - 2026-06-12

## Summary

The local and endpoint pilot runners now support:

```text
--require-no-extra-tool-text
```

This optional flag makes `tool_call_exact` cases fail when a model emits extra
text around otherwise correct `<tool_call>` payloads. It is intended for
Hermes-style strict-format checks and avoids over-reading permissive parsed-tool
pilot results.

## Run

Model:

`/Volumes/PortableSSD/huggingface/hub/models--mlx-community--gemma-4-E4B-it-qat-4bit/snapshots/0f35c6f6d386f7f74e628bd7c6526ce531212300`

Command:

```bash
./.venv/bin/python scripts/run_local_pilot_benchmark.py \
  --suite benchmarks/endpoint_pilots/bfcl_pilot.json \
  --model /Volumes/PortableSSD/huggingface/hub/models--mlx-community--gemma-4-E4B-it-qat-4bit/snapshots/0f35c6f6d386f7f74e628bd7c6526ce531212300 \
  --run-id gemma4-e4b-mlx-strict-profile-no-extra-pilot-20260612 \
  --max-tokens 160 \
  --user-prefix 'Final answer only. Do not include thought. For valid tools emit only <tool_call>{"name":"TOOL","arguments":{}}</tool_call>. For unavailable tools, refuse briefly without repeating the unavailable tool name.' \
  --require-no-extra-tool-text
```

SSD output:

`/Volumes/PortableSSD/hermes-evals/standard-benchmarks/local-pilots/gemma4-e4b-mlx-strict-profile-no-extra-pilot-20260612`

## Result

| Scoring mode | Pass rate | Note |
|---|---:|---|
| Base raw BFCL-style pilot | 0.000 | No parsed strict Hermes calls. |
| Profiled, permissive parsed-tool pilot | 0.333 | Simple lookup parsed, but with thought text. |
| Profiled, no-extra-text pilot | 0.000 | Simple lookup fails because extra thought text remains. |
| Gemma-native score normalizer | 0.333 | Runtime-adapter analysis only, not strict evidence. |

Failure details for the no-extra run:

- `bfcl-simple-customer-lookup`: tool call matched, but extra Gemma thought text
  preceded it.
- `bfcl-parallel-ticket-routing`: no complete expected tool-call sequence was
  emitted.
- `bfcl-invalid-tool`: refusal marker was present, but the forbidden unavailable
  tool name was repeated in the thought text.

## Decision

- Status: `scorer-hardened; gemma-profile-not-promoted`
- Use `--require-no-extra-tool-text` for Hermes strict local pilot claims.
- Keep the permissive parsed-tool score and Gemma-native normalizer as
  diagnostic/runtime-adapter evidence only.
