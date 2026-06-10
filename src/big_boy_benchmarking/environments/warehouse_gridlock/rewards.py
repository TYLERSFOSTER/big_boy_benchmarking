"""Reward policies for Warehouse Gridlock."""

from __future__ import annotations

from collections.abc import Mapping
from dataclasses import dataclass

from big_boy_benchmarking.environments.warehouse_gridlock.graph import GridNode
from big_boy_benchmarking.environments.warehouse_gridlock.ids import (
    WAREHOUSE_GRIDLOCK_REWARD_POLICY_ID,
)
from big_boy_benchmarking.environments.warehouse_gridlock.state import (
    WarehouseGridlockState,
)

DIAGNOSTIC_NO_REWARD_ID = "warehouse_gridlock_diagnostic_no_reward_v001"


@dataclass(frozen=True)
class RewardPolicy:
    reward_policy_id: str = WAREHOUSE_GRIDLOCK_REWARD_POLICY_ID
    terminal_success_reward: float = 1000.0
    elapsed_time_penalty_per_second: float = -1.0
    correct_box_reward: float = 1.0
    correct_robot_reward: float = 1.0
    invalid_action_penalty: float = 0.0

    def to_dict(self) -> dict[str, object]:
        return {
            "reward_policy_id": self.reward_policy_id,
            "terminal_success_reward": self.terminal_success_reward,
            "elapsed_time_penalty_per_second": self.elapsed_time_penalty_per_second,
            "correct_box_reward": self.correct_box_reward,
            "correct_robot_reward": self.correct_robot_reward,
            "invalid_action_penalty": self.invalid_action_penalty,
        }


def is_terminal(
    state: WarehouseGridlockState,
    *,
    robot_targets: Mapping[str, GridNode],
    box_targets: Mapping[str, GridNode],
) -> bool:
    return all(
        state.robot_positions[key] == target for key, target in robot_targets.items()
    ) and all(state.box_positions[key] == target for key, target in box_targets.items())


def target_counts(
    state: WarehouseGridlockState,
    *,
    robot_targets: Mapping[str, GridNode],
    box_targets: Mapping[str, GridNode],
) -> dict[str, int]:
    correct_robots = sum(
        1 for key, target in robot_targets.items() if state.robot_positions[key] == target
    )
    correct_boxes = sum(
        1 for key, target in box_targets.items() if state.box_positions[key] == target
    )
    return {
        "correct_robot_count": correct_robots,
        "correct_box_count": correct_boxes,
        "misplaced_robot_count": len(robot_targets) - correct_robots,
        "misplaced_box_count": len(box_targets) - correct_boxes,
    }


def compute_reward(
    *,
    state: WarehouseGridlockState,
    robot_targets: Mapping[str, GridNode],
    box_targets: Mapping[str, GridNode],
    policy: RewardPolicy,
    valid_transition: bool,
    reward_mode_id: str | None = None,
) -> float:
    if reward_mode_id == DIAGNOSTIC_NO_REWARD_ID:
        return 0.0
    counts = target_counts(state, robot_targets=robot_targets, box_targets=box_targets)
    reward = (
        counts["correct_box_count"] * policy.correct_box_reward
        + counts["correct_robot_count"] * policy.correct_robot_reward
    )
    if valid_transition:
        reward += policy.elapsed_time_penalty_per_second
    else:
        reward += policy.invalid_action_penalty
    if is_terminal(state, robot_targets=robot_targets, box_targets=box_targets):
        reward += policy.terminal_success_reward
    return float(reward)
