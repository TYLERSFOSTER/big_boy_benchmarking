"""Composite PlateSupport structural diagnostics."""

from __future__ import annotations

import random
from dataclasses import dataclass
from typing import Any

from big_boy_benchmarking.environments.plate_support.geometry import (
    orientation_summary,
    position_summary,
    reachability_pattern_summary,
    support_pattern_summary,
    validity_predicate_summary,
)
from big_boy_benchmarking.environments.plate_support.graph import (
    PlateSupportGraphDiagnostics,
    build_plate_support_graph_diagnostics,
)
from big_boy_benchmarking.environments.plate_support.states import (
    state_to_record,
)
from big_boy_benchmarking.environments.plate_support.types import (
    RandomPolicyReconRecord,
    StateRecord,
    TowerProbeRecord,
)
from big_boy_benchmarking.environments.plate_support.upstream import (
    ImportedPlateSupportSurface,
    import_plate_support_surface,
)


@dataclass(frozen=True)
class PlateSupportStructuralDiagnostics:
    state_records: tuple[StateRecord, ...]
    graph: PlateSupportGraphDiagnostics
    support_pattern_summary: tuple[dict[str, object], ...]
    reachability_pattern_summary: tuple[dict[str, object], ...]
    orientation_summary: tuple[dict[str, object], ...]
    position_summary: tuple[dict[str, object], ...]
    validity_predicate_summary: tuple[dict[str, object], ...]
    random_policy_recon: RandomPolicyReconRecord
    training_surface_availability: dict[str, bool]
    tower_probe_records: tuple[TowerProbeRecord, ...]


def collect_plate_support_structural_diagnostics(
    *,
    surface: ImportedPlateSupportSurface | None = None,
    random_policy_episodes: int = 1000,
    random_policy_seed: int = 0,
    tower_probe_records: tuple[TowerProbeRecord, ...] = (),
) -> PlateSupportStructuralDiagnostics:
    surface = surface or import_plate_support_surface()
    valid_states = tuple(surface.all_valid_states())
    candidate_states = tuple(surface.all_candidate_states())
    state_records = tuple(
        _state_record_with_role(state, surface=surface)
        for state in valid_states
    )
    graph = build_plate_support_graph_diagnostics(surface=surface)
    return PlateSupportStructuralDiagnostics(
        state_records=state_records,
        graph=graph,
        support_pattern_summary=tuple(support_pattern_summary(state_records)),
        reachability_pattern_summary=tuple(reachability_pattern_summary(state_records)),
        orientation_summary=tuple(orientation_summary(state_records)),
        position_summary=tuple(position_summary(state_records)),
        validity_predicate_summary=tuple(
            validity_predicate_summary(
                candidate_states=candidate_states,
                valid_states=valid_states,
                surface=surface,
            )
        ),
        random_policy_recon=random_policy_reconnaissance(
            surface=surface,
            episode_count=random_policy_episodes,
            seed=random_policy_seed,
        ),
        training_surface_availability=surface.training_surface_availability(),
        tower_probe_records=tower_probe_records,
    )


def random_policy_reconnaissance(
    *,
    surface: ImportedPlateSupportSurface | None = None,
    episode_count: int = 1000,
    seed: int = 0,
) -> RandomPolicyReconRecord:
    surface = surface or import_plate_support_surface()
    rng = random.Random(seed)
    total_reward = 0.0
    total_steps = 0
    success_count = 0
    invalid_move_count = 0
    for episode_index in range(episode_count):
        env = surface.create_env()
        env.reset(seed=seed + episode_index)
        terminated = False
        truncated = False
        episode_reward = 0.0
        step_count = 0
        while not (terminated or truncated):
            action = rng.randrange(surface.ACTION_COUNT)
            _, reward, terminated, truncated, info = env.step(action)
            step_count += 1
            episode_reward += float(reward)
            if info.get("invalid_move"):
                invalid_move_count += 1
            if info.get("goal_reached"):
                success_count += 1
        total_reward += episode_reward
        total_steps += step_count
    return RandomPolicyReconRecord(
        policy_id="uniform_random_primitive_action_recon_v001",
        seed=seed,
        episode_count=episode_count,
        max_steps_per_episode=int(surface.MAX_STEPS),
        success_count=success_count,
        success_rate=0.0 if episode_count == 0 else success_count / episode_count,
        mean_total_reward=0.0 if episode_count == 0 else total_reward / episode_count,
        mean_step_count=0.0 if episode_count == 0 else total_steps / episode_count,
        invalid_move_count=invalid_move_count,
        invalid_move_rate=0.0 if total_steps == 0 else invalid_move_count / total_steps,
    )


def _state_record_with_role(state: Any, *, surface: ImportedPlateSupportSurface) -> StateRecord:
    roles = []
    if state == surface.START_STATE:
        roles.append("start")
    if state == surface.CANDIDATE_GOAL_STATE:
        roles.append("goal")
    return state_to_record(state, role=",".join(roles), surface=surface)
