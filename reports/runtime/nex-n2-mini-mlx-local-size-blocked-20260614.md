# Nex N2 Mini MLX Local Size Blocked - 2026-06-14

## Summary

`nex-agi/Nex-N2-mini` was checked as priority 7 in the runtime-proof action
queue. This queue entry is marked as a Mac MLX lane, so the first check was
whether the Apple MLX runtime was present and whether the base or community MLX
artifacts were small enough for a bounded local proof.

The Apple MLX option is installed in the project environment:

- `mlx`: import succeeds
- `mlx_lm`: `0.31.3`

The blocker is artifact size, not missing MLX support.

## Commands

```bash
source scripts/env.sh
./.venv/bin/python - <<'PY'
mods = ['mlx', 'mlx_lm', 'transformers']
for mod in mods:
    try:
        m = __import__(mod)
        print(f'{mod}: installed {getattr(m, "__version__", "unknown")}')
    except Exception as exc:
        print(f'{mod}: unavailable: {type(exc).__name__}: {exc}')
PY
```

```bash
/Users/doughnut/.local/bin/hf download \
  nex-agi/Nex-N2-mini \
  --cache-dir /Volumes/PortableSSD/huggingface/hub \
  --dry-run \
  --json
```

```bash
/Users/doughnut/.local/bin/hf download \
  mlx-community/Nex-N2-mini-nvfp4 \
  --cache-dir /Volumes/PortableSSD/huggingface/hub \
  --dry-run \
  --json
```

```bash
/Users/doughnut/.local/bin/hf download \
  mlx-community/Nex-N2-mini-8bit \
  --cache-dir /Volumes/PortableSSD/huggingface/hub \
  --dry-run \
  --json
```

## Result

- Base repo: 16 safetensor shards totaling roughly `70G`.
- `mlx-community/Nex-N2-mini-nvfp4`: four safetensor shards totaling about
  `20.5G`.
- `mlx-community/Nex-N2-mini-8bit`: larger than the nvfp4 path.
- No local benchmark was run.

## Decision

- Status: `local-size-blocked`
- Keep the lane behind cloud/offload capacity, or wait for a smaller quantized
  MLX artifact.
- Do not treat this as an Apple MLX installation blocker.
