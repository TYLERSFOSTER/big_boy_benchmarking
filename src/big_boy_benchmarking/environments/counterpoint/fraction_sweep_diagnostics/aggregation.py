"""Aggregation helpers for counterpoint contraction fraction sweep diagnostics."""

from __future__ import annotations

import csv
import json
import statistics
from collections import Counter, defaultdict
from pathlib import Path
from typing import Any

from big_boy_benchmarking.artifacts.writers import write_csv, write_json
from big_boy_benchmarking.environments.counterpoint.fraction_sweep_diagnostics.config import (
    EVALUATION_ID,
    EVALUATION_RUN_FAMILY_ID,
    NEAR_FULL_COLLAPSE_THRESHOLD,
    NO_CONTRACTION_ARM_ID,
)
from big_boy_benchmarking.environments.counterpoint.fraction_sweep_diagnostics.events import (
    ABCSelectionSummaryRow,
    ABCTierSignalSummaryRow,
    CollapseThresholdSummaryRow,
    ConcreteStepSummaryRow,
    ControlActionSummaryRow,
    EndpointCoalescenceSummaryRow,
    FractionSweepAggregateTableRow,
    FractionSweepTowerShapeSummaryRow,
    LegacyOneThirdEquivalenceSummaryRow,
    LiftFailureByTierRow,
    SchemaFractionSummaryRow,
    TierExecutabilitySummaryRow,
    TierOccupancySummaryRow,
)
from big_boy_benchmarking.environments.counterpoint.fraction_sweep_diagnostics.manifests import (
    aggregate_summary_payload,
    readout_source_payload,
)
from big_boy_benchmarking.environments.counterpoint.fraction_sweep_diagnostics.paths import (
    build_fraction_sweep_diagnostics_paths,
    repo_readout_surface,
    validate_repo_resident_artifact_root,
)


def aggregate_fraction_sweep_diagnostics_results(
    artifact_root: Path | str,
    *,
    docs_root: Path | str | None = None,
) -> dict[str, Any]:
    artifact_root = validate_repo_resident_artifact_root(artifact_root)
    paths = build_fraction_sweep_diagnostics_paths(artifact_root)
    paths.results_dir.mkdir(parents=True, exist_ok=True)
    if not paths.evaluation_run_index_csv.exists():
        raise FileNotFoundError(f"missing evaluation run index: {paths.evaluation_run_index_csv}")
    run_rows = list(csv.DictReader(paths.evaluation_run_index_csv.open()))

    schema_fraction_rows: list[dict[str, Any]] = []
    tower_shape_rows: list[dict[str, Any]] = []
    endpoint_rows: list[dict[str, Any]] = []
    tier_executability_rows: list[dict[str, Any]] = []
    control_action_rows: list[dict[str, Any]] = []
    abc_selection_rows: list[dict[str, Any]] = []
    abc_tier_signal_rows: list[dict[str, Any]] = []
    tier_occupancy_rows: list[dict[str, Any]] = []
    lift_failure_rows: list[dict[str, Any]] = []
    concrete_step_rows: list[dict[str, Any]] = []
    legacy_rows: list[dict[str, Any]] = []
    aggregate_rows: list[dict[str, Any]] = []

    schema_seen: set[tuple[str, str, str]] = set()
    legacy_seen: set[tuple[str, str]] = set()
    classification_counts: Counter[str] = Counter()
    complete_run_count = 0
    for run_row in run_rows:
        if run_row["status"] != "success":
            aggregate = _failed_aggregate_row(run_row)
            aggregate_rows.append(aggregate.to_flat_dict())
            classification_counts[aggregate.structural_limit_classification] += 1
            continue
        complete_run_count += 1
        run_root = _run_root(artifact_root, run_row["run_id"])
        quotient_summary = _read_json(run_root / "quotient_summary.json")
        schema_key = (run_row["instance_id"], run_row["arm_id"], run_row["schema_seed"])
        if schema_key not in schema_seen:
            schema_fraction_rows.extend(quotient_summary.get("schema_fraction_summary", []))
            schema_seen.add(schema_key)
        legacy_key = (run_row["instance_id"], run_row["schema_seed"])
        if legacy_key not in legacy_seen:
            legacy_rows.extend(quotient_summary.get("legacy_one_third_equivalence_summary", []))
            if quotient_summary.get("legacy_one_third_equivalence_summary"):
                legacy_seen.add(legacy_key)
        tower_shape_rows.extend(quotient_summary.get("tower_shape_summary", []))
        endpoint_rows.extend(quotient_summary.get("endpoint_coalescence_summary", []))

        control_rows = _read_csv(run_root / "control_events.csv")
        step_rows = _read_csv(run_root / "step_events.csv")
        lift_rows = _read_csv(run_root / "lift_fiber_events.csv")
        abc_selection_event_rows = _read_csv(run_root / "abc_selection_events.csv")
        abc_tier_signal_event_rows = _read_csv(run_root / "abc_tier_signal_events.csv")
        episode_rows = _read_csv(run_root / "episodes.csv")

        tier_executability_rows.extend(
            row.to_flat_dict()
            for row in _tier_executability_summary(run_row, abc_tier_signal_event_rows)
        )
        control_action_rows.extend(
            row.to_flat_dict() for row in _control_action_summary(run_row, control_rows)
        )
        abc_selection_rows.extend(
            row.to_flat_dict()
            for row in _abc_selection_summary(run_row, abc_selection_event_rows)
        )
        abc_tier_signal_rows.extend(
            row.to_flat_dict()
            for row in _abc_tier_signal_summary(run_row, abc_tier_signal_event_rows)
        )
        tier_occupancy_rows.extend(
            row.to_flat_dict()
            for row in _tier_occupancy_summary(run_row, control_rows, step_rows)
        )
        lift_failure_rows.extend(
            row.to_flat_dict() for row in _lift_failure_summary(run_row, lift_rows)
        )
        concrete_step_rows.append(
            _concrete_step_summary(run_row, episode_rows, step_rows).to_flat_dict()
        )
        aggregate = _aggregate_row(
            run_row=run_row,
            tower_shape_rows=quotient_summary.get("tower_shape_summary", []),
            control_rows=control_rows,
            step_rows=step_rows,
            abc_selection_rows=abc_selection_event_rows,
        )
        aggregate_rows.append(aggregate.to_flat_dict())
        classification_counts[aggregate.structural_limit_classification] += 1

    collapse_rows = [
        row.to_flat_dict()
        for row in _collapse_threshold_summary(tower_shape_rows, legacy_rows)
    ]
    sweep_verdict_counts = Counter(row["sweep_verdict"] for row in collapse_rows)

    result_paths = (
        paths.results_dir / "schema_fraction_summary.csv",
        paths.results_dir / "tower_shape_summary.csv",
        paths.results_dir / "endpoint_coalescence_summary.csv",
        paths.results_dir / "tier_executability_summary.csv",
        paths.results_dir / "tier_occupancy_summary.csv",
        paths.results_dir / "control_action_summary.csv",
        paths.results_dir / "abc_selection_summary.csv",
        paths.results_dir / "abc_tier_signal_summary.csv",
        paths.results_dir / "lift_failure_by_tier.csv",
        paths.results_dir / "concrete_step_summary.csv",
        paths.results_dir / "collapse_threshold_summary.csv",
        paths.results_dir / "legacy_one_third_equivalence_summary.csv",
    )
    write_csv(result_paths[0], schema_fraction_rows, SchemaFractionSummaryRow.fieldnames())
    write_csv(result_paths[1], tower_shape_rows, FractionSweepTowerShapeSummaryRow.fieldnames())
    write_csv(result_paths[2], endpoint_rows, EndpointCoalescenceSummaryRow.fieldnames())
    write_csv(result_paths[3], tier_executability_rows, TierExecutabilitySummaryRow.fieldnames())
    write_csv(result_paths[4], tier_occupancy_rows, TierOccupancySummaryRow.fieldnames())
    write_csv(result_paths[5], control_action_rows, ControlActionSummaryRow.fieldnames())
    write_csv(result_paths[6], abc_selection_rows, ABCSelectionSummaryRow.fieldnames())
    write_csv(result_paths[7], abc_tier_signal_rows, ABCTierSignalSummaryRow.fieldnames())
    write_csv(result_paths[8], lift_failure_rows, LiftFailureByTierRow.fieldnames())
    write_csv(result_paths[9], concrete_step_rows, ConcreteStepSummaryRow.fieldnames())
    write_csv(result_paths[10], collapse_rows, CollapseThresholdSummaryRow.fieldnames())
    write_csv(result_paths[11], legacy_rows, LegacyOneThirdEquivalenceSummaryRow.fieldnames())
    write_csv(
        paths.evaluation_aggregate_table_csv,
        aggregate_rows,
        FractionSweepAggregateTableRow.fieldnames(),
    )
    status = "complete" if complete_run_count == len(run_rows) and run_rows else "incomplete"
    summary = aggregate_summary_payload(
        status=status,
        run_count=len(run_rows),
        complete_run_count=complete_run_count,
        table_path=paths.evaluation_aggregate_table_csv,
        result_paths=result_paths,
        classification_counts=dict(classification_counts),
        sweep_verdict_counts=dict(sweep_verdict_counts),
    )
    write_json(paths.evaluation_aggregate_summary, summary)
    _write_readout_source(
        artifact_root=artifact_root,
        docs_root=Path(docs_root) if docs_root is not None else repo_readout_surface(),
        paths=paths,
        result_paths=result_paths,
    )
    return summary


def _write_readout_source(
    *,
    artifact_root: Path,
    docs_root: Path,
    paths,
    result_paths: tuple[Path, ...],
) -> None:
    source_files = {
        "aggregate_table": paths.evaluation_aggregate_table_csv,
        "run_index": paths.evaluation_run_index_csv,
        "aggregate_summary": paths.evaluation_aggregate_summary,
        "schema_fraction_summary": result_paths[0],
        "tower_shape_summary": result_paths[1],
        "endpoint_coalescence_summary": result_paths[2],
        "tier_executability_summary": result_paths[3],
        "tier_occupancy_summary": result_paths[4],
        "control_action_summary": result_paths[5],
        "abc_selection_summary": result_paths[6],
        "abc_tier_signal_summary": result_paths[7],
        "lift_failure_by_tier": result_paths[8],
        "concrete_step_summary": result_paths[9],
        "collapse_threshold_summary": result_paths[10],
        "legacy_one_third_equivalence_summary": result_paths[11],
    }
    budget = _read_json(paths.evaluation_budget_lock)
    payload = readout_source_payload(
        repo_readout_surface=docs_root,
        source_artifact_root=artifact_root,
        source_evaluation_root=paths.root,
        artifact_run_label=artifact_root.name,
        source_files=source_files,
        budget=budget,
    )
    docs_root.mkdir(parents=True, exist_ok=True)
    write_json(docs_root / "readout_source.json", payload, create_parents=True)
    write_json(paths.readout_source, payload, create_parents=True)


def _tier_executability_summary(
    run_row: dict[str, str],
    tier_rows: list[dict[str, str]],
) -> tuple[TierExecutabilitySummaryRow, ...]:
    grouped: dict[int, list[dict[str, str]]] = defaultdict(list)
    for row in tier_rows:
        grouped[int(row["tier_index"])].append(row)
    return tuple(
        TierExecutabilitySummaryRow(
            evaluation_id=EVALUATION_ID,
            run_id=run_row["run_id"],
            instance_id=run_row["instance_id"],
            arm_id=run_row["arm_id"],
            numerator=int(run_row["numerator"]),
            denominator=int(run_row["denominator"]),
            schema_seed=int(run_row["schema_seed"]),
            replicate_index=int(run_row["replicate_index"]),
            tier_index=tier,
            event_count=len(rows),
            executable_event_count=sum(_as_bool(row["executable"]) for row in rows),
            executable_event_share=_share(
                sum(_as_bool(row["executable"]) for row in rows),
                len(rows),
            ),
            selected_event_count=sum(_as_bool(row["selected"]) for row in rows),
        )
        for tier, rows in sorted(grouped.items())
    )


def _control_action_summary(
    run_row: dict[str, str],
    control_rows: list[dict[str, str]],
) -> tuple[ControlActionSummaryRow, ...]:
    counts = Counter(row["control_action"] for row in control_rows)
    total = max(1, len(control_rows))
    return tuple(
        ControlActionSummaryRow(
            evaluation_id=EVALUATION_ID,
            run_id=run_row["run_id"],
            instance_id=run_row["instance_id"],
            arm_id=run_row["arm_id"],
            numerator=int(run_row["numerator"]),
            denominator=int(run_row["denominator"]),
            schema_seed=int(run_row["schema_seed"]),
            replicate_index=int(run_row["replicate_index"]),
            control_action=action,
            event_count=count,
            event_share=count / total,
        )
        for action, count in sorted(counts.items())
    )


def _abc_selection_summary(
    run_row: dict[str, str],
    selection_rows: list[dict[str, str]],
) -> tuple[ABCSelectionSummaryRow, ...]:
    grouped: dict[tuple[str, str, str, str], list[dict[str, str]]] = defaultdict(list)
    for row in selection_rows:
        grouped[
            (
                row["selected_tier"],
                row["predicted_movement_direction"],
                row["control_action"],
                row["blocked_reason"],
            )
        ].append(row)
    result = []
    for (selected_tier, movement, action, blocked), rows in sorted(grouped.items()):
        consistent = sum(_as_bool(row["action_consistent"]) for row in rows)
        result.append(
            ABCSelectionSummaryRow(
                evaluation_id=EVALUATION_ID,
                run_id=run_row["run_id"],
                instance_id=run_row["instance_id"],
                arm_id=run_row["arm_id"],
                numerator=int(run_row["numerator"]),
                denominator=int(run_row["denominator"]),
                schema_seed=int(run_row["schema_seed"]),
                replicate_index=int(run_row["replicate_index"]),
                selected_tier=None if selected_tier == "" else int(selected_tier),
                predicted_movement_direction=movement,
                control_action=action,
                blocked_reason=blocked or None,
                event_count=len(rows),
                action_consistent_count=consistent,
                action_consistent_share=_share(consistent, len(rows)),
            )
        )
    return tuple(result)


def _abc_tier_signal_summary(
    run_row: dict[str, str],
    tier_rows: list[dict[str, str]],
) -> tuple[ABCTierSignalSummaryRow, ...]:
    grouped: dict[int, list[dict[str, str]]] = defaultdict(list)
    for row in tier_rows:
        grouped[int(row["tier_index"])].append(row)
    result = []
    for tier, rows in sorted(grouped.items()):
        pressures = [_as_float(row["productive_learning_pressure"]) for row in rows]
        result.append(
            ABCTierSignalSummaryRow(
                evaluation_id=EVALUATION_ID,
                run_id=run_row["run_id"],
                instance_id=run_row["instance_id"],
                arm_id=run_row["arm_id"],
                numerator=int(run_row["numerator"]),
                denominator=int(run_row["denominator"]),
                schema_seed=int(run_row["schema_seed"]),
                replicate_index=int(run_row["replicate_index"]),
                tier_index=tier,
                event_count=len(rows),
                executable_event_share=_share(
                    sum(_as_bool(row["executable"]) for row in rows), len(rows)
                ),
                unclosed_event_share=_share(
                    sum(_as_bool(row["unclosed"]) for row in rows), len(rows)
                ),
                mean_productive_learning_pressure=statistics.mean(pressures)
                if pressures
                else None,
                selected_event_count=sum(_as_bool(row["selected"]) for row in rows),
                active_event_count=sum(_as_bool(row["active"]) for row in rows),
            )
        )
    return tuple(result)


def _tier_occupancy_summary(
    run_row: dict[str, str],
    control_rows: list[dict[str, str]],
    step_rows: list[dict[str, str]],
) -> tuple[TierOccupancySummaryRow, ...]:
    grouped: dict[tuple[str, str], list[dict[str, str]]] = defaultdict(list)
    for row in control_rows:
        grouped[(row["active_tier_after"], row["control_action"])].append(row)
    control_by_event = {
        (row["episode_index"], row["controller_event_index"]): row
        for row in control_rows
    }
    rewards_by_key: dict[tuple[str, str], list[float]] = defaultdict(list)
    for row in step_rows:
        control = control_by_event.get((row["episode_index"], row["controller_event_index"]))
        action = "" if control is None else control["control_action"]
        rewards_by_key[(row["active_tier_after"], action)].append(_as_float(row["reward"]))
    total_events = max(1, len(control_rows))
    total_steps = max(1, len(step_rows))
    result = []
    for (tier_text, action), rows in sorted(grouped.items()):
        rewards = rewards_by_key.get((tier_text, action), [])
        concrete_step_count = len(rewards)
        result.append(
            TierOccupancySummaryRow(
                evaluation_id=EVALUATION_ID,
                run_id=run_row["run_id"],
                instance_id=run_row["instance_id"],
                arm_id=run_row["arm_id"],
                numerator=int(run_row["numerator"]),
                denominator=int(run_row["denominator"]),
                schema_seed=int(run_row["schema_seed"]),
                replicate_index=int(run_row["replicate_index"]),
                tier_index=None if tier_text == "" else int(tier_text),
                control_action=action,
                event_count=len(rows),
                event_share=len(rows) / total_events,
                concrete_step_count=concrete_step_count,
                concrete_step_share=concrete_step_count / total_steps,
                mean_reward_on_concrete_steps=statistics.mean(rewards) if rewards else None,
            )
        )
    return tuple(result)


def _lift_failure_summary(
    run_row: dict[str, str],
    lift_rows: list[dict[str, str]],
) -> tuple[LiftFailureByTierRow, ...]:
    grouped: dict[tuple[str, str, str], list[dict[str, str]]] = defaultdict(list)
    for row in lift_rows:
        grouped[
            (
                row["active_tier"],
                row["failure_reason"],
                row["fiber_departure_reason"],
            )
        ].append(row)
    result = []
    for (tier_text, failure_reason, fiber_reason), rows in sorted(grouped.items()):
        candidate_counts = [_as_float(row["candidate_count"]) for row in rows]
        successes = sum(_as_bool(row["success"]) for row in rows)
        result.append(
            LiftFailureByTierRow(
                evaluation_id=EVALUATION_ID,
                run_id=run_row["run_id"],
                instance_id=run_row["instance_id"],
                arm_id=run_row["arm_id"],
                numerator=int(run_row["numerator"]),
                denominator=int(run_row["denominator"]),
                schema_seed=int(run_row["schema_seed"]),
                replicate_index=int(run_row["replicate_index"]),
                active_tier=None if tier_text == "" else int(tier_text),
                failure_reason=failure_reason or None,
                fiber_departure_reason=fiber_reason or None,
                lift_attempt_count=len(rows),
                lift_success_count=successes,
                lift_failure_count=len(rows) - successes,
                mean_candidate_count=statistics.mean(candidate_counts)
                if candidate_counts
                else None,
            )
        )
    return tuple(result)


def _concrete_step_summary(
    run_row: dict[str, str],
    episode_rows: list[dict[str, str]],
    step_rows: list[dict[str, str]],
) -> ConcreteStepSummaryRow:
    rewards = [_as_float(row["reward"]) for row in step_rows]
    final_counts = Counter(row["final_state"] for row in episode_rows)
    return ConcreteStepSummaryRow(
        evaluation_id=EVALUATION_ID,
        run_id=run_row["run_id"],
        instance_id=run_row["instance_id"],
        arm_id=run_row["arm_id"],
        numerator=int(run_row["numerator"]),
        denominator=int(run_row["denominator"]),
        schema_seed=int(run_row["schema_seed"]),
        replicate_index=int(run_row["replicate_index"]),
        episode_count=len(episode_rows),
        concrete_step_count=len(step_rows),
        zero_step_episode_count=sum(
            1 for row in episode_rows if int(row["concrete_step_count"]) == 0
        ),
        mean_reward=statistics.mean(rewards) if rewards else None,
        terminated_count=sum(_as_bool(row["terminated"]) for row in episode_rows),
        truncated_count=sum(_as_bool(row["truncated"]) for row in episode_rows),
        final_state_summary=json.dumps(dict(final_counts), sort_keys=True),
    )


def _aggregate_row(
    *,
    run_row: dict[str, str],
    tower_shape_rows: list[dict[str, Any]],
    control_rows: list[dict[str, str]],
    step_rows: list[dict[str, str]],
    abc_selection_rows: list[dict[str, str]],
) -> FractionSweepAggregateTableRow:
    first_projection = next(
        (row for row in tower_shape_rows if int(row.get("tier_index", -1)) == 1),
        None,
    )
    largest_share = (
        None
        if first_projection is None
        else float(first_projection["largest_state_cell_share"])
    )
    full_collapse = largest_share is not None and int(first_projection["state_cell_count"]) == 1
    near_full = (
        largest_share is not None
        and largest_share >= NEAR_FULL_COLLAPSE_THRESHOLD
        and not full_collapse
    )
    selected_non_exec = sum(
        row["selected_tier_executable"] == "False" for row in abc_selection_rows
    )
    no_available = sum(row["control_action"] == "no_available_action" for row in control_rows)
    zero_steps = len(step_rows) == 0
    missing_abc = len(control_rows) > 0 and not abc_selection_rows
    classification = _classification(
        full_collapse=full_collapse,
        near_full=near_full,
        selected_non_exec=selected_non_exec,
        no_available=no_available,
        zero_steps=zero_steps,
        missing_abc=missing_abc,
    )
    return FractionSweepAggregateTableRow(
        evaluation_id=EVALUATION_ID,
        run_id=run_row["run_id"],
        instance_id=run_row["instance_id"],
        arm_id=run_row["arm_id"],
        numerator=int(run_row["numerator"]),
        denominator=int(run_row["denominator"]),
        schema_seed=int(run_row["schema_seed"]),
        replicate_index=int(run_row["replicate_index"]),
        status=run_row["status"],
        first_projection_largest_state_cell_share=largest_share,
        full_first_projection_collapse=full_collapse,
        near_full_first_projection_collapse=near_full,
        selected_tier_non_executability_count=selected_non_exec,
        no_available_action_count=no_available,
        zero_concrete_steps=zero_steps,
        missing_abc_context=missing_abc,
        structural_limit_classification=classification,
    )


def _failed_aggregate_row(run_row: dict[str, str]) -> FractionSweepAggregateTableRow:
    return FractionSweepAggregateTableRow(
        evaluation_id=EVALUATION_ID,
        run_id=run_row.get("run_id", ""),
        instance_id=run_row["instance_id"],
        arm_id=run_row["arm_id"],
        numerator=int(run_row["numerator"]),
        denominator=int(run_row["denominator"]),
        schema_seed=int(run_row["schema_seed"]),
        replicate_index=int(run_row["replicate_index"]),
        status=run_row["status"],
        first_projection_largest_state_cell_share=None,
        full_first_projection_collapse=False,
        near_full_first_projection_collapse=False,
        selected_tier_non_executability_count=0,
        no_available_action_count=0,
        zero_concrete_steps=True,
        missing_abc_context=True,
        structural_limit_classification="run_failed",
    )


def _collapse_threshold_summary(
    tower_shape_rows: list[dict[str, Any]],
    legacy_rows: list[dict[str, Any]],
) -> tuple[CollapseThresholdSummaryRow, ...]:
    grouped: dict[tuple[str, int], list[dict[str, Any]]] = defaultdict(list)
    for row in tower_shape_rows:
        if row["arm_id"] == NO_CONTRACTION_ARM_ID:
            continue
        if int(row["tier_index"]) != 1:
            continue
        grouped[(row["instance_id"], int(row["schema_seed"]))].append(row)
    legacy_by_key = {
        (row["instance_id"], int(row["schema_seed"])): _as_bool(row["equivalent"])
        for row in legacy_rows
    }
    result = []
    for (instance_id, schema_seed), rows in sorted(grouped.items()):
        by_n = {int(row["numerator"]): row for row in rows}
        full = [
            numerator
            for numerator, row in by_n.items()
            if _as_bool(row["full_collapse"]) or int(row["state_cell_count"]) == 1
        ]
        near = [
            numerator
            for numerator, row in by_n.items()
            if _as_bool(row["near_collapse"])
            or float(row["largest_state_cell_share"]) >= NEAR_FULL_COLLAPSE_THRESHOLD
        ]
        nontrivial = [
            numerator
            for numerator, row in by_n.items()
            if int(row["state_cell_count"]) > 1
            and float(row["largest_state_cell_share"]) < NEAR_FULL_COLLAPSE_THRESHOLD
        ]
        first_full = min(full) if full else None
        first_near = min(near) if near else first_full
        last_nontrivial = max(nontrivial) if nontrivial else None
        if first_full == 1:
            verdict = "immediate_collapse"
        elif first_full is not None:
            verdict = "threshold_found"
        elif len(by_n) >= 6:
            verdict = "no_collapse"
        else:
            verdict = "mixed"
        result.append(
            CollapseThresholdSummaryRow(
                evaluation_id=EVALUATION_ID,
                instance_id=instance_id,
                schema_seed=schema_seed,
                first_full_collapse_numerator=first_full,
                first_near_collapse_numerator=first_near,
                last_nontrivial_numerator=last_nontrivial,
                n06_matches_legacy=legacy_by_key.get((instance_id, schema_seed)),
                sweep_verdict=verdict,
            )
        )
    return tuple(result)


def _classification(
    *,
    full_collapse: bool,
    near_full: bool,
    selected_non_exec: int,
    no_available: int,
    zero_steps: bool,
    missing_abc: bool,
) -> str:
    labels: list[str] = []
    if full_collapse:
        labels.append("full_first_projection_collapse")
    elif near_full:
        labels.append("near_full_first_projection_collapse")
    if selected_non_exec:
        labels.append("selected_tier_non_executability")
    if no_available:
        labels.append("no_available_action")
    if zero_steps:
        labels.append("zero_concrete_steps")
    if missing_abc:
        labels.append("missing_abc_context")
    return "+".join(labels) if labels else "diagnostic_complete"


def _run_root(artifact_root: Path, run_id: str) -> Path:
    return artifact_root / "runs" / EVALUATION_RUN_FAMILY_ID / "runs" / run_id


def _read_csv(path: Path) -> list[dict[str, str]]:
    if not path.exists():
        return []
    return list(csv.DictReader(path.open()))


def _read_json(path: Path) -> dict[str, Any]:
    if not path.exists():
        return {}
    return json.loads(path.read_text())


def _as_bool(value: object) -> bool:
    return str(value) == "True" or value is True


def _as_float(value: object) -> float:
    if value is None or value == "":
        return 0.0
    return float(value)


def _share(count: int, total: int) -> float | None:
    if total <= 0:
        return None
    return count / total

