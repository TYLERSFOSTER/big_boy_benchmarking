"""Runner for PlateSupport gauntlet Stage 5 threshold calibration."""

from __future__ import annotations

import csv
from dataclasses import dataclass
from datetime import UTC, datetime
from pathlib import Path

from big_boy_benchmarking.artifacts.schemas import ARTIFACT_SCHEMA_VERSION
from big_boy_benchmarking.artifacts.writers import write_csv, write_json
from big_boy_benchmarking.upstream.state_collapser import (
    STATE_COLLAPSER_DEPENDENCY_SPEC,
    collect_state_collapser_dependency_state,
)

from ..ids import (
    ENVIRONMENT_FAMILY_ID,
    ENVIRONMENT_INSTANCE_ID,
    STRUCTURAL_TOWER_DIAGNOSTICS_STAGE_ID,
    SUITE_ID,
    THRESHOLD_FRONTIER_CALIBRATION_STAGE_ID,
    TOWER_TRAINING_HEALTH_STAGE_ID,
)
from ..paths import suite_evaluation_root, suite_readout_surface
from ..status import STAGE_STATUS_FIELDS
from .aggregation import (
    RESULT_TABLE_FIELDNAMES,
    build_stage5_aggregate_row,
    build_stage5_summary,
    build_stage5_tables,
)
from .config import ThresholdFrontierCalibrationConfig
from .docs_writer import write_threshold_frontier_calibration_docs
from .manifests import (
    calibration_arm_manifest,
    parent_training_health_manifest,
    stage_budget_lock,
    stage_input_manifest,
    stage_manifest,
    stage_output_manifest,
    threshold_policy_manifest,
)
from .stage_sources import (
    Stage5SourceError,
    default_stage1_source_for_stage4,
    load_stage1_structural_context,
    load_stage4_training_health_source,
)


@dataclass(frozen=True)
class ThresholdFrontierCalibrationResult:
    """Run result for Stage 5."""

    status: str
    stage_root: Path
    readout_source_path: Path
    artifact_paths: dict[str, str]
    recommended_target_policy_id: str
    failure_reason: str | None = None


def run_threshold_frontier_calibration(
    config: ThresholdFrontierCalibrationConfig,
    *,
    repo_root: Path | str,
) -> ThresholdFrontierCalibrationResult:
    """Run Stage 5 and write threshold calibration artifacts."""

    repo_root = Path(repo_root).expanduser().resolve()
    artifact_root = Path(config.artifact_root).expanduser().resolve()
    stage_root = artifact_root / "stages" / "threshold_frontier_calibration"
    results_dir = stage_root / "results"
    results_dir.mkdir(parents=True, exist_ok=True)

    try:
        stage4_source = load_stage4_training_health_source(
            config.training_health_source_path,
            repo_root=repo_root,
            allow_warning_candidates=config.allow_warning_candidates,
            candidate_cap=config.candidate_cap,
        )
        stage1_source_path = (
            config.stage1_source_path
            if config.stage1_source_path is not None
            else default_stage1_source_for_stage4(stage4_source)
        )
        structural_context = load_stage1_structural_context(
            stage1_source_path,
            repo_root=repo_root,
        )
        tables, arms = build_stage5_tables(
            config=config,
            stage4_source=stage4_source,
            structural_context=structural_context,
        )
    except Stage5SourceError as exc:
        return _write_blocked_result(
            config=config,
            repo_root=repo_root,
            stage_root=stage_root,
            reason=str(exc),
        )

    dependency_state = collect_state_collapser_dependency_state(
        dependency_spec=STATE_COLLAPSER_DEPENDENCY_SPEC,
    ).to_dict()
    dependency_status = str(dependency_state.get("inspection_status", "unknown"))
    output_paths = _write_result_tables(stage_root=stage_root, tables=tables)
    aggregate_row = build_stage5_aggregate_row(
        artifact_root=str(stage_root),
        tables=tables,
        stage1_source_path=str(structural_context.path),
        stage4_source_path=str(stage4_source.path),
        state_collapser_dependency_status=dependency_status,
    )
    aggregate_summary = build_stage5_summary(aggregate_row)
    recommended_target = tables["recommended_comparison_target"][0]

    write_json(stage_root / "stage_manifest.json", stage_manifest(config), create_parents=True)
    write_json(
        stage_root / "stage_budget_lock.json",
        stage_budget_lock(config),
        create_parents=True,
    )
    write_json(
        stage_root / "stage_input_manifest.json",
        stage_input_manifest(
            stage4_source=stage4_source,
            structural_context=structural_context,
        ),
        create_parents=True,
    )
    write_json(
        stage_root / "threshold_policy_manifest.json",
        threshold_policy_manifest(tables["recommended_comparison_target"]),
        create_parents=True,
    )
    write_json(
        stage_root / "calibration_arm_manifest.json",
        calibration_arm_manifest(arms),
        create_parents=True,
    )
    write_json(
        stage_root / "parent_training_health_manifest.json",
        parent_training_health_manifest(stage4_source),
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
                "stage_id": THRESHOLD_FRONTIER_CALIBRATION_STAGE_ID,
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

    readout_surface = suite_readout_surface(repo_root) / "threshold_frontier_calibration"
    readout_source_path = readout_surface / "readout_source.json"
    write_json(
        readout_source_path,
        _stage5_readout_source(
            readout_surface=readout_surface,
            stage_root=stage_root,
            config=config,
            output_paths=output_paths,
            recommended_target=recommended_target,
        ),
        create_parents=True,
    )
    doc_paths = write_threshold_frontier_calibration_docs(
        readout_surface=readout_surface,
        artifact_root=artifact_root,
        stage_root=stage_root,
        aggregate_summary=aggregate_summary,
        recommended_target=recommended_target,
        readout_source_path=readout_source_path,
        output_paths=output_paths,
    )
    all_paths = {
        **output_paths,
        "stage_manifest": str(stage_root / "stage_manifest.json"),
        "stage_budget_lock": str(stage_root / "stage_budget_lock.json"),
        "stage_input_manifest": str(stage_root / "stage_input_manifest.json"),
        "threshold_policy_manifest": str(stage_root / "threshold_policy_manifest.json"),
        "calibration_arm_manifest": str(stage_root / "calibration_arm_manifest.json"),
        "parent_training_health_manifest": str(
            stage_root / "parent_training_health_manifest.json"
        ),
        "stage_output_manifest": str(stage_root / "stage_output_manifest.json"),
        "stage_aggregate_summary": str(stage_root / "stage_aggregate_summary.json"),
        "stage_aggregate_table": str(stage_root / "stage_aggregate_table.csv"),
        "stage_run_index": str(stage_root / "stage_run_index.csv"),
        "readout_source": str(readout_source_path),
        **doc_paths,
    }
    failure_reason = (
        None if aggregate_row["blocking_reason"] == "" else str(aggregate_row["blocking_reason"])
    )
    return ThresholdFrontierCalibrationResult(
        status=str(aggregate_row["status"]),
        stage_root=stage_root,
        readout_source_path=readout_source_path,
        artifact_paths=all_paths,
        recommended_target_policy_id=str(recommended_target["target_policy_id"]),
        failure_reason=failure_reason,
    )


def _write_result_tables(
    *,
    stage_root: Path,
    tables: dict[str, list[dict[str, object]]],
) -> dict[str, str]:
    output_paths: dict[str, str] = {}
    results_dir = stage_root / "results"
    for table_name, fieldnames in RESULT_TABLE_FIELDNAMES.items():
        path = results_dir / f"{table_name}.csv"
        write_csv(
            path,
            [_select_fields(row, fieldnames) for row in tables[table_name]],
            fieldnames,
            create_parents=True,
        )
        output_paths[table_name] = str(path)
    return output_paths


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
    filtered = [
        row
        for row in prior_rows
        if row.get("stage_id") != THRESHOLD_FRONTIER_CALIBRATION_STAGE_ID
    ]
    stage_status_row = {field: aggregate_row[field] for field in STAGE_STATUS_FIELDS}
    write_csv(status_path, [*filtered, stage_status_row], STAGE_STATUS_FIELDS, create_parents=True)
    write_csv(
        suite_root / "stage_run_index.csv",
        [
            {
                "suite_id": SUITE_ID,
                "stage_id": THRESHOLD_FRONTIER_CALIBRATION_STAGE_ID,
                "run_label": run_label,
                "artifact_root": str(artifact_root),
                "status": aggregate_row["status"],
            }
        ],
        ("suite_id", "stage_id", "run_label", "artifact_root", "status"),
        create_parents=True,
    )


def _stage5_readout_source(
    *,
    readout_surface: Path,
    stage_root: Path,
    config: ThresholdFrontierCalibrationConfig,
    output_paths: dict[str, str],
    recommended_target: dict[str, object],
) -> dict[str, object]:
    required = tuple(RESULT_TABLE_FIELDNAMES)
    return {
        "artifact_schema_version": ARTIFACT_SCHEMA_VERSION,
        "source_binding_type": "evaluation_readout_source",
        "repo_readout_surface": str(readout_surface),
        "source_artifact_root": str(stage_root),
        "source_evaluation_root": str(stage_root),
        "evaluation_id": THRESHOLD_FRONTIER_CALIBRATION_STAGE_ID,
        "environment_family_id": ENVIRONMENT_FAMILY_ID,
        "environment_instance_id": ENVIRONMENT_INSTANCE_ID,
        "artifact_run_label": config.run_label,
        "run_mode": "stage5_threshold_frontier_calibration",
        "source_files": {key: output_paths[key] for key in required},
        "expected_files": {
            "required": [output_paths[key] for key in required],
            "expected_absent_is_gap": [],
            "conditional": {},
            "not_applicable": [],
            "expectation_sources": [
                "docs/design/first_plate_support_environment/standard_gauntlet_suite/"
                "05_threshold_frontier_calibration/"
                "01_001_plate_support_threshold_frontier_calibration_blueprint.md"
            ],
        },
        "goal_criteria": [
            {
                "goal_id": "plate_support_stage5_threshold_calibrated",
                "question": "Can Stage 5 select a feasible target for Stage 6?",
                "success_signal": (
                    "recommended_comparison_target.csv has calibration_status "
                    "threshold_calibrated"
                ),
                "partial_signal": "target exists but reason warns about smoke-budget sparsity",
                "failure_signal": "calibration_status is threshold_unresolved",
                "claim_if_met": "Stage 6 paired replicate comparison may consume the target",
                "claim_if_not_met": "Stage 6 is blocked until target calibration is repaired",
            }
        ],
        "calibrated_target": recommended_target,
        "claim_boundary": [
            "Stage 5 may claim a PlateSupport target is calibrated or unresolved",
            "Stage 5 may not claim tower-vs-flat benefit",
        ],
        "goal_summary_sources": [
            "docs/design/first_plate_support_environment/standard_gauntlet_suite/"
            "05_threshold_frontier_calibration/"
            "01_001_plate_support_threshold_frontier_calibration_blueprint.md",
            str(readout_surface / "method.md"),
        ],
        "methodology_summary_sources": [
            "docs/design/first_plate_support_environment/standard_gauntlet_suite/"
            "05_threshold_frontier_calibration/"
            "01_001_plate_support_threshold_frontier_calibration_blueprint.md",
            str(readout_surface / "method.md"),
            str(readout_surface / "runbook.md"),
        ],
        "structural_limit_checks": [
            {
                "check_id": "stage5_no_comparison_claim",
                "trigger": "reader interprets target calibration as performance comparison",
                "interpretation_if_triggered": (
                    "This stage only chooses a Stage 6 target policy; paired evidence "
                    "must be produced by the next stage."
                ),
                "claim_effect": "blocks tower-benefit claims from Stage 5",
            }
        ],
        "source_stage_ids": [
            STRUCTURAL_TOWER_DIAGNOSTICS_STAGE_ID,
            TOWER_TRAINING_HEALTH_STAGE_ID,
        ],
    }


def _write_blocked_result(
    *,
    config: ThresholdFrontierCalibrationConfig,
    repo_root: Path,
    stage_root: Path,
    reason: str,
) -> ThresholdFrontierCalibrationResult:
    stage_root.mkdir(parents=True, exist_ok=True)
    readout_source_path = (
        suite_readout_surface(repo_root)
        / "threshold_frontier_calibration"
        / "readout_source.json"
    )
    payload = {
        "artifact_schema_version": ARTIFACT_SCHEMA_VERSION,
        "suite_id": SUITE_ID,
        "stage_id": THRESHOLD_FRONTIER_CALIBRATION_STAGE_ID,
        "status": "blocked",
        "claim_status": "threshold_unresolved",
        "blocking_reason": reason,
        "run_label": config.run_label,
    }
    write_json(stage_root / "stage_aggregate_summary.json", payload, create_parents=True)
    return ThresholdFrontierCalibrationResult(
        status="blocked",
        stage_root=stage_root,
        readout_source_path=readout_source_path,
        artifact_paths={
            "stage_aggregate_summary": str(stage_root / "stage_aggregate_summary.json")
        },
        recommended_target_policy_id="",
        failure_reason=reason,
    )


def _select_fields(row: dict[str, object], fieldnames: tuple[str, ...]) -> dict[str, object]:
    return {field: row.get(field, "") for field in fieldnames}


def _now() -> str:
    return datetime.now(UTC).isoformat()
