"""Manifest payloads for the counterpoint threshold-frontier probe."""

from __future__ import annotations

from pathlib import Path
from typing import Any

from big_boy_benchmarking.artifacts.schemas import ARTIFACT_SCHEMA_VERSION
from big_boy_benchmarking.environments.counterpoint.liftability import (
    STATE_COLLAPSER_V072_POINTWISE_LIFTABILITY_SEMANTICS_ID,
)
from big_boy_benchmarking.environments.counterpoint.second_serious_comparison.arms import (
    SCHEMA0_ARM,
    SCHEMA1_ARM,
)

from .config import (
    EVALUATION_ID,
    EVALUATION_RUN_FAMILY_ID,
    ThresholdFrontierProbeBudget,
)
from .thresholds import threshold_label


def evaluation_manifest_payload(*, budget: ThresholdFrontierProbeBudget) -> dict[str, Any]:
    return {
        "artifact_schema_version": ARTIFACT_SCHEMA_VERSION,
        "evaluation_id": EVALUATION_ID,
        "evaluation_run_family_id": EVALUATION_RUN_FAMILY_ID,
        "evaluation_class": "threshold_frontier_probe",
        "environment_family_id": "counterpoint_symbolic_v001",
        "environment_instance_id": budget.environment_instance_id,
        "run_mode": budget.run_mode,
        "comparison_object": "schema_condition_threshold_frontier",
        "primary_metric_id": "episode_total_reward",
        "persistence_rule_id": "4_of_5",
        "claim_scope": (
            "single corrected candidate threshold frontier under matched seed and budget"
        ),
    }


def evaluation_arm_manifest_payload() -> dict[str, Any]:
    return {
        "evaluation_id": EVALUATION_ID,
        "schema_classes": [
            {
                "schema_class_id": SCHEMA0_ARM.schema_class_id,
                "display_name": SCHEMA0_ARM.display_name,
                "schema_id": SCHEMA0_ARM.schema_id,
                "requires_candidate": SCHEMA0_ARM.requires_candidate,
                "claim_role": SCHEMA0_ARM.claim_role,
            },
            {
                "schema_class_id": SCHEMA1_ARM.schema_class_id,
                "display_name": SCHEMA1_ARM.display_name,
                "schema_id": SCHEMA1_ARM.schema_id,
                "requires_candidate": SCHEMA1_ARM.requires_candidate,
                "claim_role": SCHEMA1_ARM.claim_role,
            },
        ],
    }


def budget_lock_payload(*, budget: ThresholdFrontierProbeBudget) -> dict[str, Any]:
    payload = budget.to_dict()
    payload["artifact_schema_version"] = ARTIFACT_SCHEMA_VERSION
    payload["evaluation_id"] = EVALUATION_ID
    payload["evaluation_run_family_id"] = EVALUATION_RUN_FAMILY_ID
    return payload


def threshold_frontier_policy_payload(*, budget: ThresholdFrontierProbeBudget) -> dict[str, Any]:
    return {
        "artifact_schema_version": ARTIFACT_SCHEMA_VERSION,
        "evaluation_id": EVALUATION_ID,
        "evaluation_run_family_id": EVALUATION_RUN_FAMILY_ID,
        "threshold_grid": [
            {
                "threshold_value": value,
                "threshold_label": threshold_label(value),
            }
            for value in budget.threshold_values
        ],
        "metric_id": "episode_total_reward",
        "comparison": "greater_than_or_equal",
        "window_length": budget.window_length,
        "required_count": budget.required_count,
        "scope": "total_space",
        "threshold_grid_source": "blueprint_locked_or_cli_explicit",
        "claim_boundary": ("next-measure frontier probe only; not a final serious comparison"),
    }


def threshold_run_manifest_payload(*, threshold_runs: list[dict[str, Any]]) -> dict[str, Any]:
    return {
        "artifact_schema_version": ARTIFACT_SCHEMA_VERSION,
        "evaluation_id": EVALUATION_ID,
        "evaluation_run_family_id": EVALUATION_RUN_FAMILY_ID,
        "threshold_runs": threshold_runs,
    }


def parent_source_manifest_payload(*, selection) -> dict[str, Any]:
    return {
        "evaluation_id": EVALUATION_ID,
        "candidate_readout_source": str(selection.candidate_readout_source),
        "source_evaluation_root": str(selection.source_evaluation_root),
        "source_artifact_root": str(selection.source_artifact_root),
        "artifact_run_label": selection.artifact_run_label,
        "parent_readout_source": (
            None
            if selection.parent_readout_source is None
            else str(selection.parent_readout_source)
        ),
        "parent_source_evaluation_root": (
            None
            if selection.parent_source_evaluation_root is None
            else str(selection.parent_source_evaluation_root)
        ),
        "source_files": {key: str(value) for key, value in selection.source_files.items()},
    }


def candidate_manifest_payload(
    *,
    selection,
    budget: ThresholdFrontierProbeBudget,
) -> dict[str, Any]:
    return {
        "evaluation_id": EVALUATION_ID,
        "schema1_tower_source": budget.schema1_tower_source,
        "selected_schema1_candidates": [row.to_dict() for row in selection.selected],
        "excluded_schema1_candidates": [row.to_dict() for row in selection.excluded],
        "candidate_readout_source": str(selection.candidate_readout_source),
        "source_files": {key: str(value) for key, value in selection.source_files.items()},
    }


def run_family_summary_payload(
    *,
    budget: ThresholdFrontierProbeBudget,
    threshold_runs: list[dict[str, Any]],
) -> dict[str, Any]:
    return {
        "artifact_schema_version": ARTIFACT_SCHEMA_VERSION,
        "evaluation_id": EVALUATION_ID,
        "run_family_id": EVALUATION_RUN_FAMILY_ID,
        "run_mode": budget.run_mode,
        "threshold_count": len(threshold_runs),
        "threshold_runs": threshold_runs,
    }


def readout_source_payload(
    *,
    repo_readout_surface: Path,
    source_artifact_root: Path,
    source_evaluation_root: Path,
    artifact_run_label: str,
    run_mode: str,
    source_files: dict[str, Path],
    budget: dict[str, Any],
    recommended_replicate_probe_threshold: float | None,
) -> dict[str, Any]:
    import state_collapser

    return {
        "artifact_schema_version": ARTIFACT_SCHEMA_VERSION,
        "evaluation_id": EVALUATION_ID,
        "artifact_run_label": artifact_run_label,
        "run_mode": run_mode,
        "state_collapser_version": str(getattr(state_collapser, "__version__", "")),
        "liftability_semantics_id": STATE_COLLAPSER_V072_POINTWISE_LIFTABILITY_SEMANTICS_ID,
        "repo_readout_surface": str(repo_readout_surface),
        "source_artifact_root": str(source_artifact_root),
        "source_evaluation_root": str(source_evaluation_root),
        "source_files": {key: str(path) for key, path in source_files.items()},
        "budget": budget,
        "threshold_grid": list(budget.get("threshold_values", ())),
        "threshold_frontier_policy": {
            "metric_id": "episode_total_reward",
            "comparison": "greater_than_or_equal",
            "window_length": budget.get("window_length"),
            "required_count": budget.get("required_count"),
            "scope": "total_space",
        },
        "recommended_replicate_probe_threshold": recommended_replicate_probe_threshold,
        "goal_criteria": [
            {
                "goal_id": "threshold_grid_complete",
                "question": "Did every locked threshold produce evidence?",
                "success_signal": "threshold_run_manifest lists every threshold as complete",
                "partial_signal": "some thresholds complete while others are blocked",
                "failure_signal": "missing threshold rows or incomplete threshold subruns",
                "claim_if_met": "The frontier table is interpretable.",
                "claim_if_not_met": "The frontier claim is blocked by missing evidence.",
            },
            {
                "goal_id": "frontier_separation",
                "question": "Does Schema 1 sustain a stricter threshold than Schema 0?",
                "success_signal": "frontier_summary.csv reports Schema 1-only passing thresholds",
                "partial_signal": "Schema 1 has margin wins but no frontier separation",
                "failure_signal": "Schema 1 does not separate or is worse on the frontier",
                "claim_if_met": "The result motivates a paired replicate threshold choice.",
                "claim_if_not_met": "The result does not show frontier advantage.",
            },
        ],
        "badge_policy": {
            "dimensions": [
                "artifact_status",
                "thresholds_tested",
                "frontier_status",
                "highest_shared_passing_threshold",
                "schema1_only_passing_threshold",
                "recommended_replicate_threshold",
                "liftability_semantics",
                "lift_failures",
                "provenance_status",
            ]
        },
        "goal_summary_sources": [
            "docs/design/first_counterpoint_environment/threshold_frontier_probe/01_001_counterpoint_threshold_frontier_probe_blueprint.md",
            "docs/design/first_counterpoint_environment/threshold_frontier_probe/README.md",
        ],
        "methodology_summary_sources": [
            "docs/design/first_counterpoint_environment/threshold_frontier_probe/01_002_counterpoint_threshold_frontier_probe_implementation_gameplan.md",
            "docs/prime_directive/evaluation_construction_for_readable_artifacts_protocol.md",
        ],
        "structural_limit_checks": [
            {
                "check_id": "threshold_subrun_incomplete",
                "trigger": "threshold_run_manifest status != complete",
                "interpretation_if_triggered": "The threshold row is blocked.",
                "claim_effect": "blocks frontier interpretation at that threshold",
            },
            {
                "check_id": "lift_failure_present",
                "trigger": "lift_failure_by_tier has nonzero event_count",
                "interpretation_if_triggered": "Tower runtime may be structurally blocked.",
                "claim_effect": "downgrades or blocks threshold interpretation",
            },
        ],
        "expected_files": {
            "required": [
                "evaluation_manifest.json",
                "evaluation_arm_manifest.json",
                "evaluation_budget_lock.json",
                "threshold_frontier_policy_manifest.json",
                "threshold_run_manifest.json",
                "candidate_manifest.json",
                "parent_source_manifest.json",
                "evaluation_run_index.csv",
                "evaluation_aggregate_table.csv",
                "evaluation_aggregate_summary.json",
                "results/threshold_arm_summary.csv",
                "results/threshold_pair_summary.csv",
                "results/post_hit_margin_summary.csv",
                "results/first_failure_frontier_summary.csv",
                "results/frontier_summary.csv",
                "results/tower_shape_summary.csv",
                "results/lift_success_by_tier.csv",
                "results/lift_failure_by_tier.csv",
                "results/timing_summary.csv",
            ],
            "expected_absent_is_gap": [],
            "conditional": {},
            "not_applicable": [
                "statistical significance testing",
                "multi-candidate broad comparison",
                "tensor-enabled runtime records",
            ],
            "expectation_sources": [
                "docs/design/first_counterpoint_environment/threshold_frontier_probe/01_002_counterpoint_threshold_frontier_probe_implementation_gameplan.md"
            ],
        },
        "claim_boundary": [
            "threshold-frontier next-measure probe only",
            "no broad abstraction superiority claim",
            "no final serious comparison claim",
            "no statistical significance claim",
            "no tensor-enabled runtime claim",
            "no musical quality claim",
        ],
    }
