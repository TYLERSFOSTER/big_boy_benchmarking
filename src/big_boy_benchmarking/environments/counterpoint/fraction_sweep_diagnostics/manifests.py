"""Manifest payloads for counterpoint contraction fraction sweep diagnostics."""

from __future__ import annotations

from pathlib import Path
from typing import Any

from big_boy_benchmarking.artifacts.schemas import ARTIFACT_SCHEMA_VERSION
from big_boy_benchmarking.environments.counterpoint import ids
from big_boy_benchmarking.environments.counterpoint.fraction_sweep_diagnostics.config import (
    DEFAULT_SCHEMA_FAMILY_ID,
    EVALUATION_ID,
    EVALUATION_RUN_FAMILY_ID,
    NEAR_FULL_COLLAPSE_THRESHOLD,
    RUN_MODE_ID,
    FractionSweepDiagnosticsBudget,
)

BLUEPRINT_PATH = (
    "docs/design/system_learning_from_evaluations/"
    "counterpoint_one_third_schema_unexpected_collapse/"
    "03_n_over_18_contraction_fraction_sweep_blueprint.md"
)
ARCHIVE_PATH = (
    "docs/design/system_learning_from_evaluations/"
    "counterpoint_one_third_schema_unexpected_collapse/README.md"
)


def evaluation_manifest_payload(*, budget: FractionSweepDiagnosticsBudget) -> dict[str, Any]:
    return {
        "artifact_schema_version": ARTIFACT_SCHEMA_VERSION,
        "evaluation_id": EVALUATION_ID,
        "evaluation_run_family_id": EVALUATION_RUN_FAMILY_ID,
        "environment_family_id": ids.ENVIRONMENT_FAMILY_ID,
        "environment_instance_ids": list(budget.instance_ids),
        "schema_family_id": DEFAULT_SCHEMA_FAMILY_ID,
        "numerators": list(budget.numerators),
        "denominator": budget.denominator,
        "arm_ids": list(budget.arm_ids()),
        "schema_seeds": list(budget.schema_seeds),
        "mode_id": RUN_MODE_ID,
        "linearization_mode_id": budget.linearization_mode_id,
        "claim_boundary": claim_boundary(),
        "expected_file_policy": expected_file_policy(),
        "structural_limit_checks": structural_limit_checks(),
        "goal_criteria": goal_criteria(),
        "methodology_source_references": [
            BLUEPRINT_PATH,
            "docs/prime_directive/evaluation_construction_for_readable_artifacts_protocol.md",
            "docs/prime_directive/artifact_table_to_readable_document_protocol.md",
        ],
    }


def evaluation_arm_manifest_payload(*, budget: FractionSweepDiagnosticsBudget) -> dict[str, Any]:
    return {
        "artifact_schema_version": ARTIFACT_SCHEMA_VERSION,
        "evaluation_id": EVALUATION_ID,
        "arms": [
            {
                "arm_id": arm_id,
                "numerator": 0 if arm_id == "no_contraction_control" else numerator,
                "denominator": budget.denominator,
                "role": "structural_control"
                if arm_id == "no_contraction_control"
                else "fraction_sweep_diagnostic",
            }
            for arm_id, numerator in (
                [("no_contraction_control", 0)]
                if budget.include_no_contraction_control
                else []
            )
            + [
                (f"n{numerator:02d}_over_{budget.denominator}", numerator)
                for numerator in budget.numerators
            ]
        ],
    }


def budget_lock_payload(*, budget: FractionSweepDiagnosticsBudget) -> dict[str, Any]:
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
    sweep_verdict_counts: dict[str, int],
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
        "sweep_verdict_counts": sweep_verdict_counts,
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
        "schema_family_id": DEFAULT_SCHEMA_FAMILY_ID,
        "numerators": [] if budget is None else budget.get("numerators", []),
        "denominator": None if budget is None else budget.get("denominator"),
        "schema_seeds": [] if budget is None else budget.get("schema_seeds", []),
        "artifact_run_label": artifact_run_label,
        "artifact_schema_version": ARTIFACT_SCHEMA_VERSION,
        "run_mode": RUN_MODE_ID,
        "source_files": {key: str(path) for key, path in source_files.items()},
        "expected_files": expected_file_policy(),
        "goal_criteria": goal_criteria(),
        "badge_policy": {
            "dimensions": [
                "artifact_status",
                "sweep_status",
                "legacy_endpoint_status",
                "runtime_executability_status",
                "claim_scope",
                "provenance_status",
            ]
        },
        "goal_summary_sources": [BLUEPRINT_PATH, ARCHIVE_PATH],
        "methodology_summary_sources": [
            BLUEPRINT_PATH,
            "docs/prime_directive/evaluation_construction_for_readable_artifacts_protocol.md",
        ],
        "structural_limit_checks": structural_limit_checks(),
        "claim_boundary": claim_boundary(),
    }


def expected_file_policy() -> dict[str, Any]:
    required = [
        "evaluation_manifest.json",
        "evaluation_arm_manifest.json",
        "evaluation_budget_lock.json",
        "evaluation_run_index.csv",
        "evaluation_aggregate_table.csv",
        "evaluation_aggregate_summary.json",
        "results/schema_fraction_summary.csv",
        "results/tower_shape_summary.csv",
        "results/endpoint_coalescence_summary.csv",
        "results/tier_executability_summary.csv",
        "results/tier_occupancy_summary.csv",
        "results/control_action_summary.csv",
        "results/abc_selection_summary.csv",
        "results/abc_tier_signal_summary.csv",
        "results/lift_failure_by_tier.csv",
        "results/concrete_step_summary.csv",
        "results/collapse_threshold_summary.csv",
        "results/legacy_one_third_equivalence_summary.csv",
    ]
    return {
        "required": required,
        "expected_absent_is_gap": [],
        "conditional": {},
        "not_applicable": [
            "direct arm comparison tables",
            "tensor-enabled conversion records",
            "learning performance comparison tables",
        ],
        "expectation_sources": [
            "docs/design/system_learning_from_evaluations/"
            "counterpoint_one_third_schema_unexpected_collapse/"
            "04_n_over_18_contraction_fraction_sweep_implementation_workplan.md"
        ],
    }


def goal_criteria() -> list[dict[str, str]]:
    return [
        {
            "goal_id": "sweep_artifacts_complete",
            "question": "Did every requested arm produce required evidence?",
            "success_signal": "all required result tables exist and every requested n/18 arm is represented",
            "partial_signal": "some arms or summary tables are missing",
            "failure_signal": "run index or core result tables are missing",
            "claim_if_met": "The contraction-fraction sweep completed its artifact contract.",
            "claim_if_not_met": "The sweep cannot yet support human-readable diagnosis.",
        },
        {
            "goal_id": "threshold_visibility",
            "question": "Does the sweep reveal whether collapse emerges gradually or immediately?",
            "success_signal": "collapse_threshold_summary.csv reports first collapse and last nontrivial n",
            "partial_signal": "collapse status exists for only part of the sweep",
            "failure_signal": "collapse status is absent",
            "claim_if_met": (
                "The evaluation identifies the observed first-tier collapse threshold under "
                "current BBB/state_collapser schema semantics."
            ),
            "claim_if_not_met": "The evaluation cannot distinguish threshold behavior.",
        },
        {
            "goal_id": "legacy_one_third_check",
            "question": "Does 6/18 reproduce the old one-third first block?",
            "success_signal": "legacy_one_third_equivalence_summary.csv reports equivalent=True",
            "partial_signal": "equivalence is checked but mixed across instances or seeds",
            "failure_signal": "equivalence is missing or false",
            "claim_if_met": "The sweep endpoint is comparable to the prior one-third diagnostic.",
            "claim_if_not_met": "The sweep endpoint cannot be compared to the prior one-third diagnostic.",
        },
        {
            "goal_id": "active_surface_readability",
            "question": "Can a human tell which tiers are actually executable?",
            "success_signal": "active action-cell counts, tier occupancy, lift, and concrete steps are summarized",
            "partial_signal": "some active-surface tables are present",
            "failure_signal": "active-surface tables are missing",
            "claim_if_met": "The evaluation distinguishes constructed quotient shape from live executable control surface.",
            "claim_if_not_met": "The evaluation risks confusing quotient construction with execution.",
        },
    ]


def structural_limit_checks() -> list[dict[str, str]]:
    return [
        {
            "check_id": "full_first_projection_collapse",
            "trigger": "tier 1 state_cell_count == 1",
            "interpretation_if_triggered": "The first scheduled block collapses all base states into one state cell.",
            "claim_effect": "diagnostic-only; blocks learning-performance interpretation",
        },
        {
            "check_id": "near_full_first_projection_collapse",
            "trigger": f"tier 1 largest_state_cell_share >= {NEAR_FULL_COLLAPSE_THRESHOLD:.2f}",
            "interpretation_if_triggered": "One tier-1 cell contains at least 90 percent of base states.",
            "claim_effect": "marks quotient geometry as structurally limiting",
        },
        {
            "check_id": "legacy_endpoint_mismatch",
            "trigger": "n06_over_18 selected edge set differs from old one-third block 0",
            "interpretation_if_triggered": "The sweep endpoint is not comparable to the prior one-third diagnostic.",
            "claim_effect": "invalidates endpoint comparison",
        },
        {
            "check_id": "non_monotone_selected_edges",
            "trigger": "selected edges are not nested across increasing n",
            "interpretation_if_triggered": "The sweep is not a clean contraction-width threshold experiment.",
            "claim_effect": "invalidates threshold interpretation",
        },
    ]


def claim_boundary() -> list[str]:
    return [
        "diagnostic tower-geometry and ABC-runtime evidence only",
        "no direct-vs-tower performance claim",
        "no tower advantage or disadvantage claim",
        "no tensor-enabled runtime claim",
        "no musical quality claim",
        "no claim that the counterpoint environment is degenerate",
    ]

