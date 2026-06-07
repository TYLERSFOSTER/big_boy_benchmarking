"""Configuration for PlateSupport gauntlet Stage 2 schema sweep."""

from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path

from big_boy_benchmarking.environments.plate_support.standard_gauntlet.ids import (
    LINEARIZATION_MODE_ID,
)
from big_boy_benchmarking.environments.plate_support.standard_gauntlet.paths import (
    suite_artifact_root,
    suite_readout_surface,
)


@dataclass(frozen=True)
class SchemaSweepConfig:
    """Explicit runtime context for the Stage 2 schema sweep."""

    artifact_root: Path
    run_label: str
    stage1_readout_source_path: Path
    locked_by: str
    schema_families: tuple[str, ...] = (
        "no_contraction",
        "upstream_default",
        "source_local_ratio",
        "action_category",
        "edge_global_noisy_rate",
        "geometry_coordinate",
        "controlled_degeneracy",
    )
    schema_seeds: tuple[int, ...] = (0,)
    source_local_ratio_numerators: tuple[int, ...] = (1,)
    source_local_ratio_denominator: int = 18
    edge_global_numerators: tuple[int, ...] = (1, 2, 4, 8)
    near_full_collapse_threshold: float = 0.90
    tower_probe_steps: int = 20
    tower_probe_sample_size: int = 20
    smoke_seed: int = 0
    linearization_mode_id: str = LINEARIZATION_MODE_ID

    def __post_init__(self) -> None:
        if self.source_local_ratio_denominator <= 0:
            raise ValueError("source_local_ratio_denominator must be positive")
        if any(numerator <= 0 for numerator in self.source_local_ratio_numerators):
            raise ValueError("source_local_ratio_numerators must all be positive")


def default_schema_sweep_config(
    *,
    repo_root: Path | str,
    run_label: str = "smoke_001",
    locked_by: str = "cli",
) -> SchemaSweepConfig:
    """Build default Stage 2 config from explicit architecture paths."""

    return SchemaSweepConfig(
        artifact_root=suite_artifact_root(repo_root, run_label),
        run_label=run_label,
        stage1_readout_source_path=(
            suite_readout_surface(repo_root)
            / "structural_and_tower_diagnostics"
            / "readout_source.json"
        ),
        locked_by=locked_by,
    )
