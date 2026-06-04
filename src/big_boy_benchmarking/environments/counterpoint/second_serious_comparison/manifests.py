"""Manifest payloads for the second serious schema comparison."""

from __future__ import annotations

from pathlib import Path
from typing import Any

from big_boy_benchmarking.artifacts.schemas import ARTIFACT_SCHEMA_VERSION
from big_boy_benchmarking.environments.counterpoint.second_serious_comparison.arms import (
    SCHEMA0_ARM,
    SCHEMA1_ARM,
)
from big_boy_benchmarking.environments.counterpoint.second_serious_comparison.config import (
    EVALUATION_ID,
    EVALUATION_RUN_FAMILY_ID,
    SCHEMA0_CLASS_ID,
    SCHEMA1_CLASS_ID,
    SecondSeriousComparisonBudget,
)
from big_boy_benchmarking.environments.counterpoint.second_serious_comparison.thresholds import (
    ThresholdPolicy,
    TierJumpPolicy,
)


def evaluation_manifest_payload(*, budget: SecondSeriousComparisonBudget) -> dict[str, Any]:
    return {
        "artifact_schema_version": ARTIFACT_SCHEMA_VERSION,
        "evaluation_id": EVALUATION_ID,
        "evaluation_run_family_id": EVALUATION_RUN_FAMILY_ID,
        "evaluation_class": "schema_comparison_first_sustained_hit",
        "environment_family_id": "counterpoint_symbolic_v001",
        "environment_instance_id": budget.environment_instance_id,
        "run_mode": budget.run_mode,
        "comparison_object": "schema_condition",
        "primary_metric_id": "episode_total_reward",
        "persistence_rule_id": "4_of_5",
        "claim_scope": "first sustained total-space hit under matched tower-control runtime",
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


def budget_lock_payload(*, budget: SecondSeriousComparisonBudget) -> dict[str, Any]:
    payload = budget.to_dict()
    payload["artifact_schema_version"] = ARTIFACT_SCHEMA_VERSION
    payload["evaluation_id"] = EVALUATION_ID
    payload["evaluation_run_family_id"] = EVALUATION_RUN_FAMILY_ID
    return payload


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
    budget: SecondSeriousComparisonBudget,
) -> dict[str, Any]:
    return {
        "evaluation_id": EVALUATION_ID,
        "schema1_tower_source": budget.schema1_tower_source,
        "selected_schema1_candidates": [row.to_dict() for row in selection.selected],
        "excluded_schema1_candidates": [row.to_dict() for row in selection.excluded],
        "candidate_readout_source": str(selection.candidate_readout_source),
        "source_files": {key: str(value) for key, value in selection.source_files.items()},
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
) -> dict[str, Any]:
    return {
        "artifact_schema_version": ARTIFACT_SCHEMA_VERSION,
        "evaluation_id": EVALUATION_ID,
        "artifact_run_label": artifact_run_label,
        "run_mode": run_mode,
        "repo_readout_surface": str(repo_readout_surface),
        "source_artifact_root": str(source_artifact_root),
        "source_evaluation_root": str(source_evaluation_root),
        "source_files": {key: str(path) for key, path in source_files.items()},
        "budget": budget,
        "goal_criteria": [
            {
                "goal_id": "matched_schema_comparison",
                "question": "Did Schema 0 and Schema 1 run under matched training conditions?",
                "success_signal": "paired_schema_comparison.csv contains unblocked pairs",
                "partial_signal": "runs exist but some pairs are claim-blocked",
                "failure_signal": "schema0_harness_mismatch or artifact_incomplete",
                "claim_if_met": "The evaluation supports bounded schema-condition comparison.",
                "claim_if_not_met": "The evaluation does not support a schema comparison claim.",
            },
            {
                "goal_id": "first_sustained_hit",
                "question": "Which schema condition first reached sustained total-space adequacy?",
                "success_signal": "first_sustained_hit_summary.csv has sustained_hit rows",
                "partial_signal": "transient_hit_only rows exist",
                "failure_signal": "never_hit for all runs or threshold_saturated_immediately",
                "claim_if_met": (
                    "Episodes-to-hit can be compared within the locked threshold policy."
                ),
                "claim_if_not_met": (
                    "The threshold did not produce an interpretable hit comparison."
                ),
            },
        ],
        "badge_policy": {
            "dimensions": [
                "artifact_status",
                "candidate_status",
                "threshold_status",
                "comparison_status",
                "claim_scope",
                "provenance_status",
            ]
        },
        "goal_summary_sources": [
            "docs/design/first_counterpoint_environment/second_counterpoint_serious_evaluation/01_001_counterpoint_second_serious_schema_comparison_blueprint.md",
            "docs/design/first_counterpoint_environment/second_counterpoint_serious_evaluation/design_discussion.md",
        ],
        "methodology_summary_sources": [
            "docs/design/first_counterpoint_environment/second_counterpoint_serious_evaluation/01_002_counterpoint_second_serious_schema_comparison_implementation_gameplan.md",
            "docs/prime_directive/evaluation_construction_for_readable_artifacts_protocol.md",
        ],
        "structural_limit_checks": [
            {"check_id": "schema1_collapsed_tier", "trigger": "tier1 state_cell_count <= 1"},
            {
                "check_id": "schema1_non_executable_tier",
                "trigger": "tier1 active_action_cell_count <= 0",
            },
            {"check_id": "schema1_no_tier1_use", "trigger": "no selected tier-1 events"},
            {"check_id": "schema1_lift_failure_dominant", "trigger": "lift failures dominate"},
            {
                "check_id": "schema0_harness_mismatch",
                "trigger": "Schema 0 not run through matched harness",
            },
            {
                "check_id": "threshold_unreached_all",
                "trigger": "no sustained hits in either schema",
            },
            {
                "check_id": "threshold_saturated_immediately",
                "trigger": "both schemas satisfy threshold in first window",
            },
            {"check_id": "artifact_incomplete", "trigger": "required artifacts missing"},
        ],
        "expected_files": {
            "required": [
                "evaluation_manifest.json",
                "evaluation_arm_manifest.json",
                "evaluation_budget_lock.json",
                "threshold_policy_manifest.json",
                "candidate_manifest.json",
                "parent_source_manifest.json",
                "evaluation_run_index.csv",
                "evaluation_aggregate_table.csv",
                "evaluation_aggregate_summary.json",
                "results/arm_summary.csv",
                "results/candidate_summary.csv",
                "results/schema_summary.csv",
                "results/training_episode_summary.csv",
                "results/threshold_window_summary.csv",
                "results/first_sustained_hit_summary.csv",
                "results/paired_schema_comparison.csv",
                "results/comparison_claim_summary.csv",
            ],
            "conditional": {
                SCHEMA0_CLASS_ID: ["tier/lift/ABC evidence may be structurally one-tier"],
                SCHEMA1_CLASS_ID: [
                    "tier/lift/ABC evidence expected when candidate runtime executes"
                ],
            },
            "not_applicable": [
                "old direct tabular-Q baseline artifacts",
                "masked-random baseline artifacts",
                "tensor-enabled conversion records",
                "musical quality judgments",
            ],
        },
        "claim_boundary": [
            "schema-condition learning comparison only",
            "no old-direct-runner comparison claim",
            "no broad abstraction superiority claim",
            "no musical quality claim",
            "no tensor-enabled runtime claim",
        ],
    }


def threshold_policy_payload(policy: ThresholdPolicy) -> dict[str, Any]:
    return policy.to_dict()


def tier_jump_policy_payload(policy: TierJumpPolicy) -> dict[str, Any]:
    return policy.to_dict()
