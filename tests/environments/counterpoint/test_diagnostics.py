from big_boy_benchmarking.environments.counterpoint.diagnostics import (
    balanced_addressability_diagnostics,
    lift_fiber_diagnostics,
    reward_fiber_diagnostics,
)
from big_boy_benchmarking.environments.counterpoint.graph import enumerate_reachable_graph
from big_boy_benchmarking.environments.counterpoint.instances import default_tiny_spec
from big_boy_benchmarking.environments.counterpoint.schemas import (
    SchemaConstruction,
    build_bad_schema,
    build_empty_schema,
    build_random_balanced_schema,
    build_random_unbalanced_schema,
)


def test_reward_fiber_diagnostics_zero_and_nonzero_variance() -> None:
    graph = enumerate_reachable_graph(default_tiny_spec())
    empty = build_empty_schema(graph)
    bad = build_bad_schema(graph)

    assert all(row.reward_variance == 0 for row in reward_fiber_diagnostics(graph, empty))
    assert any(row.reward_variance > 0 for row in reward_fiber_diagnostics(graph, bad))


def test_lift_fiber_diagnostics_no_data_and_nonempty() -> None:
    graph = enumerate_reachable_graph(default_tiny_spec())
    empty = build_empty_schema(graph)
    no_data = SchemaConstruction(spec=empty.spec, state_partition={}, edge_partition={})

    assert lift_fiber_diagnostics(no_data) == ()
    assert lift_fiber_diagnostics(empty)


def test_balanced_addressability_distinguishes_schema_shapes() -> None:
    graph = enumerate_reachable_graph(default_tiny_spec())
    balanced = balanced_addressability_diagnostics(
        build_random_balanced_schema(graph, schema_seed=1)
    )
    unbalanced = balanced_addressability_diagnostics(
        build_random_unbalanced_schema(graph, schema_seed=1)
    )

    assert balanced.effective_number_of_cells > unbalanced.effective_number_of_cells
    assert balanced.address_count <= unbalanced.address_count
