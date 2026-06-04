"""Aggregation for the second serious counterpoint schema comparison."""

from __future__ import annotations

import csv
import json
import statistics
from collections import Counter, defaultdict
from pathlib import Path
from typing import Any

from big_boy_benchmarking.artifacts.writers import write_csv, write_json
from big_boy_benchmarking.environments.counterpoint.second_serious_comparison.config import (
    EVALUATION_ID,
    SCHEMA0_CLASS_ID,
    SCHEMA1_CLASS_ID,
    SCHEMA1_TOWER_SOURCE_FULL_ITERATED,
)
from big_boy_benchmarking.environments.counterpoint.second_serious_comparison.events import (
    ArmSummaryRow,
    ComparisonAggregateTableRow,
    ComparisonCandidateSummaryRow,
    ComparisonClaimSummaryRow,
    FirstSustainedHitSummaryRow,
    PairedSchemaComparisonRow,
)
from big_boy_benchmarking.environments.counterpoint.second_serious_comparison.manifests import (
    readout_source_payload,
)
from big_boy_benchmarking.environments.counterpoint.second_serious_comparison.paths import (
    build_second_serious_comparison_paths,
    repo_readout_surface,
    validate_repo_resident_artifact_root,
)


def aggregate_second_serious_comparison_results(
    artifact_root: Path | str,
    *,
    docs_root: Path | str | None = None,
) -> dict[str, Any]:
    artifact_root = validate_repo_resident_artifact_root(artifact_root)
    paths = build_second_serious_comparison_paths(artifact_root)
    paths.results_dir.mkdir(parents=True, exist_ok=True)
    if not paths.evaluation_run_index_csv.exists():
        raise FileNotFoundError(f"missing evaluation run index: {paths.evaluation_run_index_csv}")

    run_rows = _read_csv(paths.evaluation_run_index_csv)
    budget = _read_json(paths.evaluation_budget_lock)
    candidate_manifest = _read_json(paths.candidate_manifest)
    episode_rows_all: list[dict[str, str]] = []
    first_hit_rows: list[dict[str, str]] = []
    threshold_rows: list[dict[str, str]] = []
    tower_rows: list[dict[str, str]] = []
    aggregate_rows: list[dict[str, Any]] = []
    control_rows: list[dict[str, str]] = []
    lift_rows: list[dict[str, str]] = []
    abc_selection_rows: list[dict[str, str]] = []
    abc_tier_rows: list[dict[str, str]] = []
    learner_rows: list[dict[str, str]] = []
    timing_rows: list[dict[str, Any]] = []
    complete_run_count = 0

    for run_row in run_rows:
        if run_row["status"] != "success":
            aggregate_rows.append(_failed_aggregate_row(run_row))
            continue
        complete_run_count += 1
        run_root = _run_root(artifact_root, run_row["run_id"])
        episodes = _read_csv(run_root / "episodes.csv")
        first_hit = _read_csv(run_root / "first_sustained_hit_summary.csv")
        thresholds = _read_csv(run_root / "threshold_window_events.csv")
        tower = _read_csv(run_root / "tower_shape_summary.csv")
        controls = _read_csv(run_root / "control_events.csv")
        lifts = _read_csv(run_root / "lift_fiber_events.csv")
        abc_selection = _read_csv(run_root / "abc_selection_events.csv")
        abc_tiers = _read_csv(run_root / "abc_tier_signal_events.csv")
        learners = _read_csv(run_root / "learner_update_events.csv")
        timing_summary = _read_json(run_root / "timing_summary.json")
        episode_rows_all.extend(episodes)
        first_hit_rows.extend(first_hit)
        threshold_rows.extend(thresholds)
        tower_rows.extend(tower)
        control_rows.extend(controls)
        lift_rows.extend(lifts)
        abc_selection_rows.extend(abc_selection)
        abc_tier_rows.extend(abc_tiers)
        learner_rows.extend(learners)
        timing_rows.append(
            {
                "run_id": run_row["run_id"],
                "schema_class_id": run_row["schema_class_id"],
                "timing_summary": json.dumps(timing_summary, sort_keys=True),
            }
        )
        aggregate_rows.append(_aggregate_row(run_row, episodes, first_hit, lifts, learners))

    candidate_summary_rows = _candidate_summary_rows(
        candidate_manifest,
        budget=budget,
        tower_rows=tower_rows,
    )
    paired_rows = _paired_rows(run_rows, aggregate_rows)
    arm_rows = _arm_summary_rows(aggregate_rows)
    claim_rows = _claim_rows(budget, paired_rows)
    health_rows = _health_rows(aggregate_rows, tower_rows, lift_rows, abc_selection_rows)

    result_files = {
        "arm_summary": paths.results_dir / "arm_summary.csv",
        "candidate_summary": paths.results_dir / "candidate_summary.csv",
        "schema_summary": paths.results_dir / "schema_summary.csv",
        "training_episode_summary": paths.results_dir / "training_episode_summary.csv",
        "training_curve_summary": paths.results_dir / "training_curve_summary.csv",
        "threshold_window_summary": paths.results_dir / "threshold_window_summary.csv",
        "first_sustained_hit_summary": paths.results_dir / "first_sustained_hit_summary.csv",
        "paired_schema_comparison": paths.results_dir / "paired_schema_comparison.csv",
        "schema0_total_space_summary": paths.results_dir / "schema0_total_space_summary.csv",
        "schema1_candidate_summary": paths.results_dir / "schema1_candidate_summary.csv",
        "tower_shape_summary": paths.results_dir / "tower_shape_summary.csv",
        "tier_occupancy_summary": paths.results_dir / "tier_occupancy_summary.csv",
        "tier_executability_summary": paths.results_dir / "tier_executability_summary.csv",
        "lift_success_by_tier": paths.results_dir / "lift_success_by_tier.csv",
        "lift_failure_by_tier": paths.results_dir / "lift_failure_by_tier.csv",
        "concrete_step_summary": paths.results_dir / "concrete_step_summary.csv",
        "controller_action_summary": paths.results_dir / "controller_action_summary.csv",
        "abc_selection_summary": paths.results_dir / "abc_selection_summary.csv",
        "abc_tier_signal_summary": paths.results_dir / "abc_tier_signal_summary.csv",
        "learner_update_summary": paths.results_dir / "learner_update_summary.csv",
        "timing_summary": paths.results_dir / "timing_summary.csv",
        "training_health_summary": paths.results_dir / "training_health_summary.csv",
        "comparison_claim_summary": paths.results_dir / "comparison_claim_summary.csv",
    }
    write_csv(
        result_files["arm_summary"],
        [row.to_flat_dict() for row in arm_rows],
        ArmSummaryRow.fieldnames(),
    )
    write_csv(
        result_files["candidate_summary"],
        candidate_summary_rows,
        ComparisonCandidateSummaryRow.fieldnames(),
    )
    write_csv(
        result_files["schema_summary"],
        _schema_summary_rows(aggregate_rows),
        _fieldnames(_schema_summary_rows(aggregate_rows)),
    )
    write_csv(
        result_files["training_episode_summary"], episode_rows_all, _fieldnames(episode_rows_all)
    )
    write_csv(
        result_files["training_curve_summary"],
        _training_curve_rows(episode_rows_all),
        _fieldnames(_training_curve_rows(episode_rows_all)),
    )
    write_csv(result_files["threshold_window_summary"], threshold_rows, _fieldnames(threshold_rows))
    write_csv(
        result_files["first_sustained_hit_summary"],
        first_hit_rows,
        FirstSustainedHitSummaryRow.fieldnames(),
    )
    write_csv(
        result_files["paired_schema_comparison"],
        [row.to_flat_dict() for row in paired_rows],
        PairedSchemaComparisonRow.fieldnames(),
    )
    write_csv(
        result_files["schema0_total_space_summary"],
        [row for row in aggregate_rows if row["schema_class_id"] == SCHEMA0_CLASS_ID],
        ComparisonAggregateTableRow.fieldnames(),
    )
    write_csv(
        result_files["schema1_candidate_summary"],
        [row for row in aggregate_rows if row["schema_class_id"] == SCHEMA1_CLASS_ID],
        ComparisonAggregateTableRow.fieldnames(),
    )
    write_csv(result_files["tower_shape_summary"], tower_rows, _fieldnames(tower_rows))
    write_csv(
        result_files["tier_occupancy_summary"],
        _tier_occupancy_rows(control_rows),
        _fieldnames(_tier_occupancy_rows(control_rows)),
    )
    write_csv(
        result_files["tier_executability_summary"],
        _tier_executability_rows(abc_tier_rows),
        _fieldnames(_tier_executability_rows(abc_tier_rows)),
    )
    write_csv(
        result_files["lift_success_by_tier"],
        _lift_rows(lift_rows, success=True),
        _fieldnames(_lift_rows(lift_rows, success=True)),
    )
    write_csv(
        result_files["lift_failure_by_tier"],
        _lift_rows(lift_rows, success=False),
        _fieldnames(_lift_rows(lift_rows, success=False)),
    )
    write_csv(
        result_files["concrete_step_summary"],
        _concrete_rows(episode_rows_all),
        _fieldnames(_concrete_rows(episode_rows_all)),
    )
    write_csv(
        result_files["controller_action_summary"],
        _controller_action_rows(control_rows),
        _fieldnames(_controller_action_rows(control_rows)),
    )
    write_csv(
        result_files["abc_selection_summary"],
        _abc_selection_summary_rows(abc_selection_rows),
        _fieldnames(_abc_selection_summary_rows(abc_selection_rows)),
    )
    write_csv(
        result_files["abc_tier_signal_summary"],
        _abc_tier_summary_rows(abc_tier_rows),
        _fieldnames(_abc_tier_summary_rows(abc_tier_rows)),
    )
    write_csv(
        result_files["learner_update_summary"],
        _learner_update_rows(learner_rows),
        _fieldnames(_learner_update_rows(learner_rows)),
    )
    write_csv(result_files["timing_summary"], timing_rows, _fieldnames(timing_rows))
    write_csv(result_files["training_health_summary"], health_rows, _fieldnames(health_rows))
    write_csv(
        result_files["comparison_claim_summary"],
        [row.to_flat_dict() for row in claim_rows],
        ComparisonClaimSummaryRow.fieldnames(),
    )
    write_csv(
        paths.evaluation_aggregate_table_csv,
        aggregate_rows,
        ComparisonAggregateTableRow.fieldnames(),
    )

    status = "complete" if run_rows and complete_run_count == len(run_rows) else "incomplete"
    summary = {
        "evaluation_id": EVALUATION_ID,
        "status": status,
        "run_count": len(run_rows),
        "complete_run_count": complete_run_count,
        "schema_class_counts": dict(Counter(row["schema_class_id"] for row in aggregate_rows)),
        "hit_status_counts": dict(Counter(row["hit_status"] for row in aggregate_rows)),
        "pair_count": len(paired_rows),
        "unblocked_pair_count": sum(not row.claim_blocked for row in paired_rows),
        "evaluation_aggregate_table": str(paths.evaluation_aggregate_table_csv),
        "result_files": {key: str(value) for key, value in result_files.items()},
    }
    write_json(paths.evaluation_aggregate_summary, summary)
    docs_root = Path(docs_root) if docs_root is not None else repo_readout_surface()
    _write_readout_source(
        artifact_root=artifact_root,
        docs_root=docs_root,
        paths=paths,
        result_files=result_files,
        budget=budget,
    )
    return summary


def _write_readout_source(
    *,
    artifact_root: Path,
    docs_root: Path,
    paths,
    result_files: dict[str, Path],
    budget: dict[str, Any],
) -> None:
    source_files = {
        "aggregate_table": paths.evaluation_aggregate_table_csv,
        "run_index": paths.evaluation_run_index_csv,
        "aggregate_summary": paths.evaluation_aggregate_summary,
        "evaluation_manifest": paths.evaluation_manifest,
        "evaluation_arm_manifest": paths.evaluation_arm_manifest,
        "evaluation_budget_lock": paths.evaluation_budget_lock,
        "threshold_policy_manifest": paths.threshold_policy_manifest,
        "tier_jump_policy_manifest": paths.tier_jump_policy_manifest,
        "candidate_manifest": paths.candidate_manifest,
        "parent_source_manifest": paths.parent_source_manifest,
        **result_files,
    }
    docs_root.mkdir(parents=True, exist_ok=True)
    payload = readout_source_payload(
        repo_readout_surface=docs_root,
        source_artifact_root=artifact_root,
        source_evaluation_root=paths.root,
        artifact_run_label=artifact_root.name,
        run_mode=str(budget.get("run_mode", "")),
        source_files=source_files,
        budget=budget,
    )
    write_json(docs_root / "readout_source.json", payload, create_parents=True)
    write_json(paths.readout_source, payload, create_parents=True)


def _candidate_summary_rows(
    candidate_manifest: dict[str, Any],
    *,
    budget: dict[str, Any],
    tower_rows: list[dict[str, str]],
) -> list[dict[str, Any]]:
    runtime_sequences = (
        _runtime_schema1_tier_sequences(tower_rows)
        if budget.get("schema1_tower_source") == SCHEMA1_TOWER_SOURCE_FULL_ITERATED
        else {}
    )
    rows = []
    for selected in candidate_manifest.get("selected_schema1_candidates", []):
        state_sequence, active_sequence = runtime_sequences.get(
            selected["candidate_id"],
            (
                selected["tier_state_cell_count_sequence"],
                selected["tier_active_action_cell_count_sequence"],
            ),
        )
        rows.append(
            ComparisonCandidateSummaryRow(
                evaluation_id=EVALUATION_ID,
                candidate_group_id=selected["candidate_id"],
                schema1_candidate_id=selected["candidate_id"],
                instance_id=selected["instance_id"],
                arm_id=selected["arm_id"],
                numerator=int(selected["numerator"]),
                denominator=int(selected["denominator"]),
                requested_rate=float(selected["requested_rate"]),
                selector_rule_id=selected["selector_rule_id"],
                schema_seed=int(selected["schema_seed"]),
                tier_state_cell_count_sequence=state_sequence,
                tier_active_action_cell_count_sequence=active_sequence,
                parent_training_health_class=selected["parent_training_health_class"],
                parent_concrete_step_count=int(selected["parent_concrete_step_count"]),
                parent_learner_update_count=int(selected["parent_learner_update_count"]),
                selected=True,
                exclusion_reason=None,
            ).to_flat_dict()
        )
    for excluded in candidate_manifest.get("excluded_schema1_candidates", []):
        rows.append(
            ComparisonCandidateSummaryRow(
                evaluation_id=EVALUATION_ID,
                candidate_group_id=excluded["candidate_id"],
                schema1_candidate_id=excluded["candidate_id"],
                instance_id=excluded["instance_id"],
                arm_id=excluded["arm_id"],
                numerator=int(excluded["numerator"]),
                denominator=int(excluded["denominator"]),
                requested_rate=float(excluded["requested_rate"]),
                selector_rule_id=excluded["selector_rule_id"],
                schema_seed=int(excluded["schema_seed"]),
                tier_state_cell_count_sequence=excluded["tier_state_cell_count_sequence"],
                tier_active_action_cell_count_sequence=excluded[
                    "tier_active_action_cell_count_sequence"
                ],
                parent_training_health_class=excluded["parent_training_health_class"],
                parent_concrete_step_count=int(excluded["parent_concrete_step_count"]),
                parent_learner_update_count=int(excluded["parent_learner_update_count"]),
                selected=False,
                exclusion_reason=excluded["candidate_exclusion_reason"],
            ).to_flat_dict()
        )
    return rows


def _runtime_schema1_tier_sequences(
    tower_rows: list[dict[str, str]],
) -> dict[str, tuple[str, str]]:
    rows_by_candidate_and_replicate: dict[tuple[str, int], list[dict[str, str]]] = defaultdict(
        list
    )
    for row in tower_rows:
        if row.get("schema_class_id") != SCHEMA1_CLASS_ID:
            continue
        rows_by_candidate_and_replicate[
            (row["candidate_id"], int(row.get("training_replicate_index") or 0))
        ].append(row)

    result = {}
    candidate_ids = {candidate_id for candidate_id, _ in rows_by_candidate_and_replicate}
    for candidate_id in candidate_ids:
        replicate_indices = sorted(
            replicate
            for current_candidate_id, replicate in rows_by_candidate_and_replicate
            if current_candidate_id == candidate_id
        )
        if not replicate_indices:
            continue
        rows = sorted(
            rows_by_candidate_and_replicate[(candidate_id, replicate_indices[0])],
            key=lambda item: int(item.get("tier_index") or 0),
        )
        state_sequence = [int(row.get("state_cell_count") or 0) for row in rows]
        active_sequence = [int(row.get("active_action_cell_count") or 0) for row in rows]
        result[candidate_id] = (
            json.dumps(state_sequence),
            json.dumps(active_sequence),
        )
    return result


def _aggregate_row(
    run_row: dict[str, str],
    episodes: list[dict[str, str]],
    first_hit_rows: list[dict[str, str]],
    lifts: list[dict[str, str]],
    learners: list[dict[str, str]],
) -> dict[str, Any]:
    first_hit = first_hit_rows[0] if first_hit_rows else {}
    rewards = [_float(row["total_reward"]) for row in episodes]
    structural = "ok"
    if first_hit.get("hit_status") == "artifact_incomplete":
        structural = "artifact_incomplete"
    return ComparisonAggregateTableRow(
        evaluation_id=EVALUATION_ID,
        run_id=run_row["run_id"],
        run_mode=run_row["run_mode"],
        candidate_group_id=run_row["candidate_group_id"],
        schema_class_id=run_row["schema_class_id"],
        candidate_id=run_row["candidate_id"],
        instance_id=run_row["instance_id"],
        arm_id=run_row["arm_id"],
        schema_seed=int(run_row["schema_seed"]),
        training_replicate_index=int(run_row["training_replicate_index"]),
        status=run_row["status"],
        hit_status=first_hit.get("hit_status", "artifact_incomplete"),
        first_sustained_hit_episode_index=_optional_int(
            first_hit.get("first_sustained_hit_episode_index")
        ),
        episodes_to_sustained_hit=_optional_int(first_hit.get("episodes_to_sustained_hit")),
        mean_total_reward=statistics.mean(rewards) if rewards else None,
        concrete_step_count=sum(int(row["concrete_step_count"]) for row in episodes),
        lift_success_count=sum(_bool(row["success"]) for row in lifts),
        learner_update_count=sum(_bool(row["success"]) for row in learners),
        structural_limit_classification=structural,
        artifact_root=run_row["artifact_root"],
        failure_reason=run_row.get("failure_reason") or None,
    ).to_flat_dict()


def _failed_aggregate_row(run_row: dict[str, str]) -> dict[str, Any]:
    return ComparisonAggregateTableRow(
        evaluation_id=EVALUATION_ID,
        run_id=run_row.get("run_id", ""),
        run_mode=run_row["run_mode"],
        candidate_group_id=run_row["candidate_group_id"],
        schema_class_id=run_row["schema_class_id"],
        candidate_id=run_row["candidate_id"],
        instance_id=run_row["instance_id"],
        arm_id=run_row["arm_id"],
        schema_seed=int(run_row["schema_seed"]),
        training_replicate_index=int(run_row["training_replicate_index"]),
        status=run_row["status"],
        hit_status="runtime_failed",
        first_sustained_hit_episode_index=None,
        episodes_to_sustained_hit=None,
        mean_total_reward=None,
        concrete_step_count=0,
        lift_success_count=0,
        learner_update_count=0,
        structural_limit_classification="runtime_failed",
        artifact_root=run_row["artifact_root"],
        failure_reason=run_row.get("failure_reason") or None,
    ).to_flat_dict()


def _paired_rows(
    run_rows: list[dict[str, str]],
    aggregate_rows: list[dict[str, Any]],
) -> tuple[PairedSchemaComparisonRow, ...]:
    seed_by_run = {row["run_id"]: row for row in run_rows}
    grouped: dict[tuple[str, str, str], dict[str, dict[str, Any]]] = defaultdict(dict)
    for row in aggregate_rows:
        seed = seed_by_run.get(row["run_id"], {})
        key = (
            row["candidate_group_id"],
            seed.get("seed_bundle_id", ""),
            str(row["training_replicate_index"]),
        )
        grouped[key][row["schema_class_id"]] = row
    result = []
    for (candidate_group_id, seed_bundle_id, replicate), rows in sorted(grouped.items()):
        schema0 = rows.get(SCHEMA0_CLASS_ID)
        schema1 = rows.get(SCHEMA1_CLASS_ID)
        if schema0 is None or schema1 is None:
            continue
        delta = None
        if schema0["episodes_to_sustained_hit"] not in (None, "") and schema1[
            "episodes_to_sustained_hit"
        ] not in (None, ""):
            delta = int(schema1["episodes_to_sustained_hit"]) - int(
                schema0["episodes_to_sustained_hit"]
            )
        claim_blocked = (
            schema0["structural_limit_classification"] != "ok"
            or schema1["structural_limit_classification"] != "ok"
            or schema0["hit_status"] != "sustained_hit"
            or schema1["hit_status"] != "sustained_hit"
        )
        if claim_blocked:
            pair_status = "blocked_or_non_sustained"
            interpretation = "Pair does not support speed-to-hit comparison."
        elif delta is None:
            pair_status = "unresolved"
            interpretation = "Pair has sustained hits but missing delta."
        elif delta < 0:
            pair_status = "schema1_faster"
            interpretation = "Schema 1 reached the sustained threshold sooner."
        elif delta > 0:
            pair_status = "schema1_slower"
            interpretation = "Schema 1 reached the sustained threshold later."
        else:
            pair_status = "same_episode_to_hit"
            interpretation = "Both schemas reached the sustained threshold at the same episode."
        result.append(
            PairedSchemaComparisonRow(
                evaluation_id=EVALUATION_ID,
                candidate_group_id=candidate_group_id,
                seed_bundle_id=seed_bundle_id,
                training_replicate_index=int(replicate),
                schema0_run_id=schema0["run_id"],
                schema1_run_id=schema1["run_id"],
                schema0_hit_status=schema0["hit_status"],
                schema1_hit_status=schema1["hit_status"],
                schema0_episodes_to_hit=schema0["episodes_to_sustained_hit"],
                schema1_episodes_to_hit=schema1["episodes_to_sustained_hit"],
                schema1_minus_schema0_episodes_to_hit=delta,
                pair_status=pair_status,
                claim_blocked=claim_blocked,
                interpretation=interpretation,
            )
        )
    return tuple(result)


def _arm_summary_rows(aggregate_rows: list[dict[str, Any]]) -> tuple[ArmSummaryRow, ...]:
    grouped: dict[str, list[dict[str, Any]]] = defaultdict(list)
    for row in aggregate_rows:
        grouped[row["schema_class_id"]].append(row)
    rows = []
    for schema_class_id, items in sorted(grouped.items()):
        sustained = [row for row in items if row["hit_status"] == "sustained_hit"]
        episodes = [
            int(row["episodes_to_sustained_hit"])
            for row in sustained
            if row["episodes_to_sustained_hit"] not in (None, "")
        ]
        rows.append(
            ArmSummaryRow(
                evaluation_id=EVALUATION_ID,
                schema_class_id=schema_class_id,
                run_count=len(items),
                sustained_hit_count=len(sustained),
                transient_hit_count=sum(row["hit_status"] == "transient_hit_only" for row in items),
                never_hit_count=sum(row["hit_status"] == "never_hit" for row in items),
                artifact_incomplete_count=sum(
                    row["hit_status"] in {"artifact_incomplete", "runtime_failed"} for row in items
                ),
                sustained_hit_rate=len(sustained) / len(items) if items else None,
                median_episodes_to_sustained_hit=statistics.median(episodes) if episodes else None,
            )
        )
    return tuple(rows)


def _claim_rows(
    budget: dict[str, Any],
    paired_rows: tuple[PairedSchemaComparisonRow, ...],
) -> tuple[ComparisonClaimSummaryRow, ...]:
    unblocked = [row for row in paired_rows if not row.claim_blocked]
    faster = sum(row.pair_status == "schema1_faster" for row in unblocked)
    slower = sum(row.pair_status == "schema1_slower" for row in unblocked)
    same = sum(row.pair_status == "same_episode_to_hit" for row in paired_rows)
    blocked = sum(row.claim_blocked for row in paired_rows)
    if not paired_rows:
        status = "no_pairs"
        text = "No paired Schema 0/Schema 1 rows were available."
    elif not unblocked:
        status = "claim_blocked"
        text = "All pairs are blocked or non-sustained; no speed-to-hit claim is supported."
    else:
        status = "bounded_comparison_available"
        text = (
            "At least one unblocked pair supports bounded speed-to-sustained-hit "
            "comparison under the locked threshold policy."
        )
    return (
        ComparisonClaimSummaryRow(
            evaluation_id=EVALUATION_ID,
            run_mode=str(budget.get("run_mode", "")),
            pair_count=len(paired_rows),
            unblocked_pair_count=len(unblocked),
            schema1_faster_pair_count=faster,
            schema1_slower_pair_count=slower,
            same_status_pair_count=same,
            blocked_pair_count=blocked,
            claim_status=status,
            bounded_claim_text=text,
        ),
    )


def _schema_summary_rows(rows: list[dict[str, Any]]) -> list[dict[str, Any]]:
    return [
        {
            "schema_class_id": row.schema_class_id,
            "run_count": row.run_count,
            "sustained_hit_count": row.sustained_hit_count,
            "sustained_hit_rate": row.sustained_hit_rate,
            "median_episodes_to_sustained_hit": row.median_episodes_to_sustained_hit,
        }
        for row in _arm_summary_rows(rows)
    ]


def _training_curve_rows(episodes: list[dict[str, str]]) -> list[dict[str, Any]]:
    grouped: dict[tuple[str, str], list[dict[str, str]]] = defaultdict(list)
    for row in episodes:
        grouped[(row["run_id"], row["schema_class_id"])].append(row)
    rows = []
    for (run_id, schema_class_id), items in sorted(grouped.items()):
        rewards = [_float(row["total_reward"]) for row in items]
        rows.append(
            {
                "evaluation_id": EVALUATION_ID,
                "run_id": run_id,
                "schema_class_id": schema_class_id,
                "episode_window_start": min(int(row["episode_index"]) for row in items),
                "episode_window_end": max(int(row["episode_index"]) for row in items),
                "mean_total_reward": statistics.mean(rewards) if rewards else None,
                "zero_step_episode_count": sum(
                    int(row["concrete_step_count"]) == 0 for row in items
                ),
            }
        )
    return rows


def _tier_occupancy_rows(rows: list[dict[str, str]]) -> list[dict[str, Any]]:
    grouped = Counter(
        (row["schema_class_id"], row["active_tier_after"], row["control_action"]) for row in rows
    )
    total = max(1, len(rows))
    return [
        {
            "evaluation_id": EVALUATION_ID,
            "schema_class_id": schema,
            "tier_index": tier,
            "control_action": action,
            "event_count": count,
            "event_share": count / total,
        }
        for (schema, tier, action), count in sorted(grouped.items())
    ]


def _tier_executability_rows(rows: list[dict[str, str]]) -> list[dict[str, Any]]:
    grouped: dict[tuple[str, str], list[dict[str, str]]] = defaultdict(list)
    for row in rows:
        grouped[(row["schema_class_id"], row["tier_index"])].append(row)
    return [
        {
            "evaluation_id": EVALUATION_ID,
            "schema_class_id": schema,
            "tier_index": tier,
            "event_count": len(items),
            "executable_event_count": sum(_bool(item["executable"]) for item in items),
            "selected_event_count": sum(_bool(item["selected"]) for item in items),
        }
        for (schema, tier), items in sorted(grouped.items())
    ]


def _lift_rows(rows: list[dict[str, str]], *, success: bool) -> list[dict[str, Any]]:
    filtered = [row for row in rows if _bool(row["success"]) is success]
    grouped = Counter(
        (row["schema_class_id"], row["active_tier"], row["failure_reason"]) for row in filtered
    )
    return [
        {
            "evaluation_id": EVALUATION_ID,
            "schema_class_id": schema,
            "active_tier": tier,
            "failure_reason": failure,
            "event_count": count,
        }
        for (schema, tier, failure), count in sorted(grouped.items())
    ]


def _concrete_rows(rows: list[dict[str, str]]) -> list[dict[str, Any]]:
    grouped: dict[tuple[str, str], list[dict[str, str]]] = defaultdict(list)
    for row in rows:
        grouped[(row["run_id"], row["schema_class_id"])].append(row)
    return [
        {
            "evaluation_id": EVALUATION_ID,
            "run_id": run_id,
            "schema_class_id": schema,
            "episode_count": len(items),
            "concrete_step_count": sum(int(row["concrete_step_count"]) for row in items),
            "zero_step_episode_count": sum(int(row["concrete_step_count"]) == 0 for row in items),
            "mean_total_reward": statistics.mean(_float(row["total_reward"]) for row in items),
        }
        for (run_id, schema), items in sorted(grouped.items())
    ]


def _controller_action_rows(rows: list[dict[str, str]]) -> list[dict[str, Any]]:
    grouped = Counter((row["schema_class_id"], row["control_action"]) for row in rows)
    return [
        {
            "evaluation_id": EVALUATION_ID,
            "schema_class_id": schema,
            "control_action": action,
            "event_count": count,
        }
        for (schema, action), count in sorted(grouped.items())
    ]


def _abc_selection_summary_rows(rows: list[dict[str, str]]) -> list[dict[str, Any]]:
    grouped = Counter(
        (
            row["schema_class_id"],
            row["selected_tier"],
            row["predicted_movement_direction"],
            row["control_action"],
            row["blocked_reason"],
        )
        for row in rows
    )
    return [
        {
            "evaluation_id": EVALUATION_ID,
            "schema_class_id": schema,
            "selected_tier": tier,
            "predicted_movement_direction": movement,
            "control_action": action,
            "blocked_reason": blocked,
            "event_count": count,
        }
        for (schema, tier, movement, action, blocked), count in sorted(grouped.items())
    ]


def _abc_tier_summary_rows(rows: list[dict[str, str]]) -> list[dict[str, Any]]:
    grouped = Counter((row["schema_class_id"], row["tier_index"]) for row in rows)
    return [
        {
            "evaluation_id": EVALUATION_ID,
            "schema_class_id": schema,
            "tier_index": tier,
            "event_count": count,
        }
        for (schema, tier), count in sorted(grouped.items())
    ]


def _learner_update_rows(rows: list[dict[str, str]]) -> list[dict[str, Any]]:
    grouped: dict[tuple[str, str], list[dict[str, str]]] = defaultdict(list)
    for row in rows:
        grouped[(row["run_id"], row["schema_class_id"])].append(row)
    return [
        {
            "evaluation_id": EVALUATION_ID,
            "run_id": run_id,
            "schema_class_id": schema,
            "update_count": len(items),
            "successful_update_count": sum(_bool(row["success"]) for row in items),
        }
        for (run_id, schema), items in sorted(grouped.items())
    ]


def _health_rows(
    aggregate_rows: list[dict[str, Any]],
    tower_rows: list[dict[str, str]],
    lift_rows: list[dict[str, str]],
    abc_selection_rows: list[dict[str, str]],
) -> list[dict[str, Any]]:
    del tower_rows
    lift_failures = Counter(
        row["run_id"] for row in lift_rows if row.get("success") not in {"True", "true", "1"}
    )
    tier1_selected = Counter(
        row["run_id"] for row in abc_selection_rows if row.get("selected_tier") == "1"
    )
    rows = []
    for row in aggregate_rows:
        classification = "comparison_ready"
        if row["status"] != "success":
            classification = "runtime_failed"
        elif row["hit_status"] != "sustained_hit":
            classification = "non_sustained"
        elif row["schema_class_id"] == SCHEMA1_CLASS_ID and tier1_selected[row["run_id"]] == 0:
            classification = "schema1_no_tier1_use"
        if lift_failures[row["run_id"]] > row["lift_success_count"]:
            classification = "schema1_lift_failure_dominant"
        rows.append(
            {
                "evaluation_id": EVALUATION_ID,
                "run_id": row["run_id"],
                "schema_class_id": row["schema_class_id"],
                "status": row["status"],
                "comparison_health_class": classification,
                "hit_status": row["hit_status"],
                "concrete_step_count": row["concrete_step_count"],
                "lift_success_count": row["lift_success_count"],
                "learner_update_count": row["learner_update_count"],
            }
        )
    return rows


def _run_root(artifact_root: Path, run_id: str) -> Path:
    return (
        artifact_root
        / "runs"
        / "counterpoint_symbolic_v001_second_serious_schema_comparison_v001"
        / "runs"
        / run_id
    )


def _read_csv(path: Path) -> list[dict[str, str]]:
    if not path.exists():
        return []
    return list(csv.DictReader(path.open(encoding="utf-8")))


def _read_json(path: Path) -> dict[str, Any]:
    if not path.exists():
        return {}
    return json.loads(path.read_text(encoding="utf-8"))


def _fieldnames(rows: list[dict[str, Any]]) -> tuple[str, ...]:
    keys: list[str] = []
    for row in rows:
        for key in row:
            if key not in keys:
                keys.append(key)
    return tuple(keys)


def _float(value: object) -> float:
    return float(value or 0.0)


def _bool(value: object) -> bool:
    return str(value) in {"True", "true", "1"}


def _optional_int(value: object) -> int | None:
    if value in (None, ""):
        return None
    return int(float(value))
