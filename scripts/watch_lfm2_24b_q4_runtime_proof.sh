#!/usr/bin/env bash
# Wait for the LFM2 24B-A2B GGUF to finish assembling, then run its runtime proof.

set -euo pipefail

ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
source "$ROOT/scripts/env.sh"

MODEL_PATH="${MODEL_PATH:-/Volumes/PortableSSD/hermes-models/frontier-gguf/lfm2-24b-a2b-q4/LFM2-24B-A2B-Q4_K_M.gguf}"
EXPECTED_SIZE="${EXPECTED_SIZE:-14415473952}"
POLL_SECONDS="${POLL_SECONDS:-300}"
MAX_WAIT_SECONDS="${MAX_WAIT_SECONDS:-0}"
RUN_LOG_DIR="${RUN_LOG_DIR:-/Volumes/PortableSSD/hermes-evals/runtime-proof-completion/logs}"
WATCH_LOG="${WATCH_LOG:-$RUN_LOG_DIR/lfm2-24b-a2b-q4-proof-watch-20260525.log}"
LOCK_DIR="${LOCK_DIR:-/Volumes/PortableSSD/hermes-evals/runtime-proof-completion/lfm2-24b-proof-watch.lock}"

mkdir -p "$RUN_LOG_DIR"

log() {
    printf '%s %s\n' "$(date '+%Y-%m-%dT%H:%M:%S%z')" "$*" | tee -a "$WATCH_LOG"
}

file_size() {
    if [[ -f "$1" ]]; then
        python3 - "$1" <<'PY'
import os
import sys
print(os.path.getsize(sys.argv[1]))
PY
    else
        echo 0
    fi
}

if ! mkdir "$LOCK_DIR" 2>/dev/null; then
    log "watcher already active: $LOCK_DIR"
    exit 0
fi
trap 'rmdir "$LOCK_DIR" 2>/dev/null || true' EXIT

started_at="$(date +%s)"
log "watching model_path=$MODEL_PATH expected_size=$EXPECTED_SIZE poll_seconds=$POLL_SECONDS"

while true; do
    actual_size="$(file_size "$MODEL_PATH")"
    if [[ "$actual_size" == "$EXPECTED_SIZE" ]]; then
        log "complete file detected; starting runtime proof"
        bash "$ROOT/scripts/run_lfm2_24b_q4_runtime_proof.sh" 2>&1 | tee -a "$WATCH_LOG"
        log "runtime proof command finished"
        exit 0
    fi

    if [[ -f "$MODEL_PATH" && "$actual_size" != "$EXPECTED_SIZE" ]]; then
        log "final path exists but size is not complete: actual=$actual_size expected=$EXPECTED_SIZE"
    else
        log "waiting for final GGUF: actual=$actual_size expected=$EXPECTED_SIZE"
    fi

    if [[ "$MAX_WAIT_SECONDS" != "0" ]]; then
        now="$(date +%s)"
        elapsed=$((now - started_at))
        if (( elapsed >= MAX_WAIT_SECONDS )); then
            log "max wait reached without complete file: elapsed=$elapsed"
            exit 1
        fi
    fi

    sleep "$POLL_SECONDS"
done
