# Granite 4.1 3B Native-Normalized Local Pilot - 2026-06-12

## Summary

Granite 4.1 3B was evaluated through the existing BFCL-style local pilot, then
re-scored with the opt-in Granite native tool-call normalizer:

```text
--score-normalizer granite-native-tool-call
```

This normalizer converts Granite-style native function payloads such as:

```json
{"type":"function","function":{"name":"lookup_customer","parameters":{"customer_id":"CUST-1007"}}}
```

into strict Hermes scoring form without mutating the raw benchmark output.

## Run

Model:

`/Volumes/PortableSSD/huggingface/hub/models--mlx-community--granite-4.1-3b-4bit/snapshots/b1b476b5a17c46b7d6cd663b4a8ed44b66720aef`

Raw strict pilot:

```bash
./.venv/bin/python scripts/run_local_pilot_benchmark.py \
  --suite benchmarks/endpoint_pilots/bfcl_pilot.json \
  --model /Volumes/PortableSSD/huggingface/hub/models--mlx-community--granite-4.1-3b-4bit/snapshots/b1b476b5a17c46b7d6cd663b4a8ed44b66720aef \
  --run-id granite41-3b-mlx-strict-no-extra-pilot-20260612 \
  --max-tokens 96 \
  --require-no-extra-tool-text
```

Native-normalized strict pilot:

```bash
./.venv/bin/python scripts/run_local_pilot_benchmark.py \
  --suite benchmarks/endpoint_pilots/bfcl_pilot.json \
  --model /Volumes/PortableSSD/huggingface/hub/models--mlx-community--granite-4.1-3b-4bit/snapshots/b1b476b5a17c46b7d6cd663b4a8ed44b66720aef \
  --run-id granite41-3b-mlx-granite-native-normalized-strict-pilot-20260612 \
  --max-tokens 96 \
  --score-normalizer granite-native-tool-call \
  --require-no-extra-tool-text
```

SSD output:

`/Volumes/PortableSSD/hermes-evals/standard-benchmarks/local-pilots/granite41-3b-mlx-granite-native-normalized-strict-pilot-20260612`

## Result

### Raw strict pilot

- Pass rate: `0.333`
- Only `bfcl-invalid-tool` passed.
- `bfcl-simple-customer-lookup` emitted JSON, but not Hermes `<tool_call>`
  format.
- `bfcl-parallel-ticket-routing` emitted an incomplete `<tool_call>` wrapper
  and failed the strict no-extra gate.

### Native-normalized strict pilot

| Category | Cases | Pass rate |
|---|---:|---:|
| `tool_call_exact` | 2 | 0.500 |
| `contains_excludes` | 1 | 1.000 |

Overall pass rate: `0.667`.

The score-only normalizer rescued the simple lookup and the invalid-tool
refusal case. The parallel ticket-routing case still failed because the model
did not emit a complete Granite-native payload in the bounded response.

## Decision

- Status: `runtime-adapter-analysis; not-promoted`
- Granite 4.1 3B is a useful local helper/extraction comparison point.
- It is not yet a strict Hermes tool-call default.
