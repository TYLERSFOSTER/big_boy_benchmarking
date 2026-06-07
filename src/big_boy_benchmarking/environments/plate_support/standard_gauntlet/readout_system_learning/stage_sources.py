"""Source loading for PlateSupport standard gauntlet readout synthesis."""

from __future__ import annotations

import csv
import json
from dataclasses import dataclass
from pathlib import Path

from ..ids import STAGE_DEFINITIONS, SUITE_ID


@dataclass(frozen=True)
class StageSourceRecord:
    """Normalized stage readout/source state."""

    stage_number: int
    stage_id: str
    short_name: str
    readout_source_path: Path | None
    status: str
    claim_status: str
    claim_boundary: str
    source_artifact_root: Path | None
    source_files: dict[str, Path]
    blocking_reason: str


@dataclass(frozen=True)
class SuiteReadoutSource:
    """Validated suite-level readout source."""

    path: Path
    repo_root: Path
    repo_readout_surface: Path
    source_artifact_root: Path
    source_evaluation_root: Path
    source_files: dict[str, Path]
    run_label: str
    stage_records: tuple[StageSourceRecord, ...]
    status_rows: list[dict[str, str]]


class ReadoutSourceError(ValueError):
    """Raised when the explicit readout source cannot drive Stage 7."""


def load_suite_readout_source(path: Path | str) -> SuiteReadoutSource:
    """Load the suite readout source and all available stage sources."""

    source_path = Path(path).expanduser().resolve()
    if source_path.name != "readout_source.json":
        raise ReadoutSourceError(
            "readout build requires an explicit readout_source.json, not a directory "
            f"or artifact root: {source_path}"
        )
    if not source_path.exists():
        raise ReadoutSourceError(f"readout source does not exist: {source_path}")
    repo_root = _find_repo_root(source_path)
    _require_under_repo(source_path, repo_root, "suite readout source")
    payload = _read_json(source_path)
    if payload.get("evaluation_id") != SUITE_ID:
        raise ReadoutSourceError(
            f"expected suite id {SUITE_ID!r}, got {payload.get('evaluation_id')!r}"
        )
    readout_surface = _repo_path(
        payload.get("repo_readout_surface"), repo_root, "repo_readout_surface"
    )
    artifact_root = _repo_path(
        payload.get("source_artifact_root"), repo_root, "source_artifact_root"
    )
    evaluation_root = _repo_path(
        payload.get("source_evaluation_root"), repo_root, "source_evaluation_root"
    )
    source_files = _source_files(payload.get("source_files"), repo_root)
    status_rows = _read_csv(source_files.get("aggregate_table"))
    status_by_stage = {row.get("stage_id", ""): row for row in status_rows}
    stage_paths = [Path(str(item)).expanduser().resolve() for item in payload.get(
        "stage_readout_source_paths", []
    )]
    stage_by_id: dict[str, dict[str, object]] = {}
    for stage_path in stage_paths:
        if not stage_path.exists():
            continue
        _require_under_repo(stage_path, repo_root, "stage readout source")
        stage_payload = _read_json(stage_path)
        stage_by_id[str(stage_payload.get("evaluation_id", ""))] = {
            "path": stage_path,
            "payload": stage_payload,
        }
    stage_records = tuple(
        _stage_record(stage_def, status_by_stage.get(stage_def.stage_id), stage_by_id, repo_root)
        for stage_def in STAGE_DEFINITIONS
    )
    return SuiteReadoutSource(
        path=source_path,
        repo_root=repo_root,
        repo_readout_surface=readout_surface,
        source_artifact_root=artifact_root,
        source_evaluation_root=evaluation_root,
        source_files=source_files,
        run_label=str(payload.get("artifact_run_label", "")),
        stage_records=stage_records,
        status_rows=status_rows,
    )


def read_stage_table(record: StageSourceRecord, table_name: str) -> list[dict[str, str]]:
    """Read a table from a validated stage record if present."""

    path = record.source_files.get(table_name)
    if path is None or not path.exists():
        return []
    return _read_csv(path)


def _stage_record(
    stage_def: object,
    status_row: dict[str, str] | None,
    stage_by_id: dict[str, dict[str, object]],
    repo_root: Path,
) -> StageSourceRecord:
    stage_id = stage_def.stage_id
    source = stage_by_id.get(stage_id)
    stage_payload = source["payload"] if source is not None else {}
    source_files = _source_files(stage_payload.get("source_files"), repo_root)
    artifact_root = None
    if stage_payload.get("source_artifact_root"):
        artifact_root = _repo_path(
            stage_payload.get("source_artifact_root"),
            repo_root,
            f"{stage_id} source_artifact_root",
        )
    if status_row is None:
        return StageSourceRecord(
            stage_number=stage_def.stage_number,
            stage_id=stage_id,
            short_name=stage_def.short_name,
            readout_source_path=source["path"] if source is not None else None,
            status="not_run",
            claim_status="not_run",
            claim_boundary="stage has no suite status row",
            source_artifact_root=artifact_root,
            source_files=source_files,
            blocking_reason="stage status row missing",
        )
    return StageSourceRecord(
        stage_number=stage_def.stage_number,
        stage_id=stage_id,
        short_name=stage_def.short_name,
        readout_source_path=source["path"] if source is not None else None,
        status=str(status_row.get("status", "")),
        claim_status=str(status_row.get("claim_status", "")),
        claim_boundary=str(status_row.get("claim_boundary", "")),
        source_artifact_root=artifact_root,
        source_files=source_files,
        blocking_reason=str(status_row.get("blocking_reason", "")),
    )


def _source_files(value: object, repo_root: Path) -> dict[str, Path]:
    if not isinstance(value, dict):
        return {}
    result: dict[str, Path] = {}
    for key, raw in value.items():
        path = Path(str(raw)).expanduser().resolve()
        _require_under_repo(path, repo_root, f"source file {key}")
        result[str(key)] = path
    return result


def _repo_path(value: object, repo_root: Path, label: str) -> Path:
    path = Path(str(value)).expanduser().resolve()
    _require_under_repo(path, repo_root, label)
    return path


def _require_under_repo(path: Path, repo_root: Path, label: str) -> None:
    try:
        path.relative_to(repo_root)
    except ValueError as exc:
        raise ReadoutSourceError(f"{label} is outside repository: {path}") from exc


def _find_repo_root(path: Path) -> Path:
    for parent in (path, *path.parents):
        if (parent / "pyproject.toml").exists() and (parent / "src").exists():
            return parent
    raise ReadoutSourceError(f"could not locate repository root for {path}")


def _read_json(path: Path) -> dict[str, object]:
    with path.open(encoding="utf-8") as handle:
        payload = json.load(handle)
    if not isinstance(payload, dict):
        raise ReadoutSourceError(f"expected JSON object in {path}")
    return payload


def _read_csv(path: Path | None) -> list[dict[str, str]]:
    if path is None or not path.exists():
        return []
    with path.open(encoding="utf-8", newline="") as handle:
        return list(csv.DictReader(handle))
