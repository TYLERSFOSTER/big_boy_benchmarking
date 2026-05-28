"""Timing helpers for benchmark runs."""

from __future__ import annotations

import time
from collections.abc import Iterator
from contextlib import contextmanager
from dataclasses import dataclass

from big_boy_benchmarking.metrics.events import TimingSegmentRow

SEGMENT_CATEGORIES: dict[str, tuple[str, bool]] = {
    "environment_reset": ("algorithm_online", True),
    "environment_step": ("algorithm_online", True),
    "tower_reset": ("algorithm_online", True),
    "tower_update": ("algorithm_online", True),
    "controller_decision": ("algorithm_online", True),
    "lift_resolve": ("algorithm_online", True),
    "learner_act": ("algorithm_online", True),
    "learner_update": ("algorithm_online", True),
    "artifact_logging": ("benchmark_online", True),
    "compatibility_readout": ("readout", False),
    "morphism_construction": ("morphism", False),
    "posthoc_diagnostics": ("posthoc", False),
    "summary_generation": ("summary", False),
}


@dataclass
class TimingRecorder:
    run_id: str
    rows: list[TimingSegmentRow]

    @classmethod
    def create(cls, run_id: str) -> TimingRecorder:
        return cls(run_id=run_id, rows=[])

    @contextmanager
    def segment(self, segment_name: str) -> Iterator[None]:
        started = time.perf_counter()
        try:
            yield
        finally:
            elapsed = time.perf_counter() - started
            category, online = SEGMENT_CATEGORIES.get(segment_name, ("other", False))
            self.rows.append(
                TimingSegmentRow(
                    run_id=self.run_id,
                    segment_name=segment_name,
                    category=category,
                    seconds=elapsed,
                    online=online,
                )
            )


@contextmanager
def timing_segment(recorder: TimingRecorder, segment_name: str) -> Iterator[None]:
    with recorder.segment(segment_name):
        yield


def summarize_timing_segments(rows: list[TimingSegmentRow]) -> dict[str, float]:
    totals: dict[str, float] = {}
    for row in rows:
        totals[row.category] = totals.get(row.category, 0.0) + row.seconds
    totals["total"] = sum(row.seconds for row in rows)
    return totals
