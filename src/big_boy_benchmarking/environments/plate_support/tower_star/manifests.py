"""Manifest helpers for the PlateSupport tower-star diagnostic."""

from __future__ import annotations

from dataclasses import dataclass

from .config import (
    CURRENT_LIFT_EXECUTABLE_GUARD,
    DIRECT_INVALID_GUARD_ARM_ID,
    DIRECT_NONSELF_GUARD_ARM_ID,
    DIRECT_RAW_ARM_ID,
    INVALID_GUARD,
    NONSELF_GUARD,
    ORACLE_ONE_STEP_INFORMATION_MODE,
    RAW_GUARD,
    TOWER_INVALID_GUARD_ARM_ID,
    TOWER_LIFT_EXECUTABLE_CURRENT_ARM_ID,
    TOWER_NONSELF_GUARD_ARM_ID,
)


@dataclass(frozen=True)
class TowerStarArm:
    """One tower-star diagnostic arm."""

    arm_id: str
    arm_type: str
    guard_type: str
    candidate_id: str
    schema_id: str
    schema_mode: str
    baseline_role: str
    information_mode: str
    action_surface_description: str

    def to_row(self) -> dict[str, object]:
        return {
            "arm_id": self.arm_id,
            "arm_type": self.arm_type,
            "guard_type": self.guard_type,
            "candidate_id": self.candidate_id,
            "schema_id": self.schema_id,
            "schema_mode": self.schema_mode,
            "baseline_role": self.baseline_role,
            "information_mode": self.information_mode,
            "action_surface_description": self.action_surface_description,
        }


ARM_MANIFEST_FIELDS = (
    "arm_id",
    "arm_type",
    "guard_type",
    "candidate_id",
    "schema_id",
    "schema_mode",
    "baseline_role",
    "information_mode",
    "action_surface_description",
)


def build_tower_star_arms(candidate: object) -> tuple[TowerStarArm, ...]:
    """Build the six required tower-star diagnostic arms."""

    candidate_id = str(getattr(candidate, "candidate_id"))
    schema_id = str(getattr(candidate, "schema_id"))
    schema_mode = str(getattr(candidate, "schema_mode"))
    return (
        TowerStarArm(
            arm_id=DIRECT_RAW_ARM_ID,
            arm_type="direct_concrete_baseline",
            guard_type=RAW_GUARD,
            candidate_id="direct_baseline",
            schema_id="no_contraction",
            schema_mode="none",
            baseline_role="raw_direct_control",
            information_mode="ambient_primitive_action_alphabet",
            action_surface_description="all primitive actions",
        ),
        TowerStarArm(
            arm_id=DIRECT_INVALID_GUARD_ARM_ID,
            arm_type="direct_guarded_baseline",
            guard_type=INVALID_GUARD,
            candidate_id="direct_invalid_guard",
            schema_id="no_contraction",
            schema_mode="none",
            baseline_role="oracle_one_step_invalid_guard_control",
            information_mode=ORACLE_ONE_STEP_INFORMATION_MODE,
            action_surface_description="primitive actions except invalid one-step moves",
        ),
        TowerStarArm(
            arm_id=DIRECT_NONSELF_GUARD_ARM_ID,
            arm_type="direct_guarded_baseline",
            guard_type=NONSELF_GUARD,
            candidate_id="direct_nonself_guard",
            schema_id="no_contraction",
            schema_mode="none",
            baseline_role="oracle_one_step_nonself_guard_control",
            information_mode=ORACLE_ONE_STEP_INFORMATION_MODE,
            action_surface_description="primitive actions except one-step self loops",
        ),
        TowerStarArm(
            arm_id=TOWER_LIFT_EXECUTABLE_CURRENT_ARM_ID,
            arm_type="tower_candidate",
            guard_type=CURRENT_LIFT_EXECUTABLE_GUARD,
            candidate_id=candidate_id,
            schema_id=schema_id,
            schema_mode=schema_mode,
            baseline_role="current_lift_executable_tower",
            information_mode="executable_quotient_action_cells",
            action_surface_description="deepest executable tower action cells",
        ),
        TowerStarArm(
            arm_id=TOWER_INVALID_GUARD_ARM_ID,
            arm_type="tower_candidate",
            guard_type=INVALID_GUARD,
            candidate_id=candidate_id,
            schema_id=schema_id,
            schema_mode=schema_mode,
            baseline_role="tower_invalid_guard",
            information_mode=ORACLE_ONE_STEP_INFORMATION_MODE,
            action_surface_description=(
                "tower action cells with at least one executable lift whose "
                "primitive transition is not invalid"
            ),
        ),
        TowerStarArm(
            arm_id=TOWER_NONSELF_GUARD_ARM_ID,
            arm_type="tower_candidate",
            guard_type=NONSELF_GUARD,
            candidate_id=candidate_id,
            schema_id=schema_id,
            schema_mode=schema_mode,
            baseline_role="tower_nonself_guard",
            information_mode=ORACLE_ONE_STEP_INFORMATION_MODE,
            action_surface_description=(
                "tower action cells with at least one executable lift whose "
                "primitive transition is nonself"
            ),
        ),
    )
