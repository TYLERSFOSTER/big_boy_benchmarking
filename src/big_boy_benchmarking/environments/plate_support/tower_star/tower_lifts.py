"""Tower-star lift-candidate surfaces for PlateSupport."""

from __future__ import annotations

import random
from dataclasses import dataclass
from typing import Any

from big_boy_benchmarking.environments.plate_support.standard_gauntlet.tower_training_health.training_surfaces import (
    cell_text,
    state_payload_text,
)

from .config import CURRENT_LIFT_EXECUTABLE_GUARD, INVALID_GUARD, NONSELF_GUARD
from .guards import classify_primitive_transition


@dataclass(frozen=True)
class TowerLiftCandidate:
    """One executable concrete lift candidate inside a quotient action cell."""

    tier: int
    state_cell_id: Any
    action_cell_id: Any
    edge_id: str
    action_index: int
    source_state_id: str
    next_state_id: str
    primitive_invalid_move: bool
    primitive_self_loop: bool
    primitive_valid_clipped_self_loop: bool
    primitive_nonself_transition: bool
    invalid_guard_compatible: bool
    nonself_guard_compatible: bool
    edge: Any


@dataclass(frozen=True)
class TowerActionCellSurface:
    """Pre-star and post-star lift pool for one tower action cell."""

    tier: int
    state_cell_id: Any
    action_cell_id: Any
    candidate_lift_count: int
    executable_lift_count: int
    lifts: tuple[TowerLiftCandidate, ...]

    @property
    def invalid_guard_lifts(self) -> tuple[TowerLiftCandidate, ...]:
        return tuple(lift for lift in self.lifts if lift.invalid_guard_compatible)

    @property
    def nonself_guard_lifts(self) -> tuple[TowerLiftCandidate, ...]:
        return tuple(lift for lift in self.lifts if lift.nonself_guard_compatible)

    def guarded_lifts(self, guard_type: str) -> tuple[TowerLiftCandidate, ...]:
        if guard_type == CURRENT_LIFT_EXECUTABLE_GUARD:
            return self.lifts
        if guard_type == INVALID_GUARD:
            return self.invalid_guard_lifts
        if guard_type == NONSELF_GUARD:
            return self.nonself_guard_lifts
        raise ValueError(f"unknown tower guard_type: {guard_type!r}")


@dataclass(frozen=True)
class TowerStarActionChoice:
    """One tower action cell after arm-specific star filtering."""

    tier: int
    state_cell_id: Any
    action_cell_id: Any
    action_index: int
    candidate_lift_count: int
    executable_lift_count: int
    guarded_lift_count: int
    selected_lift: TowerLiftCandidate
    selected_edge: Any
    q_key: tuple[str, str, str]
    q_value: float
    surface: TowerActionCellSurface


def enumerate_tower_action_cell_surfaces(
    *,
    snapshot: Any,
    surface: Any,
) -> list[TowerActionCellSurface]:
    """Enumerate current executable tower action-cell lift pools before star."""

    partition_tower = snapshot.partition_tower_view
    current_base_state = snapshot.current_base_state
    surfaces: list[TowerActionCellSurface] = []
    for tier, state_cell_id in enumerate(snapshot.current_position_at_every_tier):
        if not partition_tower.tier_is_executable_from_state(tier, current_base_state):
            continue
        action_cell_ids = partition_tower.executable_action_cells(
            tier,
            state_cell_id,
            current_base_state,
        )
        for action_cell_id in action_cell_ids:
            representative_edges = tuple(
                partition_tower.representative_edges(tier, action_cell_id)
            )
            executable_edges = tuple(
                partition_tower.executable_lift_candidates(
                    tier,
                    action_cell_id,
                    current_base_state,
                )
            )
            lifts = tuple(
                _lift_candidate(
                    tier=tier,
                    state_cell_id=state_cell_id,
                    action_cell_id=action_cell_id,
                    edge_index=edge_index,
                    edge=edge,
                    surface=surface,
                    current_base_state=current_base_state,
                )
                for edge_index, edge in enumerate(executable_edges)
            )
            surfaces.append(
                TowerActionCellSurface(
                    tier=tier,
                    state_cell_id=state_cell_id,
                    action_cell_id=action_cell_id,
                    candidate_lift_count=len(representative_edges),
                    executable_lift_count=len(executable_edges),
                    lifts=lifts,
                )
            )
    return surfaces


def available_tower_star_action_choices(
    *,
    snapshot: Any,
    surface: Any,
    q_table: dict[tuple[str, str, str], float],
    guard_type: str,
) -> list[TowerStarActionChoice]:
    """Enumerate tower action cells after arm-specific lift-candidate filtering."""

    choices: list[TowerStarActionChoice] = []
    for action_surface in enumerate_tower_action_cell_surfaces(
        snapshot=snapshot,
        surface=surface,
    ):
        guarded_lifts = action_surface.guarded_lifts(guard_type)
        if not guarded_lifts:
            continue
        selected_lift = min(guarded_lifts, key=lambda lift: lift.action_index)
        q_key = (
            str(action_surface.tier),
            cell_text(action_surface.state_cell_id),
            cell_text(action_surface.action_cell_id),
        )
        choices.append(
            TowerStarActionChoice(
                tier=action_surface.tier,
                state_cell_id=action_surface.state_cell_id,
                action_cell_id=action_surface.action_cell_id,
                action_index=selected_lift.action_index,
                candidate_lift_count=action_surface.candidate_lift_count,
                executable_lift_count=action_surface.executable_lift_count,
                guarded_lift_count=len(guarded_lifts),
                selected_lift=selected_lift,
                selected_edge=selected_lift.edge,
                q_key=q_key,
                q_value=q_table.get(q_key, 0.0),
                surface=action_surface,
            )
        )
    return choices


def choose_tower_star_action(
    *,
    snapshot: Any,
    surface: Any,
    q_table: dict[tuple[str, str, str], float],
    rng: random.Random,
    epsilon: float,
    guard_type: str,
) -> tuple[TowerStarActionChoice | None, str]:
    """Choose a tower-star action from the deepest available guarded tier."""

    choices = available_tower_star_action_choices(
        snapshot=snapshot,
        surface=surface,
        q_table=q_table,
        guard_type=guard_type,
    )
    if not choices:
        return None, "no_guarded_tower_action"
    deepest_tier = max(choice.tier for choice in choices)
    tier_choices = [choice for choice in choices if choice.tier == deepest_tier]
    if rng.random() < epsilon:
        return rng.choice(tier_choices), "epsilon_explore"
    return max(
        tier_choices,
        key=lambda choice: (
            choice.q_value,
            cell_text(choice.action_cell_id),
            -choice.action_index,
        ),
    ), "greedy"


def next_state_best_tower_star_value(
    *,
    snapshot: Any,
    surface: Any,
    q_table: dict[tuple[str, str, str], float],
    guard_type: str,
) -> float:
    """Return the best next-state Q value under the same tower-star guard."""

    choices = available_tower_star_action_choices(
        snapshot=snapshot,
        surface=surface,
        q_table=q_table,
        guard_type=guard_type,
    )
    if not choices:
        return 0.0
    deepest_tier = max(choice.tier for choice in choices)
    return max(choice.q_value for choice in choices if choice.tier == deepest_tier)


def lift_surface_rows(
    *,
    arm: Any,
    bundle: Any,
    run_id: str,
    episode_index: int,
    step_index: int,
    surfaces: list[TowerActionCellSurface],
    selected_choice: TowerStarActionChoice | None,
) -> list[dict[str, object]]:
    """Render action-cell lift surfaces as event/result rows."""

    selected_key = None
    if selected_choice is not None:
        selected_key = (
            selected_choice.tier,
            cell_text(selected_choice.state_cell_id),
            cell_text(selected_choice.action_cell_id),
        )
    rows: list[dict[str, object]] = []
    for action_surface in surfaces:
        key = (
            action_surface.tier,
            cell_text(action_surface.state_cell_id),
            cell_text(action_surface.action_cell_id),
        )
        invalid_count = len(action_surface.invalid_guard_lifts)
        nonself_count = len(action_surface.nonself_guard_lifts)
        selected = selected_key == key
        selected_lift = selected_choice.selected_lift if selected and selected_choice else None
        rows.append(
            {
                "pair_id": bundle.pair_id,
                "arm_id": arm.arm_id,
                "arm_type": arm.arm_type,
                "guard_type": arm.guard_type,
                "candidate_id": arm.candidate_id,
                "schema_id": arm.schema_id,
                "run_id": run_id,
                "replicate_index": bundle.replicate_index,
                "episode_index": episode_index,
                "step_index": step_index,
                "tier": action_surface.tier,
                "state_cell_id": key[1],
                "action_cell_id": key[2],
                "candidate_lift_count": action_surface.candidate_lift_count,
                "executable_lift_count": action_surface.executable_lift_count,
                "invalid_guard_compatible_lift_count": invalid_count,
                "nonself_guard_compatible_lift_count": nonself_count,
                "selected_by_current_tower": (
                    selected and arm.guard_type == CURRENT_LIFT_EXECUTABLE_GUARD
                ),
                "selected_by_tower_star": (
                    selected and arm.guard_type != CURRENT_LIFT_EXECUTABLE_GUARD
                ),
                "action_cell_available_before_star": action_surface.executable_lift_count > 0,
                "action_cell_available_after_invalid_star": invalid_count > 0,
                "action_cell_available_after_nonself_star": nonself_count > 0,
                "action_cell_removed_by_invalid_star": action_surface.executable_lift_count > 0
                and invalid_count == 0,
                "action_cell_removed_by_nonself_star": action_surface.executable_lift_count > 0
                and nonself_count == 0,
                "selected_lift_source": "" if selected_lift is None else selected_lift.source_state_id,
                "selected_lift_target": "" if selected_lift is None else selected_lift.next_state_id,
                "selected_action_index": "" if selected_lift is None else selected_lift.action_index,
                "selected_lift_invalid_move": (
                    "" if selected_lift is None else selected_lift.primitive_invalid_move
                ),
                "selected_lift_self_loop": (
                    "" if selected_lift is None else selected_lift.primitive_self_loop
                ),
                "selected_lift_nonself_transition": (
                    "" if selected_lift is None else selected_lift.primitive_nonself_transition
                ),
                "lift_status": "selected" if selected else "available",
                "failure_reason": "",
            }
        )
    return rows


def _lift_candidate(
    *,
    tier: int,
    state_cell_id: Any,
    action_cell_id: Any,
    edge_index: int,
    edge: Any,
    surface: Any,
    current_base_state: Any,
) -> TowerLiftCandidate:
    action_index = int(surface.module.primitive_action_to_action_index(edge.action))
    classification = classify_primitive_transition(surface, current_base_state, action_index)
    return TowerLiftCandidate(
        tier=tier,
        state_cell_id=state_cell_id,
        action_cell_id=action_cell_id,
        edge_id=f"{cell_text(action_cell_id)}:{edge_index}:{action_index}",
        action_index=action_index,
        source_state_id=state_payload_text(edge.source),
        next_state_id=state_payload_text(edge.target),
        primitive_invalid_move=classification.invalid_move,
        primitive_self_loop=classification.self_loop,
        primitive_valid_clipped_self_loop=classification.valid_clipped_self_loop,
        primitive_nonself_transition=classification.nonself_transition,
        invalid_guard_compatible=not classification.invalid_move,
        nonself_guard_compatible=classification.nonself_transition,
        edge=edge,
    )
