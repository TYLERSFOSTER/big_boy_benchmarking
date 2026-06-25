"""Aggregation for Warehouse full-tower PPO."""

from __future__ import annotations

import csv
from pathlib import Path

from big_boy_benchmarking.artifacts.writers import write_csv, write_json

from .events import (
    EPISODE_FIELDNAMES,
    POINTWISE_SURFACE_FIELDNAMES,
    PPO_UPDATE_FIELDNAMES,
    RUN_INDEX_FIELDNAMES,
    STEP_FIELDNAMES,
    TIER_POLICY_FIELDNAMES,
    TIMING_FIELDNAMES,
)
from .paths import FullTowerPPOPaths
from .trace_retention import TraceRecord, write_trace_index


def write_evaluation_tables(
    *,
    paths: FullTowerPPOPaths,
    run_index_rows: list[dict[str, object]],
    episode_rows: list[dict[str, object]],
    step_rows: list[dict[str, object]],
    surface_rows: list[dict[str, object]],
    update_rows: list[dict[str, object]],
    tier_policy_rows: list[dict[str, object]],
    timing_rows: list[dict[str, object]],
    trace_records: list[TraceRecord] | None = None,
) -> dict[str, object]:
    trace_records = trace_records or []
    write_csv(paths.run_index, run_index_rows, RUN_INDEX_FIELDNAMES, create_parents=True)
    write_csv(paths.results_dir / "episode_summary.csv", episode_rows, EPISODE_FIELDNAMES)
    write_csv(paths.results_dir / "step_summary.csv", step_rows, STEP_FIELDNAMES)
    write_csv(
        paths.results_dir / "pointwise_action_surface_summary.csv",
        surface_rows,
        POINTWISE_SURFACE_FIELDNAMES,
    )
    write_csv(paths.results_dir / "ppo_update_summary.csv", update_rows, PPO_UPDATE_FIELDNAMES)
    write_csv(
        paths.results_dir / "tier_policy_summary.csv",
        tier_policy_rows,
        TIER_POLICY_FIELDNAMES,
    )
    write_csv(paths.results_dir / "timing_summary.csv", timing_rows, TIMING_FIELDNAMES)
    write_trace_index(paths.trace_index, trace_records)
    summary = aggregate_from_rows(
        episode_rows=episode_rows,
        update_rows=update_rows,
        surface_rows=surface_rows,
        trace_count=len(trace_records),
    )
    write_json(paths.aggregate_summary, summary, create_parents=True)
    write_csv(paths.aggregate_table, [summary], list(summary.keys()), create_parents=True)
    return summary


def summarize_existing(paths: FullTowerPPOPaths) -> dict[str, object]:
    episode_rows = _read_csv(paths.results_dir / "episode_summary.csv")
    update_rows = _read_csv(paths.results_dir / "ppo_update_summary.csv")
    surface_rows = _read_csv(paths.results_dir / "pointwise_action_surface_summary.csv")
    trace_rows = _read_csv(paths.trace_index)
    summary = aggregate_from_rows(
        episode_rows=[dict(row) for row in episode_rows],
        update_rows=[dict(row) for row in update_rows],
        surface_rows=[dict(row) for row in surface_rows],
        trace_count=len(trace_rows),
    )
    write_json(paths.aggregate_summary, summary, create_parents=True)
    write_csv(paths.aggregate_table, [summary], list(summary.keys()), create_parents=True)
    return summary


def aggregate_from_rows(
    *,
    episode_rows: list[dict[str, object]],
    update_rows: list[dict[str, object]],
    surface_rows: list[dict[str, object]],
    trace_count: int = 0,
) -> dict[str, object]:
    rewards = [_float(row.get("total_reward")) for row in episode_rows]
    successes = [_truthy(row.get("terminated")) for row in episode_rows]
    optimizer_steps = max((_int(row.get("optimizer_steps")) for row in update_rows), default=0)
    representative_fallback_count = 0
    if surface_rows:
        empty_actor_surface_count = sum(
            1 for row in surface_rows if _int(row.get("candidate_action_count")) <= 0
        )
        pointwise_surface_row_count = len(surface_rows)
        tier_indices = sorted({_int(row.get("tier_index")) for row in surface_rows})
    else:
        empty_actor_surface_count = sum(
            _int(row.get("empty_actor_surface_count")) for row in episode_rows
        )
        pointwise_surface_row_count = sum(
            _int(row.get("pointwise_surface_count")) for row in episode_rows
        )
        tier_indices = _episode_tier_indices(episode_rows)
    return {
        "status": "complete",
        "evaluation_status": (
            "ppo_updates_present" if optimizer_steps > 0 else "no_ppo_updates"
        ),
        "claim_boundary": (
            "system readiness and smoke evidence only; not a final broad benchmark claim"
        ),
        "episode_count": len(episode_rows),
        "success_count": sum(1 for item in successes if item),
        "success_rate": _ratio(sum(1 for item in successes if item), len(successes)),
        "mean_total_reward": _mean(rewards),
        "max_total_reward": max(rewards) if rewards else 0.0,
        "min_total_reward": min(rewards) if rewards else 0.0,
        "ppo_update_row_count": len(update_rows),
        "optimizer_steps": optimizer_steps,
        "tier_indices_seen": "|".join(str(index) for index in tier_indices),
        "representative_fallback_count": representative_fallback_count,
        "empty_actor_surface_count": empty_actor_surface_count,
        "pointwise_surface_row_count": pointwise_surface_row_count,
        "retained_trace_count": trace_count,
    }


def _read_csv(path: Path) -> list[dict[str, str]]:
    if not path.exists():
        return []
    with path.open(newline="", encoding="utf-8") as handle:
        return list(csv.DictReader(handle))


def _float(value: object) -> float:
    try:
        return float(value)  # type: ignore[arg-type]
    except (TypeError, ValueError):
        return 0.0


def _int(value: object) -> int:
    try:
        return int(float(value))  # type: ignore[arg-type]
    except (TypeError, ValueError):
        return 0


def _truthy(value: object) -> bool:
    return str(value).lower() in {"1", "true", "yes"}


def _mean(values: list[float]) -> float:
    return 0.0 if not values else sum(values) / len(values)


def _ratio(numerator: float, denominator: float) -> float:
    return 0.0 if denominator == 0 else numerator / denominator


def _episode_tier_indices(rows: list[dict[str, object]]) -> list[int]:
    values: set[int] = set()
    for row in rows:
        for item in str(row.get("tier_indices_seen", "")).split("|"):
            if not item:
                continue
            values.add(_int(item))
    return sorted(values)
