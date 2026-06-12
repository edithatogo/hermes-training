# EXAONE 4.0 1.2B Q4_K_M llama.cpp Strict BFCL Pilot - 2026-06-13

## Summary

`LGAI-EXAONE/EXAONE-4.0-1.2B-GGUF` was run through the strict Hermes
BFCL-style endpoint pilot using the cached SSD GGUF artifact and Homebrew
llama.cpp server.

Result: `0/3` cases passed, pass rate `0.000`.

This is promotion-blocking evidence. The model loads quickly and is small enough
for the local Mac runtime lane, but it does not follow Hermes tool-call
contracts under the strict prompt.

## Artifact

- Repo: `LGAI-EXAONE/EXAONE-4.0-1.2B-GGUF`
- File: `EXAONE-4.0-1.2B-Q4_K_M.gguf`
- Local path:
  `/Volumes/PortableSSD/huggingface/hub/models--LGAI-EXAONE--EXAONE-4.0-1.2B-GGUF/snapshots/162446400ea4596377a3ce1d3ddffa32971af0a6/EXAONE-4.0-1.2B-Q4_K_M.gguf`
- Storage: external SSD cache under `/Volumes/PortableSSD/huggingface/hub`
- Cache size: `790M`

## Server

```bash
/opt/homebrew/bin/llama-server \
  -m /Volumes/PortableSSD/huggingface/hub/models--LGAI-EXAONE--EXAONE-4.0-1.2B-GGUF/snapshots/162446400ea4596377a3ce1d3ddffa32971af0a6/EXAONE-4.0-1.2B-Q4_K_M.gguf \
  --host 127.0.0.1 \
  --port 18083 \
  --ctx-size 4096 \
  --alias lgai-exaone-4-0-1-2b-q4km \
  --jinja \
  -ngl 999
```

llama.cpp selected `peg-native` chat formatting. During the short pilot calls it
reported roughly `155-161` generation tokens per second.

Runtime warning:

```text
special_eos_id is not in special_eog_ids - the tokenizer config may be incorrect
```

## Benchmark

```bash
source scripts/env.sh
./.venv/bin/python scripts/run_endpoint_pilot_benchmark.py \
  --model lgai-exaone-4-0-1-2b-q4km \
  --base-url http://127.0.0.1:18083/v1 \
  --suite benchmarks/endpoint_pilots/bfcl_pilot.json \
  --run-id exaone4-12b-q4km-llamacpp-strict-bfcl-pilot-20260613 \
  --max-tokens 256 \
  --require-no-extra-tool-text
```

SSD output:

`/Volumes/PortableSSD/hermes-evals/standard-benchmarks/endpoint-pilots/exaone4-12b-q4km-llamacpp-strict-bfcl-pilot-20260613`

## Result

| Case | Result | Note |
|---|---:|---|
| `bfcl-simple-customer-lookup` | fail | Refused to use the listed lookup tool and suggested external CRM/support steps. |
| `bfcl-parallel-ticket-routing` | fail | Wrote a prose ticket instead of emitting the two required tool calls. |
| `bfcl-invalid-tool` | fail | Suggested `delete_customer_record`, the unavailable tool name that the gate explicitly forbids. |

## Decision

- Status: `strict-endpoint-pilot-complete; not-promoted`
- Do not promote to Hermes default, training, or publication.
- Keep only as a tiny local runtime comparison lane unless a future prompt
  profile or adapter explicitly repairs strict tool-use behavior.
