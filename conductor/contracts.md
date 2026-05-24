# Contracts — Hermes Training Hub

## COND-001: Conductor Repository Structure

Required files for each Conductor root:

```text
conductor/
├── index.md
├── product.md
├── tech-stack.md
├── workflow.md
└── tracks.md
```

Hub roots also require:

```text
conductor/product-guidelines.md
conductor/requirements.md
conductor/design.md
conductor/contracts.md
```

## DATA-001: Chat JSONL Split

Each line:

```json
{
  "id": "string",
  "messages": [
    {"role": "system|user|assistant", "content": "string"}
  ]
}
```

Required split files:

- `train.jsonl`
- `val.jsonl`
- `valid.jsonl`
- `test.jsonl`

`valid.jsonl` is required for current `mlx-lm` compatibility.

## TRAIN-001: MLX LoRA Config

Required YAML keys:

```yaml
model: string
adapter_path: string
data: string
lora_rank: integer
lora_scale: float
lora_layers: integer
batch_size: integer
iters: integer
max_seq_length: integer
learning_rate: float
```

Configs must support `--dry-run` through the track launcher.

## MODEL-001: Model Radar Entry

Each candidate in `MODEL_CANDIDATES.yaml` must include:

```yaml
id: string
family: string
tier: string
role: local-finetune | local-runtime | cloud-teacher | cloud-finetune | retrieval | research-runtime | watchlist
environment: mac-mlx | mac-ollama | mac-lmstudio | azure-cuda | hf-transformers | specialist-runtime
feasibility: ready | needs-auth | needs-runtime-proof | cloud-only | speculative
parameters: string
architecture: string
license: string
first_runtime: string
first_finetune: string
notes: string
```

Watchlist entries may point to speculative or unverified models, but they cannot be used for training, publication, or benchmark claims until promoted to a verified role.

## AZURE-001: Azure Scale-Out Preflight

Before any Azure compute is created or any Azure ML job is submitted, the run must record:

- active Azure user and subscription name
- subscription state is `Enabled`
- target account is `d.a.mordaunt@gmail.com` unless explicitly overridden
- Azure ML CLI extension status
- selected region
- GPU quota status or quota-request blocker
- cost policy: Spot/low-priority, `min_instances: 0`, `max_instances: 1` unless explicitly changed
- local artifact root on `/Volumes/PortableSSD`

Azure preflight is allowed to inspect account state. It must not create compute.

## PLATFORM-001: Lane Assignment

Every runnable model or benchmark track must declare exactly one primary platform lane:

- `mac-mlx`
- `mac-ollama`
- `mac-lmstudio`
- `azure-cuda`
- `hf-transformers`
- `retrieval`
- `specialist-runtime`

Secondary lanes are allowed only after the primary lane has a smoke result.

## FORMAT-001: Runtime And Training Format Ladder

Every model track must declare its primary format lane before training, benchmark, runtime proof, or publication work begins.

Required lane definitions live in:

```text
RUNTIME_FORMAT_LANES.yaml
```

The minimum required lanes are:

- `mlx-native`: Mac-local training/runtime for MLX checkpoints and adapters.
- `gguf-portability`: runtime and packaging for llama.cpp, LM Studio, and Ollama compatibility.
- `unsloth-cloud`: CUDA-backed Unsloth/TRL/PEFT training and distillation.
- `ktransformers-moe`: specialist sparse-MoE runtime or LoRA experiments.
- `liquid-leap-lfm`: Liquid/LFM-specific edge runtime and tuning paths.
- `recurrent-ssm-bitnet`: RWKV, Mamba/SSM, BitNet, and recursive/RLM research runtimes.
- `hosted-frontier-api`: API-only teacher/evaluator use.

GGUF artifacts must not be treated as training evidence. A GGUF proof can show that a model runs through a local endpoint, but it cannot prove that a fine-tune improved behavior.

Publication claims require:

- native training or adapter evidence where training occurred
- runtime proof in the claimed serving lane
- benchmark evidence in the claimed behavior lane
- storage proof that large artifacts and outputs stayed on `/Volumes/PortableSSD`

Hosted API outputs are teacher/evaluator evidence only unless the published claim is explicitly about hosted evaluation.

## ART-001: Adapter Output

Adapter directories must contain:

```text
adapters.safetensors
adapter_config.json
```

Adapters are local artifacts until benchmark promotion. They must not be committed to Git.

## BENCH-001: Benchmark Result Packet

Every promoted run must include:

- dataset audit
- train config
- trained token count
- loss/memory/runtime summary
- Hermes-local benchmark output
- standard benchmark status appropriate to gate
- promotion decision

## RUNTIME-001: Hermes Runtime Endpoint

Every runtime card must state:

- runtime: MLX, Ollama, LM Studio, or other
- model name
- command used
- endpoint URL
- tested prompt
- result
- limitations

## PUB-001: Publication Contract

GitHub publishes:

- code
- configs
- specs/plans
- benchmark definitions
- summary reports

Hugging Face publishes:

- dataset repos with dataset cards
- adapter repos with model cards
- benchmark artifacts when size/license-compatible

## HEALTH-001: Track Completion Contract

No Conductor track may be marked complete unless it includes:

- health target: `>= 9.5 / 10`
- current health estimate
- evidence supporting the estimate
- remaining gaps or explicit statement that no blocking gaps remain
- passing hub readiness validation
