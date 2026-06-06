"""Runner for PlateSupport gauntlet Stage 1 diagnostics."""

from __future__ import annotations

import json
from dataclasses import dataclass
from datetime import UTC, datetime
from pathlib import Path
from typing import Any

from big_boy_benchmarking.artifacts.schemas import ARTIFACT_SCHEMA_VERSION
from big_boy_benchmarking.artifacts.writers import write_csv, write_json
from big_boy_benchmarking.environments.plate_support.standard_gauntlet.ids import (
    ENVIRONMENT_FAMILY_ID,
    ENVIRONMENT_INSTANCE_ID,
    STRUCTURAL_TOWER_DIAGNOSTICS_STAGE_ID,
    SUITE_ID,
)
from big_boy_benchmarking.environments.plate_support.standard_gauntlet.paths import (
    suite_evaluation_root,
    suite_readout_surface,
)
from big_boy_benchmarking.environments.plate_support.standard_gauntlet.structural_and_tower_diagnostics.aggregation import (
    build_stage_aggregate_row,
    build_stage_aggregate_summary,
)
from big_boy_benchmarking.environments.plate_support.standard_gauntlet.structural_and_tower_diagnostics.config import (
    StructuralDiagnosticsConfig,
)
from big_boy_benchmarking.environments.plate_support.standard_gauntlet.structural_and_tower_diagnostics.diagnostics import (
    collect_stage1_diagnostics,
)
from big_boy_benchmarking.environments.plate_support.standard_gauntlet.structural_and_tower_diagnostics.docs_writer import (
    write_stage1_docs,
)
from big_boy_benchmarking.environments.plate_support.standard_gauntlet.structural_and_tower_diagnostics.manifests import (
    readiness_source_manifest,
    stage_budget_lock,
    stage_input_manifest,
    stage_manifest,
    stage_output_manifest,
)
from big_boy_benchmarking.environments.plate_support.standard_gauntlet.structural_and_tower_diagnostics.readiness_source import (
    ReadinessSourceError,
    load_readiness_source,
)
from big_boy_benchmarking.environments.plate_support.standard_gauntlet.status import (
    STAGE_STATUS_FIELDS,
)
from big_boy_benchmarking.upstream.state_collapser import (
    STATE_COLLAPSER_DEPENDENCY_SPEC,
    collect_state_collapser_dependency_state,
)

RESULT_TABLE_FIELDNAMES = {
    "identity_summary": (
        "suite_id",
        "stage_id",
        "run_label",
        "environment_family_id",
        "environment_instance_id",
        "upstream_smoke_id",
        "upstream_module",
        "linearization_mode_id",
        "readiness_source",
        "readiness_artifact_root",
        "environment_doc",
        "artifact_root",
        "state_collapser_dependency_status",
    ),
    "state_space_summary": (
        "candidate_state_count",
        "valid_state_count",
        "reachable_state_count",
        "reachable_from_start",
        "start_state_id",
        "goal_state_id",
        "start_valid",
        "goal_valid",
    ),
    "action_table": (
        "action_index",
        "action_label",
        "action_category",
        "description",
        "upstream_identity",
    ),
    "transition_summary": (
        "source_state_id",
        "action_index",
        "action_label",
        "candidate_state_id",
        "next_state_id",
        "candidate_valid",
        "valid_transition",
        "invalid_move",
        "valid_self_transition",
        "reward",
        "terminated",
        "truncated_at_one_step",
    ),
    "shortest_path_summary": (
        "shortest_path_length",
        "goal_one_step_from_start",
        "action_labels",
        "reward_sequence",
        "total_shortest_path_reward",
        "terminal_state_id",
        "claim_boundary",
    ),
    "validity_predicate_summary": (
        "predicate_name",
        "valid_state_true_count",
        "valid_state_false_count",
        "ambient_true_count",
        "ambient_false_count",
        "interpretation",
    ),
    "geometry_summary": (
        "geometry_domain",
        "label",
        "valid_state_count",
        "share",
    ),
    "random_policy_recon_summary": (
        "policy_id",
        "seed",
        "episode_count",
        "max_steps_per_episode",
        "success_count",
        "success_rate",
        "mean_total_reward",
        "mean_step_count",
        "invalid_move_count",
        "invalid_move_rate",
        "claim_boundary",
    ),
    "tower_shape_summary": (
        "schema_id",
        "upstream_schema_mode",
        "env_name",
        "steps",
        "sample_size",
        "seed",
        "use_contraction_policy",
        "reset_on_terminal",
        "max_depth",
        "scheduled_assignment_count",
        "unscheduled_assignment_count",
        "depth_curve",
        "reset_event_count",
        "claim_boundary",
    ),
    "training_surface_availability": (
        "surface_name",
        "available",
        "required_for_later_stages",
    ),
    "downstream_readiness_summary": (
        "suite_id",
        "stage_id",
        "environment_instance_id",
        "ready_for_schema_sweep",
        "ready_for_candidate_discovery",
        "ready_for_training_health",
        "ready_for_threshold_calibration",
        "ready_for_paired_comparison",
        "blocking_reason",
        "candidate_state_count",
        "valid_state_count",
        "reachable_state_count",
        "valid_nonself_edge_count",
        "invalid_move_count",
        "valid_self_transition_count",
        "shortest_path_length",
        "default_schema_max_depth",
        "flat_schema_max_depth",
        "training_surfaces_available",
        "claim_boundary",
    ),
}


@dataclass(frozen=True)
class StructuralDiagnosticsResult:
    """Run result for Stage 1."""

    status: str
    stage_root: Path
    readout_source_path: Path
    artifact_paths: dict[str, str]
    warning_count: int
    failure_reason: str | None = None


def run_structural_and_tower_diagnostics(
    config: StructuralDiagnosticsConfig,
    *,
    repo_root: Path | str,
) -> StructuralDiagnosticsResult:
    """Run Stage 1 and write evaluation-stage diagnostics."""

    repo_root = Path(repo_root).expanduser().resolve()
    artifact_root = Path(config.artifact_root).expanduser().resolve()
    stage_root = artifact_root / "stages" / "structural_and_tower_diagnostics"
    results_dir = stage_root / "results"
    results_dir.mkdir(parents=True, exist_ok=True)
    try:
        readiness = load_readiness_source(config.readiness_source_path, repo_root=repo_root)
    except ReadinessSourceError as exc:
        return _write_blocked_result(
            config=config,
            repo_root=repo_root,
            stage_root=stage_root,
            reason=str(exc),
        )

    dependency_state = collect_state_collapser_dependency_state(
        dependency_spec=STATE_COLLAPSER_DEPENDENCY_SPEC,
    ).to_dict()
    current_dependency_status = str(dependency_state.get("inspection_status", "unknown"))
    rows = collect_stage1_diagnostics(
        config=config,
        readiness=readiness,
        dependency_state=dependency_state,
    )
    output_paths = _write_stage_tables(stage_root=stage_root, rows=rows)
    downstream_row = rows["downstream_readiness_summary"][0]
    aggregate_row = build_stage_aggregate_row(
        artifact_root=str(stage_root),
        downstream_row=downstream_row,
        warning_count=0,
        state_collapser_dependency_status=current_dependency_status,
    )
    aggregate_summary = build_stage_aggregate_summary(aggregate_row)

    write_json(stage_root / "stage_manifest.json", stage_manifest(config), create_parents=True)
    write_json(stage_root / "stage_budget_lock.json", stage_budget_lock(config), create_parents=True)
    write_json(
        stage_root / "stage_input_manifest.json",
        stage_input_manifest(
            config=config,
            readiness=readiness,
            dependency_state=dependency_state,
        ),
        create_parents=True,
    )
    write_json(
        stage_root / "readiness_source_manifest.json",
        readiness_source_manifest(readiness),
        create_parents=True,
    )
    write_json(
        stage_root / "stage_output_manifest.json",
        stage_output_manifest(output_paths),
        create_parents=True,
    )
    write_json(
        stage_root / "stage_aggregate_summary.json",
        aggregate_summary,
        create_parents=True,
    )
    write_csv(
        stage_root / "stage_aggregate_table.csv",
        [aggregate_row],
        tuple(aggregate_row.keys()),
        create_parents=True,
    )
    write_csv(
        stage_root / "stage_run_index.csv",
        [
            {
                "suite_id": SUITE_ID,
                "stage_id": STRUCTURAL_TOWER_DIAGNOSTICS_STAGE_ID,
                "run_label": config.run_label,
                "status": aggregate_row["status"],
                "started_at": _now(),
                "ended_at": _now(),
                "artifact_schema_version": ARTIFACT_SCHEMA_VERSION,
            }
        ],
        (
            "suite_id",
            "stage_id",
            "run_label",
            "status",
            "started_at",
            "ended_at",
            "artifact_schema_version",
        ),
        create_parents=True,
    )
    _write_suite_stage_status(
        repo_root=repo_root,
        artifact_root=artifact_root,
        run_label=config.run_label,
        aggregate_row=aggregate_row,
    )

    readout_surface = (
        suite_readout_surface(repo_root) / "structural_and_tower_diagnostics"
    )
    readout_source_path = readout_surface / "readout_source.json"
    readout_source = _stage_readout_source(
        repo_root=repo_root,
        readout_surface=readout_surface,
        stage_root=stage_root,
        config=config,
        output_paths=output_paths,
    )
    write_json(readout_source_path, readout_source, create_parents=True)
    doc_paths = write_stage1_docs(
        readout_surface=readout_surface,
        artifact_root=artifact_root,
        stage_root=stage_root,
        aggregate_summary=aggregate_summary,
        readout_source_path=readout_source_path,
        output_paths=output_paths,
    )
    all_paths = {
        **output_paths,
        "stage_manifest": str(stage_root / "stage_manifest.json"),
        "stage_budget_lock": str(stage_root / "stage_budget_lock.json"),
        "stage_input_manifest": str(stage_root / "stage_input_manifest.json"),
        "stage_output_manifest": str(stage_root / "stage_output_manifest.json"),
        "readiness_source_manifest": str(stage_root / "readiness_source_manifest.json"),
        "stage_aggregate_summary": str(stage_root / "stage_aggregate_summary.json"),
        "stage_aggregate_table": str(stage_root / "stage_aggregate_table.csv"),
        "stage_run_index": str(stage_root / "stage_run_index.csv"),
        "readout_source": str(readout_source_path),
        **doc_paths,
    }
    return StructuralDiagnosticsResult(
        status=str(aggregate_row["status"]),
        stage_root=stage_root,
        readout_source_path=readout_source_path,
        artifact_paths=all_paths,
        warning_count=0,
        failure_reason=None if aggregate_row["status"] == "complete" else str(
            aggregate_row["blocking_reason"]
        ),
    )


def _write_stage_tables(
    *,
    stage_root: Path,
    rows: dict[str, object],
) -> dict[str, str]:
    results_dir = stage_root / "results"
    output_paths: dict[str, str] = {}
    table_keys = (
        "identity_summary",
        "state_space_summary",
        "action_table",
        "transition_summary",
        "shortest_path_summary",
        "validity_predicate_summary",
        "geometry_summary",
        "random_policy_recon_summary",
        "tower_shape_summary",
        "training_surface_availability",
        "downstream_readiness_summary",
    )
    for key in table_keys:
        path = results_dir / f"{key}.csv"
        table_rows = rows[key]
        fieldnames = RESULT_TABLE_FIELDNAMES.get(key)
        if fieldnames is None:
            table_rows = list(table_rows)
            fieldnames = tuple(table_rows[0].keys()) if table_rows else ()
        write_csv(path, table_rows, fieldnames, create_parents=True)
        output_paths[key] = str(path)

    distribution_rows = rows["distribution_rows"]
    for key, table_rows in distribution_rows.items():
        path = results_dir / f"{key}.csv"
        table_rows = list(table_rows)
        fieldnames = tuple(table_rows[0].keys()) if table_rows else ()
        write_csv(path, table_rows, fieldnames, create_parents=True)
        output_paths[key] = str(path)

    write_json(stage_root / "graph_summary.json", rows["graph_summary"], create_parents=True)
    output_paths["graph_summary"] = str(stage_root / "graph_summary.json")
    return output_paths


def _write_suite_stage_status(
    *,
    repo_root: Path,
    artifact_root: Path,
    run_label: str,
    aggregate_row: dict[str, object],
) -> None:
    suite_root = suite_evaluation_root(repo_root, run_label, SUITE_ID)
    suite_root.mkdir(parents=True, exist_ok=True)
    stage_status_row = {
        field: aggregate_row[field]
        for field in STAGE_STATUS_FIELDS
    }
    write_csv(
        suite_root / "stage_status_summary.csv",
        [stage_status_row],
        STAGE_STATUS_FIELDS,
        create_parents=True,
    )
    write_csv(
        suite_root / "stage_run_index.csv",
        [
            {
                "suite_id": SUITE_ID,
                "stage_id": STRUCTURAL_TOWER_DIAGNOSTICS_STAGE_ID,
                "run_label": run_label,
                "artifact_root": str(artifact_root),
                "status": aggregate_row["status"],
            }
        ],
        ("suite_id", "stage_id", "run_label", "artifact_root", "status"),
        create_parents=True,
    )


def _stage_readout_source(
    *,
    repo_root: Path,
    readout_surface: Path,
    stage_root: Path,
    config: StructuralDiagnosticsConfig,
    output_paths: dict[str, str],
) -> dict[str, object]:
    required = [
        "identity_summary",
        "state_space_summary",
        "action_table",
        "transition_summary",
        "shortest_path_summary",
        "validity_predicate_summary",
        "geometry_summary",
        "random_policy_recon_summary",
        "tower_shape_summary",
        "training_surface_availability",
        "downstream_readiness_summary",
    ]
    return {
        "artifact_schema_version": ARTIFACT_SCHEMA_VERSION,
        "source_binding_type": "evaluation_readout_source",
        "repo_readout_surface": str(readout_surface),
        "source_artifact_root": str(stage_root),
        "source_evaluation_root": str(stage_root),
        "evaluation_id": STRUCTURAL_TOWER_DIAGNOSTICS_STAGE_ID,
        "environment_family_id": ENVIRONMENT_FAMILY_ID,
        "environment_instance_id": ENVIRONMENT_INSTANCE_ID,
        "artifact_run_label": config.run_label,
        "run_mode": "stage1_structural_diagnostics",
        "source_files": {key: output_paths[key] for key in required},
        "expected_files": {
            "required": [output_paths[key] for key in required],
            "expected_absent_is_gap": [],
            "conditional": {},
            "not_applicable": [],
            "expectation_sources": [
                "docs/design/first_plate_support_environment/standard_gauntlet_suite/"
                "01_structural_and_tower_diagnostics/"
                "01_001_plate_support_structural_and_tower_diagnostics_blueprint.md"
            ],
        },
        "goal_criteria": [
            {
                "goal_id": "plate_support_stage1_ready_for_schema_sweep",
                "question": "Is PlateSupport structurally ready for the schema sweep stage?",
                "success_signal": "downstream_readiness_summary.csv ready_for_schema_sweep is true",
                "partial_signal": "diagnostic tables exist but warning fields are nonempty",
                "failure_signal": "downstream_readiness_summary.csv has a blocking_reason",
                "claim_if_met": "Stage 2 schema sweep may consume Stage 1 artifacts",
                "claim_if_not_met": "Downstream schema sweep is blocked until Stage 1 is repaired",
            }
        ],
        "badge_policy": {
            "dimensions": [
                "artifact_status",
                "behavioral_status",
                "goal_status",
                "claim_scope",
                "provenance_status",
            ]
        },
        "goal_summary_sources": [
            "docs/design/first_plate_support_environment/standard_gauntlet_suite/"
            "01_structural_and_tower_diagnostics/"
            "01_001_plate_support_structural_and_tower_diagnostics_blueprint.md",
            str(readout_surface / "method.md"),
        ],
        "methodology_summary_sources": [
            "docs/design/first_plate_support_environment/standard_gauntlet_suite/"
            "01_structural_and_tower_diagnostics/"
            "01_001_plate_support_structural_and_tower_diagnostics_blueprint.md",
            str(readout_surface / "method.md"),
            str(readout_surface / "runbook.md"),
        ],
        "structural_limit_checks": [
            {
                "check_id": "stage1_schema_sweep_gate",
                "trigger": "ready_for_schema_sweep is false",
                "interpretation_if_triggered": (
                    "The environment diagnostic stage completed enough to explain the block, "
                    "but Stage 2 must not run until the blocking reason is resolved."
                ),
                "claim_effect": "blocks schema sweep and all downstream claims",
            }
        ],
        "claim_boundary": [
            "Stage 1 may claim structural and tower diagnostics are complete",
            "Stage 1 may claim schema sweep readiness if downstream_readiness_summary allows it",
            "Stage 1 may not claim tower learning benefit or comparison success",
        ],
        "repo_root": str(repo_root),
    }


def _write_blocked_result(
    *,
    config: StructuralDiagnosticsConfig,
    repo_root: Path,
    stage_root: Path,
    reason: str,
) -> StructuralDiagnosticsResult:
    stage_root.mkdir(parents=True, exist_ok=True)
    readout_surface = (
        suite_readout_surface(repo_root) / "structural_and_tower_diagnostics"
    )
    readout_source_path = readout_surface / "readout_source.json"
    payload = {
        "artifact_schema_version": ARTIFACT_SCHEMA_VERSION,
        "suite_id": SUITE_ID,
        "stage_id": STRUCTURAL_TOWER_DIAGNOSTICS_STAGE_ID,
        "status": "blocked",
        "blocking_reason": reason,
    }
    write_json(stage_root / "stage_aggregate_summary.json", payload, create_parents=True)
    return StructuralDiagnosticsResult(
        status="blocked",
        stage_root=stage_root,
        readout_source_path=readout_source_path,
        artifact_paths={"stage_aggregate_summary": str(stage_root / "stage_aggregate_summary.json")},
        warning_count=0,
        failure_reason=reason,
    )


def _now() -> str:
    return datetime.now(UTC).isoformat()
