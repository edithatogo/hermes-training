# mem0 Data

mem0 data is retrieval and memory data, not chat SFT data.

Use contrastive examples for embedding and retriever tuning:

```json
{
  "id": "string",
  "anchor": "query or memory lookup need",
  "positive": "memory text that should be retrieved",
  "negatives": ["similar but wrong memory text"],
  "category": "direct_recall | recency_conflict | distractor_resistance | tool_state_recall",
  "metadata": {
    "source": "string",
    "license": "string"
  }
}
```

The initial seed file is `contrastive_seed.jsonl`. It is tiny and exists to lock the schema, not to train a useful model by itself.

## Rules

- Do not include private user memory in publishable datasets.
- Keep recency examples explicit: the positive should represent the current fact or preference.
- Keep distractors semantically close enough to test ranking.
- Do not mix chat assistant target text into embedding triplets.
- Larger generated or private corpora should stay out of Git and be summarized by digest/run card.

