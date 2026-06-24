"""state_collapser-backed decision surfaces for Warehouse full-tower PPO."""

from __future__ import annotations

from dataclasses import dataclass
from typing import Any

from state_collapser.core.edges import BaseEdge
from state_collapser.core.state import State
from state_collapser.tower.partition.tower import PartitionTower

from big_boy_benchmarking.environments.warehouse_gridlock.instances import (
    WarehouseGridlockInstance,
)
from big_boy_benchmarking.environments.warehouse_gridlock.masked_direct_vs_live_lift_tower.admissibility import (
    mask_direct_candidates,
)
from big_boy_benchmarking.environments.warehouse_gridlock.masked_direct_vs_live_lift_tower.candidate_generation import (
    DirectActionCandidate,
    generate_direct_candidates,
)
from big_boy_benchmarking.environments.warehouse_gridlock.masked_direct_vs_live_lift_tower.warehouse_tower_adapter import (
    WarehouseGeneratedEdge,
    core_state_to_warehouse_state,
    primitive_action_to_warehouse_action,
    warehouse_edge_to_base_edge,
    warehouse_state_to_core_state,
)
from big_boy_benchmarking.environments.warehouse_gridlock.state import (
    WarehouseGridlockState,
)

from .config import WarehouseFullTowerPPOArmConfig, WarehouseFullTowerPPOConfig
from .ids import (
    WAREHOUSE_GRIDLOCK_POINTWISE_LIFTABILITY_SEMANTICS_ID,
    WAREHOUSE_GRIDLOCK_TIER_DIRECTION_CONVENTION,
)
from .schema_arms import schema_for_arm


@dataclass(frozen=True)
class PointwiseActionChoice:
    local_index: int
    tier_index: int
    state_cell_id: str
    action_cell_id: str
    executable_edges: tuple[BaseEdge, ...]
    representative_edges: tuple[BaseEdge, ...]

    @property
    def executable_lift_count(self) -> int:
        return len(self.executable_edges)

    @property
    def candidate_lift_count(self) -> int:
        return len(self.representative_edges)

    @property
    def selected_edge(self) -> BaseEdge:
        if not self.executable_edges:
            raise ValueError("cannot select edge from empty executable lift set")
        return self.executable_edges[0]

    @property
    def action_id(self) -> str:
        action = primitive_action_to_warehouse_action(self.selected_edge.action)
        return action.stable_id

    @property
    def target_state(self) -> WarehouseGridlockState:
        return core_state_to_warehouse_state(self.selected_edge.target)


@dataclass(frozen=True)
class WarehouseDecisionSurface:
    arm_id: str
    schema_id: str
    schema_seed: int
    current_state: WarehouseGridlockState
    current_base_state: State
    partition_tower: PartitionTower
    tier_index: int
    state_cell_id: str
    current_position_at_every_tier: tuple[str | None, ...]
    action_choices: tuple[PointwiseActionChoice, ...]
    valid_edges: tuple[WarehouseGeneratedEdge, ...]
    direct_candidates: tuple[DirectActionCandidate, ...]
    generated_candidate_count: int
    valid_candidate_count: int
    invalid_candidate_count: int
    candidate_generation_complete: bool
    surface_scope: str = "generated_discovered_surface"
    mask_kind: str = "pointwise_executable"
    semantics_id: str = WAREHOUSE_GRIDLOCK_POINTWISE_LIFTABILITY_SEMANTICS_ID

    @property
    def actor_callable(self) -> bool:
        return bool(self.action_choices)

    @property
    def candidate_action_ids(self) -> tuple[str, ...]:
        return tuple(choice.action_cell_id for choice in self.action_choices)

    @property
    def candidate_mask(self) -> tuple[bool, ...]:
        return tuple(True for _ in self.action_choices)

    def to_summary_row(self, *, run_id: str, episode_index: int, step_index: int) -> dict[str, object]:
        return {
            "run_id": run_id,
            "arm_id": self.arm_id,
            "episode_index": episode_index,
            "step_index": step_index,
            "schema_id": self.schema_id,
            "schema_seed": self.schema_seed,
            "tier_index": self.tier_index,
            "state_cell_id": self.state_cell_id,
            "candidate_action_count": len(self.action_choices),
            "generated_candidate_count": self.generated_candidate_count,
            "valid_candidate_count": self.valid_candidate_count,
            "invalid_candidate_count": self.invalid_candidate_count,
            "surface_scope": self.surface_scope,
            "mask_kind": self.mask_kind,
            "semantics_id": self.semantics_id,
            "tier_direction_convention": WAREHOUSE_GRIDLOCK_TIER_DIRECTION_CONVENTION,
            "current_position_at_every_tier": "|".join(
                "" if item is None else str(item)
                for item in self.current_position_at_every_tier
            ),
        }


def build_decision_surface(
    *,
    instance: WarehouseGridlockInstance,
    state: WarehouseGridlockState,
    arm: WarehouseFullTowerPPOArmConfig,
    config: WarehouseFullTowerPPOConfig,
    schema_seed: int,
    generation_seed: int,
) -> WarehouseDecisionSurface:
    direct_candidates = generate_direct_candidates(
        instance=instance,
        state=state,
        budget=config.candidate_proposals_per_step,
        seed=generation_seed,
        max_active_robots=config.max_active_robots,
        candidate_mix_id=config.candidate_mix_id,
    )
    mask_result = mask_direct_candidates(
        instance=instance,
        state=state,
        candidates=direct_candidates,
        max_seconds=config.max_seconds_per_episode,
    )
    by_id = {candidate.candidate_id: candidate for candidate in direct_candidates}
    valid_edges: list[WarehouseGeneratedEdge] = []
    for query in mask_result.query_results:
        if not query.valid:
            continue
        candidate = by_id[query.candidate_id]
        valid_edges.append(
            WarehouseGeneratedEdge(
                source=state,
                action=candidate.action,
                target=query.result.next_state,
                reward=query.result.reward,
                labels=(
                    "warehouse_gridlock_full_tower_ppo_transition",
                    ("arm_id", arm.arm_id),
                    ("schema_id", arm.schema_id),
                    ("valid_transition", True),
                ),
            )
        )
    base_state = warehouse_state_to_core_state(state)
    tower = PartitionTower(schema=schema_for_arm(arm, schema_seed=schema_seed))
    base_edges = tuple(warehouse_edge_to_base_edge(edge) for edge in valid_edges)
    initial_states_by_id: dict[object, State] = {base_state.canonical_identity: base_state}
    for edge in base_edges:
        initial_states_by_id[edge.target.canonical_identity] = edge.target
    tower.initialize(
        initial_states=tuple(initial_states_by_id.values()),
        initial_edges=base_edges,
        current_state=base_state,
    )
    tier_index, state_cell_id, action_choices = _deepest_pointwise_surface(
        tower=tower,
        current_base_state=base_state,
    )
    position = tuple(None if item is None else str(item) for item in tower.current_position_at_every_tier(base_state))
    return WarehouseDecisionSurface(
        arm_id=arm.arm_id,
        schema_id=arm.schema_id,
        schema_seed=schema_seed,
        current_state=state,
        current_base_state=base_state,
        partition_tower=tower,
        tier_index=tier_index,
        state_cell_id="" if state_cell_id is None else str(state_cell_id),
        current_position_at_every_tier=position,
        action_choices=tuple(action_choices),
        valid_edges=tuple(valid_edges),
        direct_candidates=tuple(direct_candidates),
        generated_candidate_count=len(direct_candidates),
        valid_candidate_count=len(valid_edges),
        invalid_candidate_count=mask_result.inadmissible_count,
        candidate_generation_complete=all(
            candidate.generation_complete_for_scope for candidate in direct_candidates
        ),
    )


def selected_warehouse_action(choice: PointwiseActionChoice) -> Any:
    return primitive_action_to_warehouse_action(choice.selected_edge.action)


def selected_next_state(choice: PointwiseActionChoice) -> WarehouseGridlockState:
    return core_state_to_warehouse_state(choice.selected_edge.target)


def _deepest_pointwise_surface(
    *,
    tower: PartitionTower,
    current_base_state: State,
) -> tuple[int, Any, list[PointwiseActionChoice]]:
    for tier in reversed(range(len(tower.state_layers))):
        if not tower.tier_is_executable_from_state(tier, current_base_state):
            continue
        state_cell_id = tower.current_state_cell(tier, current_base_state)
        if state_cell_id is None:
            continue
        action_cell_ids = tower.executable_action_cells(
            tier,
            state_cell_id,
            current_base_state,
        )
        choices: list[PointwiseActionChoice] = []
        for index, action_cell_id in enumerate(action_cell_ids):
            executable = tuple(
                tower.executable_lift_candidates(tier, action_cell_id, current_base_state)
            )
            if not executable:
                continue
            choices.append(
                PointwiseActionChoice(
                    local_index=index,
                    tier_index=tier,
                    state_cell_id=str(state_cell_id),
                    action_cell_id=str(action_cell_id),
                    executable_edges=executable,
                    representative_edges=tuple(tower.representative_edges(tier, action_cell_id)),
                )
            )
        if choices:
            return tier, state_cell_id, choices
    return 0, None, []
