"""Paths for Warehouse Gridlock transformer policy artifacts."""

from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path

from big_boy_benchmarking.environments.warehouse_gridlock.transformer_policy.config import (
    EVALUATION_ID,
)

READOUT_SURFACE = Path("docs/evaluations/warehouse_gridlock_001/transformer_policy")
DEFAULT_READINESS_SOURCE = Path(
    "docs/evaluations/warehouse_gridlock_001/environment_readiness/readout_source.json"
)


def repo_readout_surface(repo_root: Path | str) -> Path:
    return Path(repo_root) / READOUT_SURFACE


def default_readiness_source(repo_root: Path | str) -> Path:
    return Path(repo_root) / DEFAULT_READINESS_SOURCE


@dataclass(frozen=True)
class TransformerEvaluationPaths:
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
    def checkpoints_dir(self) -> Path:
        return self.artifact_root / "checkpoints"

    @property
    def traces_dir(self) -> Path:
        return self.artifact_root / "traces"

    @property
    def docs_results_dir(self) -> Path:
        return self.readout_surface / "results"

    @property
    def badges_dir(self) -> Path:
        return self.readout_surface / "badges"

    @property
    def movies_dir(self) -> Path:
        return self.readout_surface / "movies"

    @property
    def evaluation_manifest(self) -> Path:
        return self.artifact_root / "evaluation_manifest.json"

    @property
    def evaluation_budget_lock(self) -> Path:
        return self.artifact_root / "evaluation_budget_lock.json"

    @property
    def environment_instance_manifest(self) -> Path:
        return self.artifact_root / "environment_instance_manifest.json"

    @property
    def policy_contract_manifest(self) -> Path:
        return self.artifact_root / "policy_contract_manifest.json"

    @property
    def transformer_model_manifest(self) -> Path:
        return self.artifact_root / "transformer_model_manifest.json"

    @property
    def optimizer_manifest(self) -> Path:
        return self.artifact_root / "optimizer_manifest.json"

    @property
    def curriculum_manifest(self) -> Path:
        return self.artifact_root / "curriculum_manifest.json"

    @property
    def checkpoint_manifest(self) -> Path:
        return self.artifact_root / "checkpoint_manifest.json"

    @property
    def trace_retention_manifest(self) -> Path:
        return self.artifact_root / "trace_retention_manifest.json"

    @property
    def artifact_retention_manifest(self) -> Path:
        return self.artifact_root / "artifact_retention_manifest.json"

    @property
    def dependency_manifest(self) -> Path:
        return self.artifact_root / "dependency_manifest.json"

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
    def artifact_readout_source(self) -> Path:
        return self.artifact_root / "readout_source.json"

    @property
    def repo_readout_source(self) -> Path:
        return self.readout_surface / "readout_source.json"

    def run_root(self, run_id: str) -> Path:
        return self.runs_dir / run_id

    def trace_episode_dir(self, *, run_id: str, episode_index: int) -> Path:
        return self.traces_dir / run_id / f"episode_{episode_index:06d}"

    def ensure(self) -> None:
        for path in (
            self.artifact_root,
            self.results_dir,
            self.runs_dir,
            self.checkpoints_dir,
            self.traces_dir,
            self.readout_surface,
            self.docs_results_dir,
            self.badges_dir,
            self.movies_dir,
        ):
            path.mkdir(parents=True, exist_ok=True)


def run_id(*, arm_id: str, replicate_index: int, schema_seed: int, run_label: str) -> str:
    clean_arm = arm_id.replace("warehouse_", "").replace("_", "-")
    return f"{EVALUATION_ID}-{run_label}-{clean_arm}-rep{replicate_index}-schema{schema_seed}"

