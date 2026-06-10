from big_boy_benchmarking.environments.warehouse_gridlock.graph import (
    Direction,
    GridNode,
    WarehouseGraph,
    build_grid_graph,
    validate_graph,
)
from big_boy_benchmarking.environments.warehouse_gridlock.instances import load_instance


def test_full_manifest_graph_counts_and_blocked_columns() -> None:
    instance = load_instance()

    assert len(instance.graph.nodes) == 256
    assert len(instance.graph.blocked_nodes) == 5
    assert len(instance.graph.nodes - instance.graph.blocked_nodes) == 251
    assert len(instance.graph.edges) == 920
    assert GridNode(4, 4) in instance.graph.blocked_nodes
    assert not instance.graph.is_traversable_node(GridNode(4, 4))


def test_neighbor_lookup_and_bidirectional_edges() -> None:
    graph = build_grid_graph(rows=3, cols=3, blocked_nodes=())

    center = GridNode(2, 2)
    north = graph.neighbor(center, Direction.NORTH)
    south = graph.neighbor(center, Direction.SOUTH)

    assert north == GridNode(1, 2)
    assert south == GridNode(3, 2)
    assert graph.has_edge(center, north)
    assert graph.has_edge(north, center)


def test_graph_validation_rejects_edge_touching_blocked_node() -> None:
    graph = WarehouseGraph(
        rows=2,
        cols=2,
        nodes=frozenset({GridNode(1, 1), GridNode(1, 2)}),
        edges=frozenset({(GridNode(1, 1), GridNode(1, 2))}),
        blocked_nodes=frozenset({GridNode(1, 2)}),
        blocked_edges=frozenset(),
    )

    report = validate_graph(graph)

    assert not report.ok
    assert any("blocked node" in error for error in report.errors)
