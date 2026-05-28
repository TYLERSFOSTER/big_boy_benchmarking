"""Readout call counters for diagnostics and tests."""

from __future__ import annotations

from collections.abc import Callable
from dataclasses import dataclass
from typing import Any


@dataclass
class ReadoutCallCounter:
    compatibility_calls: int = 0
    morphism_calls: int = 0

    def wrap_compatibility(self, method: Callable[..., Any]) -> Callable[..., Any]:
        def wrapped(*args: Any, **kwargs: Any) -> Any:
            self.compatibility_calls += 1
            return method(*args, **kwargs)

        return wrapped

    def wrap_morphism(self, method: Callable[..., Any]) -> Callable[..., Any]:
        def wrapped(*args: Any, **kwargs: Any) -> Any:
            self.morphism_calls += 1
            return method(*args, **kwargs)

        return wrapped
