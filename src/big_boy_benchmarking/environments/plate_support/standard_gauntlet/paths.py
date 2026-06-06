"""Explicit path contracts for PlateSupport standard gauntlet artifacts."""

from __future__ import annotations

from pathlib import Path

from big_boy_benchmarking.environments.plate_support.standard_gauntlet.ids import (
    ENVIRONMENT_INSTANCE_ID,
)


def normalize_repo_root(repo_root: Path | str) -> Path:
    """Resolve an explicit repository root argument."""

    root = Path(repo_root).expanduser().resolve()
    if not (root / "pyproject.toml").exists():
        raise ValueError(f"repo_root does not look like the BBB repository: {root}")
    return root


def suite_readout_surface(repo_root: Path | str) -> Path:
    """Return the repo-side human-readable gauntlet evaluation surface."""

    root = normalize_repo_root(repo_root)
    return root / "docs" / "evaluations" / ENVIRONMENT_INSTANCE_ID / "standard_gauntlet"


def suite_artifact_root(repo_root: Path | str, run_label: str) -> Path:
    """Return the raw artifact root for a named gauntlet run."""

    surface = suite_readout_surface(repo_root)
    target = surface / "artifacts" / run_label
    if "docs/evaluations" not in target.as_posix():
        raise ValueError(f"suite artifact root escaped docs/evaluations: {target}")
    return target


def suite_evaluation_root(repo_root: Path | str, run_label: str, evaluation_id: str) -> Path:
    """Return the suite-level machine-readable evaluation root for a run."""

    return suite_artifact_root(repo_root, run_label) / "evaluations" / evaluation_id


def default_readiness_source_path(
    repo_root: Path | str,
    readiness_run_label: str = "dev_001",
) -> Path:
    """Return the environment-readiness source binding consumed by Stage 1."""

    root = normalize_repo_root(repo_root)
    return (
        root
        / "docs"
        / "environments"
        / ENVIRONMENT_INSTANCE_ID
        / "readiness"
        / readiness_run_label
        / "readout_source.json"
    )
