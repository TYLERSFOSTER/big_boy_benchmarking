"""Path helpers for one-third counterpoint tower diagnostics."""

from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path

from big_boy_benchmarking.environments.counterpoint.one_third_diagnostics.config import (
    EVALUATION_ID,
)

REPO_ROOT = Path(__file__).resolve().parents[5]
DEFAULT_REPO_READOUT_SURFACE = (
    REPO_ROOT
    / "docs"
    / "evaluations"
    / "counterpoint_symbolic_v001"
    / "one_third_schema_tower_diagnostics"
)


@dataclass(frozen=True)
class OneThirdDiagnosticsEvaluationPaths:
    root: Path
    evaluation_manifest: Path
    evaluation_budget_lock: Path
    evaluation_run_index_csv: Path
    evaluation_aggregate_summary: Path
    evaluation_aggregate_table_csv: Path
    results_dir: Path
    readout_source: Path


def build_one_third_diagnostics_paths(
    artifact_root: Path | str,
    *,
    evaluation_id: str = EVALUATION_ID,
) -> OneThirdDiagnosticsEvaluationPaths:
    root = Path(artifact_root) / "evaluations" / evaluation_id
    return OneThirdDiagnosticsEvaluationPaths(
        root=root,
        evaluation_manifest=root / "evaluation_manifest.json",
        evaluation_budget_lock=root / "evaluation_budget_lock.json",
        evaluation_run_index_csv=root / "evaluation_run_index.csv",
        evaluation_aggregate_summary=root / "evaluation_aggregate_summary.json",
        evaluation_aggregate_table_csv=root / "evaluation_aggregate_table.csv",
        results_dir=root / "results",
        readout_source=root / "readout_source.json",
    )


def default_artifact_root(run_label: str = "latest") -> Path:
    return DEFAULT_REPO_READOUT_SURFACE / "artifacts" / run_label


def normalize_repo_path(path: Path | str) -> Path:
    return Path(path).expanduser().resolve()


def validate_repo_resident_artifact_root(artifact_root: Path | str) -> Path:
    root = normalize_repo_path(artifact_root)
    repo_root = normalize_repo_path(REPO_ROOT)
    try:
        root.relative_to(repo_root)
    except ValueError as exc:
        raise ValueError(
            "one-third diagnostics artifacts must be repo-resident under "
            f"{repo_root}; got {root}"
        ) from exc
    return root


def repo_readout_surface() -> Path:
    return DEFAULT_REPO_READOUT_SURFACE
