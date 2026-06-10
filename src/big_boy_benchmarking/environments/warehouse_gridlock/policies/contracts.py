"""Full-state/full-action policy contract for Warehouse Gridlock."""

from __future__ import annotations

from collections.abc import Mapping
from dataclasses import dataclass, field
from typing import Any

from big_boy_benchmarking.environments.warehouse_gridlock.actions import (
    DirectionOrStay,
    WarehouseGridlockAction,
    validate_action,
)
from big_boy_benchmarking.environments.warehouse_gridlock.graph import GridNode
from big_boy_benchmarking.environments.warehouse_gridlock.instances import (
    WarehouseGridlockInstance,
)
from big_boy_benchmarking.environments.warehouse_gridlock.rewards import target_counts
from big_boy_benchmarking.environments.warehouse_gridlock.state import WarehouseGridlockState
from big_boy_benchmarking.environments.warehouse_gridlock.transition import (
    WarehouseGridlockStepResult,
)
from big_boy_benchmarking.environments.warehouse_gridlock.policies.serialization import (
    stable_hash,
)

POLICY_CONTRACT_ID = "warehouse_full_state_full_action_policy_contract_v001"


def _node_key(node: GridNode) -> str:
    return node.key


@dataclass(frozen=True)
class WarehouseStaticSystemConfig:
    environment_instance_id: str
    grid_dimensions: tuple[int, int]
    traversable_nodes: tuple[str, ...]
    blocked_nodes: tuple[str, ...]
    traversable_edges: tuple[tuple[str, str], ...]
    robot_ids: tuple[str, ...]
    box_ids: tuple[str, ...]
    robot_target_map: Mapping[str, str]
    box_target_map: Mapping[str, str]
    reward_constants: Mapping[str, float | str]
    max_seconds_per_episode: int

    def to_dict(self) -> dict[str, object]:
        return {
            "environment_instance_id": self.environment_instance_id,
            "grid_dimensions": list(self.grid_dimensions),
            "traversable_nodes": list(self.traversable_nodes),
            "blocked_nodes": list(self.blocked_nodes),
            "traversable_edges": [list(edge) for edge in self.traversable_edges],
            "robot_ids": list(self.robot_ids),
            "box_ids": list(self.box_ids),
            "robot_target_map": dict(sorted(self.robot_target_map.items())),
            "box_target_map": dict(sorted(self.box_target_map.items())),
            "reward_constants": dict(sorted(self.reward_constants.items())),
            "max_seconds_per_episode": self.max_seconds_per_episode,
        }


@dataclass(frozen=True)
class WarehouseDynamicSystemConfig:
    state_id: str
    time_step: int
    robot_positions: Mapping[str, str]
    box_positions: Mapping[str, str]
    current_target_counts: Mapping[str, int]
    terminal: bool = False

    def to_dict(self) -> dict[str, object]:
        return {
            "state_id": self.state_id,
            "time_step": self.time_step,
            "robot_positions": dict(sorted(self.robot_positions.items())),
            "box_positions": dict(sorted(self.box_positions.items())),
            "current_target_counts": dict(sorted(self.current_target_counts.items())),
            "terminal": self.terminal,
        }


@dataclass(frozen=True)
class WarehouseFullSystemConfig:
    static: WarehouseStaticSystemConfig
    dynamic: WarehouseDynamicSystemConfig

    def to_dict(self) -> dict[str, object]:
        return {"static": self.static.to_dict(), "dynamic": self.dynamic.to_dict()}

    @property
    def stable_hash(self) -> str:
        return stable_hash(self.to_dict())


@dataclass(frozen=True)
class WarehouseActionVectorValidation:
    ok: bool
    errors: tuple[str, ...]


@dataclass(frozen=True)
class WarehouseFullActionVector:
    commands: Mapping[str, DirectionOrStay]

    def to_action(self) -> WarehouseGridlockAction:
        return WarehouseGridlockAction(commands=dict(self.commands))

    def to_dict(self) -> dict[str, str]:
        return {robot_id: command.value for robot_id, command in sorted(self.commands.items())}

    @property
    def stable_id(self) -> str:
        return self.to_action().stable_id

    @property
    def stable_hash(self) -> str:
        return stable_hash(self.to_dict())

    def validate(self, *, required_robot_ids: tuple[str, ...]) -> WarehouseActionVectorValidation:
        report = validate_action(self.to_action(), required_robot_ids=required_robot_ids)
        return WarehouseActionVectorValidation(ok=report.ok, errors=report.errors)

    @classmethod
    def all_stay(cls, robot_ids: tuple[str, ...]) -> WarehouseFullActionVector:
        return cls(commands={robot_id: DirectionOrStay.STAY for robot_id in robot_ids})

    @classmethod
    def from_action(cls, action: WarehouseGridlockAction) -> WarehouseFullActionVector:
        return cls(commands=dict(action.commands))


@dataclass(frozen=True)
class WarehousePolicyRng:
    seed: int


@dataclass(frozen=True)
class WarehouseMaskContext:
    arm_id: str
    run_id: str
    episode_index: int
    step_index: int
    max_seconds_per_episode: int
    projection_attempt_budget: int


@dataclass(frozen=True)
class WarehouseProjectionTrace:
    projection_strategy_id: str
    projection_attempt_budget: int
    attempt_count: int
    raw_valid: bool
    selected_valid: bool
    fallback_used: bool
    invalid_reasons_seen: tuple[str, ...]
    selected_reason: str
    successor_out_count_used_for_selection: bool = False

    def to_row(self) -> dict[str, object]:
        return {
            "projection_strategy_id": self.projection_strategy_id,
            "projection_attempt_budget": self.projection_attempt_budget,
            "projection_attempt_count": self.attempt_count,
            "raw_valid": self.raw_valid,
            "selected_valid": self.selected_valid,
            "fallback_used": self.fallback_used,
            "invalid_reasons_seen": "|".join(self.invalid_reasons_seen),
            "selected_reason": self.selected_reason,
            "successor_out_count_used_for_selection": self.successor_out_count_used_for_selection,
        }


@dataclass(frozen=True)
class WarehousePolicyDecision:
    policy_id: str
    model_family_id: str
    second: int
    raw_action_vector: WarehouseFullActionVector
    selected_action_vector: WarehouseFullActionVector | None
    raw_valid: bool
    selected_valid: bool
    projection_trace: WarehouseProjectionTrace | None
    prior_signal_used: bool
    decision_score_summary: Mapping[str, float | int | str] = field(default_factory=dict)
    robot_command_margins: Mapping[str, float] = field(default_factory=dict)
    tier: int | None = None
    tier_state_id: str | None = None

    @property
    def raw_action_vector_hash(self) -> str:
        return self.raw_action_vector.stable_hash

    @property
    def selected_action_vector_hash(self) -> str:
        if self.selected_action_vector is None:
            return ""
        return self.selected_action_vector.stable_hash

    def to_event_row(self, *, run_id: str, arm_id: str, episode_index: int, step_index: int) -> dict[str, object]:
        return {
            "run_id": run_id,
            "arm_id": arm_id,
            "episode_index": episode_index,
            "step_index": step_index,
            "second": self.second,
            "policy_id": self.policy_id,
            "model_family_id": self.model_family_id,
            "raw_action_vector_hash": self.raw_action_vector_hash,
            "selected_action_vector_hash": self.selected_action_vector_hash,
            "raw_valid": self.raw_valid,
            "selected_valid": self.selected_valid,
            "projection_attempt_count": (
                self.projection_trace.attempt_count if self.projection_trace else 0
            ),
            "projection_strategy_id": (
                self.projection_trace.projection_strategy_id if self.projection_trace else ""
            ),
            "prior_signal_used": self.prior_signal_used,
            "tier": "" if self.tier is None else self.tier,
            "tier_state_id": self.tier_state_id or "",
            "decision_score_summary": stable_hash(dict(self.decision_score_summary)),
        }


@dataclass(frozen=True)
class WarehousePolicyTransition:
    pre_config: WarehouseFullSystemConfig
    pre_second: int
    selected_full_action_vector: WarehouseFullActionVector
    projection_trace: WarehouseProjectionTrace
    reward: float
    post_config: WarehouseFullSystemConfig
    post_second: int
    terminated: bool
    truncated: bool
    episode_index: int
    step_index: int
    step_result: WarehouseGridlockStepResult


@dataclass(frozen=True)
class WarehousePolicyUpdate:
    policy_id: str
    model_family_id: str
    parameter_state_hash_before: str
    parameter_state_hash_after: str
    update_norm_or_change_count: float
    non_noop_update: bool
    reward_signal_used: float
    progress_signal_used: float

    def to_event_row(self, *, run_id: str, arm_id: str, episode_index: int, step_index: int) -> dict[str, object]:
        return {
            "run_id": run_id,
            "arm_id": arm_id,
            "episode_index": episode_index,
            "step_index": step_index,
            "policy_id": self.policy_id,
            "model_family_id": self.model_family_id,
            "parameter_state_hash_before": self.parameter_state_hash_before,
            "parameter_state_hash_after": self.parameter_state_hash_after,
            "update_norm_or_change_count": self.update_norm_or_change_count,
            "non_noop_update": self.non_noop_update,
            "reward_signal_used": self.reward_signal_used,
            "progress_signal_used": self.progress_signal_used,
        }


def config_from_instance_state(
    *,
    instance: WarehouseGridlockInstance,
    state: WarehouseGridlockState,
    max_seconds_per_episode: int,
) -> WarehouseFullSystemConfig:
    manifest = instance.manifest
    graph = instance.graph
    traversable_nodes = tuple(sorted(node.key for node in graph.nodes - graph.blocked_nodes))
    blocked_nodes = tuple(sorted(node.key for node in graph.blocked_nodes))
    traversable_edges = tuple(
        sorted((source.key, target.key) for source, target in graph.edges)
    )
    reward = manifest.reward_policy
    static = WarehouseStaticSystemConfig(
        environment_instance_id=manifest.instance_id,
        grid_dimensions=(manifest.grid.rows, manifest.grid.cols),
        traversable_nodes=traversable_nodes,
        blocked_nodes=blocked_nodes,
        traversable_edges=traversable_edges,
        robot_ids=tuple(sorted(manifest.robot_ids)),
        box_ids=tuple(sorted(manifest.box_ids)),
        robot_target_map={
            robot_id: _node_key(node) for robot_id, node in sorted(manifest.robot_target_map().items())
        },
        box_target_map={
            box_id: _node_key(node) for box_id, node in sorted(manifest.box_target_map().items())
        },
        reward_constants=reward.to_dict(),
        max_seconds_per_episode=max_seconds_per_episode,
    )
    counts = target_counts(
        state,
        robot_targets=manifest.robot_target_map(),
        box_targets=manifest.box_target_map(),
    )
    dynamic = WarehouseDynamicSystemConfig(
        state_id=state.stable_id,
        time_step=state.time_step,
        robot_positions={
            robot_id: _node_key(node) for robot_id, node in sorted(state.robot_positions.items())
        },
        box_positions={box_id: _node_key(node) for box_id, node in sorted(state.box_positions.items())},
        current_target_counts={key: int(value) for key, value in sorted(counts.items())},
        terminal=all(
            state.robot_positions[key] == target
            for key, target in manifest.robot_target_map().items()
        )
        and all(
            state.box_positions[key] == target for key, target in manifest.box_target_map().items()
        ),
    )
    return WarehouseFullSystemConfig(static=static, dynamic=dynamic)
