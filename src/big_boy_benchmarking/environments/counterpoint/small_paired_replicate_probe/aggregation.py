"""Aggregation for the counterpoint small paired replicate probe."""

from __future__ import annotations

import csv
import json
import statistics
from collections import Counter, defaultdict
from pathlib import Path
from typing import Any

from big_boy_benchmarking.artifacts.writers import write_csv, write_json

from .config import (
    EVALUATION_ID,
    EVALUATION_RUN_FAMILY_ID,
    SCHEMA0_CLASS_ID,
    SCHEMA1_CLASS_ID,
)
from .manifests import readout_source_payload
from .paths import (
    build_small_paired_replicate_probe_paths,
    repo_readout_surface,
    validate_repo_resident_artifact_root,
)
from .threshold_source import ResolvedThreshold

AGGREGATE_FIELDNAMES = (
    "evaluation_id",
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
    "hit_status",
    "episodes_to_sustained_hit",
    "post_hit_window_mean",
    "post_hit_window_min",
    "post_hit_window_success_count",
    "mean_total_reward",
    "concrete_step_count",
    "lift_success_count",
    "lift_failure_count",
    "learner_update_count",
    "structural_limit_classification",
    "artifact_root",
    "failure_reason",
)
PAIR_FIELDNAMES = (
    "candidate_group_id",
    "seed_bundle_id",
    "training_replicate_index",
    "schema0_run_id",
    "schema1_run_id",
    "schema0_hit_status",
    "schema1_hit_status",
    "schema0_episodes_to_hit",
    "schema1_episodes_to_hit",
    "schema1_minus_schema0_episodes_to_hit",
    "schema0_post_hit_window_mean",
    "schema1_post_hit_window_mean",
    "schema1_minus_schema0_post_hit_window_mean",
    "schema0_post_hit_window_min",
    "schema1_post_hit_window_min",
    "schema1_minus_schema0_post_hit_window_min",
    "schema0_post_hit_success_count",
    "schema1_post_hit_success_count",
    "schema1_minus_schema0_post_hit_success_count",
    "pair_status",
    "claim_blocked",
    "interpretation",
)
DELTA_FIELDNAMES = (
    "candidate_group_id",
    "pair_count",
    "unblocked_pair_count",
    "schema1_faster_pair_count",
    "schema1_slower_pair_count",
    "same_episode_pair_count",
    "schema1_margin_win_count",
    "schema1_margin_loss_count",
    "schema1_margin_same_count",
    "blocked_pair_count",
    "median_schema1_minus_schema0_episodes_to_hit",
    "median_schema1_minus_schema0_post_hit_window_mean",
    "median_schema1_minus_schema0_post_hit_window_min",
    "mean_schema1_minus_schema0_post_hit_success_count",
    "claim_status",
    "bounded_claim_text",
)
ARM_FIELDNAMES = (
    "schema_class_id",
    "run_count",
    "sustained_hit_count",
    "transient_hit_count",
    "never_hit_count",
    "artifact_incomplete_count",
    "sustained_hit_rate",
    "median_episodes_to_sustained_hit",
    "mean_episodes_to_sustained_hit",
    "median_post_hit_window_mean",
    "median_post_hit_window_min",
    "mean_post_hit_window_success_count",
)
MARGIN_FIELDNAMES = (
    "candidate_group_id",
    "seed_bundle_id",
    "training_replicate_index",
    "schema_class_id",
    "run_id",
    "post_hit_window_mean",
    "post_hit_window_min",
    "post_hit_window_success_count",
    "threshold_margin_mean",
    "threshold_margin_min",
    "threshold_success_fraction",
    "schema1_minus_schema0_post_hit_window_mean",
    "schema1_minus_schema0_post_hit_window_min",
    "schema1_minus_schema0_post_hit_success_count",
)
HIT_RATE_FIELDNAMES = (
    "schema_class_id",
    "run_count",
    "sustained_hit_count",
    "sustained_hit_rate",
    "schema1_minus_schema0_sustained_hit_rate",
    "blocked_pair_count",
)
SEED_FIELDNAMES = (
    "candidate_group_id",
    "seed_bundle_id",
    "training_replicate_index",
    "schema0_run_id",
    "schema1_run_id",
    "schema0_seed_bundle_path",
    "schema1_seed_bundle_path",
    "pair_status",
)


def aggregate_small_paired_replicate_probe_results(
    artifact_root: Path | str,
    *,
    docs_root: Path | str | None = None,
) -> dict[str, Any]:
    artifact_root = validate_repo_resident_artifact_root(artifact_root)
    paths = build_small_paired_replicate_probe_paths(artifact_root)
    paths.results_dir.mkdir(parents=True, exist_ok=True)
    if not paths.evaluation_run_index_csv.exists():
        raise FileNotFoundError(f"missing evaluation run index: {paths.evaluation_run_index_csv}")

    run_rows = _read_csv(paths.evaluation_run_index_csv)
    budget = _read_json(paths.evaluation_budget_lock)
    threshold_manifest = _read_json(paths.threshold_policy_manifest)
    threshold = ResolvedThreshold(
        threshold_value=float(threshold_manifest["threshold_value"]),
        threshold_source_type=str(threshold_manifest.get("threshold_source_type", "")),
        threshold_source_readout=threshold_manifest.get("threshold_source_readout"),
        threshold_source_field=str(threshold_manifest.get("threshold_source_field", "")),
    )
    aggregate_rows: list[dict[str, Any]] = []
    episode_rows_all: list[dict[str, str]] = []
    first_hit_rows: list[dict[str, str]] = []
    threshold_rows: list[dict[str, str]] = []
    tower_rows: list[dict[str, str]] = []
    lift_rows: list[dict[str, str]] = []
    control_rows: list[dict[str, str]] = []
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
        lifts = _read_csv(run_root / "lift_fiber_events.csv")
        controls = _read_csv(run_root / "control_events.csv")
        learners = _read_csv(run_root / "learner_update_events.csv")
        timing_summary = _read_json(run_root / "timing_summary.json")
        episode_rows_all.extend(episodes)
        first_hit_rows.extend(first_hit)
        threshold_rows.extend(thresholds)
        tower_rows.extend(tower)
        lift_rows.extend(lifts)
        control_rows.extend(controls)
        learner_rows.extend(learners)
        timing_rows.append(
            {
                "run_id": run_row["run_id"],
                "schema_class_id": run_row["schema_class_id"],
                "timing_summary": json.dumps(timing_summary, sort_keys=True),
            }
        )
        aggregate_rows.append(_aggregate_row(run_row, episodes, first_hit, lifts, learners))

    pair_rows = _pair_rows(run_rows, aggregate_rows)
    delta_rows = _delta_distribution_rows(pair_rows)
    arm_rows = _arm_distribution_rows(aggregate_rows)
    margin_rows = _post_hit_margin_rows(pair_rows, aggregate_rows, threshold=threshold)
    hit_rate_rows = _hit_rate_rows(aggregate_rows, pair_rows)
    seed_rows = _seed_bundle_rows(run_rows, pair_rows)
    lift_success_rows = _lift_rows(lift_rows, success=True)
    lift_failure_rows = _lift_rows(lift_rows, success=False)

    result_files = {
        "replicate_pair_summary": paths.results_dir / "replicate_pair_summary.csv",
        "paired_delta_distribution": paths.results_dir / "paired_delta_distribution.csv",
        "schema_arm_distribution": paths.results_dir / "schema_arm_distribution.csv",
        "post_hit_margin_distribution": paths.results_dir / "post_hit_margin_distribution.csv",
        "sustained_hit_rate_summary": paths.results_dir / "sustained_hit_rate_summary.csv",
        "seed_bundle_summary": paths.results_dir / "seed_bundle_summary.csv",
        "lift_success_by_tier": paths.results_dir / "lift_success_by_tier.csv",
        "lift_failure_by_tier": paths.results_dir / "lift_failure_by_tier.csv",
        "tower_shape_summary": paths.results_dir / "tower_shape_summary.csv",
        "timing_summary": paths.results_dir / "timing_summary.csv",
        "training_episode_summary": paths.results_dir / "training_episode_summary.csv",
        "threshold_window_summary": paths.results_dir / "threshold_window_summary.csv",
        "first_sustained_hit_summary": paths.results_dir / "first_sustained_hit_summary.csv",
        "controller_action_summary": paths.results_dir / "controller_action_summary.csv",
        "learner_update_summary": paths.results_dir / "learner_update_summary.csv",
    }
    write_csv(result_files["replicate_pair_summary"], pair_rows, PAIR_FIELDNAMES)
    write_csv(result_files["paired_delta_distribution"], delta_rows, DELTA_FIELDNAMES)
    write_csv(result_files["schema_arm_distribution"], arm_rows, ARM_FIELDNAMES)
    write_csv(result_files["post_hit_margin_distribution"], margin_rows, MARGIN_FIELDNAMES)
    write_csv(result_files["sustained_hit_rate_summary"], hit_rate_rows, HIT_RATE_FIELDNAMES)
    write_csv(result_files["seed_bundle_summary"], seed_rows, SEED_FIELDNAMES)
    write_csv(result_files["lift_success_by_tier"], lift_success_rows, _lift_fieldnames())
    write_csv(result_files["lift_failure_by_tier"], lift_failure_rows, _lift_fieldnames())
    write_csv(result_files["tower_shape_summary"], tower_rows, _fieldnames(tower_rows))
    write_csv(result_files["timing_summary"], timing_rows, _fieldnames(timing_rows))
    write_csv(
        result_files["training_episode_summary"], episode_rows_all, _fieldnames(episode_rows_all)
    )
    write_csv(result_files["threshold_window_summary"], threshold_rows, _fieldnames(threshold_rows))
    write_csv(
        result_files["first_sustained_hit_summary"],
        first_hit_rows,
        _fieldnames(first_hit_rows),
    )
    write_csv(
        result_files["controller_action_summary"],
        _controller_action_rows(control_rows),
        _fieldnames(_controller_action_rows(control_rows)),
    )
    write_csv(
        result_files["learner_update_summary"],
        _learner_update_rows(learner_rows),
        _fieldnames(_learner_update_rows(learner_rows)),
    )
    write_csv(paths.evaluation_aggregate_table_csv, aggregate_rows, AGGREGATE_FIELDNAMES)

    status = "complete" if run_rows and complete_run_count == len(run_rows) else "incomplete"
    summary = {
        "evaluation_id": EVALUATION_ID,
        "status": status,
        "run_count": len(run_rows),
        "complete_run_count": complete_run_count,
        "pair_count": len(pair_rows),
        "unblocked_pair_count": sum(_false(row["claim_blocked"]) for row in pair_rows),
        "schema1_margin_win_count": sum(
            row["schema1_minus_schema0_post_hit_window_mean"] not in (None, "")
            and float(row["schema1_minus_schema0_post_hit_window_mean"]) > 0
            for row in pair_rows
            if _false(row["claim_blocked"])
        ),
        "lift_failure_count": sum(int(row["event_count"]) for row in lift_failure_rows),
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
        threshold=threshold,
    )
    return summary


def _write_readout_source(
    *,
    artifact_root: Path,
    docs_root: Path,
    paths,
    result_files: dict[str, Path],
    budget: dict[str, Any],
    threshold: ResolvedThreshold,
) -> None:
    source_files = {
        "aggregate_table": paths.evaluation_aggregate_table_csv,
        "run_index": paths.evaluation_run_index_csv,
        "aggregate_summary": paths.evaluation_aggregate_summary,
        "evaluation_manifest": paths.evaluation_manifest,
        "evaluation_arm_manifest": paths.evaluation_arm_manifest,
        "evaluation_budget_lock": paths.evaluation_budget_lock,
        "replicate_probe_policy_manifest": paths.replicate_probe_policy_manifest,
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
        threshold=threshold,
    )
    write_json(docs_root / "readout_source.json", payload, create_parents=True)
    write_json(paths.readout_source, payload, create_parents=True)


def _aggregate_row(
    run_row: dict[str, str],
    episodes: list[dict[str, str]],
    first_hit_rows: list[dict[str, str]],
    lifts: list[dict[str, str]],
    learners: list[dict[str, str]],
) -> dict[str, Any]:
    first_hit = first_hit_rows[0] if first_hit_rows else {}
    rewards = [_float(row["total_reward"]) for row in episodes]
    hit_status = first_hit.get("hit_status", "artifact_incomplete")
    structural = "ok" if hit_status != "artifact_incomplete" else "artifact_incomplete"
    lift_failure_count = sum(not _bool(row["success"]) for row in lifts)
    if lift_failure_count:
        structural = "lift_failures_present"
    return {
        "evaluation_id": EVALUATION_ID,
        "run_id": run_row["run_id"],
        "run_mode": run_row["run_mode"],
        "candidate_group_id": run_row["candidate_group_id"],
        "schema_class_id": run_row["schema_class_id"],
        "candidate_id": run_row["candidate_id"],
        "instance_id": run_row["instance_id"],
        "arm_id": run_row["arm_id"],
        "schema_seed": int(run_row["schema_seed"]),
        "seed_bundle_id": run_row["seed_bundle_id"],
        "training_replicate_index": int(run_row["training_replicate_index"]),
        "status": run_row["status"],
        "hit_status": hit_status,
        "episodes_to_sustained_hit": _optional_int(first_hit.get("episodes_to_sustained_hit")),
        "post_hit_window_mean": _optional_float(first_hit.get("post_hit_window_mean")),
        "post_hit_window_min": _optional_float(first_hit.get("post_hit_window_min")),
        "post_hit_window_success_count": _optional_int(
            first_hit.get("post_hit_window_success_count")
        ),
        "mean_total_reward": statistics.mean(rewards) if rewards else None,
        "concrete_step_count": sum(int(row["concrete_step_count"]) for row in episodes),
        "lift_success_count": sum(_bool(row["success"]) for row in lifts),
        "lift_failure_count": lift_failure_count,
        "learner_update_count": sum(_bool(row["success"]) for row in learners),
        "structural_limit_classification": structural,
        "artifact_root": run_row["artifact_root"],
        "failure_reason": run_row.get("failure_reason") or None,
    }


def _failed_aggregate_row(run_row: dict[str, str]) -> dict[str, Any]:
    return {
        "evaluation_id": EVALUATION_ID,
        "run_id": run_row.get("run_id", ""),
        "run_mode": run_row["run_mode"],
        "candidate_group_id": run_row["candidate_group_id"],
        "schema_class_id": run_row["schema_class_id"],
        "candidate_id": run_row["candidate_id"],
        "instance_id": run_row["instance_id"],
        "arm_id": run_row["arm_id"],
        "schema_seed": int(run_row["schema_seed"]),
        "seed_bundle_id": run_row["seed_bundle_id"],
        "training_replicate_index": int(run_row["training_replicate_index"]),
        "status": run_row["status"],
        "hit_status": "runtime_failed",
        "episodes_to_sustained_hit": None,
        "post_hit_window_mean": None,
        "post_hit_window_min": None,
        "post_hit_window_success_count": None,
        "mean_total_reward": None,
        "concrete_step_count": 0,
        "lift_success_count": 0,
        "lift_failure_count": 0,
        "learner_update_count": 0,
        "structural_limit_classification": "runtime_failed",
        "artifact_root": run_row["artifact_root"],
        "failure_reason": run_row.get("failure_reason") or None,
    }


def _pair_rows(
    run_rows: list[dict[str, str]],
    aggregate_rows: list[dict[str, Any]],
) -> list[dict[str, Any]]:
    grouped: dict[tuple[str, str, str], dict[str, dict[str, Any]]] = defaultdict(dict)
    for row in aggregate_rows:
        key = (
            row["candidate_group_id"],
            row["seed_bundle_id"],
            str(row["training_replicate_index"]),
        )
        grouped[key][row["schema_class_id"]] = row
    result = []
    for (candidate_group_id, seed_bundle_id, replicate), rows in sorted(grouped.items()):
        schema0 = rows.get(SCHEMA0_CLASS_ID)
        schema1 = rows.get(SCHEMA1_CLASS_ID)
        result.append(
            _single_pair_row(
                candidate_group_id=candidate_group_id,
                seed_bundle_id=seed_bundle_id,
                replicate=int(replicate),
                schema0=schema0,
                schema1=schema1,
            )
        )
    return result


def _single_pair_row(
    *,
    candidate_group_id: str,
    seed_bundle_id: str,
    replicate: int,
    schema0: dict[str, Any] | None,
    schema1: dict[str, Any] | None,
) -> dict[str, Any]:
    delta_episode = _delta(
        None if schema0 is None else schema0["episodes_to_sustained_hit"],
        None if schema1 is None else schema1["episodes_to_sustained_hit"],
        integer=True,
    )
    delta_mean = _delta(
        None if schema0 is None else schema0["post_hit_window_mean"],
        None if schema1 is None else schema1["post_hit_window_mean"],
    )
    delta_min = _delta(
        None if schema0 is None else schema0["post_hit_window_min"],
        None if schema1 is None else schema1["post_hit_window_min"],
    )
    delta_success = _delta(
        None if schema0 is None else schema0["post_hit_window_success_count"],
        None if schema1 is None else schema1["post_hit_window_success_count"],
        integer=True,
    )
    pair_status, claim_blocked, interpretation = _pair_status(
        schema0, schema1, delta_episode, delta_mean
    )
    return {
        "candidate_group_id": candidate_group_id,
        "seed_bundle_id": seed_bundle_id,
        "training_replicate_index": replicate,
        "schema0_run_id": "" if schema0 is None else schema0["run_id"],
        "schema1_run_id": "" if schema1 is None else schema1["run_id"],
        "schema0_hit_status": "missing" if schema0 is None else schema0["hit_status"],
        "schema1_hit_status": "missing" if schema1 is None else schema1["hit_status"],
        "schema0_episodes_to_hit": None
        if schema0 is None
        else schema0["episodes_to_sustained_hit"],
        "schema1_episodes_to_hit": None
        if schema1 is None
        else schema1["episodes_to_sustained_hit"],
        "schema1_minus_schema0_episodes_to_hit": delta_episode,
        "schema0_post_hit_window_mean": None
        if schema0 is None
        else schema0["post_hit_window_mean"],
        "schema1_post_hit_window_mean": None
        if schema1 is None
        else schema1["post_hit_window_mean"],
        "schema1_minus_schema0_post_hit_window_mean": delta_mean,
        "schema0_post_hit_window_min": None if schema0 is None else schema0["post_hit_window_min"],
        "schema1_post_hit_window_min": None if schema1 is None else schema1["post_hit_window_min"],
        "schema1_minus_schema0_post_hit_window_min": delta_min,
        "schema0_post_hit_success_count": None
        if schema0 is None
        else schema0["post_hit_window_success_count"],
        "schema1_post_hit_success_count": None
        if schema1 is None
        else schema1["post_hit_window_success_count"],
        "schema1_minus_schema0_post_hit_success_count": delta_success,
        "pair_status": pair_status,
        "claim_blocked": claim_blocked,
        "interpretation": interpretation,
    }


def _pair_status(
    schema0: dict[str, Any] | None,
    schema1: dict[str, Any] | None,
    delta_episode: int | None,
    delta_mean: float | None,
) -> tuple[str, bool, str]:
    if schema0 is None or schema1 is None:
        return "artifact_incomplete", True, "One schema arm is missing from this pair."
    if schema0["status"] != "success" or schema1["status"] != "success":
        return "runtime_failed", True, "At least one schema arm failed at runtime."
    if schema0["hit_status"] != "sustained_hit" or schema1["hit_status"] != "sustained_hit":
        return "blocked_or_non_sustained", True, "At least one schema arm lacked a sustained hit."
    if delta_episode is not None and delta_episode < 0:
        return "schema1_faster", False, "Schema 1 reached the sustained threshold sooner."
    if delta_episode is not None and delta_episode > 0:
        return "schema1_slower", False, "Schema 1 reached the sustained threshold later."
    if delta_mean is not None and delta_mean > 0:
        return (
            "schema1_margin_higher",
            False,
            "Both hit at the same speed; Schema 1 had higher post-hit mean reward.",
        )
    if delta_mean is not None and delta_mean < 0:
        return (
            "schema1_margin_lower",
            False,
            "Both hit at the same speed; Schema 1 had lower post-hit mean reward.",
        )
    return "same_margin", False, "Both hit at the same speed with no post-hit mean margin."


def _delta(left: Any, right: Any, *, integer: bool = False) -> int | float | None:
    if left in (None, "") or right in (None, ""):
        return None
    value = float(right) - float(left)
    return int(value) if integer else value


def _delta_distribution_rows(pair_rows: list[dict[str, Any]]) -> list[dict[str, Any]]:
    grouped: dict[str, list[dict[str, Any]]] = defaultdict(list)
    for row in pair_rows:
        grouped[row["candidate_group_id"]].append(row)
    result = []
    for candidate_group_id, rows in sorted(grouped.items()):
        unblocked = [row for row in rows if _false(row["claim_blocked"])]
        episode_deltas = [
            int(row["schema1_minus_schema0_episodes_to_hit"])
            for row in unblocked
            if row["schema1_minus_schema0_episodes_to_hit"] not in (None, "")
        ]
        mean_deltas = [
            float(row["schema1_minus_schema0_post_hit_window_mean"])
            for row in unblocked
            if row["schema1_minus_schema0_post_hit_window_mean"] not in (None, "")
        ]
        min_deltas = [
            float(row["schema1_minus_schema0_post_hit_window_min"])
            for row in unblocked
            if row["schema1_minus_schema0_post_hit_window_min"] not in (None, "")
        ]
        success_deltas = [
            int(row["schema1_minus_schema0_post_hit_success_count"])
            for row in unblocked
            if row["schema1_minus_schema0_post_hit_success_count"] not in (None, "")
        ]
        margin_wins = sum(delta > 0 for delta in mean_deltas)
        margin_losses = sum(delta < 0 for delta in mean_deltas)
        margin_same = sum(delta == 0 for delta in mean_deltas)
        status, text = _claim_status(
            pair_count=len(rows),
            unblocked_count=len(unblocked),
            margin_wins=margin_wins,
            margin_losses=margin_losses,
        )
        result.append(
            {
                "candidate_group_id": candidate_group_id,
                "pair_count": len(rows),
                "unblocked_pair_count": len(unblocked),
                "schema1_faster_pair_count": sum(
                    row["pair_status"] == "schema1_faster" for row in unblocked
                ),
                "schema1_slower_pair_count": sum(
                    row["pair_status"] == "schema1_slower" for row in unblocked
                ),
                "same_episode_pair_count": sum(
                    row["schema1_minus_schema0_episodes_to_hit"] == 0 for row in unblocked
                ),
                "schema1_margin_win_count": margin_wins,
                "schema1_margin_loss_count": margin_losses,
                "schema1_margin_same_count": margin_same,
                "blocked_pair_count": len(rows) - len(unblocked),
                "median_schema1_minus_schema0_episodes_to_hit": (
                    statistics.median(episode_deltas) if episode_deltas else None
                ),
                "median_schema1_minus_schema0_post_hit_window_mean": (
                    statistics.median(mean_deltas) if mean_deltas else None
                ),
                "median_schema1_minus_schema0_post_hit_window_min": (
                    statistics.median(min_deltas) if min_deltas else None
                ),
                "mean_schema1_minus_schema0_post_hit_success_count": (
                    statistics.mean(success_deltas) if success_deltas else None
                ),
                "claim_status": status,
                "bounded_claim_text": text,
            }
        )
    return result


def _claim_status(
    *,
    pair_count: int,
    unblocked_count: int,
    margin_wins: int,
    margin_losses: int,
) -> tuple[str, str]:
    if pair_count == 0:
        return "no_pairs", "No paired rows were available."
    if unblocked_count == 0:
        return "claim_blocked", "All pairs are blocked or non-sustained."
    if margin_wins > margin_losses:
        return "weak_positive_margin_pattern", "Schema 1 has more post-hit margin wins than losses."
    if margin_losses > margin_wins:
        return "weak_negative_margin_pattern", "Schema 1 has more post-hit margin losses than wins."
    return "mixed_or_inconclusive", "The paired post-hit margin pattern is mixed or tied."


def _arm_distribution_rows(rows: list[dict[str, Any]]) -> list[dict[str, Any]]:
    grouped: dict[str, list[dict[str, Any]]] = defaultdict(list)
    for row in rows:
        grouped[row["schema_class_id"]].append(row)
    result = []
    for schema_class_id, items in sorted(grouped.items()):
        sustained = [row for row in items if row["hit_status"] == "sustained_hit"]
        episodes = [
            int(row["episodes_to_sustained_hit"])
            for row in sustained
            if row["episodes_to_sustained_hit"] not in (None, "")
        ]
        post_means = [
            float(row["post_hit_window_mean"])
            for row in sustained
            if row["post_hit_window_mean"] not in (None, "")
        ]
        post_mins = [
            float(row["post_hit_window_min"])
            for row in sustained
            if row["post_hit_window_min"] not in (None, "")
        ]
        post_counts = [
            int(row["post_hit_window_success_count"])
            for row in sustained
            if row["post_hit_window_success_count"] not in (None, "")
        ]
        result.append(
            {
                "schema_class_id": schema_class_id,
                "run_count": len(items),
                "sustained_hit_count": len(sustained),
                "transient_hit_count": sum(
                    row["hit_status"] == "transient_hit_only" for row in items
                ),
                "never_hit_count": sum(row["hit_status"] == "never_hit" for row in items),
                "artifact_incomplete_count": sum(
                    row["hit_status"] in {"artifact_incomplete", "runtime_failed"} for row in items
                ),
                "sustained_hit_rate": len(sustained) / len(items) if items else None,
                "median_episodes_to_sustained_hit": statistics.median(episodes)
                if episodes
                else None,
                "mean_episodes_to_sustained_hit": statistics.mean(episodes) if episodes else None,
                "median_post_hit_window_mean": statistics.median(post_means)
                if post_means
                else None,
                "median_post_hit_window_min": statistics.median(post_mins) if post_mins else None,
                "mean_post_hit_window_success_count": statistics.mean(post_counts)
                if post_counts
                else None,
            }
        )
    return result


def _post_hit_margin_rows(
    pair_rows: list[dict[str, Any]],
    aggregate_rows: list[dict[str, Any]],
    *,
    threshold: ResolvedThreshold,
) -> list[dict[str, Any]]:
    by_run_id = {row["run_id"]: row for row in aggregate_rows}
    result = []
    for pair in pair_rows:
        for schema_class_id, run_key in (
            (SCHEMA0_CLASS_ID, "schema0_run_id"),
            (SCHEMA1_CLASS_ID, "schema1_run_id"),
        ):
            run = by_run_id.get(pair[run_key], {})
            mean_value = run.get("post_hit_window_mean")
            min_value = run.get("post_hit_window_min")
            success_count = run.get("post_hit_window_success_count")
            result.append(
                {
                    "candidate_group_id": pair["candidate_group_id"],
                    "seed_bundle_id": pair["seed_bundle_id"],
                    "training_replicate_index": pair["training_replicate_index"],
                    "schema_class_id": schema_class_id,
                    "run_id": pair[run_key],
                    "post_hit_window_mean": mean_value,
                    "post_hit_window_min": min_value,
                    "post_hit_window_success_count": success_count,
                    "threshold_margin_mean": _margin(mean_value, threshold.threshold_value),
                    "threshold_margin_min": _margin(min_value, threshold.threshold_value),
                    "threshold_success_fraction": (
                        None if success_count in (None, "") else int(success_count) / 5
                    ),
                    "schema1_minus_schema0_post_hit_window_mean": pair[
                        "schema1_minus_schema0_post_hit_window_mean"
                    ],
                    "schema1_minus_schema0_post_hit_window_min": pair[
                        "schema1_minus_schema0_post_hit_window_min"
                    ],
                    "schema1_minus_schema0_post_hit_success_count": pair[
                        "schema1_minus_schema0_post_hit_success_count"
                    ],
                }
            )
    return result


def _hit_rate_rows(
    aggregate_rows: list[dict[str, Any]],
    pair_rows: list[dict[str, Any]],
) -> list[dict[str, Any]]:
    arm_rows = _arm_distribution_rows(aggregate_rows)
    rate_by_schema = {row["schema_class_id"]: row["sustained_hit_rate"] for row in arm_rows}
    delta = None
    if (
        rate_by_schema.get(SCHEMA0_CLASS_ID) is not None
        and rate_by_schema.get(SCHEMA1_CLASS_ID) is not None
    ):
        delta = float(rate_by_schema[SCHEMA1_CLASS_ID]) - float(rate_by_schema[SCHEMA0_CLASS_ID])
    blocked_count = sum(_bool(row["claim_blocked"]) for row in pair_rows)
    return [
        {
            "schema_class_id": row["schema_class_id"],
            "run_count": row["run_count"],
            "sustained_hit_count": row["sustained_hit_count"],
            "sustained_hit_rate": row["sustained_hit_rate"],
            "schema1_minus_schema0_sustained_hit_rate": delta,
            "blocked_pair_count": blocked_count,
        }
        for row in arm_rows
    ]


def _seed_bundle_rows(
    run_rows: list[dict[str, str]],
    pair_rows: list[dict[str, Any]],
) -> list[dict[str, Any]]:
    run_by_id = {row["run_id"]: row for row in run_rows}
    rows = []
    for pair in pair_rows:
        schema0_run = run_by_id.get(pair["schema0_run_id"], {})
        schema1_run = run_by_id.get(pair["schema1_run_id"], {})
        rows.append(
            {
                "candidate_group_id": pair["candidate_group_id"],
                "seed_bundle_id": pair["seed_bundle_id"],
                "training_replicate_index": pair["training_replicate_index"],
                "schema0_run_id": pair["schema0_run_id"],
                "schema1_run_id": pair["schema1_run_id"],
                "schema0_seed_bundle_path": _seed_bundle_path(schema0_run),
                "schema1_seed_bundle_path": _seed_bundle_path(schema1_run),
                "pair_status": pair["pair_status"],
            }
        )
    return rows


def _seed_bundle_path(run_row: dict[str, str]) -> str:
    run_id = run_row.get("run_id")
    artifact_root = run_row.get("artifact_root")
    if not run_id or not artifact_root:
        return ""
    return str(_run_root(Path(artifact_root), run_id) / "seed_bundle.json")


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


def _learner_update_rows(rows: list[dict[str, str]]) -> list[dict[str, Any]]:
    grouped: dict[str, list[dict[str, str]]] = defaultdict(list)
    for row in rows:
        grouped[row["schema_class_id"]].append(row)
    return [
        {
            "evaluation_id": EVALUATION_ID,
            "schema_class_id": schema,
            "event_count": len(items),
            "successful_update_count": sum(_bool(item["success"]) for item in items),
        }
        for schema, items in sorted(grouped.items())
    ]


def _lift_fieldnames() -> tuple[str, ...]:
    return ("evaluation_id", "schema_class_id", "active_tier", "failure_reason", "event_count")


def _margin(value: Any, threshold: float) -> float | None:
    if value in (None, ""):
        return None
    return float(value) - threshold


def _fieldnames(rows: list[dict[str, Any]]) -> tuple[str, ...]:
    seen: list[str] = []
    for row in rows:
        for key in row:
            if key not in seen:
                seen.append(key)
    return tuple(seen)


def _read_csv(path: Path) -> list[dict[str, str]]:
    if not path.exists():
        return []
    return list(csv.DictReader(path.open(encoding="utf-8")))


def _read_json(path: Path) -> dict[str, Any]:
    if not path.exists():
        return {}
    return json.loads(path.read_text(encoding="utf-8"))


def _run_root(artifact_root: Path, run_id: str) -> Path:
    return artifact_root / "runs" / EVALUATION_RUN_FAMILY_ID / "runs" / run_id


def _optional_float(value: Any) -> float | None:
    if value in (None, ""):
        return None
    return float(value)


def _optional_int(value: Any) -> int | None:
    if value in (None, ""):
        return None
    return int(float(value))


def _float(value: Any) -> float:
    return float(value)


def _bool(value: Any) -> bool:
    if isinstance(value, bool):
        return value
    return str(value).lower() in {"true", "1", "yes"}


def _false(value: Any) -> bool:
    return not _bool(value)
