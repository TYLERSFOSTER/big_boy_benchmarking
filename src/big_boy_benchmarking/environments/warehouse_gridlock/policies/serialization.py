"""Stable serialization helpers for Warehouse Gridlock policy artifacts."""

from __future__ import annotations

import hashlib
import json
from collections.abc import Mapping
from typing import Any


def stable_json(payload: Any) -> str:
    return json.dumps(payload, sort_keys=True, separators=(",", ":"), ensure_ascii=True)


def stable_hash(payload: Any) -> str:
    return hashlib.sha256(stable_json(payload).encode("utf-8")).hexdigest()


def stable_short_hash(payload: Any, *, length: int = 16) -> str:
    return stable_hash(payload)[:length]


def sorted_float_mapping(mapping: Mapping[str, float]) -> dict[str, float]:
    return {str(key): float(mapping[key]) for key in sorted(mapping)}


def policy_state_hash(*, weights: Mapping[str, float], baseline: float, update_count: int) -> str:
    return stable_hash(
        {
            "weights": sorted_float_mapping(weights),
            "baseline": float(baseline),
            "update_count": int(update_count),
        }
    )


def feature_key(*parts: object) -> str:
    return "::".join(str(part) for part in parts)
