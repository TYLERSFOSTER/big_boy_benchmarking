"""Deterministic artifact path builders."""

from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path


@dataclass(frozen=True)
class RunFamilyPaths:
    """Paths owned by one run-family artifact directory."""

    root: Path
    family_manifest: Path
    matrix_manifest: Path
    environment_family_manifest: Path
    dependency_manifest: Path
    run_index: Path
    summaries_dir: Path
    summary_json: Path
    summary_csv: Path
    bootstrap_intervals_csv: Path
    runs_dir: Path


@dataclass(frozen=True)
class RunPaths:
    """Paths owned by one concrete run artifact directory."""

    root: Path
    run_manifest: Path
    seed_bundle: Path
    mode_manifest: Path
    timing_summary: Path
    episodes_csv: Path
    step_events_csv: Path
    control_events_csv: Path
    timing_segments_csv: Path
    structural_diagnostics_jsonl: Path
    warnings_jsonl: Path
    external_artifacts: Path


@dataclass(frozen=True)
class ArtifactPaths:
    """Combined path record for a run family and optional concrete run."""

    run_family: RunFamilyPaths
    run: RunPaths | None = None


def build_run_family_paths(artifact_root: Path | str, run_family_id: str) -> RunFamilyPaths:
    """Build paths for a run family without creating directories."""

    root = Path(artifact_root) / "runs" / run_family_id
    summaries_dir = root / "summaries"
    return RunFamilyPaths(
        root=root,
        family_manifest=root / "family_manifest.json",
        matrix_manifest=root / "matrix_manifest.json",
        environment_family_manifest=root / "environment_family_manifest.json",
        dependency_manifest=root / "dependency_manifest.json",
        run_index=root / "run_index.jsonl",
        summaries_dir=summaries_dir,
        summary_json=summaries_dir / "summary.json",
        summary_csv=summaries_dir / "summary.csv",
        bootstrap_intervals_csv=summaries_dir / "bootstrap_intervals.csv",
        runs_dir=root / "runs",
    )


def build_run_paths(artifact_root: Path | str, run_family_id: str, run_id: str) -> RunPaths:
    """Build paths for a concrete run without creating directories."""

    family = build_run_family_paths(artifact_root, run_family_id)
    root = family.runs_dir / run_id
    return RunPaths(
        root=root,
        run_manifest=root / "run_manifest.json",
        seed_bundle=root / "seed_bundle.json",
        mode_manifest=root / "mode_manifest.json",
        timing_summary=root / "timing_summary.json",
        episodes_csv=root / "episodes.csv",
        step_events_csv=root / "step_events.csv",
        control_events_csv=root / "control_events.csv",
        timing_segments_csv=root / "timing_segments.csv",
        structural_diagnostics_jsonl=root / "structural_diagnostics.jsonl",
        warnings_jsonl=root / "warnings.jsonl",
        external_artifacts=root / "external_artifacts.json",
    )
