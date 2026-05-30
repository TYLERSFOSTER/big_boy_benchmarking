"""Aggregation helpers for serious counterpoint learning artifacts."""

from __future__ import annotations

import csv
import json
import math
import statistics
from collections import Counter, defaultdict
from pathlib import Path
from typing import Any

from big_boy_benchmarking.artifacts.writers import write_csv, write_json
from big_boy_benchmarking.environments.counterpoint.serious_learning.arms import (
    DIRECT_TABULAR_Q_ARM_ID,
    REQUIRED_SERIOUS_LEARNING_ARM_IDS,
    TOWER_EMPTY_ARM_ID,
)
from big_boy_benchmarking.environments.counterpoint.serious_learning.direct import (
    SERIOUS_DIRECT_RUN_FAMILY_ID,
)
from big_boy_benchmarking.environments.counterpoint.serious_learning.evaluation_paths import (
    build_serious_learning_evaluation_paths,
)
from big_boy_benchmarking.environments.counterpoint.serious_learning.manifests import (
    AggregateSummary,
)
from big_boy_benchmarking.environments.counterpoint.serious_learning.tower_control import (
    SERIOUS_TOWER_RUN_FAMILY_ID,
)
from big_boy_benchmarking.metrics.bootstrap import mean_std, percentile_bootstrap_interval

AGGREGATE_FIELDNAMES = (
    "arm_id",
    "run_count",
    "episode_count",
    "mean_return",
    "std_return",
    "ci95_lower",
    "ci95_upper",
    "bootstrap_lower",
    "bootstrap_upper",
    "delta_vs_direct_tabular_q",
    "delta_vs_empty_tower",
    "schema_seed_count",
    "schema_seed_return_std",
    "status",
)


def aggregate_serious_learning_results(artifact_root: Path | str) -> dict[str, Any]:
    paths = build_serious_learning_evaluation_paths(artifact_root)
    paths.results_dir.mkdir(parents=True, exist_ok=True)
    run_index_path = (
        paths.evaluation_run_index_csv
        if paths.evaluation_run_index_csv.exists()
        else paths.calibration_run_index_csv
    )
    if not run_index_path.exists():
        raise FileNotFoundError(f"missing evaluation run index: {run_index_path}")
    run_rows = list(csv.DictReader(run_index_path.open()))
    learning_rows: list[dict[str, Any]] = []
    timing_rows: list[dict[str, Any]] = []
    controller_rows: list[dict[str, Any]] = []
    schema_rows: list[dict[str, Any]] = []
    returns_by_arm: dict[str, list[float]] = defaultdict(list)
    returns_by_arm_schema_seed: dict[tuple[str, str], list[float]] = defaultdict(list)
    status_by_arm: dict[str, set[str]] = defaultdict(set)

    for run_row in run_rows:
        arm_id = run_row["arm_id"]
        status_by_arm[arm_id].add(run_row["status"])
        if run_row["status"] != "success":
            continue
        run_id = run_row["run_id"]
        run_root = _run_root(Path(artifact_root), arm_id, run_id)
        for episode_row in _read_csv(run_root / "episodes.csv"):
            total_reward = float(episode_row["total_reward"])
            returns_by_arm[arm_id].append(total_reward)
            schema_seed = run_row.get("schema_seed") or ""
            if schema_seed:
                returns_by_arm_schema_seed[(arm_id, schema_seed)].append(total_reward)
            learning_rows.append(
                {
                    "arm_id": arm_id,
                    "run_id": run_id,
                    "schema_seed": schema_seed,
                    "episode_index": episode_row["episode_index"],
                    "total_reward": total_reward,
                    "step_count": episode_row["step_count"],
                    "success": episode_row["success"],
                }
            )
        timing_summary = _read_json(run_root / "timing_summary.json")
        for category, seconds in timing_summary.items():
            timing_rows.append(
                {
                    "arm_id": arm_id,
                    "run_id": run_id,
                    "category": category,
                    "seconds": seconds,
                }
            )
        action_counts = Counter(
            row["control_action"] for row in _read_csv(run_root / "control_events.csv")
        )
        for action, count in sorted(action_counts.items()):
            controller_rows.append(
                {
                    "arm_id": arm_id,
                    "run_id": run_id,
                    "control_action": action,
                    "count": count,
                }
            )
        quotient_summary = _read_json(run_root / "quotient_summary.json")
        if quotient_summary:
            schema_rows.append(
                {
                    "arm_id": arm_id,
                    "run_id": run_id,
                    "schema_id": quotient_summary.get("schema_id"),
                    "partition_tier_count": quotient_summary.get("partition_tier_count"),
                    "edge_count": quotient_summary.get("edge_count"),
                }
            )

    aggregate_rows = _aggregate_rows(returns_by_arm, returns_by_arm_schema_seed, status_by_arm)
    write_csv(paths.evaluation_aggregate_table_csv, aggregate_rows, AGGREGATE_FIELDNAMES)
    write_csv(
        paths.results_dir / "learning_curves.csv",
        learning_rows,
        (
            "arm_id",
            "run_id",
            "schema_seed",
            "episode_index",
            "total_reward",
            "step_count",
            "success",
        ),
    )
    write_csv(
        paths.results_dir / "timing_summary.csv",
        timing_rows,
        ("arm_id", "run_id", "category", "seconds"),
    )
    write_csv(
        paths.results_dir / "controller_summary.csv",
        controller_rows,
        ("arm_id", "run_id", "control_action", "count"),
    )
    write_csv(
        paths.results_dir / "schema_diagnostic_summary.csv",
        schema_rows,
        ("arm_id", "run_id", "schema_id", "partition_tier_count", "edge_count"),
    )
    complete_arm_count = sum(
        1 for arm_id in REQUIRED_SERIOUS_LEARNING_ARM_IDS if returns_by_arm.get(arm_id)
    )
    summary = AggregateSummary(
        evaluation_id="counterpoint_first_serious_learning_v001",
        status="complete"
        if complete_arm_count == len(REQUIRED_SERIOUS_LEARNING_ARM_IDS)
        else "incomplete",
        arm_count=len(REQUIRED_SERIOUS_LEARNING_ARM_IDS),
        complete_arm_count=complete_arm_count,
        baseline_arm_id=DIRECT_TABULAR_Q_ARM_ID,
        empty_tower_baseline_arm_id=TOWER_EMPTY_ARM_ID,
        table_path=str(paths.evaluation_aggregate_table_csv),
        result_paths=(
            str(paths.results_dir / "learning_curves.csv"),
            str(paths.results_dir / "timing_summary.csv"),
            str(paths.results_dir / "controller_summary.csv"),
            str(paths.results_dir / "schema_diagnostic_summary.csv"),
        ),
    )
    write_json(paths.evaluation_aggregate_summary, summary.to_dict())
    return summary.to_dict()


def _aggregate_rows(
    returns_by_arm: dict[str, list[float]],
    returns_by_arm_schema_seed: dict[tuple[str, str], list[float]],
    status_by_arm: dict[str, set[str]],
) -> list[dict[str, Any]]:
    direct_mean = _mean_or_none(returns_by_arm.get(DIRECT_TABULAR_Q_ARM_ID, []))
    empty_mean = _mean_or_none(returns_by_arm.get(TOWER_EMPTY_ARM_ID, []))
    rows: list[dict[str, Any]] = []
    for arm_id in REQUIRED_SERIOUS_LEARNING_ARM_IDS:
        returns = returns_by_arm.get(arm_id, [])
        mean_value, std_value = (None, None) if not returns else mean_std(tuple(returns))
        ci_lower, ci_upper = _normal_ci(returns)
        bootstrap_lower, bootstrap_upper = _bootstrap_or_none(returns, arm_id)
        schema_means = [
            statistics.mean(values)
            for (schema_arm_id, _seed), values in returns_by_arm_schema_seed.items()
            if schema_arm_id == arm_id and values
        ]
        rows.append(
            {
                "arm_id": arm_id,
                "run_count": len(returns),
                "episode_count": len(returns),
                "mean_return": mean_value,
                "std_return": std_value,
                "ci95_lower": ci_lower,
                "ci95_upper": ci_upper,
                "bootstrap_lower": bootstrap_lower,
                "bootstrap_upper": bootstrap_upper,
                "delta_vs_direct_tabular_q": None
                if mean_value is None or direct_mean is None
                else mean_value - direct_mean,
                "delta_vs_empty_tower": None
                if mean_value is None or empty_mean is None
                else mean_value - empty_mean,
                "schema_seed_count": len(schema_means),
                "schema_seed_return_std": statistics.pstdev(schema_means)
                if len(schema_means) > 1
                else None,
                "status": "complete"
                if returns
                else ("failed" if "failed" in status_by_arm.get(arm_id, set()) else "missing"),
            }
        )
    return rows


def _run_root(artifact_root: Path, arm_id: str, run_id: str) -> Path:
    family_id = (
        SERIOUS_DIRECT_RUN_FAMILY_ID
        if arm_id in {DIRECT_TABULAR_Q_ARM_ID, "direct_masked_random"}
        else SERIOUS_TOWER_RUN_FAMILY_ID
    )
    return artifact_root / "runs" / family_id / "runs" / run_id


def _read_csv(path: Path) -> list[dict[str, str]]:
    if not path.exists():
        return []
    return list(csv.DictReader(path.open()))


def _read_json(path: Path) -> dict[str, Any]:
    if not path.exists():
        return {}
    return json.loads(path.read_text())


def _mean_or_none(values: list[float]) -> float | None:
    if not values:
        return None
    return statistics.mean(values)


def _normal_ci(values: list[float]) -> tuple[float | None, float | None]:
    if len(values) < 2:
        return None, None
    mean_value = statistics.mean(values)
    stderr = statistics.stdev(values) / math.sqrt(len(values))
    spread = 1.96 * stderr
    return mean_value - spread, mean_value + spread


def _bootstrap_or_none(values: list[float], arm_id: str) -> tuple[float | None, float | None]:
    if len(values) < 2:
        return None, None
    seed = sum(ord(char) for char in arm_id)
    return percentile_bootstrap_interval(tuple(values), seed=seed, resamples=200)
