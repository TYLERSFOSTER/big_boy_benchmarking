"""Source loading for PlateSupport gauntlet Stage 5."""

from __future__ import annotations

import csv
import json
from dataclasses import dataclass
from pathlib import Path

from ..ids import (
    STRUCTURAL_TOWER_DIAGNOSTICS_STAGE_ID,
    TOWER_TRAINING_HEALTH_STAGE_ID,
)
from ..paths import suite_readout_surface

REQUIRED_STAGE4_TABLES = (
    "training_episode_summary",
    "training_curve_summary",
    "concrete_step_summary",
    "candidate_training_health_summary",
    "downstream_comparison_input_summary",
)

REQUIRED_STAGE4_COLUMNS = {
    "training_episode_summary": (
        "candidate_id",
        "schema_id",
        "run_id",
        "replicate_index",
        "episode_index",
        "episode_seed",
        "status",
        "step_count",
        "total_reward",
        "terminated",
        "truncated",
        "goal_reached",
        "blocked_reason",
    ),
    "training_curve_summary": (
        "candidate_id",
        "schema_id",
        "episode_index",
        "episode_count",
        "mean_total_reward",
        "success_rate",
        "mean_step_count",
    ),
    "concrete_step_summary": (
        "candidate_id",
        "schema_id",
        "run_count",
        "concrete_step_count",
        "valid_step_count",
        "invalid_move_count",
        "self_transition_count",
        "terminal_step_count",
    ),
    "candidate_training_health_summary": (
        "candidate_id",
        "schema_id",
        "episode_count",
        "success_count",
        "concrete_step_count",
        "lift_success_count",
        "learner_update_count",
        "runtime_failure_count",
        "blocked_controller_step_count",
        "artifact_complete",
        "health_status",
        "health_reason",
    ),
    "downstream_comparison_input_summary": (
        "candidate_id",
        "schema_id",
        "health_status",
        "allowed_downstream_stage",
        "stage5_threshold_frontier_calibration",
        "stage6_paired_replicate_comparison",
        "source_artifact_root",
    ),
}

REQUIRED_STAGE1_TABLES = (
    "shortest_path_summary",
    "random_policy_recon_summary",
    "state_space_summary",
    "transition_summary",
)


@dataclass(frozen=True)
class TrainableCandidate:
    """Candidate admitted from Stage 4 into Stage 5 calibration."""

    candidate_id: str
    schema_id: str
    health_status: str
    health_reason: str
    schema_mode: str
    ratio_numerator: int
    ratio_denominator: int
    max_iterations: int
    selector_rule_id: str
    selection_mode: str
    max_depth: int
    nontrivial_tier_count: int
    episode_count: int
    success_count: int
    source_artifact_root: Path


@dataclass(frozen=True)
class Stage4TrainingHealthSource:
    """Validated Stage 4 readout source and trace tables."""

    path: Path
    repo_root: Path
    repo_readout_surface: Path
    source_artifact_root: Path
    source_files: dict[str, Path]
    trainable_candidates: tuple[TrainableCandidate, ...]
    tables: dict[str, list[dict[str, str]]]


@dataclass(frozen=True)
class Stage1StructuralContext:
    """PlateSupport structural and reward facts consumed by calibration."""

    path: Path
    repo_root: Path
    repo_readout_surface: Path
    source_artifact_root: Path
    source_files: dict[str, Path]
    shortest_path_length: int
    total_shortest_path_reward: float
    max_steps_per_episode: int
    random_policy_success_rate: float
    random_policy_mean_reward: float
    random_policy_invalid_move_rate: float
    valid_state_count: int
    reachable_state_count: int
    transition_count: int
    valid_transition_count: int
    invalid_move_count: int
    valid_self_transition_count: int


class Stage5SourceError(ValueError):
    """Raised when Stage 5 cannot safely consume an upstream source."""


def load_stage4_training_health_source(
    path: Path | str,
    *,
    repo_root: Path | str,
    allow_warning_candidates: bool,
    candidate_cap: int,
) -> Stage4TrainingHealthSource:
    """Load and validate Stage 4 training-health artifacts."""

    root = Path(repo_root).expanduser().resolve()
    source_path = Path(path).expanduser().resolve()
    _require_under_repo(source_path, root, "Stage 4 source")
    payload = _read_json(source_path, "Stage 4 source")
    if payload.get("evaluation_id") != TOWER_TRAINING_HEALTH_STAGE_ID:
        raise Stage5SourceError(
            f"expected Stage 4 source, got {payload.get('evaluation_id')!r}"
        )
    readout_surface = _repo_path(
        payload.get("repo_readout_surface"),
        root,
        "Stage 4 readout surface",
    )
    artifact_root = _repo_path(
        payload.get("source_artifact_root"),
        root,
        "Stage 4 artifact root",
    )
    source_files = _resolve_required_source_files(
        payload.get("source_files"),
        root,
        REQUIRED_STAGE4_TABLES,
        "Stage 4",
    )
    tables = {
        table_name: _read_csv_with_columns(
            source_files[table_name],
            REQUIRED_STAGE4_COLUMNS[table_name],
            f"Stage 4 {table_name}",
        )
        for table_name in REQUIRED_STAGE4_TABLES
    }
    candidates = _select_trainable_candidates(
        tables["candidate_training_health_summary"],
        tables["downstream_comparison_input_summary"],
        allow_warning_candidates=allow_warning_candidates,
        candidate_cap=candidate_cap,
        repo_root=root,
    )
    if not candidates:
        raise Stage5SourceError("Stage 4 has no trainable candidate for Stage 5")
    candidate_ids = {candidate.candidate_id for candidate in candidates}
    episode_rows = [
        row
        for row in tables["training_episode_summary"]
        if str(row["candidate_id"]) in candidate_ids
    ]
    if not episode_rows:
        raise Stage5SourceError("Stage 4 trainable candidate has no episode traces")
    tables = {**tables, "training_episode_summary": episode_rows}
    return Stage4TrainingHealthSource(
        path=source_path,
        repo_root=root,
        repo_readout_surface=readout_surface,
        source_artifact_root=artifact_root,
        source_files=source_files,
        trainable_candidates=tuple(candidates),
        tables=tables,
    )


def load_stage1_structural_context(
    path: Path | str,
    *,
    repo_root: Path | str,
) -> Stage1StructuralContext:
    """Load Stage 1 structural/reward context used to explain thresholds."""

    root = Path(repo_root).expanduser().resolve()
    source_path = Path(path).expanduser().resolve()
    _require_under_repo(source_path, root, "Stage 1 source")
    payload = _read_json(source_path, "Stage 1 source")
    if payload.get("evaluation_id") != STRUCTURAL_TOWER_DIAGNOSTICS_STAGE_ID:
        raise Stage5SourceError(
            f"expected Stage 1 source, got {payload.get('evaluation_id')!r}"
        )
    readout_surface = _repo_path(
        payload.get("repo_readout_surface"),
        root,
        "Stage 1 readout surface",
    )
    artifact_root = _repo_path(
        payload.get("source_artifact_root"),
        root,
        "Stage 1 artifact root",
    )
    source_files = _resolve_required_source_files(
        payload.get("source_files"),
        root,
        REQUIRED_STAGE1_TABLES,
        "Stage 1",
    )
    shortest_path_rows = _read_csv_with_columns(
        source_files["shortest_path_summary"],
        ("shortest_path_length", "total_shortest_path_reward"),
        "Stage 1 shortest_path_summary",
    )
    random_rows = _read_csv_with_columns(
        source_files["random_policy_recon_summary"],
        (
            "max_steps_per_episode",
            "success_rate",
            "mean_total_reward",
            "invalid_move_rate",
        ),
        "Stage 1 random_policy_recon_summary",
    )
    state_rows = _read_csv_with_columns(
        source_files["state_space_summary"],
        ("valid_state_count", "reachable_state_count"),
        "Stage 1 state_space_summary",
    )
    transition_rows = _read_csv_with_columns(
        source_files["transition_summary"],
        ("valid_transition", "invalid_move", "valid_self_transition"),
        "Stage 1 transition_summary",
    )
    shortest_path = shortest_path_rows[0]
    random_policy = random_rows[0]
    state_space = state_rows[0]
    return Stage1StructuralContext(
        path=source_path,
        repo_root=root,
        repo_readout_surface=readout_surface,
        source_artifact_root=artifact_root,
        source_files=source_files,
        shortest_path_length=int(shortest_path["shortest_path_length"]),
        total_shortest_path_reward=float(shortest_path["total_shortest_path_reward"]),
        max_steps_per_episode=int(random_policy["max_steps_per_episode"]),
        random_policy_success_rate=float(random_policy["success_rate"]),
        random_policy_mean_reward=float(random_policy["mean_total_reward"]),
        random_policy_invalid_move_rate=float(random_policy["invalid_move_rate"]),
        valid_state_count=int(state_space["valid_state_count"]),
        reachable_state_count=int(state_space["reachable_state_count"]),
        transition_count=len(transition_rows),
        valid_transition_count=sum(_truthy(row["valid_transition"]) for row in transition_rows),
        invalid_move_count=sum(_truthy(row["invalid_move"]) for row in transition_rows),
        valid_self_transition_count=sum(
            _truthy(row["valid_self_transition"]) for row in transition_rows
        ),
    )


def default_stage1_source_for_stage4(
    stage4_source: Stage4TrainingHealthSource,
) -> Path:
    """Return the default sibling Stage 1 readout source for a Stage 4 source."""

    return (
        suite_readout_surface(stage4_source.repo_root)
        / "structural_and_tower_diagnostics"
        / "readout_source.json"
    )


def _select_trainable_candidates(
    health_rows: list[dict[str, str]],
    downstream_rows: list[dict[str, str]],
    *,
    allow_warning_candidates: bool,
    candidate_cap: int,
    repo_root: Path,
) -> list[TrainableCandidate]:
    downstream_by_candidate = {row["candidate_id"]: row for row in downstream_rows}
    allowed_statuses = {"trainable_clean"}
    if allow_warning_candidates:
        allowed_statuses.add("trainable_warning")
    candidates: list[TrainableCandidate] = []
    for row in health_rows:
        health_status = str(row["health_status"])
        if health_status not in allowed_statuses:
            continue
        downstream = downstream_by_candidate.get(row["candidate_id"])
        if downstream is None:
            raise Stage5SourceError(
                f"candidate {row['candidate_id']} is missing Stage 4 downstream row"
            )
        if downstream.get("stage5_threshold_frontier_calibration") != "allowed":
            raise Stage5SourceError(
                f"candidate {row['candidate_id']} is not allowed into Stage 5"
            )
        source_artifact_root = _repo_path(
            downstream.get("source_artifact_root"),
            repo_root,
            f"candidate {row['candidate_id']} source artifact root",
        )
        candidates.append(
            TrainableCandidate(
                candidate_id=str(row["candidate_id"]),
                schema_id=str(row["schema_id"]),
                health_status=health_status,
                health_reason=str(row["health_reason"]),
                schema_mode=str(row.get("schema_mode", "source_local_ratio")),
                ratio_numerator=_int_or_zero(row.get("ratio_numerator")),
                ratio_denominator=_int_or_zero(row.get("ratio_denominator")),
                max_iterations=_int_or_zero(row.get("max_iterations")),
                selector_rule_id=str(row.get("selector_rule_id", "not_applicable")),
                selection_mode=str(row.get("selection_mode", "not_applicable")),
                max_depth=_int_or_zero(row.get("max_depth")),
                nontrivial_tier_count=_int_or_zero(row.get("nontrivial_tier_count")),
                episode_count=int(row["episode_count"]),
                success_count=int(row["success_count"]),
                source_artifact_root=source_artifact_root,
            )
        )
    return candidates[:candidate_cap]


def _resolve_required_source_files(
    payload: object,
    repo_root: Path,
    required_tables: tuple[str, ...],
    label: str,
) -> dict[str, Path]:
    if not isinstance(payload, dict):
        raise Stage5SourceError(f"{label} source_files must be a mapping")
    source_files: dict[str, Path] = {}
    for table_name in required_tables:
        source_files[table_name] = _repo_path(
            payload.get(table_name),
            repo_root,
            f"{label} {table_name}",
        )
    return source_files


def _read_csv_with_columns(
    path: Path,
    required_columns: tuple[str, ...],
    label: str,
) -> list[dict[str, str]]:
    if not path.exists():
        raise Stage5SourceError(f"{label} table is missing: {path}")
    with path.open(encoding="utf-8", newline="") as handle:
        reader = csv.DictReader(handle)
        fieldnames = set(reader.fieldnames or ())
        missing = [field for field in required_columns if field not in fieldnames]
        if missing:
            raise Stage5SourceError(f"{label} table is missing columns: {missing}")
        return list(reader)


def _read_json(path: Path, label: str) -> dict[str, object]:
    if not path.exists():
        raise Stage5SourceError(f"{label} does not exist: {path}")
    with path.open(encoding="utf-8") as handle:
        payload = json.load(handle)
    if not isinstance(payload, dict):
        raise Stage5SourceError(f"{label} must be a JSON object")
    return payload


def _repo_path(value: object, repo_root: Path, label: str) -> Path:
    if value in (None, ""):
        raise Stage5SourceError(f"{label} path is missing")
    path = Path(str(value)).expanduser().resolve()
    _require_under_repo(path, repo_root, label)
    if not path.exists():
        raise Stage5SourceError(f"{label} path does not exist: {path}")
    return path


def _require_under_repo(path: Path, repo_root: Path, label: str) -> None:
    try:
        path.relative_to(repo_root)
    except ValueError as exc:
        raise Stage5SourceError(f"{label} is outside repository: {path}") from exc


def _truthy(value: object) -> bool:
    return str(value).strip().lower() in {"1", "true", "yes"}


def _int_or_zero(value: object) -> int:
    text = str(value or "")
    return int(text) if text.isdigit() else 0
