# Gemma 4 E4B Native-Normalized Local Pilot - 2026-06-12

## Summary

The local pilot runner now supports a score-only Gemma native tool-call
normalizer:

```text
--score-normalizer gemma-native-tool-call
```

This converts Gemma-style native fragments such as:

```json
{"function":"lookup_customer","customer_id":"CUST-1007"}
```

into strict Hermes scoring form:

```text
<tool_call>{"name":"lookup_customer","arguments":{"customer_id":"CUST-1007"}}</tool_call>
```

Raw model responses are preserved in the output files. This is runtime-adapter
evidence only; it does not change strict raw benchmark promotion rules.

## Run

Model:

`/Volumes/PortableSSD/huggingface/hub/models--mlx-community--gemma-4-E4B-it-qat-4bit/snapshots/0f35c6f6d386f7f74e628bd7c6526ce531212300`

Command:

```bash
./.venv/bin/python scripts/run_local_pilot_benchmark.py \
  --suite benchmarks/endpoint_pilots/bfcl_pilot.json \
  --model /Volumes/PortableSSD/huggingface/hub/models--mlx-community--gemma-4-E4B-it-qat-4bit/snapshots/0f35c6f6d386f7f74e628bd7c6526ce531212300 \
  --run-id gemma4-e4b-mlx-gemma-native-normalized-pilot-20260612 \
  --max-tokens 96 \
  --score-normalizer gemma-native-tool-call
```

SSD output:

`/Volumes/PortableSSD/hermes-evals/standard-benchmarks/local-pilots/gemma4-e4b-mlx-gemma-native-normalized-pilot-20260612`

## Result

| Category | Cases | Pass rate |
|---|---:|---:|
| `tool_call_exact` | 2 | 0.500 |
| `contains_excludes` | 1 | 0.000 |

Overall pass rate: `0.333`.

The normalizer rescued only `bfcl-simple-customer-lookup`. It did not rescue
the parallel tool-call case because no complete native call was emitted in the
bounded response. It did not rescue the invalid-tool case because the raw text
still contained the forbidden `delete_customer_record` marker.

## Decision

- Status: `runtime-adapter-analysis; not-promoted`
- Gemma 4 E4B has partial semantic tool intent, but not enough strict or
  adapter-normalized reliability for Hermes use.
- A future Gemma prompt/profile repair track should target complete native tool
  emission and forbidden-tool redaction before any training or publication work.
