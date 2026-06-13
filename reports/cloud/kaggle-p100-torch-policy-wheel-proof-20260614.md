# Kaggle P100 Torch Policy Wheel Proof

Status: `pass`

Policy: `p100-cu118`

Index: `https://download.pytorch.org/whl/cu118`

## Verified Wheels

| Package | Wheel | Result |
|---|---|---|
| `torch` | `torch-2.2.2+cu118-cp312-cp312-linux_x86_64.whl` | `present` |
| `torchvision` | `torchvision-0.17.2+cu118-cp312-cp312-linux_x86_64.whl` | `present` |
| `torchaudio` | `torchaudio-2.2.2+cu118-cp312-cp312-linux_x86_64.whl` | `present` |

## Boundary

This proves the pinned CPython 3.12 Linux CUDA 11.8 wheels exist. It does not
prove Kaggle runtime scoring or P100 execution until a rerun completes.

The bulk download probe was cancelled after a partial `torch` download
(`289.1 MB / 819.1 MB`) because index proof was sufficient and the full download
was slow.
