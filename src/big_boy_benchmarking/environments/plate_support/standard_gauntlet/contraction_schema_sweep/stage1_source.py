"""Stage 1 source loading for the PlateSupport schema sweep."""

from __future__ import annotations

import csv
import json
from dataclasses import dataclass
from pathlib import Path

from big_boy_benchmarking.environments.plate_support.standard_gauntlet.ids import (
    STRUCTURAL_TOWER_DIAGNOSTICS_STAGE_ID,
)


REQUIRED_STAGE1_TABLES = (
    "transition_summary",
    "tower_shape_summary",
    "validity_predicate_summary",
    "geometry_summary",
    "downstream_readiness_summary",
)


@dataclass(frozen=True)
class Stage1Source:
    """Validated Stage 1 readout source and required table paths."""

    path: Path
    repo_root: Path
    repo_readout_surface: Path
    source_artifact_root: Path
    source_files: dict[str, Path]
    downstream_readiness_row: dict[str, str]


class Stage1SourceError(ValueError):
    """Raised when Stage 1 cannot safely feed Stage 2."""


def load_stage1_source(path: Path | str, *, repo_root: Path | str) -> Stage1Source:
    """Load Stage 1 source binding and required source tables."""

    root = Path(repo_root).expanduser().resolve()
    source_path = Path(path).expanduser().resolve()
    _require_under_repo(source_path, root, "Stage 1 source")
    if not source_path.exists():
        raise Stage1SourceError(f"Stage 1 readout source does not exist: {source_path}")
    with source_path.open(encoding="utf-8") as handle:
        payload = json.load(handle)

    if payload.get("evaluation_id") != STRUCTURAL_TOWER_DIAGNOSTICS_STAGE_ID:
        raise Stage1SourceError(
            "Stage 1 source does not identify structural tower diagnostics: "
            f"{payload.get('evaluation_id')!r}"
        )
    readout_surface = Path(str(payload["repo_readout_surface"])).expanduser().resolve()
    artifact_root = Path(str(payload["source_artifact_root"])).expanduser().resolve()
    _require_under_repo(readout_surface, root, "Stage 1 readout surface")
    _require_under_repo(artifact_root, root, "Stage 1 artifact root")
    if "docs/evaluations" not in readout_surface.as_posix():
        raise Stage1SourceError(f"Stage 1 readout surface is not under docs/evaluations: {readout_surface}")

    source_files_payload = payload.get("source_files", {})
    if not isinstance(source_files_payload, dict):
        raise Stage1SourceError("Stage 1 source_files must be a mapping")
    source_files: dict[str, Path] = {}
    for table_name in REQUIRED_STAGE1_TABLES:
        table_path = Path(str(source_files_payload.get(table_name, ""))).expanduser().resolve()
        _require_under_repo(table_path, root, f"Stage 1 {table_name}")
        if not table_path.exists():
            raise Stage1SourceError(f"required Stage 1 table missing: {table_path}")
        source_files[table_name] = table_path

    downstream_rows = _read_rows(source_files["downstream_readiness_summary"])
    if not downstream_rows:
        raise Stage1SourceError("Stage 1 downstream readiness table is empty")
    if downstream_rows[0].get("ready_for_schema_sweep") != "True":
        raise Stage1SourceError(
            "Stage 1 blocks schema sweep: "
            f"{downstream_rows[0].get('blocking_reason', 'unknown')}"
        )
    return Stage1Source(
        path=source_path,
        repo_root=root,
        repo_readout_surface=readout_surface,
        source_artifact_root=artifact_root,
        source_files=source_files,
        downstream_readiness_row=downstream_rows[0],
    )


def read_stage1_table(source: Stage1Source, table_name: str) -> list[dict[str, str]]:
    """Read a validated Stage 1 table."""

    if table_name not in source.source_files:
        raise Stage1SourceError(f"Stage 1 table not registered: {table_name}")
    return _read_rows(source.source_files[table_name])


def _read_rows(path: Path) -> list[dict[str, str]]:
    with path.open(encoding="utf-8", newline="") as handle:
        return list(csv.DictReader(handle))


def _require_under_repo(path: Path, repo_root: Path, label: str) -> None:
    try:
        path.relative_to(repo_root)
    except ValueError as exc:
        raise Stage1SourceError(f"{label} is outside repository: {path}") from exc
