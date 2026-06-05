"""Threshold grid helpers for the counterpoint threshold-frontier probe."""

from __future__ import annotations

from decimal import ROUND_HALF_UP, Decimal, InvalidOperation


def parse_threshold_values(value: str | tuple[float, ...] | list[float]) -> tuple[float, ...]:
    if isinstance(value, str):
        parts = [item.strip() for item in value.split(",") if item.strip()]
        if not parts:
            raise ValueError("threshold grid must contain at least one value")
        try:
            values = tuple(float(Decimal(part)) for part in parts)
        except (InvalidOperation, ValueError) as exc:
            raise ValueError(f"malformed threshold value in {value!r}") from exc
        return normalize_threshold_values(values)
    return normalize_threshold_values(tuple(float(item) for item in value))


def normalize_threshold_values(values: tuple[float, ...]) -> tuple[float, ...]:
    if not values:
        raise ValueError("threshold grid must contain at least one value")
    if len(set(values)) != len(values):
        raise ValueError("threshold grid values must be unique")
    if tuple(sorted(values)) != values:
        raise ValueError("threshold grid values must be sorted ascending")
    return values


def threshold_label(value: float) -> str:
    scaled = (Decimal(str(value)) * Decimal("1000")).quantize(
        Decimal("1"),
        rounding=ROUND_HALF_UP,
    )
    return f"r{int(scaled):06d}"
