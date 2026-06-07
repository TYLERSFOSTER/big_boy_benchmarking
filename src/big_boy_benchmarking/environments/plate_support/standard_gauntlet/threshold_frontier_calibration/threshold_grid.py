"""Evidence-derived return threshold grid construction."""

from __future__ import annotations

from .stage_sources import Stage1StructuralContext


def build_threshold_grid(
    *,
    calibration_episode_rows: list[dict[str, object]],
    structural_context: Stage1StructuralContext,
    quantiles: tuple[float, ...],
) -> list[dict[str, object]]:
    """Build threshold rows from observed rewards and Stage 1 context."""

    rows: list[dict[str, object]] = []
    seen_values: set[float] = set()

    def add(
        *,
        value: float,
        source_metric: str,
        source_arm: str,
        source_quantile: str,
        construction_reason: str,
    ) -> None:
        rounded = round(float(value), 12)
        if rounded in seen_values:
            return
        seen_values.add(rounded)
        rows.append(
            {
                "threshold_id": f"return_threshold_{len(rows):03d}",
                "threshold_value": rounded,
                "source_metric": source_metric,
                "source_arm": source_arm,
                "source_quantile": source_quantile,
                "construction_reason": construction_reason,
            }
        )

    grouped_rewards: dict[str, list[float]] = {}
    grouped_goal_rewards: dict[str, list[float]] = {}
    grouped_miss_rewards: dict[str, list[float]] = {}
    for row in calibration_episode_rows:
        arm_id = str(row["calibration_arm_id"])
        reward = float(row["total_reward"])
        grouped_rewards.setdefault(arm_id, []).append(reward)
        if _truthy(row["goal_reached"]):
            grouped_goal_rewards.setdefault(arm_id, []).append(reward)
        else:
            grouped_miss_rewards.setdefault(arm_id, []).append(reward)

    for arm_id, rewards in sorted(grouped_rewards.items()):
        sorted_rewards = sorted(rewards)
        for quantile in quantiles:
            add(
                value=_quantile(sorted_rewards, quantile),
                source_metric="total_reward",
                source_arm=arm_id,
                source_quantile=f"{quantile:g}",
                construction_reason="observed arm reward quantile",
            )
        goal_rewards = grouped_goal_rewards.get(arm_id, [])
        miss_rewards = grouped_miss_rewards.get(arm_id, [])
        if goal_rewards:
            add(
                value=min(goal_rewards),
                source_metric="total_reward",
                source_arm=arm_id,
                source_quantile="min_goal_reached",
                construction_reason="minimum observed successful episode return",
            )
        if goal_rewards and miss_rewards:
            add(
                value=(max(miss_rewards) + min(goal_rewards)) / 2.0,
                source_metric="total_reward",
                source_arm=arm_id,
                source_quantile="failure_success_midpoint",
                construction_reason=(
                    "midpoint between best observed miss and weakest observed success"
                ),
            )

    add(
        value=structural_context.random_policy_mean_reward,
        source_metric="random_policy_mean_total_reward",
        source_arm="stage1_random_policy_recon",
        source_quantile="mean",
        construction_reason="Stage 1 random policy reward context",
    )
    add(
        value=structural_context.total_shortest_path_reward,
        source_metric="shortest_path_total_reward",
        source_arm="stage1_shortest_path_anchor",
        source_quantile="anchor",
        construction_reason="Stage 1 shortest valid path reward context",
    )
    return rows


def _quantile(sorted_values: list[float], quantile: float) -> float:
    if not sorted_values:
        raise ValueError("cannot build threshold quantile from empty values")
    if len(sorted_values) == 1:
        return sorted_values[0]
    position = quantile * (len(sorted_values) - 1)
    lower_index = int(position)
    upper_index = min(lower_index + 1, len(sorted_values) - 1)
    fraction = position - lower_index
    return sorted_values[lower_index] * (1.0 - fraction) + sorted_values[upper_index] * fraction


def _truthy(value: object) -> bool:
    return str(value).strip().lower() in {"1", "true", "yes"}
