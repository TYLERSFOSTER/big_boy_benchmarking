"""Manifest writers for Warehouse full-tower PPO."""

from __future__ import annotations

import importlib.metadata as metadata
import sys
from pathlib import Path
from typing import Any

from big_boy_benchmarking.artifacts.writers import write_json

from .config import WarehouseFullTowerPPOConfig
from .ids import (
    WAREHOUSE_GRIDLOCK_FULL_TOWER_GPU_PPO_ARTIFACT_CONTRACT_ID,
    WAREHOUSE_GRIDLOCK_POINTWISE_LIFTABILITY_SEMANTICS_ID,
    WAREHOUSE_GRIDLOCK_SOURCE_AUTHORITY_FILES,
)
from .paths import FullTowerPPOPaths
from .schema_arms import schema_manifest_for_arm
from .tokenization import tokenization_manifest


def write_initial_manifests(
    *,
    paths: FullTowerPPOPaths,
    config: WarehouseFullTowerPPOConfig,
    actual_device: str,
) -> dict[str, str]:
    payloads: dict[str, dict[str, Any]] = {
        "evaluation_manifest": {
            "evaluation_id": config.evaluation_id,
            "artifact_contract_id": WAREHOUSE_GRIDLOCK_FULL_TOWER_GPU_PPO_ARTIFACT_CONTRACT_ID,
            "claim_boundary": [
                "full-tower GPU PPO system readiness evidence",
                "not a final broad Warehouse benchmark claim",
            ],
            "source_authority_files": list(WAREHOUSE_GRIDLOCK_SOURCE_AUTHORITY_FILES),
        },
        "evaluation_budget_lock": config.to_manifest(),
        "schema_arm_manifest": {
            "arms": [
                schema_manifest_for_arm(arm, schema_seed=0)
                for arm in config.active_arms()
            ],
        },
        "device_manifest": {
            "requested_device": config.device.device,
            "actual_device": actual_device,
            "dtype": config.device.dtype,
            "mixed_precision": config.device.mixed_precision,
            "torch_version": _version("torch"),
            "cuda_available": _cuda_available(),
        },
        "dependency_manifest": {
            "python_version": sys.version,
            "state_collapser_version": _version("state_collapser"),
            "torch_version": _version("torch"),
            "tqdm_version": _version("tqdm"),
        },
        "state_collapser_runtime_manifest": {
            "runtime_surface": "PartitionTower",
            "pointwise_liftability_semantics_id": WAREHOUSE_GRIDLOCK_POINTWISE_LIFTABILITY_SEMANTICS_ID,
            "required_methods": [
                "current_state_cell",
                "current_position_at_every_tier",
                "outgoing_action_cells",
                "representative_edges",
                "executable_lift_candidates",
                "executable_action_cells",
                "tier_is_executable_from_state",
            ],
            "representative_fallback_for_execution": False,
        },
        "record_schema_manifest": {
            "geometry_records_exclude_mutable_rollout_fields": True,
            "decision_context_mask_kind": "pointwise_executable",
            "rollout_samples_store_old_log_prob": True,
        },
        "tokenization_manifest": tokenization_manifest(),
        "retention_manifest": config.retention.to_manifest(),
    }
    outputs = {
        "evaluation_manifest": paths.evaluation_manifest,
        "evaluation_budget_lock": paths.evaluation_budget_lock,
        "schema_arm_manifest": paths.artifact_root / "schema_arm_manifest.json",
        "device_manifest": paths.artifact_root / "device_manifest.json",
        "dependency_manifest": paths.artifact_root / "dependency_manifest.json",
        "state_collapser_runtime_manifest": paths.artifact_root
        / "state_collapser_runtime_manifest.json",
        "record_schema_manifest": paths.artifact_root / "record_schema_manifest.json",
        "tokenization_manifest": paths.artifact_root / "tokenization_manifest.json",
        "retention_manifest": paths.artifact_root / "retention_manifest.json",
    }
    for key, path in outputs.items():
        write_json(path, payloads[key], create_parents=True)
    return {key: str(path) for key, path in outputs.items()}


def _version(package: str) -> str:
    try:
        return metadata.version(package)
    except metadata.PackageNotFoundError:
        return "not_installed"


def _cuda_available() -> bool:
    try:
        import torch

        return bool(torch.cuda.is_available())
    except Exception:
        return False
