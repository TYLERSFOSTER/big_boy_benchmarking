"""Path helpers for the counterpoint threshold-frontier probe."""

from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path

from .config import EVALUATION_ID, EVALUATION_RUN_FAMILY_ID
from .thresholds import threshold_label

REPO_ROOT = Path(__file__).resolve().parents[5]
DEFAULT_REPO_READOUT_SURFACE = (
    REPO_ROOT / "docs" / "evaluations" / "counterpoint_symbolic_v001" / "threshold_frontier_probe"
)
DEFAULT_CANDIDATE_READOUT_SOURCE = (
    REPO_ROOT
    / "docs"
    / "evaluations"
    / "counterpoint_symbolic_v001"
    / "noisy_rate_full_tower_training_diagnostic"
    / "readout_source.json"
)


@dataclass(frozen=True)
class ThresholdFrontierProbePaths:
    root: Path
    evaluation_manifest: Path
    evaluation_arm_manifest: Path
    evaluation_budget_lock: Path
    threshold_frontier_policy_manifest: Path
    threshold_run_manifest: Path
    candidate_manifest: Path
    parent_source_manifest: Path
    evaluation_run_index_csv: Path
    evaluation_aggregate_table_csv: Path
    evaluation_aggregate_summary: Path
    results_dir: Path
    readout_source: Path
    run_family_summary: Path


def build_threshold_frontier_probe_paths(
    artifact_root: Path | str,
    *,
    evaluation_id: str = EVALUATION_ID,
) -> ThresholdFrontierProbePaths:
    root = Path(artifact_root) / "evaluations" / evaluation_id
    run_family_root = Path(artifact_root) / "runs" / EVALUATION_RUN_FAMILY_ID
    return ThresholdFrontierProbePaths(
        root=root,
        evaluation_manifest=root / "evaluation_manifest.json",
        evaluation_arm_manifest=root / "evaluation_arm_manifest.json",
        evaluation_budget_lock=root / "evaluation_budget_lock.json",
        threshold_frontier_policy_manifest=root / "threshold_frontier_policy_manifest.json",
        threshold_run_manifest=root / "threshold_run_manifest.json",
        candidate_manifest=root / "candidate_manifest.json",
        parent_source_manifest=root / "parent_source_manifest.json",
        evaluation_run_index_csv=root / "evaluation_run_index.csv",
        evaluation_aggregate_table_csv=root / "evaluation_aggregate_table.csv",
        evaluation_aggregate_summary=root / "evaluation_aggregate_summary.json",
        results_dir=root / "results",
        readout_source=root / "readout_source.json",
        run_family_summary=run_family_root / "summaries" / "summary.json",
    )


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


def default_artifact_root(run_label: str = "smoke_001") -> Path:
    return DEFAULT_REPO_READOUT_SURFACE / "artifacts" / run_label


def default_candidate_readout_source() -> Path:
    return DEFAULT_CANDIDATE_READOUT_SOURCE


def repo_readout_surface() -> Path:
    return DEFAULT_REPO_READOUT_SURFACE


def threshold_run_root(artifact_root: Path | str, threshold_value: float) -> Path:
    return Path(artifact_root) / "threshold_runs" / threshold_label(threshold_value)
