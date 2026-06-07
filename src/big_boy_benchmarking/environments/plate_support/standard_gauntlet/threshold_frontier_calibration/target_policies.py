"""Target policy vocabulary for PlateSupport Stage 5 calibration."""

from __future__ import annotations

BINARY_SUCCESS_TARGET_POLICY_ID = "plate_support_binary_goal_success_v001"
FIRST_HIT_TARGET_POLICY_ID = "plate_support_first_hit_v001"
RETURN_THRESHOLD_TARGET_POLICY_ID = "plate_support_return_threshold_v001"

CLAIM_BOUNDARY = "threshold calibration evidence only; no tower-vs-flat comparison claim"


def sustained_hit_target_policy_id(required_count: int, window_length: int) -> str:
    """Return a stable policy id for a K-of-W sustained-hit rule."""

    return f"plate_support_sustained_hit_{required_count}_of_{window_length}_v001"
