"""Aggregation for Warehouse transformer policy runs."""

from __future__ import annotations

from collections import defaultdict
from pathlib import Path

from big_boy_benchmarking.artifacts.writers import write_csv, write_json

from .checkpoints import CheckpointRecord
from .trace_retention import TraceRecord, write_trace_index

EPISODE_FIELDNAMES = [
    "run_id",
    "arm_id",
    "replicate_index",
    "schema_seed",
    "episode_index",
    "max_seconds",
    "step_count",
    "total_reward",
    "terminated",
    "truncated",
    "failure_reason",
    "optimizer_steps",
    "policy_loss",
    "value_loss",
    "entropy",
    "grad_norm",
    "correct_box_count",
    "correct_robot_count",
]

TRAINING_CURVE_FIELDNAMES = [
    "run_id",
    "arm_id",
    "episode_index",
    "total_reward",
    "rolling_mean_reward",
    "optimizer_steps",
    "max_seconds",
]

RUN_INDEX_FIELDNAMES = [
    "run_id",
    "arm_id",
    "replicate_index",
    "schema_seed",
    "seed",
    "status",
    "run_root",
]

RESOLVER_FIELDNAMES = [
    "run_id",
    "arm_id",
    "raw_valid_count",
    "selected_valid_count",
    "fallback_used_count",
    "projection_attempt_count",
    "successor_out_count_used_for_selection_count",
]

TOWER_LIVE_LIFT_FIELDNAMES = [
    "run_id",
    "arm_id",
    "live_lift_step_count",
    "dead_lift_failure_count",
    "mean_candidate_count",
    "mean_live_out_count",
]

CURRICULUM_FIELDNAMES = [
    "run_id",
    "arm_id",
    "min_max_seconds",
    "max_max_seconds",
    "episode_count",
]

TIMING_FIELDNAMES = [
    "run_id",
    "arm_id",
    "duration_seconds",
    "episode_count",
]

ARTIFACT_RETENTION_FIELDNAMES = [
    "artifact_root",
    "artifact_root_size_bytes",
    "soft_artifact_budget_bytes",
    "hard_artifact_budget_bytes",
    "budget_status",
    "selected_trace_count",
    "all_episode_step_events_written",
]


def write_result_tables(
    *,
    results_dir: Path,
    episode_rows: list[dict[str, object]],
    run_index_rows: list[dict[str, object]],
    resolver_rows: list[dict[str, object]],
    tower_rows: list[dict[str, object]],
    timing_rows: list[dict[str, object]],
    trace_records: list[TraceRecord],
    checkpoint_records: list[CheckpointRecord],
    artifact_retention: dict[str, object],
) -> dict[str, object]:
    results_dir.mkdir(parents=True, exist_ok=True)
    write_csv(results_dir / "episode_summary.csv", episode_rows, EPISODE_FIELDNAMES)
    write_csv(
        results_dir / "training_curve_summary.csv",
        _training_curve_rows(episode_rows),
        TRAINING_CURVE_FIELDNAMES,
    )
    write_csv(
        results_dir / "resolver_summary.csv",
        _resolver_summary_rows(resolver_rows),
        RESOLVER_FIELDNAMES,
    )
    write_csv(
        results_dir / "tower_live_lift_summary.csv",
        _tower_summary_rows(tower_rows),
        TOWER_LIVE_LIFT_FIELDNAMES,
    )
    write_csv(
        results_dir / "curriculum_summary.csv",
        _curriculum_summary_rows(episode_rows),
        CURRICULUM_FIELDNAMES,
    )
    write_csv(results_dir / "timing_summary.csv", timing_rows, TIMING_FIELDNAMES)
    write_csv(
        results_dir / "checkpoint_summary.csv",
        [record.to_manifest_row() for record in checkpoint_records],
        [
            "checkpoint_id",
            "path",
            "episode_index",
            "optimizer_steps",
            "reason",
            "rolling_reward",
            "file_size_bytes",
            "sha256",
        ],
    )
    write_trace_index(results_dir / "trace_episode_index.csv", trace_records)
    write_csv(
        results_dir / "artifact_retention_summary.csv",
        [artifact_retention],
        ARTIFACT_RETENTION_FIELDNAMES,
    )
    write_csv(results_dir.parent / "run_index.csv", run_index_rows, RUN_INDEX_FIELDNAMES)
    summary = aggregate_summary(
        episode_rows=episode_rows,
        checkpoint_records=checkpoint_records,
        trace_records=trace_records,
        artifact_retention=artifact_retention,
    )
    write_json(results_dir.parent / "evaluation_aggregate_summary.json", summary)
    return summary


def aggregate_summary(
    *,
    episode_rows: list[dict[str, object]],
    checkpoint_records: list[CheckpointRecord],
    trace_records: list[TraceRecord],
    artifact_retention: dict[str, object],
) -> dict[str, object]:
    rewards = [float(row["total_reward"]) for row in episode_rows]
    optimizer_steps = max((int(row["optimizer_steps"]) for row in episode_rows), default=0)
    return {
        "status": "complete",
        "claim_boundary": [
            "transformer policy training surface smoke/diagnostic evidence only",
            "not a broad tower superiority claim",
            "not a final Warehouse Gridlock benchmark",
        ],
        "episode_count": len(episode_rows),
        "mean_total_reward": sum(rewards) / len(rewards) if rewards else 0.0,
        "max_total_reward": max(rewards) if rewards else 0.0,
        "min_total_reward": min(rewards) if rewards else 0.0,
        "optimizer_steps": optimizer_steps,
        "checkpoint_count": len(checkpoint_records),
        "selected_trace_count": len(trace_records),
        "artifact_budget_status": artifact_retention.get("budget_status", "unknown"),
        "all_episode_step_events_written": False,
        "model_training_status": (
            "optimizer_steps_present" if optimizer_steps > 0 else "no_optimizer_steps"
        ),
    }


def _training_curve_rows(rows: list[dict[str, object]]) -> list[dict[str, object]]:
    grouped: dict[str, list[dict[str, object]]] = defaultdict(list)
    for row in rows:
        grouped[str(row["run_id"])].append(row)
    output: list[dict[str, object]] = []
    for run_id, group in grouped.items():
        group = sorted(group, key=lambda item: int(item["episode_index"]))
        rewards: list[float] = []
        for row in group:
            rewards.append(float(row["total_reward"]))
            window = rewards[-10:]
            output.append(
                {
                    "run_id": run_id,
                    "arm_id": row["arm_id"],
                    "episode_index": row["episode_index"],
                    "total_reward": row["total_reward"],
                    "rolling_mean_reward": sum(window) / len(window),
                    "optimizer_steps": row["optimizer_steps"],
                    "max_seconds": row["max_seconds"],
                }
            )
    return output


def _resolver_summary_rows(rows: list[dict[str, object]]) -> list[dict[str, object]]:
    grouped: dict[tuple[str, str], list[dict[str, object]]] = defaultdict(list)
    for row in rows:
        grouped[(str(row["run_id"]), str(row["arm_id"]))].append(row)
    return [
        {
            "run_id": run_id,
            "arm_id": arm_id,
            "raw_valid_count": sum(1 for row in group if row["raw_valid"]),
            "selected_valid_count": sum(1 for row in group if row["selected_valid"]),
            "fallback_used_count": sum(1 for row in group if row["fallback_used"]),
            "projection_attempt_count": sum(int(row["projection_attempt_count"]) for row in group),
            "successor_out_count_used_for_selection_count": sum(
                1 for row in group if row["successor_out_count_used_for_selection"]
            ),
        }
        for (run_id, arm_id), group in sorted(grouped.items())
    ]


def _tower_summary_rows(rows: list[dict[str, object]]) -> list[dict[str, object]]:
    grouped: dict[tuple[str, str], list[dict[str, object]]] = defaultdict(list)
    for row in rows:
        grouped[(str(row["run_id"]), str(row["arm_id"]))].append(row)
    output = []
    for (run_id, arm_id), group in sorted(grouped.items()):
        output.append(
            {
                "run_id": run_id,
                "arm_id": arm_id,
                "live_lift_step_count": len(group),
                "dead_lift_failure_count": sum(1 for row in group if row["lift_failure"]),
                "mean_candidate_count": _mean([float(row["candidate_count"]) for row in group]),
                "mean_live_out_count": _mean([float(row["live_out_count"]) for row in group]),
            }
        )
    return output


def _curriculum_summary_rows(rows: list[dict[str, object]]) -> list[dict[str, object]]:
    grouped: dict[tuple[str, str], list[dict[str, object]]] = defaultdict(list)
    for row in rows:
        grouped[(str(row["run_id"]), str(row["arm_id"]))].append(row)
    return [
        {
            "run_id": run_id,
            "arm_id": arm_id,
            "min_max_seconds": min(int(row["max_seconds"]) for row in group),
            "max_max_seconds": max(int(row["max_seconds"]) for row in group),
            "episode_count": len(group),
        }
        for (run_id, arm_id), group in sorted(grouped.items())
    ]


def _mean(values: list[float]) -> float:
    return sum(values) / len(values) if values else 0.0
