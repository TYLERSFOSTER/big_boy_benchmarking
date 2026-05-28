"""Thin command-line interface for Big Boy Benchmarking."""

from __future__ import annotations

import argparse
import json
from collections.abc import Sequence
from pathlib import Path

from big_boy_benchmarking.artifacts.schemas import ARTIFACT_SCHEMA_VERSION
from big_boy_benchmarking.artifacts.validators import validate_artifact_schema_version
from big_boy_benchmarking.artifacts.writers import append_jsonl, write_csv, write_json
from big_boy_benchmarking.environments.counterpoint.artifacts import (
    write_environment_artifacts,
    write_schema_artifacts,
)
from big_boy_benchmarking.environments.counterpoint.diagnostics import (
    balanced_addressability_diagnostics,
    lift_fiber_diagnostics,
    reward_fiber_diagnostics,
)
from big_boy_benchmarking.environments.counterpoint.fixture_search import (
    search_fixture_candidates,
)
from big_boy_benchmarking.environments.counterpoint.graph import enumerate_reachable_graph
from big_boy_benchmarking.environments.counterpoint.instances import (
    default_small_spec,
    default_tiny_spec,
    small_candidate_specs,
    tiny_candidate_specs,
)
from big_boy_benchmarking.environments.counterpoint.path_volume import exact_path_volume
from big_boy_benchmarking.environments.counterpoint.runners import (
    run_direct_masked_random,
    run_direct_tabular_q,
    run_tower_schema_smoke,
)
from big_boy_benchmarking.environments.counterpoint.schemas import build_schema_for_id
from big_boy_benchmarking.modes.contracts import validate_mode_contract
from big_boy_benchmarking.modes.registry import iter_mode_contracts
from big_boy_benchmarking.runners.upstream_smoke import (
    run_upstream_smoke,
    summarize_upstream_smoke,
)
from big_boy_benchmarking.seeds.bundles import generate_seed_bundles
from big_boy_benchmarking.upstream.smoke_envs import iter_smoke_environment_specs

RESERVED_CONSOLE_COMMAND = "bbb"


def _validate_contracts() -> int:
    validate_artifact_schema_version(ARTIFACT_SCHEMA_VERSION).require_valid()
    for contract in iter_mode_contracts():
        validate_mode_contract(contract, allow_reserved=True)
    smoke_ids = [spec.smoke_id for spec in iter_smoke_environment_specs()]
    print(
        json.dumps(
            {
                "status": "ok",
                "artifact_schema_version": ARTIFACT_SCHEMA_VERSION,
                "mode_count": len(iter_mode_contracts()),
                "smoke_ids": smoke_ids,
                "reserved_console_command": RESERVED_CONSOLE_COMMAND,
            },
            sort_keys=True,
        )
    )
    return 0


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(prog="python -m big_boy_benchmarking.cli")
    subparsers = parser.add_subparsers(dest="command", required=True)

    subparsers.add_parser("validate-contracts")

    run_parser = subparsers.add_parser("run-upstream-smoke")
    run_parser.add_argument("--smoke-id", required=True)
    run_parser.add_argument("--artifact-root", required=True, type=Path)
    run_parser.add_argument("--mode-id", default="tower_empty_schema_tabular")
    run_parser.add_argument("--run-id")
    run_parser.add_argument("--request-readout", action="store_true")

    summary_parser = subparsers.add_parser("summarize-smoke")
    summary_parser.add_argument("--artifact-root", required=True, type=Path)
    summary_parser.add_argument(
        "--run-family-id",
        default="upstream_smoke_readout_discipline_v001",
    )

    counterpoint_parser = subparsers.add_parser("counterpoint")
    counterpoint_subparsers = counterpoint_parser.add_subparsers(
        dest="counterpoint_command",
        required=True,
    )

    fixture_parser = counterpoint_subparsers.add_parser("search-fixtures")
    fixture_parser.add_argument("--artifact-root", required=True, type=Path)
    fixture_parser.add_argument("--scale", choices=("tiny", "small"), default="tiny")

    graph_parser = counterpoint_subparsers.add_parser("graph-diagnostics")
    graph_parser.add_argument("--artifact-root", required=True, type=Path)
    graph_parser.add_argument("--instance-id", choices=("tiny", "small"), default="tiny")

    schema_parser = counterpoint_subparsers.add_parser("schema-diagnostics")
    schema_parser.add_argument("--artifact-root", required=True, type=Path)
    schema_parser.add_argument("--instance-id", choices=("tiny", "small"), default="tiny")
    schema_parser.add_argument("--schema-id", required=True)
    schema_parser.add_argument("--schema-seed", type=int)

    direct_parser = counterpoint_subparsers.add_parser("run-direct")
    direct_parser.add_argument("--artifact-root", required=True, type=Path)
    direct_parser.add_argument("--instance-id", choices=("tiny", "small"), default="tiny")
    direct_parser.add_argument(
        "--policy",
        choices=("masked-random", "tabular-q"),
        default="masked-random",
    )
    direct_parser.add_argument("--seed", type=int, default=0)
    direct_parser.add_argument("--episodes", type=int, default=1)
    direct_parser.add_argument("--horizon", type=int)

    tower_parser = counterpoint_subparsers.add_parser("tower-smoke")
    tower_parser.add_argument("--artifact-root", required=True, type=Path)
    tower_parser.add_argument("--instance-id", choices=("tiny", "small"), default="tiny")
    tower_parser.add_argument("--schema-id", required=True)
    tower_parser.add_argument("--seed", type=int, default=0)
    tower_parser.add_argument("--schema-seed", type=int)

    return parser


def _counterpoint_spec(instance_id: str):
    if instance_id == "tiny":
        return default_tiny_spec()
    if instance_id == "small":
        return default_small_spec()
    raise ValueError(f"unknown counterpoint instance id: {instance_id}")


def _run_counterpoint_command(args: argparse.Namespace) -> int:
    if args.counterpoint_command == "search-fixtures":
        candidates = tiny_candidate_specs() if args.scale == "tiny" else small_candidate_specs()
        results = search_fixture_candidates(candidates)
        target = args.artifact_root / "counterpoint" / "fixture_search"
        target.mkdir(parents=True, exist_ok=True)
        for result in results:
            append_jsonl(target / f"{args.scale}_fixture_search.jsonl", result.to_dict())
        write_json(
            target / f"{args.scale}_fixture_search_summary.json",
            {
                "scale": args.scale,
                "candidate_count": len(results),
                "selected": [
                    result.environment_instance_id for result in results if result.selected
                ],
            },
        )
        print(json.dumps({"status": "ok", "candidate_count": len(results)}, sort_keys=True))
        return 0

    if args.counterpoint_command == "graph-diagnostics":
        spec = _counterpoint_spec(args.instance_id)
        graph = enumerate_reachable_graph(spec)
        path_summary = exact_path_volume(spec, length=spec.horizon_steps, graph=graph)
        target = (
            args.artifact_root
            / "counterpoint"
            / "graph_diagnostics"
            / spec.environment_instance_id
        )
        artifact_paths = write_environment_artifacts(
            target,
            graph=graph,
            path_summary=path_summary,
        )
        print(
            json.dumps(
                {
                    "status": "ok",
                    "state_count": len(graph.states),
                    "edge_count": len(graph.edges),
                    "artifact_count": len(artifact_paths),
                },
                sort_keys=True,
            )
        )
        return 0

    if args.counterpoint_command == "schema-diagnostics":
        spec = _counterpoint_spec(args.instance_id)
        graph = enumerate_reachable_graph(spec)
        schema = build_schema_for_id(
            graph,
            schema_id=args.schema_id,
            schema_seed=args.schema_seed,
        )
        target = args.artifact_root / "counterpoint" / "schema_diagnostics" / schema.spec.schema_id
        artifact_paths = write_schema_artifacts(target, schema=schema)
        reward_rows = [row.to_dict() for row in reward_fiber_diagnostics(graph, schema)]
        lift_rows = [row.to_dict() for row in lift_fiber_diagnostics(schema)]
        addressability = balanced_addressability_diagnostics(schema)
        write_csv(
            target / "reward_fiber_variance.csv",
            reward_rows,
            [
                "schema_id",
                "cell_id",
                "fine_transition_count",
                "reward_mean",
                "reward_variance",
                "reward_min",
                "reward_max",
                "term_variance",
            ],
        )
        write_csv(
            target / "lift_fiber_summary.csv",
            lift_rows,
            [
                "cell_id",
                "fine_candidate_count",
                "entropy",
                "valid_lift_count",
                "failed_lift_count",
                "failed_lift_reason_counts",
            ],
        )
        write_json(target / "balanced_addressability.json", addressability.to_dict())
        print(
            json.dumps(
                {
                    "status": "ok",
                    "schema_id": schema.spec.schema_id,
                    "artifact_count": len(artifact_paths) + 3,
                },
                sort_keys=True,
            )
        )
        return 0

    if args.counterpoint_command == "run-direct":
        spec = _counterpoint_spec(args.instance_id)
        seed_bundle = generate_seed_bundles(base_seed=args.seed, replicate_count=1)[0]
        if args.policy == "masked-random":
            result = run_direct_masked_random(
                spec=spec,
                seed_bundle=seed_bundle,
                artifact_root=args.artifact_root,
                episode_count=args.episodes,
                horizon=args.horizon,
            )
        else:
            result = run_direct_tabular_q(
                spec=spec,
                seed_bundle=seed_bundle,
                artifact_root=args.artifact_root,
                episode_count=args.episodes,
                horizon=args.horizon,
            )
        print(json.dumps({"status": result.status, "run_id": result.run_id}, sort_keys=True))
        return 0 if result.status == "success" else 2

    if args.counterpoint_command == "tower-smoke":
        spec = _counterpoint_spec(args.instance_id)
        seed_bundle = generate_seed_bundles(base_seed=args.seed, replicate_count=1)[0]
        result = run_tower_schema_smoke(
            spec=spec,
            schema_id=args.schema_id,
            seed_bundle=seed_bundle,
            artifact_root=args.artifact_root,
            schema_seed=args.schema_seed,
        )
        print(json.dumps({"status": result.status, "run_id": result.run_id}, sort_keys=True))
        return 0 if result.status == "success" else 2

    raise ValueError(f"unknown counterpoint command: {args.counterpoint_command}")


def main(argv: Sequence[str] | None = None) -> int:
    parser = build_parser()
    args = parser.parse_args(argv)

    if args.command == "validate-contracts":
        return _validate_contracts()

    if args.command == "run-upstream-smoke":
        result = run_upstream_smoke(
            smoke_id=args.smoke_id,
            artifact_root=args.artifact_root,
            mode_id=args.mode_id,
            run_id=args.run_id,
            request_readout=True if args.request_readout else None,
        )
        print(json.dumps({"status": result.status, "run_id": result.run_id}, sort_keys=True))
        return 0 if result.status == "success" else 2

    if args.command == "summarize-smoke":
        summary = summarize_upstream_smoke(args.artifact_root, args.run_family_id)
        print(json.dumps(summary, sort_keys=True))
        return 0

    if args.command == "counterpoint":
        return _run_counterpoint_command(args)

    parser.error(f"unknown command: {args.command}")
    return 2
