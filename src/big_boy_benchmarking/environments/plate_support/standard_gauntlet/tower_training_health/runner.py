"""Runner for PlateSupport gauntlet Stage 4 tower training health."""

from __future__ import annotations

import csv
import random
import time
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
    SUITE_ID,
    TOWER_TRAINING_HEALTH_STAGE_ID,
)
from ..paths import (
    suite_evaluation_root,
    suite_readout_surface,
)
from ..status import (
    STAGE_STATUS_FIELDS,
)
from .aggregation import (
    build_stage4_aggregate_row,
    build_stage4_summary,
    build_stage4_tables,
)
from .candidate_source import (
    Stage3CandidateSource,
    Stage3CandidateSourceError,
    TrainingCandidate,
    load_stage3_candidate_source,
)
from .config import TowerTrainingHealthConfig
from .docs_writer import write_tower_training_health_docs
from .events import (
    CONCRETE_STEP_FIELDS,
    CONTROLLER_ACTION_FIELDS,
    EPISODE_FIELDS,
    LEARNER_UPDATE_FIELDS,
    LIFT_FIBER_FIELDS,
    TIER_TRANSITION_FIELDS,
    TIMING_FIELDS,
)
from .manifests import (
    candidate_manifest,
    parent_candidate_manifest,
    seed_bundle_payload,
    stage_budget_lock,
    stage_input_manifest,
    stage_manifest,
    stage_output_manifest,
    training_config_manifest,
    training_surface_manifest,
)
from .training_surfaces import (
    build_training_surface,
    cell_text,
    choose_executable_tower_action,
    next_state_best_value,
    state_payload_text,
)

RESULT_TABLE_FIELDNAMES = {
    "training_episode_summary": EPISODE_FIELDS,
    "training_curve_summary": (
        "candidate_id",
        "schema_id",
        "episode_index",
        "episode_count",
        "mean_total_reward",
        "success_rate",
        "mean_step_count",
    ),
    "concrete_step_summary": (
        "candidate_id",
        "schema_id",
        "run_count",
        "concrete_step_count",
        "valid_step_count",
        "invalid_move_count",
        "self_transition_count",
        "terminal_step_count",
    ),
    "lift_success_by_tier": (
        "candidate_id",
        "schema_id",
        "tier",
        "lift_success_count",
        "mean_executable_lift_count",
    ),
    "lift_failure_by_tier": (
        "candidate_id",
        "schema_id",
        "tier",
        "lift_failure_count",
        "failure_reasons",
    ),
    "tier_occupancy_summary": (
        "candidate_id",
        "schema_id",
        "tier",
        "controller_step_count",
        "controller_step_share",
    ),
    "tier_executability_summary": (
        "candidate_id",
        "schema_id",
        "tier",
        "controller_step_count",
        "min_active_action_cell_count",
        "mean_active_action_cell_count",
        "max_active_action_cell_count",
    ),
    "controller_action_summary": (
        "candidate_id",
        "schema_id",
        "tier",
        "action_index",
        "action_cell_id",
        "selection_count",
    ),
    "learner_update_summary": (
        "candidate_id",
        "schema_id",
        "learner_update_count",
        "mean_abs_td_error",
        "max_abs_td_error",
    ),
    "candidate_training_health_summary": (
        "candidate_id",
        "schema_id",
        "schema_mode",
        "ratio_numerator",
        "ratio_denominator",
        "max_iterations",
        "selector_rule_id",
        "selection_mode",
        "max_depth",
        "nontrivial_tier_count",
        "episode_count",
        "success_count",
        "concrete_step_count",
        "lift_success_count",
        "learner_update_count",
        "runtime_failure_count",
        "blocked_controller_step_count",
        "artifact_complete",
        "health_status",
        "health_reason",
    ),
    "downstream_comparison_input_summary": (
        "candidate_id",
        "schema_id",
        "schema_mode",
        "ratio_numerator",
        "ratio_denominator",
        "max_iterations",
        "selector_rule_id",
        "selection_mode",
        "max_depth",
        "nontrivial_tier_count",
        "health_status",
        "allowed_downstream_stage",
        "stage5_threshold_frontier_calibration",
        "stage6_paired_replicate_comparison",
        "source_artifact_root",
    ),
    "timing_summary": (
        "candidate_id",
        "schema_id",
        "run_id",
        "total_duration_seconds",
    ),
}


@dataclass(frozen=True)
class TowerTrainingHealthResult:
    """Run result for Stage 4."""

    status: str
    stage_root: Path
    readout_source_path: Path
    artifact_paths: dict[str, str]
    warning_count: int
    failure_reason: str | None = None


def run_tower_training_health(
    config: TowerTrainingHealthConfig,
    *,
    repo_root: Path | str,
) -> TowerTrainingHealthResult:
    """Run Stage 4 and write tower training-health artifacts."""

    repo_root = Path(repo_root).expanduser().resolve()
    artifact_root = Path(config.artifact_root).expanduser().resolve()
    stage_root = artifact_root / "stages" / "tower_training_health"
    results_dir = stage_root / "results"
    results_dir.mkdir(parents=True, exist_ok=True)
    try:
        source = load_stage3_candidate_source(
            config.candidate_source_path,
            repo_root=repo_root,
            allow_warning_candidates=config.allow_warning_candidates,
            candidate_cap=config.candidate_cap,
        )
    except Stage3CandidateSourceError as exc:
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
    raw_events = _run_training_candidates(config=config, stage_root=stage_root, source=source)
    tables = build_stage4_tables(
        candidates=source.selected_candidates,
        episode_rows=raw_events["episode_rows"],
        concrete_step_rows=raw_events["concrete_step_rows"],
        lift_rows=raw_events["lift_rows"],
        tier_rows=raw_events["tier_rows"],
        controller_rows=raw_events["controller_rows"],
        learner_rows=raw_events["learner_rows"],
        timing_rows=raw_events["timing_rows"],
        runtime_failure_rows=raw_events["runtime_failure_rows"],
    )
    output_paths = _write_result_tables(stage_root=stage_root, tables=tables)
    aggregate_row = build_stage4_aggregate_row(
        artifact_root=str(stage_root),
        health_rows=tables["candidate_training_health_summary"],
        state_collapser_dependency_status=dependency_status,
    )
    aggregate_summary = build_stage4_summary(aggregate_row)
    surface_manifest_payload = raw_events["training_surface_manifest"]
    write_json(
        stage_root / "stage_manifest.json",
        stage_manifest(config),
        create_parents=True,
    )
    write_json(
        stage_root / "stage_budget_lock.json",
        stage_budget_lock(config),
        create_parents=True,
    )
    write_json(
        stage_root / "stage_input_manifest.json",
        stage_input_manifest(source),
        create_parents=True,
    )
    write_json(
        stage_root / "candidate_manifest.json",
        candidate_manifest(source),
        create_parents=True,
    )
    write_json(
        stage_root / "training_config_manifest.json",
        training_config_manifest(config),
        create_parents=True,
    )
    write_json(
        stage_root / "training_surface_manifest.json",
        surface_manifest_payload,
        create_parents=True,
    )
    write_json(
        stage_root / "parent_candidate_manifest.json",
        parent_candidate_manifest(source),
        create_parents=True,
    )
    write_json(
        stage_root / "stage_output_manifest.json",
        stage_output_manifest(output_paths),
        create_parents=True,
    )
    write_json(stage_root / "stage_aggregate_summary.json", aggregate_summary, create_parents=True)
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
                "stage_id": TOWER_TRAINING_HEALTH_STAGE_ID,
                "run_label": config.run_label,
                "status": aggregate_row["status"],
                "started_at": raw_events["started_at"],
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
    readout_surface = suite_readout_surface(repo_root) / "tower_training_health"
    readout_source_path = readout_surface / "readout_source.json"
    write_json(
        readout_source_path,
        _stage4_readout_source(
            readout_surface=readout_surface,
            stage_root=stage_root,
            config=config,
            output_paths=output_paths,
        ),
        create_parents=True,
    )
    doc_paths = write_tower_training_health_docs(
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
        "candidate_manifest": str(stage_root / "candidate_manifest.json"),
        "training_config_manifest": str(stage_root / "training_config_manifest.json"),
        "training_surface_manifest": str(stage_root / "training_surface_manifest.json"),
        "parent_candidate_manifest": str(stage_root / "parent_candidate_manifest.json"),
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
    return TowerTrainingHealthResult(
        status=str(aggregate_row["status"]),
        stage_root=stage_root,
        readout_source_path=readout_source_path,
        artifact_paths=all_paths,
        warning_count=sum(
            row["health_status"] == "trainable_warning"
            for row in tables["candidate_training_health_summary"]
        ),
        failure_reason=failure_reason,
    )


def _run_training_candidates(
    *,
    config: TowerTrainingHealthConfig,
    stage_root: Path,
    source: Stage3CandidateSource,
) -> dict[str, object]:
    started_at = _now()
    episode_rows: list[dict[str, object]] = []
    concrete_step_rows: list[dict[str, object]] = []
    lift_rows: list[dict[str, object]] = []
    tier_rows: list[dict[str, object]] = []
    controller_rows: list[dict[str, object]] = []
    learner_rows: list[dict[str, object]] = []
    timing_rows: list[dict[str, object]] = []
    runtime_failure_rows: list[dict[str, object]] = []
    surface_manifest = training_surface_manifest(
        strategy_id="not_initialized",
        event_observability={"runner": "not_initialized"},
    )
    for candidate_index, candidate in enumerate(source.selected_candidates):
        for replicate_index in range(config.training_replicates_per_candidate):
            run_start = time.perf_counter()
            run_id = _run_id(config, candidate, replicate_index)
            run_dir = stage_root / "runs" / run_id
            run_dir.mkdir(parents=True, exist_ok=True)
            try:
                training_surface = build_training_surface(candidate)
                surface_manifest = training_surface_manifest(
                    strategy_id=training_surface.strategy_id,
                    event_observability=training_surface.event_observability,
                )
                q_table: dict[tuple[str, str, str], float] = {}
                rng = random.Random(
                    _replicate_seed(config, candidate_index, replicate_index)
                )
                for episode_index in range(config.episodes_per_replicate):
                    episode_seed = _episode_seed(
                        config,
                        candidate_index,
                        replicate_index,
                        episode_index,
                    )
                    episode = _run_episode(
                        config=config,
                        candidate=candidate,
                        run_id=run_id,
                        replicate_index=replicate_index,
                        episode_index=episode_index,
                        episode_seed=episode_seed,
                        training_surface=training_surface,
                        q_table=q_table,
                        rng=rng,
                    )
                    episode_rows.append(episode["episode_row"])
                    concrete_step_rows.extend(episode["concrete_step_rows"])
                    lift_rows.extend(episode["lift_rows"])
                    tier_rows.extend(episode["tier_rows"])
                    controller_rows.extend(episode["controller_rows"])
                    learner_rows.extend(episode["learner_rows"])
            except Exception as exc:  # pragma: no cover - exercised by artifact output
                runtime_failure_rows.append(
                    {
                        "candidate_id": candidate.candidate_id,
                        "schema_id": candidate.schema_id,
                        "run_id": run_id,
                        "replicate_index": replicate_index,
                        "failure_reason": repr(exc),
                    }
                )
            timing_rows.append(
                {
                    "candidate_id": candidate.candidate_id,
                    "schema_id": candidate.schema_id,
                    "run_id": run_id,
                    "segment_name": "run_total",
                    "duration_seconds": time.perf_counter() - run_start,
                }
            )
            _write_run_artifacts(
                run_dir=run_dir,
                config=config,
                candidate=candidate,
                run_id=run_id,
                replicate_index=replicate_index,
                episode_rows=[row for row in episode_rows if row["run_id"] == run_id],
                concrete_step_rows=[
                    row for row in concrete_step_rows if row["run_id"] == run_id
                ],
                lift_rows=[row for row in lift_rows if row["run_id"] == run_id],
                tier_rows=[row for row in tier_rows if row["run_id"] == run_id],
                controller_rows=[
                    row for row in controller_rows if row["run_id"] == run_id
                ],
                learner_rows=[row for row in learner_rows if row["run_id"] == run_id],
                timing_rows=[row for row in timing_rows if row["run_id"] == run_id],
            )
    return {
        "started_at": started_at,
        "episode_rows": episode_rows,
        "concrete_step_rows": concrete_step_rows,
        "lift_rows": lift_rows,
        "tier_rows": tier_rows,
        "controller_rows": controller_rows,
        "learner_rows": learner_rows,
        "timing_rows": timing_rows,
        "runtime_failure_rows": runtime_failure_rows,
        "training_surface_manifest": surface_manifest,
    }


def _run_episode(
    *,
    config: TowerTrainingHealthConfig,
    candidate: TrainingCandidate,
    run_id: str,
    replicate_index: int,
    episode_index: int,
    episode_seed: int,
    training_surface: object,
    q_table: dict[tuple[str, str, str], float],
    rng: random.Random,
) -> dict[str, object]:
    runtime = training_surface.runtime
    surface = training_surface.surface
    reset = runtime.reset(seed=episode_seed)
    snapshot = reset.runtime_snapshot
    total_reward = 0.0
    step_count = 0
    blocked_reason = ""
    goal_reached = False
    concrete_step_rows: list[dict[str, object]] = []
    lift_rows: list[dict[str, object]] = []
    tier_rows: list[dict[str, object]] = []
    controller_rows: list[dict[str, object]] = []
    learner_rows: list[dict[str, object]] = []
    terminated = False
    truncated = False
    for step_index in range(config.max_steps_per_episode):
        choice, selection_mode = choose_executable_tower_action(
            snapshot=snapshot,
            surface=surface,
            q_table=q_table,
            rng=rng,
            epsilon=config.epsilon,
        )
        if choice is None:
            blocked_reason = selection_mode
            tier_rows.append(
                _blocked_tier_row(
                    candidate=candidate,
                    run_id=run_id,
                    replicate_index=replicate_index,
                    episode_index=episode_index,
                    step_index=step_index,
                    blocked_reason=blocked_reason,
                )
            )
            break
        source_state = snapshot.current_base_state
        q_value_before = q_table.get(choice.q_key, 0.0)
        controller_rows.append(
            {
                "candidate_id": candidate.candidate_id,
                "schema_id": candidate.schema_id,
                "run_id": run_id,
                "replicate_index": replicate_index,
                "episode_index": episode_index,
                "step_index": step_index,
                "tier": choice.tier,
                "state_cell_id": cell_text(choice.state_cell_id),
                "action_cell_id": cell_text(choice.action_cell_id),
                "action_index": choice.action_index,
                "selection_mode": selection_mode,
                "q_value_before": q_value_before,
            }
        )
        lift_rows.append(
            {
                "candidate_id": candidate.candidate_id,
                "schema_id": candidate.schema_id,
                "run_id": run_id,
                "replicate_index": replicate_index,
                "episode_index": episode_index,
                "step_index": step_index,
                "tier": choice.tier,
                "state_cell_id": cell_text(choice.state_cell_id),
                "action_cell_id": cell_text(choice.action_cell_id),
                "candidate_lift_count": choice.candidate_lift_count,
                "executable_lift_count": choice.executable_lift_count,
                "selected_lift_source": state_payload_text(choice.selected_edge.source),
                "selected_lift_target": state_payload_text(choice.selected_edge.target),
                "selected_action_index": choice.action_index,
                "lift_status": "success",
                "failure_reason": "",
            }
        )
        step = runtime.step(choice.action_index)
        next_snapshot = step.runtime_snapshot
        reward = float(step.reward)
        total_reward += reward
        step_count += 1
        terminated = bool(step.terminated)
        truncated = bool(step.truncated)
        info = step.info or {}
        goal_reached = goal_reached or bool(info.get("goal_reached", False))
        target_state = next_snapshot.current_base_state
        concrete_step_rows.append(
            {
                "candidate_id": candidate.candidate_id,
                "schema_id": candidate.schema_id,
                "run_id": run_id,
                "replicate_index": replicate_index,
                "episode_index": episode_index,
                "step_index": step_index,
                "source_state": state_payload_text(source_state),
                "action_index": choice.action_index,
                "target_state": state_payload_text(target_state),
                "reward": reward,
                "terminated": terminated,
                "truncated": truncated,
                "valid_transition": bool(info.get("valid_transition", True)),
                "invalid_move": bool(info.get("invalid_move", False)),
                "self_transition": state_payload_text(source_state)
                == state_payload_text(target_state),
                "lift_status": "success",
            }
        )
        tier_after = _tier_after(choice.tier, next_snapshot)
        tier_rows.append(
            {
                "candidate_id": candidate.candidate_id,
                "schema_id": candidate.schema_id,
                "run_id": run_id,
                "replicate_index": replicate_index,
                "episode_index": episode_index,
                "step_index": step_index,
                "tier_before": choice.tier,
                "tier_after": choice.tier,
                "state_cell_before": cell_text(choice.state_cell_id),
                "state_cell_after": cell_text(tier_after),
                "active_action_cell_count": choice.executable_lift_count,
                "blocked_reason": "",
            }
        )
        next_best = 0.0 if terminated or truncated else next_state_best_value(
            snapshot=next_snapshot,
            surface=surface,
            q_table=q_table,
        )
        old_value = q_table.get(choice.q_key, 0.0)
        td_error = reward + config.discount * next_best - old_value
        new_value = old_value + config.learning_rate * td_error
        q_table[choice.q_key] = new_value
        learner_rows.append(
            {
                "candidate_id": candidate.candidate_id,
                "schema_id": candidate.schema_id,
                "run_id": run_id,
                "replicate_index": replicate_index,
                "episode_index": episode_index,
                "step_index": step_index,
                "learner_state_key": choice.q_key[1],
                "learner_action_key": choice.q_key[2],
                "reward": reward,
                "next_state_best_value": next_best,
                "td_error": td_error,
                "old_value": old_value,
                "new_value": new_value,
                "update_applied": True,
            }
        )
        snapshot = next_snapshot
        if terminated or truncated:
            break
    episode_row = {
        "candidate_id": candidate.candidate_id,
        "schema_id": candidate.schema_id,
        "run_id": run_id,
        "replicate_index": replicate_index,
        "episode_index": episode_index,
        "episode_seed": episode_seed,
        "status": "complete" if not blocked_reason else "controller_blocked",
        "step_count": step_count,
        "total_reward": total_reward,
        "terminated": terminated,
        "truncated": truncated,
        "goal_reached": goal_reached,
        "blocked_reason": blocked_reason,
    }
    return {
        "episode_row": episode_row,
        "concrete_step_rows": concrete_step_rows,
        "lift_rows": lift_rows,
        "tier_rows": tier_rows,
        "controller_rows": controller_rows,
        "learner_rows": learner_rows,
    }


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


def _write_run_artifacts(
    *,
    run_dir: Path,
    config: TowerTrainingHealthConfig,
    candidate: TrainingCandidate,
    run_id: str,
    replicate_index: int,
    episode_rows: list[dict[str, object]],
    concrete_step_rows: list[dict[str, object]],
    lift_rows: list[dict[str, object]],
    tier_rows: list[dict[str, object]],
    controller_rows: list[dict[str, object]],
    learner_rows: list[dict[str, object]],
    timing_rows: list[dict[str, object]],
) -> None:
    write_json(
        run_dir / "run_manifest.json",
        {
            "artifact_schema_version": ARTIFACT_SCHEMA_VERSION,
            "run_id": run_id,
            "candidate_id": candidate.candidate_id,
            "schema_id": candidate.schema_id,
            "replicate_index": replicate_index,
        },
        create_parents=True,
    )
    write_json(
        run_dir / "seed_bundle.json",
        seed_bundle_payload(
            run_id=run_id,
            candidate_id=candidate.candidate_id,
            replicate_index=replicate_index,
            base_seed=config.base_seed,
        ),
        create_parents=True,
    )
    write_csv(run_dir / "episodes.csv", episode_rows, EPISODE_FIELDS, create_parents=True)
    write_csv(
        run_dir / "concrete_step_events.csv",
        concrete_step_rows,
        CONCRETE_STEP_FIELDS,
        create_parents=True,
    )
    write_csv(
        run_dir / "lift_fiber_events.csv",
        lift_rows,
        LIFT_FIBER_FIELDS,
        create_parents=True,
    )
    write_csv(
        run_dir / "tier_transition_events.csv",
        tier_rows,
        TIER_TRANSITION_FIELDS,
        create_parents=True,
    )
    write_csv(
        run_dir / "controller_action_events.csv",
        controller_rows,
        CONTROLLER_ACTION_FIELDS,
        create_parents=True,
    )
    write_csv(
        run_dir / "learner_update_events.csv",
        learner_rows,
        LEARNER_UPDATE_FIELDS,
        create_parents=True,
    )
    write_csv(
        run_dir / "timing_segments.csv",
        timing_rows,
        TIMING_FIELDS,
        create_parents=True,
    )


def _blocked_tier_row(
    *,
    candidate: TrainingCandidate,
    run_id: str,
    replicate_index: int,
    episode_index: int,
    step_index: int,
    blocked_reason: str,
) -> dict[str, object]:
    return {
        "candidate_id": candidate.candidate_id,
        "schema_id": candidate.schema_id,
        "run_id": run_id,
        "replicate_index": replicate_index,
        "episode_index": episode_index,
        "step_index": step_index,
        "tier_before": "",
        "tier_after": "",
        "state_cell_before": "",
        "state_cell_after": "",
        "active_action_cell_count": 0,
        "blocked_reason": blocked_reason,
    }


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
        if row.get("stage_id") != TOWER_TRAINING_HEALTH_STAGE_ID
    ]
    stage_status_row = {field: aggregate_row[field] for field in STAGE_STATUS_FIELDS}
    write_csv(status_path, [*filtered, stage_status_row], STAGE_STATUS_FIELDS, create_parents=True)
    write_csv(
        suite_root / "stage_run_index.csv",
        [
            {
                "suite_id": SUITE_ID,
                "stage_id": TOWER_TRAINING_HEALTH_STAGE_ID,
                "run_label": run_label,
                "artifact_root": str(artifact_root),
                "status": aggregate_row["status"],
            }
        ],
        ("suite_id", "stage_id", "run_label", "artifact_root", "status"),
        create_parents=True,
    )


def _stage4_readout_source(
    *,
    readout_surface: Path,
    stage_root: Path,
    config: TowerTrainingHealthConfig,
    output_paths: dict[str, str],
) -> dict[str, object]:
    required = tuple(RESULT_TABLE_FIELDNAMES)
    return {
        "artifact_schema_version": ARTIFACT_SCHEMA_VERSION,
        "source_binding_type": "evaluation_readout_source",
        "repo_readout_surface": str(readout_surface),
        "source_artifact_root": str(stage_root),
        "source_evaluation_root": str(stage_root),
        "evaluation_id": TOWER_TRAINING_HEALTH_STAGE_ID,
        "environment_family_id": ENVIRONMENT_FAMILY_ID,
        "environment_instance_id": ENVIRONMENT_INSTANCE_ID,
        "artifact_run_label": config.run_label,
        "run_mode": "stage4_tower_training_health",
        "source_files": {key: output_paths[key] for key in required},
        "expected_files": {
            "required": [output_paths[key] for key in required],
            "expected_absent_is_gap": [],
            "conditional": {},
            "not_applicable": [],
            "expectation_sources": [
                "docs/design/first_plate_support_environment/standard_gauntlet_suite/"
                "04_tower_training_health/"
                "01_001_plate_support_tower_training_health_blueprint.md"
            ],
        },
        "goal_criteria": [
            {
                "goal_id": "plate_support_stage4_training_health",
                "question": (
                    "Can selected PlateSupport tower candidates emit training-health traces?"
                ),
                "success_signal": (
                    "candidate_training_health_summary.csv has trainable_clean or "
                    "trainable_warning rows"
                ),
                "partial_signal": "events exist but classifier records trainable_warning",
                "failure_signal": "no concrete steps, lift success, or learner updates",
                "claim_if_met": "Stage 5 threshold frontier calibration may run",
                "claim_if_not_met": "Stage 5 is blocked by training_health_blocked",
            }
        ],
        "claim_boundary": [
            "Stage 4 may claim tower-only training health status",
            "Stage 4 may not claim calibrated thresholds or tower-vs-flat benefit",
        ],
        "goal_summary_sources": [
            "docs/design/first_plate_support_environment/standard_gauntlet_suite/"
            "04_tower_training_health/"
            "01_001_plate_support_tower_training_health_blueprint.md",
            str(readout_surface / "method.md"),
        ],
        "methodology_summary_sources": [
            "docs/design/first_plate_support_environment/standard_gauntlet_suite/"
            "04_tower_training_health/"
            "01_001_plate_support_tower_training_health_blueprint.md",
            str(readout_surface / "method.md"),
            str(readout_surface / "runbook.md"),
        ],
    }


def _write_blocked_result(
    *,
    config: TowerTrainingHealthConfig,
    repo_root: Path,
    stage_root: Path,
    reason: str,
) -> TowerTrainingHealthResult:
    stage_root.mkdir(parents=True, exist_ok=True)
    readout_source_path = (
        suite_readout_surface(repo_root) / "tower_training_health" / "readout_source.json"
    )
    payload = {
        "artifact_schema_version": ARTIFACT_SCHEMA_VERSION,
        "suite_id": SUITE_ID,
        "stage_id": TOWER_TRAINING_HEALTH_STAGE_ID,
        "status": "blocked",
        "blocking_reason": reason,
        "run_label": config.run_label,
    }
    write_json(stage_root / "stage_aggregate_summary.json", payload, create_parents=True)
    return TowerTrainingHealthResult(
        status="blocked",
        stage_root=stage_root,
        readout_source_path=readout_source_path,
        artifact_paths={
            "stage_aggregate_summary": str(stage_root / "stage_aggregate_summary.json")
        },
        warning_count=0,
        failure_reason=reason,
    )


def _select_fields(row: dict[str, object], fieldnames: tuple[str, ...]) -> dict[str, object]:
    return {field: row.get(field, "") for field in fieldnames}


def _run_id(
    config: TowerTrainingHealthConfig,
    candidate: TrainingCandidate,
    replicate_index: int,
) -> str:
    safe_candidate = "".join(
        character if character.isalnum() else "-"
        for character in candidate.candidate_id
    ).strip("-")
    return f"{config.run_label}-{safe_candidate}-trainrep{replicate_index}"


def _replicate_seed(
    config: TowerTrainingHealthConfig,
    candidate_index: int,
    replicate_index: int,
) -> int:
    return config.base_seed + candidate_index * 100_000 + replicate_index * 1_000


def _episode_seed(
    config: TowerTrainingHealthConfig,
    candidate_index: int,
    replicate_index: int,
    episode_index: int,
) -> int:
    return _replicate_seed(config, candidate_index, replicate_index) + episode_index


def _tier_after(tier: int, snapshot: object) -> object:
    positions = getattr(snapshot, "current_position_at_every_tier", ())
    if tier < len(positions):
        return positions[tier]
    return ""


def _now() -> str:
    return datetime.now(UTC).isoformat()
