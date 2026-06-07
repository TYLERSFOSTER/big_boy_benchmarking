"""Runner for PlateSupport gauntlet Stage 2 schema sweep."""

from __future__ import annotations

import csv
from dataclasses import dataclass
from datetime import UTC, datetime
from pathlib import Path

from big_boy_benchmarking.artifacts.schemas import ARTIFACT_SCHEMA_VERSION
from big_boy_benchmarking.artifacts.writers import write_csv, write_json
from big_boy_benchmarking.environments.plate_support.standard_gauntlet.contraction_schema_sweep.aggregation import (
    build_stage2_aggregate_row,
    build_stage2_summary,
)
from big_boy_benchmarking.environments.plate_support.standard_gauntlet.contraction_schema_sweep.classification import (
    classify_schema_arm,
)
from big_boy_benchmarking.environments.plate_support.standard_gauntlet.contraction_schema_sweep.config import (
    SchemaSweepConfig,
)
from big_boy_benchmarking.environments.plate_support.standard_gauntlet.contraction_schema_sweep.docs_writer import (
    write_schema_sweep_docs,
)
from big_boy_benchmarking.environments.plate_support.standard_gauntlet.contraction_schema_sweep.manifests import (
    schema_family_manifest,
    stage_budget_lock,
    stage_input_manifest,
    stage_manifest,
    stage_output_manifest,
)
from big_boy_benchmarking.environments.plate_support.standard_gauntlet.contraction_schema_sweep.schema_builders import (
    construct_schema_arm,
)
from big_boy_benchmarking.environments.plate_support.standard_gauntlet.contraction_schema_sweep.schema_families import (
    enumerate_schema_arms,
)
from big_boy_benchmarking.environments.plate_support.standard_gauntlet.contraction_schema_sweep.schema_runner import (
    run_schema_tower_diagnostics,
)
from big_boy_benchmarking.environments.plate_support.standard_gauntlet.contraction_schema_sweep.stage1_source import (
    Stage1SourceError,
    load_stage1_source,
)
from big_boy_benchmarking.environments.plate_support.standard_gauntlet.ids import (
    CONTRACTION_SCHEMA_SWEEP_STAGE_ID,
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
    "schema_arm_summary": (
        "schema_id",
        "schema_family_id",
        "schema_seed",
        "selection_policy_id",
        "selection_rate",
        "selection_count",
        "state_feature_basis",
        "action_category_basis",
        "edge_basis",
        "schema_mode",
        "expected_role",
        "construction_supported",
        "unsupported_reason",
        "ratio_numerator",
        "ratio_denominator",
        "max_iterations",
        "selector_rule_id",
        "selection_mode",
    ),
    "schema_construction_summary": (
        "schema_id",
        "schema_family_id",
        "schema_seed",
        "construction_status",
        "schema_mode",
        "builder_surface",
        "blocking_reason",
    ),
    "schema_selection_summary": (
        "schema_id",
        "schema_family_id",
        "schema_seed",
        "selection_policy_id",
        "selection_rate",
        "selection_count",
        "state_feature_basis",
        "action_category_basis",
        "edge_basis",
        "schema_mode",
        "ratio_numerator",
        "ratio_denominator",
        "max_iterations",
        "selector_rule_id",
        "selection_mode",
    ),
    "tower_shape_summary": (
        "schema_id",
        "schema_family_id",
        "schema_seed",
        "tier_index",
        "max_depth",
        "state_cell_count",
        "action_cell_count",
        "largest_cell_share",
        "singleton_cell_share",
        "scheduled_assignment_count",
        "unscheduled_assignment_count",
        "depth_curve",
        "reset_event_count",
        "diagnostic_status",
    ),
    "tier_occupancy_summary": (
        "schema_id",
        "schema_family_id",
        "schema_seed",
        "tier_index",
        "current_state_cell",
        "state_cell_count",
        "outgoing_action_cell_count",
        "active_action_cell_count",
        "diagnostic_status",
    ),
    "tier_executability_summary": (
        "schema_id",
        "schema_family_id",
        "schema_seed",
        "tier_index",
        "tier_executable_from_current_state",
        "lift_success_probe_count",
        "lift_failure_probe_count",
        "active_action_cell_count",
        "diagnostic_status",
    ),
    "endpoint_coalescence_summary": (
        "schema_id",
        "schema_family_id",
        "schema_seed",
        "tier_index",
        "action_cell_count",
        "endpoint_pair_count",
        "endpoint_coalescence_count",
        "diagnostic_status",
    ),
    "collapse_diagnostic_summary": (
        "schema_id",
        "schema_family_id",
        "schema_seed",
        "structural_class",
        "largest_cell_share",
        "near_full_collapse_threshold",
        "blocking_reason",
    ),
    "schema_candidate_signal_summary": (
        "schema_id",
        "schema_family_id",
        "schema_seed",
        "structural_class",
        "candidate_signal",
        "candidate_signal_reason",
        "schema_mode",
        "selection_rate",
        "ratio_numerator",
        "ratio_denominator",
        "max_iterations",
        "selector_rule_id",
        "selection_mode",
        "max_depth",
        "nontrivial_tier_count",
        "first_nonbase_tier_state_cell_count",
        "largest_cell_share",
        "active_action_cell_min",
        "active_action_cell_mean",
        "lift_success_probe_count",
        "lift_failure_probe_count",
        "selected_edge_count",
        "zero_selected_source_count",
        "recommended_for_candidate_discovery",
        "blocking_reason",
        "near_full_collapse_threshold",
    ),
    "timing_summary": (
        "schema_id",
        "schema_family_id",
        "schema_seed",
        "timing_category",
        "duration_seconds",
        "diagnostic_status",
    ),
    "downstream_candidate_input_summary": (
        "schema_id",
        "schema_family_id",
        "schema_seed",
        "candidate_signal",
        "recommended_for_candidate_discovery",
        "structural_class",
        "source_stage_id",
        "source_artifact_root",
        "schema_mode",
        "selection_rate",
        "ratio_numerator",
        "ratio_denominator",
        "max_iterations",
        "selector_rule_id",
        "selection_mode",
        "max_depth",
        "nontrivial_tier_count",
        "blocking_reason",
    ),
    "iterated_plan_summary": (
        "schema_id",
        "schema_family_id",
        "schema_seed",
        "selector_rule_id",
        "selection_mode",
        "ratio_numerator",
        "ratio_denominator",
        "max_iterations",
        "iteration_index",
        "component_count_before",
        "candidate_edge_count",
        "selected_edge_count",
        "changed_union_count",
        "component_count_after",
        "block_id",
        "iteration_status",
        "stop_reason",
        "diagnostic_status",
    ),
    "iterated_schema_stop_summary": (
        "schema_id",
        "schema_family_id",
        "schema_seed",
        "selector_rule_id",
        "selection_mode",
        "ratio_numerator",
        "ratio_denominator",
        "max_iterations",
        "completed_iteration_count",
        "ordered_block_count",
        "final_component_count",
        "stop_reason",
        "selected_edge_count_total",
        "changed_union_count_total",
        "max_depth",
        "nontrivial_tier_count",
        "largest_cell_share_final",
        "near_full_collapse_threshold",
        "diagnostic_status",
    ),
    "many_tier_candidate_signal_summary": (
        "schema_id",
        "schema_family_id",
        "schema_seed",
        "selector_rule_id",
        "selection_mode",
        "ratio_numerator",
        "ratio_denominator",
        "max_iterations",
        "max_depth",
        "nontrivial_tier_count",
        "min_required_nontrivial_tiers",
        "has_immediate_collapse",
        "has_empty_executable_tier",
        "max_largest_cell_share",
        "min_nonbase_state_cell_count",
        "max_nonbase_state_cell_count",
        "min_nonbase_active_action_cell_count",
        "candidate_signal",
        "candidate_signal_reason",
        "near_full_collapse_threshold",
        "diagnostic_status",
    ),
}


@dataclass(frozen=True)
class SchemaSweepResult:
    """Run result for Stage 2."""

    status: str
    stage_root: Path
    readout_source_path: Path
    artifact_paths: dict[str, str]
    warning_count: int
    failure_reason: str | None = None


def run_contraction_schema_sweep(
    config: SchemaSweepConfig,
    *,
    repo_root: Path | str,
) -> SchemaSweepResult:
    """Run Stage 2 and write schema sweep diagnostics."""

    repo_root = Path(repo_root).expanduser().resolve()
    artifact_root = Path(config.artifact_root).expanduser().resolve()
    stage_root = artifact_root / "stages" / "contraction_schema_sweep"
    results_dir = stage_root / "results"
    results_dir.mkdir(parents=True, exist_ok=True)
    try:
        stage1 = load_stage1_source(config.stage1_readout_source_path, repo_root=repo_root)
    except Stage1SourceError as exc:
        return _write_blocked_result(config=config, repo_root=repo_root, stage_root=stage_root, reason=str(exc))

    valid_nonself_edge_count = int(stage1.downstream_readiness_row["valid_nonself_edge_count"])
    arms = enumerate_schema_arms(
        schema_families=config.schema_families,
        schema_seeds=config.schema_seeds,
        source_local_ratio_numerators=config.source_local_ratio_numerators,
        source_local_ratio_denominator=config.source_local_ratio_denominator,
        edge_global_numerators=config.edge_global_numerators,
        valid_nonself_edge_count=valid_nonself_edge_count,
        iterated_source_local_ratio_numerators=(
            config.iterated_source_local_ratio_numerators
        ),
        iterated_source_local_ratio_denominators=(
            config.iterated_source_local_ratio_denominators
        ),
        iterated_source_local_max_iterations=config.iterated_source_local_max_iterations,
        iterated_source_local_selector_rule_id=(
            config.iterated_source_local_selector_rule_id
        ),
        iterated_source_local_selection_mode=config.iterated_source_local_selection_mode,
        iterated_source_local_schema_seeds=config.iterated_source_local_schema_seeds,
    )
    dependency_state = collect_state_collapser_dependency_state(
        dependency_spec=STATE_COLLAPSER_DEPENDENCY_SPEC,
    ).to_dict()
    dependency_status = str(dependency_state.get("inspection_status", "unknown"))

    construction_rows: list[dict[str, object]] = []
    tower_rows: list[dict[str, object]] = []
    occupancy_rows: list[dict[str, object]] = []
    executability_rows: list[dict[str, object]] = []
    endpoint_rows: list[dict[str, object]] = []
    timing_rows: list[dict[str, object]] = []
    candidate_rows: list[dict[str, object]] = []
    iterated_plan_rows: list[dict[str, object]] = []
    iterated_stop_rows: list[dict[str, object]] = []
    many_tier_rows: list[dict[str, object]] = []
    mandatory_failures: list[str] = []

    for arm in arms:
        construction = construct_schema_arm(arm)
        construction_rows.append(construction.to_dict())
        diagnostics = run_schema_tower_diagnostics(
            arm=arm,
            construction=construction,
            config=config,
        )
        arm_tower_rows = list(diagnostics.tower_shape_rows)
        arm_executability_rows = list(diagnostics.tier_executability_rows)
        tower_rows.extend(arm_tower_rows)
        occupancy_rows.extend(diagnostics.tier_occupancy_rows)
        executability_rows.extend(arm_executability_rows)
        endpoint_rows.extend(diagnostics.endpoint_coalescence_rows)
        timing_rows.extend(diagnostics.timing_rows)
        iterated_plan_rows.extend(diagnostics.iterated_plan_rows)
        iterated_stop_rows.extend(diagnostics.iterated_schema_stop_rows)
        many_tier_rows.extend(diagnostics.many_tier_candidate_signal_rows)
        candidate_row = classify_schema_arm(
            arm=arm,
            construction=construction,
            tower_rows=arm_tower_rows,
            executability_rows=arm_executability_rows,
            near_full_collapse_threshold=(
                config.iterated_near_full_collapse_threshold
                if arm.schema_family_id == "source_local_ratio_iterated"
                else config.near_full_collapse_threshold
            ),
            iterated_min_nontrivial_tiers=config.iterated_min_nontrivial_tiers,
        )
        candidate_rows.append(candidate_row)
        if arm.schema_family_id in ("no_contraction", "upstream_default") and (
            construction.construction_status != "constructed"
        ):
            mandatory_failures.append(f"{arm.schema_id}:{construction.blocking_reason}")

    warning_count = sum(
        1
        for row in candidate_rows
        if row["candidate_signal"] in ("warning_signal", "blocked_signal")
    )
    aggregate_row = build_stage2_aggregate_row(
        artifact_root=str(stage_root),
        candidate_rows=candidate_rows,
        mandatory_failures=mandatory_failures,
        warning_count=warning_count,
        state_collapser_dependency_status=dependency_status,
    )
    aggregate_summary = build_stage2_summary(aggregate_row)

    output_paths = _write_result_tables(
        stage_root=stage_root,
        arms=arms,
        construction_rows=construction_rows,
        tower_rows=tower_rows,
        occupancy_rows=occupancy_rows,
        executability_rows=executability_rows,
        endpoint_rows=endpoint_rows,
        timing_rows=timing_rows,
        candidate_rows=candidate_rows,
        iterated_plan_rows=iterated_plan_rows,
        iterated_stop_rows=iterated_stop_rows,
        many_tier_rows=many_tier_rows,
    )
    write_json(stage_root / "stage_manifest.json", stage_manifest(config), create_parents=True)
    write_json(stage_root / "stage_budget_lock.json", stage_budget_lock(config), create_parents=True)
    write_json(stage_root / "stage_input_manifest.json", stage_input_manifest(stage1), create_parents=True)
    write_json(stage_root / "stage_source_manifest.json", stage_input_manifest(stage1), create_parents=True)
    write_json(stage_root / "schema_family_manifest.json", schema_family_manifest(arms), create_parents=True)
    write_json(
        stage_root / "schema_arm_manifest.json",
        {"schema_arms": [arm.to_dict() for arm in arms]},
        create_parents=True,
    )
    write_json(
        stage_root / "schema_construction_manifest.json",
        {"schema_construction": construction_rows},
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
                "stage_id": CONTRACTION_SCHEMA_SWEEP_STAGE_ID,
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

    readout_surface = suite_readout_surface(repo_root) / "contraction_schema_sweep"
    readout_source_path = readout_surface / "readout_source.json"
    readout_source = _stage2_readout_source(
        readout_surface=readout_surface,
        stage_root=stage_root,
        config=config,
        output_paths=output_paths,
    )
    write_json(readout_source_path, readout_source, create_parents=True)
    doc_paths = write_schema_sweep_docs(
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
        "stage_source_manifest": str(stage_root / "stage_source_manifest.json"),
        "schema_family_manifest": str(stage_root / "schema_family_manifest.json"),
        "schema_arm_manifest": str(stage_root / "schema_arm_manifest.json"),
        "schema_construction_manifest": str(stage_root / "schema_construction_manifest.json"),
        "stage_output_manifest": str(stage_root / "stage_output_manifest.json"),
        "stage_aggregate_summary": str(stage_root / "stage_aggregate_summary.json"),
        "stage_aggregate_table": str(stage_root / "stage_aggregate_table.csv"),
        "stage_run_index": str(stage_root / "stage_run_index.csv"),
        "readout_source": str(readout_source_path),
        **doc_paths,
    }
    return SchemaSweepResult(
        status=str(aggregate_row["status"]),
        stage_root=stage_root,
        readout_source_path=readout_source_path,
        artifact_paths=all_paths,
        warning_count=warning_count,
        failure_reason=None if aggregate_row["status"] == "complete" else str(aggregate_row["blocking_reason"]),
    )


def _write_result_tables(
    *,
    stage_root: Path,
    arms: tuple[object, ...],
    construction_rows: list[dict[str, object]],
    tower_rows: list[dict[str, object]],
    occupancy_rows: list[dict[str, object]],
    executability_rows: list[dict[str, object]],
    endpoint_rows: list[dict[str, object]],
    timing_rows: list[dict[str, object]],
    candidate_rows: list[dict[str, object]],
    iterated_plan_rows: list[dict[str, object]],
    iterated_stop_rows: list[dict[str, object]],
    many_tier_rows: list[dict[str, object]],
) -> dict[str, str]:
    results_dir = stage_root / "results"
    selection_rows = [
        {
            key: arm.to_dict()[key]
            for key in RESULT_TABLE_FIELDNAMES["schema_selection_summary"]
        }
        for arm in arms
    ]
    collapse_rows = [
        {
            key: row[key]
            for key in RESULT_TABLE_FIELDNAMES["collapse_diagnostic_summary"]
        }
        for row in candidate_rows
    ]
    downstream_rows = [
        {
            "schema_id": row["schema_id"],
            "schema_family_id": row["schema_family_id"],
            "schema_seed": row["schema_seed"],
            "candidate_signal": row["candidate_signal"],
            "recommended_for_candidate_discovery": row["recommended_for_candidate_discovery"],
            "structural_class": row["structural_class"],
            "source_stage_id": CONTRACTION_SCHEMA_SWEEP_STAGE_ID,
            "source_artifact_root": str(stage_root),
            "schema_mode": row["schema_mode"],
            "selection_rate": row["selection_rate"],
            "ratio_numerator": row["ratio_numerator"],
            "ratio_denominator": row["ratio_denominator"],
            "max_iterations": row["max_iterations"],
            "selector_rule_id": row["selector_rule_id"],
            "selection_mode": row["selection_mode"],
            "max_depth": row["max_depth"],
            "nontrivial_tier_count": row["nontrivial_tier_count"],
            "blocking_reason": row["blocking_reason"],
        }
        for row in candidate_rows
    ]
    tables = {
        "schema_arm_summary": [arm.to_dict() for arm in arms],
        "schema_construction_summary": construction_rows,
        "schema_selection_summary": selection_rows,
        "tower_shape_summary": tower_rows,
        "tier_occupancy_summary": occupancy_rows,
        "tier_executability_summary": executability_rows,
        "endpoint_coalescence_summary": endpoint_rows,
        "collapse_diagnostic_summary": collapse_rows,
        "schema_candidate_signal_summary": candidate_rows,
        "timing_summary": timing_rows,
        "downstream_candidate_input_summary": downstream_rows,
        "iterated_plan_summary": iterated_plan_rows,
        "iterated_schema_stop_summary": iterated_stop_rows,
        "many_tier_candidate_signal_summary": many_tier_rows,
    }
    output_paths: dict[str, str] = {}
    for key, rows in tables.items():
        path = results_dir / f"{key}.csv"
        write_csv(path, rows, RESULT_TABLE_FIELDNAMES[key], create_parents=True)
        output_paths[key] = str(path)
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
        row for row in prior_rows if row.get("stage_id") != CONTRACTION_SCHEMA_SWEEP_STAGE_ID
    ]
    stage_status_row = {field: aggregate_row[field] for field in STAGE_STATUS_FIELDS}
    write_csv(status_path, [*filtered, stage_status_row], STAGE_STATUS_FIELDS, create_parents=True)
    write_csv(
        suite_root / "stage_run_index.csv",
        [
            {
                "suite_id": SUITE_ID,
                "stage_id": CONTRACTION_SCHEMA_SWEEP_STAGE_ID,
                "run_label": run_label,
                "artifact_root": str(artifact_root),
                "status": aggregate_row["status"],
            }
        ],
        ("suite_id", "stage_id", "run_label", "artifact_root", "status"),
        create_parents=True,
    )


def _stage2_readout_source(
    *,
    readout_surface: Path,
    stage_root: Path,
    config: SchemaSweepConfig,
    output_paths: dict[str, str],
) -> dict[str, object]:
    required = tuple(RESULT_TABLE_FIELDNAMES)
    return {
        "artifact_schema_version": ARTIFACT_SCHEMA_VERSION,
        "source_binding_type": "evaluation_readout_source",
        "repo_readout_surface": str(readout_surface),
        "source_artifact_root": str(stage_root),
        "source_evaluation_root": str(stage_root),
        "evaluation_id": CONTRACTION_SCHEMA_SWEEP_STAGE_ID,
        "environment_family_id": ENVIRONMENT_FAMILY_ID,
        "environment_instance_id": ENVIRONMENT_INSTANCE_ID,
        "artifact_run_label": config.run_label,
        "run_mode": "stage2_schema_sweep",
        "source_files": {key: output_paths[key] for key in required},
        "expected_files": {
            "required": [output_paths[key] for key in required],
            "expected_absent_is_gap": [],
            "conditional": {},
            "not_applicable": [],
            "expectation_sources": [
                "docs/design/first_plate_support_environment/standard_gauntlet_suite/"
                "02_contraction_schema_sweep/"
                "01_001_plate_support_contraction_schema_sweep_blueprint.md"
            ],
        },
        "goal_criteria": [
            {
                "goal_id": "plate_support_stage2_schema_candidate_signals",
                "question": "Which PlateSupport schema arms are structured, degenerate, or blocked?",
                "success_signal": "schema_candidate_signal_summary.csv contains structured rows",
                "partial_signal": "mandatory arms run but custom arms are unsupported",
                "failure_signal": "mandatory no-contraction or upstream-default arms fail",
                "claim_if_met": "Stage 3 may consume candidate-signal rows",
                "claim_if_not_met": "Candidate discovery is blocked by schema sweep failure",
            }
        ],
        "structural_limit_checks": [
            {
                "check_id": "custom_schema_not_supported",
                "trigger": "schema_construction_summary.csv construction_status is not_supported",
                "interpretation_if_triggered": (
                    "The current upstream API cannot honestly represent that schema family."
                ),
                "claim_effect": "blocks that arm from candidate selection",
            }
        ],
        "goal_summary_sources": [
            "docs/design/first_plate_support_environment/standard_gauntlet_suite/"
            "02_contraction_schema_sweep/"
            "01_001_plate_support_contraction_schema_sweep_blueprint.md",
            str(readout_surface / "method.md"),
        ],
        "methodology_summary_sources": [
            "docs/design/first_plate_support_environment/standard_gauntlet_suite/"
            "02_contraction_schema_sweep/"
            "01_001_plate_support_contraction_schema_sweep_blueprint.md",
            str(readout_surface / "method.md"),
            str(readout_surface / "runbook.md"),
        ],
        "claim_boundary": [
            "Stage 2 may claim schema arms are flat, nonflat, degenerate, or unsupported",
            "Stage 2 may emit candidate signals for Stage 3",
            "Stage 2 may not select final candidates or claim training benefit",
        ],
    }


def _write_blocked_result(
    *,
    config: SchemaSweepConfig,
    repo_root: Path,
    stage_root: Path,
    reason: str,
) -> SchemaSweepResult:
    stage_root.mkdir(parents=True, exist_ok=True)
    readout_source_path = suite_readout_surface(repo_root) / "contraction_schema_sweep" / "readout_source.json"
    payload = {
        "artifact_schema_version": ARTIFACT_SCHEMA_VERSION,
        "suite_id": SUITE_ID,
        "stage_id": CONTRACTION_SCHEMA_SWEEP_STAGE_ID,
        "status": "blocked",
        "blocking_reason": reason,
        "run_label": config.run_label,
    }
    write_json(stage_root / "stage_aggregate_summary.json", payload, create_parents=True)
    return SchemaSweepResult(
        status="blocked",
        stage_root=stage_root,
        readout_source_path=readout_source_path,
        artifact_paths={"stage_aggregate_summary": str(stage_root / "stage_aggregate_summary.json")},
        warning_count=0,
        failure_reason=reason,
    )


def _now() -> str:
    return datetime.now(UTC).isoformat()
