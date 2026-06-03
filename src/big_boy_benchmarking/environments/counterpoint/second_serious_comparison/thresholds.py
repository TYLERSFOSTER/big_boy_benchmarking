"""Threshold and persistence helpers for sustained-hit comparisons."""

from __future__ import annotations

from dataclasses import asdict, dataclass
from typing import Any

from big_boy_benchmarking.environments.counterpoint.second_serious_comparison.config import (
    DEFAULT_REQUIRED_COUNT,
    DEFAULT_THRESHOLD_POLICY_ID,
    DEFAULT_TIER_JUMP_POLICY_ID,
    DEFAULT_WINDOW_LENGTH,
    METRIC_ID,
    SCHEMA0_CLASS_ID,
    SCHEMA1_CLASS_ID,
)


@dataclass(frozen=True)
class ThresholdPolicy:
    threshold_policy_id: str = DEFAULT_THRESHOLD_POLICY_ID
    metric_id: str = METRIC_ID
    threshold_value: float = 0.0
    window_length: int = DEFAULT_WINDOW_LENGTH
    required_count: int = DEFAULT_REQUIRED_COUNT
    comparison: str = "greater_than_or_equal"
    scope: str = "total_space"
    applies_to_schema_classes: tuple[str, ...] = (SCHEMA0_CLASS_ID, SCHEMA1_CLASS_ID)

    def __post_init__(self) -> None:
        if self.metric_id != METRIC_ID:
            raise ValueError("threshold metric is locked to episode_total_reward")
        if self.comparison != "greater_than_or_equal":
            raise ValueError("threshold comparison is locked to greater_than_or_equal")
        if self.scope != "total_space":
            raise ValueError("threshold scope is locked to total_space")
        if self.window_length <= 0:
            raise ValueError("window_length must be positive")
        if self.required_count <= 0 or self.required_count > self.window_length:
            raise ValueError("required_count must be in 1..window_length")

    def to_dict(self) -> dict[str, Any]:
        return asdict(self)


@dataclass(frozen=True)
class TierJumpPolicy:
    tier_jump_policy_id: str = DEFAULT_TIER_JUMP_POLICY_ID
    tier_jump_reward_cutoff: float | None = None
    tier_jump_metric_id: str = METRIC_ID
    tier_jump_window_length: int | None = None
    tier_jump_min_observations: int = 1
    tier_jump_applies_to_schema0: bool = False
    tier_jump_applies_to_schema1: bool = True
    tier_jump_disabled_reason: str | None = (
        "Schema 0 has no non-base tier; Schema 1 tier movement is produced by "
        "the active-tier controller and recorded observationally."
    )

    def to_dict(self) -> dict[str, Any]:
        return asdict(self)


@dataclass(frozen=True)
class ThresholdWindow:
    episode_window_start: int
    episode_window_end: int
    threshold_hit_count: int
    window_met: bool
    window_mean_total_reward: float | None
    window_min_total_reward: float | None


@dataclass(frozen=True)
class FirstHitResult:
    first_hit_episode_index: int | None
    first_sustained_hit_episode_index: int | None
    first_sustained_hit_training_step: int | None
    hit_status: str
    episodes_to_sustained_hit: int | None
    training_steps_to_sustained_hit: int | None
    post_hit_window_mean: float | None
    post_hit_window_min: float | None
    post_hit_window_success_count: int | None
    hit_failure_reason: str | None
    windows: tuple[ThresholdWindow, ...]


def compute_first_hit(
    rewards: tuple[float, ...],
    *,
    threshold_policy: ThresholdPolicy,
    steps_by_episode: tuple[int, ...] | None = None,
) -> FirstHitResult:
    if not rewards:
        return FirstHitResult(
            first_hit_episode_index=None,
            first_sustained_hit_episode_index=None,
            first_sustained_hit_training_step=None,
            hit_status="artifact_incomplete",
            episodes_to_sustained_hit=None,
            training_steps_to_sustained_hit=None,
            post_hit_window_mean=None,
            post_hit_window_min=None,
            post_hit_window_success_count=None,
            hit_failure_reason="no_episode_rewards",
            windows=(),
        )
    steps = steps_by_episode or tuple(0 for _ in rewards)
    first_hit = next(
        (
            index
            for index, reward in enumerate(rewards)
            if reward >= threshold_policy.threshold_value
        ),
        None,
    )
    windows: list[ThresholdWindow] = []
    first_sustained: int | None = None
    for start in range(0, max(0, len(rewards) - threshold_policy.window_length + 1)):
        window = rewards[start : start + threshold_policy.window_length]
        hit_count = sum(reward >= threshold_policy.threshold_value for reward in window)
        met = hit_count >= threshold_policy.required_count
        windows.append(
            ThresholdWindow(
                episode_window_start=start,
                episode_window_end=start + threshold_policy.window_length - 1,
                threshold_hit_count=hit_count,
                window_met=met,
                window_mean_total_reward=sum(window) / len(window) if window else None,
                window_min_total_reward=min(window) if window else None,
            )
        )
        if met and first_sustained is None:
            first_sustained = start + threshold_policy.window_length - 1
    if first_sustained is not None:
        window = rewards[first_sustained - threshold_policy.window_length + 1 : first_sustained + 1]
        return FirstHitResult(
            first_hit_episode_index=first_hit,
            first_sustained_hit_episode_index=first_sustained,
            first_sustained_hit_training_step=sum(steps[: first_sustained + 1]),
            hit_status="sustained_hit",
            episodes_to_sustained_hit=first_sustained + 1,
            training_steps_to_sustained_hit=sum(steps[: first_sustained + 1]),
            post_hit_window_mean=sum(window) / len(window) if window else None,
            post_hit_window_min=min(window) if window else None,
            post_hit_window_success_count=sum(
                reward >= threshold_policy.threshold_value for reward in window
            ),
            hit_failure_reason=None,
            windows=tuple(windows),
        )
    if first_hit is not None:
        status = "transient_hit_only"
        reason = "threshold_crossed_but_persistence_rule_not_met"
    else:
        status = "never_hit"
        reason = "threshold_never_crossed"
    return FirstHitResult(
        first_hit_episode_index=first_hit,
        first_sustained_hit_episode_index=None,
        first_sustained_hit_training_step=None,
        hit_status=status,
        episodes_to_sustained_hit=None,
        training_steps_to_sustained_hit=None,
        post_hit_window_mean=None,
        post_hit_window_min=None,
        post_hit_window_success_count=None,
        hit_failure_reason=reason,
        windows=tuple(windows),
    )
