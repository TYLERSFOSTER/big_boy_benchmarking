"""Selected replay-trace retention for Warehouse full-tower PPO."""

from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path

from big_boy_benchmarking.artifacts.writers import write_csv

from .config import WarehouseRetentionConfig
from .events import STEP_FIELDNAMES, TRACE_INDEX_FIELDNAMES


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


def base_retention_reason(
    *,
    episode_index: int,
    final_episode_index: int,
    config: WarehouseRetentionConfig,
) -> str:
    if not config.writes_selected_traces:
        return ""
    normalized = config.normalized_trace_indices()
    if episode_index in normalized:
        return "explicit_index"
    if "final" in normalized and episode_index == final_episode_index:
        return "final"
    if (
        config.retain_every_n_episodes > 0
        and episode_index % config.retain_every_n_episodes == 0
    ):
        return "retain_every_n_episodes"
    return ""


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
    write_csv(path, rows, STEP_FIELDNAMES, create_parents=True)
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
