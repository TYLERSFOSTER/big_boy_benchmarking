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
SOURCE_LOCAL_RATIO_ITERATED_RE = re.compile(
    r"^plate_support_schema_source_local_ratio_iterated_(?P<numerator>\d+)_over_"
    r"(?P<denominator>\d+)_i(?P<max_iterations>\d+)_v001$"
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
    schema_mode: str
    selection_rate: str
    ratio_numerator: int
    ratio_denominator: int
    max_iterations: int
    selector_rule_id: str
    selection_mode: str
    max_depth: int
    nontrivial_tier_count: int


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
        parsed = _candidate_schema_metadata(row, schema_id=schema_id)
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
                schema_mode=parsed["schema_mode"],
                selection_rate=parsed["selection_rate"],
                ratio_numerator=int(parsed["ratio_numerator"]),
                ratio_denominator=int(parsed["ratio_denominator"]),
                max_iterations=int(parsed["max_iterations"]),
                selector_rule_id=parsed["selector_rule_id"],
                selection_mode=parsed["selection_mode"],
                max_depth=_int_or_zero(row.get("max_depth")),
                nontrivial_tier_count=_int_or_zero(row.get("nontrivial_tier_count")),
            )
        )
    return candidates[:candidate_cap]


def _candidate_schema_metadata(
    row: dict[str, str],
    *,
    schema_id: str,
) -> dict[str, object]:
    schema_mode = str(row.get("schema_mode", ""))
    selection_rate = str(row.get("selection_rate", ""))
    numerator = _optional_int(row.get("ratio_numerator"))
    denominator = _optional_int(row.get("ratio_denominator"))
    max_iterations = _optional_int(row.get("max_iterations"))
    selector_rule_id = str(row.get("selector_rule_id", "") or "not_applicable")
    selection_mode = str(row.get("selection_mode", "") or "not_applicable")
    if schema_mode and numerator is not None and denominator is not None:
        return {
            "schema_mode": schema_mode,
            "selection_rate": selection_rate or f"{numerator}/{denominator}",
            "ratio_numerator": numerator,
            "ratio_denominator": denominator,
            "max_iterations": (
                max_iterations if max_iterations is not None else _default_iteration_cap(schema_mode)
            ),
            "selector_rule_id": selector_rule_id,
            "selection_mode": selection_mode,
        }
    return _parse_supported_schema_id(schema_id)


def _parse_supported_schema_id(schema_id: str) -> dict[str, object]:
    iterated_match = SOURCE_LOCAL_RATIO_ITERATED_RE.match(schema_id)
    if iterated_match:
        numerator = int(iterated_match.group("numerator"))
        denominator = int(iterated_match.group("denominator"))
        max_iterations = int(iterated_match.group("max_iterations"))
        return {
            "schema_mode": "source_local_ratio_iterated",
            "selection_rate": f"{numerator}/{denominator}",
            "ratio_numerator": numerator,
            "ratio_denominator": denominator,
            "max_iterations": max_iterations,
            "selector_rule_id": "plate_support_source_local_iterated_stable_rate_v001",
            "selection_mode": "quotient_source_representative_stable_rate",
        }
    match = SOURCE_LOCAL_RATIO_RE.match(schema_id)
    if not match:
        raise Stage3CandidateSourceError(
            "Stage 4 currently supports source-local ratio and iterated "
            "source-local ratio candidates only; "
            f"got schema_id={schema_id!r}"
        )
    numerator = int(match.group("numerator"))
    denominator = int(match.group("denominator"))
    return {
        "schema_mode": "source_local_ratio",
        "selection_rate": f"{numerator}/{denominator}",
        "ratio_numerator": numerator,
        "ratio_denominator": denominator,
        "max_iterations": 1,
        "selector_rule_id": "source_local_outgoing_ratio_catch",
        "selection_mode": "legacy_source_local_ceil_prefix",
    }


def _optional_int(value: object) -> int | None:
    text = str(value or "")
    return int(text) if text.isdigit() else None


def _int_or_zero(value: object) -> int:
    text = str(value or "")
    return int(text) if text.isdigit() else 0


def _default_iteration_cap(schema_mode: str) -> int:
    return 1 if schema_mode == "source_local_ratio" else 32


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
