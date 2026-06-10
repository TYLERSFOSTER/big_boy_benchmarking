"""Manifest helpers for the Warehouse full-state policy comparison."""

from __future__ import annotations

from pathlib import Path

from big_boy_benchmarking.artifacts.writers import write_json
from big_boy_benchmarking.environments.warehouse_gridlock.full_state_policy_comparison.config import (
    ACTIVE_ARM_IDS,
    DIRECT_ARM_ID,
    EVALUATION_ID,
    TOWER_ARM_ID,
    FullStatePolicyComparisonConfig,
)
from big_boy_benchmarking.environments.warehouse_gridlock.full_state_policy_comparison.paths import (
    EvaluationPaths,
)
from big_boy_benchmarking.environments.warehouse_gridlock.instances import (
    WarehouseGridlockInstance,
)
from big_boy_benchmarking.environments.warehouse_gridlock.masked_direct_vs_live_lift_tower.config import (
    LIVE_LIFT_POLICY_ID,
    TOWER_SCHEMA_ID,
    TOWER_SURFACE_POLICY_ID,
)
from big_boy_benchmarking.environments.warehouse_gridlock.masked_direct_vs_live_lift_tower.readiness_source import (
    ReadinessSource,
)
from big_boy_benchmarking.environments.warehouse_gridlock.policies import (
    MODEL_FAMILY_ID,
    POLICY_CONTRACT_ID,
    PROJECTION_STRATEGY_ID,
)


def write_initial_manifests(
    *,
    paths: EvaluationPaths,
    config: FullStatePolicyComparisonConfig,
    instance: WarehouseGridlockInstance,
    readiness_source: ReadinessSource,
) -> dict[str, str]:
    manifest_paths: dict[str, Path] = {
        "evaluation_manifest": paths.evaluation_manifest,
        "evaluation_budget_lock": paths.evaluation_budget_lock,
        "evaluation_arm_manifest": paths.evaluation_arm_manifest,
        "environment_instance_manifest": paths.environment_instance_manifest,
        "policy_contract_manifest": paths.policy_contract_manifest,
        "policy_model_manifest": paths.policy_model_manifest,
        "policy_training_manifest": paths.policy_training_manifest,
        "admissibility_resolver_manifest": paths.admissibility_resolver_manifest,
        "tower_policy_manifest": paths.tower_policy_manifest,
        "tower_construction_manifest": paths.tower_construction_manifest,
    }
    write_json(
        paths.evaluation_manifest,
        {
            "artifact_schema_version": config.to_manifest()["artifact_schema_version"],
            "evaluation_id": EVALUATION_ID,
            "run_label": config.run_label,
            "run_mode": config.run_mode,
            "claim_boundary": [
                "trainable policy contract smoke/pilot evidence only",
                "no broad Warehouse benchmark claim",
                "no backprop claim",
                "immediate inadmissibility masking for both arms",
                "no one-hop successor-state cul-de-sac lookahead",
                "tower live state-lift hygiene only",
            ],
        },
        create_parents=True,
    )
    write_json(paths.evaluation_budget_lock, config.to_manifest(), create_parents=True)
    write_json(
        paths.evaluation_arm_manifest,
        {
            "evaluation_id": EVALUATION_ID,
            "arms": [
                {
                    "arm_id": DIRECT_ARM_ID,
                    "label": "Direct full-state trainable policy",
                    "policy_contract_id": POLICY_CONTRACT_ID,
                    "model_family_id": MODEL_FAMILY_ID,
                    "uses_tower": False,
                    "immediate_admissibility_masked": True,
                    "one_step_successor_lookahead": False,
                },
                {
                    "arm_id": TOWER_ARM_ID,
                    "label": "Tower full-state trainable policy with live lift",
                    "policy_contract_id": POLICY_CONTRACT_ID,
                    "model_family_id": MODEL_FAMILY_ID,
                    "uses_tower": True,
                    "immediate_admissibility_masked": True,
                    "live_state_lift_hygiene": True,
                    "one_step_successor_lookahead": False,
                },
            ],
        },
        create_parents=True,
    )
    write_json(
        paths.environment_instance_manifest,
        {
            "evaluation_id": EVALUATION_ID,
            "readiness_source": str(readiness_source.path),
            "environment_instance_id": instance.manifest.instance_id,
            "environment_family_id": config.environment_family_id,
            "robot_count": len(instance.manifest.robot_ids),
            "box_count": len(instance.manifest.box_ids),
            "traversable_node_count": len(instance.graph.nodes - instance.graph.blocked_nodes),
            "directed_edge_count": len(instance.graph.edges),
            "reward_policy": instance.manifest.reward_policy.to_dict(),
        },
        create_parents=True,
    )
    write_json(
        paths.policy_contract_manifest,
        {
            "policy_contract_id": POLICY_CONTRACT_ID,
            "input": "full system configuration plus current second",
            "output": "full simultaneous Warehouse action vector",
            "active_arm_ids": list(ACTIVE_ARM_IDS),
            "not_candidate_id_learning": True,
        },
        create_parents=True,
    )
    write_json(
        paths.policy_model_manifest,
        {
            "model_family_id": MODEL_FAMILY_ID,
            "model_class": "linear_factorized_softmax",
            "neural_or_backprop": False,
            "feature_weight_learning": True,
        },
        create_parents=True,
    )
    write_json(
        paths.policy_training_manifest,
        {
            "model_family_id": MODEL_FAMILY_ID,
            "learning_rate": config.learning_rate,
            "baseline_rate": config.baseline_rate,
            "temperature_initial": config.temperature_initial,
            "temperature_floor": config.temperature_floor,
            "temperature_decay_per_episode": config.temperature_decay_per_episode,
            "progress_signal": "delta_correct_robot_count + 2.0 * delta_correct_box_count",
            "policy_parameters_persist_across_episodes": True,
            "policy_parameters_reset_between_replicates": True,
        },
        create_parents=True,
    )
    write_json(
        paths.admissibility_resolver_manifest,
        {
            "projection_strategy_id": PROJECTION_STRATEGY_ID,
            "projection_attempt_budget": config.projection_attempt_budget,
            "immediate_admissibility_only": True,
            "uses_successor_out_for_selection": False,
            "fallback": "all_stay",
        },
        create_parents=True,
    )
    write_json(
        paths.tower_policy_manifest,
        {
            "arm_id": TOWER_ARM_ID,
            "policy_namespace": "arm_id,tier_id,model_family_id",
            "live_lift_policy_id": LIVE_LIFT_POLICY_ID,
            "model_family_id": MODEL_FAMILY_ID,
            "learning_key_surface": "feature_weights_not_candidate_ids",
        },
        create_parents=True,
    )
    write_json(
        paths.tower_construction_manifest,
        {
            "schema_id": TOWER_SCHEMA_ID,
            "surface_generation_policy_id": TOWER_SURFACE_POLICY_ID,
            "surface_scope": "generated_discovered_surface",
            "complete_full_action_surface": False,
            "flat_action_count_expression": f"5^{len(instance.manifest.robot_ids)}",
            "candidate_proposals_per_step": config.candidate_proposals_per_step,
            "max_active_robots": config.max_active_robots,
            "candidate_mix_id": config.candidate_mix_id,
        },
        create_parents=True,
    )
    return {name: str(path) for name, path in manifest_paths.items()}


def write_run_manifest(path: Path, payload: dict[str, object]) -> None:
    write_json(path, {"evaluation_id": EVALUATION_ID, **payload}, create_parents=True)
