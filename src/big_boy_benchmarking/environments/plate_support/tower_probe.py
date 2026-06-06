"""Upstream tower-depth probe wrapper for PlateSupport readiness."""

from __future__ import annotations

import json

from state_collapser.examples.tower_depth_probe import continuous_probe

from big_boy_benchmarking.environments.plate_support.ids import (
    DEFAULT_SCHEMA_ID,
    NO_CONTRACTION_SCHEMA_ID,
    UPSTREAM_SMOKE_ID,
)
from big_boy_benchmarking.environments.plate_support.types import TowerProbeRecord


def run_plate_support_tower_probe(
    *,
    steps: int = 20,
    seed: int = 0,
    sample_size: int = 20,
) -> tuple[TowerProbeRecord, ...]:
    return (
        _probe_record(
            schema_id=DEFAULT_SCHEMA_ID,
            upstream_schema_mode="default",
            steps=steps,
            seed=seed,
            sample_size=sample_size,
        ),
        _probe_record(
            schema_id=NO_CONTRACTION_SCHEMA_ID,
            upstream_schema_mode="none",
            steps=steps,
            seed=seed,
            sample_size=sample_size,
        ),
    )


def _probe_record(
    *,
    schema_id: str,
    upstream_schema_mode: str,
    steps: int,
    seed: int,
    sample_size: int,
) -> TowerProbeRecord:
    result = continuous_probe(
        env_name=UPSTREAM_SMOKE_ID,
        steps=steps,
        seed=seed,
        sample_size=sample_size,
        use_contraction_policy=True,
        reset_on_terminal=True,
        schema_mode=upstream_schema_mode,
    )
    return TowerProbeRecord(
        schema_id=schema_id,
        upstream_schema_mode=upstream_schema_mode,
        env_name=result.env_name,
        steps=steps,
        sample_size=sample_size,
        seed=seed,
        use_contraction_policy=True,
        reset_on_terminal=True,
        max_depth=int(result.max_depth),
        scheduled_assignment_count=int(result.scheduled_assignment_count),
        unscheduled_assignment_count=int(result.unscheduled_assignment_count),
        depth_curve=json.dumps(result.depth_curve, separators=(",", ":")),
        reset_event_count=len(result.reset_events),
    )
