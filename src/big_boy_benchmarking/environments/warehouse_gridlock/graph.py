"""Graph primitives for Warehouse Gridlock."""

from __future__ import annotations

from collections.abc import Iterable
from dataclasses import dataclass
from enum import StrEnum


@dataclass(frozen=True, order=True)
class GridNode:
    row: int
    col: int

    def to_dict(self) -> dict[str, int]:
        return {"row": self.row, "col": self.col}

    @classmethod
    def from_dict(cls, payload: dict[str, int]) -> GridNode:
        return cls(row=int(payload["row"]), col=int(payload["col"]))

    @property
    def key(self) -> str:
        return f"r{self.row:02d}c{self.col:02d}"


class Direction(StrEnum):
    NORTH = "north"
    SOUTH = "south"
    EAST = "east"
    WEST = "west"


_DELTAS: dict[Direction, tuple[int, int]] = {
    Direction.NORTH: (-1, 0),
    Direction.SOUTH: (1, 0),
    Direction.EAST: (0, 1),
    Direction.WEST: (0, -1),
}


@dataclass(frozen=True)
class WarehouseGraph:
    rows: int
    cols: int
    nodes: frozenset[GridNode]
    edges: frozenset[tuple[GridNode, GridNode]]
    blocked_nodes: frozenset[GridNode]
    blocked_edges: frozenset[tuple[GridNode, GridNode]]

    def is_known_node(self, node: GridNode) -> bool:
        return node in self.nodes

    def is_traversable_node(self, node: GridNode) -> bool:
        return node in self.nodes and node not in self.blocked_nodes

    def has_edge(self, source: GridNode, target: GridNode) -> bool:
        return (source, target) in self.edges and (source, target) not in self.blocked_edges

    def neighbor(self, node: GridNode, direction: Direction) -> GridNode | None:
        dr, dc = _DELTAS[direction]
        candidate = GridNode(node.row + dr, node.col + dc)
        if not self.is_known_node(candidate):
            return None
        return candidate

    def iter_neighbors(self, node: GridNode) -> Iterable[GridNode]:
        for direction in Direction:
            candidate = self.neighbor(node, direction)
            if candidate is not None and self.has_edge(node, candidate):
                yield candidate


@dataclass(frozen=True)
class GraphValidationReport:
    status: str
    errors: tuple[str, ...]

    @property
    def ok(self) -> bool:
        return not self.errors

    def to_dict(self) -> dict[str, object]:
        return {"status": self.status, "errors": list(self.errors)}


def all_grid_nodes(rows: int, cols: int) -> frozenset[GridNode]:
    return frozenset(GridNode(row, col) for row in range(1, rows + 1) for col in range(1, cols + 1))


def directed_cardinal_edges(
    *,
    rows: int,
    cols: int,
    nodes: frozenset[GridNode],
    blocked_nodes: frozenset[GridNode],
    blocked_edges: frozenset[tuple[GridNode, GridNode]] = frozenset(),
) -> frozenset[tuple[GridNode, GridNode]]:
    edges: set[tuple[GridNode, GridNode]] = set()
    for node in nodes:
        if node in blocked_nodes:
            continue
        for direction in Direction:
            dr, dc = _DELTAS[direction]
            target = GridNode(node.row + dr, node.col + dc)
            if (
                1 <= target.row <= rows
                and 1 <= target.col <= cols
                and target in nodes
                and target not in blocked_nodes
                and (node, target) not in blocked_edges
            ):
                edges.add((node, target))
    return frozenset(edges)


def build_grid_graph(
    *,
    rows: int,
    cols: int,
    blocked_nodes: Iterable[GridNode],
    blocked_edges: Iterable[tuple[GridNode, GridNode]] = (),
) -> WarehouseGraph:
    nodes = all_grid_nodes(rows, cols)
    blocked_node_set = frozenset(blocked_nodes)
    blocked_edge_set = frozenset(blocked_edges)
    edges = directed_cardinal_edges(
        rows=rows,
        cols=cols,
        nodes=nodes,
        blocked_nodes=blocked_node_set,
        blocked_edges=blocked_edge_set,
    )
    return WarehouseGraph(
        rows=rows,
        cols=cols,
        nodes=nodes,
        edges=edges,
        blocked_nodes=blocked_node_set,
        blocked_edges=blocked_edge_set,
    )


def validate_graph(graph: WarehouseGraph) -> GraphValidationReport:
    errors: list[str] = []
    if graph.rows <= 0 or graph.cols <= 0:
        errors.append("grid bounds must be positive")
    for node in graph.blocked_nodes:
        if node not in graph.nodes:
            errors.append(f"blocked node outside node set: {node.key}")
    for source, target in graph.blocked_edges:
        if source not in graph.nodes or target not in graph.nodes:
            errors.append(f"blocked edge references unknown node: {source.key}->{target.key}")
    for source, target in graph.edges:
        if source not in graph.nodes or target not in graph.nodes:
            errors.append(f"edge references unknown node: {source.key}->{target.key}")
        if source in graph.blocked_nodes or target in graph.blocked_nodes:
            errors.append(f"edge touches blocked node: {source.key}->{target.key}")
        if (source, target) in graph.blocked_edges:
            errors.append(f"edge remains listed despite blocked edge: {source.key}->{target.key}")
    return GraphValidationReport(status="ok" if not errors else "error", errors=tuple(errors))


def graph_summary(graph: WarehouseGraph) -> dict[str, object]:
    traversable_nodes = graph.nodes - graph.blocked_nodes
    return {
        "rows": graph.rows,
        "cols": graph.cols,
        "visual_node_count": len(graph.nodes),
        "traversable_node_count": len(traversable_nodes),
        "blocked_node_count": len(graph.blocked_nodes),
        "directed_edge_count": len(graph.edges),
        "blocked_edge_count": len(graph.blocked_edges),
    }
