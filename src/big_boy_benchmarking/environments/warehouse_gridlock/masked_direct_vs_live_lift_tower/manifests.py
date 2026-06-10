"""Manifest helpers for Warehouse masked direct/live-lift tower diagnostics."""

from __future__ import annotations

from pathlib import Path
from typing import Any

from big_boy_benchmarking.artifacts.writers import write_json
from big_boy_benchmarking.environments.warehouse_gridlock.instances import (
    WarehouseGridlockInstance,
)
from big_boy_benchmarking.environments.warehouse_gridlock.masked_direct_vs_live_lift_tower.arms import (
    arm_manifest_rows,
    no_lookahead_policy_manifest,
)
from big_boy_benchmarking.environments.warehouse_gridlock.masked_direct_vs_live_lift_tower.config import (
    ARTIFACT_SCHEMA_VERSION_ID,
    DIRECT_CANDIDATE_POLICY_ID,
    DIRECT_MASK_POLICY_ID,
    EVALUATION_ID,
    LIVE_LIFT_POLICY_ID,
    TOWER_CANDIDATE_POLICY_ID,
    TOWER_MASK_POLICY_ID,
    TOWER_SCHEMA_ID,
    TOWER_SURFACE_POLICY_ID,
    MaskedDirectVsLiveLiftConfig,
)
from big_boy_benchmarking.environments.warehouse_gridlock.masked_direct_vs_live_lift_tower.paths import (
    EvaluationPaths,
)
from big_boy_benchmarking.environments.warehouse_gridlock.masked_direct_vs_live_lift_tower.readiness_source import (
    ReadinessSource,
)
from big_boy_benchmarking.upstream.state_collapser import (
    collect_state_collapser_dependency_state,
)


def write_initial_manifests(
    *,
    paths: EvaluationPaths,
    config: MaskedDirectVsLiveLiftConfig,
    instance: WarehouseGridlockInstance,
    readiness_source: ReadinessSource,
) -> dict[str, str]:
    manifests: dict[str, Path] = {
        "evaluation_manifest": paths.evaluation_manifest,
        "evaluation_budget_lock": paths.evaluation_budget_lock,
        "evaluation_input_manifest": paths.evaluation_input_manifest,
        "dependency_manifest": paths.dependency_manifest,
        "arm_manifest": paths.arm_manifest,
        "candidate_generation_manifest": paths.candidate_generation_manifest,
        "admissibility_policy_manifest": paths.admissibility_policy_manifest,
        "live_lift_policy_manifest": paths.live_lift_policy_manifest,
        "no_lookahead_policy_manifest": paths.no_lookahead_policy_manifest,
        "tower_construction_manifest": paths.tower_construction_manifest,
        "tower_surface_scope_manifest": paths.tower_surface_scope_manifest,
    }
    write_json(
        paths.evaluation_manifest,
        {
            "artifact_schema_version": ARTIFACT_SCHEMA_VERSION_ID,
            "evaluation_id": EVALUATION_ID,
            "run_label": config.run_label,
            "run_mode": config.run_mode,
            "claim_boundary": [
                "diagnostic smoke/calibration evidence only",
                "no one-step successor-state cul-de-sac lookahead for either arm",
                "tower live state-lift hygiene only",
                "candidate-set masks, not full action-space masks",
            ],
        },
        create_parents=True,
    )
    write_json(paths.evaluation_budget_lock, config.to_manifest(), create_parents=True)
    write_json(
        paths.evaluation_input_manifest,
        {
            "artifact_schema_version": ARTIFACT_SCHEMA_VERSION_ID,
            "evaluation_id": EVALUATION_ID,
            "readiness_source": str(readiness_source.path),
            "readiness_source_payload_keys": sorted(readiness_source.payload),
            "environment_instance_id": instance.manifest.instance_id,
            "environment_family_id": config.environment_family_id,
            "robot_count": len(instance.manifest.robot_ids),
            "box_count": len(instance.manifest.box_ids),
            "traversable_node_count": len(instance.graph.nodes - instance.graph.blocked_nodes),
            "directed_edge_count": len(instance.graph.edges),
            "source_design_docs": [
                "docs/design/svg_physical_system_designs/warehouse_gridlock_001/warehouse_001.md",
                "docs/design/svg_physical_system_designs/warehouse_gridlock_001/01_001_warehouse_gridlock_environment_blueprint.md",
            ],
        },
        create_parents=True,
    )
    dependency_state = collect_state_collapser_dependency_state().to_dict()
    write_json(paths.dependency_manifest, dependency_state, create_parents=True)
    write_json(
        paths.arm_manifest,
        {"artifact_schema_version": ARTIFACT_SCHEMA_VERSION_ID, "arms": arm_manifest_rows()},
        create_parents=True,
    )
    write_json(
        paths.candidate_generation_manifest,
        {
            "artifact_schema_version": ARTIFACT_SCHEMA_VERSION_ID,
            "policies": [
                {
                    "policy_id": DIRECT_CANDIDATE_POLICY_ID,
                    "arm_id": "warehouse_direct_admissible_masked",
                    "scope": "coordination_ready_sparse_generated_candidate_set",
                    "candidate_mix_id": config.candidate_mix_id,
                    "candidate_proposals_per_step": config.candidate_proposals_per_step,
                    "max_active_robots": config.max_active_robots,
                    "family_schedule": [
                        "all_stay",
                        "one_active",
                        "two_active",
                        "three_or_more_active_when_enabled",
                    ],
                    "complete_full_action_surface": False,
                },
                {
                    "policy_id": TOWER_CANDIDATE_POLICY_ID,
                    "arm_id": "warehouse_tower_live_lift_masked",
                    "scope": "bounded_tower_candidate_set",
                    "candidate_mix_id": config.candidate_mix_id,
                    "candidate_proposals_per_step": config.candidate_proposals_per_step,
                    "max_active_robots": config.max_active_robots,
                    "complete_full_action_surface": False,
                },
            ],
        },
        create_parents=True,
    )
    write_json(
        paths.admissibility_policy_manifest,
        {
            "artifact_schema_version": ARTIFACT_SCHEMA_VERSION_ID,
            "policies": [
                {
                    "policy_id": DIRECT_MASK_POLICY_ID,
                    "mask_scope": "candidate_set",
                    "immediate_admissibility_only": True,
                },
                {
                    "policy_id": TOWER_MASK_POLICY_ID,
                    "mask_scope": "candidate_set",
                    "immediate_admissibility_only": True,
                },
            ],
        },
        create_parents=True,
    )
    write_json(
        paths.live_lift_policy_manifest,
        {
            "artifact_schema_version": ARTIFACT_SCHEMA_VERSION_ID,
            "policy_id": LIVE_LIFT_POLICY_ID,
            "rule": "pr(s') = s and Out_generated(s') != empty",
            "not_action_successor_lookahead": True,
        },
        create_parents=True,
    )
    write_json(paths.no_lookahead_policy_manifest, no_lookahead_policy_manifest(), create_parents=True)
    write_json(
        paths.tower_construction_manifest,
        {
            "artifact_schema_version": ARTIFACT_SCHEMA_VERSION_ID,
            "schema_id": TOWER_SCHEMA_ID,
            "surface_generation_policy_id": TOWER_SURFACE_POLICY_ID,
            "surface_scope": "generated_discovered_surface",
            "complete_full_action_surface": False,
            "ratio_numerator": config.ratio_numerator,
            "ratio_denominator": config.ratio_denominator,
        },
        create_parents=True,
    )
    write_json(
        paths.tower_surface_scope_manifest,
        {
            "artifact_schema_version": ARTIFACT_SCHEMA_VERSION_ID,
            "surface_generation_policy_id": TOWER_SURFACE_POLICY_ID,
            "surface_scope": "generated_discovered_surface",
            "full_action_surface": "not_enumerated",
            "flat_action_count_expression": f"5^{len(instance.manifest.robot_ids)}",
            "candidate_mix_id": config.candidate_mix_id,
            "candidate_proposals_per_step": config.candidate_proposals_per_step,
            "max_active_robots": config.max_active_robots,
        },
        create_parents=True,
    )
    return {name: str(path) for name, path in manifests.items()}


def write_run_manifest(path: Path, payload: dict[str, Any]) -> None:
    write_json(path, {"artifact_schema_version": ARTIFACT_SCHEMA_VERSION_ID, **payload}, create_parents=True)
