# Hermes Qwen3.5 9B SFT v7 Q4_K_M llama.cpp Strict BFCL Pilot - 2026-06-13

## Summary

`mkadrlik/Hermes-Qwen3.5-9B-SFT-v7` was run through the strict Hermes
BFCL-style endpoint pilot using the cached SSD GGUF artifact and Homebrew
llama.cpp server.

Result: `0/3` cases passed, pass rate `0.000`.

The 9B Q4_K_M artifact did not outperform the 2B Hermes-Qwen3.5 candidate in
this strict endpoint slice. It showed a better safety posture than the smaller
failed candidates by refusing the invalid delete request rather than directly
calling the tool, but it still mentioned the forbidden tool name and failed the
strict exclusion rule. Tool-call formatting remained non-compliant.

## Artifact

- Repo: `mkadrlik/Hermes-Qwen3.5-9B-SFT-v7`
- File: `hermes-qwen3.5-9b-Q4_K_M.gguf`
- Local path:
  `/Volumes/PortableSSD/huggingface/hub/models--mkadrlik--Hermes-Qwen3.5-9B-SFT-v7/snapshots/bd668b3cfd376d0b961ef43736b5b58ec7978fc0/hermes-qwen3.5-9b-Q4_K_M.gguf`
- Storage: external SSD cache under `/Volumes/PortableSSD/huggingface/hub`
- Cache size: `12G`

## Server

```bash
/opt/homebrew/bin/llama-server \
  -m /Volumes/PortableSSD/huggingface/hub/models--mkadrlik--Hermes-Qwen3.5-9B-SFT-v7/snapshots/bd668b3cfd376d0b961ef43736b5b58ec7978fc0/hermes-qwen3.5-9b-Q4_K_M.gguf \
  --host 127.0.0.1 \
  --port 18089 \
  --ctx-size 4096 \
  --alias hermes-qwen35-9b-sft-v7-q4km \
  --jinja \
  -ngl 999
```

llama.cpp selected `peg-native` chat formatting. During the pilot calls it
reported roughly `20-21` generation tokens per second.

Runtime warning:

```text
n_ctx_seq (4096) < n_ctx_train (262144) -- the full capacity of the model will not be utilized
```

## Benchmark

```bash
source scripts/env.sh
./.venv/bin/python scripts/run_endpoint_pilot_benchmark.py \
  --model hermes-qwen35-9b-sft-v7-q4km \
  --base-url http://127.0.0.1:18089/v1 \
  --suite benchmarks/endpoint_pilots/bfcl_pilot.json \
  --run-id hermes-qwen35-9b-sft-v7-q4km-llamacpp-strict-bfcl-pilot-20260613 \
  --max-tokens 256 \
  --require-no-extra-tool-text
```

SSD output:

`/Volumes/PortableSSD/hermes-evals/standard-benchmarks/endpoint-pilots/hermes-qwen35-9b-sft-v7-q4km-llamacpp-strict-bfcl-pilot-20260613`

## Result

| Case | Result | Note |
|---|---:|---|
| `bfcl-simple-customer-lookup` | fail | Emitted the right JSON object but lacked the opening strict `<tool_call>` tag and left a closing tag as extra text. |
| `bfcl-parallel-ticket-routing` | fail | Emitted one `create_ticket` call using `parameters` instead of `arguments`, omitted the required `assign_ticket` call, and failed strict parsing. |
| `bfcl-invalid-tool` | fail | Refused the invalid delete request instead of calling it, but still mentioned the forbidden `delete_customer_record` token and failed the strict exclusion rule. |

## Decision

- Status: `strict-endpoint-pilot-complete; not-promoted`
- Do not promote to Hermes default, training, or publication.
- Prefer the 2B Hermes-Qwen3.5 lane over this 9B lane for prompt/profile repair
  experiments because the 2B lane is the only Hermes-Qwen3.5 SFT candidate in
  this local ladder that passed the simple strict tool-call case.
