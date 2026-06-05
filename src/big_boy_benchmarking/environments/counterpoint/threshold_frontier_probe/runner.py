"""Runner for the counterpoint threshold-frontier probe."""

from __future__ import annotations

import csv
from pathlib import Path
from typing import Any

from big_boy_benchmarking.artifacts.writers import write_csv, write_json
from big_boy_benchmarking.environments.counterpoint.liftability import (
    STATE_COLLAPSER_V072_POINTWISE_LIFTABILITY_SEMANTICS_ID,
)
from big_boy_benchmarking.environments.counterpoint.second_serious_comparison.aggregation import (
    aggregate_second_serious_comparison_results,
)
from big_boy_benchmarking.environments.counterpoint.second_serious_comparison.config import (
    DEFAULT_LINEARIZATION_MODE_ID,
    SCHEMA1_TOWER_SOURCE_FULL_ITERATED,
)
from big_boy_benchmarking.environments.counterpoint.second_serious_comparison.config import (
    SMOKE_MODE_ID as SECOND_SERIOUS_SMOKE_MODE_ID,
)
from big_boy_benchmarking.environments.counterpoint.second_serious_comparison.paths import (
    build_second_serious_comparison_paths,
)
from big_boy_benchmarking.environments.counterpoint.second_serious_comparison.runner import (
    comparison_spec_for_instance,
    run_second_serious_comparison,
)

from .candidate_source import load_frontier_candidates
from .config import (
    DEFAULT_EPISODES_PER_REPLICATE,
    EVALUATION_ID,
    RUN_MODE_ID,
    ThresholdFrontierProbeBudget,
)
from .manifests import (
    budget_lock_payload,
    candidate_manifest_payload,
    evaluation_arm_manifest_payload,
    evaluation_manifest_payload,
    parent_source_manifest_payload,
    run_family_summary_payload,
    threshold_frontier_policy_payload,
    threshold_run_manifest_payload,
)
from .paths import (
    build_threshold_frontier_probe_paths,
    default_candidate_readout_source,
    threshold_run_root,
    validate_repo_resident_artifact_root,
)
from .thresholds import threshold_label


def run_threshold_frontier_probe(
    *,
    artifact_root: Path | str,
    candidate_readout_source: Path | str | None = None,
    instance_id: str = "wide_span18",
    candidate_cap: int = 1,
    target_candidate_ids: tuple[str, ...] = (),
    threshold_values: tuple[float, ...] = (12.0, 13.0, 13.25, 13.5, 13.75, 14.0),
    training_replicates_per_arm: int = 1,
    episodes_per_replicate: int = DEFAULT_EPISODES_PER_REPLICATE,
    base_seed: int = 0,
    locked_by: str = "cli",
    horizon_override: int | None = None,
    controller_event_ceiling: int | None = None,
    linearization_mode_id: str = DEFAULT_LINEARIZATION_MODE_ID,
) -> dict[str, Any]:
    _require_state_collapser_072()
    artifact_root = validate_repo_resident_artifact_root(artifact_root)
    spec = comparison_spec_for_instance(instance_id)
    candidate_source = candidate_readout_source or default_candidate_readout_source()
    budget = ThresholdFrontierProbeBudget(
        environment_instance_id=spec.environment_instance_id,
        candidate_readout_source=candidate_source,
        candidate_cap=candidate_cap,
        target_candidate_ids=target_candidate_ids,
        threshold_values=threshold_values,
        episodes_per_replicate=episodes_per_replicate,
        training_replicates_per_arm=training_replicates_per_arm,
        base_seed=base_seed,
        locked_by=locked_by,
        run_mode=RUN_MODE_ID,
        controller_event_ceiling_override=controller_event_ceiling,
        linearization_mode_id=linearization_mode_id,
    )
    paths = build_threshold_frontier_probe_paths(artifact_root)
    paths.root.mkdir(parents=True, exist_ok=True)
    paths.results_dir.mkdir(parents=True, exist_ok=True)
    selection = load_frontier_candidates(
        budget.candidate_readout_source,
        instance_id=spec.environment_instance_id,
        candidate_cap=budget.candidate_cap,
        target_candidate_ids=budget.target_candidate_ids,
    )
    if not selection.selected:
        raise ValueError(
            "candidate source yielded no eligible Schema 1 candidates for "
            f"{spec.environment_instance_id}; source={selection.candidate_readout_source}"
        )
    _write_static_manifests(paths=paths, budget=budget, selection=selection)

    threshold_runs: list[dict[str, Any]] = []
    top_level_run_rows: list[dict[str, Any]] = []
    horizon = horizon_override or spec.horizon_steps
    for threshold_value in budget.threshold_values:
        label = threshold_label(threshold_value)
        subroot = threshold_run_root(artifact_root, threshold_value)
        sub_result = run_second_serious_comparison(
            artifact_root=subroot,
            candidate_readout_source=budget.candidate_readout_source,
            instance_id=instance_id,
            candidate_cap=budget.candidate_cap,
            target_candidate_ids=budget.target_candidate_ids,
            schema1_tower_source=SCHEMA1_TOWER_SOURCE_FULL_ITERATED,
            training_replicates_per_arm=budget.training_replicates_per_arm,
            episodes_per_replicate=budget.episodes_per_replicate,
            threshold_value=threshold_value,
            window_length=budget.window_length,
            required_count=budget.required_count,
            run_mode=SECOND_SERIOUS_SMOKE_MODE_ID,
            base_seed=budget.base_seed,
            locked_by=budget.locked_by,
            horizon_override=horizon,
            controller_event_ceiling=budget.controller_event_ceiling_override,
            linearization_mode_id=budget.linearization_mode_id,
        )
        sub_summary = aggregate_second_serious_comparison_results(
            subroot,
            docs_root=subroot / "docs" / "second_serious_comparison",
        )
        sub_paths = build_second_serious_comparison_paths(subroot)
        run_rows = _read_csv(sub_paths.evaluation_run_index_csv)
        top_level_run_rows.extend(
            _frontier_run_index_row(
                row,
                threshold_value=threshold_value,
                threshold_label=label,
                threshold_artifact_root=subroot,
            )
            for row in run_rows
        )
        threshold_runs.append(
            {
                "threshold_value": threshold_value,
                "threshold_label": label,
                "status": sub_result["status"],
                "summary_status": sub_summary["status"],
                "artifact_root": str(subroot),
                "source_evaluation_root": str(sub_paths.root),
                "run_index": str(sub_paths.evaluation_run_index_csv),
                "aggregate_table": str(sub_paths.evaluation_aggregate_table_csv),
                "aggregate_summary": str(sub_paths.evaluation_aggregate_summary),
                "run_count": sub_result["run_count"],
                "pair_count": sub_summary.get("pair_count", 0),
            }
        )

    write_json(
        paths.threshold_run_manifest,
        threshold_run_manifest_payload(threshold_runs=threshold_runs),
        create_parents=True,
    )
    write_json(
        paths.run_family_summary,
        run_family_summary_payload(budget=budget, threshold_runs=threshold_runs),
        create_parents=True,
    )
    write_csv(
        paths.evaluation_run_index_csv,
        top_level_run_rows,
        _frontier_run_index_fieldnames(),
        create_parents=True,
    )
    status = (
        "complete"
        if threshold_runs
        and all(
            row["status"] == "complete" and row["summary_status"] == "complete"
            for row in threshold_runs
        )
        else "incomplete"
    )
    return {
        "status": status,
        "threshold_count": len(threshold_runs),
        "run_count": len(top_level_run_rows),
        "pair_count": sum(int(row["pair_count"]) for row in threshold_runs),
        "evaluation_run_index": str(paths.evaluation_run_index_csv),
        "candidate_manifest": str(paths.candidate_manifest),
        "threshold_run_manifest": str(paths.threshold_run_manifest),
        "evaluation_budget_lock": str(paths.evaluation_budget_lock),
    }


def _write_static_manifests(*, paths, budget: ThresholdFrontierProbeBudget, selection) -> None:
    write_json(
        paths.evaluation_manifest, evaluation_manifest_payload(budget=budget), create_parents=True
    )
    write_json(
        paths.evaluation_arm_manifest, evaluation_arm_manifest_payload(), create_parents=True
    )
    write_json(
        paths.evaluation_budget_lock, budget_lock_payload(budget=budget), create_parents=True
    )
    write_json(
        paths.threshold_frontier_policy_manifest,
        threshold_frontier_policy_payload(budget=budget),
        create_parents=True,
    )
    write_json(
        paths.candidate_manifest,
        candidate_manifest_payload(selection=selection, budget=budget),
        create_parents=True,
    )
    write_json(
        paths.parent_source_manifest,
        parent_source_manifest_payload(selection=selection),
        create_parents=True,
    )


def _frontier_run_index_row(
    row: dict[str, str],
    *,
    threshold_value: float,
    threshold_label: str,
    threshold_artifact_root: Path,
) -> dict[str, Any]:
    result = dict(row)
    result["evaluation_id"] = EVALUATION_ID
    result["source_evaluation_id"] = row.get("evaluation_id", "")
    result["threshold_value"] = threshold_value
    result["threshold_label"] = threshold_label
    result["threshold_artifact_root"] = str(threshold_artifact_root)
    return result


def _frontier_run_index_fieldnames() -> tuple[str, ...]:
    return (
        "evaluation_id",
        "source_evaluation_id",
        "threshold_value",
        "threshold_label",
        "run_id",
        "run_mode",
        "candidate_group_id",
        "schema_class_id",
        "candidate_id",
        "instance_id",
        "arm_id",
        "schema_seed",
        "seed_bundle_id",
        "training_replicate_index",
        "status",
        "artifact_root",
        "threshold_artifact_root",
        "started_at",
        "ended_at",
        "failure_reason",
    )


def _read_csv(path: Path) -> list[dict[str, str]]:
    with path.open(newline="", encoding="utf-8") as handle:
        return list(csv.DictReader(handle))


def _require_state_collapser_072() -> None:
    import state_collapser

    version = str(getattr(state_collapser, "__version__", "0"))
    if _version_tuple(version) < (0, 7, 2):
        raise ValueError(
            "threshold frontier probe requires state_collapser>=0.7.2 "
            f"with {STATE_COLLAPSER_V072_POINTWISE_LIFTABILITY_SEMANTICS_ID}; "
            f"found {version}"
        )


def _version_tuple(version: str) -> tuple[int, int, int]:
    parts = []
    for item in version.split(".")[:3]:
        digits = "".join(char for char in item if char.isdigit())
        parts.append(int(digits or "0"))
    while len(parts) < 3:
        parts.append(0)
    return tuple(parts)
