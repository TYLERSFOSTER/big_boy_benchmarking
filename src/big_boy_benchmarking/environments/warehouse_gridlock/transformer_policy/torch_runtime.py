"""Optional Torch runtime helpers for Warehouse transformer policy code."""

from __future__ import annotations

from dataclasses import dataclass
from importlib.util import find_spec
from typing import Any


class TorchUnavailableError(RuntimeError):
    """Raised when a transformer command needs Torch but Torch is not installed."""


@dataclass(frozen=True)
class TorchRuntimeInfo:
    available: bool
    version: str | None
    cuda_available: bool
    selected_device: str

    def to_manifest(self) -> dict[str, object]:
        return {
            "torch_available": self.available,
            "torch_version": self.version,
            "cuda_available": self.cuda_available,
            "selected_device": self.selected_device,
        }


def torch_is_available() -> bool:
    return find_spec("torch") is not None


def require_torch() -> Any:
    if not torch_is_available():
        raise TorchUnavailableError(
            "Torch is required for warehouse-gridlock transformer-policy commands. "
            "Install the optional ML dependency surface for this repository."
        )
    import torch  # type: ignore[import-not-found]

    return torch


def runtime_info(*, requested_device: str = "cpu") -> TorchRuntimeInfo:
    if not torch_is_available():
        return TorchRuntimeInfo(
            available=False,
            version=None,
            cuda_available=False,
            selected_device=requested_device,
        )
    torch = require_torch()
    cuda_available = bool(torch.cuda.is_available())
    selected = requested_device
    if requested_device == "cuda" and not cuda_available:
        selected = "cpu"
    return TorchRuntimeInfo(
        available=True,
        version=str(torch.__version__),
        cuda_available=cuda_available,
        selected_device=selected,
    )

