"""Candidate selection from parent noisy-rate diagnostic readout sources."""

from __future__ import annotations

import csv
import json
from dataclasses import dataclass
from pathlib import Path
from typing import Any

from big_boy_benchmarking.environments.counterpoint.noisy_rate_full_training.config import (
    EVALUATION_ID,
    NO_CONTRACTION_ARM_ID,
)
from big_boy_benchmarking.environments.counterpoint.noisy_rate_full_training.events import (
    FullTrainingCandidateSummaryRow,
)
from big_boy_benchmarking.environments.counterpoint.noisy_rate_full_training.paths import (
    validate_repo_resident_path,
)


@dataclass(frozen=True)
class CandidateSelectionResult:
    parent_readout_source: Path
    parent_source_evaluation_root: Path
    parent_evaluation_id: str
    parent_artifact_run_label: str
    parent_source_files: dict[str, Path]
    selected: tuple[FullTrainingCandidateSummaryRow, ...]
    excluded: tuple[FullTrainingCandidateSummaryRow, ...]


def load_candidate_selection(
    parent_readout_source: Path | str,
    *,
    include_runtime_anchor: bool = False,
    candidate_cap: int | None = None,
) -> CandidateSelectionResult:
    source_path = validate_repo_resident_path(parent_readout_source)
    if source_path.name != "readout_source.json":
        raise ValueError("candidate source must be a repo-side readout_source.json")
    if not source_path.exists():
        raise FileNotFoundError(f"missing parent readout source: {source_path}")
    source = json.loads(source_path.read_text(encoding="utf-8"))
    parent_root = validate_repo_resident_path(source["source_evaluation_root"])
    files = {
        key: validate_repo_resident_path(value)
        for key, value in dict(source["source_files"]).items()
    }
    required_keys = (
        "aggregate_table",
        "tower_shape_summary",
        "noisy_rate_selection_summary",
        "noisy_rate_source_coverage_summary",
        "noisy_rate_selection_consistency_summary",
        "endpoint_coalescence_summary",
    )
    for key in required_keys:
        if key not in files:
            raise FileNotFoundError(f"parent source missing required file key: {key}")
        if not files[key].exists():
            raise FileNotFoundError(f"parent source file missing for {key}: {files[key]}")

    rows = _candidate_rows(
        parent_evaluation_id=str(source["evaluation_id"]),
        parent_artifact_run_label=str(source["artifact_run_label"]),
        aggregate_rows=_read_csv(files["aggregate_table"]),
        tower_rows=_read_csv(files["tower_shape_summary"]),
        selection_rows=_read_csv(files["noisy_rate_selection_summary"]),
        coverage_rows=_read_csv(files["noisy_rate_source_coverage_summary"]),
        consistency_rows=_read_csv(files["noisy_rate_selection_consistency_summary"]),
        endpoint_rows=_read_csv(files["endpoint_coalescence_summary"]),
        include_runtime_anchor=include_runtime_anchor,
    )
    eligible = tuple(row for row in rows if row.candidate_eligible)
    if candidate_cap is not None:
        eligible = eligible[:candidate_cap]
    if not eligible:
        raise ValueError("candidate selection yielded no eligible non-collapsed candidates")
    eligible_ids = {row.candidate_id for row in eligible}
    excluded = tuple(row for row in rows if row.candidate_id not in eligible_ids)
    return CandidateSelectionResult(
        parent_readout_source=source_path,
        parent_source_evaluation_root=parent_root,
        parent_evaluation_id=str(source["evaluation_id"]),
        parent_artifact_run_label=str(source["artifact_run_label"]),
        parent_source_files=files,
        selected=eligible,
        excluded=excluded,
    )


def candidate_to_manifest_dict(row: FullTrainingCandidateSummaryRow) -> dict[str, Any]:
    return row.to_flat_dict()


def _candidate_rows(
    *,
    parent_evaluation_id: str,
    parent_artifact_run_label: str,
    aggregate_rows: list[dict[str, str]],
    tower_rows: list[dict[str, str]],
    selection_rows: list[dict[str, str]],
    coverage_rows: list[dict[str, str]],
    consistency_rows: list[dict[str, str]],
    endpoint_rows: list[dict[str, str]],
    include_runtime_anchor: bool,
) -> tuple[FullTrainingCandidateSummaryRow, ...]:
    tower_by_key: dict[tuple[str, str, int], list[dict[str, str]]] = {}
    for row in tower_rows:
        key = (row["instance_id"], row["arm_id"], int(row["schema_seed"]))
        tower_by_key.setdefault(key, []).append(row)
    selection_by_key = _index_by_key(selection_rows)
    coverage_by_key = _index_by_key(coverage_rows)
    consistency_by_key = _index_by_key(consistency_rows)
    endpoint_by_key = {
        (row["instance_id"], row["arm_id"], int(row["schema_seed"])): row
        for row in endpoint_rows
    }
    result = []
    for aggregate in sorted(
        aggregate_rows,
        key=lambda row: (
            row["instance_id"],
            float(row.get("requested_rate") or 0.0),
            int(row.get("schema_seed") or 0),
            row["arm_id"],
        ),
    ):
        key = (
            aggregate["instance_id"],
            aggregate["arm_id"],
            int(aggregate["schema_seed"]),
        )
        selection = selection_by_key.get(key, {})
        coverage = coverage_by_key.get(key, {})
        consistency = consistency_by_key.get(key, {})
        endpoint = endpoint_by_key.get(key, {})
        tiers = sorted(tower_by_key.get(key, []), key=lambda row: int(row["tier_index"]))
        candidate_id = (
            f"{aggregate['instance_id']}-{aggregate['arm_id']}-"
            f"schema{aggregate['schema_seed']}"
        )
        state_seq = [int(row["state_cell_count"]) for row in tiers]
        active_seq = [int(row["active_action_cell_count"]) for row in tiers]
        deepest = tiers[-1] if tiers else {}
        reason = _exclusion_reason(
            aggregate=aggregate,
            consistency=consistency,
            tiers=tiers,
            include_runtime_anchor=include_runtime_anchor,
        )
        result.append(
            FullTrainingCandidateSummaryRow(
                evaluation_id=EVALUATION_ID,
                candidate_id=candidate_id,
                parent_evaluation_id=parent_evaluation_id,
                parent_artifact_run_label=parent_artifact_run_label,
                parent_run_id=aggregate.get("run_id", ""),
                instance_id=aggregate["instance_id"],
                arm_id=aggregate["arm_id"],
                numerator=int(float(aggregate.get("numerator") or 0)),
                denominator=int(float(aggregate.get("denominator") or 1)),
                requested_rate=float(aggregate.get("requested_rate") or 0.0),
                selector_rule_id=aggregate.get("selector_rule_id", ""),
                schema_seed=int(aggregate["schema_seed"]),
                selected_edge_count=int(float(selection.get("selected_edge_count") or 0)),
                selected_edge_share=float(
                    selection.get("realized_selected_edge_share")
                    or aggregate.get("selected_edge_share")
                    or 0.0
                ),
                selected_source_share=_optional_float(
                    coverage.get("selected_source_share")
                    or aggregate.get("selected_source_share")
                ),
                zero_selected_source_count=int(
                    float(coverage.get("zero_selected_source_count") or 0)
                ),
                tier_state_cell_count_sequence=json.dumps(state_seq),
                tier_active_action_cell_count_sequence=json.dumps(active_seq),
                deepest_tier_index=int(deepest.get("tier_index") or 0),
                deepest_tier_state_cell_count=int(deepest.get("state_cell_count") or 0),
                deepest_tier_active_action_cell_count=int(
                    deepest.get("active_action_cell_count") or 0
                ),
                largest_state_cell_share=float(
                    deepest.get("largest_state_cell_share")
                    or aggregate.get("first_projection_largest_state_cell_share")
                    or 0.0
                ),
                endpoint_useful_coalescence_count=int(
                    float(endpoint.get("useful_coalescence_count") or 0)
                ),
                candidate_eligible=reason is None,
                candidate_exclusion_reason=reason,
                candidate_liftability_evidence_source=(
                    "static_tower_shape_active_action_cell_count"
                ),
                candidate_liftability_compatibility_note=(
                    "parent candidate source lacks current-base-state pointwise "
                    "liftability fields; downstream training reruns use "
                    "state_collapser_v072_pointwise masks and lift resolution"
                ),
            )
        )
    return tuple(result)


def _exclusion_reason(
    *,
    aggregate: dict[str, str],
    consistency: dict[str, str],
    tiers: list[dict[str, str]],
    include_runtime_anchor: bool,
) -> str | None:
    if aggregate.get("arm_id") == NO_CONTRACTION_ARM_ID and not include_runtime_anchor:
        return "no_contraction_control_excluded"
    if aggregate.get("status") != "success":
        return "parent_run_not_success"
    if consistency and consistency.get("selection_sets_equal") != "True":
        return "selection_consistency_mismatch"
    if len(tiers) < 2 and aggregate.get("arm_id") != NO_CONTRACTION_ARM_ID:
        return "missing_non_base_tier"
    deepest = tiers[-1] if tiers else {}
    if int(deepest.get("state_cell_count") or 0) <= 1:
        return "deepest_tier_collapsed"
    if int(deepest.get("active_action_cell_count") or 0) <= 0:
        return "deepest_tier_not_executable"
    classification = aggregate.get("structural_limit_classification", "")
    if "full_collapse" in classification or "invalid" in classification:
        return "parent_structural_limit"
    return None


def _index_by_key(rows: list[dict[str, str]]) -> dict[tuple[str, str, int], dict[str, str]]:
    return {
        (row["instance_id"], row["arm_id"], int(row["schema_seed"])): row for row in rows
    }


def _read_csv(path: Path) -> list[dict[str, str]]:
    return list(csv.DictReader(path.open(encoding="utf-8")))


def _optional_float(value: object) -> float | None:
    if value in (None, ""):
        return None
    return float(value)
