"""Thin command-line interface for Big Boy Benchmarking."""

from __future__ import annotations

import argparse
import json
from collections.abc import Sequence
from pathlib import Path

from big_boy_benchmarking.artifacts.schemas import ARTIFACT_SCHEMA_VERSION
from big_boy_benchmarking.artifacts.validators import validate_artifact_schema_version
from big_boy_benchmarking.modes.contracts import validate_mode_contract
from big_boy_benchmarking.modes.registry import iter_mode_contracts
from big_boy_benchmarking.runners.upstream_smoke import (
    run_upstream_smoke,
    summarize_upstream_smoke,
)
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

    return parser


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

    parser.error(f"unknown command: {args.command}")
    return 2
