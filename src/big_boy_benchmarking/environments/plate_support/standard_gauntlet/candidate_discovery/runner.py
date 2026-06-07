"""Runner for PlateSupport gauntlet Stage 3 candidate discovery."""

from __future__ import annotations

import csv
import json
from dataclasses import dataclass
from datetime import UTC, datetime
from pathlib import Path

from big_boy_benchmarking.artifacts.schemas import ARTIFACT_SCHEMA_VERSION
from big_boy_benchmarking.artifacts.writers import write_csv, write_json
from big_boy_benchmarking.environments.plate_support.standard_gauntlet.candidate_discovery.aggregation import (
    build_stage3_aggregate_row,
    build_stage3_summary,
)
from big_boy_benchmarking.environments.plate_support.standard_gauntlet.candidate_discovery.config import (
    CandidateDiscoveryConfig,
)
from big_boy_benchmarking.environments.plate_support.standard_gauntlet.candidate_discovery.docs_writer import (
    write_candidate_discovery_docs,
)
from big_boy_benchmarking.environments.plate_support.standard_gauntlet.candidate_discovery.eligibility import (
    classify_candidate,
    normalize_candidate_rows,
)
from big_boy_benchmarking.environments.plate_support.standard_gauntlet.candidate_discovery.manifests import (
    parent_schema_sweep_manifest,
    selection_policy_manifest,
    stage_budget_lock,
    stage_input_manifest,
    stage_manifest,
    stage_output_manifest,
)
from big_boy_benchmarking.environments.plate_support.standard_gauntlet.candidate_discovery.selection import (
    select_candidates,
)
from big_boy_benchmarking.environments.plate_support.standard_gauntlet.candidate_discovery.stage2_source import (
    Stage2SourceError,
    load_stage2_source,
    read_stage2_table,
)
from big_boy_benchmarking.environments.plate_support.standard_gauntlet.ids import (
    CANDIDATE_DISCOVERY_STAGE_ID,
    ENVIRONMENT_FAMILY_ID,
    ENVIRONMENT_INSTANCE_ID,
    SUITE_ID,
)
from big_boy_benchmarking.environments.plate_support.standard_gauntlet.paths import (
    suite_evaluation_root,
    suite_readout_surface,
)
from big_boy_benchmarking.environments.plate_support.standard_gauntlet.status import (
    STAGE_STATUS_FIELDS,
)
from big_boy_benchmarking.upstream.state_collapser import (
    STATE_COLLAPSER_DEPENDENCY_SPEC,
    collect_state_collapser_dependency_state,
)

RESULT_TABLE_FIELDNAMES = {
    "candidate_eligibility_summary": (
        "candidate_id",
        "schema_id",
        "schema_family_id",
        "schema_seed",
        "schema_mode",
        "selection_rate",
        "ratio_numerator",
        "ratio_denominator",
        "max_iterations",
        "selector_rule_id",
        "selection_mode",
        "max_depth",
        "nontrivial_tier_count",
        "candidate_role",
        "selection_status",
        "eligibility_score",
        "eligibility_reason",
        "candidate_signal",
        "structural_class",
        "allowed_downstream_stage",
        "source_row_id",
    ),
    "selected_candidate_summary": (
        "candidate_id",
        "schema_id",
        "schema_family_id",
        "schema_seed",
        "schema_mode",
        "selection_rate",
        "ratio_numerator",
        "ratio_denominator",
        "max_iterations",
        "selector_rule_id",
        "selection_mode",
        "max_depth",
        "nontrivial_tier_count",
        "selection_status",
        "allowed_downstream_stage",
        "eligibility_reason",
    ),
    "blocked_candidate_summary": (
        "candidate_id",
        "schema_id",
        "schema_family_id",
        "schema_seed",
        "schema_mode",
        "selection_rate",
        "ratio_numerator",
        "ratio_denominator",
        "max_iterations",
        "selector_rule_id",
        "selection_mode",
        "max_depth",
        "nontrivial_tier_count",
        "selection_status",
        "blocking_reason",
        "eligibility_reason",
    ),
    "control_anchor_summary": (
        "candidate_id",
        "schema_id",
        "schema_family_id",
        "schema_seed",
        "schema_mode",
        "selection_rate",
        "ratio_numerator",
        "ratio_denominator",
        "max_iterations",
        "selector_rule_id",
        "selection_mode",
        "max_depth",
        "nontrivial_tier_count",
        "selection_status",
        "allowed_downstream_stage",
    ),
    "degeneracy_anchor_summary": (
        "candidate_id",
        "schema_id",
        "schema_family_id",
        "schema_seed",
        "schema_mode",
        "selection_rate",
        "ratio_numerator",
        "ratio_denominator",
        "max_iterations",
        "selector_rule_id",
        "selection_mode",
        "max_depth",
        "nontrivial_tier_count",
        "selection_status",
        "allowed_downstream_stage",
        "eligibility_reason",
    ),
    "candidate_source_trace": (
        "candidate_id",
        "source_stage_id",
        "source_row_id",
        "source_artifact_root",
        "source_trace_status",
    ),
    "downstream_training_health_input_summary": (
        "candidate_id",
        "schema_id",
        "schema_family_id",
        "schema_seed",
        "schema_mode",
        "selection_rate",
        "ratio_numerator",
        "ratio_denominator",
        "max_iterations",
        "selector_rule_id",
        "selection_mode",
        "max_depth",
        "nontrivial_tier_count",
        "selection_status",
        "allowed_downstream_stage",
        "source_artifact_root",
    ),
}


@dataclass(frozen=True)
class CandidateDiscoveryResult:
    """Run result for Stage 3."""

    status: str
    stage_root: Path
    readout_source_path: Path
    artifact_paths: dict[str, str]
    warning_count: int
    failure_reason: str | None = None


def run_candidate_discovery(
    config: CandidateDiscoveryConfig,
    *,
    repo_root: Path | str,
) -> CandidateDiscoveryResult:
    """Run Stage 3 and write candidate discovery artifacts."""

    repo_root = Path(repo_root).expanduser().resolve()
    artifact_root = Path(config.artifact_root).expanduser().resolve()
    stage_root = artifact_root / "stages" / "candidate_discovery"
    results_dir = stage_root / "results"
    results_dir.mkdir(parents=True, exist_ok=True)
    try:
        stage2 = load_stage2_source(config.schema_sweep_source_path, repo_root=repo_root)
    except Stage2SourceError as exc:
        return _write_blocked_result(config=config, repo_root=repo_root, stage_root=stage_root, reason=str(exc))

    signal_rows = read_stage2_table(stage2, "schema_candidate_signal_summary")
    normalized = normalize_candidate_rows(
        signal_rows,
        source_artifact_root=str(stage2.source_artifact_root),
    )
    classified = [classify_candidate(row) for row in normalized]
    selected_rows = select_candidates(classified, config=config)
    dependency_state = collect_state_collapser_dependency_state(
        dependency_spec=STATE_COLLAPSER_DEPENDENCY_SPEC,
    ).to_dict()
    dependency_status = str(dependency_state.get("inspection_status", "unknown"))
    aggregate_row = build_stage3_aggregate_row(
        artifact_root=str(stage_root),
        selected_rows=selected_rows,
        state_collapser_dependency_status=dependency_status,
    )
    aggregate_summary = build_stage3_summary(aggregate_row)
    output_paths = _write_result_tables(stage_root=stage_root, selected_rows=selected_rows)
    write_json(stage_root / "stage_manifest.json", stage_manifest(config), create_parents=True)
    write_json(stage_root / "stage_budget_lock.json", stage_budget_lock(config), create_parents=True)
    write_json(stage_root / "stage_input_manifest.json", stage_input_manifest(stage2), create_parents=True)
    write_json(
        stage_root / "candidate_selection_policy_manifest.json",
        selection_policy_manifest(),
        create_parents=True,
    )
    write_json(
        stage_root / "candidate_manifest.json",
        {"candidates": selected_rows, "aggregate_summary": aggregate_summary},
        create_parents=True,
    )
    write_json(
        stage_root / "parent_schema_sweep_manifest.json",
        parent_schema_sweep_manifest(stage2),
        create_parents=True,
    )
    write_json(stage_root / "stage_output_manifest.json", stage_output_manifest(output_paths), create_parents=True)
    write_json(stage_root / "stage_aggregate_summary.json", aggregate_summary, create_parents=True)
    write_csv(stage_root / "stage_aggregate_table.csv", [aggregate_row], tuple(aggregate_row.keys()), create_parents=True)
    write_csv(
        stage_root / "stage_run_index.csv",
        [
            {
                "suite_id": SUITE_ID,
                "stage_id": CANDIDATE_DISCOVERY_STAGE_ID,
                "run_label": config.run_label,
                "status": aggregate_row["status"],
                "started_at": _now(),
                "ended_at": _now(),
                "artifact_schema_version": ARTIFACT_SCHEMA_VERSION,
            }
        ],
        ("suite_id", "stage_id", "run_label", "status", "started_at", "ended_at", "artifact_schema_version"),
        create_parents=True,
    )
    _write_suite_stage_status(
        repo_root=repo_root,
        artifact_root=artifact_root,
        run_label=config.run_label,
        aggregate_row=aggregate_row,
    )
    readout_surface = suite_readout_surface(repo_root) / "candidate_discovery"
    readout_source_path = readout_surface / "readout_source.json"
    write_json(
        readout_source_path,
        _stage3_readout_source(
            readout_surface=readout_surface,
            stage_root=stage_root,
            config=config,
            output_paths=output_paths,
        ),
        create_parents=True,
    )
    doc_paths = write_candidate_discovery_docs(
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
        "candidate_selection_policy_manifest": str(stage_root / "candidate_selection_policy_manifest.json"),
        "candidate_manifest": str(stage_root / "candidate_manifest.json"),
        "parent_schema_sweep_manifest": str(stage_root / "parent_schema_sweep_manifest.json"),
        "stage_output_manifest": str(stage_root / "stage_output_manifest.json"),
        "stage_aggregate_summary": str(stage_root / "stage_aggregate_summary.json"),
        "stage_aggregate_table": str(stage_root / "stage_aggregate_table.csv"),
        "stage_run_index": str(stage_root / "stage_run_index.csv"),
        "readout_source": str(readout_source_path),
        **doc_paths,
    }
    return CandidateDiscoveryResult(
        status=str(aggregate_row["status"]),
        stage_root=stage_root,
        readout_source_path=readout_source_path,
        artifact_paths=all_paths,
        warning_count=0,
        failure_reason=(
            None
            if aggregate_row["claim_status"] == "candidate_found"
            else str(aggregate_row["blocking_reason"])
        ),
    )


def _write_result_tables(
    *,
    stage_root: Path,
    selected_rows: list[dict[str, object]],
) -> dict[str, str]:
    results_dir = stage_root / "results"
    selected_training = [
        row for row in selected_rows if row["selection_status"] == "selected_training_candidate"
    ]
    blocked = [
        row
        for row in selected_rows
        if row["selection_status"] == "not_selected"
        and row["candidate_role"] == "blocked_candidate"
    ]
    controls = [
        row for row in selected_rows if row["selection_status"] == "selected_control_anchor"
    ]
    degeneracy = [
        row for row in selected_rows if row["selection_status"] == "selected_degeneracy_anchor"
    ]
    source_trace = [
        {
            "candidate_id": row["candidate_id"],
            "source_stage_id": row["source_stage_id"],
            "source_row_id": row["source_row_id"],
            "source_artifact_root": row["source_artifact_root"],
            "source_trace_status": row["source_trace_status"],
        }
        for row in selected_rows
    ]
    downstream = [
        {
            "candidate_id": row["candidate_id"],
            "schema_id": row["schema_id"],
            "schema_family_id": row["schema_family_id"],
            "schema_seed": row["schema_seed"],
            "schema_mode": row.get("schema_mode", ""),
            "selection_rate": row.get("selection_rate", ""),
            "ratio_numerator": row.get("ratio_numerator", ""),
            "ratio_denominator": row.get("ratio_denominator", ""),
            "max_iterations": row.get("max_iterations", ""),
            "selector_rule_id": row.get("selector_rule_id", ""),
            "selection_mode": row.get("selection_mode", ""),
            "max_depth": row.get("max_depth", ""),
            "nontrivial_tier_count": row.get("nontrivial_tier_count", ""),
            "selection_status": row["selection_status"],
            "allowed_downstream_stage": row["allowed_downstream_stage"],
            "source_artifact_root": row["source_artifact_root"],
        }
        for row in selected_training
    ]
    tables = {
        "candidate_eligibility_summary": selected_rows,
        "selected_candidate_summary": selected_training,
        "blocked_candidate_summary": blocked,
        "control_anchor_summary": controls,
        "degeneracy_anchor_summary": degeneracy,
        "candidate_source_trace": source_trace,
        "downstream_training_health_input_summary": downstream,
    }
    output_paths: dict[str, str] = {}
    for key, rows in tables.items():
        path = results_dir / f"{key}.csv"
        write_csv(
            path,
            [_select_fields(row, RESULT_TABLE_FIELDNAMES[key]) for row in rows],
            RESULT_TABLE_FIELDNAMES[key],
            create_parents=True,
        )
        output_paths[key] = str(path)
    return output_paths


def _select_fields(row: dict[str, object], fieldnames: tuple[str, ...]) -> dict[str, object]:
    return {field: row.get(field, "") for field in fieldnames}


def _write_suite_stage_status(
    *,
    repo_root: Path,
    artifact_root: Path,
    run_label: str,
    aggregate_row: dict[str, object],
) -> None:
    suite_root = suite_evaluation_root(repo_root, run_label, SUITE_ID)
    status_path = suite_root / "stage_status_summary.csv"
    prior_rows: list[dict[str, str]] = []
    if status_path.exists():
        with status_path.open(encoding="utf-8", newline="") as handle:
            prior_rows = list(csv.DictReader(handle))
    filtered = [row for row in prior_rows if row.get("stage_id") != CANDIDATE_DISCOVERY_STAGE_ID]
    stage_status_row = {field: aggregate_row[field] for field in STAGE_STATUS_FIELDS}
    write_csv(status_path, [*filtered, stage_status_row], STAGE_STATUS_FIELDS, create_parents=True)
    write_csv(
        suite_root / "stage_run_index.csv",
        [
            {
                "suite_id": SUITE_ID,
                "stage_id": CANDIDATE_DISCOVERY_STAGE_ID,
                "run_label": run_label,
                "artifact_root": str(artifact_root),
                "status": aggregate_row["status"],
            }
        ],
        ("suite_id", "stage_id", "run_label", "artifact_root", "status"),
        create_parents=True,
    )


def _stage3_readout_source(
    *,
    readout_surface: Path,
    stage_root: Path,
    config: CandidateDiscoveryConfig,
    output_paths: dict[str, str],
) -> dict[str, object]:
    required = tuple(RESULT_TABLE_FIELDNAMES)
    return {
        "artifact_schema_version": ARTIFACT_SCHEMA_VERSION,
        "source_binding_type": "evaluation_readout_source",
        "repo_readout_surface": str(readout_surface),
        "source_artifact_root": str(stage_root),
        "source_evaluation_root": str(stage_root),
        "evaluation_id": CANDIDATE_DISCOVERY_STAGE_ID,
        "environment_family_id": ENVIRONMENT_FAMILY_ID,
        "environment_instance_id": ENVIRONMENT_INSTANCE_ID,
        "artifact_run_label": config.run_label,
        "run_mode": "stage3_candidate_discovery",
        "source_files": {key: output_paths[key] for key in required},
        "expected_files": {
            "required": [output_paths[key] for key in required],
            "expected_absent_is_gap": [],
            "conditional": {},
            "not_applicable": [],
            "expectation_sources": [
                "docs/design/first_plate_support_environment/standard_gauntlet_suite/"
                "03_candidate_discovery/"
                "01_001_plate_support_candidate_discovery_blueprint.md"
            ],
        },
        "goal_criteria": [
            {
                "goal_id": "plate_support_stage3_training_candidates",
                "question": "Did Stage 2 yield any selected training candidates?",
                "success_signal": "downstream_training_health_input_summary.csv has rows",
                "partial_signal": "control or degeneracy anchors exist but no training candidate",
                "failure_signal": "candidate manifest missing or source trace incomplete",
                "claim_if_met": "Stage 4 tower training health may run",
                "claim_if_not_met": "Stage 4 is blocked by candidate_not_found",
            }
        ],
        "claim_boundary": [
            "Stage 3 may claim candidates were classified or not found",
            "Stage 3 may not claim training health or performance benefit",
        ],
        "goal_summary_sources": [
            "docs/design/first_plate_support_environment/standard_gauntlet_suite/"
            "03_candidate_discovery/"
            "01_001_plate_support_candidate_discovery_blueprint.md",
            str(readout_surface / "method.md"),
        ],
        "methodology_summary_sources": [
            "docs/design/first_plate_support_environment/standard_gauntlet_suite/"
            "03_candidate_discovery/"
            "01_001_plate_support_candidate_discovery_blueprint.md",
            str(readout_surface / "method.md"),
            str(readout_surface / "runbook.md"),
        ],
    }


def _write_blocked_result(
    *,
    config: CandidateDiscoveryConfig,
    repo_root: Path,
    stage_root: Path,
    reason: str,
) -> CandidateDiscoveryResult:
    stage_root.mkdir(parents=True, exist_ok=True)
    readout_source_path = suite_readout_surface(repo_root) / "candidate_discovery" / "readout_source.json"
    payload = {
        "artifact_schema_version": ARTIFACT_SCHEMA_VERSION,
        "suite_id": SUITE_ID,
        "stage_id": CANDIDATE_DISCOVERY_STAGE_ID,
        "status": "blocked",
        "blocking_reason": reason,
        "run_label": config.run_label,
    }
    write_json(stage_root / "stage_aggregate_summary.json", payload, create_parents=True)
    return CandidateDiscoveryResult(
        status="blocked",
        stage_root=stage_root,
        readout_source_path=readout_source_path,
        artifact_paths={"stage_aggregate_summary": str(stage_root / "stage_aggregate_summary.json")},
        warning_count=0,
        failure_reason=reason,
    )


def _now() -> str:
    return datetime.now(UTC).isoformat()
