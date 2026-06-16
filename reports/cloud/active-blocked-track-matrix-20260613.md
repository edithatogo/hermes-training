# Active Blocked Track Matrix

Registry: `conductor/tracks.md`
Unblock checklist: `reports/cloud/backend-unblock-checklist-20260613.json`

| Track | Backend | Backend status | Blocker | Next unchecked task |
|---|---|---|---|---|
| `qwen3-v4-peft-lightning-scorecard_20260614` | `lightning` | `blocked-needs-teamspace-owner` | Lightning SDK is installed, but Studio/Job commands need login and a configured Teamspace owner. | Run Lightning login and identify a real Teamspace only after explicit user approval. |
| `qwen3-v4-peft-ngc-cloud-function-scorecard_20260613` | `ngc` | `blocked` | NGC has no configured API key, SSO session, org/team, GPU quota, or benchmark container. | Configure NGC auth only after the user supplies keys or completes SSO. |

## Commands

### qwen3-v4-peft-lightning-scorecard_20260614

```bash
lightning login
lightning studio list
lightning machine list
lightning job list
./.venv/bin/python scripts/submit_lightning_peft_scorecard.py
./.venv/bin/python scripts/submit_lightning_peft_scorecard.py --teamspace <owner>/<teamspace> --execute --confirm-lightning-run --confirm-zero-cost-compute
```

### qwen3-v4-peft-ngc-cloud-function-scorecard_20260613

```bash
ngc sso login
ngc config current
ngc cloud-function gpu quota
ngc cloud-function task create --help
./.venv/bin/python scripts/submit_ngc_cloud_function_scorecard.py
./.venv/bin/python scripts/submit_ngc_cloud_function_scorecard.py --container-image <ngc-registry-image> --gpu-specification <gpu-spec> --execute --confirm-ngc-run
```
