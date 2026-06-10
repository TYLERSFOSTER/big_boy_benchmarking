"""Paths for Warehouse full-state policy comparison artifacts."""

from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path

from big_boy_benchmarking.environments.warehouse_gridlock.full_state_policy_comparison.config import (
    EVALUATION_ID,
)

READOUT_SURFACE = Path("docs/evaluations/warehouse_gridlock_001/full_state_policy_comparison")
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
    def docs_results_dir(self) -> Path:
        return self.readout_surface / "results"

    @property
    def badges_dir(self) -> Path:
        return self.readout_surface / "badges"

    def run_root(self, run_id: str) -> Path:
        return self.runs_dir / run_id

    @property
    def evaluation_manifest(self) -> Path:
        return self.artifact_root / "evaluation_manifest.json"

    @property
    def evaluation_budget_lock(self) -> Path:
        return self.artifact_root / "evaluation_budget_lock.json"

    @property
    def evaluation_arm_manifest(self) -> Path:
        return self.artifact_root / "evaluation_arm_manifest.json"

    @property
    def environment_instance_manifest(self) -> Path:
        return self.artifact_root / "environment_instance_manifest.json"

    @property
    def policy_contract_manifest(self) -> Path:
        return self.artifact_root / "policy_contract_manifest.json"

    @property
    def policy_model_manifest(self) -> Path:
        return self.artifact_root / "policy_model_manifest.json"

    @property
    def policy_training_manifest(self) -> Path:
        return self.artifact_root / "policy_training_manifest.json"

    @property
    def admissibility_resolver_manifest(self) -> Path:
        return self.artifact_root / "admissibility_resolver_manifest.json"

    @property
    def tower_policy_manifest(self) -> Path:
        return self.artifact_root / "tower_policy_manifest.json"

    @property
    def tower_construction_manifest(self) -> Path:
        return self.artifact_root / "tower_construction_manifest.json"

    @property
    def run_index(self) -> Path:
        return self.artifact_root / "run_index.csv"

    @property
    def progress_events(self) -> Path:
        return self.artifact_root / "progress_events.jsonl"

    @property
    def aggregate_summary(self) -> Path:
        return self.artifact_root / "evaluation_aggregate_summary.json"

    @property
    def aggregate_table(self) -> Path:
        return self.artifact_root / "evaluation_aggregate_table.csv"

    @property
    def artifact_readout_source(self) -> Path:
        return self.artifact_root / "readout_source.json"

    @property
    def repo_readout_source(self) -> Path:
        return self.readout_surface / "readout_source.json"

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
