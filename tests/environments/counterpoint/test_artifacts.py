from big_boy_benchmarking.environments.counterpoint.artifacts import (
    action_mask_manifest,
    edge_label_manifest,
    environment_family_manifest,
    environment_instance_manifest,
    graph_summary_artifact,
    legality_manifest,
    quotient_summary,
    reward_bundle_manifest,
    schema_manifest,
    write_environment_artifacts,
    write_schema_artifacts,
)
from big_boy_benchmarking.environments.counterpoint.graph import enumerate_reachable_graph
from big_boy_benchmarking.environments.counterpoint.instances import default_tiny_spec
from big_boy_benchmarking.environments.counterpoint.path_volume import exact_path_volume
from big_boy_benchmarking.environments.counterpoint.schemas import build_empty_schema


def test_environment_manifest_builders_have_required_keys() -> None:
    spec = default_tiny_spec()
    graph = enumerate_reachable_graph(spec)

    assert environment_family_manifest((spec,))["environment_family_id"]
    assert environment_instance_manifest(spec)["spec"]["environment_instance_id"]
    assert legality_manifest(spec)["legality_contract_id"]
    assert reward_bundle_manifest(spec)["terms"]
    assert edge_label_manifest(spec)["label_families"]
    assert graph_summary_artifact(graph)["state_count"] == 8
    assert action_mask_manifest(spec)["uses_legality_contract_id"] == spec.legality_contract_id


def test_schema_artifact_builders_have_required_keys() -> None:
    graph = enumerate_reachable_graph(default_tiny_spec())
    schema = build_empty_schema(graph)

    assert schema_manifest(schema)["schema_id"] == "counterpoint_empty_schema_v001"
    assert quotient_summary(schema)["fine_edge_count"] == len(graph.edges)


def test_artifact_writers_use_explicit_roots(tmp_path) -> None:
    spec = default_tiny_spec()
    graph = enumerate_reachable_graph(spec)
    path_summary = exact_path_volume(spec, length=spec.horizon_steps, graph=graph)
    schema = build_empty_schema(graph)

    env_paths = write_environment_artifacts(
        tmp_path / "env",
        graph=graph,
        path_summary=path_summary,
    )
    schema_paths = write_schema_artifacts(tmp_path / "schema", schema=schema)

    assert "graph_summary.json" in env_paths
    assert "mask_density.csv" in env_paths
    assert "schema_manifest.json" in schema_paths
    assert "quotient_cells.csv" in schema_paths
