# Spec: mem0 Hermes Runtime Tool

## Goal

Expose the guarded mem0 read path as an explicit Hermes-agent tool contract
without editing the dirty/behind Hermes-agent checkout or changing mem0
defaults.

## Requirements

- Provide a stable command wrapper around `scripts/mem0_read.py`.
- Accept either `--query` or stdin JSON so Hermes-agent/plugin adapters can call
  it directly.
- Keep the tool read-only and report that it does not mutate mem0 config.
- Default to `close-margin` with an opt-in cache TTL for repeated reads.
- Keep `vector` as rollback and `qwen3` as explicit experimental mode.
- Document the manifest and command contract.
- Validate with unit tests and a live read smoke.

## Non-Goals

- Do not edit `/Volumes/PortableSSD/GitHub/hermes-agent` in this track.
- Do not wire the tool as an automatic every-turn prelude.
- Do not publish or alter the Hugging Face dataset.
- Do not promote Qwen3 reranking as the default live mem0 path.
