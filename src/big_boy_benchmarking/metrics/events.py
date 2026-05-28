"""Flat metric/event row contracts."""

from __future__ import annotations

from dataclasses import asdict, dataclass, fields
from typing import Any


class FlatRow:
    """Mixin for stable field order and flat dictionary serialization."""

    def to_flat_dict(self) -> dict[str, Any]:
        return asdict(self)

    @classmethod
    def fieldnames(cls) -> tuple[str, ...]:
        return tuple(field.name for field in fields(cls))


@dataclass(frozen=True)
class RunIndexRow(FlatRow):
    run_family_id: str
    run_id: str
    environment_id: str
    mode_id: str
    status: str
    started_at: str
    ended_at: str | None
    artifact_schema_version: str


@dataclass(frozen=True)
class EpisodeRow(FlatRow):
    run_id: str
    episode_index: int
    seed_bundle_id: str
    total_reward: float
    step_count: int
    terminated: bool
    truncated: bool


@dataclass(frozen=True)
class StepEventRow(FlatRow):
    run_id: str
    episode_index: int
    step_index: int
    action: int | str
    reward: float
    terminated: bool
    truncated: bool
    active_tier_before: int | None = None
    active_tier_after: int | None = None


@dataclass(frozen=True)
class ControlEventRow(FlatRow):
    run_id: str
    episode_index: int
    step_index: int
    control_action: str
    active_tier_before: int | None
    active_tier_after: int | None
    lift_success: bool | None
    fallback_reason: str | None


@dataclass(frozen=True)
class TimingSegmentRow(FlatRow):
    run_id: str
    segment_name: str
    category: str
    seconds: float
    online: bool


@dataclass(frozen=True)
class StructuralDiagnosticRow(FlatRow):
    run_id: str
    diagnostic_name: str
    lifecycle: str
    exact_or_sampled: str
    readout_backed: bool
    tier_index: int | None
    schema_id: str | None
    value: str


@dataclass(frozen=True)
class WarningRow(FlatRow):
    run_id: str
    warning_code: str
    message: str


@dataclass(frozen=True)
class BootstrapIntervalRow(FlatRow):
    metric_name: str
    seed_count: int
    replicate_count: int
    lower: float
    upper: float
    confidence_level: float
