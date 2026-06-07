import pytest

from state_collapser.core.action import PrimitiveAction
from state_collapser.core.edges import BaseEdge
from state_collapser.core.state import State
from state_collapser.tower.partition.base_registry import BaseGraphRegistry

from big_boy_benchmarking.environments.plate_support.standard_gauntlet.contraction_schema_sweep.source_local_ratio_schema import (
    DEFAULT_ITERATED_SOURCE_LOCAL_SELECTION_MODE,
    DEFAULT_ITERATED_SOURCE_LOCAL_SELECTOR_RULE_ID,
    IteratedSourceLocalOutgoingRatioSchema,
    source_local_ratio_iterated_schema_id,
    stable_iterated_source_local_score,
)


def test_iterated_schema_id_includes_rate_and_iteration_cap() -> None:
    assert (
        source_local_ratio_iterated_schema_id(1, 144, 32)
        == "plate_support_schema_source_local_ratio_iterated_001_over_144_i032_v001"
    )


def test_stable_iterated_source_local_score_is_repeatable() -> None:
    kwargs = {
        "selector_rule_id": DEFAULT_ITERATED_SOURCE_LOCAL_SELECTOR_RULE_ID,
        "seed": 7,
        "selection_mode": DEFAULT_ITERATED_SOURCE_LOCAL_SELECTION_MODE,
        "iteration_index": 3,
        "source_component_key": 1,
        "target_component_key": 4,
        "action_key": 2,
        "edge_key": (1, 4, 2, 9),
    }

    first = stable_iterated_source_local_score(**kwargs)
    second = stable_iterated_source_local_score(**kwargs)

    assert first == second
    assert 0.0 <= first < 1.0


@pytest.mark.parametrize(
    ("kwargs", "message"),
    (
        ({"numerator": 0, "denominator": 1}, "numerator"),
        ({"numerator": 1, "denominator": 0}, "denominator"),
        ({"numerator": 2, "denominator": 1}, "numerator"),
        ({"numerator": 1, "denominator": 1, "max_iterations": 0}, "max_iterations"),
        (
            {"numerator": 1, "denominator": 1, "selector_rule_id": ""},
            "selector_rule_id",
        ),
        (
            {"numerator": 1, "denominator": 1, "selection_mode": "bad"},
            "selection_mode",
        ),
    ),
)
def test_iterated_schema_validates_constructor(
    kwargs: dict[str, object],
    message: str,
) -> None:
    with pytest.raises(ValueError, match=message):
        IteratedSourceLocalOutgoingRatioSchema(**kwargs)


def test_iterated_schema_produces_multiple_ordered_blocks() -> None:
    registry = _chain_registry()
    schema = IteratedSourceLocalOutgoingRatioSchema(
        numerator=1,
        denominator=2,
        seed=0,
        max_iterations=8,
    )

    assignments = {
        edge_id: schema.assign_edge(edge_id, registry) for edge_id in registry.edge_ids
    }

    blocks = schema.ordered_blocks()
    diagnostics = schema.plan_diagnostics()
    stop_summary = schema.stop_summary()

    assert len(blocks) == 2
    assert len(set(blocks)) == 2
    assert all(block.value[-1] == index for index, block in enumerate(blocks))
    assert any(block is not None for block in assignments.values())
    assert len(diagnostics) == 2
    assert diagnostics[0]["iteration_status"] == "completed"
    assert diagnostics[1]["iteration_status"] == "completed"
    assert stop_summary["ordered_block_count"] == 2
    assert stop_summary["final_component_count"] == 1
    assert stop_summary["stop_reason"] == "component_count_leq_one"


def _chain_registry() -> BaseGraphRegistry:
    states = tuple(State(payload=str(index), identity=("iterated-test-state", index)) for index in range(6))
    actions = (
        PrimitiveAction(payload="step", identity=("iterated-test-action", "step")),
        PrimitiveAction(payload="skip", identity=("iterated-test-action", "skip")),
    )
    edges = []
    for index in range(5):
        edges.append(
            BaseEdge(
                source=states[index],
                action=actions[0],
                target=states[index + 1],
            )
        )
    for index in range(4):
        edges.append(
            BaseEdge(
                source=states[index],
                action=actions[1],
                target=states[index + 2],
            )
        )
    registry = BaseGraphRegistry()
    registry.register_states(states)
    registry.register_edges(edges)
    return registry
