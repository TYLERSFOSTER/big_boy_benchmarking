"""Configuration for PlateSupport gauntlet Stage 6 paired replicate comparison."""

from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path

from ..ids import LINEARIZATION_MODE_ID
from ..paths import suite_artifact_root, suite_readout_surface


@dataclass(frozen=True)
class PairedReplicateComparisonConfig:
    """Explicit runtime context for Stage 6."""

    artifact_root: Path
    run_label: str
    candidate_source_path: Path
    training_health_source_path: Path
    threshold_source_path: Path
    locked_by: str
    structural_source_path: Path | None = None
    candidate_cap: int = 1
    allow_warning_candidates: bool = False
    allow_legacy_dependency: bool = False
    episodes_per_replicate: int | None = None
    replicates_per_arm: int | None = None
    max_steps_per_episode: int = 50
    base_seed: int = 0
    learning_rate: float = 0.25
    discount: float = 0.95
    epsilon: float = 0.20
    include_direct_baseline: bool = True
    include_no_contraction_control: bool = True
    linearization_mode_id: str = LINEARIZATION_MODE_ID

    def __post_init__(self) -> None:
        if self.candidate_cap <= 0:
            raise ValueError("candidate_cap must be positive")
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


def default_paired_replicate_comparison_config(
    *,
    repo_root: Path | str,
    run_label: str = "smoke_001",
    locked_by: str = "cli",
) -> PairedReplicateComparisonConfig:
    """Build default Stage 6 config from explicit gauntlet paths."""

    surface = suite_readout_surface(repo_root)
    return PairedReplicateComparisonConfig(
        artifact_root=suite_artifact_root(repo_root, run_label),
        run_label=run_label,
        candidate_source_path=surface / "candidate_discovery" / "readout_source.json",
        training_health_source_path=surface / "tower_training_health" / "readout_source.json",
        threshold_source_path=surface / "threshold_frontier_calibration" / "readout_source.json",
        locked_by=locked_by,
    )
