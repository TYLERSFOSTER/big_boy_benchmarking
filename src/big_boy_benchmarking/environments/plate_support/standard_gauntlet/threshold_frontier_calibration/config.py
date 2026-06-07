"""Configuration for PlateSupport gauntlet Stage 5 threshold calibration."""

from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path

from ..ids import LINEARIZATION_MODE_ID
from ..paths import suite_artifact_root, suite_readout_surface

DEFAULT_TARGET_TYPES = (
    "binary_success",
    "first_hit",
    "sustained_hit",
    "return_threshold",
)

DEFAULT_SUSTAINED_WINDOWS = (
    (1, 4),
    (2, 8),
    (4, 16),
    (4, 5),
)

DEFAULT_THRESHOLD_QUANTILES = (0.0, 0.25, 0.5, 0.75, 0.9, 1.0)


@dataclass(frozen=True)
class ThresholdFrontierCalibrationConfig:
    """Explicit runtime context for Stage 5 threshold calibration."""

    artifact_root: Path
    run_label: str
    training_health_source_path: Path
    locked_by: str
    stage1_source_path: Path | None = None
    candidate_cap: int = 1
    allow_warning_candidates: bool = False
    calibration_arms: tuple[str, ...] = ("selected_trainable_candidate",)
    target_types: tuple[str, ...] = DEFAULT_TARGET_TYPES
    sustained_windows: tuple[tuple[int, int], ...] = DEFAULT_SUSTAINED_WINDOWS
    threshold_quantiles: tuple[float, ...] = DEFAULT_THRESHOLD_QUANTILES
    recommended_episodes_per_replicate: int = 32
    recommended_replicates_per_arm: int = 4
    include_baseline_arm: bool = False
    linearization_mode_id: str = LINEARIZATION_MODE_ID

    def __post_init__(self) -> None:
        if self.candidate_cap <= 0:
            raise ValueError("candidate_cap must be positive")
        if not self.calibration_arms:
            raise ValueError("calibration_arms must not be empty")
        if not self.target_types:
            raise ValueError("target_types must not be empty")
        for required_count, window_length in self.sustained_windows:
            if required_count <= 0:
                raise ValueError("sustained window required_count must be positive")
            if window_length <= 0:
                raise ValueError("sustained window length must be positive")
            if required_count > window_length:
                raise ValueError("sustained window required_count cannot exceed length")
        for quantile in self.threshold_quantiles:
            if not 0.0 <= quantile <= 1.0:
                raise ValueError("threshold quantiles must be in [0, 1]")
        if self.recommended_episodes_per_replicate <= 0:
            raise ValueError("recommended_episodes_per_replicate must be positive")
        if self.recommended_replicates_per_arm <= 0:
            raise ValueError("recommended_replicates_per_arm must be positive")


def default_threshold_frontier_calibration_config(
    *,
    repo_root: Path | str,
    run_label: str = "smoke_001",
    locked_by: str = "cli",
) -> ThresholdFrontierCalibrationConfig:
    """Build default Stage 5 config from explicit architecture paths."""

    return ThresholdFrontierCalibrationConfig(
        artifact_root=suite_artifact_root(repo_root, run_label),
        run_label=run_label,
        training_health_source_path=(
            suite_readout_surface(repo_root)
            / "tower_training_health"
            / "readout_source.json"
        ),
        locked_by=locked_by,
    )
