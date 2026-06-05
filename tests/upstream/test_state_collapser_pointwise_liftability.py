from __future__ import annotations

from dataclasses import dataclass

from state_collapser.core.action import PrimitiveAction
from state_collapser.core.edges import BaseEdge
from state_collapser.core.state import State
from state_collapser.tower.partition import PartitionTower
from state_collapser.tower.partition.ids import EdgeId, SchemaBlockId
from state_collapser.tower.partition.schema import ContractionSchema


@dataclass(frozen=True)
class _ContractZeroToOneSchema(ContractionSchema):
    zero: State
    one: State

    def assign_edge(self, edge_id: EdgeId, registry) -> SchemaBlockId | None:  # noqa: ANN001
        edge = registry.edge_for_id(edge_id)
        if edge.source == self.zero and edge.target == self.one:
            return SchemaBlockId(("contract_zero_to_one",))
        return None

    def ordered_blocks(self) -> tuple[SchemaBlockId, ...]:
        return (SchemaBlockId(("contract_zero_to_one",)),)


def test_partition_tower_executable_lift_candidates_are_pointwise() -> None:
    zero = State(payload="0", identity=("simplex_point", 0))
    one = State(payload="1", identity=("simplex_point", 1))
    two = State(payload="2", identity=("simplex_point", 2))
    contract = PrimitiveAction(payload="contract", identity=("simplex_action", "contract"))
    upper = PrimitiveAction(payload="upper", identity=("simplex_action", "upper"))
    tower = PartitionTower(schema=_ContractZeroToOneSchema(zero=zero, one=one))
    tower.initialize(
        initial_states=(zero, one, two),
        initial_edges=(
            BaseEdge(source=zero, action=contract, target=one),
            BaseEdge(source=zero, action=upper, target=two),
        ),
        current_state=zero,
    )

    merged_state_cell = tower.current_state_cell(1, one)
    quotient_action_cells = tower.outgoing_action_cells(1, merged_state_cell)

    assert quotient_action_cells
    action_cell = quotient_action_cells[0]
    assert tower.lift_candidates(1, action_cell, one)
    assert tower.executable_lift_candidates(1, action_cell, one) == ()
    assert tower.executable_lift_candidates(1, action_cell, zero)
    assert tower.tier_is_executable_from_state(1, one) is False
    assert tower.tier_is_executable_from_state(1, zero) is True
