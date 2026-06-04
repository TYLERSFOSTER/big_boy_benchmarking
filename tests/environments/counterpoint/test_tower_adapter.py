from state_collapser.core.edges import BaseEdge
from state_collapser.tower.partition import PartitionTower

from big_boy_benchmarking.environments.counterpoint import ids
from big_boy_benchmarking.environments.counterpoint.actions import CounterpointAction
from big_boy_benchmarking.environments.counterpoint.instances import (
    default_small_spec,
    default_tiny_spec,
)
from big_boy_benchmarking.environments.counterpoint.state import CounterpointState
from big_boy_benchmarking.environments.counterpoint.tower_adapter import (
    CounterpointHiddenGraph,
    CounterpointOutgoingThirdsSchema,
    build_counterpoint_iterated_noisy_rate_partition_tower,
    build_counterpoint_noisy_rate_partition_tower,
    build_counterpoint_partition_tower,
    contraction_schema_for_id,
    counterpoint_action_to_primitive_action,
    counterpoint_state_to_core_state,
    graph_edge_to_base_edge,
)


def test_hidden_graph_adapter_exposes_states_actions_and_edges() -> None:
    spec = default_tiny_spec()
    hidden_graph = CounterpointHiddenGraph(spec)
    state = counterpoint_state_to_core_state(CounterpointState((60, 64, 67), 0))

    actions = tuple(hidden_graph.out_actions(state))
    edges = tuple(hidden_graph.out_edges(state))

    assert hidden_graph.is_valid_state(state)
    assert actions
    assert all(hidden_graph.is_valid_action(action) for action in actions)
    assert all(isinstance(edge, BaseEdge) for edge in edges)


def test_partition_tower_builds_without_compatibility_readout(monkeypatch) -> None:
    def fail_readout(self):  # noqa: ANN001
        raise AssertionError("compatibility readout should not be called")

    monkeypatch.setattr(PartitionTower, "to_quotient_tier_views", fail_readout)

    result = build_counterpoint_partition_tower(
        default_tiny_spec(),
        schema_id=ids.STRUCTURED_MOTION_SCHEMA_ID,
    )

    assert len(result.tower.state_layers) > 1
    assert result.tower.last_update_result is not None


def test_adapter_identity_surfaces_are_stable() -> None:
    state = CounterpointState((60, 64, 67), 0)
    action = CounterpointAction((0, -1, 0))
    core_state = counterpoint_state_to_core_state(state)
    primitive_action = counterpoint_action_to_primitive_action(action)

    assert core_state.canonical_identity == (
        "counterpoint_symbolic_v001_state",
        state.pitches,
        state.beat_index,
    )
    assert primitive_action.canonical_identity == (
        "counterpoint_symbolic_v001_action",
        action.deltas,
    )


def test_base_edge_labels_are_hashable() -> None:
    build = build_counterpoint_partition_tower(default_tiny_spec(), schema_id=ids.EMPTY_SCHEMA_ID)
    edge = graph_edge_to_base_edge(build.graph.edges[0])

    assert hash(edge)
    assert "counterpoint_transition" in edge.labels


def test_one_third_runtime_schema_exposes_three_ordered_blocks() -> None:
    schema = contraction_schema_for_id(ids.ONE_THIRD_OUTGOING_SCHEMA_ID, schema_seed=7)

    assert isinstance(schema, CounterpointOutgoingThirdsSchema)
    assert [block.value for block in schema.ordered_blocks()] == [
        ("counterpoint_one_third", 0),
        ("counterpoint_one_third", 1),
        ("counterpoint_one_third", 2),
    ]


def test_one_third_tower_assignments_are_seeded_and_source_local() -> None:
    first = build_counterpoint_partition_tower(
        default_tiny_spec(),
        schema_id=ids.ONE_THIRD_OUTGOING_SCHEMA_ID,
        schema_seed=1,
    )
    second = build_counterpoint_partition_tower(
        default_tiny_spec(),
        schema_id=ids.ONE_THIRD_OUTGOING_SCHEMA_ID,
        schema_seed=1,
    )
    third = build_counterpoint_partition_tower(
        default_tiny_spec(),
        schema_id=ids.ONE_THIRD_OUTGOING_SCHEMA_ID,
        schema_seed=2,
    )

    first_assignments = first.tower.schema_assignment_store.assignment_by_edge_id
    second_assignments = second.tower.schema_assignment_store.assignment_by_edge_id
    third_assignments = third.tower.schema_assignment_store.assignment_by_edge_id

    assert len(first.tower.state_layers) == 4
    assert first_assignments == second_assignments
    assert first_assignments != third_assignments

    for state_id in first.tower.registry.state_ids:
        outgoing = first.tower.registry.outgoing_edge_ids(state_id)
        if not outgoing:
            continue
        assigned = {
            first_assignments[edge_id].value
            for edge_id in outgoing
            if first_assignments[edge_id] is not None
        }
        assert assigned <= {
            ("counterpoint_one_third", 0),
            ("counterpoint_one_third", 1),
            ("counterpoint_one_third", 2),
        }


def test_iterated_noisy_rate_tower_extends_one_drop_prefix() -> None:
    spec = default_small_spec()
    one_drop = build_counterpoint_noisy_rate_partition_tower(
        spec,
        numerator=1,
        denominator=18,
        schema_seed=0,
    )
    full_iterated = build_counterpoint_iterated_noisy_rate_partition_tower(
        spec,
        numerator=1,
        denominator=18,
        schema_seed=0,
    )

    one_drop_shape = [len(layer.all_cell_ids()) for layer in one_drop.tower.state_layers]
    full_shape = [len(layer.all_cell_ids()) for layer in full_iterated.tower.state_layers]

    assert one_drop_shape == [108, 54]
    assert full_shape[: len(one_drop_shape)] == one_drop_shape
    assert len(full_shape) > len(one_drop_shape)
    assert full_shape == [108, 54, 27, 19, 14]
