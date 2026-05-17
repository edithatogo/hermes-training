# Design — Hermes Training Hub Architecture

> **Status:** Active
> **Version:** 1.0
> **See also:** `REQUIREMENTS.md` for MoSCoW, `CONTRACTS.md` for interface contracts

---

## 1. Pipeline Architecture

```mermaid
flowchart LR
    subgraph Data["Data Layer (SSD)"]
        HF[(HuggingFace Hub)]
        RAW[data/raw/*.jsonl]
        SPLITS[data/splits/*.jsonl]
    end

    subgraph Cache["Model Cache (SSD)"]
        CACHE[(HF_HUB_CACHE)]
    end

    subgraph Training["Training (MLX on M1 Max)"]
        BASE[Base Model]
        LORA[LoRA Adapter]
        TRAIN[MLX LoRA Train]
        MERGE[Merge Adapter]
    end

    subgraph Eval["Evaluation"]
        PROMPTS[eval/prompts.jsonl]
        EVAL[evaluate.py]
        COMPARE[compare.py]
        REPORT[HTML Report]
    end

    subgraph Export["Export Pipeline"]
        GGUF[convert_hf_to_gguf.py]
        QUANT[llama-quantize]
        OLLAMA[ollama create]
    end

    subgraph Publish["Publishing"]
        GH[GitHub]
        HF_PUB[HuggingFace Hub]
    end

    HF -->|download| RAW
    RAW -->|build_dataset.py| SPLITS
    CACHE -->|mlx_lm.load| BASE
    SPLITS -->|train.py| TRAIN
    BASE --> TRAIN
    TRAIN --> LORA
    LORA --> EVAL
    BASE --> EVAL
    PROMPTS --> EVAL
    EVAL --> REPORT
    REPORT -->|compare.py| COMPARE
    LORA --> MERGE
    BASE --> MERGE
    MERGE --> GGUF
    GGUF --> QUANT
    QUANT --> OLLAMA
    OLLAMA -->|ollama list| GH
    LORA -->|push_to_hf.sh| HF_PUB
    SPLITS -->|push_to_hf.sh| HF_PUB
```

## 2. Repository Dependency Graph

```mermaid
flowchart TD
    subgraph Hub["hermes-training/ (Hub)"]
        CONDUCTOR[CONDUCTOR.md]
        REQS[REQUIREMENTS.md]
        DESIGN[DESIGN.md]
        CONTRACTS[CONTRACTS.md]
    end

    subgraph G4["gemma4/"]
        G4_SCRIPT[scripts/train.py]
        G4_DATA[data/splits/]
        G4_ADAPTER[experiments/gemma4-e4b/]
    end

    subgraph L2["lfm2/"]
        L2_SCRIPT[scripts/train.py]
        L2_DATA[data/splits/]
        L2_ADAPTER[experiments/lfm2-8b-a1b/]
    end

    subgraph OP["ollama-pack/"]
        OP_MODEL[modelfiles/]
        OP_EXPORT[scripts/export_ollama.sh]
    end

    Hub -->|references| G4
    Hub -->|references| L2
    Hub -->|references| OP
    G4_ADAPTER -->|export_ollama.sh| OP_EXPORT
    L2_ADAPTER -->|export_ollama.sh| OP_EXPORT
    OP_MODEL -.->|Modelfile template| OP_EXPORT

    style Hub fill:#e1f5fe,stroke:#0288d1
    style G4 fill:#fff3e0,stroke:#f57c00
    style L2 fill:#f3e5f5,stroke:#7b1fa2
    style OP fill:#e8f5e9,stroke:#388e3c
```

## 3. Training Data Flow

```mermaid
sequenceDiagram
    participant HF as HuggingFace Hub
    participant DL as download_hermes_dataset.py
    participant RAW as data/raw/
    participant BD as build_dataset.py
    participant SPLITS as data/splits/
    participant TR as train.py

    HF->>DL: Stream Hermes-3-Dataset
    HF->>DL: Stream hermes-function-calling-v1
    DL->>RAW: Write JSONL (messages format)
    
    RAW->>BD: Read raw conversations
    BD->>BD: Validate schema
    BD->>BD: Deduplicate (SHA256 hash)
    BD->>BD: Filter (2-100 turns)
    BD->>BD: Shuffle + split (80/10/10)
    BD->>SPLITS: Write train.jsonl
    BD->>SPLITS: Write val.jsonl
    BD->>SPLITS: Write test.jsonl

    SPLITS->>TR: Load training split
    HF->>TR: Load base model (MLX)
    TR->>TR: Apply LoRA adapters
    TR->>TR: Train for N iterations
    TR->>TR: Save adapter weights
```

## 4. Deployment Flow

```mermaid
sequenceDiagram
    participant TR as train.py
    participant AD as experiments/*/lora_adapter/
    participant EXP as export_ollama.sh
    participant LC as llama.cpp
    participant OL as Ollama
    participant HX as Hermes Agent

    TR->>AD: Write adapters.safetensors
    TR->>AD: Write adapter_config.json
    
    EXP->>AD: Read adapter
    EXP->>AD: Read base model
    EXP->>LC: mlx_lm.fuse (merge adapter)
    LC->>LC: convert_hf_to_gguf.py (→ .gguf)
    LC->>LC: quantize (→ q4_k_m)
    LC->>EXP: Return GGUF file
    
    EXP->>OL: ollama create -f Modelfile
    OL->>OL: ollama run (smoke test)
    
    HX->>OL: Switch model in Hermes picker
    OL->>HX: Serve inference requests
```

## 5. Component Architecture

```mermaid
flowchart TB
    subgraph Core["Core Pipeline"]
        direction TB
        A[build_dataset.py] --> B[train.py]
        B --> C[evaluate.py]
        B --> D[export_ollama.sh]
    end

    subgraph Support["Support Scripts"]
        E[download_hermes_dataset.py]
        F[bakeoff.py]
        G[compare.py]
        H[push_to_hf.sh]
    end

    subgraph Config["Configuration"]
        I[train_config.yaml]
        J[Modelfile]
    end

    E --> A
    F -.->|informs model choice| B
    C --> G
    D --> J
    B --> I
    H -->|uploads| HF[(HuggingFace)]
    D --> O[(Ollama)]
```

## 6. File Relationship Map

```mermaid
flowchart LR
    CONFIG[train_config.yaml] -->|parameters| TRAIN[train.py]
    RAW[data/raw/*.jsonl] -->|input| BUILD[build_dataset.py]
    BUILD -->|output| SPLITS[data/splits/*.jsonl]
    SPLITS -->|training data| TRAIN
    HF_MODEL[Base model (HF)] -->|mlx_lm.load| TRAIN
    TRAIN -->|produces| ADAPTER[experiments/*/lora_adapter/]
    ADAPTER -->|input| EVAL[evaluate.py]
    PROMPTS[eval/prompts.jsonl] --> EVAL
    EVAL -->|output| RESULTS[eval/results.jsonl]
    EVAL -->|generates| REPORT[eval/report.html]
    ADAPTER -->|input| COMPARE[compare.py]
    COMPARE -->|generates| COMP_HTML[eval/comparison.html]
    ADAPTER -->|input| EXPORT[export_ollama.sh]
    EXPORT -->|converts| GGUF[*.gguf]
    GGUF -->|ollama create| OLLAMA_MODEL[Ollama model]
    ADAPTER -->|input| PUSH[push_to_hf.sh]
    PUSH -->|uploads| HF[HuggingFace]
```

## 7. State Machine

```mermaid
stateDiagram-v2
    [*] --> Scaffolded: repo created
    Scaffolded --> Downloading: start download
    Downloading --> Cached: model/data on SSD
    Cached --> Training: run train.py
    Training --> Trained: adapter saved
    Trained --> Evaluating: run evaluate.py
    Evaluating --> Evaluated: results saved
    Evaluated --> Exporting: run export_ollama.sh
    Exporting --> Deployed: ollama create
    Deployed --> Published: push_to_hf.sh
    Published --> [*]

    Training --> Failed: error
    Failed --> Training: fix + retry
    Downloading --> Failed: disk full / timeout
```

## 8. Hardware Resource Budget

```mermaid
pie title M1 Max 32GB Memory Budget
    "Base Model (4B E4B)" : 8
    "LoRA Adapter" : 2
    "Tokenized Data" : 4
    "OS + Other Apps" : 10
    "Headroom" : 8
```

| Resource | Available | Allocated | Notes |
|----------|-----------|-----------|-------|
| RAM | 32 GB | ~8 GB model + ~4 GB data | 4B MoE fits comfortably |
| Disk (SSD) | 743 GB | ~50 GB for models + datasets | Ample space for 5+ models |
| Disk (internal) | 13 GB free | ~1 GB for code | Code repos are small |
| CPU cores | 10 (8P+2E) | 4 for training | MLX uses ANE + GPU primarily |
| GPU cores | 24 | 24 | MLX uses Metal GPU |
