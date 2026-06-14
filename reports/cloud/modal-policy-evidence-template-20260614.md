# Modal Policy Evidence Template

Copy the JSON template to `reports/cloud/modal-policy-evidence-20260614.json`
only after the Modal workspace has confirmed free credit, an academic grant, or
explicit paid-compute approval.

Do not include tokens, payment details, private account identifiers, or
screenshots with secrets. The validator only needs a non-secret summary plus a
bounded GPU-hour/spend allowance.

Valid `evidence_type` values:

- `free_credit`
- `academic_grant`
- `explicit_paid_compute_approval`

The Modal scorecard still requires explicit run approval after this evidence
gate passes. Benchmark promotion remains blocked until result ingest passes.
