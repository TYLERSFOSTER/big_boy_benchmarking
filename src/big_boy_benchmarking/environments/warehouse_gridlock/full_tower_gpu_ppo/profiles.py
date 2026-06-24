"""Named profiles for Warehouse full-tower PPO runs."""

from __future__ import annotations

from pathlib import Path

from .config import (
    WarehouseCheckpointConfig,
    WarehouseDeviceConfig,
    WarehouseFullTowerPPOConfig,
    WarehousePPOHyperparameters,
    WarehousePolicyCapacityConfig,
    WarehouseRetentionConfig,
)


def apply_profile(
    *,
    profile_id: str,
    repo_root: Path,
    artifact_root: Path,
    readiness_source: Path,
    run_label: str,
    locked_by: str,
    episodes_per_arm: int | None = None,
    replicates_per_arm: int | None = None,
    schema_seeds: int | None = None,
    max_seconds_per_episode: int | None = None,
    device: str | None = None,
    confirm_long_run: bool = False,
) -> WarehouseFullTowerPPOConfig:
    if profile_id == "smoke_cpu":
        return WarehouseFullTowerPPOConfig(
            repo_root=repo_root,
            artifact_root=artifact_root,
            readiness_source=readiness_source,
            run_label=run_label,
            locked_by=locked_by,
            episodes_per_arm=episodes_per_arm or 2,
            replicates_per_arm=replicates_per_arm or 1,
            schema_seeds=schema_seeds or 1,
            max_seconds_per_episode=max_seconds_per_episode or 8,
            candidate_proposals_per_step=24,
            ppo=WarehousePPOHyperparameters(update_interval_samples=4, minibatch_size=8),
            capacity=WarehousePolicyCapacityConfig(capacity_0=64, min_capacity=32),
            device=WarehouseDeviceConfig(device=device or "cpu"),
            retention=WarehouseRetentionConfig(profile_id="smoke_debug"),
            checkpoint=WarehouseCheckpointConfig(checkpoint_every_updates=1),
            profile_id=profile_id,
            progress_every_episodes=1,
        )
    if profile_id == "debug_gpu":
        return WarehouseFullTowerPPOConfig(
            repo_root=repo_root,
            artifact_root=artifact_root,
            readiness_source=readiness_source,
            run_label=run_label,
            locked_by=locked_by,
            episodes_per_arm=episodes_per_arm or 8,
            replicates_per_arm=replicates_per_arm or 1,
            schema_seeds=schema_seeds or 1,
            max_seconds_per_episode=max_seconds_per_episode or 32,
            candidate_proposals_per_step=64,
            ppo=WarehousePPOHyperparameters(update_interval_samples=16, minibatch_size=16),
            capacity=WarehousePolicyCapacityConfig(capacity_0=128, min_capacity=48),
            device=WarehouseDeviceConfig(device=device or "cuda"),
            retention=WarehouseRetentionConfig(profile_id="smoke_debug"),
            checkpoint=WarehouseCheckpointConfig(checkpoint_every_updates=1),
            profile_id=profile_id,
            progress_every_episodes=1,
        )
    if profile_id == "serious_gpu":
        return WarehouseFullTowerPPOConfig(
            repo_root=repo_root,
            artifact_root=artifact_root,
            readiness_source=readiness_source,
            run_label=run_label,
            locked_by=locked_by,
            episodes_per_arm=episodes_per_arm or 1024,
            replicates_per_arm=replicates_per_arm or 1,
            schema_seeds=schema_seeds or 1,
            max_seconds_per_episode=max_seconds_per_episode or 64,
            candidate_proposals_per_step=128,
            ppo=WarehousePPOHyperparameters(update_interval_samples=128, minibatch_size=64),
            capacity=WarehousePolicyCapacityConfig(capacity_0=192, min_capacity=64),
            device=WarehouseDeviceConfig(device=device or "cuda"),
            retention=WarehouseRetentionConfig(profile_id="serious_train"),
            checkpoint=WarehouseCheckpointConfig(checkpoint_every_updates=1),
            profile_id=profile_id,
            progress_every_episodes=1,
            confirm_long_run=confirm_long_run,
        )
    raise ValueError(f"unknown full-tower PPO profile: {profile_id!r}")
