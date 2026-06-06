"""Stage 2 source loading for candidate discovery."""

from __future__ import annotations

import csv
import json
from dataclasses import dataclass
from pathlib import Path

from big_boy_benchmarking.environments.plate_support.standard_gauntlet.ids import (
    CONTRACTION_SCHEMA_SWEEP_STAGE_ID,
)

REQUIRED_STAGE2_TABLES = (
    "schema_candidate_signal_summary",
    "schema_arm_summary",
    "schema_construction_summary",
    "tower_shape_summary",
    "tier_executability_summary",
    "collapse_diagnostic_summary",
    "downstream_candidate_input_summary",
)


@dataclass(frozen=True)
class Stage2Source:
    """Validated Stage 2 readout source and required tables."""

    path: Path
    repo_root: Path
    repo_readout_surface: Path
    source_artifact_root: Path
    source_files: dict[str, Path]


class Stage2SourceError(ValueError):
    """Raised when Stage 2 cannot safely feed candidate discovery."""


def load_stage2_source(path: Path | str, *, repo_root: Path | str) -> Stage2Source:
    """Load Stage 2 readout source and validate required tables."""

    root = Path(repo_root).expanduser().resolve()
    source_path = Path(path).expanduser().resolve()
    _require_under_repo(source_path, root, "Stage 2 source")
    if not source_path.exists():
        raise Stage2SourceError(f"Stage 2 readout source does not exist: {source_path}")
    with source_path.open(encoding="utf-8") as handle:
        payload = json.load(handle)
    if payload.get("evaluation_id") != CONTRACTION_SCHEMA_SWEEP_STAGE_ID:
        raise Stage2SourceError(
            f"expected Stage 2 source, got {payload.get('evaluation_id')!r}"
        )
    readout_surface = Path(str(payload["repo_readout_surface"])).expanduser().resolve()
    artifact_root = Path(str(payload["source_artifact_root"])).expanduser().resolve()
    _require_under_repo(readout_surface, root, "Stage 2 readout surface")
    _require_under_repo(artifact_root, root, "Stage 2 artifact root")
    source_files_payload = payload.get("source_files", {})
    if not isinstance(source_files_payload, dict):
        raise Stage2SourceError("Stage 2 source_files must be a mapping")
    source_files: dict[str, Path] = {}
    for table_name in REQUIRED_STAGE2_TABLES:
        table_path = Path(str(source_files_payload.get(table_name, ""))).expanduser().resolve()
        _require_under_repo(table_path, root, f"Stage 2 {table_name}")
        if not table_path.exists():
            raise Stage2SourceError(f"required Stage 2 table missing: {table_path}")
        source_files[table_name] = table_path
    if not (artifact_root / "stage_aggregate_summary.json").exists():
        raise Stage2SourceError("Stage 2 aggregate summary is missing")
    return Stage2Source(
        path=source_path,
        repo_root=root,
        repo_readout_surface=readout_surface,
        source_artifact_root=artifact_root,
        source_files=source_files,
    )


def read_stage2_table(source: Stage2Source, table_name: str) -> list[dict[str, str]]:
    """Read a validated Stage 2 table."""

    if table_name not in source.source_files:
        raise Stage2SourceError(f"Stage 2 table not registered: {table_name}")
    with source.source_files[table_name].open(encoding="utf-8", newline="") as handle:
        return list(csv.DictReader(handle))


def _require_under_repo(path: Path, repo_root: Path, label: str) -> None:
    try:
        path.relative_to(repo_root)
    except ValueError as exc:
        raise Stage2SourceError(f"{label} is outside repository: {path}") from exc
