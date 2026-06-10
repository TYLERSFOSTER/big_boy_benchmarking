"""Configuration for the Warehouse masked direct/live-lift tower diagnostic."""

from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path

from big_boy_benchmarking.artifacts.schemas import ARTIFACT_SCHEMA_VERSION
from big_boy_benchmarking.environments.warehouse_gridlock.ids import (
    WAREHOUSE_GRIDLOCK_ENVIRONMENT_FAMILY_ID,
    WAREHOUSE_GRIDLOCK_FULL_INSTANCE_ID,
)

EVALUATION_ID = "warehouse_gridlock_masked_direct_vs_live_lift_tower_no_lookahead_v001"
RUN_FAMILY_ID = EVALUATION_ID
ARTIFACT_SCHEMA_VERSION_ID = ARTIFACT_SCHEMA_VERSION

DIRECT_ARM_ID = "warehouse_direct_admissible_masked"
TOWER_ARM_ID = "warehouse_tower_live_lift_masked"
ACTIVE_ARM_IDS = (DIRECT_ARM_ID, TOWER_ARM_ID)

DIRECT_CANDIDATE_POLICY_ID = "warehouse_coordination_ready_sparse_ensemble_candidate_generator_v001"
TOWER_CANDIDATE_POLICY_ID = "warehouse_bounded_tower_candidate_generator_v001"
DIRECT_MASK_POLICY_ID = "warehouse_direct_candidate_admissibility_mask_v001"
TOWER_MASK_POLICY_ID = "warehouse_tower_current_action_admissibility_mask_v001"
LIVE_LIFT_POLICY_ID = "warehouse_tower_live_state_lift_only_v001"
NO_LOOKAHEAD_POLICY_ID = "warehouse_no_successor_out_selection_v001"
TOWER_SURFACE_POLICY_ID = "warehouse_generated_discovered_surface_v001"
TOWER_SCHEMA_ID = "warehouse_source_local_ratio_iterated_v001"
CONTROLLER_POLICY_ID = "warehouse_seeded_first_nonstay_valid_candidate_v001"
CANDIDATE_MIX_COORDINATION_READY = "coordination_ready_sparse_interleaved_v001"

DEFAULT_RUN_LABEL = "smoke_001"
DEFAULT_EPISODES_PER_ARM = 2
DEFAULT_REPLICATES_PER_ARM = 1
DEFAULT_MAX_SECONDS_PER_EPISODE = 32
DEFAULT_CANDIDATE_PROPOSALS_PER_STEP = 64
DEFAULT_MAX_ACTIVE_ROBOTS = 3
DEFAULT_SCHEMA_SEEDS = 1
DEFAULT_SEED = 0
DEFAULT_RATIO_NUMERATOR = 9
DEFAULT_RATIO_DENOMINATOR = 10


@dataclass(frozen=True)
class MaskedDirectVsLiveLiftConfig:
    """Runtime config for one Warehouse diagnostic run."""

    repo_root: Path
    artifact_root: Path
    readiness_source: Path
    run_label: str = DEFAULT_RUN_LABEL
    locked_by: str = "unknown"
    instance_id: str = WAREHOUSE_GRIDLOCK_FULL_INSTANCE_ID
    environment_family_id: str = WAREHOUSE_GRIDLOCK_ENVIRONMENT_FAMILY_ID
    episodes_per_arm: int = DEFAULT_EPISODES_PER_ARM
    replicates_per_arm: int = DEFAULT_REPLICATES_PER_ARM
    max_seconds_per_episode: int = DEFAULT_MAX_SECONDS_PER_EPISODE
    candidate_proposals_per_step: int = DEFAULT_CANDIDATE_PROPOSALS_PER_STEP
    max_active_robots: int = DEFAULT_MAX_ACTIVE_ROBOTS
    candidate_mix_id: str = CANDIDATE_MIX_COORDINATION_READY
    schema_seeds: int = DEFAULT_SCHEMA_SEEDS
    seed: int = DEFAULT_SEED
    smoke: bool = False
    ratio_numerator: int = DEFAULT_RATIO_NUMERATOR
    ratio_denominator: int = DEFAULT_RATIO_DENOMINATOR

    @property
    def run_mode(self) -> str:
        return "smoke" if self.smoke or self.run_label.startswith("smoke") else "diagnostic"

    def to_manifest(self) -> dict[str, object]:
        return {
            "artifact_schema_version": ARTIFACT_SCHEMA_VERSION_ID,
            "evaluation_id": EVALUATION_ID,
            "run_label": self.run_label,
            "run_mode": self.run_mode,
            "locked_by": self.locked_by,
            "instance_id": self.instance_id,
            "environment_family_id": self.environment_family_id,
            "episodes_per_arm": self.episodes_per_arm,
            "replicates_per_arm": self.replicates_per_arm,
            "max_seconds_per_episode": self.max_seconds_per_episode,
            "candidate_proposals_per_step": self.candidate_proposals_per_step,
            "max_active_robots": self.max_active_robots,
            "candidate_mix_id": self.candidate_mix_id,
            "schema_seeds": self.schema_seeds,
            "seed": self.seed,
            "ratio_numerator": self.ratio_numerator,
            "ratio_denominator": self.ratio_denominator,
            "active_arm_ids": list(ACTIVE_ARM_IDS),
            "no_lookahead_policy_id": NO_LOOKAHEAD_POLICY_ID,
        }
