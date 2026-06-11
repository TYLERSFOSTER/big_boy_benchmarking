"""Selected trace retention and artifact-size helpers."""

from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path

from big_boy_benchmarking.artifacts.writers import write_csv, write_json

from .config import TraceRetentionConfig

TRACE_FIELDNAMES = [
    "run_id",
    "arm_id",
    "replicate_index",
    "schema_seed",
    "episode_index",
    "step_index",
    "state_id",
    "next_state_id",
    "selected_action_id",
    "selected_action_summary",
    "reward",
    "correct_box_count",
    "correct_robot_count",
    "terminated",
    "truncated",
]

TRACE_INDEX_FIELDNAMES = [
    "run_id",
    "arm_id",
    "replicate_index",
    "schema_seed",
    "episode_index",
    "trace_path",
    "reason_retained",
    "step_count",
    "renderability_status",
]


@dataclass(frozen=True)
class TraceRecord:
    run_id: str
    arm_id: str
    replicate_index: int
    schema_seed: int
    episode_index: int
    trace_path: Path
    reason_retained: str
    step_count: int
    renderability_status: str = "renderable"

    def to_row(self) -> dict[str, object]:
        return {
            "run_id": self.run_id,
            "arm_id": self.arm_id,
            "replicate_index": self.replicate_index,
            "schema_seed": self.schema_seed,
            "episode_index": self.episode_index,
            "trace_path": str(self.trace_path),
            "reason_retained": self.reason_retained,
            "step_count": self.step_count,
            "renderability_status": self.renderability_status,
        }


def should_retain_episode(
    *,
    episode_index: int,
    final_episode_index: int,
    config: TraceRetentionConfig,
) -> tuple[bool, str]:
    normalized = config.normalized_trace_indices()
    if episode_index in normalized:
        return True, "explicit_index"
    if "final" in normalized and episode_index == final_episode_index:
        return True, "final"
    if config.trace_every_episodes > 0 and episode_index % config.trace_every_episodes == 0:
        return True, "trace_every_episodes"
    return False, ""


def write_selected_trace(
    *,
    trace_dir: Path,
    rows: list[dict[str, object]],
    run_id: str,
    arm_id: str,
    replicate_index: int,
    schema_seed: int,
    episode_index: int,
    reason: str,
) -> TraceRecord:
    trace_dir.mkdir(parents=True, exist_ok=True)
    path = trace_dir / "step_events.csv"
    write_csv(path, rows, TRACE_FIELDNAMES, create_parents=True)
    return TraceRecord(
        run_id=run_id,
        arm_id=arm_id,
        replicate_index=replicate_index,
        schema_seed=schema_seed,
        episode_index=episode_index,
        trace_path=path,
        reason_retained=reason,
        step_count=len(rows),
    )


def write_trace_index(path: Path, records: list[TraceRecord]) -> None:
    write_csv(
        path,
        [record.to_row() for record in records],
        TRACE_INDEX_FIELDNAMES,
        create_parents=True,
    )


def artifact_tree_size(path: Path) -> int:
    if not path.exists():
        return 0
    return sum(item.stat().st_size for item in path.rglob("*") if item.is_file())


def write_artifact_retention_manifest(
    *,
    path: Path,
    artifact_root: Path,
    config: TraceRetentionConfig,
    trace_records: list[TraceRecord],
) -> dict[str, object]:
    size = artifact_tree_size(artifact_root)
    status = "ok"
    if size > config.hard_artifact_budget_bytes:
        status = "hard_budget_exceeded"
    elif size > config.soft_artifact_budget_bytes:
        status = "soft_budget_warning"
    payload = {
        "artifact_retention_policy": "summary_first_selected_traces_only",
        "artifact_root": str(artifact_root),
        "artifact_root_size_bytes": size,
        "soft_artifact_budget_bytes": config.soft_artifact_budget_bytes,
        "hard_artifact_budget_bytes": config.hard_artifact_budget_bytes,
        "budget_status": status,
        "selected_trace_count": len(trace_records),
        "all_episode_step_events_written": False,
    }
    write_json(path, payload, create_parents=True)
    return payload
