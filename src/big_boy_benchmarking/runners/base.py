"""Base runner request/result contracts."""

from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path
from typing import Any, Protocol

from big_boy_benchmarking.seeds.bundles import SeedBundle
from big_boy_benchmarking.upstream.state_collapser import StateCollapserDependencyState


@dataclass(frozen=True)
class BenchmarkRunRequest:
    run_id: str
    run_family_id: str
    environment_id: str
    mode_id: str
    linearization_mode_id: str
    schema_id: str
    learner_id: str
    controller_id: str
    seed_bundle: SeedBundle
    budget: dict[str, Any]
    artifact_root: Path
    diagnostic_profile: str
    timing_profile: str
    dependency_state: StateCollapserDependencyState | None = None


@dataclass(frozen=True)
class BenchmarkRunResult:
    run_id: str
    status: str
    artifact_paths: dict[str, str]
    summary_path: str | None
    warning_count: int
    started_at: str
    ended_at: str | None
    failure_reason: str | None = None


class BenchmarkRunner(Protocol):
    def run(self, request: BenchmarkRunRequest) -> BenchmarkRunResult:
        """Run one benchmark request."""
