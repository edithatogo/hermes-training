# PortableSSD Root Migration Audit

Date: 2026-05-24

Status: narrow migration completed on 2026-05-24.

## Purpose

Check whether development folders currently sitting directly under
`/Volumes/PortableSSD` should be migrated under `/Volumes/PortableSSD/GitHub`.

## Summary

Most top-level folders are intentional SSD-backed artifact, cache, app-state, or
media roots and should not be moved into `GitHub`.

After a broader pass over the root folder, the original conservative approach
was confirmed: there was no evidence of a broad set of misplaced project
folders. The only Git checkout found outside `/Volumes/PortableSSD/GitHub` was
`/Volumes/PortableSSD/hermes-tools/llama.cpp`, and that checkout has now been
migrated under `GitHub` with a compatibility symlink left at the old path.

The only strong code-repository candidate found outside `GitHub` was:

| Path | Classification | Current state | Recommendation |
|---|---|---|---|
| `/Volumes/PortableSSD/hermes-tools/llama.cpp` | Compatibility symlink to `GitHub/llama.cpp-convert-tool` | points to migrated checkout | Keep symlink in place for existing Hermes tooling. |
| `/Volumes/PortableSSD/GitHub/llama.cpp-convert-tool` | Git checkout of `ggerganov/llama.cpp` | clean working tree, branch `master`, HEAD `ad27757` | Use this as the conversion/tool checkout. Do not merge it into the dirty `GitHub/llama.cpp` checkout. |

## Full Root Pass Evidence

The root folder contains these broad categories:

| Category | Paths | Migration assessment |
|---|---|---|
| Source repo root | `/Volumes/PortableSSD/GitHub` | Correct place for project source. |
| Model/eval artifacts | `/Volumes/PortableSSD/hermes-evals`, `/Volumes/PortableSSD/hermes-exports`, `/Volumes/PortableSSD/hermes-models`, `/Volumes/PortableSSD/models` | Keep outside GitHub; these are large generated or downloaded assets. |
| Runtime model stores | `/Volumes/PortableSSD/Ollama`, `/Volumes/PortableSSD/ollama-models`, `/Volumes/PortableSSD/huggingface` | Keep stable; moving would break cache/runtime configuration. |
| Benchmark placeholders | `/Volumes/PortableSSD/lm-eval`, `/Volumes/PortableSSD/opencompass`, `/Volumes/PortableSSD/helm` | Keep outside GitHub; referenced as benchmark/output roots, not source repos. |
| Caches/toolchains | `/Volumes/PortableSSD/cache`, `/Volumes/PortableSSD/homebrew-cache`, `/Volumes/PortableSSD/pip-cache`, `/Volumes/PortableSSD/uv-cache`, `/Volumes/PortableSSD/.pnpm-store`, `/Volumes/PortableSSD/toolchains`, `/Volumes/PortableSSD/torch` | Keep outside GitHub. |
| App/user state | `/Volumes/PortableSSD/appdata`, `/Volumes/PortableSSD/home-relocated`, `/Volumes/PortableSSD/userdata` | Keep outside GitHub. |
| Media/user data | `/Volumes/PortableSSD/Movies`, `/Volumes/PortableSSD/OneDrive`, `/Volumes/PortableSSD/installers` | Keep outside GitHub. |
| Scratch/test | `/Volumes/PortableSSD/tmp`, `/Volumes/PortableSSD/tmp-test`, `/Volumes/PortableSSD/test_speed.bin` | Do not migrate to GitHub. |
| Tool checkout | `/Volumes/PortableSSD/GitHub/llama.cpp-convert-tool` with `/Volumes/PortableSSD/hermes-tools/llama.cpp` symlink | Migrated under GitHub while preserving old path compatibility. |

Searches for source markers outside `GitHub` only found:

- `/Volumes/PortableSSD/hermes-tools/llama.cpp`: real Git checkout with
  `CMakeLists.txt`, `pyproject.toml`, `requirements.txt`, and `README.md`.
- `/Volumes/PortableSSD/appdata/continue/package.json`: Continue app
  configuration (`continue-config`), not a project source tree.
- `/Volumes/PortableSSD/hermes-training-envs/.venv`: shared Python environment,
  not source.

The checkout scan found only one `.git` directory outside `GitHub` before
migration:

```text
/Volumes/PortableSSD/hermes-tools/llama.cpp/.git
```

After migration, that checkout lives at:

```text
/Volumes/PortableSSD/GitHub/llama.cpp-convert-tool/.git
```

## Root Folders That Should Stay at SSD Root

These are not project source folders. They are shared artifact/cache/runtime
roots referenced by the Hermes tooling and should remain stable:

| Path | Reason |
|---|---|
| `/Volumes/PortableSSD/huggingface` | Hugging Face cache root. Referenced by `HF_HOME` / `HF_HUB_CACHE`. |
| `/Volumes/PortableSSD/hermes-evals` | Raw benchmark output root. Reports in Git link back to these outputs. |
| `/Volumes/PortableSSD/hermes-exports` | GGUF/export artifact root. Intentionally outside Git. |
| `/Volumes/PortableSSD/hermes-models` | Frontier GGUF/model acquisition root. Intentionally outside Git. |
| `/Volumes/PortableSSD/Ollama` and `/Volumes/PortableSSD/ollama-models` | Ollama model stores. Do not move. |
| `/Volumes/PortableSSD/hermes-training-envs` | Shared Python venv root for this work. |
| `/Volumes/PortableSSD/cache`, `/Volumes/PortableSSD/pip-cache`, `/Volumes/PortableSSD/uv-cache`, `/Volumes/PortableSSD/homebrew-cache`, `/Volumes/PortableSSD/.pnpm-store` | Package/build caches. |
| `/Volumes/PortableSSD/toolchains` | Toolchain installs and venvs. |
| `/Volumes/PortableSSD/appdata`, `/Volumes/PortableSSD/home-relocated`, `/Volumes/PortableSSD/userdata` | App/user state relocation roots. |
| `/Volumes/PortableSSD/OneDrive`, `/Volumes/PortableSSD/Movies` | Non-development user data/media. |

## Ambiguous But Not Migration Candidates

| Path | Finding | Recommendation |
|---|---|---|
| `/Volumes/PortableSSD/lm-eval` | Empty cache/output placeholder. Referenced as benchmark/output root in `conductor/tech-stack.md`. | Keep at root or remove only if no benchmark workflow uses it. Do not move to `GitHub`. |
| `/Volumes/PortableSSD/opencompass` | Empty `cache/` and `datasets/` placeholders. Referenced as benchmark/output root. | Keep at root. |
| `/Volumes/PortableSSD/helm` | Empty placeholder. Referenced as benchmark/output root. | Keep at root or remove later if unused. Do not move to `GitHub`. |
| `/Volumes/PortableSSD/torch` | Empty placeholder. Likely intended for `TORCH_HOME` or torch cache. | Keep at root if `TORCH_HOME` may point here. |
| `/Volumes/PortableSSD/models` | Model artifact tree, currently includes `baa-ai/Qwen3.6-35B-A3B-RAM-19GB-MLX`. | Keep at root; this is a model artifact root, not source. |
| `/Volumes/PortableSSD/appdata/continue` | Continue app configuration with a small `package.json` named `continue-config`. | Keep under app state; do not move into `GitHub`. |

## Existing GitHub Conflict

`/Volumes/PortableSSD/GitHub/llama.cpp` already exists:

```text
remote: https://github.com/ggml-org/llama.cpp.git
branch: master
working tree: dirty
```

Observed local changes include:

```text
M convert_hf_to_gguf.py
M tools/server/server-http.h
?? conductor/
?? convert_hf_to_gguf.py.bak
?? quantize
?? src/models/lfm2.cpp.bak
```

Because that checkout is dirty, do not replace or merge it automatically with
`/Volumes/PortableSSD/GitHub/llama.cpp-convert-tool`.

## Path Compatibility

Hermes tooling currently expects the tool checkout at the root-level path unless
`HERMES_LLAMA_CPP` is overridden. For example,
`ollama-pack/scripts/export_ollama.sh` uses:

```bash
LLAMA_CPP="${HERMES_LLAMA_CPP:-${HERMES_STORAGE_ROOT:-$REPO_DIR}/hermes-tools/llama.cpp}"
```

That means any migration needs either a compatibility symlink or explicit
environment override. The compatibility symlink is now in place:

```text
/Volumes/PortableSSD/hermes-tools/llama.cpp -> /Volumes/PortableSSD/GitHub/llama.cpp-convert-tool
```

## Migration Verification

Commands verified after migration:

```text
git status --short: clean
remote: https://github.com/ggerganov/llama.cpp.git
branch: master
HEAD: ad27757
symlink target: /Volumes/PortableSSD/GitHub/llama.cpp-convert-tool
old path compatibility: compatible
```

`ollama-pack/scripts/export_ollama.sh` was also updated in the nested
`ollama-pack` checkout to resolve llama.cpp in this order:

1. `HERMES_LLAMA_CPP`, when explicitly set.
2. `$HERMES_STORAGE_ROOT/GitHub/llama.cpp-convert-tool`, when present.
3. `$HERMES_STORAGE_ROOT/hermes-tools/llama.cpp`, as the legacy fallback.

`scripts/check_storage_layout.py` now provides a bounded repeatable validation
for the SSD layout. It checks expected root directories, the canonical
llama.cpp checkout, the legacy symlink, and stray Git checkouts outside
`GitHub` within a limited depth:

```bash
./scripts/check_storage_layout.py --root /Volumes/PortableSSD
```

The checker is also called by `scripts/validate_readiness.py` when the storage
root is present, and surfaced in `scripts/repo_status.sh` for quick read-only
workspace status checks.

Latest result:

```text
ok: canonical llama.cpp checkout at GitHub/llama.cpp-convert-tool
ok: llama.cpp converter at GitHub/llama.cpp-convert-tool/convert_hf_to_gguf.py
ok: legacy llama.cpp symlink points to GitHub/llama.cpp-convert-tool
ok: no git checkouts outside GitHub within depth 4
```

Unit coverage was added in `tests/test_check_storage_layout.py` for:

- valid canonical checkout plus legacy symlink
- wrong legacy symlink target
- missing converter file
- stray Git checkout outside `GitHub`

Latest test command:

```bash
PYTHONPATH=. python3 -m unittest discover -s tests
```

Latest result: 9 tests passed.

This preserves any tooling that expects the old `hermes-tools/llama.cpp` path
while keeping the actual checkout under `GitHub`.

## Conservative Recommendation

Do not move any additional root folders into `GitHub`.

The current layout is mostly intentional:

- source repos live under `/Volumes/PortableSSD/GitHub`
- large artifacts and caches live at `/Volumes/PortableSSD/<artifact-root>`
- `hermes-tools/llama.cpp` was the lone exception and is now a compatibility
  symlink to `/Volumes/PortableSSD/GitHub/llama.cpp-convert-tool`
- there is still an active dirty `/Volumes/PortableSSD/GitHub/llama.cpp`
  checkout, so the converted tool checkout should remain separate

The best next step is to keep using
`/Volumes/PortableSSD/GitHub/llama.cpp-convert-tool` for conversion-tool work
and leave the symlink in place for scripts that expect the historical root-level
tool path.
