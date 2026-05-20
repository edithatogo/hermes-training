#!/usr/bin/env bash
set -euo pipefail

# Shared local runtime defaults for Hermes training scripts.
#
# Override HERMES_STORAGE_ROOT when using a different external volume.
# The default keeps model caches and temp files off the internal disk.
if [[ -z "${HERMES_STORAGE_ROOT:-}" ]]; then
  if [[ -d /Volumes/PortableSSD ]]; then
    HERMES_STORAGE_ROOT="/Volumes/PortableSSD"
  else
    HERMES_STORAGE_ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)/.local-storage"
  fi
fi

export HERMES_STORAGE_ROOT
export HF_HOME="${HF_HOME:-$HERMES_STORAGE_ROOT/huggingface}"
export HF_HUB_CACHE="${HF_HUB_CACHE:-$HF_HOME/hub}"
export HF_HUB_DISABLE_XET="${HF_HUB_DISABLE_XET:-1}"
export HF_DATASETS_CACHE="${HF_DATASETS_CACHE:-$HF_HOME/datasets}"
export TRANSFORMERS_CACHE="${TRANSFORMERS_CACHE:-$HF_HOME/transformers}"
export XDG_CACHE_HOME="${XDG_CACHE_HOME:-$HERMES_STORAGE_ROOT/cache}"
export PIP_CACHE_DIR="${PIP_CACHE_DIR:-$HERMES_STORAGE_ROOT/pip-cache}"
export TORCH_HOME="${TORCH_HOME:-$HERMES_STORAGE_ROOT/torch}"
export LM_HARNESS_CACHE_PATH="${LM_HARNESS_CACHE_PATH:-$HERMES_STORAGE_ROOT/lm-eval/cache}"
export HELM_HOME="${HELM_HOME:-$HERMES_STORAGE_ROOT/helm}"
export OPENCOMPASS_CACHE_DIR="${OPENCOMPASS_CACHE_DIR:-$HERMES_STORAGE_ROOT/opencompass/cache}"
export OPENCOMPASS_DATASETS="${OPENCOMPASS_DATASETS:-$HERMES_STORAGE_ROOT/opencompass/datasets}"
export HERMES_EVAL_ROOT="${HERMES_EVAL_ROOT:-$HERMES_STORAGE_ROOT/hermes-evals}"
export HERMES_EXPORT_ROOT="${HERMES_EXPORT_ROOT:-$HERMES_STORAGE_ROOT/hermes-exports}"

if [[ -n "${HERMES_TMPDIR:-}" ]]; then
  export TMPDIR="$HERMES_TMPDIR"
elif [[ "${HERMES_USE_SYSTEM_TMP:-0}" != "1" ]]; then
  export TMPDIR="$HERMES_STORAGE_ROOT/tmp"
fi

mkdir -p \
  "$HF_HUB_CACHE" \
  "$HF_DATASETS_CACHE" \
  "$TRANSFORMERS_CACHE" \
  "$XDG_CACHE_HOME" \
  "$PIP_CACHE_DIR" \
  "$TORCH_HOME" \
  "$LM_HARNESS_CACHE_PATH" \
  "$HELM_HOME" \
  "$OPENCOMPASS_CACHE_DIR" \
  "$OPENCOMPASS_DATASETS" \
  "$HERMES_EVAL_ROOT" \
  "$HERMES_EXPORT_ROOT" \
  "$TMPDIR"
