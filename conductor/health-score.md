# Project Health Score

## Target

Every active track should be shaped to reach **health >= 9.5 / 10** before it is marked complete or used for publication.

## Scoring Rubric

| Dimension | Weight | Requirement for Full Credit |
|---|---:|---|
| Conductor completeness | 1.0 | Product, tech stack, workflow, requirements, design, contracts, tracks, specs, and plans exist and are linked |
| SSD/storage safety | 1.0 | Caches, temp files, model downloads, benchmark outputs, and exports resolve to SSD-backed paths |
| Reproducibility | 1.0 | Commands, configs, dataset audit, run cards, and exact model IDs are recorded |
| Training correctness | 1.0 | Dry runs and smoke/full-smoke runs complete with adapters saved and artifacts ignored |
| Benchmark quality | 1.5 | Hermes-local and standard benchmark gates are defined and executed for the track stage |
| Runtime validation | 1.0 | MLX/Ollama/LM Studio/Hermes paths are tested as applicable and documented |
| Publication readiness | 1.0 | GitHub/Hugging Face model/dataset cards and license notes are ready before publication |
| Maintainability | 1.0 | Validation scripts pass, plans are current, and nested repo state is understandable |
| Evidence quality | 1.5 | Results distinguish pipeline proof from quality proof, with raw outputs or reports retained appropriately |

## Minimum Completion Rule

A track cannot be marked complete unless:

- estimated health is at least 9.5
- `scripts/validate_readiness.py` passes from the hub
- the track plan contains a completed health checkpoint
- any score below full credit is documented with an explicit reason and next action

## Health Check Template

```markdown
## Health Check

- Target: >= 9.5 / 10
- Current estimate:
- Evidence:
- Gaps:
- Decision:
```
