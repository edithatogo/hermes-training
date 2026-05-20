#!/bin/bash
# Show hub and track repo status without mutating anything.

set -euo pipefail

ROOT="$(cd "$(dirname "$0")/.." && pwd)"

echo "== hub =="
git -C "$ROOT" status -sb
echo
git -C "$ROOT" submodule status --recursive || true

for repo in gemma4 lfm2 ollama-pack; do
    echo
    echo "== $repo =="
    git -C "$ROOT/$repo" status -sb
    git -C "$ROOT/$repo" remote -v | sed -n '1,2p'
done
