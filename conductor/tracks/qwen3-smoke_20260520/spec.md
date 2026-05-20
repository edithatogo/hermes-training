# Specification: Qwen3 4B Smoke Training

## Overview

Validate `Qwen/Qwen3-4B-MLX-4bit` as the next practical local fine-tune target after LFM2.5.

## Requirements

- Use authenticated or pre-fetched Hugging Face download to avoid the previous unauthenticated stall.
- Keep model cache and temp files on the SSD.
- Run the existing Qwen3 4B smoke config.
- Fix only track-local issues discovered by the smoke run.
- Record result and blockers.

## Acceptance Criteria

- Model loads from SSD cache.
- Smoke training reaches adapter save.
- Run note documents trained tokens, memory, loss, and next decision.

## Out of Scope

- Qwen3.6/Gemma4 MoE local fine-tuning.
- Publishing Qwen adapter.
