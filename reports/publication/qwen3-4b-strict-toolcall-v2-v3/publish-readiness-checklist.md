# Publish Readiness: Qwen3 4B Strict Tool-Call V2/V3

Status: BLOCKED

## Gates

- [x] Structural readiness checks exist.
- [x] Dataset token audits recorded.
- [x] Mirrored and held-out benchmark outputs recorded on SSD.
- [x] Strict scoring kept unchanged.
- [x] Publication decision documented.
- [ ] Held-out strict local tool-call suite passes at `1.000`.
- [ ] Base-vs-adapter standardized benchmarks complete.
- [ ] License and redistribution review complete for adapter publishing.
- [ ] Runtime card passes MLX plus at least one endpoint path.

## Blocker

Both V2 and V3 failed the held-out strict publication gate:

- V2 held-out strict pass: `0.250`
- V3 held-out strict pass: `0.250`

The V3 diagnostic empty-think-stripped score improved to `0.875`, but diagnostic normalization is not a substitute for the strict benchmark gate.
