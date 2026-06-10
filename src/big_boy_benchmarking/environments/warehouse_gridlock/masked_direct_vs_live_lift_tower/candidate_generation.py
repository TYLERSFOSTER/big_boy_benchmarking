"""Bounded candidate generation for Warehouse Gridlock diagnostic arms."""

from __future__ import annotations

import hashlib
import math
import random
from dataclasses import dataclass, field
from typing import Any

from big_boy_benchmarking.environments.warehouse_gridlock.actions import (
    DirectionOrStay,
    WarehouseGridlockAction,
)
from big_boy_benchmarking.environments.warehouse_gridlock.instances import (
    WarehouseGridlockInstance,
)
from big_boy_benchmarking.environments.warehouse_gridlock.state import (
    WarehouseGridlockState,
)
from big_boy_benchmarking.environments.warehouse_gridlock.transition import (
    action_from_overrides,
)
from big_boy_benchmarking.environments.warehouse_gridlock.masked_direct_vs_live_lift_tower.config import (
    CANDIDATE_MIX_COORDINATION_READY,
    DEFAULT_MAX_ACTIVE_ROBOTS,
    DIRECT_CANDIDATE_POLICY_ID,
    TOWER_CANDIDATE_POLICY_ID,
)

MOVE_COMMANDS = (
    DirectionOrStay.NORTH,
    DirectionOrStay.SOUTH,
    DirectionOrStay.EAST,
    DirectionOrStay.WEST,
)

CANDIDATE_FAMILY_ALL_STAY = "all_stay"
CANDIDATE_FAMILY_ONE_ACTIVE = "one_active"
CANDIDATE_FAMILY_TWO_ACTIVE = "two_active"
CANDIDATE_FAMILY_THREE_ACTIVE = "three_active"
CANDIDATE_FAMILY_MULTI_ACTIVE = "multi_active"


@dataclass(frozen=True)
class DirectActionCandidate:
    candidate_id: str
    action: WarehouseGridlockAction
    rank: int
    policy_id: str = DIRECT_CANDIDATE_POLICY_ID
    generation_scope: str = "coordination_ready_sparse_generated_candidate_set"
    generation_budget: int = 0
    generation_seed: int = 0
    generation_complete_for_scope: bool = True
    metadata: dict[str, Any] = field(default_factory=dict)

    @property
    def active_robot_count(self) -> int:
        return sum(1 for command in self.action.commands.values() if command != DirectionOrStay.STAY)

    @property
    def is_all_stay(self) -> bool:
        return self.active_robot_count == 0

    def action_summary(self) -> str:
        active = [
            f"{robot_id}:{command.value}"
            for robot_id, command in sorted(self.action.commands.items())
            if command != DirectionOrStay.STAY
        ]
        return "all_stay" if not active else "|".join(active)

    def to_event_row(
        self,
        *,
        run_id: str,
        arm_id: str,
        episode_index: int,
        step_index: int,
        state: WarehouseGridlockState,
    ) -> dict[str, object]:
        return {
            "run_id": run_id,
            "arm_id": arm_id,
            "episode_index": episode_index,
            "step_index": step_index,
            "state_id": state.stable_id,
            "candidate_id": self.candidate_id,
            "candidate_generation_policy_id": self.policy_id,
            "candidate_generation_scope": self.generation_scope,
            "candidate_generation_budget": self.generation_budget,
            "candidate_rank": self.rank,
            "candidate_action_id": self.action.stable_id,
            "candidate_action_summary": self.action_summary(),
            "is_all_stay": self.is_all_stay,
            "active_robot_count": self.active_robot_count,
            "candidate_family": self.metadata.get("candidate_family", ""),
            "candidate_mix_id": self.metadata.get("candidate_mix_id", ""),
            "max_active_robots": self.metadata.get("max_active_robots", ""),
            "generation_complete_for_scope": self.generation_complete_for_scope,
        }


@dataclass(frozen=True)
class TowerLiftCandidate:
    candidate_id: str
    downstairs_state_id: str
    lift_state: WarehouseGridlockState
    tier: int
    state_cell_id: str
    out_count: int
    out_scope: str
    policy_id: str = TOWER_CANDIDATE_POLICY_ID

    @property
    def live(self) -> bool:
        return self.out_count > 0


@dataclass(frozen=True)
class TowerActionCandidate:
    candidate_id: str
    tier: int
    state_cell_id: str
    action_cell_id: str
    concrete_candidate: DirectActionCandidate
    rank: int
    policy_id: str = TOWER_CANDIDATE_POLICY_ID
    generation_scope: str = "current_tower_action_candidate_set"
    generation_complete_for_scope: bool = True


@dataclass(frozen=True)
class TowerConcreteRealizationCandidate:
    candidate_id: str
    tower_action_candidate_id: str
    concrete_candidate: DirectActionCandidate
    rank: int
    generation_scope: str = "current_concrete_realization_candidate_set"


@dataclass(frozen=True)
class CandidateGenerationReport:
    policy_id: str
    generation_scope: str
    generation_budget: int
    generation_seed: int
    candidate_count_before_mask: int
    generation_complete_for_scope: bool
    full_action_surface_complete: bool = False

    def to_manifest(self) -> dict[str, object]:
        return {
            "policy_id": self.policy_id,
            "generation_scope": self.generation_scope,
            "generation_budget": self.generation_budget,
            "generation_seed": self.generation_seed,
            "candidate_count_before_mask": self.candidate_count_before_mask,
            "generation_complete_for_scope": self.generation_complete_for_scope,
            "complete_full_action_surface": self.full_action_surface_complete,
        }


def generate_direct_candidates(
    *,
    instance: WarehouseGridlockInstance,
    state: WarehouseGridlockState,
    budget: int,
    seed: int,
    max_active_robots: int = DEFAULT_MAX_ACTIVE_ROBOTS,
    candidate_mix_id: str = CANDIDATE_MIX_COORDINATION_READY,
) -> list[DirectActionCandidate]:
    """Generate a bounded sparse, coordination-ready ensemble-action set.

    The current `state` participates in the stable candidate ids. It does not
    affect the generation rule beyond identity; validity is handled by the
    admissibility layer.
    """

    if budget < 1:
        return []
    robot_ids = tuple(sorted(instance.manifest.robot_ids))
    max_active = max(0, min(max_active_robots, len(robot_ids)))
    candidates: list[tuple[WarehouseGridlockAction, str]] = [
        (
            action_from_overrides(robot_ids, {}),
            CANDIDATE_FAMILY_ALL_STAY,
        ),
    ]

    if max_active == 0 or len(candidates) >= budget:
        return _wrap_direct_candidates(
            candidates=candidates,
            state=state,
            budget=budget,
            seed=seed,
            complete=max_active == 0,
            max_active_robots=max_active,
            candidate_mix_id=candidate_mix_id,
        )

    if candidate_mix_id != CANDIDATE_MIX_COORDINATION_READY:
        raise ValueError(f"unsupported Warehouse candidate mix: {candidate_mix_id}")

    per_family_pool_size = max(budget * 4, 32)
    pools = [
        _candidate_pool_for_active_count(
            robot_ids=robot_ids,
            state=state,
            seed=seed,
            active_count=active_count,
            limit=per_family_pool_size,
        )
        for active_count in range(1, max_active + 1)
    ]
    cursors = [0 for _ in pools]
    seen_action_ids = {candidates[0][0].stable_id}

    while len(candidates) < budget and any(cursor < len(pool) for cursor, pool in zip(cursors, pools)):
        for index, pool in enumerate(pools):
            if len(candidates) >= budget:
                break
            if cursors[index] >= len(pool):
                continue
            action, family = pool[cursors[index]]
            cursors[index] += 1
            if action.stable_id in seen_action_ids:
                continue
            seen_action_ids.add(action.stable_id)
            candidates.append((action, family))

    complete = _active_count_surface_size(robot_count=len(robot_ids), max_active=max_active) <= len(candidates)
    return _wrap_direct_candidates(
        candidates=candidates,
        state=state,
        budget=budget,
        seed=seed,
        complete=complete,
        max_active_robots=max_active,
        candidate_mix_id=candidate_mix_id,
    )


def tower_action_candidates_from_direct(
    *,
    direct_candidates: list[DirectActionCandidate],
    tier: int,
    state_cell_id: str,
    budget: int,
) -> list[TowerActionCandidate]:
    tower_candidates: list[TowerActionCandidate] = []
    for rank, direct_candidate in enumerate(direct_candidates[:budget]):
        action_cell_id = tower_action_cell_id(direct_candidate)
        tower_candidates.append(
            TowerActionCandidate(
                candidate_id=_stable_id(
                    "tower-action",
                    str(tier),
                    state_cell_id,
                    direct_candidate.candidate_id,
                ),
                tier=tier,
                state_cell_id=state_cell_id,
                action_cell_id=action_cell_id,
                concrete_candidate=direct_candidate,
                rank=rank,
                generation_complete_for_scope=len(direct_candidates) <= budget,
            )
        )
    return tower_candidates


def tower_action_cell_id(candidate: DirectActionCandidate) -> str:
    active = [
        command.value
        for _, command in sorted(candidate.action.commands.items())
        if command != DirectionOrStay.STAY
    ]
    if not active:
        return "tower_action_cell:all_stay"
    return "tower_action_cell:active_count={}:commands={}".format(
        len(active),
        ",".join(sorted(active)),
    )


def _wrap_direct_candidates(
    *,
    candidates: list[tuple[WarehouseGridlockAction, str]],
    state: WarehouseGridlockState,
    budget: int,
    seed: int,
    complete: bool,
    max_active_robots: int,
    candidate_mix_id: str,
) -> list[DirectActionCandidate]:
    wrapped: list[DirectActionCandidate] = []
    for rank, (action, family) in enumerate(candidates[:budget]):
        wrapped.append(
            DirectActionCandidate(
                candidate_id=_stable_id("direct", state.stable_id, str(rank), action.stable_id),
                action=action,
                rank=rank,
                generation_budget=budget,
                generation_seed=seed,
                generation_complete_for_scope=complete,
                metadata={
                    "candidate_family": family,
                    "candidate_mix_id": candidate_mix_id,
                    "max_active_robots": max_active_robots,
                },
            )
        )
    return wrapped


def _candidate_pool_for_active_count(
    *,
    robot_ids: tuple[str, ...],
    state: WarehouseGridlockState,
    seed: int,
    active_count: int,
    limit: int,
) -> list[tuple[WarehouseGridlockAction, str]]:
    if active_count == 1:
        return [
            (action_from_overrides(robot_ids, {robot_id: command}), CANDIDATE_FAMILY_ONE_ACTIVE)
            for robot_id in robot_ids
            for command in MOVE_COMMANDS
        ][:limit]

    family = _candidate_family_for_active_count(active_count)
    rng = random.Random(
        f"warehouse-active-count:{active_count}:{seed}:{state.stable_id}"
    )
    pool: list[tuple[WarehouseGridlockAction, str]] = []
    seen_action_ids: set[str] = set()
    attempts = 0
    max_attempts = max(limit * 50, 256)
    while len(pool) < limit and attempts < max_attempts:
        attempts += 1
        robot_tuple = tuple(sorted(rng.sample(robot_ids, active_count)))
        commands = tuple(rng.choice(MOVE_COMMANDS) for _ in range(active_count))
        overrides = dict(zip(robot_tuple, commands, strict=True))
        action = action_from_overrides(robot_ids, overrides)
        if action.stable_id in seen_action_ids:
            continue
        seen_action_ids.add(action.stable_id)
        pool.append((action, family))
    return pool


def _candidate_family_for_active_count(active_count: int) -> str:
    if active_count == 2:
        return CANDIDATE_FAMILY_TWO_ACTIVE
    if active_count == 3:
        return CANDIDATE_FAMILY_THREE_ACTIVE
    return CANDIDATE_FAMILY_MULTI_ACTIVE


def _active_count_surface_size(*, robot_count: int, max_active: int) -> int:
    return 1 + sum(
        math.comb(robot_count, active_count) * (len(MOVE_COMMANDS) ** active_count)
        for active_count in range(1, max_active + 1)
    )


def _stable_id(*parts: str) -> str:
    digest = hashlib.sha256("||".join(parts).encode("utf-8")).hexdigest()[:16]
    return f"{parts[0]}-{digest}"
