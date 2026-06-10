"""Runner for Warehouse masked direct vs live-lift tower diagnostics."""

from __future__ import annotations

import csv
import sys
import time
from dataclasses import dataclass
from pathlib import Path
from typing import Any

from big_boy_benchmarking.artifacts.writers import append_jsonl, write_csv, write_json
from big_boy_benchmarking.environments.warehouse_gridlock.instances import load_instance
from big_boy_benchmarking.environments.warehouse_gridlock.rewards import (
    is_terminal,
    target_counts,
)
from big_boy_benchmarking.environments.warehouse_gridlock.state import (
    WarehouseGridlockState,
)
from big_boy_benchmarking.environments.warehouse_gridlock.masked_direct_vs_live_lift_tower.admissibility import (
    direct_mask_event_row,
    mask_direct_candidates,
    mask_tower_action_candidates,
    tower_action_mask_event_row,
)
from big_boy_benchmarking.environments.warehouse_gridlock.masked_direct_vs_live_lift_tower.aggregation import (
    aggregate_results,
)
from big_boy_benchmarking.environments.warehouse_gridlock.masked_direct_vs_live_lift_tower.candidate_generation import (
    DirectActionCandidate,
    generate_direct_candidates,
)
from big_boy_benchmarking.environments.warehouse_gridlock.masked_direct_vs_live_lift_tower.config import (
    CONTROLLER_POLICY_ID,
    DIRECT_ARM_ID,
    DIRECT_CANDIDATE_POLICY_ID,
    EVALUATION_ID,
    TOWER_ARM_ID,
    TOWER_CANDIDATE_POLICY_ID,
    MaskedDirectVsLiveLiftConfig,
)
from big_boy_benchmarking.environments.warehouse_gridlock.masked_direct_vs_live_lift_tower.docs_writer import (
    write_human_docs,
    write_readout_source,
)
from big_boy_benchmarking.environments.warehouse_gridlock.masked_direct_vs_live_lift_tower.events import (
    DIRECT_CANDIDATE_FIELDNAMES,
    DIRECT_MASK_FIELDNAMES,
    EPISODE_FIELDNAMES,
    LEARNER_UPDATE_FIELDNAMES,
    RUN_INDEX_FIELDNAMES,
    STEP_FIELDNAMES,
    SUCCESSOR_DIAGNOSTIC_FIELDNAMES,
    TIMING_SEGMENT_FIELDNAMES,
    TOWER_ACTION_MASK_FIELDNAMES,
    TOWER_SHAPE_FIELDNAMES,
    TOWER_STATE_LIFT_FIELDNAMES,
    TOWER_SURFACE_SCOPE_FIELDNAMES,
)
from big_boy_benchmarking.environments.warehouse_gridlock.masked_direct_vs_live_lift_tower.manifests import (
    write_initial_manifests,
    write_run_manifest,
)
from big_boy_benchmarking.environments.warehouse_gridlock.masked_direct_vs_live_lift_tower.paths import (
    EvaluationPaths,
    run_id as build_run_id,
)
from big_boy_benchmarking.environments.warehouse_gridlock.masked_direct_vs_live_lift_tower.readiness_source import (
    load_readiness_source,
    validate_readiness_source,
)
from big_boy_benchmarking.environments.warehouse_gridlock.masked_direct_vs_live_lift_tower.tower_surface import (
    build_tower_surface,
    select_live_lift,
    tower_state_lift_event_row,
)


@dataclass(frozen=True)
class WarehouseMaskedTowerResult:
    status: str
    artifact_paths: dict[str, str]
    summary: dict[str, object]


@dataclass
class _RunRows:
    episode_rows: list[dict[str, object]]
    step_rows: list[dict[str, object]]
    direct_candidate_rows: list[dict[str, object]]
    direct_mask_rows: list[dict[str, object]]
    tower_lift_rows: list[dict[str, object]]
    tower_action_mask_rows: list[dict[str, object]]
    successor_rows: list[dict[str, object]]
    learner_rows: list[dict[str, object]]
    timing_rows: list[dict[str, object]]
    tower_surface_rows: list[dict[str, object]]
    tower_shape_rows: list[dict[str, object]]


def run_masked_direct_vs_live_lift_tower(
    config: MaskedDirectVsLiveLiftConfig,
) -> WarehouseMaskedTowerResult:
    started = time.perf_counter()
    paths = EvaluationPaths(repo_root=config.repo_root, artifact_root=config.artifact_root)
    paths.ensure()
    readiness_source = load_readiness_source(config.readiness_source)
    validate_readiness_source(readiness_source, expected_instance_id=config.instance_id)
    instance = load_instance(instance_id=config.instance_id)
    manifest_paths = write_initial_manifests(
        paths=paths,
        config=config,
        instance=instance,
        readiness_source=readiness_source,
    )

    all_episode_rows: list[dict[str, object]] = []
    all_step_rows: list[dict[str, object]] = []
    all_direct_candidate_rows: list[dict[str, object]] = []
    all_direct_mask_rows: list[dict[str, object]] = []
    all_tower_lift_rows: list[dict[str, object]] = []
    all_tower_action_mask_rows: list[dict[str, object]] = []
    all_successor_rows: list[dict[str, object]] = []
    all_learner_rows: list[dict[str, object]] = []
    all_timing_rows: list[dict[str, object]] = []
    all_tower_surface_rows: list[dict[str, object]] = []
    all_tower_shape_rows: list[dict[str, object]] = []
    run_index_rows: list[dict[str, object]] = []
    total_runs = config.schema_seeds * config.replicates_per_arm * len((DIRECT_ARM_ID, TOWER_ARM_ID))
    progress = _ProgressReporter(paths=paths, config=config, total_runs=total_runs)
    progress.record_evaluation_start()

    for schema_seed in range(config.schema_seeds):
        for replicate_index in range(config.replicates_per_arm):
            for arm_id in (DIRECT_ARM_ID, TOWER_ARM_ID):
                current_run_id = build_run_id(
                    arm_id=arm_id,
                    replicate_index=replicate_index,
                    schema_seed=schema_seed,
                    run_label=config.run_label,
                )
                run_root = paths.run_root(current_run_id)
                run_root.mkdir(parents=True, exist_ok=True)
                seed = config.seed + schema_seed * 1000 + replicate_index * 100
                progress.record_run_start(
                    run_id=current_run_id,
                    arm_id=arm_id,
                    replicate_index=replicate_index,
                    schema_seed=schema_seed,
                )
                rows = _run_arm(
                    instance=instance,
                    config=config,
                    arm_id=arm_id,
                    run_id=current_run_id,
                    replicate_index=replicate_index,
                    schema_seed=schema_seed,
                    seed=seed,
                    progress=progress,
                )
                progress.record_run_complete(
                    run_id=current_run_id,
                    arm_id=arm_id,
                    replicate_index=replicate_index,
                    schema_seed=schema_seed,
                )
                _write_run_rows(run_root=run_root, rows=rows)
                write_run_manifest(
                    run_root / "run_manifest.json",
                    {
                        "evaluation_id": EVALUATION_ID,
                        "run_id": current_run_id,
                        "arm_id": arm_id,
                        "replicate_index": replicate_index,
                        "schema_seed": schema_seed,
                        "run_label": config.run_label,
                    },
                )
                write_json(
                    run_root / "seed_bundle.json",
                    {
                        "seed": seed,
                        "schema_seed": schema_seed,
                        "replicate_index": replicate_index,
                    },
                    create_parents=True,
                )
                all_episode_rows.extend(rows.episode_rows)
                all_step_rows.extend(rows.step_rows)
                all_direct_candidate_rows.extend(rows.direct_candidate_rows)
                all_direct_mask_rows.extend(rows.direct_mask_rows)
                all_tower_lift_rows.extend(rows.tower_lift_rows)
                all_tower_action_mask_rows.extend(rows.tower_action_mask_rows)
                all_successor_rows.extend(rows.successor_rows)
                all_learner_rows.extend(rows.learner_rows)
                all_timing_rows.extend(rows.timing_rows)
                all_tower_surface_rows.extend(rows.tower_surface_rows)
                all_tower_shape_rows.extend(rows.tower_shape_rows)
                run_index_rows.append(
                    {
                        "run_id": current_run_id,
                        "arm_id": arm_id,
                        "replicate_index": replicate_index,
                        "schema_seed": schema_seed,
                        "episode_count": config.episodes_per_arm,
                        "max_seconds_per_episode": config.max_seconds_per_episode,
                        "candidate_proposals_per_step": config.candidate_proposals_per_step,
                        "max_active_robots": config.max_active_robots,
                        "candidate_mix_id": config.candidate_mix_id,
                        "run_root": str(run_root),
                        "status": "success",
                        "failure_reason": "",
                    }
                )

    _write_evaluation_level_tables(
        paths=paths,
        run_index_rows=run_index_rows,
        direct_candidate_rows=all_direct_candidate_rows,
        direct_mask_rows=all_direct_mask_rows,
        tower_lift_rows=all_tower_lift_rows,
        tower_action_mask_rows=all_tower_action_mask_rows,
        successor_rows=all_successor_rows,
        learner_rows=all_learner_rows,
        timing_rows=all_timing_rows,
        tower_surface_rows=all_tower_surface_rows,
        tower_shape_rows=all_tower_shape_rows,
    )
    summary = aggregate_results(
        paths=paths,
        run_label=config.run_label,
        episode_rows=all_episode_rows,
        direct_candidate_rows=all_direct_candidate_rows,
        direct_mask_rows=all_direct_mask_rows,
        tower_lift_rows=all_tower_lift_rows,
        no_lookahead_rows=all_successor_rows,
    )
    readout_source_path = write_readout_source(paths=paths, run_label=config.run_label, summary=summary)
    docs = write_human_docs(paths=paths, run_label=config.run_label, summary=summary)
    elapsed = time.perf_counter() - started
    summary = {**summary, "duration_seconds": elapsed}
    progress.record_evaluation_complete(status="success", duration_seconds=elapsed)
    artifact_paths = {
        **manifest_paths,
        "run_index": str(paths.run_index),
        "progress_events": str(paths.progress_events),
        "aggregate_summary": str(paths.aggregate_summary),
        "readout_source": str(readout_source_path),
        **docs,
    }
    return WarehouseMaskedTowerResult(status="success", artifact_paths=artifact_paths, summary=summary)


def summarize_masked_direct_vs_live_lift_tower(
    *,
    repo_root: Path,
    artifact_root: Path,
) -> WarehouseMaskedTowerResult:
    paths = EvaluationPaths(repo_root=repo_root, artifact_root=artifact_root)
    episode_rows = _read_run_csvs(paths=paths, filename="episode_events.csv")
    direct_candidate_rows = _read_run_csvs(paths=paths, filename="direct_candidate_events.csv")
    direct_mask_rows = _read_run_csvs(paths=paths, filename="direct_admissibility_mask_events.csv")
    tower_lift_rows = _read_run_csvs(paths=paths, filename="tower_state_lift_events.csv")
    successor_rows = _read_run_csvs(paths=paths, filename="successor_diagnostic_events.csv")
    run_label = artifact_root.name
    summary = aggregate_results(
        paths=paths,
        run_label=run_label,
        episode_rows=episode_rows,
        direct_candidate_rows=direct_candidate_rows,
        direct_mask_rows=direct_mask_rows,
        tower_lift_rows=tower_lift_rows,
        no_lookahead_rows=successor_rows,
    )
    readout_source_path = write_readout_source(paths=paths, run_label=run_label, summary=summary)
    docs = write_human_docs(paths=paths, run_label=run_label, summary=summary)
    return WarehouseMaskedTowerResult(
        status=str(summary.get("status", "success")),
        artifact_paths={"readout_source": str(readout_source_path), **docs},
        summary=summary,
    )


def _run_arm(
    *,
    instance,
    config: MaskedDirectVsLiveLiftConfig,
    arm_id: str,
    run_id: str,
    replicate_index: int,
    schema_seed: int,
    seed: int,
    progress: "_ProgressReporter",
) -> _RunRows:
    rows = _RunRows([], [], [], [], [], [], [], [], [], [], [])
    q_values: dict[str, float] = {}
    run_started = time.perf_counter()
    for episode_index in range(config.episodes_per_arm):
        state = instance.start_state
        total_reward = 0.0
        valid_selected = 0
        invalid_selected = 0
        initial_counts = target_counts(
            state,
            robot_targets=instance.manifest.robot_target_map(),
            box_targets=instance.manifest.box_target_map(),
        )
        failure_reason = ""
        for step_index in range(config.max_seconds_per_episode):
            if arm_id == DIRECT_ARM_ID:
                step_payload = _direct_step(
                    instance=instance,
                    config=config,
                    state=state,
                    run_id=run_id,
                    arm_id=arm_id,
                    episode_index=episode_index,
                    step_index=step_index,
                    seed=seed + episode_index * 1000 + step_index,
                    q_values=q_values,
                    rows=rows,
                )
            else:
                step_payload = _tower_step(
                    instance=instance,
                    config=config,
                    state=state,
                    run_id=run_id,
                    arm_id=arm_id,
                    episode_index=episode_index,
                    step_index=step_index,
                    seed=seed + episode_index * 1000 + step_index,
                    schema_seed=schema_seed,
                    q_values=q_values,
                    rows=rows,
                )
            if step_payload is None:
                failure_reason = "no_admissible_candidate_or_live_lift"
                break
            result = step_payload["result"]
            selected = step_payload["selected"]
            previous_value = q_values.get(selected.candidate_id, 0.0)
            new_value = previous_value + 0.1 * (result.reward - previous_value)
            q_values[selected.candidate_id] = new_value
            total_reward += result.reward
            valid_selected += int(result.valid)
            invalid_selected += int(not result.valid)
            counts = target_counts(
                result.next_state,
                robot_targets=instance.manifest.robot_target_map(),
                box_targets=instance.manifest.box_target_map(),
            )
            rows.step_rows.append(
                {
                    "run_id": run_id,
                    "arm_id": arm_id,
                    "replicate_index": replicate_index,
                    "schema_seed": schema_seed,
                    "episode_index": episode_index,
                    "step_index": step_index,
                    "state_id": state.stable_id,
                    "selected_action_id": selected.action.stable_id,
                    "selected_action_summary": selected.action_summary(),
                    "valid": result.valid,
                    "reward": result.reward,
                    "terminated": result.terminated,
                    "truncated": result.truncated,
                    "next_state_id": result.next_state.stable_id,
                    "correct_box_count": counts["correct_box_count"],
                    "correct_robot_count": counts["correct_robot_count"],
                    "invalid_reasons": "|".join(result.invalid_reasons),
                }
            )
            rows.learner_rows.append(
                {
                    "run_id": run_id,
                    "arm_id": arm_id,
                    "episode_index": episode_index,
                    "step_index": step_index,
                    "learner_key": selected.candidate_id,
                    "previous_value": previous_value,
                    "reward": result.reward,
                    "next_estimate": 0.0,
                    "new_value": new_value,
                    "controller_policy_id": CONTROLLER_POLICY_ID,
                }
            )
            _record_successor_diagnostic(
                instance=instance,
                config=config,
                rows=rows,
                run_id=run_id,
                arm_id=arm_id,
                episode_index=episode_index,
                step_index=step_index,
                selected_action_id=selected.action.stable_id,
                successor_state=result.next_state,
                seed=seed + 900_000 + episode_index * 1000 + step_index,
            )
            state = result.next_state
            if result.terminated or result.truncated:
                break
        final_counts = target_counts(
            state,
            robot_targets=instance.manifest.robot_target_map(),
            box_targets=instance.manifest.box_target_map(),
        )
        terminal = is_terminal(
            state,
            robot_targets=instance.manifest.robot_target_map(),
            box_targets=instance.manifest.box_target_map(),
        )
        episode_row = {
            "run_id": run_id,
            "arm_id": arm_id,
            "replicate_index": replicate_index,
            "schema_seed": schema_seed,
            "episode_index": episode_index,
            "status": "success" if not failure_reason else "blocked",
            "failure_reason": failure_reason,
            "total_reward": total_reward,
            "initial_correct_box_count": initial_counts["correct_box_count"],
            "final_correct_box_count": final_counts["correct_box_count"],
            "initial_correct_robot_count": initial_counts["correct_robot_count"],
            "final_correct_robot_count": final_counts["correct_robot_count"],
            "terminal_success": terminal,
            "terminated": terminal,
            "truncated": state.time_step >= config.max_seconds_per_episode and not terminal,
            "selected_step_count": valid_selected + invalid_selected,
            "valid_selected_step_count": valid_selected,
            "invalid_selected_step_count": invalid_selected,
        }
        rows.episode_rows.append(episode_row)
        progress.record_episode_complete(episode_row)
    rows.timing_rows.append(
        {
            "run_id": run_id,
            "arm_id": arm_id,
            "segment": "run_total",
            "duration_seconds": time.perf_counter() - run_started,
        }
    )
    return rows


class _ProgressReporter:
    def __init__(
        self,
        *,
        paths: EvaluationPaths,
        config: MaskedDirectVsLiveLiftConfig,
        total_runs: int,
    ) -> None:
        self.paths = paths
        self.config = config
        self.total_runs = total_runs
        self.total_episodes = max(1, total_runs * config.episodes_per_arm)
        self.completed_episodes = 0
        self.completed_runs = 0
        self.started = time.perf_counter()
        self.enabled = config.progress_every_episodes > 0
        if self.enabled:
            paths.progress_events.write_text("", encoding="utf-8")

    def record_evaluation_start(self) -> None:
        self._emit(
            {
                "event_type": "evaluation_start",
                "run_label": self.config.run_label,
                "total_runs": self.total_runs,
                "total_episodes": self.total_episodes,
                "episodes_per_arm": self.config.episodes_per_arm,
                "replicates_per_arm": self.config.replicates_per_arm,
                "schema_seeds": self.config.schema_seeds,
                "max_seconds_per_episode": self.config.max_seconds_per_episode,
                "candidate_proposals_per_step": self.config.candidate_proposals_per_step,
                "max_active_robots": self.config.max_active_robots,
                "candidate_mix_id": self.config.candidate_mix_id,
            },
            force_stderr=True,
        )

    def record_run_start(
        self,
        *,
        run_id: str,
        arm_id: str,
        replicate_index: int,
        schema_seed: int,
    ) -> None:
        self._emit(
            {
                "event_type": "run_start",
                "run_id": run_id,
                "arm_id": arm_id,
                "replicate_index": replicate_index,
                "schema_seed": schema_seed,
                "completed_runs": self.completed_runs,
                "total_runs": self.total_runs,
            },
            force_stderr=True,
        )

    def record_episode_complete(self, episode_row: dict[str, object]) -> None:
        self.completed_episodes += 1
        should_print = (
            self.completed_episodes == self.total_episodes
            or self.completed_episodes % self.config.progress_every_episodes == 0
        )
        self._emit(
            {
                "event_type": "episode_complete",
                "completed_episodes": self.completed_episodes,
                "total_episodes": self.total_episodes,
                "percent_complete": round(
                    100.0 * self.completed_episodes / self.total_episodes,
                    3,
                ),
                "elapsed_seconds": round(time.perf_counter() - self.started, 3),
                **episode_row,
            },
            force_stderr=should_print,
        )

    def record_run_complete(
        self,
        *,
        run_id: str,
        arm_id: str,
        replicate_index: int,
        schema_seed: int,
    ) -> None:
        self.completed_runs += 1
        self._emit(
            {
                "event_type": "run_complete",
                "run_id": run_id,
                "arm_id": arm_id,
                "replicate_index": replicate_index,
                "schema_seed": schema_seed,
                "completed_runs": self.completed_runs,
                "total_runs": self.total_runs,
                "completed_episodes": self.completed_episodes,
                "total_episodes": self.total_episodes,
                "elapsed_seconds": round(time.perf_counter() - self.started, 3),
            },
            force_stderr=True,
        )

    def record_evaluation_complete(self, *, status: str, duration_seconds: float) -> None:
        self._emit(
            {
                "event_type": "evaluation_complete",
                "status": status,
                "completed_runs": self.completed_runs,
                "total_runs": self.total_runs,
                "completed_episodes": self.completed_episodes,
                "total_episodes": self.total_episodes,
                "duration_seconds": round(duration_seconds, 3),
            },
            force_stderr=True,
        )

    def _emit(self, payload: dict[str, object], *, force_stderr: bool) -> None:
        if not self.enabled:
            return
        append_jsonl(self.paths.progress_events, payload, create_parents=True)
        if self.config.progress_to_stderr and force_stderr:
            print(_progress_line(payload), file=sys.stderr, flush=True)


def _progress_line(payload: dict[str, object]) -> str:
    event_type = str(payload.get("event_type", "progress"))
    if event_type == "episode_complete":
        return (
            "[warehouse progress] "
            f"{payload.get('completed_episodes')}/{payload.get('total_episodes')} episodes "
            f"({payload.get('percent_complete')}%) "
            f"arm={payload.get('arm_id')} "
            f"rep={payload.get('replicate_index')} "
            f"schema={payload.get('schema_seed')} "
            f"episode={payload.get('episode_index')} "
            f"reward={payload.get('total_reward')} "
            f"boxes={payload.get('final_correct_box_count')} "
            f"robots={payload.get('final_correct_robot_count')} "
            f"terminal={payload.get('terminal_success')} "
            f"elapsed={payload.get('elapsed_seconds')}s"
        )
    if event_type == "run_start":
        return (
            "[warehouse progress] "
            f"run start {payload.get('completed_runs')}/{payload.get('total_runs')} "
            f"arm={payload.get('arm_id')} rep={payload.get('replicate_index')} "
            f"schema={payload.get('schema_seed')}"
        )
    if event_type == "run_complete":
        return (
            "[warehouse progress] "
            f"run complete {payload.get('completed_runs')}/{payload.get('total_runs')} "
            f"arm={payload.get('arm_id')} "
            f"episodes={payload.get('completed_episodes')}/{payload.get('total_episodes')} "
            f"elapsed={payload.get('elapsed_seconds')}s"
        )
    if event_type == "evaluation_start":
        return (
            "[warehouse progress] "
            f"start run_label={payload.get('run_label')} "
            f"runs={payload.get('total_runs')} episodes={payload.get('total_episodes')} "
            f"candidates={payload.get('candidate_proposals_per_step')} "
            f"max_active={payload.get('max_active_robots')}"
        )
    if event_type == "evaluation_complete":
        return (
            "[warehouse progress] "
            f"complete status={payload.get('status')} "
            f"runs={payload.get('completed_runs')}/{payload.get('total_runs')} "
            f"episodes={payload.get('completed_episodes')}/{payload.get('total_episodes')} "
            f"duration={payload.get('duration_seconds')}s"
        )
    return f"[warehouse progress] {event_type}"


def _direct_step(
    *,
    instance,
    config: MaskedDirectVsLiveLiftConfig,
    state: WarehouseGridlockState,
    run_id: str,
    arm_id: str,
    episode_index: int,
    step_index: int,
    seed: int,
    q_values: dict[str, float],
    rows: _RunRows,
) -> dict[str, Any] | None:
    candidates = generate_direct_candidates(
        instance=instance,
        state=state,
        budget=config.candidate_proposals_per_step,
        seed=seed,
        max_active_robots=config.max_active_robots,
        candidate_mix_id=config.candidate_mix_id,
    )
    rows.direct_candidate_rows.extend(
        candidate.to_event_row(
            run_id=run_id,
            arm_id=arm_id,
            episode_index=episode_index,
            step_index=step_index,
            state=state,
        )
        for candidate in candidates
    )
    mask_result = mask_direct_candidates(
        instance=instance,
        state=state,
        candidates=candidates,
        max_seconds=config.max_seconds_per_episode,
    )
    selected = _select_candidate(mask_result.admissible_direct_candidates, q_values)
    rows.direct_mask_rows.append(
        direct_mask_event_row(
            run_id=run_id,
            arm_id=arm_id,
            episode_index=episode_index,
            step_index=step_index,
            state_id=state.stable_id,
            candidate_generation_policy_id=DIRECT_CANDIDATE_POLICY_ID,
            mask_result=mask_result,
            selected_action_id=selected.action.stable_id if selected else None,
        )
    )
    if selected is None:
        return None
    query = next(result for result in mask_result.query_results if result.candidate_id == selected.candidate_id)
    return {"selected": selected, "result": query.result}


def _tower_step(
    *,
    instance,
    config: MaskedDirectVsLiveLiftConfig,
    state: WarehouseGridlockState,
    run_id: str,
    arm_id: str,
    episode_index: int,
    step_index: int,
    seed: int,
    schema_seed: int,
    q_values: dict[str, float],
    rows: _RunRows,
) -> dict[str, Any] | None:
    surface = build_tower_surface(
        instance=instance,
        state=state,
        candidate_budget=config.candidate_proposals_per_step,
        seed=seed,
        schema_seed=schema_seed,
        max_seconds=config.max_seconds_per_episode,
        max_active_robots=config.max_active_robots,
        candidate_mix_id=config.candidate_mix_id,
    )
    rows.tower_surface_rows.append(surface.surface_scope_row(run_id=run_id))
    rows.tower_shape_rows.extend(surface.tower_shape_rows(run_id=run_id))
    selected_lift, lift_reason = select_live_lift(surface)
    rows.tower_lift_rows.append(
        tower_state_lift_event_row(
            run_id=run_id,
            arm_id=arm_id,
            episode_index=episode_index,
            step_index=step_index,
            surface=surface,
            selected=selected_lift,
            failure_reason=lift_reason,
        )
    )
    if selected_lift is None:
        return None
    tower_candidates = surface.tower_action_candidates()
    mask_result, valid_tower_candidates = mask_tower_action_candidates(
        instance=instance,
        state=state,
        candidates=tower_candidates,
        max_seconds=config.max_seconds_per_episode,
    )
    selected_tower = _select_tower_candidate(valid_tower_candidates, q_values)
    selected_concrete = selected_tower.concrete_candidate if selected_tower else None
    rows.tower_action_mask_rows.append(
        tower_action_mask_event_row(
            run_id=run_id,
            arm_id=arm_id,
            episode_index=episode_index,
            step_index=step_index,
            tier=surface.tier,
            state_cell_id=surface.state_cell_id,
            mask_result=mask_result,
            selected_tower_action_id=selected_tower.candidate_id if selected_tower else None,
            selected_concrete_action_id=selected_concrete.action.stable_id if selected_concrete else None,
        )
    )
    rows.direct_mask_rows.append(
        direct_mask_event_row(
            run_id=run_id,
            arm_id=arm_id,
            episode_index=episode_index,
            step_index=step_index,
            state_id=state.stable_id,
            candidate_generation_policy_id=TOWER_CANDIDATE_POLICY_ID,
            mask_result=mask_result,
            selected_action_id=selected_concrete.action.stable_id if selected_concrete else None,
        )
    )
    if selected_tower is None or selected_concrete is None:
        return None
    query = next(
        result
        for result in mask_result.query_results
        if result.candidate_id == selected_concrete.candidate_id
    )
    return {"selected": selected_concrete, "result": query.result}


def _select_candidate(
    candidates: tuple[DirectActionCandidate, ...],
    q_values: dict[str, float],
) -> DirectActionCandidate | None:
    if not candidates:
        return None
    moving = [candidate for candidate in candidates if not candidate.is_all_stay]
    pool = moving or list(candidates)
    return max(
        pool,
        key=lambda candidate: (
            q_values.get(candidate.candidate_id, 0.0),
            -candidate.rank,
            candidate.candidate_id,
        ),
    )


def _select_tower_candidate(candidates, q_values: dict[str, float]):
    if not candidates:
        return None
    moving = [candidate for candidate in candidates if not candidate.concrete_candidate.is_all_stay]
    pool = moving or list(candidates)
    return max(
        pool,
        key=lambda candidate: (
            q_values.get(candidate.concrete_candidate.candidate_id, 0.0),
            -candidate.rank,
            candidate.candidate_id,
        ),
    )


def _record_successor_diagnostic(
    *,
    instance,
    config: MaskedDirectVsLiveLiftConfig,
    rows: _RunRows,
    run_id: str,
    arm_id: str,
    episode_index: int,
    step_index: int,
    selected_action_id: str,
    successor_state: WarehouseGridlockState,
    seed: int,
) -> None:
    candidates = generate_direct_candidates(
        instance=instance,
        state=successor_state,
        budget=config.candidate_proposals_per_step,
        seed=seed,
        max_active_robots=config.max_active_robots,
        candidate_mix_id=config.candidate_mix_id,
    )
    mask_result = mask_direct_candidates(
        instance=instance,
        state=successor_state,
        candidates=candidates,
        max_seconds=config.max_seconds_per_episode,
    )
    rows.successor_rows.append(
        {
            "run_id": run_id,
            "arm_id": arm_id,
            "episode_index": episode_index,
            "step_index": step_index,
            "selected_action_id": selected_action_id,
            "successor_state_id": successor_state.stable_id,
            "successor_out_count_observed": mask_result.candidates_after,
            "successor_out_scope": "generated_candidate_set_after_selection",
            "successor_out_count_used_for_selection": False,
            "selection_policy_id": CONTROLLER_POLICY_ID,
            "selection_policy_description": "seeded first non-stay valid candidate with tabular value tie-break",
        }
    )


def _write_run_rows(*, run_root: Path, rows: _RunRows) -> None:
    write_csv(run_root / "episode_events.csv", rows.episode_rows, EPISODE_FIELDNAMES, create_parents=True)
    write_csv(run_root / "step_events.csv", rows.step_rows, STEP_FIELDNAMES, create_parents=True)
    write_csv(
        run_root / "direct_candidate_events.csv",
        rows.direct_candidate_rows,
        DIRECT_CANDIDATE_FIELDNAMES,
        create_parents=True,
    )
    write_csv(
        run_root / "direct_admissibility_mask_events.csv",
        rows.direct_mask_rows,
        DIRECT_MASK_FIELDNAMES,
        create_parents=True,
    )
    write_csv(
        run_root / "tower_state_lift_events.csv",
        rows.tower_lift_rows,
        TOWER_STATE_LIFT_FIELDNAMES,
        create_parents=True,
    )
    write_csv(
        run_root / "tower_action_mask_events.csv",
        rows.tower_action_mask_rows,
        TOWER_ACTION_MASK_FIELDNAMES,
        create_parents=True,
    )
    write_csv(
        run_root / "successor_diagnostic_events.csv",
        rows.successor_rows,
        SUCCESSOR_DIAGNOSTIC_FIELDNAMES,
        create_parents=True,
    )
    write_csv(
        run_root / "learner_update_events.csv",
        rows.learner_rows,
        LEARNER_UPDATE_FIELDNAMES,
        create_parents=True,
    )
    write_csv(
        run_root / "timing_segments.csv",
        rows.timing_rows,
        TIMING_SEGMENT_FIELDNAMES,
        create_parents=True,
    )


def _write_evaluation_level_tables(
    *,
    paths: EvaluationPaths,
    run_index_rows: list[dict[str, object]],
    direct_candidate_rows: list[dict[str, object]],
    direct_mask_rows: list[dict[str, object]],
    tower_lift_rows: list[dict[str, object]],
    tower_action_mask_rows: list[dict[str, object]],
    successor_rows: list[dict[str, object]],
    learner_rows: list[dict[str, object]],
    timing_rows: list[dict[str, object]],
    tower_surface_rows: list[dict[str, object]],
    tower_shape_rows: list[dict[str, object]],
) -> None:
    write_csv(paths.run_index, run_index_rows, RUN_INDEX_FIELDNAMES, create_parents=True)
    write_csv(
        paths.results_dir / "direct_candidate_events.csv",
        direct_candidate_rows,
        DIRECT_CANDIDATE_FIELDNAMES,
        create_parents=True,
    )
    write_csv(
        paths.results_dir / "direct_admissibility_mask_events.csv",
        direct_mask_rows,
        DIRECT_MASK_FIELDNAMES,
        create_parents=True,
    )
    write_csv(
        paths.results_dir / "tower_state_lift_events.csv",
        tower_lift_rows,
        TOWER_STATE_LIFT_FIELDNAMES,
        create_parents=True,
    )
    write_csv(
        paths.results_dir / "tower_action_mask_events.csv",
        tower_action_mask_rows,
        TOWER_ACTION_MASK_FIELDNAMES,
        create_parents=True,
    )
    write_csv(
        paths.results_dir / "successor_diagnostic_events.csv",
        successor_rows,
        SUCCESSOR_DIAGNOSTIC_FIELDNAMES,
        create_parents=True,
    )
    write_csv(
        paths.results_dir / "learner_update_events.csv",
        learner_rows,
        LEARNER_UPDATE_FIELDNAMES,
        create_parents=True,
    )
    write_csv(
        paths.results_dir / "timing_summary.csv",
        timing_rows,
        TIMING_SEGMENT_FIELDNAMES,
        create_parents=True,
    )
    write_csv(
        paths.results_dir / "tower_surface_scope_summary.csv",
        tower_surface_rows,
        TOWER_SURFACE_SCOPE_FIELDNAMES,
        create_parents=True,
    )
    write_csv(
        paths.results_dir / "tower_shape_summary.csv",
        tower_shape_rows,
        TOWER_SHAPE_FIELDNAMES,
        create_parents=True,
    )


def _read_run_csvs(*, paths: EvaluationPaths, filename: str) -> list[dict[str, object]]:
    rows: list[dict[str, object]] = []
    for path in sorted(paths.runs_dir.glob(f"*/{filename}")):
        with path.open(newline="", encoding="utf-8") as handle:
            rows.extend(dict(row) for row in csv.DictReader(handle))
    return rows
