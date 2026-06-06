"""Configuration for PlateSupport gauntlet Stage 1 diagnostics."""

from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path

from big_boy_benchmarking.environments.plate_support.standard_gauntlet.ids import (
    LINEARIZATION_MODE_ID,
)
from big_boy_benchmarking.environments.plate_support.standard_gauntlet.paths import (
    default_readiness_source_path,
    suite_artifact_root,
)


@dataclass(frozen=True)
class StructuralDiagnosticsConfig:
    """Explicit runtime context for Stage 1 diagnostics."""

    artifact_root: Path
    run_label: str
    readiness_source_path: Path
    locked_by: str
    random_policy_seed: int = 0
    random_policy_episode_count: int = 1000
    tower_probe_steps: int = 20
    tower_probe_sample_size: int = 20
    linearization_mode_id: str = LINEARIZATION_MODE_ID


def default_structural_diagnostics_config(
    *,
    repo_root: Path | str,
    run_label: str = "smoke_001",
    locked_by: str = "cli",
    readiness_run_label: str = "dev_001",
) -> StructuralDiagnosticsConfig:
    """Build Stage 1 config from explicit architecture path helpers."""

    return StructuralDiagnosticsConfig(
        artifact_root=suite_artifact_root(repo_root, run_label),
        run_label=run_label,
        readiness_source_path=default_readiness_source_path(
            repo_root,
            readiness_run_label=readiness_run_label,
        ),
        locked_by=locked_by,
    )
