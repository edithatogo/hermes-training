# Specification: MiniCPM5 1B GGUF Endpoint Repair Completion

## Overview

Close the endpoint-gated prompt/profile repair rows for
`openbmb/MiniCPM5-1B-GGUF`.

## Scope

- Run the cached GGUF through `llama-server` on Metal.
- Execute the queued strict suffix and MiniCPM empty-tag prompt variants.
- Record source summaries, tracked reports, and non-promotional ledger rows.

## Decision

The best variant scored `1/3`, passing only the unavailable-tool refusal. Raw
strict-output promotion remains blocked.
