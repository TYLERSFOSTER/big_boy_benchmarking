"""Observable tower-training surfaces for PlateSupport gauntlet Stage 4."""

from __future__ import annotations

import random
from dataclasses import dataclass
from typing import Any

from big_boy_benchmarking.environments.plate_support.upstream import (
    ImportedPlateSupportSurface,
    import_plate_support_surface,
)

from ..contraction_schema_sweep.source_local_ratio_schema import (
    IteratedSourceLocalOutgoingRatioSchema,
    SourceLocalOutgoingRatioSchema,
)
from .candidate_source import (
    TrainingCandidate,
)


@dataclass(frozen=True)
class TrainingSurface:
    """Runtime, schema, and upstream import surface for one candidate."""

    surface: ImportedPlateSupportSurface
    schema: SourceLocalOutgoingRatioSchema | IteratedSourceLocalOutgoingRatioSchema
    runtime: Any
    strategy_id: str
    event_observability: dict[str, str]


@dataclass(frozen=True)
class TowerActionChoice:
    """One executable tower action cell and concrete lift."""

    tier: int
    state_cell_id: Any
    action_cell_id: Any
    action_index: int
    candidate_lift_count: int
    executable_lift_count: int
    selected_edge: Any
    q_key: tuple[str, str, str]
    q_value: float


def build_training_surface(candidate: TrainingCandidate) -> TrainingSurface:
    """Build the BBB-side runtime strategy for a selected source-local candidate."""

    surface = import_plate_support_surface()
    schema = _schema_for_candidate(candidate)
    return TrainingSurface(
        surface=surface,
        schema=schema,
        runtime=surface.create_runtime(schema=schema),
        strategy_id="bbb_runtime_tower_action_cell_q_learning_v001",
        event_observability={
            "episode_events": "observable_from_bbb_runtime_loop",
            "concrete_step_events": "observable_from_runtime_step",
            "lift_fiber_events": "observable_from_partition_tower_executable_lifts",
            "tier_controller_events": "observable_from_partition_tower_snapshot",
            "learner_update_events": "observable_from_bbb_tabular_q_update",
            "timing_events": "observable_from_bbb_perf_counter",
        },
    )


def _schema_for_candidate(
    candidate: TrainingCandidate,
) -> SourceLocalOutgoingRatioSchema | IteratedSourceLocalOutgoingRatioSchema:
    if candidate.schema_mode == "source_local_ratio_iterated":
        return IteratedSourceLocalOutgoingRatioSchema(
            numerator=candidate.ratio_numerator,
            denominator=candidate.ratio_denominator,
            seed=candidate.schema_seed,
            selector_rule_id=candidate.selector_rule_id,
            max_iterations=candidate.max_iterations,
            selection_mode=candidate.selection_mode,
        )
    if candidate.schema_mode == "source_local_ratio":
        return SourceLocalOutgoingRatioSchema(
            numerator=candidate.ratio_numerator,
            denominator=candidate.ratio_denominator,
            seed=candidate.schema_seed,
        )
    raise ValueError(f"unsupported training schema_mode: {candidate.schema_mode!r}")


def choose_executable_tower_action(
    *,
    snapshot: Any,
    surface: ImportedPlateSupportSurface,
    q_table: dict[tuple[str, str, str], float],
    rng: random.Random,
    epsilon: float,
) -> tuple[TowerActionChoice | None, str]:
    """Choose an executable action from the deepest currently executable tier."""

    choices = available_tower_action_choices(
        snapshot=snapshot,
        surface=surface,
        q_table=q_table,
    )
    if not choices:
        return None, "no_executable_tower_action"
    deepest_tier = max(choice.tier for choice in choices)
    tier_choices = [choice for choice in choices if choice.tier == deepest_tier]
    if rng.random() < epsilon:
        return rng.choice(tier_choices), "epsilon_explore"
    return max(
        tier_choices,
        key=lambda choice: (
            choice.q_value,
            _stable_id(choice.action_cell_id),
            -choice.action_index,
        ),
    ), "greedy"


def available_tower_action_choices(
    *,
    snapshot: Any,
    surface: ImportedPlateSupportSurface,
    q_table: dict[tuple[str, str, str], float],
) -> list[TowerActionChoice]:
    """Enumerate executable tower action cells backed by concrete lift edges."""

    partition_tower = snapshot.partition_tower_view
    current_base_state = snapshot.current_base_state
    choices: list[TowerActionChoice] = []
    for tier, state_cell_id in enumerate(snapshot.current_position_at_every_tier):
        if not partition_tower.tier_is_executable_from_state(tier, current_base_state):
            continue
        action_cell_ids = partition_tower.executable_action_cells(
            tier,
            state_cell_id,
            current_base_state,
        )
        for action_cell_id in action_cell_ids:
            lifts = partition_tower.executable_lift_candidates(
                tier,
                action_cell_id,
                current_base_state,
            )
            if not lifts:
                continue
            selected_edge = min(
                lifts,
                key=lambda edge: surface.module.primitive_action_to_action_index(edge.action),
            )
            action_index = surface.module.primitive_action_to_action_index(
                selected_edge.action
            )
            q_key = (
                str(tier),
                _stable_id(state_cell_id),
                _stable_id(action_cell_id),
            )
            choices.append(
                TowerActionChoice(
                    tier=tier,
                    state_cell_id=state_cell_id,
                    action_cell_id=action_cell_id,
                    action_index=action_index,
                    candidate_lift_count=len(
                        partition_tower.representative_edges(tier, action_cell_id)
                    ),
                    executable_lift_count=len(lifts),
                    selected_edge=selected_edge,
                    q_key=q_key,
                    q_value=q_table.get(q_key, 0.0),
                )
            )
    return choices


def next_state_best_value(
    *,
    snapshot: Any,
    surface: ImportedPlateSupportSurface,
    q_table: dict[tuple[str, str, str], float],
) -> float:
    """Return the best available Q value at the deepest executable next tier."""

    choices = available_tower_action_choices(
        snapshot=snapshot,
        surface=surface,
        q_table=q_table,
    )
    if not choices:
        return 0.0
    deepest_tier = max(choice.tier for choice in choices)
    return max(choice.q_value for choice in choices if choice.tier == deepest_tier)


def state_payload_text(state: Any) -> str:
    """Return a stable human-ish state payload representation."""

    return repr(getattr(state, "payload", state))


def cell_text(cell_id: Any) -> str:
    """Return a stable cell-id representation."""

    return _stable_id(cell_id)


def _stable_id(value: Any) -> str:
    return repr(value)
