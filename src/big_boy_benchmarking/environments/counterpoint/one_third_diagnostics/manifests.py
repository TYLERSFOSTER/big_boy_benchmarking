"""Manifest payloads for one-third counterpoint tower diagnostics."""

from __future__ import annotations

from pathlib import Path
from typing import Any

from big_boy_benchmarking.artifacts.schemas import ARTIFACT_SCHEMA_VERSION
from big_boy_benchmarking.environments.counterpoint import ids
from big_boy_benchmarking.environments.counterpoint.one_third_diagnostics.config import (
    DEFAULT_MODE_ID,
    DEFAULT_SCHEMA_ID,
    EVALUATION_ID,
    EVALUATION_RUN_FAMILY_ID,
    NEAR_FULL_COLLAPSE_THRESHOLD,
    OneThirdDiagnosticsBudget,
)


def evaluation_manifest_payload(
    *,
    budget: OneThirdDiagnosticsBudget,
) -> dict[str, Any]:
    return {
        "artifact_schema_version": ARTIFACT_SCHEMA_VERSION,
        "evaluation_id": EVALUATION_ID,
        "evaluation_run_family_id": EVALUATION_RUN_FAMILY_ID,
        "environment_family_id": ids.ENVIRONMENT_FAMILY_ID,
        "environment_instance_ids": list(budget.instance_ids),
        "schema_id": budget.schema_id,
        "schema_seeds": list(budget.schema_seeds),
        "mode_id": DEFAULT_MODE_ID,
        "linearization_mode_id": budget.linearization_mode_id,
        "claim_boundary": [
            "diagnostic evidence about one-third tower geometry and ABC runtime behavior",
            "not a direct-vs-tower performance comparison",
            "not a musical quality claim",
            "not a tensor-enabled runtime claim",
        ],
        "expected_file_policy": expected_file_policy(),
        "structural_limit_checks": structural_limit_checks(),
        "goal_criteria": goal_criteria(),
        "methodology_source_references": [
            "docs/design/first_counterpoint_environment/one_third_schema_tower_diagnostics/"
            "01_001_counterpoint_one_third_schema_tower_diagnostics_blueprint.md",
            "docs/prime_directive/evaluation_construction_for_readable_artifacts_protocol.md",
            "docs/prime_directive/artifact_table_to_readable_document_protocol.md",
        ],
    }


def budget_lock_payload(
    *,
    budget: OneThirdDiagnosticsBudget,
) -> dict[str, Any]:
    payload = budget.to_dict()
    payload.update(
        {
            "artifact_schema_version": ARTIFACT_SCHEMA_VERSION,
            "evaluation_id": EVALUATION_ID,
            "evaluation_run_family_id": EVALUATION_RUN_FAMILY_ID,
        }
    )
    return payload


def aggregate_summary_payload(
    *,
    status: str,
    run_count: int,
    complete_run_count: int,
    table_path: Path,
    result_paths: tuple[Path, ...],
    classification_counts: dict[str, int],
) -> dict[str, Any]:
    return {
        "artifact_schema_version": ARTIFACT_SCHEMA_VERSION,
        "evaluation_id": EVALUATION_ID,
        "status": status,
        "run_count": run_count,
        "complete_run_count": complete_run_count,
        "table_path": str(table_path),
        "result_paths": [str(path) for path in result_paths],
        "classification_counts": classification_counts,
    }


def readout_source_payload(
    *,
    repo_readout_surface: Path,
    source_artifact_root: Path,
    source_evaluation_root: Path,
    artifact_run_label: str,
    source_files: dict[str, Path],
    budget: dict[str, Any] | None = None,
) -> dict[str, Any]:
    return {
        "repo_readout_surface": str(repo_readout_surface),
        "source_artifact_root": str(source_artifact_root),
        "source_evaluation_root": str(source_evaluation_root),
        "evaluation_id": EVALUATION_ID,
        "environment_instance_ids": [] if budget is None else budget.get("instance_ids", []),
        "schema_id": DEFAULT_SCHEMA_ID,
        "schema_seeds": [] if budget is None else budget.get("schema_seeds", []),
        "artifact_run_label": artifact_run_label,
        "artifact_schema_version": ARTIFACT_SCHEMA_VERSION,
        "run_mode": "diagnostic_one_third_tower_abc",
        "source_files": {key: str(path) for key, path in source_files.items()},
        "expected_files": expected_file_policy(),
        "goal_criteria": goal_criteria(),
        "badge_policy": {
            "dimensions": [
                "artifact_status",
                "schema_geometry_status",
                "abc_runtime_status",
                "lift_executability_status",
                "claim_scope",
                "provenance_status",
            ]
        },
        "goal_summary_sources": [
            "docs/design/first_counterpoint_environment/one_third_schema_tower_diagnostics/"
            "01_001_counterpoint_one_third_schema_tower_diagnostics_blueprint.md"
        ],
        "methodology_summary_sources": [
            "docs/prime_directive/evaluation_construction_for_readable_artifacts_protocol.md"
        ],
        "structural_limit_checks": structural_limit_checks(),
        "claim_boundary": [
            "diagnostic tower-geometry and ABC-runtime evidence only",
            "no direct-vs-tower performance claim",
            "no tensor-enabled runtime claim",
        ],
    }


def expected_file_policy() -> dict[str, Any]:
    required = [
        "evaluation_manifest.json",
        "evaluation_budget_lock.json",
        "evaluation_run_index.csv",
        "evaluation_aggregate_table.csv",
        "evaluation_aggregate_summary.json",
        "results/schema_block_summary.csv",
        "results/tower_shape_summary.csv",
        "results/tier_executability_summary.csv",
        "results/control_action_summary.csv",
        "results/abc_selection_summary.csv",
        "results/abc_tier_signal_summary.csv",
        "results/tier_occupancy_summary.csv",
        "results/lift_failure_by_tier.csv",
        "results/concrete_step_summary.csv",
    ]
    return {
        "required": required,
        "expected_absent_is_gap": [],
        "conditional": {},
        "not_applicable": [
            "direct arm comparison tables",
            "tensor-enabled conversion records",
        ],
        "expectation_sources": [
            "docs/design/first_counterpoint_environment/one_third_schema_tower_diagnostics/"
            "01_002_counterpoint_one_third_schema_tower_diagnostics_implementation_gameplan.md"
        ],
    }


def goal_criteria() -> list[dict[str, str]]:
    return [
        {
            "goal_id": "schema_geometry_observed",
            "question": "What tower geometry does source-local one-third contraction produce?",
            "success_signal": "tower_shape_summary.csv has rows for small and medium tiers",
            "partial_signal": "tower_shape_summary.csv exists for only part of the locked budget",
            "failure_signal": "tower_shape_summary.csv is missing or empty",
            "claim_if_met": "BBB can describe one-third quotient geometry for the run budget.",
            "claim_if_not_met": "BBB cannot yet interpret one-third quotient geometry.",
        },
        {
            "goal_id": "abc_runtime_observed",
            "question": "How does upstream ABC choose active tiers under this schema?",
            "success_signal": (
                "abc_selection_summary.csv and abc_tier_signal_summary.csv are present"
            ),
            "partial_signal": "ABC rows are present but missing for some controller events",
            "failure_signal": "ABC rows are absent",
            "claim_if_met": "BBB can inspect upstream ABC tier selection behavior.",
            "claim_if_not_met": "BBB lacks the controller evidence needed for this diagnostic.",
        },
        {
            "goal_id": "lift_executability_observed",
            "question": "Do selected abstract actions lift to concrete counterpoint steps?",
            "success_signal": "lift_failure_by_tier.csv and concrete_step_summary.csv are present",
            "partial_signal": (
                "some lift data exists but structural-limit classifications are triggered"
            ),
            "failure_signal": "lift and concrete step evidence is missing",
            "claim_if_met": "BBB can separate quotient geometry from lift/execution behavior.",
            "claim_if_not_met": "BBB cannot distinguish geometry from lift failure.",
        },
    ]


def structural_limit_checks() -> list[dict[str, str]]:
    return [
        {
            "check_id": "full_first_projection_collapse",
            "trigger": "tier 1 largest_state_fiber_share == 1.0",
            "interpretation_if_triggered": (
                "The first projection has collapsed all base states into one state cell."
            ),
            "claim_effect": "blocks ordinary performance interpretation; diagnostic remains valid",
        },
        {
            "check_id": "near_full_first_projection_collapse",
            "trigger": (
                f"tier 1 largest_state_fiber_share >= {NEAR_FULL_COLLAPSE_THRESHOLD:.2f}"
            ),
            "interpretation_if_triggered": (
                "One tier-1 cell contains at least 90 percent of base states."
            ),
            "claim_effect": "marks quotient geometry as structurally limiting",
        },
        {
            "check_id": "selected_tier_non_executability",
            "trigger": "ABC selected tier is recorded as non-executable",
            "interpretation_if_triggered": (
                "The controller is targeting a tier that cannot emit concrete actions."
            ),
            "claim_effect": "diagnostic-only; requires lift/executability follow-up",
        },
        {
            "check_id": "no_available_action",
            "trigger": "control_action == no_available_action",
            "interpretation_if_triggered": (
                "The runtime could not find an executable tier/action at that point."
            ),
            "claim_effect": "blocks learning-performance interpretation for affected runs",
        },
        {
            "check_id": "zero_concrete_steps",
            "trigger": "concrete_step_count == 0",
            "interpretation_if_triggered": (
                "The controller loop ran without producing concrete environment steps."
            ),
            "claim_effect": "runtime/geometry diagnostic only",
        },
        {
            "check_id": "missing_abc_context",
            "trigger": "controller events exist without ABC diagnostic rows",
            "interpretation_if_triggered": (
                "The run is missing the ABC evidence needed for tier-selection interpretation."
            ),
            "claim_effect": "blocks ABC-selection claims",
        },
    ]
