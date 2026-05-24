# mem0 Runtime Targets

mem0 runtime work has two independent paths:

- extraction and summarization models use chat/completions-style LLM endpoints.
- embedding and retriever models use embedding, reranking, or retrieval APIs.

Do not require one runtime to cover every role. The acceptance rule is that every candidate exposes a stable local API that mem0 or a thin adapter can call, and that the result is benchmarked against the current default.

## Runtime Matrix

| Runtime | Good fit | Endpoint shape | Mac / Metal notes |
|---|---|---|---|
| Ollama | current embedder and extractor, GGUF chat models | `/api/embeddings`, OpenAI-compatible `/v1/chat/completions` | Best daily default. Uses SSD-backed model store on this machine. |
| llama.cpp | GGUF chat models, some embedding models, server smoke | `llama-server` OpenAI-compatible endpoints where supported | Build with Metal on Apple Silicon; record commit and flags in run card. |
| LM Studio | GGUF chat and embedding models exposed through UI/server | OpenAI-compatible local server | Good desktop validation path. Requires active app/server or `lms` CLI. |
| MLX / MLX-LM | Mac-first models and adapters | `mlx_lm.server` for chat; custom embedding wrappers where needed | Preferred for Apple Silicon fine-tune and adapter smoke. |
| Transformers / sentence-transformers | embedding/reranker baselines | Python harness or small local service | Use when Ollama/llama.cpp do not expose embedding support for the candidate. |
| FAISS + SQLite | retriever experiments | local Python API or `POST /retrieve` service | Good for dense retrieval experiments. Keep separate from Qdrant collections. |
| ColBERT-style index | late-interaction retrieval | `POST /retrieve` service | Requires separate index artifacts and cannot be treated as plain dense Qdrant. |

## Endpoint Contracts

### Extractor

Extractor candidates must support:

- deterministic temperature `0` or near-zero operation
- compact memory JSON or text output
- refusal to store secrets or prompt-injection payloads
- low enough latency for interactive CLI use

### Embedder

Embedder candidates must record:

- model id and revision
- vector dimension
- normalization policy
- batching support
- collection name
- index distance metric
- add/search latency

### Retriever

Retriever candidates must expose:

```http
GET /health
POST /retrieve
```

`POST /retrieve` should return:

```json
{
  "results": [
    {
      "doc_id": "string",
      "chunk_id": "string",
      "source_id": "string",
      "score": 0.0,
      "citation": "string",
      "index_id": "string",
      "model_id": "string"
    }
  ]
}
```

## Metal-Specific Rules

- Prefer MLX for Apple Silicon adapter experiments when model support exists.
- Prefer llama.cpp Metal builds for GGUF runtime proof.
- Record whether the runtime used CPU, Metal GPU layers, MLX, or MPS.
- Keep first tests at small context lengths before trying long-context memory scenarios.
- Do not assume a model is usable for mem0 just because it loads; run add/search and recency tests.

