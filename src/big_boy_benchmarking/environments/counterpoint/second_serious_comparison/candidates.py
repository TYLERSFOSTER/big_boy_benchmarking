"""Candidate loading for second serious schema comparison."""

from __future__ import annotations

import csv
import json
from dataclasses import asdict, dataclass
from pathlib import Path
from typing import Any

from big_boy_benchmarking.environments.counterpoint.noisy_rate_full_training.config import (
    NO_CONTRACTION_ARM_ID,
)
from big_boy_benchmarking.environments.counterpoint.second_serious_comparison.paths import (
    validate_repo_resident_path,
)


@dataclass(frozen=True)
class SchemaCandidate:
    candidate_id: str
    instance_id: str
    arm_id: str
    numerator: int
    denominator: int
    requested_rate: float
    selector_rule_id: str
    schema_seed: int
    tier_state_cell_count_sequence: str
    tier_active_action_cell_count_sequence: str
    parent_training_health_class: str
    parent_concrete_step_count: int
    parent_learner_update_count: int
    parent_status: str
    parent_run_id: str
    parent_evaluation_id: str
    parent_artifact_run_label: str
    selected_edge_count: int
    selected_edge_share: float
    selected_source_share: float | None
    zero_selected_source_count: int
    candidate_eligible: bool
    candidate_exclusion_reason: str | None

    def to_dict(self) -> dict[str, Any]:
        return asdict(self)


@dataclass(frozen=True)
class CandidateSelection:
    candidate_readout_source: Path
    source_evaluation_root: Path
    source_artifact_root: Path
    artifact_run_label: str
    parent_readout_source: Path | None
    parent_source_evaluation_root: Path | None
    source_files: dict[str, Path]
    selected: tuple[SchemaCandidate, ...]
    excluded: tuple[SchemaCandidate, ...]


def load_schema1_candidates(
    candidate_readout_source: Path | str,
    *,
    instance_id: str,
    candidate_cap: int,
) -> CandidateSelection:
    source_path = validate_repo_resident_path(candidate_readout_source)
    if source_path.name != "readout_source.json":
        raise ValueError("candidate source must be a repo-side readout_source.json")
    if not source_path.exists():
        raise FileNotFoundError(f"missing candidate readout source: {source_path}")
    source = json.loads(source_path.read_text(encoding="utf-8"))
    files = {
        key: validate_repo_resident_path(value)
        for key, value in dict(source.get("source_files", {})).items()
    }
    required = (
        "candidate_summary",
        "training_health_summary",
        "tower_shape_summary",
        "concrete_step_summary",
        "learner_update_summary",
    )
    for key in required:
        if key not in files:
            raise FileNotFoundError(f"candidate source missing required file key: {key}")
        if not files[key].exists():
            raise FileNotFoundError(f"candidate source file missing for {key}: {files[key]}")

    rows = _candidate_rows(
        source=source,
        candidate_rows=_read_csv(files["candidate_summary"]),
        health_rows=_read_csv(files["training_health_summary"]),
        concrete_rows=_read_csv(files["concrete_step_summary"]),
        learner_rows=_read_csv(files["learner_update_summary"]),
    )
    matching = tuple(row for row in rows if row.instance_id == instance_id)
    eligible = tuple(row for row in matching if row.candidate_eligible)
    selected = eligible[:candidate_cap]
    selected_ids = {row.candidate_id for row in selected}
    excluded = tuple(row for row in rows if row.candidate_id not in selected_ids)
    return CandidateSelection(
        candidate_readout_source=source_path,
        source_evaluation_root=validate_repo_resident_path(source["source_evaluation_root"]),
        source_artifact_root=validate_repo_resident_path(source["source_artifact_root"]),
        artifact_run_label=str(source.get("artifact_run_label", "")),
        parent_readout_source=_optional_repo_path(source.get("parent_readout_source")),
        parent_source_evaluation_root=_optional_repo_path(
            source.get("parent_source_evaluation_root")
        ),
        source_files=files,
        selected=selected,
        excluded=excluded,
    )


def require_serious_medium_candidate_gate(selection: CandidateSelection) -> None:
    medium = "counterpoint_symbolic_n3_medium_v001"
    eligible_medium = tuple(
        row for row in selection.selected if row.instance_id == medium and row.candidate_eligible
    )
    if len(eligible_medium) < 4:
        raise ValueError(
            "serious medium run requires four eligible medium Schema 1 candidates; "
            f"candidate source provided {len(eligible_medium)} selected medium candidates "
            f"from {selection.candidate_readout_source}"
        )


def _candidate_rows(
    *,
    source: dict[str, Any],
    candidate_rows: list[dict[str, str]],
    health_rows: list[dict[str, str]],
    concrete_rows: list[dict[str, str]],
    learner_rows: list[dict[str, str]],
) -> tuple[SchemaCandidate, ...]:
    health_by_candidate = {row["candidate_id"]: row for row in health_rows}
    concrete_by_candidate = {row["candidate_id"]: row for row in concrete_rows}
    learner_by_candidate = {row["candidate_id"]: row for row in learner_rows}
    result = []
    for row in sorted(
        candidate_rows,
        key=lambda item: (
            item["instance_id"],
            float(item.get("requested_rate") or 0.0),
            int(float(item.get("schema_seed") or 0)),
            item["candidate_id"],
        ),
    ):
        health = health_by_candidate.get(row["candidate_id"], {})
        concrete = concrete_by_candidate.get(row["candidate_id"], {})
        learner = learner_by_candidate.get(row["candidate_id"], {})
        reason = _exclusion_reason(row=row, health=health, concrete=concrete, learner=learner)
        result.append(
            SchemaCandidate(
                candidate_id=row["candidate_id"],
                instance_id=row["instance_id"],
                arm_id=row["arm_id"],
                numerator=int(float(row.get("numerator") or 0)),
                denominator=int(float(row.get("denominator") or 1)),
                requested_rate=float(row.get("requested_rate") or 0.0),
                selector_rule_id=row.get("selector_rule_id", ""),
                schema_seed=int(float(row.get("schema_seed") or 0)),
                tier_state_cell_count_sequence=row.get("tier_state_cell_count_sequence", "[]"),
                tier_active_action_cell_count_sequence=row.get(
                    "tier_active_action_cell_count_sequence", "[]"
                ),
                parent_training_health_class=health.get("training_health_class", ""),
                parent_concrete_step_count=int(float(concrete.get("concrete_step_count") or 0)),
                parent_learner_update_count=int(float(learner.get("successful_update_count") or 0)),
                parent_status=health.get("status", ""),
                parent_run_id=health.get("run_id", row.get("parent_run_id", "")),
                parent_evaluation_id=str(source.get("evaluation_id", "")),
                parent_artifact_run_label=str(source.get("artifact_run_label", "")),
                selected_edge_count=int(float(row.get("selected_edge_count") or 0)),
                selected_edge_share=float(row.get("selected_edge_share") or 0.0),
                selected_source_share=_optional_float(row.get("selected_source_share")),
                zero_selected_source_count=int(float(row.get("zero_selected_source_count") or 0)),
                candidate_eligible=reason is None,
                candidate_exclusion_reason=reason,
            )
        )
    return tuple(result)


def _exclusion_reason(
    *,
    row: dict[str, str],
    health: dict[str, str],
    concrete: dict[str, str],
    learner: dict[str, str],
) -> str | None:
    if row.get("arm_id") == NO_CONTRACTION_ARM_ID:
        return "no_contraction_control_excluded"
    if row.get("candidate_eligible") not in {"True", "true", "1"}:
        return row.get("candidate_exclusion_reason") or "parent_candidate_not_eligible"
    tier_seq = json.loads(row.get("tier_state_cell_count_sequence") or "[]")
    active_seq = json.loads(row.get("tier_active_action_cell_count_sequence") or "[]")
    if len(tier_seq) < 2:
        return "missing_non_base_tier"
    if int(tier_seq[1]) <= 1:
        return "tier1_collapsed"
    if len(active_seq) < 2 or int(active_seq[1]) <= 0:
        return "tier1_non_executable"
    if not health:
        return "missing_parent_training_health"
    if health.get("status") != "success":
        return "parent_training_not_success"
    if health.get("training_health_class") not in {"trainable_clean", "trainable_with_warnings"}:
        return "parent_training_health_not_eligible"
    if int(float(concrete.get("concrete_step_count") or 0)) <= 0:
        return "missing_parent_concrete_step_evidence"
    if int(float(learner.get("successful_update_count") or 0)) <= 0:
        return "missing_parent_learner_update_evidence"
    return None


def _read_csv(path: Path) -> list[dict[str, str]]:
    return list(csv.DictReader(path.open(encoding="utf-8")))


def _optional_float(value: object) -> float | None:
    if value in (None, ""):
        return None
    return float(value)


def _optional_repo_path(value: object) -> Path | None:
    if value in (None, ""):
        return None
    return validate_repo_resident_path(str(value))
