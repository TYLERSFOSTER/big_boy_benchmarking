"""Arm manifests for the Warehouse masked direct/live-lift tower diagnostic."""

from __future__ import annotations

from big_boy_benchmarking.environments.warehouse_gridlock.masked_direct_vs_live_lift_tower.config import (
    CONTROLLER_POLICY_ID,
    DIRECT_ARM_ID,
    DIRECT_CANDIDATE_POLICY_ID,
    DIRECT_MASK_POLICY_ID,
    LIVE_LIFT_POLICY_ID,
    NO_LOOKAHEAD_POLICY_ID,
    TOWER_ARM_ID,
    TOWER_CANDIDATE_POLICY_ID,
    TOWER_MASK_POLICY_ID,
)


def arm_manifest_rows() -> list[dict[str, object]]:
    return [
        {
            "arm_id": DIRECT_ARM_ID,
            "arm_type": "direct_concrete",
            "candidate_generation_policy_id": DIRECT_CANDIDATE_POLICY_ID,
            "mask_policy_id": DIRECT_MASK_POLICY_ID,
            "live_lift_policy_id": "not_applicable",
            "controller_policy_id": CONTROLLER_POLICY_ID,
            "immediate_admissibility_mask": True,
            "one_step_successor_lookahead": False,
            "successor_out_used_for_selection": False,
            "claim_boundary": "direct baseline over generated admissible candidate set",
        },
        {
            "arm_id": TOWER_ARM_ID,
            "arm_type": "tower_scoped_generated_surface",
            "candidate_generation_policy_id": TOWER_CANDIDATE_POLICY_ID,
            "mask_policy_id": TOWER_MASK_POLICY_ID,
            "live_lift_policy_id": LIVE_LIFT_POLICY_ID,
            "controller_policy_id": CONTROLLER_POLICY_ID,
            "immediate_admissibility_mask": True,
            "one_step_successor_lookahead": False,
            "successor_out_used_for_selection": False,
            "claim_boundary": "tower arm over scoped generated surface with live state-lift hygiene",
        },
    ]


def no_lookahead_policy_manifest() -> dict[str, object]:
    return {
        "policy_id": NO_LOOKAHEAD_POLICY_ID,
        "successor_out_may_be_recorded_after_selection": True,
        "successor_out_used_for_selection": False,
        "forbidden_selection_signals": [
            "successor_out_count",
            "successor_is_culdesac",
            "successor_deadness",
            "one_step_nonself_filter",
        ],
    }
