"""Manifest payloads for noisy-rate full-tower training diagnostics."""

from __future__ import annotations

from pathlib import Path
from typing import Any

from big_boy_benchmarking.artifacts.schemas import ARTIFACT_SCHEMA_VERSION
from big_boy_benchmarking.environments.counterpoint import ids
from big_boy_benchmarking.environments.counterpoint.noisy_rate_full_training.config import (
    EVALUATION_ID,
    EVALUATION_RUN_FAMILY_ID,
    RUN_MODE_ID,
    NoisyRateFullTrainingBudget,
)

BLUEPRINT_PATH = (
    "docs/design/system_learning_from_evaluations/"
    "counterpoint_noisy_rate_full_tower_training_diagnostic/"
    "01_counterpoint_noisy_rate_full_tower_training_diagnostic_blueprint.md"
)
WORKPLAN_PATH = (
    "docs/design/system_learning_from_evaluations/"
    "counterpoint_noisy_rate_full_tower_training_diagnostic/"
    "02_counterpoint_noisy_rate_full_tower_training_diagnostic_implementation_workplan.md"
)
ARCHIVE_PATH = (
    "docs/design/system_learning_from_evaluations/"
    "counterpoint_noisy_rate_full_tower_training_diagnostic/README.md"
)
PARENT_READOUT_PATH = (
    "docs/evaluations/counterpoint_symbolic_v001/"
    "noisy_rate_contraction_diagnostics/readout_source.json"
)


def evaluation_manifest_payload(*, budget: NoisyRateFullTrainingBudget) -> dict[str, Any]:
    return {
        "artifact_schema_version": ARTIFACT_SCHEMA_VERSION,
        "evaluation_id": EVALUATION_ID,
        "evaluation_run_family_id": EVALUATION_RUN_FAMILY_ID,
        "environment_family_id": ids.ENVIRONMENT_FAMILY_ID,
        "mode_id": RUN_MODE_ID,
        "training_surface": "tower",
        "linearization_mode_id": budget.linearization_mode_id,
        "parent_candidate_readout_source": str(budget.parent_candidate_readout_source),
        "candidate_cap": budget.candidate_cap,
        "include_runtime_anchor": budget.include_runtime_anchor,
        "claim_boundary": claim_boundary(),
        "expected_file_policy": expected_file_policy(),
        "structural_limit_checks": structural_limit_checks(),
        "goal_criteria": goal_criteria(),
        "methodology_source_references": [
            BLUEPRINT_PATH,
            WORKPLAN_PATH,
            "docs/prime_directive/evaluation_construction_for_readable_artifacts_protocol.md",
            "docs/prime_directive/artifact_table_to_readable_document_protocol.md",
        ],
    }


def budget_lock_payload(*, budget: NoisyRateFullTrainingBudget) -> dict[str, Any]:
    payload = budget.to_dict()
    payload.update(
        {
            "artifact_schema_version": ARTIFACT_SCHEMA_VERSION,
            "evaluation_id": EVALUATION_ID,
            "evaluation_run_family_id": EVALUATION_RUN_FAMILY_ID,
        }
    )
    return payload


def candidate_manifest_payload(
    *,
    selected_candidates: list[dict[str, Any]],
    excluded_candidates: list[dict[str, Any]],
    parent_readout_source: Path,
    parent_source_files: dict[str, Path],
    budget: NoisyRateFullTrainingBudget,
) -> dict[str, Any]:
    return {
        "artifact_schema_version": ARTIFACT_SCHEMA_VERSION,
        "evaluation_id": EVALUATION_ID,
        "parent_readout_source": str(parent_readout_source),
        "parent_source_files": {key: str(path) for key, path in parent_source_files.items()},
        "candidate_selection_rules": [
            "parent run status must be success",
            "no_contraction_control is excluded by default",
            "selection consistency must be true",
            "candidate must have at least one non-base tier",
            "deepest tier must have more than one state cell",
            "deepest tier must have at least one active action cell",
            "parent aggregate must not indicate full collapse or uninterpretable status",
        ],
        "include_runtime_anchor": budget.include_runtime_anchor,
        "candidate_cap": budget.candidate_cap,
        "selected_candidates": selected_candidates,
        "excluded_candidates": excluded_candidates,
    }


def aggregate_summary_payload(
    *,
    status: str,
    run_count: int,
    complete_run_count: int,
    table_path: Path,
    result_paths: tuple[Path, ...],
    health_class_counts: dict[str, int],
) -> dict[str, Any]:
    return {
        "artifact_schema_version": ARTIFACT_SCHEMA_VERSION,
        "evaluation_id": EVALUATION_ID,
        "status": status,
        "run_count": run_count,
        "complete_run_count": complete_run_count,
        "table_path": str(table_path),
        "result_paths": [str(path) for path in result_paths],
        "health_class_counts": health_class_counts,
    }


def readout_source_payload(
    *,
    repo_readout_surface: Path,
    source_artifact_root: Path,
    source_evaluation_root: Path,
    artifact_run_label: str,
    parent_readout_source: Path,
    parent_source_evaluation_root: Path,
    source_files: dict[str, Path],
    budget: dict[str, Any] | None = None,
) -> dict[str, Any]:
    return {
        "repo_readout_surface": str(repo_readout_surface),
        "source_artifact_root": str(source_artifact_root),
        "source_evaluation_root": str(source_evaluation_root),
        "parent_readout_source": str(parent_readout_source),
        "parent_source_evaluation_root": str(parent_source_evaluation_root),
        "evaluation_id": EVALUATION_ID,
        "artifact_run_label": artifact_run_label,
        "artifact_schema_version": ARTIFACT_SCHEMA_VERSION,
        "run_mode": RUN_MODE_ID,
        "budget": {} if budget is None else budget,
        "source_files": {key: str(path) for key, path in source_files.items()},
        "expected_files": expected_file_policy(),
        "goal_criteria": goal_criteria(),
        "badge_policy": {
            "dimensions": [
                "artifact_status",
                "candidate_status",
                "training_health_status",
                "runtime_executability_status",
                "lift_status",
                "claim_scope",
                "provenance_status",
            ]
        },
        "goal_summary_sources": [BLUEPRINT_PATH, ARCHIVE_PATH],
        "methodology_summary_sources": [
            BLUEPRINT_PATH,
            WORKPLAN_PATH,
            "docs/prime_directive/evaluation_construction_for_readable_artifacts_protocol.md",
        ],
        "structural_limit_checks": structural_limit_checks(),
        "claim_boundary": claim_boundary(),
    }


def expected_file_policy() -> dict[str, Any]:
    required = [
        "evaluation_manifest.json",
        "evaluation_budget_lock.json",
        "candidate_manifest.json",
        "evaluation_run_index.csv",
        "evaluation_aggregate_table.csv",
        "evaluation_aggregate_summary.json",
        "results/candidate_summary.csv",
        "results/tower_shape_summary.csv",
        "results/training_episode_summary.csv",
        "results/training_curve_summary.csv",
        "results/tier_occupancy_summary.csv",
        "results/tier_executability_summary.csv",
        "results/lift_success_by_tier.csv",
        "results/lift_failure_by_tier.csv",
        "results/concrete_step_summary.csv",
        "results/controller_action_summary.csv",
        "results/abc_selection_summary.csv",
        "results/abc_tier_signal_summary.csv",
        "results/learner_update_summary.csv",
        "results/training_health_summary.csv",
    ]
    return {
        "required": required,
        "expected_absent_is_gap": [],
        "conditional": {},
        "not_applicable": [
            "direct baseline artifacts",
            "direct-vs-tower comparison tables",
            "schema ranking tables",
            "deep repeated-contraction tower artifacts",
            "tensor-enabled conversion records",
        ],
        "expectation_sources": [WORKPLAN_PATH],
    }


def goal_criteria() -> list[dict[str, str]]:
    return [
        {
            "goal_id": "candidate_source_bound",
            "question": "Were training candidates selected from the parent readout source?",
            "success_signal": "candidate_manifest includes selected parent candidates and source files",
            "partial_signal": "candidate manifest exists but lacks parent source detail",
            "failure_signal": "candidate manifest is missing",
            "claim_if_met": "Training candidates are traceable to repo-resident parent diagnostics.",
            "claim_if_not_met": "Training candidate provenance is not established.",
        },
        {
            "goal_id": "persistent_tower_training",
            "question": "Did each replicate preserve learner state across episodes?",
            "success_signal": "persistent_learner_across_episodes is true and learner updates are recorded",
            "partial_signal": "runtime traces exist but learner update evidence is sparse",
            "failure_signal": "learner update evidence is missing or episode-local only",
            "claim_if_met": "The run is a real tower-only training health diagnostic.",
            "claim_if_not_met": "The run is only an executability probe, not full training.",
        },
        {
            "goal_id": "tower_runtime_health",
            "question": "Did selected towers produce concrete steps and successful lifts?",
            "success_signal": "concrete_step_count and lift_success_count are positive",
            "partial_signal": "some candidates train with warnings",
            "failure_signal": "zero concrete steps or lift failures dominate",
            "claim_if_met": "Selected towers support tower-only training under the locked budget.",
            "claim_if_not_met": "Some selected towers do not train cleanly under the locked budget.",
        },
    ]


def structural_limit_checks() -> list[dict[str, str]]:
    return [
        {
            "check_id": "candidate_invalid",
            "trigger": "candidate_eligible == False",
            "interpretation_if_triggered": "Parent evidence no longer supports using this candidate.",
            "claim_effect": "blocks training-health interpretation for that candidate",
        },
        {
            "check_id": "no_concrete_steps",
            "trigger": "concrete_step_count == 0",
            "interpretation_if_triggered": "The tower runtime did not emit base transitions.",
            "claim_effect": "marks candidate untrainable under this budget",
        },
        {
            "check_id": "no_learner_updates",
            "trigger": "learner_update_count == 0",
            "interpretation_if_triggered": "The run executed but did not provide learner-update evidence.",
            "claim_effect": "blocks clean-training claim",
        },
        {
            "check_id": "selected_tier_non_executable",
            "trigger": "selected_tier_non_executability_count > 0",
            "interpretation_if_triggered": "The controller selected a tier with no live actions.",
            "claim_effect": "downgrades training health",
        },
    ]


def claim_boundary() -> list[str]:
    return [
        "tower-training health diagnostic only",
        "no direct-vs-tower comparison claim",
        "no tower advantage or disadvantage claim",
        "no noisy-rate arm ranking claim",
        "no deep repeated-contraction tower claim",
        "no tensor-enabled runtime claim",
        "no musical quality claim",
    ]

