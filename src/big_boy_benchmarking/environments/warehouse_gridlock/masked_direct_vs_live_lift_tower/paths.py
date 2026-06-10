"""Paths for the Warehouse masked direct/live-lift tower diagnostic."""

from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path

from big_boy_benchmarking.environments.warehouse_gridlock.masked_direct_vs_live_lift_tower.config import (
    EVALUATION_ID,
)

READOUT_SURFACE = Path("docs/evaluations/warehouse_gridlock_001/masked_direct_vs_live_lift_tower")
DEFAULT_READINESS_SOURCE = Path(
    "docs/evaluations/warehouse_gridlock_001/environment_readiness/readout_source.json"
)


def repo_readout_surface(repo_root: Path | str) -> Path:
    return Path(repo_root) / READOUT_SURFACE


def default_readiness_source(repo_root: Path | str) -> Path:
    return Path(repo_root) / DEFAULT_READINESS_SOURCE


@dataclass(frozen=True)
class EvaluationPaths:
    repo_root: Path
    artifact_root: Path

    @property
    def readout_surface(self) -> Path:
        return repo_readout_surface(self.repo_root)

    @property
    def results_dir(self) -> Path:
        return self.artifact_root / "results"

    @property
    def runs_dir(self) -> Path:
        return self.artifact_root / "runs"

    @property
    def badges_dir(self) -> Path:
        return self.readout_surface / "badges"

    @property
    def docs_results_dir(self) -> Path:
        return self.readout_surface / "results"

    def run_root(self, run_id: str) -> Path:
        return self.runs_dir / run_id

    @property
    def evaluation_manifest(self) -> Path:
        return self.artifact_root / "evaluation_manifest.json"

    @property
    def evaluation_budget_lock(self) -> Path:
        return self.artifact_root / "evaluation_budget_lock.json"

    @property
    def evaluation_input_manifest(self) -> Path:
        return self.artifact_root / "evaluation_input_manifest.json"

    @property
    def dependency_manifest(self) -> Path:
        return self.artifact_root / "dependency_manifest.json"

    @property
    def arm_manifest(self) -> Path:
        return self.artifact_root / "arm_manifest.json"

    @property
    def candidate_generation_manifest(self) -> Path:
        return self.artifact_root / "candidate_generation_manifest.json"

    @property
    def admissibility_policy_manifest(self) -> Path:
        return self.artifact_root / "admissibility_policy_manifest.json"

    @property
    def live_lift_policy_manifest(self) -> Path:
        return self.artifact_root / "live_lift_policy_manifest.json"

    @property
    def no_lookahead_policy_manifest(self) -> Path:
        return self.artifact_root / "no_lookahead_policy_manifest.json"

    @property
    def tower_construction_manifest(self) -> Path:
        return self.artifact_root / "tower_construction_manifest.json"

    @property
    def tower_surface_scope_manifest(self) -> Path:
        return self.artifact_root / "tower_surface_scope_manifest.json"

    @property
    def run_index(self) -> Path:
        return self.artifact_root / "run_index.csv"

    @property
    def artifact_readout_source(self) -> Path:
        return self.artifact_root / "readout_source.json"

    @property
    def repo_readout_source(self) -> Path:
        return self.readout_surface / "readout_source.json"

    @property
    def aggregate_summary(self) -> Path:
        return self.artifact_root / "evaluation_aggregate_summary.json"

    @property
    def aggregate_table(self) -> Path:
        return self.artifact_root / "evaluation_aggregate_table.csv"

    def ensure(self) -> None:
        self.artifact_root.mkdir(parents=True, exist_ok=True)
        self.results_dir.mkdir(parents=True, exist_ok=True)
        self.runs_dir.mkdir(parents=True, exist_ok=True)
        self.readout_surface.mkdir(parents=True, exist_ok=True)
        self.docs_results_dir.mkdir(parents=True, exist_ok=True)
        self.badges_dir.mkdir(parents=True, exist_ok=True)


def run_id(*, arm_id: str, replicate_index: int, schema_seed: int, run_label: str) -> str:
    clean_arm = arm_id.replace("warehouse_", "").replace("_", "-")
    return f"{EVALUATION_ID}-{run_label}-{clean_arm}-rep{replicate_index}-schema{schema_seed}"
