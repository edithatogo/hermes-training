#!/usr/bin/env bash
# Run the LFM2 24B-A2B Q4_K_M runtime proof after the GGUF download completes.

set -euo pipefail

ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
source "$ROOT/scripts/env.sh"

MODEL_ID="${MODEL_ID:-lfm2-24b-a2b-q4}"
BASE_URL="${BASE_URL:-http://127.0.0.1:8095/v1}"
PORT="${PORT:-8095}"
CTX_SIZE="${CTX_SIZE:-4096}"
EXPECTED_SIZE="${EXPECTED_SIZE:-14415473952}"
DATE_STAMP="${DATE_STAMP:-$(date +%Y%m%d)}"
SESSION_NAME="${SESSION_NAME:-lfm2_24b_llamacpp_8095}"
LLAMA_SERVER="${LLAMA_SERVER:-/Volumes/PortableSSD/GitHub/llama.cpp/build/bin/llama-server}"
MODEL_PATH="${MODEL_PATH:-/Volumes/PortableSSD/hermes-models/frontier-gguf/lfm2-24b-a2b-q4/LFM2-24B-A2B-Q4_K_M.gguf}"
RUN_ROOT="${RUN_ROOT:-/Volumes/PortableSSD/hermes-evals/runtime-proof-completion/lfm2-24b-a2b-q4-llamacpp-${DATE_STAMP}}"
STD_ROOT="${STD_ROOT:-/Volumes/PortableSSD/hermes-evals/standard-benchmarks}"
LOG_DIR="${LOG_DIR:-/Volumes/PortableSSD/hermes-evals/runtime-proof-completion/logs}"
SERVER_LOG="$LOG_DIR/${MODEL_ID}-llamacpp-${DATE_STAMP}.log"

require_file() {
    local path="$1"
    local label="$2"
    if [[ ! -f "$path" ]]; then
        echo "$label not found: $path" >&2
        exit 1
    fi
}

file_size() {
    python3 - "$1" <<'PY'
import os
import sys
print(os.path.getsize(sys.argv[1]))
PY
}

wait_for_models() {
    local attempts="${1:-90}"
    local delay="${2:-5}"
    for _ in $(seq 1 "$attempts"); do
        if curl -fsS "$BASE_URL/models" >/dev/null 2>&1; then
            return 0
        fi
        sleep "$delay"
    done
    echo "llama.cpp endpoint did not become ready: $BASE_URL/models" >&2
    exit 1
}

run_pilot() {
    local suite_name="$1"
    local suite_path="$2"
    local run_id="${MODEL_ID}-${suite_name}-pilot-nothink-${DATE_STAMP}"
    "$ROOT/.venv/bin/python" "$ROOT/scripts/run_endpoint_pilot_benchmark.py" \
        --model "$MODEL_ID" \
        --suite "$ROOT/$suite_path" \
        --base-url "$BASE_URL" \
        --user-prefix /no_think \
        --run-id "$run_id" \
        --output-dir "$STD_ROOT/endpoint-pilots/$run_id"
}

require_file "$MODEL_PATH" "LFM2 GGUF"
require_file "$LLAMA_SERVER" "llama-server"

actual_size="$(file_size "$MODEL_PATH")"
if [[ "$actual_size" != "$EXPECTED_SIZE" ]]; then
    echo "LFM2 GGUF has unexpected size: $actual_size bytes; expected $EXPECTED_SIZE" >&2
    echo "Do not run runtime proof until acquisition and assembly are complete." >&2
    exit 1
fi

mkdir -p "$RUN_ROOT" "$STD_ROOT/endpoint-tool-call-benchmark" "$STD_ROOT/endpoint-pilots" "$LOG_DIR"

if tmux has-session -t "$SESSION_NAME" 2>/dev/null; then
    echo "tmux session already exists: $SESSION_NAME"
else
    tmux new-session -d -s "$SESSION_NAME" \
        "$LLAMA_SERVER -m '$MODEL_PATH' --host 127.0.0.1 --port '$PORT' --alias '$MODEL_ID' -c '$CTX_SIZE' -ngl auto >'$SERVER_LOG' 2>&1"
    echo "started tmux session: $SESSION_NAME"
fi

wait_for_models

SMOKE_PROMPT='Return exactly this JSON object and nothing else: {"ok": true}' \
    bash "$ROOT/ollama-pack/scripts/runtime_smoke.sh" "$MODEL_ID" "$BASE_URL" \
    | tee "$RUN_ROOT/smoke.txt"

"$ROOT/.venv/bin/python" "$ROOT/scripts/run_endpoint_tool_call_benchmark.py" \
    --model "$MODEL_ID" \
    --suite "$ROOT/benchmarks/tool_call_local/heldout_suite.json" \
    --base-url "$BASE_URL" \
    --user-prefix /no_think \
    --run-id "${MODEL_ID}-llamacpp-heldout-nothink-${DATE_STAMP}" \
    --output-dir "$STD_ROOT/endpoint-tool-call-benchmark/${MODEL_ID}-llamacpp-heldout-nothink-${DATE_STAMP}"

run_pilot "bfcl" "benchmarks/endpoint_pilots/bfcl_pilot.json"
run_pilot "ifeval" "benchmarks/endpoint_pilots/ifeval_pilot.json"
run_pilot "coding" "benchmarks/endpoint_pilots/coding_pilot.json"

cat >"$RUN_ROOT/summary.txt" <<EOF
model_id=$MODEL_ID
base_url=$BASE_URL
model_path=$MODEL_PATH
expected_size=$EXPECTED_SIZE
server_session=$SESSION_NAME
server_log=$SERVER_LOG
heldout_output=$STD_ROOT/endpoint-tool-call-benchmark/${MODEL_ID}-llamacpp-heldout-nothink-${DATE_STAMP}
bfcl_output=$STD_ROOT/endpoint-pilots/${MODEL_ID}-bfcl-pilot-nothink-${DATE_STAMP}
ifeval_output=$STD_ROOT/endpoint-pilots/${MODEL_ID}-ifeval-pilot-nothink-${DATE_STAMP}
coding_output=$STD_ROOT/endpoint-pilots/${MODEL_ID}-coding-pilot-nothink-${DATE_STAMP}
EOF

echo "LFM2 runtime proof complete. Summary: $RUN_ROOT/summary.txt"
