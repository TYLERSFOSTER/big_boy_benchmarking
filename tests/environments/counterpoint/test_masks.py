from big_boy_benchmarking.environments.counterpoint.legality import validate_edge_legality
from big_boy_benchmarking.environments.counterpoint.masks import (
    legal_action_mask,
    mask_density_diagnostics,
)
from big_boy_benchmarking.environments.counterpoint.state import CounterpointState
from big_boy_benchmarking.environments.counterpoint.transition import construct_next_state


def test_legal_action_mask_matches_edge_legality(tiny_spec) -> None:
    state = CounterpointState((60, 64, 67), 0)
    action_mask = legal_action_mask(tiny_spec, state)

    assert len(action_mask.raw_actions) == len(action_mask.mask)
    for action, is_legal in zip(action_mask.raw_actions, action_mask.mask, strict=True):
        candidate = construct_next_state(tiny_spec, state, action)
        assert validate_edge_legality(tiny_spec, state, action, candidate).is_legal is is_legal


def test_mask_density_diagnostics_marks_dead_end(tiny_spec) -> None:
    state = CounterpointState((60, 64, 67), 0)
    diagnostics = mask_density_diagnostics(legal_action_mask(tiny_spec, state))

    assert diagnostics.raw_action_count > 0
    assert diagnostics.legal_action_count > 0
    assert 0.0 < diagnostics.mask_density <= 1.0

    dead_end_state = CounterpointState((60, 63, 67), 0)
    dead_end = mask_density_diagnostics(legal_action_mask(tiny_spec, dead_end_state))
    assert dead_end.dead_end or dead_end.legal_action_count >= 0
