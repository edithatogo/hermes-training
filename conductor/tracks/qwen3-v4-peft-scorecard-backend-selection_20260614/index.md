# Track qwen3-v4-peft-scorecard-backend-selection_20260614 Context

- [Specification](./spec.md)
- [Implementation Plan](./plan.md)
- [Metadata](./metadata.json)
- [Hub Requirements](../../requirements.md)
- [Hub Design](../../design.md)
- [Hub Contracts](../../contracts.md)

## Summary

The scorecard offload lanes now have a generated backend-selection report:
`reports/cloud/qwen3-v4-peft-scorecard-backend-selection-20260614.md`.

It ranks Kaggle as the next prepared route because the public-input contract,
quota evidence, and result-ingest gate are ready. It remains fail-closed:
`execute=false`, `promotion_allowed=false`, and explicit run approval plus
cost/zero-cost policy and artifact recovery gates remain required.
