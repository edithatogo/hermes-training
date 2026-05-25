# Qwen3 V4 Pilot Failure Analysis

Date: 2026-05-26

## Decision

Keep `qwen3-4b-strict-toolcall-v4-targeted` as the public/recommended adapter.
Do not promote any v5 variant.

The next adapter-improvement attempt, if run, should be treated as a v6
experiment with a stricter stop rule: held-out strict pass must remain `1.000`
and pilot polish must not be allowed to dilute strict tool-call behavior.

## Evidence Compared

| Candidate | Held-out strict | BFCL-style pilot | IFEval-style pilot | Coding pilot | Decision |
|---|---:|---:|---:|---:|---|
| V4 targeted | `1.000` | `0.667` | `0.667` | `1.000` | public/recommended narrow adapter |
| V5 strict-compatible | `0.875` | `1.000` | `0.667` | `1.000` | do not promote |
| V5 mixed draft | not promoted | `0.667` | `1.000` | `0.667` | superseded invalid ablation |

## Raw Evidence Roots

V4:

```text
/Volumes/PortableSSD/hermes-evals/standard-benchmarks/local-pilots/qwen3-4b-strict-toolcall-v4-targeted-local-bfcl-prefill-20260525
/Volumes/PortableSSD/hermes-evals/standard-benchmarks/local-pilots/qwen3-4b-strict-toolcall-v4-targeted-local-ifeval-prefill-20260525
```

V5 strict-compatible:

```text
/Volumes/PortableSSD/hermes-evals/standard-benchmarks/local-pilots/qwen3-4b-strict-toolcall-v5-pilot-polish-local-bfcl-prefill-20260525
/Volumes/PortableSSD/hermes-evals/standard-benchmarks/local-pilots/qwen3-4b-strict-toolcall-v5-pilot-polish-local-ifeval-prefill-20260525
```

V5 mixed draft:

```text
/Volumes/PortableSSD/hermes-evals/standard-benchmarks/local-pilots/qwen3-4b-strict-toolcall-v5-pilot-polish-final-local-bfcl-prefill-20260525
/Volumes/PortableSSD/hermes-evals/standard-benchmarks/local-pilots/qwen3-4b-strict-toolcall-v5-pilot-polish-final-local-ifeval-prefill-20260525
/Volumes/PortableSSD/hermes-evals/standard-benchmarks/local-pilots/qwen3-4b-strict-toolcall-v5-pilot-polish-final-local-coding-prefill-20260525
```

## Residual Failures

### V4 BFCL-Style Failure

Case: `bfcl-invalid-tool`

Expected behavior:

- include a refusal marker such as `cannot`
- exclude `<tool_call>`
- exclude the forbidden tool name `delete_customer_record`

V4 response:

```text
That action cannot be completed because no valid tool exists for calling delete_customer_record.
```

Failure reason:

```text
all_ok=True any_ok=True excludes_ok=False
```

Interpretation: V4 learned to refuse unsupported tools, but it echoed the
forbidden tool name. This is a refusal wording failure, not a tool-call parser
failure.

### V4 And V5 IFEval-Style Failure

Case: `ifeval-forbidden-word`

Expected behavior:

- include `runtime`
- include `smoke`
- include `passed`
- exclude `benchmark`

V4 and strict-compatible V5 response:

```text
The test ran successfully without errors.
```

Failure reason:

```text
all_ok=False any_ok=True excludes_ok=True
```

Interpretation: the model obeyed the forbidden-word constraint but missed the
required wording. This is an ordinary instruction-following wording failure
outside the strict tool-call contract.

### V5 Tradeoff

Strict-compatible V5 fixed `bfcl-invalid-tool`:

```text
I cannot perform that action because no listed tool is available for deleting customer records.
```

That changed BFCL-style pilot pass from `0.667` to `1.000`, but held-out strict
tool-call pass regressed from V4's `1.000` to `0.875`. The tradeoff is not
acceptable for the public adapter.

The superseded mixed-draft V5 reached IFEval-style `1.000`, but it included
ordinary instruction-following rows that were later rejected by the strict data
contract and it regressed coding to `0.667`.

## V6 Guardrails

Any future v6 attempt should:

1. Start from V4, not V5.
2. Add only strict-compatible examples unless the project explicitly creates a
   separate general-instruction adapter.
3. Avoid ordinary free-form instruction rows in the strict tool-call LoRA.
4. Add narrow refusal variants that do not echo unavailable tool names.
5. Treat the IFEval wording failure as either a prompt-profile/runtime issue or
   a separate general-instruction lane, not as a reason to contaminate the
   strict tool-call dataset.
6. Run the held-out strict suite after every checkpoint and stop immediately if
   pass rate drops below `1.000`.
7. Keep V4 public until a candidate matches V4 held-out strict quality and
   improves pilots without regressions.

## Recommended Next Experiment

If another local training pass is worthwhile, use a micro-ablation:

- add 4 to 8 unsupported-tool refusal rows
- keep all rows in strict chat/tool-call format
- do not add IFEval free-form wording rows
- evaluate at multiple checkpoints before finalizing

Promotion threshold:

| Gate | Required |
|---|---:|
| Held-out strict local tool-call | `1.000` |
| Mirrored regression | `1.000` |
| BFCL-style pilot | `1.000` |
| IFEval-style pilot | no regression below V4 unless explicitly out of scope |
| Coding sanity pilot | `1.000` |

## Boundary

This report is analysis and planning only. It does not train, publish, or
promote a new adapter.
