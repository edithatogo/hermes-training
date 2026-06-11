# BitNet b1.58 2B Native Runtime Smoke

Run ID: `bitnet-b158-2b-native-smoke-20260612`
Started: 2026-06-11T15:54:37Z
Model: `microsoft/bitnet-b1.58-2B-4T`
Runtime: `/Volumes/PortableSSD/GitHub/BitNet/bin/bitnet`
Model file: `/Volumes/PortableSSD/GitHub/BitNet/models/BitNet-b1.58-2B-4T/ggml-model-i2_s.gguf`
Output log: `/Volumes/PortableSSD/hermes-evals/runtime-format-lanes/recurrent-ssm-bitnet/bitnet-b158-2b-native-smoke-20260612/bitnet.log`

## Result

| Check | Result |
|---|---|
| Native BitNet runtime present | Passed |
| SSD-backed BitNet model file present | Passed |
| Model load | Passed |
| Token generation | Passed |
| Instruction compliance | Failed |
| Exit code | 0 |
| Wall time | 70.42s |
| Maximum resident set size | 1324318720 bytes |
| Model size | 1.10 GiB |
| Context | 512 |
| Generated tokens | 16 |

## Runtime Evidence

The model loaded as `bitnet-b1.58` with GGUF V3 metadata and `I2_S - 2 bpw
ternary` file type. The run used CPU inference with Metal initialization on the
Apple M1 Max, a 512-token context, and a 16-token generation cap.

The generated output did not obey the JSON-only instruction:

```text
Return only JSON: {"ok": true} havingotifyrac ownership understand explanationssit/groups takingSelf began convention usebinding markedtime
```

Timing from the raw log:

```text
load time = 8180.36 ms
prompt eval time = 20656.56 ms / 11 tokens
eval time = 41124.72 ms / 15 runs
total time = 61790.34 ms / 26 tokens
```

## Decision

This is a completed native runtime proof for the recurrent/SSM/BitNet lane. It
does not promote BitNet as a Hermes model. The runtime can load and generate on
the Mac from SSD-backed artifacts, but prompt-following quality is poor on this
bounded smoke. Next work should test an instruct/chat prompt profile, a
conversation-mode prompt, and a small deterministic Hermes extraction/tool-call
suite before any training or default-runtime claim.
