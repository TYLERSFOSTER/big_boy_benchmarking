"""Path helpers for the counterpoint small paired replicate probe."""

from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path

from big_boy_benchmarking.environments.counterpoint.small_paired_replicate_probe.config import (
    EVALUATION_ID,
)

REPO_ROOT = Path(__file__).resolve().parents[5]
DEFAULT_REPO_READOUT_SURFACE = (
    REPO_ROOT
    / "docs"
    / "evaluations"
    / "counterpoint_symbolic_v001"
    / "small_paired_replicate_probe"
)
DEFAULT_CANDIDATE_READOUT_SOURCE = (
    REPO_ROOT
    / "docs"
    / "evaluations"
    / "counterpoint_symbolic_v001"
    / "noisy_rate_full_tower_training_diagnostic"
    / "readout_source.json"
)
DEFAULT_THRESHOLD_FRONTIER_READOUT_SOURCE = (
    REPO_ROOT
    / "docs"
    / "evaluations"
    / "counterpoint_symbolic_v001"
    / "threshold_frontier_probe"
    / "readout_source.json"
)


@dataclass(frozen=True)
class SmallPairedReplicateProbePaths:
    root: Path
    evaluation_manifest: Path
    evaluation_arm_manifest: Path
    evaluation_budget_lock: Path
    replicate_probe_policy_manifest: Path
    threshold_policy_manifest: Path
    tier_jump_policy_manifest: Path
    candidate_manifest: Path
    parent_source_manifest: Path
    evaluation_run_index_csv: Path
    evaluation_aggregate_table_csv: Path
    evaluation_aggregate_summary: Path
    results_dir: Path
    readout_source: Path


def build_small_paired_replicate_probe_paths(
    artifact_root: Path | str,
    *,
    evaluation_id: str = EVALUATION_ID,
) -> SmallPairedReplicateProbePaths:
    root = Path(artifact_root) / "evaluations" / evaluation_id
    return SmallPairedReplicateProbePaths(
        root=root,
        evaluation_manifest=root / "evaluation_manifest.json",
        evaluation_arm_manifest=root / "evaluation_arm_manifest.json",
        evaluation_budget_lock=root / "evaluation_budget_lock.json",
        replicate_probe_policy_manifest=root / "replicate_probe_policy_manifest.json",
        threshold_policy_manifest=root / "threshold_policy_manifest.json",
        tier_jump_policy_manifest=root / "tier_jump_policy_manifest.json",
        candidate_manifest=root / "candidate_manifest.json",
        parent_source_manifest=root / "parent_source_manifest.json",
        evaluation_run_index_csv=root / "evaluation_run_index.csv",
        evaluation_aggregate_table_csv=root / "evaluation_aggregate_table.csv",
        evaluation_aggregate_summary=root / "evaluation_aggregate_summary.json",
        results_dir=root / "results",
        readout_source=root / "readout_source.json",
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


def default_threshold_frontier_readout_source() -> Path:
    return DEFAULT_THRESHOLD_FRONTIER_READOUT_SOURCE


def repo_readout_surface() -> Path:
    return DEFAULT_REPO_READOUT_SURFACE
