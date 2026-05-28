import pytest

from big_boy_benchmarking.environments.counterpoint.diagnostics import (
    balanced_addressability_diagnostics,
    reward_fiber_diagnostics,
)
from big_boy_benchmarking.environments.counterpoint.graph import enumerate_reachable_graph
from big_boy_benchmarking.environments.counterpoint.instances import default_tiny_spec
from big_boy_benchmarking.environments.counterpoint.schemas import (
    SchemaSpec,
    build_bad_schema,
    build_empty_schema,
    build_projection_audit_schema,
    build_random_balanced_schema,
    build_random_unbalanced_schema,
    build_structured_motion_schema,
)


def test_schema_spec_requires_leakage_risk_statement() -> None:
    with pytest.raises(ValueError, match="leakage_risk_statement"):
        SchemaSpec(
            schema_id="x",
            schema_family_id="x",
            schema_version="v001",
            environment_family_id="counterpoint_symbolic_v001",
            environment_instance_id="fixture",
            schema_seed=None,
            construction_method="test",
            source_label_families=(),
            state_partition_description="states",
            action_partition_description="actions",
            expected_tower_depth=1,
            expected_compression_target="none",
            leakage_risk_statement="",
            intended_role="test",
            online_eligible=True,
            diagnostic_only=False,
        )


def test_empty_schema_is_identity_baseline() -> None:
    graph = enumerate_reachable_graph(default_tiny_spec())
    schema = build_empty_schema(graph)

    assert schema.spec.intended_role == "baseline_empty"
    assert len(set(schema.edge_partition.values())) == len(graph.edges)
    assert all(item.reward_variance == 0 for item in reward_fiber_diagnostics(graph, schema))


def test_random_balanced_schema_is_seeded_and_random_unbalanced_differs() -> None:
    graph = enumerate_reachable_graph(default_tiny_spec())
    first = build_random_balanced_schema(graph, schema_seed=1)
    second = build_random_balanced_schema(graph, schema_seed=1)
    third = build_random_balanced_schema(graph, schema_seed=2)
    unbalanced = build_random_unbalanced_schema(graph, schema_seed=1)

    assert first == second
    assert first.edge_partition != third.edge_partition
    balanced_diag = balanced_addressability_diagnostics(first)
    unbalanced_diag = balanced_addressability_diagnostics(unbalanced)
    assert unbalanced_diag.largest_cell_share > balanced_diag.largest_cell_share


def test_structured_projection_and_bad_schema_roles() -> None:
    graph = enumerate_reachable_graph(default_tiny_spec())
    structured = build_structured_motion_schema(graph)
    projection = build_projection_audit_schema(graph)
    bad = build_bad_schema(graph)

    assert len(set(structured.edge_partition.values())) > 1
    assert structured.spec.source_label_families
    assert projection.spec.diagnostic_only
    assert not projection.spec.online_eligible
    assert bad.spec.intended_role == "bad_control"
    assert balanced_addressability_diagnostics(bad).largest_cell_share == 1.0
