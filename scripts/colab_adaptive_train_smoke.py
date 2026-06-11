#!/usr/bin/env python3
"""Tiny Colab training smoke that adapts to CUDA, TPU/XLA, or CPU."""
from __future__ import annotations

import json
import platform
import sys
import time
from datetime import UTC, datetime
from pathlib import Path
from typing import Any


def select_device() -> dict[str, Any]:
    import torch

    if torch.cuda.is_available():
        return {
            "backend": "cuda",
            "device": torch.device("cuda"),
            "device_name": torch.cuda.get_device_name(0),
            "torch_xla": None,
        }
    try:
        import torch_xla.core.xla_model as xm  # type: ignore[import-not-found]
    except Exception as exc:  # noqa: BLE001
        return {
            "backend": "cpu",
            "device": torch.device("cpu"),
            "device_name": "cpu",
            "torch_xla_error": f"{type(exc).__name__}: {exc}",
            "torch_xla": None,
        }
    return {
        "backend": "xla",
        "device": xm.xla_device(),
        "device_name": "xla:0",
        "torch_xla": xm,
    }


def train(steps: int, batch_size: int) -> dict[str, Any]:
    import torch

    selected = select_device()
    device = selected["device"]
    xm = selected.get("torch_xla")
    torch.manual_seed(17)

    model = torch.nn.Sequential(torch.nn.Linear(16, 32), torch.nn.ReLU(), torch.nn.Linear(32, 4)).to(device)
    optimizer = torch.optim.AdamW(model.parameters(), lr=0.01)
    losses: list[float] = []
    started = time.time()

    for _ in range(steps):
        features = torch.randn(batch_size, 16, device=device)
        labels = torch.randint(0, 4, (batch_size,), device=device)
        logits = model(features)
        loss = torch.nn.functional.cross_entropy(logits, labels)
        optimizer.zero_grad(set_to_none=True)
        loss.backward()
        if selected["backend"] == "xla" and xm is not None:
            xm.optimizer_step(optimizer)
            xm.mark_step()
        else:
            optimizer.step()
        losses.append(float(loss.detach().cpu().item()))

    return {
        "backend": selected["backend"],
        "device_name": selected["device_name"],
        "steps": steps,
        "batch_size": batch_size,
        "initial_loss": losses[0] if losses else None,
        "final_loss": losses[-1] if losses else None,
        "duration_s": time.time() - started,
        "losses": losses,
        "torch_version": torch.__version__,
        "torch_xla_error": selected.get("torch_xla_error", ""),
    }


def main() -> int:
    steps = int(sys.argv[1]) if len(sys.argv) > 1 else 8
    batch_size = int(sys.argv[2]) if len(sys.argv) > 2 else 16
    result = {
        "created_at": datetime.now(UTC).isoformat(),
        "argv": sys.argv,
        "cwd": str(Path.cwd()),
        "python": sys.version,
        "platform": platform.platform(),
        "training": train(steps=steps, batch_size=batch_size),
    }
    print(json.dumps(result, indent=2, ensure_ascii=False))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
