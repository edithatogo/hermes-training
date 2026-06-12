# Dataset Publication Live Record - 2026-06-12

Status: published

Approved user scope:

```text
I approve publishing the cleaned synthetic-only dataset at /Volumes/PortableSSD/hermes-evals/datasets/qwen3-v4-synthetic-only-20260526 to Hugging Face dataset repo edithatogo/qwen3-hermes-strict-toolcall-synthetic-v4.
```

Published Hugging Face dataset:

```text
https://huggingface.co/datasets/edithatogo/qwen3-hermes-strict-toolcall-synthetic-v4
```

Publication commit:

```text
727e7e4ecd781aca2f7506d4a8fc6d910f521d6d
```

Published local source path:

```text
/Volumes/PortableSSD/hermes-evals/datasets/qwen3-v4-synthetic-only-20260526
```

Uploaded files:

- `README.md`
- `materialization-summary.json`
- `train.jsonl`
- `validation.jsonl`
- `test.jsonl`

Published split counts:

| Split | Rows |
|---|---:|
| train | 72 |
| validation | 5 |
| test | 5 |

Total rows: 82

Unique IDs: 82

Duplicate IDs: 0

Included source families:

- `strict_tool_call_expansion_v1`
- `strict_tool_call_expansion_v2_format_guard`
- `strict_tool_call_expansion_v4_targeted`

Verification commands:

```text
hf auth whoami
hf repos create edithatogo/qwen3-hermes-strict-toolcall-synthetic-v4 --type dataset --exist-ok
hf upload edithatogo/qwen3-hermes-strict-toolcall-synthetic-v4 /tmp/qwen3-hermes-strict-toolcall-synthetic-v4-publish --type dataset --commit-message "Publish cleaned synthetic-only strict tool-call dataset"
hf datasets info edithatogo/qwen3-hermes-strict-toolcall-synthetic-v4 --format json
hf download edithatogo/qwen3-hermes-strict-toolcall-synthetic-v4 --type dataset --include README.md train.jsonl validation.jsonl test.jsonl materialization-summary.json --dry-run
```

Remote verification summary:

- repository exists
- repository is public
- repository is ungated
- remote SHA: `727e7e4ecd781aca2f7506d4a8fc6d910f521d6d`
- remote siblings include `.gitattributes`, `README.md`, `materialization-summary.json`, `train.jsonl`, `validation.jsonl`, and `test.jsonl`
