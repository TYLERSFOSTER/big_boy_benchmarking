"""Comparison-arm declarations for PlateSupport gauntlet Stage 6."""

from __future__ import annotations

from dataclasses import dataclass

from ..tower_training_health.candidate_source import TrainingCandidate

DIRECT_BASELINE_ARM_ID = "plate_support_direct_concrete_baseline"
NO_CONTRACTION_CONTROL_ARM_ID = "plate_support_no_contraction_tower_control"


@dataclass(frozen=True)
class ComparisonArm:
    """One Stage 6 comparison arm."""

    arm_id: str
    arm_type: str
    candidate_id: str
    schema_id: str
    schema_mode: str
    ratio_numerator: int | str
    ratio_denominator: int | str
    max_iterations: int | str
    selector_rule_id: str
    selection_mode: str
    max_depth: int | str
    nontrivial_tier_count: int | str
    status: str
    baseline_role: str
    source_stage_id: str
    unavailable_reason: str = ""

    def to_row(self) -> dict[str, object]:
        return {
            "arm_id": self.arm_id,
            "arm_type": self.arm_type,
            "candidate_id": self.candidate_id,
            "schema_id": self.schema_id,
            "schema_mode": self.schema_mode,
            "ratio_numerator": self.ratio_numerator,
            "ratio_denominator": self.ratio_denominator,
            "max_iterations": self.max_iterations,
            "selector_rule_id": self.selector_rule_id,
            "selection_mode": self.selection_mode,
            "max_depth": self.max_depth,
            "nontrivial_tier_count": self.nontrivial_tier_count,
            "status": self.status,
            "baseline_role": self.baseline_role,
            "source_stage_id": self.source_stage_id,
            "unavailable_reason": self.unavailable_reason,
        }


ARM_MANIFEST_FIELDS = (
    "arm_id",
    "arm_type",
    "candidate_id",
    "schema_id",
    "schema_mode",
    "ratio_numerator",
    "ratio_denominator",
    "max_iterations",
    "selector_rule_id",
    "selection_mode",
    "max_depth",
    "nontrivial_tier_count",
    "status",
    "baseline_role",
    "source_stage_id",
    "unavailable_reason",
)


def build_comparison_arms(
    *,
    candidate: TrainingCandidate,
    include_direct_baseline: bool,
    include_no_contraction_control: bool,
) -> tuple[ComparisonArm, ...]:
    """Build active and explicitly unavailable comparison arms."""

    arms: list[ComparisonArm] = []
    if include_direct_baseline:
        arms.append(
            ComparisonArm(
                arm_id=DIRECT_BASELINE_ARM_ID,
                arm_type="direct_concrete_baseline",
                candidate_id="direct_baseline",
                schema_id="no_contraction",
                schema_mode="none",
                ratio_numerator="not_applicable",
                ratio_denominator="not_applicable",
                max_iterations="not_applicable",
                selector_rule_id="not_applicable",
                selection_mode="not_applicable",
                max_depth="not_applicable",
                nontrivial_tier_count="not_applicable",
                status="active",
                baseline_role="primary_baseline",
                source_stage_id="environment_runtime",
            )
        )
    if include_no_contraction_control:
        arms.append(
            ComparisonArm(
                arm_id=NO_CONTRACTION_CONTROL_ARM_ID,
                arm_type="no_contraction_tower_control",
                candidate_id="no_contraction_tower_control",
                schema_id="no_contraction",
                schema_mode="none",
                ratio_numerator="not_applicable",
                ratio_denominator="not_applicable",
                max_iterations="not_applicable",
                selector_rule_id="not_applicable",
                selection_mode="not_applicable",
                max_depth="not_applicable",
                nontrivial_tier_count="not_applicable",
                status="unavailable",
                baseline_role="engineering_control",
                source_stage_id="not_run",
                unavailable_reason=(
                    "No approved Stage 6 no-contraction tower-control runtime adapter "
                    "exists yet; recorded rather than simulated."
                ),
            )
        )
    arms.append(
        ComparisonArm(
            arm_id=f"plate_support_selected_tower_candidate:{candidate.candidate_id}",
            arm_type="selected_tower_candidate",
            candidate_id=candidate.candidate_id,
            schema_id=candidate.schema_id,
            schema_mode=candidate.schema_mode,
            ratio_numerator=candidate.ratio_numerator,
            ratio_denominator=candidate.ratio_denominator,
            max_iterations=candidate.max_iterations,
            selector_rule_id=candidate.selector_rule_id,
            selection_mode=candidate.selection_mode,
            max_depth=candidate.max_depth,
            nontrivial_tier_count=candidate.nontrivial_tier_count,
            status="active",
            baseline_role="candidate",
            source_stage_id="plate_support_gauntlet_tower_training_health_v001",
        )
    )
    return tuple(arms)
