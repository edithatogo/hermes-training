# MLX LoRA To PEFT Conversion

Status: `converted`
Source adapter: `/Volumes/PortableSSD/GitHub/hermes-training/gemma4/experiments/qwen3-4b-strict-toolcall-v4-targeted/lora_adapter`
Source model: `Qwen/Qwen3-4B-MLX-4bit`
PEFT base model: `Qwen/Qwen3-4B`
Output: `/Volumes/PortableSSD/hermes-evals/adapters/qwen3-v4-peft-conversion-20260613`

| Field | Value |
|---|---:|
| Input keys | 112 |
| Output keys | 112 |
| LoRA rank | 8 |
| LoRA alpha | 16.0 |
| Layers | 28, 29, 30, 31, 32, 33, 34, 35 |

## Static PEFT Package Validation

- `PeftConfig.from_pretrained("/Volumes/PortableSSD/hermes-evals/adapters/qwen3-v4-peft-conversion-20260613")` loads.
- PEFT type: `PeftType.LORA`.
- Base model: `Qwen/Qwen3-4B`.
- Target modules: `down_proj, gate_proj, k_proj, o_proj, q_proj, up_proj, v_proj`.
- `adapter_model.safetensors` contains 112 tensors.
- First key: `base_model.model.model.layers.28.mlp.down_proj.lora_A.weight`.
- Last key: `base_model.model.model.layers.35.self_attn.v_proj.lora_B.weight`.

## Claim Boundary

Experimental format conversion only; requires PEFT load and behavior smoke before benchmark use.
