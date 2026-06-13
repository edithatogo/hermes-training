# HF Publication Gate: Qwen3 4B Strict Tool-Call V6 Free-Text Copy

Date: 2026-06-13

## Status

Blocked as intended. No Hugging Face publication action was performed.

## Package

SSD package:

```text
/Volumes/PortableSSD/hermes-exports/hf/qwen3-4b-hermes-strict-toolcall-v6-free-text-copy-20260613
```

Target model repo if approved later:

```text
edithatogo/qwen3-4b-hermes-strict-toolcall-v6-free-text-copy
```

## Validated Files

| File | Bytes |
|---|---:|
| `adapters.safetensors` | 14,692,068 |
| `adapter_config.json` | 351 |
| `README.md` | 2,571 |
| `package-manifest.json` | 4,341 |
| `publication-preflight-dry-run.json` | 1,658 |
| `publication-preflight-publish-blocked.json` | 1,735 |

## Preflight Evidence

Dry-run preflight command:

```bash
./.venv/bin/python scripts/publish_hf_adapter_package.py \
  --package-dir /Volumes/PortableSSD/hermes-exports/hf/qwen3-4b-hermes-strict-toolcall-v6-free-text-copy-20260613 \
  --repo-id edithatogo/qwen3-4b-hermes-strict-toolcall-v6-free-text-copy \
  --json
```

Result:

- Package directory exists.
- Package is under `/Volumes/PortableSSD/hermes-exports`.
- Required adapter, config, README, and manifest files exist.
- Manifest repo target matches.
- Manifest copied-file targets exist.
- Publication remains blocked because manifest blockers are still present.

Publish-mode preflight without approval:

```bash
./.venv/bin/python scripts/publish_hf_adapter_package.py \
  --package-dir /Volumes/PortableSSD/hermes-exports/hf/qwen3-4b-hermes-strict-toolcall-v6-free-text-copy-20260613 \
  --repo-id edithatogo/qwen3-4b-hermes-strict-toolcall-v6-free-text-copy \
  --publish \
  --json
```

Result: exit code `2`; `publish_action_performed=false`.

## Required Approval Phrase

```text
I approve publishing HF adapter package /Volumes/PortableSSD/hermes-exports/hf/qwen3-4b-hermes-strict-toolcall-v6-free-text-copy-20260613 to Hugging Face model repo edithatogo/qwen3-4b-hermes-strict-toolcall-v6-free-text-copy.
```

This approval phrase alone is not enough while the manifest still lists
publication blockers. The v6 bundle also needs final model-card review and an
explicit benchmark-scope decision before public release.
