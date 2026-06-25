# Qwen3 v4 BFCL Text-Prefix Bridge HF Artifact

- Repo: `edithatogo/hermes-training-artifacts`
- Path prefix: `qwen3-v4-bfcl-text-prefix-bridge-30-20260625/`
- Clean revision: `807d4ce396208313cfe244ecd785054445092a49`
- URL: `https://huggingface.co/datasets/edithatogo/hermes-training-artifacts/tree/807d4ce396208313cfe244ecd785054445092a49/qwen3-v4-bfcl-text-prefix-bridge-30-20260625`

The artifact contains the scored 30-case BFCL text-prefix bridge smoke, raw BFCL result JSONL files, score JSON/CSV files, the run-id file, and the updated official candidate matrix.

Upload note: commit `5fab1aa2f314574bc46d2848ce25af1120f11540` uploaded the bundle. Cleanup commit `807d4ce396208313cfe244ecd785054445092a49` removed accidental BFCL project-root `.file_locks` from the artifact prefix.

## Scores

| Metric | Score |
|---|---:|
| Overall Acc | 0.0033 |
| Non-Live Overall Acc | 0.0333 |
| simple_python AST | 0.100 |
| multiple AST | 0.100 |
| parallel AST | 0.000 |

## Boundary

Evidence-only private artifact. This is a selected 30-case BFCL repair smoke, not a full BFCL leaderboard score, not a passing Hermes tool-call claim, and not a model publication gate pass.
