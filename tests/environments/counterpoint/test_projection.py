from big_boy_benchmarking.environments.counterpoint.graph import enumerate_reachable_graph
from big_boy_benchmarking.environments.counterpoint.instances import default_tiny_spec
from big_boy_benchmarking.environments.counterpoint.projection import (
    all_drop_one_state_keys,
    projected_state_key,
    projection_diagnostics,
)
from big_boy_benchmarking.environments.counterpoint.state import CounterpointState


def test_projection_keys_cover_n3_and_n4_states() -> None:
    n3 = CounterpointState((60, 64, 67), 0)
    n4 = CounterpointState((55, 60, 64, 67), 0)

    assert projected_state_key(n3, drop_voice_index=1) == "drop1:beat0:pitches(60, 67)"
    assert len(all_drop_one_state_keys(n3)) == 3
    assert len(all_drop_one_state_keys(n4)) == 4


def test_projection_diagnostics_are_all_drop_one_posthoc() -> None:
    diagnostics = projection_diagnostics(enumerate_reachable_graph(default_tiny_spec()))

    assert diagnostics.projection_convention == "all_drop_one_posthoc"
    assert diagnostics.projected_state_count > 0
    assert diagnostics.projected_transition_count > 0
    assert diagnostics.projection_cell_size_distribution
