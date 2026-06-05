"""Aggregation for the counterpoint threshold-frontier probe."""

from __future__ import annotations

import csv
import json
import statistics
from collections import defaultdict
from pathlib import Path
from typing import Any

from big_boy_benchmarking.artifacts.writers import write_csv, write_json
from big_boy_benchmarking.environments.counterpoint.second_serious_comparison.paths import (
    build_second_serious_comparison_paths,
)

from .config import EVALUATION_ID, RUN_MODE_ID, SCHEMA0_CLASS_ID, SCHEMA1_CLASS_ID
from .manifests import readout_source_payload
from .paths import (
    build_threshold_frontier_probe_paths,
    repo_readout_surface,
    validate_repo_resident_artifact_root,
)

THRESHOLD_ARM_FIELDNAMES = (
    "threshold_value",
    "threshold_label",
    "schema_class_id",
    "run_count",
    "sustained_hit_count",
    "transient_hit_count",
    "never_hit_count",
    "artifact_incomplete_count",
    "sustained_hit_rate",
    "median_episodes_to_sustained_hit",
    "mean_episodes_to_sustained_hit",
    "post_hit_window_mean",
    "post_hit_window_min",
    "post_hit_window_success_count",
    "threshold_margin_mean",
    "threshold_margin_min",
    "threshold_success_fraction",
    "passes_frontier_threshold",
)
THRESHOLD_PAIR_FIELDNAMES = (
    "threshold_value",
    "threshold_label",
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
POST_HIT_MARGIN_FIELDNAMES = (
    "threshold_value",
    "threshold_label",
    "schema_class_id",
    "post_hit_window_mean",
    "post_hit_window_min",
    "post_hit_window_success_count",
    "threshold_margin_mean",
    "threshold_margin_min",
    "threshold_success_fraction",
)
FIRST_FAILURE_FIELDNAMES = (
    "schema_class_id",
    "first_failure_threshold",
    "highest_passing_threshold",
    "frontier_classification",
)
FRONTIER_FIELDNAMES = (
    "candidate_group_id",
    "threshold_count",
    "highest_shared_passing_threshold",
    "highest_schema0_passing_threshold",
    "highest_schema1_passing_threshold",
    "schema1_only_passing_thresholds",
    "schema0_only_passing_thresholds",
    "schema1_frontier_minus_schema0_frontier",
    "schema1_margin_win_count",
    "schema1_margin_loss_count",
    "schema1_margin_same_count",
    "blocked_threshold_count",
    "lift_failure_threshold_count",
    "recommended_replicate_probe_threshold",
    "claim_status",
    "bounded_claim_text",
)
AGGREGATE_FIELDNAMES = (
    "evaluation_id",
    "run_mode",
    "status",
    "candidate_group_id",
    "threshold_count",
    "run_count",
    "pair_count",
    "unblocked_threshold_count",
    "highest_shared_passing_threshold",
    "highest_schema0_passing_threshold",
    "highest_schema1_passing_threshold",
    "recommended_replicate_probe_threshold",
    "claim_status",
    "bounded_claim_text",
    "artifact_root",
)


def aggregate_threshold_frontier_probe_results(
    artifact_root: Path | str,
    *,
    docs_root: Path | str | None = None,
) -> dict[str, Any]:
    artifact_root = validate_repo_resident_artifact_root(artifact_root)
    paths = build_threshold_frontier_probe_paths(artifact_root)
    paths.results_dir.mkdir(parents=True, exist_ok=True)
    if not paths.threshold_run_manifest.exists():
        raise FileNotFoundError(f"missing threshold run manifest: {paths.threshold_run_manifest}")

    budget = _read_json(paths.evaluation_budget_lock)
    threshold_manifest = _read_json(paths.threshold_run_manifest)
    threshold_runs = list(threshold_manifest.get("threshold_runs", ()))
    top_run_rows = _read_csv(paths.evaluation_run_index_csv)
    threshold_arm_rows: list[dict[str, Any]] = []
    threshold_pair_rows: list[dict[str, Any]] = []
    post_hit_margin_rows: list[dict[str, Any]] = []
    tower_rows: list[dict[str, Any]] = []
    lift_success_rows: list[dict[str, Any]] = []
    lift_failure_rows: list[dict[str, Any]] = []
    timing_rows: list[dict[str, Any]] = []

    for threshold_run in threshold_runs:
        value = float(threshold_run["threshold_value"])
        label = str(threshold_run["threshold_label"])
        subroot = Path(str(threshold_run["artifact_root"]))
        sub_paths = build_second_serious_comparison_paths(subroot)
        aggregate_rows = _read_csv(sub_paths.evaluation_aggregate_table_csv)
        run_rows = _read_csv(sub_paths.evaluation_run_index_csv)
        first_hit_rows = _read_csv(sub_paths.results_dir / "first_sustained_hit_summary.csv")
        pair_rows = _threshold_pair_rows(
            threshold_value=value,
            threshold_label=label,
            run_rows=run_rows,
            first_hit_rows=first_hit_rows,
        )
        threshold_pair_rows.extend(pair_rows)
        threshold_arm_rows.extend(
            _threshold_arm_rows(
                threshold_value=value,
                threshold_label=label,
                aggregate_rows=aggregate_rows,
                first_hit_rows=first_hit_rows,
            )
        )
        post_hit_margin_rows.extend(
            _post_hit_margin_rows(
                threshold_value=value,
                threshold_label=label,
                first_hit_rows=first_hit_rows,
            )
        )
        tower_rows.extend(
            _promote_rows(
                sub_paths.results_dir / "tower_shape_summary.csv",
                threshold_value=value,
                threshold_label=label,
            )
        )
        lift_success_rows.extend(
            _promote_rows(
                sub_paths.results_dir / "lift_success_by_tier.csv",
                threshold_value=value,
                threshold_label=label,
            )
        )
        lift_failure_rows.extend(
            _promote_rows(
                sub_paths.results_dir / "lift_failure_by_tier.csv",
                threshold_value=value,
                threshold_label=label,
            )
        )
        timing_rows.extend(
            _promote_rows(
                sub_paths.results_dir / "timing_summary.csv",
                threshold_value=value,
                threshold_label=label,
            )
        )

    first_failure_rows = _first_failure_rows(threshold_arm_rows)
    frontier_rows = _frontier_rows(
        threshold_arm_rows=threshold_arm_rows,
        threshold_pair_rows=threshold_pair_rows,
        lift_failure_rows=lift_failure_rows,
    )
    frontier = frontier_rows[0] if frontier_rows else {}
    result_files = {
        "threshold_arm_summary": paths.results_dir / "threshold_arm_summary.csv",
        "threshold_pair_summary": paths.results_dir / "threshold_pair_summary.csv",
        "post_hit_margin_summary": paths.results_dir / "post_hit_margin_summary.csv",
        "first_failure_frontier_summary": (
            paths.results_dir / "first_failure_frontier_summary.csv"
        ),
        "frontier_summary": paths.results_dir / "frontier_summary.csv",
        "tower_shape_summary": paths.results_dir / "tower_shape_summary.csv",
        "lift_success_by_tier": paths.results_dir / "lift_success_by_tier.csv",
        "lift_failure_by_tier": paths.results_dir / "lift_failure_by_tier.csv",
        "timing_summary": paths.results_dir / "timing_summary.csv",
    }
    write_csv(result_files["threshold_arm_summary"], threshold_arm_rows, THRESHOLD_ARM_FIELDNAMES)
    write_csv(
        result_files["threshold_pair_summary"],
        threshold_pair_rows,
        THRESHOLD_PAIR_FIELDNAMES,
    )
    write_csv(
        result_files["post_hit_margin_summary"],
        post_hit_margin_rows,
        POST_HIT_MARGIN_FIELDNAMES,
    )
    write_csv(
        result_files["first_failure_frontier_summary"],
        first_failure_rows,
        FIRST_FAILURE_FIELDNAMES,
    )
    write_csv(result_files["frontier_summary"], frontier_rows, FRONTIER_FIELDNAMES)
    write_csv(result_files["tower_shape_summary"], tower_rows, _fieldnames(tower_rows))
    write_csv(
        result_files["lift_success_by_tier"],
        lift_success_rows,
        _fieldnames(lift_success_rows),
    )
    write_csv(
        result_files["lift_failure_by_tier"],
        lift_failure_rows,
        _fieldnames(lift_failure_rows),
    )
    write_csv(result_files["timing_summary"], timing_rows, _fieldnames(timing_rows))

    status = (
        "complete"
        if threshold_runs and all(row.get("status") == "complete" for row in threshold_runs)
        else "incomplete"
    )
    aggregate_rows = [
        {
            "evaluation_id": EVALUATION_ID,
            "run_mode": RUN_MODE_ID,
            "status": status,
            "candidate_group_id": frontier.get("candidate_group_id", ""),
            "threshold_count": len(threshold_runs),
            "run_count": len(top_run_rows),
            "pair_count": len(threshold_pair_rows),
            "unblocked_threshold_count": _unblocked_threshold_count(threshold_pair_rows),
            "highest_shared_passing_threshold": frontier.get("highest_shared_passing_threshold"),
            "highest_schema0_passing_threshold": frontier.get("highest_schema0_passing_threshold"),
            "highest_schema1_passing_threshold": frontier.get("highest_schema1_passing_threshold"),
            "recommended_replicate_probe_threshold": frontier.get(
                "recommended_replicate_probe_threshold"
            ),
            "claim_status": frontier.get("claim_status", "frontier_inconclusive"),
            "bounded_claim_text": frontier.get("bounded_claim_text", ""),
            "artifact_root": str(artifact_root),
        }
    ]
    write_csv(paths.evaluation_aggregate_table_csv, aggregate_rows, AGGREGATE_FIELDNAMES)
    summary = {
        "evaluation_id": EVALUATION_ID,
        "status": status,
        "threshold_count": len(threshold_runs),
        "run_count": len(top_run_rows),
        "pair_count": len(threshold_pair_rows),
        "unblocked_threshold_count": _unblocked_threshold_count(threshold_pair_rows),
        "lift_failure_threshold_count": frontier.get("lift_failure_threshold_count", 0),
        "recommended_replicate_probe_threshold": frontier.get(
            "recommended_replicate_probe_threshold"
        ),
        "claim_status": frontier.get("claim_status", "frontier_inconclusive"),
        "evaluation_aggregate_table": str(paths.evaluation_aggregate_table_csv),
        "result_files": {key: str(value) for key, value in result_files.items()},
    }
    write_json(paths.evaluation_aggregate_summary, summary, create_parents=True)
    docs_root = Path(docs_root) if docs_root is not None else repo_readout_surface()
    _write_readout_source(
        artifact_root=artifact_root,
        docs_root=docs_root,
        paths=paths,
        result_files=result_files,
        budget=budget,
        recommended_replicate_probe_threshold=_float_or_none(
            frontier.get("recommended_replicate_probe_threshold")
        ),
    )
    return summary


def _write_readout_source(
    *,
    artifact_root: Path,
    docs_root: Path,
    paths,
    result_files: dict[str, Path],
    budget: dict[str, Any],
    recommended_replicate_probe_threshold: float | None,
) -> None:
    source_files = {
        "aggregate_table": paths.evaluation_aggregate_table_csv,
        "run_index": paths.evaluation_run_index_csv,
        "aggregate_summary": paths.evaluation_aggregate_summary,
        "evaluation_manifest": paths.evaluation_manifest,
        "evaluation_arm_manifest": paths.evaluation_arm_manifest,
        "evaluation_budget_lock": paths.evaluation_budget_lock,
        "threshold_frontier_policy_manifest": paths.threshold_frontier_policy_manifest,
        "threshold_run_manifest": paths.threshold_run_manifest,
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
        recommended_replicate_probe_threshold=recommended_replicate_probe_threshold,
    )
    write_json(docs_root / "readout_source.json", payload, create_parents=True)
    write_json(paths.readout_source, payload, create_parents=True)


def _threshold_arm_rows(
    *,
    threshold_value: float,
    threshold_label: str,
    aggregate_rows: list[dict[str, str]],
    first_hit_rows: list[dict[str, str]],
) -> list[dict[str, Any]]:
    rows = []
    first_by_schema: dict[str, list[dict[str, str]]] = defaultdict(list)
    aggregate_by_schema: dict[str, list[dict[str, str]]] = defaultdict(list)
    for row in first_hit_rows:
        first_by_schema[row["schema_class_id"]].append(row)
    for row in aggregate_rows:
        aggregate_by_schema[row["schema_class_id"]].append(row)
    for schema_class_id in (SCHEMA0_CLASS_ID, SCHEMA1_CLASS_ID):
        hits = first_by_schema.get(schema_class_id, [])
        aggs = aggregate_by_schema.get(schema_class_id, [])
        statuses = [row.get("hit_status", "artifact_incomplete") for row in hits]
        sustained = statuses.count("sustained_hit")
        run_count = len(aggs) or len(hits)
        episodes = [_float(row.get("episodes_to_sustained_hit")) for row in hits]
        episodes = [value for value in episodes if value is not None]
        means = [_float(row.get("post_hit_window_mean")) for row in hits]
        means = [value for value in means if value is not None]
        mins = [_float(row.get("post_hit_window_min")) for row in hits]
        mins = [value for value in mins if value is not None]
        success_counts = [_float(row.get("post_hit_window_success_count")) for row in hits]
        success_counts = [value for value in success_counts if value is not None]
        mean_post = statistics.mean(means) if means else None
        min_post = min(mins) if mins else None
        rows.append(
            {
                "threshold_value": threshold_value,
                "threshold_label": threshold_label,
                "schema_class_id": schema_class_id,
                "run_count": run_count,
                "sustained_hit_count": sustained,
                "transient_hit_count": statuses.count("transient_hit"),
                "never_hit_count": statuses.count("never_hit"),
                "artifact_incomplete_count": sum(row.get("status") != "success" for row in aggs),
                "sustained_hit_rate": _share(sustained, run_count),
                "median_episodes_to_sustained_hit": (
                    statistics.median(episodes) if episodes else None
                ),
                "mean_episodes_to_sustained_hit": (statistics.mean(episodes) if episodes else None),
                "post_hit_window_mean": mean_post,
                "post_hit_window_min": min_post,
                "post_hit_window_success_count": (
                    statistics.mean(success_counts) if success_counts else None
                ),
                "threshold_margin_mean": None if mean_post is None else mean_post - threshold_value,
                "threshold_margin_min": None if min_post is None else min_post - threshold_value,
                "threshold_success_fraction": _share(
                    sum(_float(row.get("post_hit_window_success_count")) or 0 for row in hits),
                    len(hits) * 5,
                ),
                "passes_frontier_threshold": bool(run_count and sustained == run_count),
            }
        )
    return rows


def _threshold_pair_rows(
    *,
    threshold_value: float,
    threshold_label: str,
    run_rows: list[dict[str, str]],
    first_hit_rows: list[dict[str, str]],
) -> list[dict[str, Any]]:
    first_by_run = {row["run_id"]: row for row in first_hit_rows}
    grouped: dict[tuple[str, str], dict[str, dict[str, str]]] = defaultdict(dict)
    for row in run_rows:
        key = (row["candidate_group_id"], row["training_replicate_index"])
        grouped[key][row["schema_class_id"]] = row
    result = []
    for (_candidate, _replicate), arms in sorted(grouped.items()):
        schema0 = arms.get(SCHEMA0_CLASS_ID)
        schema1 = arms.get(SCHEMA1_CLASS_ID)
        if schema0 is None or schema1 is None:
            continue
        hit0 = first_by_run.get(schema0["run_id"], {})
        hit1 = first_by_run.get(schema1["run_id"], {})
        row = _pair_row(
            threshold_value=threshold_value,
            threshold_label=threshold_label,
            schema0_run=schema0,
            schema1_run=schema1,
            schema0_hit=hit0,
            schema1_hit=hit1,
        )
        result.append(row)
    return result


def _pair_row(
    *,
    threshold_value: float,
    threshold_label: str,
    schema0_run: dict[str, str],
    schema1_run: dict[str, str],
    schema0_hit: dict[str, str],
    schema1_hit: dict[str, str],
) -> dict[str, Any]:
    status0 = schema0_hit.get("hit_status", "artifact_incomplete")
    status1 = schema1_hit.get("hit_status", "artifact_incomplete")
    episodes0 = _float_or_none(schema0_hit.get("episodes_to_sustained_hit"))
    episodes1 = _float_or_none(schema1_hit.get("episodes_to_sustained_hit"))
    mean0 = _float_or_none(schema0_hit.get("post_hit_window_mean"))
    mean1 = _float_or_none(schema1_hit.get("post_hit_window_mean"))
    min0 = _float_or_none(schema0_hit.get("post_hit_window_min"))
    min1 = _float_or_none(schema1_hit.get("post_hit_window_min"))
    count0 = _float_or_none(schema0_hit.get("post_hit_window_success_count"))
    count1 = _float_or_none(schema1_hit.get("post_hit_window_success_count"))
    blocked = status0 != "sustained_hit" or status1 != "sustained_hit"
    delta_episode = _delta(episodes1, episodes0)
    delta_mean = _delta(mean1, mean0)
    delta_min = _delta(min1, min0)
    delta_count = _delta(count1, count0)
    if blocked:
        pair_status = "blocked_or_non_sustained"
        interpretation = "At least one schema arm did not satisfy sustained-hit."
    elif delta_episode is not None and delta_episode < 0:
        pair_status = "schema1_faster"
        interpretation = "Schema 1 reached sustained-hit earlier."
    elif delta_episode is not None and delta_episode > 0:
        pair_status = "schema1_slower"
        interpretation = "Schema 1 reached sustained-hit later."
    elif delta_mean is not None and delta_mean > 0:
        pair_status = "schema1_margin_higher"
        interpretation = "Both arms sustained, and Schema 1 had higher post-hit mean."
    elif delta_mean is not None and delta_mean < 0:
        pair_status = "schema1_margin_lower"
        interpretation = "Both arms sustained, and Schema 1 had lower post-hit mean."
    else:
        pair_status = "same_margin"
        interpretation = "Both arms sustained with no observed margin separation."
    return {
        "threshold_value": threshold_value,
        "threshold_label": threshold_label,
        "candidate_group_id": schema0_run["candidate_group_id"],
        "seed_bundle_id": schema0_run["seed_bundle_id"],
        "training_replicate_index": schema0_run["training_replicate_index"],
        "schema0_run_id": schema0_run["run_id"],
        "schema1_run_id": schema1_run["run_id"],
        "schema0_hit_status": status0,
        "schema1_hit_status": status1,
        "schema0_episodes_to_hit": episodes0,
        "schema1_episodes_to_hit": episodes1,
        "schema1_minus_schema0_episodes_to_hit": delta_episode,
        "schema0_post_hit_window_mean": mean0,
        "schema1_post_hit_window_mean": mean1,
        "schema1_minus_schema0_post_hit_window_mean": delta_mean,
        "schema0_post_hit_window_min": min0,
        "schema1_post_hit_window_min": min1,
        "schema1_minus_schema0_post_hit_window_min": delta_min,
        "schema0_post_hit_success_count": count0,
        "schema1_post_hit_success_count": count1,
        "schema1_minus_schema0_post_hit_success_count": delta_count,
        "pair_status": pair_status,
        "claim_blocked": blocked,
        "interpretation": interpretation,
    }


def _post_hit_margin_rows(
    *,
    threshold_value: float,
    threshold_label: str,
    first_hit_rows: list[dict[str, str]],
) -> list[dict[str, Any]]:
    grouped: dict[str, list[dict[str, str]]] = defaultdict(list)
    for row in first_hit_rows:
        grouped[row["schema_class_id"]].append(row)
    result = []
    for schema_class_id in (SCHEMA0_CLASS_ID, SCHEMA1_CLASS_ID):
        rows = grouped.get(schema_class_id, [])
        means = [_float(row.get("post_hit_window_mean")) for row in rows]
        means = [value for value in means if value is not None]
        mins = [_float(row.get("post_hit_window_min")) for row in rows]
        mins = [value for value in mins if value is not None]
        success_counts = [_float(row.get("post_hit_window_success_count")) for row in rows]
        success_counts = [value for value in success_counts if value is not None]
        post_mean = statistics.mean(means) if means else None
        post_min = min(mins) if mins else None
        result.append(
            {
                "threshold_value": threshold_value,
                "threshold_label": threshold_label,
                "schema_class_id": schema_class_id,
                "post_hit_window_mean": post_mean,
                "post_hit_window_min": post_min,
                "post_hit_window_success_count": (
                    statistics.mean(success_counts) if success_counts else None
                ),
                "threshold_margin_mean": None if post_mean is None else post_mean - threshold_value,
                "threshold_margin_min": None if post_min is None else post_min - threshold_value,
                "threshold_success_fraction": _share(
                    sum(success_counts),
                    len(rows) * 5,
                ),
            }
        )
    return result


def _first_failure_rows(rows: list[dict[str, Any]]) -> list[dict[str, Any]]:
    result = []
    by_schema: dict[str, list[dict[str, Any]]] = defaultdict(list)
    for row in rows:
        by_schema[row["schema_class_id"]].append(row)
    for schema_class_id in (SCHEMA0_CLASS_ID, SCHEMA1_CLASS_ID):
        schema_rows = sorted(
            by_schema.get(schema_class_id, ()),
            key=lambda row: float(row["threshold_value"]),
        )
        passing = [
            float(row["threshold_value"])
            for row in schema_rows
            if _bool(row["passes_frontier_threshold"])
        ]
        failing = [
            float(row["threshold_value"])
            for row in schema_rows
            if not _bool(row["passes_frontier_threshold"])
        ]
        if passing and not failing:
            classification = "no_failure_observed"
        elif failing and not passing:
            classification = "no_passing_threshold_observed"
        else:
            classification = "mixed_frontier"
        result.append(
            {
                "schema_class_id": schema_class_id,
                "first_failure_threshold": min(failing) if failing else None,
                "highest_passing_threshold": max(passing) if passing else None,
                "frontier_classification": classification,
            }
        )
    return result


def _frontier_rows(
    *,
    threshold_arm_rows: list[dict[str, Any]],
    threshold_pair_rows: list[dict[str, Any]],
    lift_failure_rows: list[dict[str, Any]],
) -> list[dict[str, Any]]:
    if not threshold_arm_rows:
        return []
    pass_by_schema: dict[str, set[float]] = defaultdict(set)
    all_thresholds = sorted({float(row["threshold_value"]) for row in threshold_arm_rows})
    for row in threshold_arm_rows:
        if _bool(row["passes_frontier_threshold"]):
            pass_by_schema[row["schema_class_id"]].add(float(row["threshold_value"]))
    schema0_pass = pass_by_schema[SCHEMA0_CLASS_ID]
    schema1_pass = pass_by_schema[SCHEMA1_CLASS_ID]
    shared = sorted(schema0_pass & schema1_pass)
    schema1_only = sorted(schema1_pass - schema0_pass)
    schema0_only = sorted(schema0_pass - schema1_pass)
    highest0 = max(schema0_pass) if schema0_pass else None
    highest1 = max(schema1_pass) if schema1_pass else None
    margin_wins = sum(
        _false(row["claim_blocked"])
        and (_float(row["schema1_minus_schema0_post_hit_window_mean"]) or 0) > 0
        for row in threshold_pair_rows
    )
    margin_losses = sum(
        _false(row["claim_blocked"])
        and (_float(row["schema1_minus_schema0_post_hit_window_mean"]) or 0) < 0
        for row in threshold_pair_rows
    )
    margin_same = sum(
        _false(row["claim_blocked"])
        and (_float(row["schema1_minus_schema0_post_hit_window_mean"]) or 0) == 0
        for row in threshold_pair_rows
    )
    blocked_threshold_count = len(
        {row["threshold_label"] for row in threshold_pair_rows if not _false(row["claim_blocked"])}
    )
    lift_failure_threshold_count = len(
        {row["threshold_label"] for row in lift_failure_rows if _event_count(row) > 0}
    )
    recommended = _recommended_threshold(
        schema1_only=schema1_only,
        threshold_pair_rows=threshold_pair_rows,
        all_thresholds=all_thresholds,
    )
    claim_status = _claim_status(
        highest0=highest0,
        highest1=highest1,
        margin_wins=margin_wins,
        margin_losses=margin_losses,
        lift_failure_threshold_count=lift_failure_threshold_count,
        threshold_pair_rows=threshold_pair_rows,
    )
    candidate_group_id = threshold_pair_rows[0]["candidate_group_id"] if threshold_pair_rows else ""
    return [
        {
            "candidate_group_id": candidate_group_id,
            "threshold_count": len(all_thresholds),
            "highest_shared_passing_threshold": max(shared) if shared else None,
            "highest_schema0_passing_threshold": highest0,
            "highest_schema1_passing_threshold": highest1,
            "schema1_only_passing_thresholds": ",".join(str(item) for item in schema1_only),
            "schema0_only_passing_thresholds": ",".join(str(item) for item in schema0_only),
            "schema1_frontier_minus_schema0_frontier": _delta(highest1, highest0),
            "schema1_margin_win_count": margin_wins,
            "schema1_margin_loss_count": margin_losses,
            "schema1_margin_same_count": margin_same,
            "blocked_threshold_count": blocked_threshold_count,
            "lift_failure_threshold_count": lift_failure_threshold_count,
            "recommended_replicate_probe_threshold": recommended,
            "claim_status": claim_status,
            "bounded_claim_text": _bounded_claim_text(claim_status, recommended),
        }
    ]


def _recommended_threshold(
    *,
    schema1_only: list[float],
    threshold_pair_rows: list[dict[str, Any]],
    all_thresholds: list[float],
) -> float | None:
    if schema1_only:
        return min(schema1_only)
    margin_positive = [
        float(row["threshold_value"])
        for row in threshold_pair_rows
        if _false(row["claim_blocked"])
        and (_float(row["schema1_minus_schema0_post_hit_window_mean"]) or 0) > 0
    ]
    if margin_positive:
        return max(margin_positive)
    if 13.0 in all_thresholds:
        return 13.0
    return all_thresholds[0] if all_thresholds else None


def _claim_status(
    *,
    highest0: float | None,
    highest1: float | None,
    margin_wins: int,
    margin_losses: int,
    lift_failure_threshold_count: int,
    threshold_pair_rows: list[dict[str, Any]],
) -> str:
    if lift_failure_threshold_count:
        return "frontier_blocked_by_liftability"
    if threshold_pair_rows and all(not _false(row["claim_blocked"]) for row in threshold_pair_rows):
        return "frontier_blocked_by_artifacts"
    if highest0 is not None and highest1 is not None:
        if highest1 > highest0:
            return "schema1_frontier_advantage_observed"
        if highest1 < highest0:
            return "schema1_frontier_disadvantage_observed"
    if margin_wins > margin_losses and margin_wins > 0:
        return "schema1_margin_advantage_only"
    if highest0 == highest1 and highest0 is not None:
        return "no_frontier_separation_observed"
    return "frontier_inconclusive"


def _bounded_claim_text(claim_status: str, recommended: float | None) -> str:
    if claim_status == "schema1_frontier_advantage_observed":
        return "Schema 1 sustained at a stricter tested threshold than Schema 0."
    if claim_status == "schema1_margin_advantage_only":
        return (
            "No frontier separation was observed, but Schema 1 had post-hit "
            f"margin wins; recommended paired threshold is {recommended}."
        )
    if claim_status == "no_frontier_separation_observed":
        return "Both arms share the same observed frontier under this small budget."
    if claim_status == "schema1_frontier_disadvantage_observed":
        return "Schema 1 did not preserve the frontier as well as Schema 0."
    if claim_status == "frontier_blocked_by_liftability":
        return "Lift failures block the threshold-frontier behavioral claim."
    if claim_status == "frontier_blocked_by_artifacts":
        return "Artifact or sustained-hit failures block the frontier claim."
    return "The frontier probe is inconclusive under this budget."


def _promote_rows(
    path: Path,
    *,
    threshold_value: float,
    threshold_label: str,
) -> list[dict[str, Any]]:
    rows = _read_csv(path) if path.exists() else []
    result = []
    for row in rows:
        promoted = dict(row)
        promoted["threshold_value"] = threshold_value
        promoted["threshold_label"] = threshold_label
        promoted["source_file"] = str(path)
        result.append(promoted)
    return result


def _unblocked_threshold_count(rows: list[dict[str, Any]]) -> int:
    return len({row["threshold_label"] for row in rows if _false(row["claim_blocked"])})


def _fieldnames(rows: list[dict[str, Any]]) -> tuple[str, ...]:
    if not rows:
        return ("threshold_value", "threshold_label", "source_file")
    keys: list[str] = []
    for row in rows:
        for key in row:
            if key not in keys:
                keys.append(key)
    return tuple(keys)


def _read_csv(path: Path) -> list[dict[str, str]]:
    with path.open(newline="", encoding="utf-8") as handle:
        return list(csv.DictReader(handle))


def _read_json(path: Path) -> dict[str, Any]:
    return json.loads(path.read_text(encoding="utf-8"))


def _float(value: object) -> float | None:
    if value in (None, ""):
        return None
    return float(value)


def _float_or_none(value: object) -> float | None:
    return _float(value)


def _delta(left: float | None, right: float | None) -> float | None:
    if left is None or right is None:
        return None
    return left - right


def _share(numerator: float, denominator: float) -> float | None:
    if not denominator:
        return None
    return numerator / denominator


def _bool(value: object) -> bool:
    if isinstance(value, bool):
        return value
    return str(value).lower() in {"true", "1", "yes"}


def _false(value: object) -> bool:
    return not _bool(value)


def _event_count(row: dict[str, Any]) -> int:
    for key in ("event_count", "lift_event_count", "count"):
        if key in row and row[key] not in (None, ""):
            return int(float(row[key]))
    if row.get("success") in {"False", "false", False}:
        return 1
    return 0
