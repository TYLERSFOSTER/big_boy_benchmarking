"""Configuration for the PlateSupport tower-star guarded lift diagnostic."""

from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path

TOWER_STAR_GUARDED_LIFT_COMPARISON_EVALUATION_ID = (
    "plate_support_tower_star_guarded_lift_comparison_v001"
)
ENVIRONMENT_FAMILY_ID = "plate_support"
ENVIRONMENT_INSTANCE_ID = "plate_support_5x5_default_v001"

DIRECT_RAW_ARM_ID = "direct_raw"
DIRECT_INVALID_GUARD_ARM_ID = "direct_invalid_guard"
DIRECT_NONSELF_GUARD_ARM_ID = "direct_nonself_guard"
TOWER_LIFT_EXECUTABLE_CURRENT_ARM_ID = "tower_lift_executable_current"
TOWER_INVALID_GUARD_ARM_ID = "tower_invalid_guard"
TOWER_NONSELF_GUARD_ARM_ID = "tower_nonself_guard"

RAW_GUARD = "raw"
CURRENT_LIFT_EXECUTABLE_GUARD = "current_lift_executable"
INVALID_GUARD = "invalid_guard"
NONSELF_GUARD = "nonself_guard"
ORACLE_ONE_STEP_INFORMATION_MODE = "oracle_one_step_local_transition"

DEFAULT_EPISODES_PER_REPLICATE = 32
DEFAULT_REPLICATES_PER_ARM = 4
SMOKE_EPISODES_PER_REPLICATE = 2
SMOKE_REPLICATES_PER_ARM = 1

CLAIM_BOUNDARY = (
    "diagnostic tower-star smoke/calibration evidence only; not a final "
    "robotics benchmark claim"
)


@dataclass(frozen=True)
class TowerStarGuardedLiftComparisonConfig:
    """Explicit runtime context for the tower-star diagnostic."""

    repo_root: Path
    artifact_root: Path
    parent_gauntlet_source: Path
    direct_star_source: Path
    run_label: str
    locked_by: str
    episodes_per_replicate: int | None = None
    replicates_per_arm: int | None = None
    max_steps_per_episode: int = 50
    base_seed: int = 0
    learning_rate: float = 0.25
    discount: float = 0.95
    epsilon: float = 0.20
    smoke: bool = False

    def __post_init__(self) -> None:
        if self.episodes_per_replicate is not None and self.episodes_per_replicate <= 0:
            raise ValueError("episodes_per_replicate must be positive when provided")
        if self.replicates_per_arm is not None and self.replicates_per_arm <= 0:
            raise ValueError("replicates_per_arm must be positive when provided")
        if self.max_steps_per_episode <= 0:
            raise ValueError("max_steps_per_episode must be positive")
        if not 0.0 <= self.learning_rate <= 1.0:
            raise ValueError("learning_rate must be in [0, 1]")
        if not 0.0 <= self.discount <= 1.0:
            raise ValueError("discount must be in [0, 1]")
        if not 0.0 <= self.epsilon <= 1.0:
            raise ValueError("epsilon must be in [0, 1]")

    def resolved_episodes_per_replicate(self, parent_default: int | None = None) -> int:
        if self.episodes_per_replicate is not None:
            return self.episodes_per_replicate
        if self.smoke:
            return SMOKE_EPISODES_PER_REPLICATE
        if parent_default is not None and parent_default > 0:
            return parent_default
        return DEFAULT_EPISODES_PER_REPLICATE

    def resolved_replicates_per_arm(self, parent_default: int | None = None) -> int:
        if self.replicates_per_arm is not None:
            return self.replicates_per_arm
        if self.smoke:
            return SMOKE_REPLICATES_PER_ARM
        if parent_default is not None and parent_default > 0:
            return parent_default
        return DEFAULT_REPLICATES_PER_ARM
