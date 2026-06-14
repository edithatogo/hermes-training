# MiniCPM V 4.6 GPTQ Acquisition And Runtime Blocked - 2026-06-14

## Summary

`openbmb/MiniCPM-V-4.6-GPTQ` was checked as priority 9 in the runtime-proof
action queue. This package is a GPTQ quantized MiniCPM-V 4.6 lane, so the
runtime proof requires both artifact acquisition and a GPTQ-capable local
runtime.

The dry-run listed one main model artifact:

- `model.safetensors`
- Reported size: `1.9G`

A live download was started into the SSD-backed Hugging Face cache. It did not
make useful progress during the bounded window and was cancelled cleanly.

The current Hermes environment does not yet have the GPTQ helper packages that
would normally be checked before a Transformers-based GPTQ load:

- `auto_gptq`: not installed
- `optimum`: not installed
- `accelerate`: installed `1.14.0`
- `transformers`: installed `5.3.0`

## Commands

```bash
/Users/doughnut/.local/bin/hf download \
  openbmb/MiniCPM-V-4.6-GPTQ \
  --cache-dir /Volumes/PortableSSD/huggingface/hub \
  --dry-run \
  --json
```

```bash
/Users/doughnut/.local/bin/hf download \
  openbmb/MiniCPM-V-4.6-GPTQ \
  model.safetensors \
  --cache-dir /Volumes/PortableSSD/huggingface/hub \
  --json
```

```bash
source scripts/env.sh
./.venv/bin/python - <<'PY'
mods = ['auto_gptq', 'optimum', 'accelerate', 'transformers']
for mod in mods:
    try:
        m = __import__(mod)
        print(f'{mod}: installed {getattr(m, "__version__", "unknown")}')
    except Exception as exc:
        print(f'{mod}: unavailable: {type(exc).__name__}: {exc}')
PY
```

## Result

- Dry-run succeeded.
- Live download stalled at a zero-byte incomplete blob.
- Partial cache namespace:
  `/Volumes/PortableSSD/huggingface/hub/models--openbmb--MiniCPM-V-4.6-GPTQ`
- No GPTQ model load or endpoint pilot was run.

## Decision

- Status: `acquisition-blocked`
- Resume or retry artifact acquisition first.
- After acquisition, install or select a GPTQ-capable runtime before claiming a
  local benchmark.
