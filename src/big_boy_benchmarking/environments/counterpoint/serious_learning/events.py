"""Event rows for serious counterpoint learning evaluation artifacts."""

from __future__ import annotations

from dataclasses import dataclass

from big_boy_benchmarking.metrics.events import FlatRow


@dataclass(frozen=True)
class SeriousEpisodeRow(FlatRow):
    evaluation_id: str
    run_id: str
    arm_id: str
    mode_id: str
    schema_id: str | None
    schema_seed: int | None
    seed_bundle_id: str
    replicate_index: int
    episode_index: int
    total_reward: float
    step_count: int
    terminated: bool
    truncated: bool
    success: bool
    final_state: str


@dataclass(frozen=True)
class SeriousStepRow(FlatRow):
    evaluation_id: str
    run_id: str
    arm_id: str
    episode_index: int
    step_index: int
    source_state: str
    action_id: int | None
    action_repr: str
    reward: float
    target_state: str
    terminated: bool
    truncated: bool
    active_tier_before: int | None = None
    active_tier_after: int | None = None


@dataclass(frozen=True)
class ControllerEventRow(FlatRow):
    evaluation_id: str
    run_id: str
    arm_id: str
    episode_index: int
    step_index: int
    active_tier_before: int | None
    active_tier_after: int | None
    control_action: str
    pressure: float | None
    learner_updated: bool | None
    td_error: float | None
    success: bool | None


@dataclass(frozen=True)
class LiftFiberEventRow(FlatRow):
    evaluation_id: str
    run_id: str
    arm_id: str
    episode_index: int
    step_index: int
    active_tier: int | None
    abstract_action: str
    realized_action: str | None
    candidate_count: int
    success: bool
    failure_reason: str | None
    fiber_departure_reason: str | None


@dataclass(frozen=True)
class EvaluationRunIndexRow(FlatRow):
    evaluation_id: str
    run_id: str
    arm_id: str
    mode_id: str
    schema_id: str | None
    schema_seed: int | None
    seed_bundle_id: str
    replicate_index: int
    status: str
    artifact_root: str
    started_at: str
    ended_at: str | None


@dataclass(frozen=True)
class ArmSummaryRow(FlatRow):
    evaluation_id: str
    arm_id: str
    mode_id: str
    schema_family_id: str | None
    run_count: int
    episode_count: int
    mean_return: float | None
    std_return: float | None
    mean_step_count: float | None
    success_rate: float | None
    status: str
