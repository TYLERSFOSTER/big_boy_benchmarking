"""Source loading for PlateSupport gauntlet Stage 6."""

from __future__ import annotations

import csv
import json
from dataclasses import dataclass
from pathlib import Path

from big_boy_benchmarking.upstream.state_collapser import (
    STATE_COLLAPSER_DEPENDENCY_SPEC,
    collect_state_collapser_dependency_state,
)

from ..ids import (
    THRESHOLD_FRONTIER_CALIBRATION_STAGE_ID,
)
from ..threshold_frontier_calibration.stage_sources import (
    Stage4TrainingHealthSource,
    Stage5SourceError,
    load_stage4_training_health_source,
)
from ..tower_training_health.candidate_source import (
    Stage3CandidateSource,
    Stage3CandidateSourceError,
    TrainingCandidate,
    load_stage3_candidate_source,
)

REQUIRED_STAGE5_TABLES = (
    "recommended_comparison_target",
    "downstream_paired_comparison_input_summary",
)

MINIMUM_STATE_COLLAPSER_VERSION = (0, 7, 2)


@dataclass(frozen=True)
class Stage5ThresholdSource:
    """Validated Stage 5 target source consumed by Stage 6."""

    path: Path
    repo_root: Path
    repo_readout_surface: Path
    source_artifact_root: Path
    source_files: dict[str, Path]
    recommended_target: dict[str, object]
    episodes_per_replicate: int
    replicates_per_arm: int
    downstream_allowed: bool


@dataclass(frozen=True)
class Stage6Sources:
    """All validated upstream source bindings for Stage 6."""

    stage3_source: Stage3CandidateSource
    stage4_source: Stage4TrainingHealthSource
    stage5_source: Stage5ThresholdSource
    selected_candidate: TrainingCandidate
    dependency_state: dict[str, object]


class Stage6SourceError(ValueError):
    """Raised when Stage 6 cannot safely consume upstream sources."""


def load_stage6_sources(
    *,
    candidate_source_path: Path | str,
    training_health_source_path: Path | str,
    threshold_source_path: Path | str,
    repo_root: Path | str,
    candidate_cap: int,
    allow_warning_candidates: bool,
    allow_legacy_dependency: bool,
) -> Stage6Sources:
    """Load and cross-check Stage 3, Stage 4, Stage 5, and dependency inputs."""

    root = Path(repo_root).expanduser().resolve()
    try:
        stage3_source = load_stage3_candidate_source(
            candidate_source_path,
            repo_root=root,
            allow_warning_candidates=allow_warning_candidates,
            candidate_cap=candidate_cap,
        )
    except Stage3CandidateSourceError as exc:
        raise Stage6SourceError(str(exc)) from exc
    try:
        stage4_source = load_stage4_training_health_source(
            training_health_source_path,
            repo_root=root,
            allow_warning_candidates=allow_warning_candidates,
            candidate_cap=candidate_cap,
        )
    except Stage5SourceError as exc:
        raise Stage6SourceError(str(exc)) from exc
    stage5_source = load_stage5_threshold_source(threshold_source_path, repo_root=root)
    candidate = _select_candidate(stage3_source, stage4_source)
    dependency_state = collect_state_collapser_dependency_state(
        dependency_spec=STATE_COLLAPSER_DEPENDENCY_SPEC,
    ).to_dict()
    _enforce_dependency_version(dependency_state, allow_legacy_dependency)
    return Stage6Sources(
        stage3_source=stage3_source,
        stage4_source=stage4_source,
        stage5_source=stage5_source,
        selected_candidate=candidate,
        dependency_state=dependency_state,
    )


def load_stage5_threshold_source(
    path: Path | str,
    *,
    repo_root: Path | str,
) -> Stage5ThresholdSource:
    """Load the Stage 5 threshold-calibration readout source."""

    root = Path(repo_root).expanduser().resolve()
    source_path = Path(path).expanduser().resolve()
    _require_under_repo(source_path, root, "Stage 5 source")
    if not source_path.exists():
        raise Stage6SourceError(f"Stage 5 readout source does not exist: {source_path}")
    payload = _read_json(source_path)
    if payload.get("evaluation_id") != THRESHOLD_FRONTIER_CALIBRATION_STAGE_ID:
        raise Stage6SourceError(
            f"expected Stage 5 source, got {payload.get('evaluation_id')!r}"
        )
    readout_surface = _repo_path(
        payload.get("repo_readout_surface"), root, "Stage 5 readout surface"
    )
    artifact_root = _repo_path(
        payload.get("source_artifact_root"), root, "Stage 5 artifact root"
    )
    source_files = _resolve_required_source_files(payload.get("source_files"), root)
    target_rows = _read_csv(source_files["recommended_comparison_target"])
    downstream_rows = _read_csv(source_files["downstream_paired_comparison_input_summary"])
    if not target_rows:
        raise Stage6SourceError("Stage 5 recommended target table is empty")
    target = dict(target_rows[0])
    if target.get("calibration_status") != "threshold_calibrated":
        raise Stage6SourceError(f"Stage 5 target is not calibrated: {target!r}")
    downstream_allowed = any(
        row.get("stage6_paired_replicate_comparison") == "allowed"
        for row in downstream_rows
    )
    if not downstream_allowed:
        reason = "; ".join(str(row.get("blocking_reason", "")) for row in downstream_rows)
        raise Stage6SourceError(f"Stage 5 downstream gate blocks Stage 6: {reason}")
    return Stage5ThresholdSource(
        path=source_path,
        repo_root=root,
        repo_readout_surface=readout_surface,
        source_artifact_root=artifact_root,
        source_files=source_files,
        recommended_target=target,
        episodes_per_replicate=int(target["recommended_episodes_per_replicate"]),
        replicates_per_arm=int(target["recommended_replicates_per_arm"]),
        downstream_allowed=downstream_allowed,
    )


def _select_candidate(
    stage3_source: Stage3CandidateSource,
    stage4_source: Stage4TrainingHealthSource,
) -> TrainingCandidate:
    trainable_ids = {
        candidate.candidate_id
        for candidate in stage4_source.trainable_candidates
        if candidate.health_status in {"trainable_clean", "trainable_warning"}
    }
    for candidate in stage3_source.selected_candidates:
        if candidate.candidate_id in trainable_ids:
            return candidate
    raise Stage6SourceError("Stage 3 and Stage 4 do not share a trainable candidate")


def _enforce_dependency_version(
    dependency_state: dict[str, object],
    allow_legacy_dependency: bool,
) -> None:
    if allow_legacy_dependency:
        return
    raw_version = str(dependency_state.get("import_version", "0.0.0"))
    if _version_tuple(raw_version) < MINIMUM_STATE_COLLAPSER_VERSION:
        raise Stage6SourceError(
            "Stage 6 requires state_collapser v0.7.2+ pointwise liftability "
            f"semantics; got {raw_version}"
        )


def _version_tuple(value: str) -> tuple[int, int, int]:
    parts = []
    for raw in value.split(".")[:3]:
        digits = "".join(character for character in raw if character.isdigit())
        parts.append(int(digits or "0"))
    while len(parts) < 3:
        parts.append(0)
    return tuple(parts)  # type: ignore[return-value]


def _resolve_required_source_files(
    value: object,
    repo_root: Path,
) -> dict[str, Path]:
    if not isinstance(value, dict):
        raise Stage6SourceError("Stage 5 source_files must be a mapping")
    result: dict[str, Path] = {}
    for table_name in REQUIRED_STAGE5_TABLES:
        table_path = _repo_path(value.get(table_name), repo_root, f"Stage 5 {table_name}")
        if not table_path.exists():
            raise Stage6SourceError(f"required Stage 5 table missing: {table_path}")
        result[table_name] = table_path
    return result


def _repo_path(value: object, repo_root: Path, label: str) -> Path:
    path = Path(str(value)).expanduser().resolve()
    _require_under_repo(path, repo_root, label)
    return path


def _require_under_repo(path: Path, repo_root: Path, label: str) -> None:
    try:
        path.relative_to(repo_root)
    except ValueError as exc:
        raise Stage6SourceError(f"{label} is outside repository: {path}") from exc


def _read_json(path: Path) -> dict[str, object]:
    with path.open(encoding="utf-8") as handle:
        payload = json.load(handle)
    if not isinstance(payload, dict):
        raise Stage6SourceError(f"expected JSON object in {path}")
    return payload


def _read_csv(path: Path) -> list[dict[str, str]]:
    with path.open(encoding="utf-8", newline="") as handle:
        return list(csv.DictReader(handle))
