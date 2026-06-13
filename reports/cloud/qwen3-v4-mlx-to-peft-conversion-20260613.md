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

## Claim Boundary

Experimental format conversion only; requires PEFT load and behavior smoke before benchmark use.
