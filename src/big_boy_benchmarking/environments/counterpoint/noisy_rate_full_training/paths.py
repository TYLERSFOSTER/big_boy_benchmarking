"""Path helpers for noisy-rate full-tower training diagnostics."""

from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path

from big_boy_benchmarking.environments.counterpoint.noisy_rate_full_training.config import (
    EVALUATION_ID,
)

REPO_ROOT = Path(__file__).resolve().parents[5]
DEFAULT_REPO_READOUT_SURFACE = (
    REPO_ROOT
    / "docs"
    / "evaluations"
    / "counterpoint_symbolic_v001"
    / "noisy_rate_full_tower_training_diagnostic"
)
DEFAULT_PARENT_CANDIDATE_READOUT_SOURCE = (
    REPO_ROOT
    / "docs"
    / "evaluations"
    / "counterpoint_symbolic_v001"
    / "noisy_rate_contraction_diagnostics"
    / "readout_source.json"
)


@dataclass(frozen=True)
class NoisyRateFullTrainingEvaluationPaths:
    root: Path
    evaluation_manifest: Path
    evaluation_budget_lock: Path
    candidate_manifest: Path
    evaluation_run_index_csv: Path
    evaluation_aggregate_summary: Path
    evaluation_aggregate_table_csv: Path
    results_dir: Path
    readout_source: Path


def build_noisy_rate_full_training_paths(
    artifact_root: Path | str,
    *,
    evaluation_id: str = EVALUATION_ID,
) -> NoisyRateFullTrainingEvaluationPaths:
    root = Path(artifact_root) / "evaluations" / evaluation_id
    return NoisyRateFullTrainingEvaluationPaths(
        root=root,
        evaluation_manifest=root / "evaluation_manifest.json",
        evaluation_budget_lock=root / "evaluation_budget_lock.json",
        candidate_manifest=root / "candidate_manifest.json",
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


def validate_repo_resident_path(path: Path | str) -> Path:
    target = normalize_repo_path(path)
    repo_root = normalize_repo_path(REPO_ROOT)
    try:
        target.relative_to(repo_root)
    except ValueError as exc:
        raise ValueError(f"path must be repo-resident under {repo_root}; got {target}") from exc
    return target


def validate_repo_resident_artifact_root(artifact_root: Path | str) -> Path:
    return validate_repo_resident_path(artifact_root)


def repo_readout_surface() -> Path:
    return DEFAULT_REPO_READOUT_SURFACE


def default_parent_candidate_readout_source() -> Path:
    return DEFAULT_PARENT_CANDIDATE_READOUT_SOURCE

