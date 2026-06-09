"""Parent-source loading for the PlateSupport tower-star diagnostic."""

from __future__ import annotations

import csv
import json
import re
from dataclasses import dataclass
from pathlib import Path

from big_boy_benchmarking.environments.plate_support.standard_gauntlet.ids import (
    CANDIDATE_DISCOVERY_STAGE_ID,
    PAIRED_REPLICATE_COMPARISON_STAGE_ID,
    THRESHOLD_FRONTIER_CALIBRATION_STAGE_ID,
    TOWER_TRAINING_HEALTH_STAGE_ID,
)
from big_boy_benchmarking.environments.plate_support.standard_gauntlet.tower_training_health.candidate_source import (
    TrainingCandidate,
)
from big_boy_benchmarking.upstream.state_collapser import (
    STATE_COLLAPSER_DEPENDENCY_SPEC,
    collect_state_collapser_dependency_state,
)

from .paths import resolve_repo_placeholder

MINIMUM_STATE_COLLAPSER_VERSION = (0, 7, 2)

ITERATED_SCHEMA_RE = re.compile(
    r"^plate_support_schema_source_local_ratio_iterated_(?P<numerator>\d+)_over_"
    r"(?P<denominator>\d+)_i(?P<max_iterations>\d+)_v001$"
)
ONE_SHOT_SCHEMA_RE = re.compile(
    r"^plate_support_schema_source_local_ratio_(?P<numerator>\d+)_over_"
    r"(?P<denominator>\d+)_v001$"
)


@dataclass(frozen=True)
class ParentSourceBinding:
    """One resolved parent stage readout binding."""

    repo_root: Path
    path: Path
    payload: dict[str, object]
    source_files: dict[str, Path]
    source_artifact_root: Path
    artifact_storage: dict[str, object]


@dataclass(frozen=True)
class TowerStarParentSources:
    """Validated parent evidence needed by the tower-star diagnostic."""

    suite_source_path: Path
    direct_star_source_path: Path
    direct_star_payload: dict[str, object]
    stage3: ParentSourceBinding
    stage4: ParentSourceBinding
    stage5: ParentSourceBinding
    stage6: ParentSourceBinding
    selected_candidate: TrainingCandidate
    target: dict[str, object]
    parent_episodes_per_replicate: int
    parent_replicates_per_arm: int
    dependency_state: dict[str, object]


class TowerStarParentSourceError(ValueError):
    """Raised when the parent gauntlet source cannot support this diagnostic."""


def load_tower_star_parent_sources(
    *,
    parent_gauntlet_source: Path | str,
    direct_star_source: Path | str,
    repo_root: Path | str,
) -> TowerStarParentSources:
    """Load the standard-gauntlet source and selected Stage 6 inputs."""

    root = Path(repo_root).expanduser().resolve()
    suite_path = Path(parent_gauntlet_source).expanduser().resolve()
    direct_star_path = Path(direct_star_source).expanduser().resolve()
    _require_under_repo(suite_path, root, "parent gauntlet readout source")
    _require_under_repo(direct_star_path, root, "direct-star readout source")
    suite_payload = _read_json(suite_path)
    direct_star_payload = _read_json(direct_star_path)
    _validate_direct_star_source(direct_star_payload, root)
    stage_paths = suite_payload.get("stage_readout_source_paths")
    if not isinstance(stage_paths, list):
        raise TowerStarParentSourceError(
            "parent gauntlet readout source lacks stage_readout_source_paths"
        )
    stages: dict[str, ParentSourceBinding] = {}
    for raw_path in stage_paths:
        path = resolve_repo_placeholder(raw_path, root)
        payload = _read_json(path)
        evaluation_id = str(payload.get("evaluation_id", ""))
        stages[evaluation_id] = _resolve_stage_binding(path, payload, root)
    required = {
        CANDIDATE_DISCOVERY_STAGE_ID: "Stage 3 candidate discovery",
        TOWER_TRAINING_HEALTH_STAGE_ID: "Stage 4 tower training health",
        THRESHOLD_FRONTIER_CALIBRATION_STAGE_ID: "Stage 5 threshold calibration",
        PAIRED_REPLICATE_COMPARISON_STAGE_ID: "Stage 6 paired comparison",
    }
    for stage_id, label in required.items():
        if stage_id not in stages:
            raise TowerStarParentSourceError(f"missing {label} readout source")
    stage3 = stages[CANDIDATE_DISCOVERY_STAGE_ID]
    stage4 = stages[TOWER_TRAINING_HEALTH_STAGE_ID]
    stage5 = stages[THRESHOLD_FRONTIER_CALIBRATION_STAGE_ID]
    stage6 = stages[PAIRED_REPLICATE_COMPARISON_STAGE_ID]
    candidate = _select_parent_candidate(stage3, stage4)
    target = _load_parent_target(stage5)
    dependency_state = collect_state_collapser_dependency_state(
        dependency_spec=STATE_COLLAPSER_DEPENDENCY_SPEC,
    ).to_dict()
    _enforce_dependency_version(dependency_state)
    return TowerStarParentSources(
        suite_source_path=suite_path,
        direct_star_source_path=direct_star_path,
        direct_star_payload=direct_star_payload,
        stage3=stage3,
        stage4=stage4,
        stage5=stage5,
        stage6=stage6,
        selected_candidate=candidate,
        target=target,
        parent_episodes_per_replicate=_int_value(
            target.get("recommended_episodes_per_replicate"),
            fallback=32,
        ),
        parent_replicates_per_arm=_int_value(
            target.get("recommended_replicates_per_arm"),
            fallback=4,
        ),
        dependency_state=dependency_state,
    )


def _validate_direct_star_source(payload: dict[str, object], repo_root: Path) -> None:
    evaluation_id = str(payload.get("evaluation_id", ""))
    if evaluation_id != "plate_support_direct_star_culdesac_control_v001":
        raise TowerStarParentSourceError(
            "direct-star source has unexpected evaluation_id: "
            f"{evaluation_id!r}"
        )
    source_files = payload.get("source_files")
    if not isinstance(source_files, dict):
        raise TowerStarParentSourceError("direct-star source lacks source_files")
    required = (
        "arm_summary",
        "guard_filter_summary",
        "interpretation_summary",
        "paired_seed_bundle_summary",
    )
    for key in required:
        path = resolve_repo_placeholder(source_files.get(key, ""), repo_root)
        if not path.exists():
            raise TowerStarParentSourceError(
                f"direct-star source file for {key!r} is missing: {path}"
            )


def _resolve_stage_binding(
    path: Path,
    payload: dict[str, object],
    repo_root: Path,
) -> ParentSourceBinding:
    _require_under_repo(path, repo_root, "stage readout source")
    source_files_payload = payload.get("source_files")
    if not isinstance(source_files_payload, dict):
        raise TowerStarParentSourceError(f"stage source_files must be a mapping: {path}")
    source_files = {
        str(name): resolve_repo_placeholder(value, repo_root)
        for name, value in source_files_payload.items()
    }
    missing = [str(file_path) for file_path in source_files.values() if not file_path.exists()]
    if missing:
        storage = payload.get("artifact_storage", {})
        if isinstance(storage, dict) and storage.get("mode") == "github_release_asset":
            raise TowerStarParentSourceError(
                "parent source files are externalized in a GitHub release asset and "
                "are not currently present in the repo checkout. Restore the parent "
                "artifact tree before running this diagnostic. First missing file: "
                f"{missing[0]}"
            )
        raise TowerStarParentSourceError(f"required parent source file missing: {missing[0]}")
    artifact_root = resolve_repo_placeholder(payload.get("source_artifact_root"), repo_root)
    storage_payload = payload.get("artifact_storage", {})
    return ParentSourceBinding(
        repo_root=repo_root,
        path=path,
        payload=payload,
        source_files=source_files,
        source_artifact_root=artifact_root,
        artifact_storage=storage_payload if isinstance(storage_payload, dict) else {},
    )


def _select_parent_candidate(
    stage3: ParentSourceBinding,
    stage4: ParentSourceBinding,
) -> TrainingCandidate:
    stage3_rows = _read_csv(stage3.source_files["downstream_training_health_input_summary"])
    stage4_rows = _read_csv(stage4.source_files["candidate_training_health_summary"])
    trainable = {
        row.get("candidate_id")
        for row in stage4_rows
        if row.get("health_status") in {"trainable_clean", "trainable_warning"}
    }
    for row in stage3_rows:
        if row.get("candidate_id") not in trainable:
            continue
        if row.get("selection_status") not in {
            "selected_training_candidate",
            "selected_warning_candidate",
        }:
            continue
        return _candidate_from_row(row, repo_root=stage3.repo_root)
    raise TowerStarParentSourceError(
        "parent Stage 3 and Stage 4 do not share a trainable selected candidate"
    )


def _candidate_from_row(row: dict[str, str], *, repo_root: Path) -> TrainingCandidate:
    schema_id = str(row["schema_id"])
    metadata = _schema_metadata(row, schema_id)
    source_artifact_root = resolve_repo_placeholder(row.get("source_artifact_root", ""), repo_root)
    return TrainingCandidate(
        candidate_id=str(row["candidate_id"]),
        schema_id=schema_id,
        schema_family_id=str(row.get("schema_family_id", "")),
        schema_seed=_int_value(row.get("schema_seed"), fallback=0),
        selection_status=str(row.get("selection_status", "")),
        allowed_downstream_stage=str(row.get("allowed_downstream_stage", "")),
        source_artifact_root=source_artifact_root,
        schema_mode=str(metadata["schema_mode"]),
        selection_rate=str(metadata["selection_rate"]),
        ratio_numerator=int(metadata["ratio_numerator"]),
        ratio_denominator=int(metadata["ratio_denominator"]),
        max_iterations=int(metadata["max_iterations"]),
        selector_rule_id=str(metadata["selector_rule_id"]),
        selection_mode=str(metadata["selection_mode"]),
        max_depth=_int_value(row.get("max_depth"), fallback=0),
        nontrivial_tier_count=_int_value(row.get("nontrivial_tier_count"), fallback=0),
    )


def _schema_metadata(row: dict[str, str], schema_id: str) -> dict[str, object]:
    schema_mode = str(row.get("schema_mode", ""))
    numerator = _optional_int(row.get("ratio_numerator"))
    denominator = _optional_int(row.get("ratio_denominator"))
    max_iterations = _optional_int(row.get("max_iterations"))
    selector_rule_id = str(row.get("selector_rule_id", "") or "not_applicable")
    selection_mode = str(row.get("selection_mode", "") or "not_applicable")
    if schema_mode and numerator is not None and denominator is not None:
        return {
            "schema_mode": schema_mode,
            "selection_rate": row.get("selection_rate") or f"{numerator}/{denominator}",
            "ratio_numerator": numerator,
            "ratio_denominator": denominator,
            "max_iterations": max_iterations if max_iterations is not None else 32,
            "selector_rule_id": selector_rule_id,
            "selection_mode": selection_mode,
        }
    iterated = ITERATED_SCHEMA_RE.match(schema_id)
    if iterated:
        numerator = int(iterated.group("numerator"))
        denominator = int(iterated.group("denominator"))
        max_iterations = int(iterated.group("max_iterations"))
        return {
            "schema_mode": "source_local_ratio_iterated",
            "selection_rate": f"{numerator}/{denominator}",
            "ratio_numerator": numerator,
            "ratio_denominator": denominator,
            "max_iterations": max_iterations,
            "selector_rule_id": "plate_support_source_local_iterated_stable_rate_v001",
            "selection_mode": "quotient_source_representative_stable_rate",
        }
    one_shot = ONE_SHOT_SCHEMA_RE.match(schema_id)
    if one_shot:
        numerator = int(one_shot.group("numerator"))
        denominator = int(one_shot.group("denominator"))
        return {
            "schema_mode": "source_local_ratio",
            "selection_rate": f"{numerator}/{denominator}",
            "ratio_numerator": numerator,
            "ratio_denominator": denominator,
            "max_iterations": 1,
            "selector_rule_id": "source_local_outgoing_ratio_catch",
            "selection_mode": "legacy_source_local_ceil_prefix",
        }
    raise TowerStarParentSourceError(f"unsupported parent schema id: {schema_id!r}")


def _load_parent_target(stage5: ParentSourceBinding) -> dict[str, object]:
    rows: list[dict[str, str]] = []
    path = stage5.source_files.get("recommended_comparison_target")
    if path is not None and path.exists():
        rows = _read_csv(path)
    if rows:
        target: dict[str, object] = dict(rows[0])
    else:
        payload_target = stage5.payload.get("calibrated_target")
        if not isinstance(payload_target, dict):
            raise TowerStarParentSourceError("Stage 5 lacks calibrated target")
        target = dict(payload_target)
    if str(target.get("calibration_status")) != "threshold_calibrated":
        raise TowerStarParentSourceError(f"parent target is not calibrated: {target!r}")
    return target


def _enforce_dependency_version(dependency_state: dict[str, object]) -> None:
    raw_version = str(dependency_state.get("import_version", "0.0.0"))
    if _version_tuple(raw_version) < MINIMUM_STATE_COLLAPSER_VERSION:
        raise TowerStarParentSourceError(
            "tower-star diagnostic requires state_collapser v0.7.2+ pointwise "
            f"liftability semantics; got {raw_version}"
        )


def _version_tuple(value: str) -> tuple[int, int, int]:
    parts: list[int] = []
    for raw in value.split(".")[:3]:
        digits = "".join(character for character in raw if character.isdigit())
        parts.append(int(digits or "0"))
    while len(parts) < 3:
        parts.append(0)
    return (parts[0], parts[1], parts[2])


def _optional_int(value: object) -> int | None:
    text = str(value or "")
    return int(text) if text.isdigit() else None


def _int_value(value: object, *, fallback: int) -> int:
    text = str(value or "")
    return int(text) if text.isdigit() else fallback


def _read_json(path: Path) -> dict[str, object]:
    if not path.exists():
        raise TowerStarParentSourceError(f"readout source does not exist: {path}")
    with path.open(encoding="utf-8") as handle:
        payload = json.load(handle)
    if not isinstance(payload, dict):
        raise TowerStarParentSourceError(f"expected JSON object in {path}")
    return payload


def _read_csv(path: Path) -> list[dict[str, str]]:
    with path.open(encoding="utf-8", newline="") as handle:
        return list(csv.DictReader(handle))


def _require_under_repo(path: Path, repo_root: Path, label: str) -> None:
    try:
        path.relative_to(repo_root)
    except ValueError as exc:
        raise TowerStarParentSourceError(f"{label} is outside repository: {path}") from exc
