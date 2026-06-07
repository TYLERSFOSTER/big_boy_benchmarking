"""Target-policy helpers for PlateSupport gauntlet Stage 6."""

from __future__ import annotations

CLAIM_BOUNDARY = (
    "bounded paired smoke comparison under the Stage 5 target and budget; "
    "not a general tower-performance claim"
)


def target_hit(row: dict[str, object], target: dict[str, object]) -> bool:
    """Evaluate the Stage 5 target policy on one episode row."""

    target_type = str(target.get("target_type", ""))
    if target_type == "binary_success":
        return _truthy(row.get("goal_reached", False))
    if target_type == "return_threshold":
        threshold = float(target["threshold_value"])
        return float(row.get("total_reward", 0.0)) >= threshold
    if target_type == "first_hit":
        return _truthy(row.get("goal_reached", False))
    raise ValueError(f"unsupported Stage 6 target type: {target_type!r}")


def _truthy(value: object) -> bool:
    if isinstance(value, bool):
        return value
    return str(value).strip().lower() in {"1", "true", "yes", "y"}
