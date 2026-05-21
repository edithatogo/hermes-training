# Runtime Run Card: Qwen3.6 and Hermes 4 SSD-First Proof

## Identity

- Run name: `qwen36-hermes4-runtime-proof`
- Date: 2026-05-22
- Platform lane: Mac local runtime proof
- Storage policy: SSD-first, no large downloads
- Track: `conductor/tracks/qwen36-runtime-proof_20260522`

## Candidate Targets

| Target | Role | Expected Runtime | Local Artifact Result |
|---|---|---|---|
| `Qwen/Qwen3.6-35B-A3B` | frontier MoE runtime/teacher candidate | LM Studio/Ollama GGUF or KTransformers if supported | no local artifact found |
| `NousResearch/Hermes-4-14B` | Hermes-aligned baseline/teacher | LM Studio/Ollama GGUF or Transformers | no local artifact found |
| `NousResearch/Hermes-4.3-36B` | newer public Hermes baseline/teacher | Transformers or compatible GGUF after proof | no local artifact found |

## Local Artifact Scan

Commands were run from `/Volumes/PortableSSD/GitHub/hermes-training`.

```bash
find /Volumes/PortableSSD -maxdepth 5 \
  \( -iname '*qwen3.6*' -o -iname '*qwen3-6*' -o -iname '*hermes*4*' -o -iname '*Hermes-4*' \) \
  -print
```

Relevant results:

- no Qwen3.6 GGUF, MLX, safetensors, or KTransformers artifact found
- no Hermes 4 GGUF, MLX, or safetensors artifact found
- existing local large artifact remains the Qwen3 4B smoke GGUF under `/Volumes/PortableSSD/hermes-exports/ollama/qwen3-4b-hermes-smoke/`

Hugging Face cache scan:

```bash
find /Volumes/PortableSSD/huggingface/hub -maxdepth 3 -type d \
  \( -iname '*Qwen3.6*' -o -iname '*Hermes-4*' -o -iname '*Qwen3-4B-MLX-4bit*' \) \
  -print
```

Relevant result:

- cached: `/Volumes/PortableSSD/huggingface/hub/models--Qwen--Qwen3-4B-MLX-4bit`
- not cached: Qwen3.6 and Hermes 4

Additional targeted scans:

```bash
find /Volumes/PortableSSD/huggingface/hub -maxdepth 2 -type d \
  \( -name 'models--Qwen--Qwen3.6*' -o -name 'models--lmstudio-community--Qwen3.6*' -o -name 'models--unsloth--Qwen3.6*' -o -name 'models--NousResearch--Hermes-4*' \) \
  -print

find /Volumes/PortableSSD/hermes-exports /Volumes/PortableSSD/huggingface/hub /Volumes/PortableSSD/GitHub/hermes-training -maxdepth 6 -type f \
  \( -iname '*.gguf' -o -iname '*.safetensors' -o -iname 'config.json' -o -iname 'Modelfile*' \) |
  rg -i 'qwen3\.6|qwen3-6|qwen36|hermes-4|hermes4|qwen3\.7|qwen37'
```

Both targeted scans returned no Qwen3.6 or Hermes 4 runnable model artifact.

## Endpoint Checks

Commands:

```bash
ollama list
curl -sS --max-time 2 http://127.0.0.1:11434/v1/models
curl -sS --max-time 2 http://127.0.0.1:8080/v1/models
curl -sS --max-time 2 http://127.0.0.1:1234/v1/models
```

Results:

- `ollama list`: `Error: could not connect to ollama server, run 'ollama serve' to start it`
- Ollama OpenAI-compatible endpoint `127.0.0.1:11434`: connection refused
- MLX server endpoint `127.0.0.1:8080`: connection refused
- LM Studio endpoint `127.0.0.1:1234`: connection refused
- `llama-server`, `llama-cli`, and `llama-completion` are installed, but no Qwen3.6 or Hermes 4 GGUF was available to serve.

Environment guardrail check:

```bash
source scripts/env.sh
printf 'HF_HOME=%s\nHF_HUB_CACHE=%s\nHERMES_EXPORT_ROOT=%s\nTMPDIR=%s\n' "$HF_HOME" "$HF_HUB_CACHE" "$HERMES_EXPORT_ROOT" "$TMPDIR"
```

Result:

- `HF_HOME=/Volumes/PortableSSD/huggingface`
- `HF_HUB_CACHE=/Volumes/PortableSSD/huggingface/hub`
- `HERMES_EXPORT_ROOT=/Volumes/PortableSSD/hermes-exports`
- `TMPDIR=/Volumes/PortableSSD/tmp`

## Decision

The runtime proof is complete as a no-download pass. Qwen3.6 and Hermes 4 remain valid next runtime targets, but no smoke test can be run until an SSD-backed artifact is deliberately obtained or an existing endpoint is provided.

Do not infer runtime compatibility from model-card availability alone. The next pass should choose an exact quantized artifact, estimate disk/RAM cost, and then download under `scripts/env.sh` only after the user explicitly wants that larger model pull.
