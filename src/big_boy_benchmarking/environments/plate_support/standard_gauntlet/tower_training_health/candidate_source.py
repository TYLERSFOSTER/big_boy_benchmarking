"""Stage 3 candidate-source loading for tower training health."""

from __future__ import annotations

import csv
import json
import re
from dataclasses import dataclass
from pathlib import Path

from ..ids import (
    CANDIDATE_DISCOVERY_STAGE_ID,
)

REQUIRED_STAGE3_TABLES = (
    "selected_candidate_summary",
    "candidate_source_trace",
    "downstream_training_health_input_summary",
)

SOURCE_LOCAL_RATIO_RE = re.compile(
    r"^plate_support_schema_source_local_ratio_(?P<numerator>\d+)_over_"
    r"(?P<denominator>\d+)_v001$"
)


@dataclass(frozen=True)
class TrainingCandidate:
    """Validated candidate row selected by Stage 3 for Stage 4."""

    candidate_id: str
    schema_id: str
    schema_family_id: str
    schema_seed: int
    selection_status: str
    allowed_downstream_stage: str
    source_artifact_root: Path
    ratio_numerator: int
    ratio_denominator: int


@dataclass(frozen=True)
class Stage3CandidateSource:
    """Validated Stage 3 readout source and selected candidates."""

    path: Path
    repo_root: Path
    repo_readout_surface: Path
    source_artifact_root: Path
    source_files: dict[str, Path]
    candidate_manifest_path: Path
    selected_candidates: tuple[TrainingCandidate, ...]


class Stage3CandidateSourceError(ValueError):
    """Raised when Stage 3 cannot safely feed Stage 4."""


def load_stage3_candidate_source(
    path: Path | str,
    *,
    repo_root: Path | str,
    allow_warning_candidates: bool = False,
    candidate_cap: int = 2,
) -> Stage3CandidateSource:
    """Load Stage 3 readout source and validate selected training candidates."""

    root = Path(repo_root).expanduser().resolve()
    source_path = Path(path).expanduser().resolve()
    _require_under_repo(source_path, root, "Stage 3 source")
    if not source_path.exists():
        raise Stage3CandidateSourceError(
            f"Stage 3 readout source does not exist: {source_path}"
        )
    with source_path.open(encoding="utf-8") as handle:
        payload = json.load(handle)
    if payload.get("evaluation_id") != CANDIDATE_DISCOVERY_STAGE_ID:
        raise Stage3CandidateSourceError(
            f"expected Stage 3 source, got {payload.get('evaluation_id')!r}"
        )
    readout_surface = Path(str(payload["repo_readout_surface"])).expanduser().resolve()
    artifact_root = Path(str(payload["source_artifact_root"])).expanduser().resolve()
    _require_under_repo(readout_surface, root, "Stage 3 readout surface")
    _require_under_repo(artifact_root, root, "Stage 3 artifact root")
    source_files_payload = payload.get("source_files", {})
    if not isinstance(source_files_payload, dict):
        raise Stage3CandidateSourceError("Stage 3 source_files must be a mapping")
    source_files: dict[str, Path] = {}
    for table_name in REQUIRED_STAGE3_TABLES:
        table_path = Path(str(source_files_payload.get(table_name, ""))).expanduser().resolve()
        _require_under_repo(table_path, root, f"Stage 3 {table_name}")
        if not table_path.exists():
            raise Stage3CandidateSourceError(f"required Stage 3 table missing: {table_path}")
        source_files[table_name] = table_path
    candidate_manifest_path = artifact_root / "candidate_manifest.json"
    _require_under_repo(candidate_manifest_path, root, "Stage 3 candidate manifest")
    if not candidate_manifest_path.exists():
        raise Stage3CandidateSourceError("Stage 3 candidate manifest is missing")
    selected_candidates = _load_selected_candidates(
        source_files["downstream_training_health_input_summary"],
        repo_root=root,
        allow_warning_candidates=allow_warning_candidates,
        candidate_cap=candidate_cap,
    )
    if not selected_candidates:
        raise Stage3CandidateSourceError("Stage 3 has no selected training candidate rows")
    return Stage3CandidateSource(
        path=source_path,
        repo_root=root,
        repo_readout_surface=readout_surface,
        source_artifact_root=artifact_root,
        source_files=source_files,
        candidate_manifest_path=candidate_manifest_path,
        selected_candidates=tuple(selected_candidates),
    )


def _load_selected_candidates(
    path: Path,
    *,
    repo_root: Path,
    allow_warning_candidates: bool,
    candidate_cap: int,
) -> list[TrainingCandidate]:
    with path.open(encoding="utf-8", newline="") as handle:
        rows = list(csv.DictReader(handle))
    allowed_statuses = {"selected_training_candidate"}
    if allow_warning_candidates:
        allowed_statuses.add("selected_warning_candidate")
    candidates: list[TrainingCandidate] = []
    for row in rows:
        status = str(row.get("selection_status", ""))
        if status not in allowed_statuses:
            continue
        downstream = str(row.get("allowed_downstream_stage", ""))
        if downstream != "stage4_training_health":
            raise Stage3CandidateSourceError(
                f"candidate {row.get('candidate_id')} has invalid downstream stage {downstream!r}"
            )
        schema_id = str(row.get("schema_id", ""))
        parsed = _parse_source_local_ratio_schema_id(schema_id)
        source_artifact_root = Path(str(row.get("source_artifact_root", ""))).expanduser().resolve()
        _require_under_repo(
            source_artifact_root,
            repo_root,
            f"candidate {row.get('candidate_id')} source artifact root",
        )
        if not source_artifact_root.exists():
            raise Stage3CandidateSourceError(
                f"candidate source artifact root does not exist: {source_artifact_root}"
            )
        candidates.append(
            TrainingCandidate(
                candidate_id=str(row["candidate_id"]),
                schema_id=schema_id,
                schema_family_id=str(row["schema_family_id"]),
                schema_seed=int(row["schema_seed"]),
                selection_status=status,
                allowed_downstream_stage=downstream,
                source_artifact_root=source_artifact_root,
                ratio_numerator=parsed[0],
                ratio_denominator=parsed[1],
            )
        )
    return candidates[:candidate_cap]


def _parse_source_local_ratio_schema_id(schema_id: str) -> tuple[int, int]:
    match = SOURCE_LOCAL_RATIO_RE.match(schema_id)
    if not match:
        raise Stage3CandidateSourceError(
            "Stage 4 currently supports source-local ratio candidates only; "
            f"got schema_id={schema_id!r}"
        )
    return int(match.group("numerator")), int(match.group("denominator"))


def read_stage3_table(source: Stage3CandidateSource, table_name: str) -> list[dict[str, str]]:
    """Read a validated Stage 3 table."""

    if table_name not in source.source_files:
        raise Stage3CandidateSourceError(f"Stage 3 table not registered: {table_name}")
    with source.source_files[table_name].open(encoding="utf-8", newline="") as handle:
        return list(csv.DictReader(handle))


def _require_under_repo(path: Path, repo_root: Path, label: str) -> None:
    try:
        path.relative_to(repo_root)
    except ValueError as exc:
        raise Stage3CandidateSourceError(f"{label} is outside repository: {path}") from exc
