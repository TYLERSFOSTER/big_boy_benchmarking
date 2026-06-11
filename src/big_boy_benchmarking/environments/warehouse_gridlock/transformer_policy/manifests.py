"""Manifest writers for Warehouse transformer policy runs."""

from __future__ import annotations

import platform
from typing import Any

from big_boy_benchmarking.artifacts.writers import write_json

from ..instances import WarehouseGridlockInstance
from .config import (
    DIRECT_ARM_ID,
    MODEL_FAMILY_ID,
    POLICY_CONTRACT_ID,
    TOWER_ARM_ID,
    WarehouseTransformerPolicyRunConfig,
)
from .model import parameter_count
from .paths import TransformerEvaluationPaths
from .torch_runtime import (
    TorchRuntimeInfo,
)


def write_initial_manifests(
    *,
    paths: TransformerEvaluationPaths,
    config: WarehouseTransformerPolicyRunConfig,
    instance: WarehouseGridlockInstance,
    model: Any,
    runtime: TorchRuntimeInfo,
) -> dict[str, str]:
    manifests = {
        paths.evaluation_manifest: {
            **config.to_manifest(),
            "claim_boundary": [
                "transformer policy training surface smoke/diagnostic evidence only",
                "no one-hop successor-Out lookahead",
                "selected-trace artifact retention by default",
            ],
        },
        paths.evaluation_budget_lock: {
            "locked_by": config.locked_by,
            "episodes": config.episodes,
            "replicates": config.replicates,
            "schema_seeds": config.schema_seeds,
            "checkpoint_every_episodes": config.checkpoint.checkpoint_every_episodes,
            "trace_retention": config.trace_retention.to_manifest(),
        },
        paths.environment_instance_manifest: instance.manifest.to_dict(),
        paths.policy_contract_manifest: {
            "policy_contract_id": POLICY_CONTRACT_ID,
            "input_contract": "full Warehouse system config plus current second",
            "output_contract": "full simultaneous robot action vector",
            "direct_arm_context_boundary": "no tower context",
            "tower_live_lift_boundary": "state-lift liveness hygiene only",
            "successor_out_count_used_for_selection": False,
            "arms": [TOWER_ARM_ID, DIRECT_ARM_ID],
        },
        paths.transformer_model_manifest: {
            "model_family_id": MODEL_FAMILY_ID,
            "model": config.model.to_manifest(),
            "parameter_count": parameter_count(model),
            "token_vocabulary": {
                "global": 0,
                "robot": 1,
                "box": 2,
                "blocked_column": 3,
                "tower_context": 4,
            },
            "primitive_action_vocabulary": ["stay", "north", "south", "west", "east"],
        },
        paths.optimizer_manifest: {
            "model_family_id": MODEL_FAMILY_ID,
            "optimizer": config.optimizer.to_manifest(),
        },
        paths.curriculum_manifest: config.curriculum.to_manifest(),
        paths.trace_retention_manifest: config.trace_retention.to_manifest(),
        paths.dependency_manifest: {
            "python_version": platform.python_version(),
            "torch": runtime.to_manifest(),
            "state_collapser_expected": (
                "v0.7.2 or newer compatible pointwise liftability semantics"
            ),
        },
    }
    output: dict[str, str] = {}
    for path, payload in manifests.items():
        write_json(path, payload, create_parents=True)
        output[path.name] = str(path)
    return output
