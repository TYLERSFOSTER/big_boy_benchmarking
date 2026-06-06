from collections import deque

from big_boy_benchmarking.environments.plate_support.states import state_id
from big_boy_benchmarking.environments.plate_support.upstream import (
    REQUIRED_SURFACE_NAMES,
    import_plate_support_surface,
)


def test_plate_support_upstream_surface_imports_required_symbols() -> None:
    surface = import_plate_support_surface()

    assert all(hasattr(surface, name) for name in REQUIRED_SURFACE_NAMES)
    assert surface.ACTION_COUNT == 12
    assert surface.MAX_STEPS == 50
    assert len(surface.all_candidate_states()) == 2700
    assert len(surface.all_valid_states()) == 89
    assert surface.is_valid_state(surface.START_STATE)
    assert surface.is_valid_state(surface.CANDIDATE_GOAL_STATE)


def test_plate_support_goal_is_not_one_primitive_action_from_start() -> None:
    surface = import_plate_support_surface()
    goal_id = state_id(surface.CANDIDATE_GOAL_STATE)

    assert all(
        state_id(next_state) != goal_id
        for _, next_state in surface.valid_outgoing_transitions(surface.START_STATE)
    )


def test_plate_support_all_valid_states_are_reachable_from_start() -> None:
    surface = import_plate_support_surface()
    valid_ids = {state_id(state) for state in surface.all_valid_states()}
    seen = {state_id(surface.START_STATE)}
    queue = deque([surface.START_STATE])
    while queue:
        current = queue.popleft()
        for _, next_state in surface.valid_outgoing_transitions(current):
            next_id = state_id(next_state)
            if next_id not in seen:
                seen.add(next_id)
                queue.append(next_state)

    assert seen == valid_ids
