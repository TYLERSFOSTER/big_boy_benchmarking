"""Evaluation-level paths for serious counterpoint learning artifacts."""

from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path


@dataclass(frozen=True)
class SeriousLearningEvaluationPaths:
    root: Path
    evaluation_manifest: Path
    evaluation_arm_manifest: Path
    evaluation_run_index_csv: Path
    evaluation_budget_lock: Path
    evaluation_aggregate_summary: Path
    evaluation_aggregate_table_csv: Path
    calibration_summary: Path
    calibration_run_index_csv: Path
    calibration_recommendation_md: Path
    docs_dir: Path
    results_dir: Path


def build_serious_learning_evaluation_paths(
    artifact_root: Path | str,
    *,
    evaluation_id: str = "counterpoint_first_serious_learning_v001",
) -> SeriousLearningEvaluationPaths:
    root = Path(artifact_root) / "evaluations" / evaluation_id
    return SeriousLearningEvaluationPaths(
        root=root,
        evaluation_manifest=root / "evaluation_manifest.json",
        evaluation_arm_manifest=root / "evaluation_arm_manifest.json",
        evaluation_run_index_csv=root / "evaluation_run_index.csv",
        evaluation_budget_lock=root / "evaluation_budget_lock.json",
        evaluation_aggregate_summary=root / "evaluation_aggregate_summary.json",
        evaluation_aggregate_table_csv=root / "evaluation_aggregate_table.csv",
        calibration_summary=root / "calibration_summary.json",
        calibration_run_index_csv=root / "calibration_run_index.csv",
        calibration_recommendation_md=root / "calibration_recommendation.md",
        docs_dir=root / "docs",
        results_dir=root / "results",
    )
