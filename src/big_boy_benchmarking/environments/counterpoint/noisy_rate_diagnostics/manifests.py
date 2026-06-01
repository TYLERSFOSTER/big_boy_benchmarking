"""Manifest payloads for counterpoint noisy-rate contraction diagnostics."""

from __future__ import annotations

from pathlib import Path
from typing import Any

from big_boy_benchmarking.artifacts.schemas import ARTIFACT_SCHEMA_VERSION
from big_boy_benchmarking.environments.counterpoint import ids
from big_boy_benchmarking.environments.counterpoint.noisy_rate_diagnostics.config import (
    DEFAULT_SCHEMA_FAMILY_ID,
    DEFAULT_SELECTOR_RULE_ID,
    EVALUATION_ID,
    EVALUATION_RUN_FAMILY_ID,
    HIGH_SOURCE_COVERAGE_THRESHOLD,
    NEAR_FULL_COLLAPSE_THRESHOLD,
    NO_CONTRACTION_ARM_ID,
    RUN_MODE_ID,
    NoisyRateDiagnosticsBudget,
)

BLUEPRINT_PATH = (
    "docs/design/system_learning_from_evaluations/"
    "counterpoint_noisy_rate_contraction_diagnostics/"
    "02_counterpoint_noisy_rate_contraction_diagnostics_blueprint.md"
)
GAMEPLAN_PATH = (
    "docs/design/system_learning_from_evaluations/"
    "counterpoint_noisy_rate_contraction_diagnostics/"
    "03_counterpoint_noisy_rate_contraction_diagnostics_implementation_gameplan.md"
)
ARCHIVE_PATH = (
    "docs/design/system_learning_from_evaluations/"
    "counterpoint_noisy_rate_contraction_diagnostics/README.md"
)
PARENT_UNEXPECTED_COLLAPSE_ARCHIVE_PATH = (
    "docs/design/system_learning_from_evaluations/"
    "counterpoint_one_third_schema_unexpected_collapse/README.md"
)
PREVIOUS_FRACTION_SWEEP_READOUT_PATH = (
    "docs/evaluations/counterpoint_symbolic_v001/"
    "contraction_fraction_sweep_diagnostics/README.md"
)


def evaluation_manifest_payload(*, budget: NoisyRateDiagnosticsBudget) -> dict[str, Any]:
    return {
        "artifact_schema_version": ARTIFACT_SCHEMA_VERSION,
        "evaluation_id": EVALUATION_ID,
        "evaluation_run_family_id": EVALUATION_RUN_FAMILY_ID,
        "environment_family_id": ids.ENVIRONMENT_FAMILY_ID,
        "environment_instance_ids": list(budget.instance_ids),
        "schema_family_id": DEFAULT_SCHEMA_FAMILY_ID,
        "selector_rule_id": budget.selector_rule_id,
        "rates": [rate.to_dict() for rate in budget.rates],
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
            GAMEPLAN_PATH,
            "docs/prime_directive/evaluation_construction_for_readable_artifacts_protocol.md",
            "docs/prime_directive/artifact_table_to_readable_document_protocol.md",
        ],
    }


def evaluation_arm_manifest_payload(*, budget: NoisyRateDiagnosticsBudget) -> dict[str, Any]:
    arms: list[dict[str, Any]] = []
    if budget.include_no_contraction_control:
        arms.append(
            {
                "arm_id": NO_CONTRACTION_ARM_ID,
                "numerator": 0,
                "denominator": 1,
                "requested_rate": 0.0,
                "selector_rule_id": "no_contraction_control",
                "role": "structural_control",
            }
        )
    arms.extend(
        {
            "arm_id": rate.arm_id,
            "numerator": rate.numerator,
            "denominator": rate.denominator,
            "requested_rate": rate.requested_rate,
            "selector_rule_id": budget.selector_rule_id,
            "role": "noisy_rate_diagnostic",
        }
        for rate in budget.rates
    )
    return {
        "artifact_schema_version": ARTIFACT_SCHEMA_VERSION,
        "evaluation_id": EVALUATION_ID,
        "arms": arms,
    }


def budget_lock_payload(*, budget: NoisyRateDiagnosticsBudget) -> dict[str, Any]:
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
        "selector_rule_id": DEFAULT_SELECTOR_RULE_ID
        if budget is None
        else budget.get("selector_rule_id", DEFAULT_SELECTOR_RULE_ID),
        "rates": [] if budget is None else budget.get("rates", []),
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
                "noisy_rate_sweep_status",
                "source_coverage_status",
                "collapse_threshold_status",
                "runtime_executability_status",
                "claim_scope",
                "provenance_status",
            ]
        },
        "goal_summary_sources": [
            BLUEPRINT_PATH,
            ARCHIVE_PATH,
            PARENT_UNEXPECTED_COLLAPSE_ARCHIVE_PATH,
            PREVIOUS_FRACTION_SWEEP_READOUT_PATH,
        ],
        "methodology_summary_sources": [
            BLUEPRINT_PATH,
            GAMEPLAN_PATH,
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
        "results/noisy_rate_selection_summary.csv",
        "results/noisy_rate_source_coverage_summary.csv",
        "results/noisy_rate_selection_consistency_summary.csv",
        "results/noisy_rate_monotonicity_summary.csv",
        "results/noisy_rate_threshold_summary.csv",
        "results/tower_shape_summary.csv",
        "results/endpoint_coalescence_summary.csv",
        "results/tier_executability_summary.csv",
        "results/tier_occupancy_summary.csv",
        "results/control_action_summary.csv",
        "results/abc_selection_summary.csv",
        "results/abc_tier_signal_summary.csv",
        "results/lift_failure_by_tier.csv",
        "results/concrete_step_summary.csv",
    ]
    return {
        "required": required,
        "expected_absent_is_gap": [],
        "conditional": {},
        "not_applicable": [
            "legacy one-third equivalence table",
            "deterministic source-local floor reference arms",
            "direct arm comparison tables",
            "tensor-enabled conversion records",
            "learning performance comparison tables",
        ],
        "expectation_sources": [GAMEPLAN_PATH],
    }


def goal_criteria() -> list[dict[str, str]]:
    return [
        {
            "goal_id": "noisy_rate_artifacts_complete",
            "question": "Did every requested noisy-rate arm produce required evidence?",
            "success_signal": "all required noisy-rate result tables exist and every requested rate arm is represented",
            "partial_signal": "some arms or summary tables are missing",
            "failure_signal": "run index or core result tables are missing",
            "claim_if_met": "The noisy-rate diagnostic completed its artifact contract.",
            "claim_if_not_met": "The diagnostic cannot yet support human-readable interpretation.",
        },
        {
            "goal_id": "source_coverage_visible",
            "question": "Can a reader distinguish selected edge share from selected source coverage?",
            "success_signal": "source coverage and zero-selected-source counts are present",
            "partial_signal": "selected edges are present but source coverage is incomplete",
            "failure_signal": "source coverage table is missing",
            "claim_if_met": "The evaluation reports whether low expected-rate selection leaves sources unselected.",
            "claim_if_not_met": "The evaluation risks repeating the source-local fraction confusion.",
        },
        {
            "goal_id": "selection_contract_valid",
            "question": "Do metadata-selected and runtime-selected edge sets agree?",
            "success_signal": "selection_consistency reports equality for every non-control arm",
            "partial_signal": "consistency exists but has mixed status",
            "failure_signal": "consistency is missing or false",
            "claim_if_met": "The metadata summaries describe the same edges the runtime schema contracted.",
            "claim_if_not_met": "The structural diagnosis is invalid until mapping is fixed.",
        },
        {
            "goal_id": "threshold_visibility",
            "question": "Does the sweep reveal whether collapse appears immediately or at a higher rate?",
            "success_signal": "noisy_rate_threshold_summary reports first collapse and last nontrivial rate",
            "partial_signal": "collapse status exists for only part of the sweep",
            "failure_signal": "threshold status is absent",
            "claim_if_met": "The evaluation identifies observed collapse threshold behavior under noisy-rate semantics.",
            "claim_if_not_met": "The evaluation cannot distinguish threshold behavior.",
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
            "check_id": "metadata_runtime_selection_mismatch",
            "trigger": "selection_sets_equal == False",
            "interpretation_if_triggered": "The metadata table and runtime schema do not identify the same contracted edges.",
            "claim_effect": "invalidates structural interpretation",
        },
        {
            "check_id": "non_monotone_selected_edges",
            "trigger": "subset_pass == False",
            "interpretation_if_triggered": "Increasing requested rate did not preserve selected-edge nesting.",
            "claim_effect": "invalidates threshold interpretation",
        },
        {
            "check_id": "zero_source_coverage",
            "trigger": "selected_source_share == 0",
            "interpretation_if_triggered": "No source contributed selected outgoing edges at this rate.",
            "claim_effect": "marks this arm as a very low-width structural diagnostic",
        },
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
            "check_id": "high_source_coverage",
            "trigger": f"selected_source_share >= {HIGH_SOURCE_COVERAGE_THRESHOLD:.2f}",
            "interpretation_if_triggered": "A high share of source states contributed at least one selected outgoing edge.",
            "claim_effect": "supports coverage-threshold interpretation if collapse appears at or after this point",
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
        "no claim that noisy-rate contraction is generally good or bad beyond observed artifact evidence",
    ]
