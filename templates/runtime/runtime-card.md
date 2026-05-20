# Runtime Card

## Identity

- Run name:
- Date:
- Operator:
- Platform lane:
- Runtime:
- Model name:
- Endpoint model ID:
- Model revision:
- Artifact location:

## Command

- Start command:
- Environment:
- Base endpoint:
- Hermes endpoint:

## Endpoint Smoke Matrix

| Runtime | Start Command | Base Endpoint | Smoke Prompt | Expected Result | Result |
|---|---|---|---|---|---|
| MLX server | `mlx_lm.server --model <path_to_model_or_hf_repo>` | `http://127.0.0.1:8080/v1` | Return JSON with key `ok` set to true. | `/v1/models` and `/v1/chat/completions` respond and the JSON reply is parseable. | |
| Ollama | `ollama launch hermes` | `http://127.0.0.1:11434/v1` | Return JSON with key `ok` set to true. | Hermes sees the model in its picker and the OpenAI-compatible endpoint responds. | |
| LM Studio | `lms server start --port 1234` | `http://localhost:1234/v1` | Return JSON with key `ok` set to true. | OpenAI-compatible chat completions respond from the LM Studio server. | |
| Specialist runtime | `<runtime-specific launcher>` | `<OpenAI-compatible endpoint>` | Return JSON with key `ok` set to true. | The runtime exposes a parseable `/v1/models` response and a valid chat completion for the recorded lane. | |

## Result

- Status:
- Latency:
- Peak memory:
- Limitation(s):
- Notes:
- Specialist runtime notes:

## SSD Artifact Policy

- Keep merged models, GGUF exports, model caches, and runtime artifacts on SSD-backed paths.
- Do not commit generated weights, exports, or cache directories to Git.
- Record the final artifact path here when the runtime card is used for a real run.

## Follow-Up

- [ ] Record the exact model ID and revision
- [ ] Record the command and endpoint actually used
- [ ] Record the smoke prompt and response
- [ ] Record any runtime limitations or compatibility notes
- [ ] Record the platform lane and any specialist-runtime launcher details
- [ ] Sync or publish only reviewed summaries, not binary artifacts
