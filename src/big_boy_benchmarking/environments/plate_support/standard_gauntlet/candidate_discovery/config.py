"""Configuration for PlateSupport gauntlet Stage 3 candidate discovery."""

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
class CandidateDiscoveryConfig:
    """Explicit runtime context for Stage 3 candidate discovery."""

    artifact_root: Path
    run_label: str
    schema_sweep_source_path: Path
    locked_by: str
    clean_candidate_cap: int = 2
    warning_candidate_cap: int = 1
    degeneracy_anchor_cap: int = 1
    allow_warning_selection: bool = False
    linearization_mode_id: str = LINEARIZATION_MODE_ID


def default_candidate_discovery_config(
    *,
    repo_root: Path | str,
    run_label: str = "smoke_001",
    locked_by: str = "cli",
) -> CandidateDiscoveryConfig:
    """Build default Stage 3 config from explicit architecture paths."""

    return CandidateDiscoveryConfig(
        artifact_root=suite_artifact_root(repo_root, run_label),
        run_label=run_label,
        schema_sweep_source_path=(
            suite_readout_surface(repo_root)
            / "contraction_schema_sweep"
            / "readout_source.json"
        ),
        locked_by=locked_by,
    )
