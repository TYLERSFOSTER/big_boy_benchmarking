"""Manifest payloads for the small paired replicate probe."""

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
from big_boy_benchmarking.environments.counterpoint.second_serious_comparison.thresholds import (
    ThresholdPolicy,
    TierJumpPolicy,
)

from .config import (
    EVALUATION_ID,
    EVALUATION_RUN_FAMILY_ID,
    SCHEMA0_CLASS_ID,
    SCHEMA1_CLASS_ID,
    SmallPairedReplicateProbeBudget,
)
from .threshold_source import ResolvedThreshold


def evaluation_manifest_payload(*, budget: SmallPairedReplicateProbeBudget) -> dict[str, Any]:
    return {
        "artifact_schema_version": ARTIFACT_SCHEMA_VERSION,
        "evaluation_id": EVALUATION_ID,
        "evaluation_run_family_id": EVALUATION_RUN_FAMILY_ID,
        "evaluation_class": "small_paired_replicate_probe",
        "environment_family_id": "counterpoint_symbolic_v001",
        "environment_instance_id": budget.environment_instance_id,
        "run_mode": budget.run_mode,
        "comparison_object": "schema_condition_seed_pair_distribution",
        "primary_metric_id": "episode_total_reward",
        "persistence_rule_id": "4_of_5",
        "claim_scope": (
            "paired seed-bundle pattern under one corrected candidate and one locked threshold"
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


def budget_lock_payload(*, budget: SmallPairedReplicateProbeBudget) -> dict[str, Any]:
    payload = budget.to_dict()
    payload["artifact_schema_version"] = ARTIFACT_SCHEMA_VERSION
    payload["evaluation_id"] = EVALUATION_ID
    payload["evaluation_run_family_id"] = EVALUATION_RUN_FAMILY_ID
    return payload


def replicate_probe_policy_payload(
    *,
    budget: SmallPairedReplicateProbeBudget,
    threshold: ResolvedThreshold,
) -> dict[str, Any]:
    return {
        "artifact_schema_version": ARTIFACT_SCHEMA_VERSION,
        "evaluation_id": EVALUATION_ID,
        "evaluation_run_family_id": EVALUATION_RUN_FAMILY_ID,
        "candidate_cap": budget.candidate_cap,
        "training_replicates_per_arm": budget.training_replicates_per_arm,
        "episodes_per_replicate": budget.episodes_per_replicate,
        "base_seed": budget.base_seed,
        "seed_pairing_policy": "same_seed_bundle_id_for_schema0_and_schema1",
        "schema1_tower_source": budget.schema1_tower_source,
        "threshold": threshold.to_dict(),
        "bounded_claim": (
            "Detect whether Schema 1's tiny reward-margin signal survives "
            "across matched seed bundles."
        ),
    }


def threshold_policy_payload(
    policy: ThresholdPolicy,
    *,
    threshold: ResolvedThreshold,
) -> dict[str, Any]:
    payload = policy.to_dict()
    payload.update(threshold.to_dict())
    payload["metric_id"] = "episode_total_reward"
    payload["comparison"] = "greater_than_or_equal"
    payload["scope"] = "total_space"
    return payload


def tier_jump_policy_payload(policy: TierJumpPolicy) -> dict[str, Any]:
    return policy.to_dict()


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
    budget: SmallPairedReplicateProbeBudget,
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
    threshold: ResolvedThreshold,
) -> dict[str, Any]:
    import state_collapser

    return {
        "artifact_schema_version": ARTIFACT_SCHEMA_VERSION,
        "evaluation_id": EVALUATION_ID,
        "artifact_run_label": artifact_run_label,
        "run_mode": run_mode,
        "state_collapser_version": str(getattr(state_collapser, "__version__", "")),
        "liftability_semantics_id": (STATE_COLLAPSER_V072_POINTWISE_LIFTABILITY_SEMANTICS_ID),
        "repo_readout_surface": str(repo_readout_surface),
        "source_artifact_root": str(source_artifact_root),
        "source_evaluation_root": str(source_evaluation_root),
        "source_files": {key: str(path) for key, path in source_files.items()},
        "budget": budget,
        "threshold_source": threshold.to_dict(),
        "threshold_policy": {
            "metric_id": "episode_total_reward",
            "comparison": "greater_than_or_equal",
            "window_length": budget.get("window_length"),
            "required_count": budget.get("required_count"),
            "scope": "total_space",
            "threshold_value": threshold.threshold_value,
        },
        "goal_criteria": [
            {
                "goal_id": "paired_seed_identity",
                "question": "Were Schema 0 and Schema 1 matched by seed bundle?",
                "success_signal": (
                    "seed_bundle_summary.csv proves one Schema 0 and one Schema 1 run per pair"
                ),
                "partial_signal": "some pairs exist but some are blocked or incomplete",
                "failure_signal": "missing or mismatched seed_bundle_id evidence",
                "claim_if_met": "The paired distribution is interpretable.",
                "claim_if_not_met": "The paired replicate claim is blocked.",
            },
            {
                "goal_id": "schema1_margin_pattern",
                "question": "Does Schema 1 keep a positive post-hit reward margin across pairs?",
                "success_signal": (
                    "paired_delta_distribution.csv has Schema 1 margin wins "
                    "in a meaningful majority"
                ),
                "partial_signal": "mixed margin wins/losses or too few unblocked pairs",
                "failure_signal": "margin signal disappears, flips, or all pairs block",
                "claim_if_met": "The result motivates a larger serious comparison.",
                "claim_if_not_met": "The result does not yet motivate scaling this comparison.",
            },
        ],
        "badge_policy": {
            "dimensions": [
                "artifact_status",
                "pair_count",
                "unblocked_pairs",
                "schema1_margin_wins",
                "sustained_hit_rate_difference",
                "liftability_semantics",
                "lift_failures",
                "provenance_status",
            ]
        },
        "goal_summary_sources": [
            "docs/design/first_counterpoint_environment/small_paired_replicate_probe/01_001_counterpoint_small_paired_replicate_probe_blueprint.md",
            "docs/design/first_counterpoint_environment/small_paired_replicate_probe/README.md",
        ],
        "methodology_summary_sources": [
            "docs/design/first_counterpoint_environment/small_paired_replicate_probe/01_002_counterpoint_small_paired_replicate_probe_implementation_gameplan.md",
            "docs/prime_directive/evaluation_construction_for_readable_artifacts_protocol.md",
        ],
        "structural_limit_checks": [
            {
                "check_id": "paired_seed_identity_missing",
                "trigger": "seed_bundle_summary contains missing or mismatched arms",
                "interpretation_if_triggered": "The pair-level claim is blocked.",
                "claim_effect": "blocks paired interpretation",
            },
            {
                "check_id": "all_pairs_blocked",
                "trigger": "unblocked_pair_count == 0",
                "interpretation_if_triggered": "No paired behavioral claim is supported.",
                "claim_effect": "blocks margin/speed claim",
            },
            {
                "check_id": "lift_failure_present",
                "trigger": "lift_failure_by_tier has nonzero event_count",
                "interpretation_if_triggered": "Tower runtime may be structurally blocked.",
                "claim_effect": "downgrades interpretation",
            },
        ],
        "expected_files": {
            "required": [
                "evaluation_manifest.json",
                "evaluation_arm_manifest.json",
                "evaluation_budget_lock.json",
                "replicate_probe_policy_manifest.json",
                "threshold_policy_manifest.json",
                "candidate_manifest.json",
                "parent_source_manifest.json",
                "evaluation_run_index.csv",
                "evaluation_aggregate_table.csv",
                "evaluation_aggregate_summary.json",
                "results/replicate_pair_summary.csv",
                "results/paired_delta_distribution.csv",
                "results/schema_arm_distribution.csv",
                "results/post_hit_margin_distribution.csv",
                "results/sustained_hit_rate_summary.csv",
                "results/seed_bundle_summary.csv",
                "results/lift_success_by_tier.csv",
                "results/lift_failure_by_tier.csv",
                "results/tower_shape_summary.csv",
                "results/timing_summary.csv",
            ],
            "conditional": {
                SCHEMA0_CLASS_ID: ["tier/lift/ABC evidence may be structurally one-tier"],
                SCHEMA1_CLASS_ID: [
                    "tier/lift/ABC evidence expected when candidate runtime executes"
                ],
            },
            "not_applicable": [
                "threshold frontier sweep tables",
                "old direct tabular-Q baseline artifacts",
                "masked-random baseline artifacts",
                "tensor-enabled conversion records",
                "musical quality judgments",
            ],
        },
        "claim_boundary": [
            "single-candidate paired seed-bundle pattern only",
            "no statistical significance claim",
            "no broad abstraction superiority claim",
            "no tensor-enabled runtime claim",
            "no musical quality claim",
        ],
    }
