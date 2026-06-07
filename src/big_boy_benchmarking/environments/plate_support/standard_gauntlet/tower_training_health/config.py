"""Configuration for PlateSupport gauntlet Stage 4 tower training health."""

from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path

from ..ids import (
    LINEARIZATION_MODE_ID,
)
from ..paths import (
    suite_artifact_root,
    suite_readout_surface,
)


@dataclass(frozen=True)
class TowerTrainingHealthConfig:
    """Explicit runtime context for Stage 4 tower training health."""

    artifact_root: Path
    run_label: str
    candidate_source_path: Path
    locked_by: str
    candidate_cap: int = 2
    training_replicates_per_candidate: int = 2
    episodes_per_replicate: int = 16
    max_steps_per_episode: int = 50
    base_seed: int = 0
    allow_warning_candidates: bool = False
    learning_rate: float = 0.25
    discount: float = 0.95
    epsilon: float = 0.20
    linearization_mode_id: str = LINEARIZATION_MODE_ID

    def __post_init__(self) -> None:
        if self.candidate_cap <= 0:
            raise ValueError("candidate_cap must be positive")
        if self.training_replicates_per_candidate <= 0:
            raise ValueError("training_replicates_per_candidate must be positive")
        if self.episodes_per_replicate <= 0:
            raise ValueError("episodes_per_replicate must be positive")
        if self.max_steps_per_episode <= 0:
            raise ValueError("max_steps_per_episode must be positive")
        if not 0.0 <= self.learning_rate <= 1.0:
            raise ValueError("learning_rate must be in [0, 1]")
        if not 0.0 <= self.discount <= 1.0:
            raise ValueError("discount must be in [0, 1]")
        if not 0.0 <= self.epsilon <= 1.0:
            raise ValueError("epsilon must be in [0, 1]")


def default_tower_training_health_config(
    *,
    repo_root: Path | str,
    run_label: str = "smoke_001",
    locked_by: str = "cli",
) -> TowerTrainingHealthConfig:
    """Build default Stage 4 config from explicit architecture paths."""

    return TowerTrainingHealthConfig(
        artifact_root=suite_artifact_root(repo_root, run_label),
        run_label=run_label,
        candidate_source_path=(
            suite_readout_surface(repo_root)
            / "candidate_discovery"
            / "readout_source.json"
        ),
        locked_by=locked_by,
    )
