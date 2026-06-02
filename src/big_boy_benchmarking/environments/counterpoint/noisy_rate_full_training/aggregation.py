"""Aggregation for noisy-rate full-tower training diagnostics."""

from __future__ import annotations

import csv
import json
import statistics
from collections import Counter, defaultdict
from pathlib import Path
from typing import Any

from big_boy_benchmarking.artifacts.writers import write_csv, write_json
from big_boy_benchmarking.environments.counterpoint.noisy_rate_full_training.config import (
    EVALUATION_ID,
    MINIMUM_CONCRETE_STEP_COUNT_FOR_CLEAN,
    MINIMUM_LEARNER_UPDATE_COUNT_FOR_CLEAN,
    MINIMUM_LIFT_SUCCESS_COUNT_FOR_CLEAN,
    SELECTED_TIER_NON_EXECUTABILITY_WARNING_COUNT,
    ZERO_STEP_EPISODE_SHARE_WARNING,
)
from big_boy_benchmarking.environments.counterpoint.noisy_rate_full_training.events import (
    FullTrainingABCSelectionSummaryRow,
    FullTrainingABCTierSignalSummaryRow,
    FullTrainingAggregateTableRow,
    FullTrainingCandidateSummaryRow,
    FullTrainingConcreteStepSummaryRow,
    FullTrainingControlActionSummaryRow,
    FullTrainingCurveSummaryRow,
    FullTrainingHealthSummaryRow,
    FullTrainingLearnerUpdateSummaryRow,
    FullTrainingLiftByTierRow,
    FullTrainingTierExecutabilitySummaryRow,
    FullTrainingTierOccupancySummaryRow,
    FullTrainingTowerShapeSummaryRow,
)
from big_boy_benchmarking.environments.counterpoint.noisy_rate_full_training.manifests import (
    aggregate_summary_payload,
    readout_source_payload,
)
from big_boy_benchmarking.environments.counterpoint.noisy_rate_full_training.paths import (
    build_noisy_rate_full_training_paths,
    repo_readout_surface,
    validate_repo_resident_artifact_root,
)


def aggregate_noisy_rate_full_training_results(
    artifact_root: Path | str,
    *,
    docs_root: Path | str | None = None,
) -> dict[str, Any]:
    artifact_root = validate_repo_resident_artifact_root(artifact_root)
    paths = build_noisy_rate_full_training_paths(artifact_root)
    paths.results_dir.mkdir(parents=True, exist_ok=True)
    if not paths.evaluation_run_index_csv.exists():
        raise FileNotFoundError(f"missing evaluation run index: {paths.evaluation_run_index_csv}")
    run_rows = list(csv.DictReader(paths.evaluation_run_index_csv.open(encoding="utf-8")))
    candidate_manifest = _read_json(paths.candidate_manifest)
    budget = _read_json(paths.evaluation_budget_lock)

    candidate_rows = candidate_manifest.get("selected_candidates", [])
    tower_rows: list[dict[str, Any]] = []
    episode_rows_all: list[dict[str, Any]] = []
    curve_rows: list[dict[str, Any]] = []
    occupancy_rows: list[dict[str, Any]] = []
    executability_rows: list[dict[str, Any]] = []
    lift_success_rows: list[dict[str, Any]] = []
    lift_failure_rows: list[dict[str, Any]] = []
    concrete_rows: list[dict[str, Any]] = []
    control_action_rows: list[dict[str, Any]] = []
    abc_selection_rows: list[dict[str, Any]] = []
    abc_tier_signal_rows: list[dict[str, Any]] = []
    learner_update_rows: list[dict[str, Any]] = []
    health_rows: list[dict[str, Any]] = []
    aggregate_rows: list[dict[str, Any]] = []

    complete_run_count = 0
    for run_row in run_rows:
        if run_row["status"] != "success":
            aggregate = _failed_aggregate_row(run_row)
            aggregate_rows.append(aggregate.to_flat_dict())
            health_rows.append(_failed_health_row(run_row).to_flat_dict())
            continue
        complete_run_count += 1
        run_root = _run_root(artifact_root, run_row["run_id"])
        quotient = _read_json(run_root / "quotient_summary.json")
        episodes = _read_csv(run_root / "episodes.csv")
        steps = _read_csv(run_root / "step_events.csv")
        controls = _read_csv(run_root / "control_events.csv")
        lifts = _read_csv(run_root / "lift_fiber_events.csv")
        abc_selections = _read_csv(run_root / "abc_selection_events.csv")
        abc_tiers = _read_csv(run_root / "abc_tier_signal_events.csv")
        learner_updates = _read_csv(run_root / "learner_update_events.csv")

        tower_rows.extend(quotient.get("tower_shape_summary", []))
        episode_rows_all.extend(episodes)
        curve_rows.extend(row.to_flat_dict() for row in _training_curve_summary(run_row, episodes, steps, lifts, abc_selections, learner_updates))
        occupancy_rows.extend(row.to_flat_dict() for row in _tier_occupancy_summary(run_row, controls, steps))
        executability_rows.extend(row.to_flat_dict() for row in _tier_executability_summary(run_row, abc_tiers))
        lift_rows = _lift_by_tier_summary(run_row, lifts)
        lift_success_rows.extend(row.to_flat_dict() for row in lift_rows if row.lift_success_count > 0)
        lift_failure_rows.extend(row.to_flat_dict() for row in lift_rows if row.lift_failure_count > 0)
        concrete_rows.append(_concrete_step_summary(run_row, episodes, steps).to_flat_dict())
        control_action_rows.extend(row.to_flat_dict() for row in _control_action_summary(run_row, controls))
        abc_selection_rows.extend(row.to_flat_dict() for row in _abc_selection_summary(run_row, abc_selections))
        abc_tier_signal_rows.extend(row.to_flat_dict() for row in _abc_tier_signal_summary(run_row, abc_tiers))
        learner_update_rows.append(_learner_update_summary(run_row, learner_updates).to_flat_dict())
        health = _health_summary(run_row, quotient, episodes, steps, lifts, abc_selections, learner_updates)
        health_rows.append(health.to_flat_dict())
        aggregate_rows.append(_aggregate_row(run_row, health, steps, lifts, learner_updates, abc_selections).to_flat_dict())

    result_paths = (
        paths.results_dir / "candidate_summary.csv",
        paths.results_dir / "tower_shape_summary.csv",
        paths.results_dir / "training_episode_summary.csv",
        paths.results_dir / "training_curve_summary.csv",
        paths.results_dir / "tier_occupancy_summary.csv",
        paths.results_dir / "tier_executability_summary.csv",
        paths.results_dir / "lift_success_by_tier.csv",
        paths.results_dir / "lift_failure_by_tier.csv",
        paths.results_dir / "concrete_step_summary.csv",
        paths.results_dir / "controller_action_summary.csv",
        paths.results_dir / "abc_selection_summary.csv",
        paths.results_dir / "abc_tier_signal_summary.csv",
        paths.results_dir / "learner_update_summary.csv",
        paths.results_dir / "training_health_summary.csv",
    )
    write_csv(result_paths[0], candidate_rows, FullTrainingCandidateSummaryRow.fieldnames())
    write_csv(result_paths[1], tower_rows, FullTrainingTowerShapeSummaryRow.fieldnames())
    write_csv(result_paths[2], episode_rows_all, _fieldnames_from_rows(episode_rows_all))
    write_csv(result_paths[3], curve_rows, FullTrainingCurveSummaryRow.fieldnames())
    write_csv(result_paths[4], occupancy_rows, FullTrainingTierOccupancySummaryRow.fieldnames())
    write_csv(result_paths[5], executability_rows, FullTrainingTierExecutabilitySummaryRow.fieldnames())
    write_csv(result_paths[6], lift_success_rows, FullTrainingLiftByTierRow.fieldnames())
    write_csv(result_paths[7], lift_failure_rows, FullTrainingLiftByTierRow.fieldnames())
    write_csv(result_paths[8], concrete_rows, FullTrainingConcreteStepSummaryRow.fieldnames())
    write_csv(result_paths[9], control_action_rows, FullTrainingControlActionSummaryRow.fieldnames())
    write_csv(result_paths[10], abc_selection_rows, FullTrainingABCSelectionSummaryRow.fieldnames())
    write_csv(result_paths[11], abc_tier_signal_rows, FullTrainingABCTierSignalSummaryRow.fieldnames())
    write_csv(result_paths[12], learner_update_rows, FullTrainingLearnerUpdateSummaryRow.fieldnames())
    write_csv(result_paths[13], health_rows, FullTrainingHealthSummaryRow.fieldnames())
    write_csv(paths.evaluation_aggregate_table_csv, aggregate_rows, FullTrainingAggregateTableRow.fieldnames())
    health_counts = Counter(row["training_health_class"] for row in health_rows)
    status = "complete" if run_rows and complete_run_count == len(run_rows) else "incomplete"
    summary = aggregate_summary_payload(
        status=status,
        run_count=len(run_rows),
        complete_run_count=complete_run_count,
        table_path=paths.evaluation_aggregate_table_csv,
        result_paths=result_paths,
        health_class_counts=dict(health_counts),
    )
    write_json(paths.evaluation_aggregate_summary, summary)
    _write_readout_source(
        artifact_root=artifact_root,
        docs_root=Path(docs_root) if docs_root is not None else repo_readout_surface(),
        paths=paths,
        result_paths=result_paths,
        budget=budget,
        candidate_manifest=candidate_manifest,
    )
    return summary


def _write_readout_source(
    *,
    artifact_root: Path,
    docs_root: Path,
    paths,
    result_paths: tuple[Path, ...],
    budget: dict[str, Any],
    candidate_manifest: dict[str, Any],
) -> None:
    source_files = {
        "aggregate_table": paths.evaluation_aggregate_table_csv,
        "run_index": paths.evaluation_run_index_csv,
        "aggregate_summary": paths.evaluation_aggregate_summary,
        "candidate_manifest": paths.candidate_manifest,
        "candidate_summary": result_paths[0],
        "tower_shape_summary": result_paths[1],
        "training_episode_summary": result_paths[2],
        "training_curve_summary": result_paths[3],
        "tier_occupancy_summary": result_paths[4],
        "tier_executability_summary": result_paths[5],
        "lift_success_by_tier": result_paths[6],
        "lift_failure_by_tier": result_paths[7],
        "concrete_step_summary": result_paths[8],
        "controller_action_summary": result_paths[9],
        "abc_selection_summary": result_paths[10],
        "abc_tier_signal_summary": result_paths[11],
        "learner_update_summary": result_paths[12],
        "training_health_summary": result_paths[13],
    }
    parent_source = Path(str(candidate_manifest.get("parent_readout_source", "")))
    parent_source_payload = _read_json(parent_source)
    parent_root = Path(
        str(parent_source_payload.get("source_evaluation_root") or parent_source.parent)
    )
    docs_root.mkdir(parents=True, exist_ok=True)
    payload = readout_source_payload(
        repo_readout_surface=docs_root,
        source_artifact_root=artifact_root,
        source_evaluation_root=paths.root,
        artifact_run_label=artifact_root.name,
        parent_readout_source=parent_source,
        parent_source_evaluation_root=parent_root,
        source_files=source_files,
        budget=budget,
    )
    write_json(docs_root / "readout_source.json", payload, create_parents=True)
    write_json(paths.readout_source, payload, create_parents=True)


def _run_root(artifact_root: Path, run_id: str) -> Path:
    return artifact_root / "runs" / "counterpoint_symbolic_v001_noisy_rate_full_tower_training_diagnostic_v001" / "runs" / run_id


def _training_curve_summary(
    run_row: dict[str, str],
    episodes: list[dict[str, str]],
    steps: list[dict[str, str]],
    lifts: list[dict[str, str]],
    abc_selections: list[dict[str, str]],
    learner_updates: list[dict[str, str]],
) -> tuple[FullTrainingCurveSummaryRow, ...]:
    if not episodes:
        return ()
    start = min(int(row["episode_index"]) for row in episodes)
    end = max(int(row["episode_index"]) for row in episodes)
    rewards = [_as_float(row["total_reward"]) for row in episodes]
    concrete_counts = [_as_float(row["concrete_step_count"]) for row in episodes]
    lift_success_share = _share(sum(_as_bool(row["success"]) for row in lifts), len(lifts))
    deepest = _deepest_tier(abc_selections)
    selected_deepest = sum(
        int(row.get("selected_tier") or -1) == deepest for row in abc_selections
    )
    step_deepest = sum(int(row.get("active_tier_after") or -1) == deepest for row in steps)
    return (
        FullTrainingCurveSummaryRow(
            evaluation_id=EVALUATION_ID,
            run_id=run_row["run_id"],
            candidate_id=run_row["candidate_id"],
            training_replicate_index=int(run_row["training_replicate_index"]),
            episode_window_start=start,
            episode_window_end=end,
            mean_total_reward=statistics.mean(rewards) if rewards else None,
            mean_concrete_step_count=statistics.mean(concrete_counts)
            if concrete_counts
            else None,
            mean_lift_success_share=lift_success_share,
            mean_selected_deepest_tier_share=_share(selected_deepest, len(abc_selections)),
            mean_deepest_tier_concrete_step_share=_share(step_deepest, len(steps)),
            zero_step_episode_count=sum(int(row["concrete_step_count"]) == 0 for row in episodes),
            learner_update_count=len(learner_updates),
        ),
    )


def _tier_occupancy_summary(
    run_row: dict[str, str],
    control_rows: list[dict[str, str]],
    step_rows: list[dict[str, str]],
) -> tuple[FullTrainingTierOccupancySummaryRow, ...]:
    grouped: dict[tuple[str, str], list[dict[str, str]]] = defaultdict(list)
    for row in control_rows:
        grouped[(row["active_tier_after"], row["control_action"])].append(row)
    control_by_event = {
        (row["episode_index"], row["controller_event_index"]): row for row in control_rows
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
        result.append(
            FullTrainingTierOccupancySummaryRow(
                **_context(run_row),
                tier_index=None if tier_text == "" else int(tier_text),
                control_action=action,
                event_count=len(rows),
                event_share=len(rows) / total_events,
                concrete_step_count=len(rewards),
                concrete_step_share=len(rewards) / total_steps,
                mean_reward_on_concrete_steps=statistics.mean(rewards) if rewards else None,
            )
        )
    return tuple(result)


def _tier_executability_summary(
    run_row: dict[str, str],
    tier_rows: list[dict[str, str]],
) -> tuple[FullTrainingTierExecutabilitySummaryRow, ...]:
    grouped: dict[int, list[dict[str, str]]] = defaultdict(list)
    for row in tier_rows:
        grouped[int(row["tier_index"])].append(row)
    return tuple(
        FullTrainingTierExecutabilitySummaryRow(
            **_context(run_row),
            tier_index=tier,
            event_count=len(rows),
            executable_event_count=sum(_as_bool(row["executable"]) for row in rows),
            executable_event_share=_share(
                sum(_as_bool(row["executable"]) for row in rows), len(rows)
            ),
            selected_event_count=sum(_as_bool(row["selected"]) for row in rows),
        )
        for tier, rows in sorted(grouped.items())
    )


def _lift_by_tier_summary(
    run_row: dict[str, str],
    lift_rows: list[dict[str, str]],
) -> tuple[FullTrainingLiftByTierRow, ...]:
    grouped: dict[tuple[str, str, str], list[dict[str, str]]] = defaultdict(list)
    for row in lift_rows:
        grouped[(row["active_tier"], row["failure_reason"], row["fiber_departure_reason"])].append(row)
    result = []
    for (tier_text, failure, fiber), rows in sorted(grouped.items()):
        counts = [_as_float(row["candidate_count"]) for row in rows]
        successes = sum(_as_bool(row["success"]) for row in rows)
        result.append(
            FullTrainingLiftByTierRow(
                **_context(run_row),
                active_tier=None if tier_text == "" else int(tier_text),
                failure_reason=failure or None,
                fiber_departure_reason=fiber or None,
                lift_attempt_count=len(rows),
                lift_success_count=successes,
                lift_failure_count=len(rows) - successes,
                mean_candidate_count=statistics.mean(counts) if counts else None,
            )
        )
    return tuple(result)


def _concrete_step_summary(
    run_row: dict[str, str],
    episode_rows: list[dict[str, str]],
    step_rows: list[dict[str, str]],
) -> FullTrainingConcreteStepSummaryRow:
    rewards = [_as_float(row["reward"]) for row in step_rows]
    final_counts = Counter(row["final_state"] for row in episode_rows)
    return FullTrainingConcreteStepSummaryRow(
        **_context(run_row),
        episode_count=len(episode_rows),
        concrete_step_count=len(step_rows),
        zero_step_episode_count=sum(int(row["concrete_step_count"]) == 0 for row in episode_rows),
        mean_reward=statistics.mean(rewards) if rewards else None,
        terminated_count=sum(_as_bool(row["terminated"]) for row in episode_rows),
        truncated_count=sum(_as_bool(row["truncated"]) for row in episode_rows),
        final_state_summary=json.dumps(dict(final_counts), sort_keys=True),
    )


def _control_action_summary(
    run_row: dict[str, str],
    control_rows: list[dict[str, str]],
) -> tuple[FullTrainingControlActionSummaryRow, ...]:
    counts = Counter(row["control_action"] for row in control_rows)
    total = max(1, len(control_rows))
    return tuple(
        FullTrainingControlActionSummaryRow(
            **_context(run_row),
            control_action=action,
            event_count=count,
            event_share=count / total,
        )
        for action, count in sorted(counts.items())
    )


def _abc_selection_summary(
    run_row: dict[str, str],
    rows: list[dict[str, str]],
) -> tuple[FullTrainingABCSelectionSummaryRow, ...]:
    grouped: dict[tuple[str, str, str, str], list[dict[str, str]]] = defaultdict(list)
    for row in rows:
        grouped[(row["selected_tier"], row["predicted_movement_direction"], row["control_action"], row["blocked_reason"])].append(row)
    result = []
    for (tier, movement, action, blocked), grouped_rows in sorted(grouped.items()):
        consistent = sum(_as_bool(row["action_consistent"]) for row in grouped_rows)
        result.append(
            FullTrainingABCSelectionSummaryRow(
                **_context(run_row),
                selected_tier=None if tier == "" else int(tier),
                predicted_movement_direction=movement,
                control_action=action,
                blocked_reason=blocked or None,
                event_count=len(grouped_rows),
                action_consistent_count=consistent,
                action_consistent_share=_share(consistent, len(grouped_rows)),
            )
        )
    return tuple(result)


def _abc_tier_signal_summary(
    run_row: dict[str, str],
    rows: list[dict[str, str]],
) -> tuple[FullTrainingABCTierSignalSummaryRow, ...]:
    grouped: dict[int, list[dict[str, str]]] = defaultdict(list)
    for row in rows:
        grouped[int(row["tier_index"])].append(row)
    result = []
    for tier, grouped_rows in sorted(grouped.items()):
        pressures = [_as_float(row["productive_learning_pressure"]) for row in grouped_rows]
        result.append(
            FullTrainingABCTierSignalSummaryRow(
                **_context(run_row),
                tier_index=tier,
                event_count=len(grouped_rows),
                executable_event_share=_share(sum(_as_bool(row["executable"]) for row in grouped_rows), len(grouped_rows)),
                unclosed_event_share=_share(sum(_as_bool(row["unclosed"]) for row in grouped_rows), len(grouped_rows)),
                mean_productive_learning_pressure=statistics.mean(pressures) if pressures else None,
                selected_event_count=sum(_as_bool(row["selected"]) for row in grouped_rows),
                active_event_count=sum(_as_bool(row["active"]) for row in grouped_rows),
            )
        )
    return tuple(result)


def _learner_update_summary(
    run_row: dict[str, str],
    rows: list[dict[str, str]],
) -> FullTrainingLearnerUpdateSummaryRow:
    successes = [row for row in rows if _as_bool(row["success"])]
    errors = [_as_float(row["td_error"]) for row in rows if row.get("td_error") not in ("", None)]
    return FullTrainingLearnerUpdateSummaryRow(
        **_context(run_row),
        update_count=len(rows),
        successful_update_count=len(successes),
        mean_td_error=statistics.mean(errors) if errors else None,
    )


def _health_summary(
    run_row: dict[str, str],
    quotient: dict[str, Any],
    episodes: list[dict[str, str]],
    steps: list[dict[str, str]],
    lifts: list[dict[str, str]],
    abc_rows: list[dict[str, str]],
    learner_updates: list[dict[str, str]],
) -> FullTrainingHealthSummaryRow:
    tower_counts = quotient.get("state_cell_count_by_tier", [])
    tower_noncollapsed = bool(tower_counts) and int(tower_counts[-1]) > 1
    active_counts = quotient.get("active_action_cell_count_by_tier", [])
    deepest_executable = bool(active_counts) and int(active_counts[-1]) > 0
    concrete_positive = len(steps) >= MINIMUM_CONCRETE_STEP_COUNT_FOR_CLEAN
    lift_success_count = sum(_as_bool(row["success"]) for row in lifts)
    lift_positive = lift_success_count >= MINIMUM_LIFT_SUCCESS_COUNT_FOR_CLEAN
    update_success_count = sum(_as_bool(row["success"]) for row in learner_updates)
    updates_positive = update_success_count >= MINIMUM_LEARNER_UPDATE_COUNT_FOR_CLEAN
    zero_share = _share(
        sum(int(row["concrete_step_count"]) == 0 for row in episodes), len(episodes)
    )
    no_available = sum(row["control_action"] == "no_available_action" for row in abc_rows)
    selected_non_exec = sum(row["blocked_reason"] == "selected_tier_non_executable" for row in abc_rows)
    health_class = _training_health_class(
        artifact_complete=True,
        tower_noncollapsed=tower_noncollapsed,
        deepest_tier_executable=deepest_executable,
        concrete_steps_positive=concrete_positive,
        lift_successes_positive=lift_positive,
        learner_updates_positive=updates_positive,
        zero_step_episode_share=zero_share,
        no_available_action_event_count=no_available,
        selected_tier_non_executability_count=selected_non_exec,
    )
    return FullTrainingHealthSummaryRow(
        evaluation_id=EVALUATION_ID,
        run_id=run_row["run_id"],
        candidate_id=run_row["candidate_id"],
        status=run_row["status"],
        training_health_class=health_class,
        artifact_complete=True,
        tower_noncollapsed=tower_noncollapsed,
        deepest_tier_executable=deepest_executable,
        concrete_steps_positive=concrete_positive,
        lift_successes_positive=lift_positive,
        learner_updates_positive=updates_positive,
        zero_step_episode_share=zero_share,
        no_available_action_event_count=no_available,
        selected_tier_non_executability_count=selected_non_exec,
        claim_if_met="Candidate supports tower-only training health under this locked budget.",
        claim_if_not_met="Candidate does not support a clean training-health claim under this locked budget.",
    )


def _training_health_class(
    *,
    artifact_complete: bool,
    tower_noncollapsed: bool,
    deepest_tier_executable: bool,
    concrete_steps_positive: bool,
    lift_successes_positive: bool,
    learner_updates_positive: bool,
    zero_step_episode_share: float | None,
    no_available_action_event_count: int,
    selected_tier_non_executability_count: int,
) -> str:
    if not artifact_complete:
        return "artifact_incomplete"
    if not tower_noncollapsed or not deepest_tier_executable:
        return "untrainable_non_executable_tier"
    if not concrete_steps_positive:
        return "untrainable_no_concrete_steps"
    if not lift_successes_positive:
        return "untrainable_lift_failure"
    if not learner_updates_positive:
        return "runtime_executable_but_training_weak"
    warnings = (
        (zero_step_episode_share or 0.0) > ZERO_STEP_EPISODE_SHARE_WARNING
        or no_available_action_event_count > 0
        or selected_tier_non_executability_count
        > SELECTED_TIER_NON_EXECUTABILITY_WARNING_COUNT
    )
    return "trainable_with_warnings" if warnings else "trainable_clean"


def _aggregate_row(
    run_row: dict[str, str],
    health: FullTrainingHealthSummaryRow,
    steps: list[dict[str, str]],
    lifts: list[dict[str, str]],
    learner_updates: list[dict[str, str]],
    abc_rows: list[dict[str, str]],
) -> FullTrainingAggregateTableRow:
    return FullTrainingAggregateTableRow(
        evaluation_id=EVALUATION_ID,
        run_id=run_row["run_id"],
        candidate_id=run_row["candidate_id"],
        instance_id=run_row["instance_id"],
        arm_id=run_row["arm_id"],
        schema_seed=int(run_row["schema_seed"]),
        training_replicate_index=int(run_row["training_replicate_index"]),
        status=run_row["status"],
        training_health_class=health.training_health_class,
        concrete_step_count=len(steps),
        lift_success_count=sum(_as_bool(row["success"]) for row in lifts),
        learner_update_count=sum(_as_bool(row["success"]) for row in learner_updates),
        zero_step_episode_share=health.zero_step_episode_share,
        selected_tier_non_executability_count=sum(
            row["blocked_reason"] == "selected_tier_non_executable" for row in abc_rows
        ),
        no_available_action_event_count=sum(
            row["control_action"] == "no_available_action" for row in abc_rows
        ),
        artifact_root=run_row["artifact_root"],
        failure_reason=run_row.get("failure_reason") or None,
    )


def _failed_aggregate_row(run_row: dict[str, str]) -> FullTrainingAggregateTableRow:
    return FullTrainingAggregateTableRow(
        evaluation_id=EVALUATION_ID,
        run_id=run_row.get("run_id", ""),
        candidate_id=run_row["candidate_id"],
        instance_id=run_row["instance_id"],
        arm_id=run_row["arm_id"],
        schema_seed=int(run_row["schema_seed"]),
        training_replicate_index=int(run_row["training_replicate_index"]),
        status=run_row["status"],
        training_health_class="artifact_incomplete",
        concrete_step_count=0,
        lift_success_count=0,
        learner_update_count=0,
        zero_step_episode_share=None,
        selected_tier_non_executability_count=0,
        no_available_action_event_count=0,
        artifact_root=run_row["artifact_root"],
        failure_reason=run_row.get("failure_reason") or None,
    )


def _failed_health_row(run_row: dict[str, str]) -> FullTrainingHealthSummaryRow:
    return FullTrainingHealthSummaryRow(
        evaluation_id=EVALUATION_ID,
        run_id=run_row.get("run_id", ""),
        candidate_id=run_row["candidate_id"],
        status=run_row["status"],
        training_health_class="artifact_incomplete",
        artifact_complete=False,
        tower_noncollapsed=False,
        deepest_tier_executable=False,
        concrete_steps_positive=False,
        lift_successes_positive=False,
        learner_updates_positive=False,
        zero_step_episode_share=None,
        no_available_action_event_count=0,
        selected_tier_non_executability_count=0,
        claim_if_met="No claim supported.",
        claim_if_not_met="Run artifacts are incomplete.",
    )


def _context(run_row: dict[str, str]) -> dict[str, Any]:
    return {
        "evaluation_id": EVALUATION_ID,
        "run_id": run_row["run_id"],
        "candidate_id": run_row["candidate_id"],
        "instance_id": run_row["instance_id"],
        "arm_id": run_row["arm_id"],
        "schema_seed": int(run_row["schema_seed"]),
        "training_replicate_index": int(run_row["training_replicate_index"]),
    }


def _deepest_tier(rows: list[dict[str, str]]) -> int:
    values = [int(row["deepest_known_tier"]) for row in rows if row.get("deepest_known_tier")]
    return max(values, default=0)


def _read_csv(path: Path) -> list[dict[str, str]]:
    if not path.exists():
        return []
    return list(csv.DictReader(path.open(encoding="utf-8")))


def _read_json(path: Path) -> dict[str, Any]:
    if not path.exists():
        return {}
    return json.loads(path.read_text(encoding="utf-8"))


def _as_bool(value: object) -> bool:
    return value is True or value == "True"


def _as_float(value: object) -> float:
    if value in (None, ""):
        return 0.0
    return float(value)


def _share(numerator: int, denominator: int) -> float | None:
    if denominator <= 0:
        return None
    return numerator / denominator


def _fieldnames_from_rows(rows: list[dict[str, Any]]) -> tuple[str, ...]:
    if not rows:
        return ()
    return tuple(rows[0].keys())
