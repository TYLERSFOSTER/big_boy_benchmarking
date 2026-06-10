"""Global collision checks for Warehouse Gridlock."""

from __future__ import annotations

from collections import Counter
from dataclasses import dataclass

from big_boy_benchmarking.environments.warehouse_gridlock.graph import GridNode


@dataclass(frozen=True)
class EntityMovement:
    entity_id: str
    entity_type: str
    source: GridNode
    target: GridNode

    def to_dict(self) -> dict[str, object]:
        return {
            "entity_id": self.entity_id,
            "entity_type": self.entity_type,
            "source": self.source.to_dict(),
            "target": self.target.to_dict(),
        }


def shared_node_conflicts(movements: list[EntityMovement]) -> tuple[str, ...]:
    counts = Counter(movement.target for movement in movements)
    return tuple(
        f"shared_node:{node.key}:{counts[node]}" for node in sorted(counts) if counts[node] > 1
    )


def head_on_swap_conflicts(movements: list[EntityMovement]) -> tuple[str, ...]:
    conflicts: set[str] = set()
    moving = [movement for movement in movements if movement.source != movement.target]
    for left_index, left in enumerate(moving):
        for right in moving[left_index + 1 :]:
            if left.source == right.target and left.target == right.source:
                pair = "-".join(sorted((left.entity_id, right.entity_id)))
                conflicts.add(f"head_on_swap:{pair}:{left.source.key}<->{left.target.key}")
    return tuple(sorted(conflicts))
