"""Runner for Warehouse full-state/full-action trainable policy comparison."""

from __future__ import annotations

import csv
import sys
import time
from dataclasses import dataclass
from pathlib import Path
from typing import Any

from tqdm import tqdm

from big_boy_benchmarking.artifacts.writers import append_jsonl, write_csv, write_json
from big_boy_benchmarking.environments.warehouse_gridlock.full_state_policy_comparison.aggregation import (
    aggregate_results,
)
from big_boy_benchmarking.environments.warehouse_gridlock.full_state_policy_comparison.config import (
    DIRECT_ARM_ID,
    EVALUATION_ID,
    TOWER_ARM_ID,
    FullStatePolicyComparisonConfig,
)
from big_boy_benchmarking.environments.warehouse_gridlock.full_state_policy_comparison.events import (
    EPISODE_FIELDNAMES,
    MASK_PROJECTION_FIELDNAMES,
    NO_LOOKAHEAD_FIELDNAMES,
    POLICY_DECISION_FIELDNAMES,
    POLICY_UPDATE_FIELDNAMES,
    RUN_INDEX_FIELDNAMES,
    STEP_FIELDNAMES,
    TIMING_FIELDNAMES,
    TOWER_LIFT_FIELDNAMES,
    TOWER_POLICY_FIELDNAMES,
    TOWER_REALIZATION_FIELDNAMES,
    TOWER_SHAPE_FIELDNAMES,
)
from big_boy_benchmarking.environments.warehouse_gridlock.full_state_policy_comparison.manifests import (
    write_initial_manifests,
    write_run_manifest,
)
from big_boy_benchmarking.environments.warehouse_gridlock.full_state_policy_comparison.paths import (
    EvaluationPaths,
    run_id as build_run_id,
)
from big_boy_benchmarking.environments.warehouse_gridlock.full_state_policy_comparison.docs_writer import (
    write_human_docs,
    write_readout_source,
)
from big_boy_benchmarking.environments.warehouse_gridlock.instances import load_instance
from big_boy_benchmarking.environments.warehouse_gridlock.masked_direct_vs_live_lift_tower.admissibility import (
    mask_tower_action_candidates,
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
from big_boy_benchmarking.environments.warehouse_gridlock.policies import (
    BoundedDeterministicWarehouseActionResolver,
    WarehouseFullActionVector,
    WarehouseLinearFactorizedSoftmaxPolicy,
    WarehouseMaskContext,
    WarehousePolicyDecision,
    WarehousePolicyRng,
    WarehousePolicyTransition,
    config_from_instance_state,
)
from big_boy_benchmarking.environments.warehouse_gridlock.policies.linear_policy import (
    decision_with_projection,
)
from big_boy_benchmarking.environments.warehouse_gridlock.rewards import is_terminal, target_counts
from big_boy_benchmarking.environments.warehouse_gridlock.state import WarehouseGridlockState


@dataclass(frozen=True)
class WarehouseFullStatePolicyResult:
    status: str
    artifact_paths: dict[str, str]
    summary: dict[str, object]


@dataclass
class _RunRows:
    episode_rows: list[dict[str, object]]
    step_rows: list[dict[str, object]]
    policy_decision_rows: list[dict[str, object]]
    policy_update_rows: list[dict[str, object]]
    projection_rows: list[dict[str, object]]
    no_lookahead_rows: list[dict[str, object]]
    tower_lift_rows: list[dict[str, object]]
    tower_policy_rows: list[dict[str, object]]
    tower_realization_rows: list[dict[str, object]]
    tower_shape_rows: list[dict[str, object]]
    timing_rows: list[dict[str, object]]


def run_full_state_policy_comparison(
    config: FullStatePolicyComparisonConfig,
) -> WarehouseFullStatePolicyResult:
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
    all_rows = _RunRows([], [], [], [], [], [], [], [], [], [], [])
    run_index_rows: list[dict[str, object]] = []
    total_runs = config.schema_seeds * config.replicates_per_arm * len(config.active_arm_ids)
    progress = _ProgressReporter(paths=paths, config=config, total_runs=total_runs)
    progress.record_evaluation_start()
    for schema_seed in range(config.schema_seeds):
        for replicate_index in range(config.replicates_per_arm):
            for arm_id in config.active_arm_ids:
                current_run_id = build_run_id(
                    arm_id=arm_id,
                    replicate_index=replicate_index,
                    schema_seed=schema_seed,
                    run_label=config.run_label,
                )
                run_root = paths.run_root(current_run_id)
                run_root.mkdir(parents=True, exist_ok=True)
                seed = config.seed + schema_seed * 1000 + replicate_index * 100
                policy_id = f"{arm_id}_linear_policy_rep{replicate_index}_schema{schema_seed}"
                policy = WarehouseLinearFactorizedSoftmaxPolicy(
                    policy_id=policy_id,
                    learning_rate=config.learning_rate,
                    baseline_rate=config.baseline_rate,
                    temperature_initial=config.temperature_initial,
                    temperature_floor=config.temperature_floor,
                    temperature_decay_per_episode=config.temperature_decay_per_episode,
                )
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
                    policy=policy,
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
                        "run_id": current_run_id,
                        "arm_id": arm_id,
                        "replicate_index": replicate_index,
                        "schema_seed": schema_seed,
                        "run_label": config.run_label,
                        "policy": policy.to_manifest(),
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
                _extend_rows(all_rows, rows)
                run_index_rows.append(
                    {
                        "run_id": current_run_id,
                        "arm_id": arm_id,
                        "replicate_index": replicate_index,
                        "schema_seed": schema_seed,
                        "seed": seed,
                        "policy_id": policy_id,
                        "model_family_id": policy.model_family_id,
                        "status": "success",
                        "artifact_root": str(run_root),
                    }
                )
    _write_evaluation_level_tables(paths=paths, run_index_rows=run_index_rows, rows=all_rows)
    summary = aggregate_results(
        paths=paths,
        run_label=config.run_label,
        episode_rows=all_rows.episode_rows,
        policy_decision_rows=all_rows.policy_decision_rows,
        policy_update_rows=all_rows.policy_update_rows,
        projection_rows=all_rows.projection_rows,
        no_lookahead_rows=all_rows.no_lookahead_rows,
        tower_lift_rows=all_rows.tower_lift_rows,
        tower_shape_rows=all_rows.tower_shape_rows,
        timing_rows=all_rows.timing_rows,
    )
    readout_source = write_readout_source(paths=paths, run_label=config.run_label, summary=summary)
    docs = write_human_docs(paths=paths, run_label=config.run_label, summary=summary)
    elapsed = time.perf_counter() - started
    summary = {**summary, "duration_seconds": elapsed}
    progress.record_evaluation_complete(status="success", duration_seconds=elapsed)
    return WarehouseFullStatePolicyResult(
        status="success",
        artifact_paths={
            **manifest_paths,
            "run_index": str(paths.run_index),
            "progress_events": str(paths.progress_events),
            "aggregate_summary": str(paths.aggregate_summary),
            "readout_source": str(readout_source),
            **docs,
        },
        summary=summary,
    )


def summarize_full_state_policy_comparison(
    *,
    repo_root: Path,
    artifact_root: Path,
) -> WarehouseFullStatePolicyResult:
    paths = EvaluationPaths(repo_root=repo_root, artifact_root=artifact_root)
    run_label = artifact_root.name
    rows = _RunRows(
        episode_rows=_read_run_csvs(paths=paths, filename="episodes.csv"),
        step_rows=_read_run_csvs(paths=paths, filename="step_events.csv"),
        policy_decision_rows=_read_run_csvs(paths=paths, filename="policy_decision_events.csv"),
        policy_update_rows=_read_run_csvs(paths=paths, filename="policy_update_events.csv"),
        projection_rows=_read_run_csvs(paths=paths, filename="mask_projection_events.csv"),
        no_lookahead_rows=_read_run_csvs(paths=paths, filename="no_lookahead_audit_events.csv"),
        tower_lift_rows=_read_run_csvs(paths=paths, filename="tower_lift_events.csv"),
        tower_policy_rows=_read_run_csvs(paths=paths, filename="tower_policy_events.csv"),
        tower_realization_rows=_read_run_csvs(paths=paths, filename="tower_realization_events.csv"),
        tower_shape_rows=_read_run_csvs(paths=paths, filename="tower_shape_events.csv"),
        timing_rows=_read_run_csvs(paths=paths, filename="timing_segments.csv"),
    )
    summary = aggregate_results(
        paths=paths,
        run_label=run_label,
        episode_rows=rows.episode_rows,
        policy_decision_rows=rows.policy_decision_rows,
        policy_update_rows=rows.policy_update_rows,
        projection_rows=rows.projection_rows,
        no_lookahead_rows=rows.no_lookahead_rows,
        tower_lift_rows=rows.tower_lift_rows,
        tower_shape_rows=rows.tower_shape_rows,
        timing_rows=rows.timing_rows,
    )
    readout_source = write_readout_source(paths=paths, run_label=run_label, summary=summary)
    docs = write_human_docs(paths=paths, run_label=run_label, summary=summary)
    return WarehouseFullStatePolicyResult(
        status=str(summary.get("status", "complete")),
        artifact_paths={"readout_source": str(readout_source), **docs},
        summary=summary,
    )


def _run_arm(
    *,
    instance,
    config: FullStatePolicyComparisonConfig,
    arm_id: str,
    run_id: str,
    replicate_index: int,
    schema_seed: int,
    seed: int,
    policy: WarehouseLinearFactorizedSoftmaxPolicy,
    progress: "_ProgressReporter",
) -> _RunRows:
    rows = _RunRows([], [], [], [], [], [], [], [], [], [], [])
    resolver = BoundedDeterministicWarehouseActionResolver(
        projection_attempt_budget=config.projection_attempt_budget
    )
    run_started = time.perf_counter()
    for episode_index in range(config.episodes_per_arm):
        episode_max_seconds = config.max_seconds_for_episode(episode_index)
        state = instance.start_state
        total_reward = 0.0
        valid_selected = 0
        invalid_selected = 0
        policy_update_count = 0
        non_noop_update_count = 0
        projection_attempt_count = 0
        initial_counts = target_counts(
            state,
            robot_targets=instance.manifest.robot_target_map(),
            box_targets=instance.manifest.box_target_map(),
        )
        failure_reason = ""
        for step_index in range(episode_max_seconds):
            step_payload = (
                _direct_step(
                    instance=instance,
                    config=config,
                    max_seconds_per_episode=episode_max_seconds,
                    state=state,
                    run_id=run_id,
                    arm_id=arm_id,
                    episode_index=episode_index,
                    step_index=step_index,
                    seed=seed,
                    policy=policy,
                    resolver=resolver,
                )
                if arm_id == DIRECT_ARM_ID
                else _tower_step(
                    instance=instance,
                    config=config,
                    max_seconds_per_episode=episode_max_seconds,
                    state=state,
                    run_id=run_id,
                    arm_id=arm_id,
                    episode_index=episode_index,
                    step_index=step_index,
                    seed=seed,
                    schema_seed=schema_seed,
                    policy=policy,
                    resolver=resolver,
                    rows=rows,
                )
            )
            if step_payload is None:
                failure_reason = "no_policy_action_or_live_lift"
                break
            decision = step_payload["decision"]
            result = step_payload["result"]
            selected_vector = step_payload["selected_vector"]
            projection_trace = step_payload["projection_trace"]
            pre_config = config_from_instance_state(
                instance=instance,
                state=state,
                max_seconds_per_episode=episode_max_seconds,
            )
            post_config = config_from_instance_state(
                instance=instance,
                state=result.next_state,
                max_seconds_per_episode=episode_max_seconds,
            )
            update = policy.update(
                transition=WarehousePolicyTransition(
                    pre_config=pre_config,
                    pre_second=state.time_step,
                    selected_full_action_vector=selected_vector,
                    projection_trace=projection_trace,
                    reward=result.reward,
                    post_config=post_config,
                    post_second=result.next_state.time_step,
                    terminated=result.terminated,
                    truncated=result.truncated,
                    episode_index=episode_index,
                    step_index=step_index,
                    step_result=result,
                )
            )
            policy_update_count += 1
            non_noop_update_count += int(update.non_noop_update)
            projection_attempt_count += projection_trace.attempt_count
            total_reward += result.reward
            valid_selected += int(result.valid)
            invalid_selected += int(not result.valid)
            counts = target_counts(
                result.next_state,
                robot_targets=instance.manifest.robot_target_map(),
                box_targets=instance.manifest.box_target_map(),
            )
            rows.policy_decision_rows.append(
                decision.to_event_row(
                    run_id=run_id,
                    arm_id=arm_id,
                    episode_index=episode_index,
                    step_index=step_index,
                )
            )
            rows.policy_update_rows.append(
                update.to_event_row(
                    run_id=run_id,
                    arm_id=arm_id,
                    episode_index=episode_index,
                    step_index=step_index,
                )
            )
            rows.projection_rows.append(
                {
                    "run_id": run_id,
                    "arm_id": arm_id,
                    "episode_index": episode_index,
                    "step_index": step_index,
                    **projection_trace.to_row(),
                }
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
                    "selected_action_id": selected_vector.stable_id,
                    "selected_action_vector_hash": selected_vector.stable_hash,
                    "selected_action_summary": _action_summary(selected_vector),
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
            rows.no_lookahead_rows.append(
                {
                    "run_id": run_id,
                    "arm_id": arm_id,
                    "episode_index": episode_index,
                    "step_index": step_index,
                    "selected_action_id": selected_vector.stable_id,
                    "successor_state_id": result.next_state.stable_id,
                    "successor_out_count_observed": "",
                    "successor_out_scope": "not_queried_for_selection",
                    "successor_out_count_used_for_selection": False,
                    "selection_policy_id": policy.policy_id,
                    "selection_policy_description": (
                        "full-state full-action trainable policy with immediate resolver"
                    ),
                }
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
            "truncated": state.time_step >= episode_max_seconds and not terminal,
            "selected_step_count": valid_selected + invalid_selected,
            "valid_selected_step_count": valid_selected,
            "invalid_selected_step_count": invalid_selected,
            "policy_update_count": policy_update_count,
            "non_noop_update_count": non_noop_update_count,
            "projection_attempt_count": projection_attempt_count,
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


def _direct_step(
    *,
    instance,
    config: FullStatePolicyComparisonConfig,
    max_seconds_per_episode: int,
    state: WarehouseGridlockState,
    run_id: str,
    arm_id: str,
    episode_index: int,
    step_index: int,
    seed: int,
    policy: WarehouseLinearFactorizedSoftmaxPolicy,
    resolver: BoundedDeterministicWarehouseActionResolver,
) -> dict[str, Any]:
    full_config = config_from_instance_state(
        instance=instance,
        state=state,
        max_seconds_per_episode=max_seconds_per_episode,
    )
    mask_context = WarehouseMaskContext(
        arm_id=arm_id,
        run_id=run_id,
        episode_index=episode_index,
        step_index=step_index,
        max_seconds_per_episode=max_seconds_per_episode,
        projection_attempt_budget=config.projection_attempt_budget,
    )
    raw_decision = policy.act(
        full_system_config=full_config,
        second=state.time_step,
        rng=WarehousePolicyRng(seed=seed),
        mask_context=mask_context,
    )
    resolved = resolver.resolve(
        instance=instance,
        state=state,
        raw_action_vector=raw_decision.raw_action_vector,
        max_seconds=max_seconds_per_episode,
        robot_command_margins=dict(raw_decision.robot_command_margins),
    )
    decision = decision_with_projection(
        decision=raw_decision,
        selected_action_vector=resolved.selected_action_vector,
        raw_valid=resolved.raw_step_result.valid,
        selected_valid=resolved.step_result.valid,
        projection_trace=resolved.projection_trace,
    )
    return {
        "decision": decision,
        "result": resolved.step_result,
        "selected_vector": resolved.selected_action_vector,
        "projection_trace": resolved.projection_trace,
    }


def _tower_step(
    *,
    instance,
    config: FullStatePolicyComparisonConfig,
    max_seconds_per_episode: int,
    state: WarehouseGridlockState,
    run_id: str,
    arm_id: str,
    episode_index: int,
    step_index: int,
    seed: int,
    schema_seed: int,
    policy: WarehouseLinearFactorizedSoftmaxPolicy,
    resolver: BoundedDeterministicWarehouseActionResolver,
    rows: _RunRows,
) -> dict[str, Any] | None:
    surface = build_tower_surface(
        instance=instance,
        state=state,
        candidate_budget=config.candidate_proposals_per_step,
        seed=seed + episode_index * 1000 + step_index,
        schema_seed=schema_seed,
        max_seconds=max_seconds_per_episode,
        max_active_robots=config.max_active_robots,
        candidate_mix_id=config.candidate_mix_id,
    )
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
    _, valid_tower_candidates = mask_tower_action_candidates(
        instance=instance,
        state=state,
        candidates=tower_candidates,
        max_seconds=max_seconds_per_episode,
    )
    if not valid_tower_candidates:
        return None
    full_config = config_from_instance_state(
        instance=instance,
        state=state,
        max_seconds_per_episode=max_seconds_per_episode,
    )
    scored = []
    for candidate in valid_tower_candidates:
        vector = WarehouseFullActionVector.from_action(candidate.concrete_candidate.action)
        score = policy.score_action_vector(
            full_system_config=full_config,
            second=state.time_step,
            action_vector=vector,
        )
        scored.append((score, -candidate.rank, candidate.candidate_id, candidate, vector))
    score, _, _, selected_tower, raw_vector = max(scored)
    raw_decision = WarehousePolicyDecision(
        policy_id=policy.policy_id,
        model_family_id=policy.model_family_id,
        second=state.time_step,
        raw_action_vector=raw_vector,
        selected_action_vector=None,
        raw_valid=False,
        selected_valid=False,
        projection_trace=None,
        prior_signal_used=any(abs(value) > 1.0e-12 for value in policy.weights.values()),
        decision_score_summary={
            "selection_score": score,
            "candidate_count": len(valid_tower_candidates),
            "nonzero_weight_count": sum(1 for value in policy.weights.values() if abs(value) > 1.0e-12),
        },
        robot_command_margins={
            robot_id: 1.0
            for robot_id, command in raw_vector.commands.items()
            if command != command.STAY
        },
        tier=surface.tier,
        tier_state_id=surface.state_cell_id,
    )
    resolved = resolver.resolve(
        instance=instance,
        state=state,
        raw_action_vector=raw_vector,
        max_seconds=max_seconds_per_episode,
        robot_command_margins=dict(raw_decision.robot_command_margins),
    )
    decision = decision_with_projection(
        decision=raw_decision,
        selected_action_vector=resolved.selected_action_vector,
        raw_valid=resolved.raw_step_result.valid,
        selected_valid=resolved.step_result.valid,
        projection_trace=resolved.projection_trace,
    )
    rows.tower_policy_rows.append(
        {
            "run_id": run_id,
            "arm_id": arm_id,
            "episode_index": episode_index,
            "step_index": step_index,
            "tier": surface.tier,
            "state_cell_id": surface.state_cell_id,
            "policy_id": policy.policy_id,
            "model_family_id": policy.model_family_id,
            "candidate_count": len(valid_tower_candidates),
            "selected_tower_action_id": selected_tower.candidate_id,
            "selected_concrete_action_id": selected_tower.concrete_candidate.action.stable_id,
            "selection_score": score,
            "selection_surface": "generated_discovered_tower_candidate_surface",
            "learning_key_surface": "feature_weights_not_candidate_ids",
        }
    )
    rows.tower_realization_rows.append(
        {
            "run_id": run_id,
            "arm_id": arm_id,
            "episode_index": episode_index,
            "step_index": step_index,
            "tier": surface.tier,
            "state_cell_id": surface.state_cell_id,
            "selected_tower_action_id": selected_tower.candidate_id,
            "selected_concrete_action_id": selected_tower.concrete_candidate.action.stable_id,
            "selected_concrete_action_vector_hash": resolved.selected_action_vector.stable_hash,
            "action_realization_candidate_count": len(valid_tower_candidates),
            "concrete_selected_valid": resolved.step_result.valid,
        }
    )
    return {
        "decision": decision,
        "result": resolved.step_result,
        "selected_vector": resolved.selected_action_vector,
        "projection_trace": resolved.projection_trace,
    }


class _ProgressReporter:
    def __init__(
        self,
        *,
        paths: EvaluationPaths,
        config: FullStatePolicyComparisonConfig,
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
        self.detail_interval = max(1, config.progress_every_episodes)
        self.bar = (
            tqdm(
                total=self.total_episodes,
                desc=f"warehouse policy {config.run_label}",
                unit="episode",
                file=sys.stderr,
                dynamic_ncols=True,
                miniters=self.detail_interval,
                leave=True,
            )
            if self.enabled and config.progress_to_stderr
            else None
        )
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
                "max_seconds_schedule_start": self.config.max_seconds_schedule_start,
                "max_seconds_schedule_end": self.config.max_seconds_schedule_end,
                "max_seconds_schedule_span_episodes": self.config.max_seconds_schedule_span_episodes,
                "projection_attempt_budget": self.config.projection_attempt_budget,
                "active_arm_ids": list(self.config.active_arm_ids),
            }
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
            }
        )
        if self.bar is not None:
            self.bar.set_description_str(f"warehouse policy {self.config.run_label} {arm_id}")

    def record_episode_complete(self, episode_row: dict[str, object]) -> None:
        self.completed_episodes += 1
        self._emit(
            {
                "event_type": "episode_complete",
                "completed_episodes": self.completed_episodes,
                "total_episodes": self.total_episodes,
                "elapsed_seconds": round(time.perf_counter() - self.started, 3),
                **episode_row,
            }
        )
        if self.bar is not None:
            self.bar.set_postfix(
                {
                    "reward": episode_row["total_reward"],
                    "updates": episode_row["non_noop_update_count"],
                    "arm": episode_row["arm_id"],
                },
                refresh=False,
            )
            self.bar.update(1)

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
            }
        )

    def record_evaluation_complete(self, *, status: str, duration_seconds: float) -> None:
        self._emit(
            {
                "event_type": "evaluation_complete",
                "status": status,
                "duration_seconds": round(duration_seconds, 3),
                "completed_runs": self.completed_runs,
                "total_runs": self.total_runs,
            }
        )
        if self.bar is not None:
            self.bar.close()

    def _emit(self, payload: dict[str, object]) -> None:
        if self.enabled:
            append_jsonl(self.paths.progress_events, payload, create_parents=True)


def _write_run_rows(*, run_root: Path, rows: _RunRows) -> None:
    write_csv(run_root / "episodes.csv", rows.episode_rows, EPISODE_FIELDNAMES, create_parents=True)
    write_csv(run_root / "step_events.csv", rows.step_rows, STEP_FIELDNAMES, create_parents=True)
    write_csv(
        run_root / "policy_decision_events.csv",
        rows.policy_decision_rows,
        POLICY_DECISION_FIELDNAMES,
        create_parents=True,
    )
    write_csv(
        run_root / "policy_update_events.csv",
        rows.policy_update_rows,
        POLICY_UPDATE_FIELDNAMES,
        create_parents=True,
    )
    write_csv(
        run_root / "mask_projection_events.csv",
        rows.projection_rows,
        MASK_PROJECTION_FIELDNAMES,
        create_parents=True,
    )
    write_csv(
        run_root / "no_lookahead_audit_events.csv",
        rows.no_lookahead_rows,
        NO_LOOKAHEAD_FIELDNAMES,
        create_parents=True,
    )
    write_csv(
        run_root / "tower_lift_events.csv",
        rows.tower_lift_rows,
        TOWER_LIFT_FIELDNAMES,
        create_parents=True,
    )
    write_csv(
        run_root / "tower_policy_events.csv",
        rows.tower_policy_rows,
        TOWER_POLICY_FIELDNAMES,
        create_parents=True,
    )
    write_csv(
        run_root / "tower_realization_events.csv",
        rows.tower_realization_rows,
        TOWER_REALIZATION_FIELDNAMES,
        create_parents=True,
    )
    write_csv(
        run_root / "tower_shape_events.csv",
        rows.tower_shape_rows,
        TOWER_SHAPE_FIELDNAMES,
        create_parents=True,
    )
    write_csv(run_root / "timing_segments.csv", rows.timing_rows, TIMING_FIELDNAMES, create_parents=True)
    (run_root / "warnings.jsonl").write_text("", encoding="utf-8")


def _write_evaluation_level_tables(
    *,
    paths: EvaluationPaths,
    run_index_rows: list[dict[str, object]],
    rows: _RunRows,
) -> None:
    write_csv(paths.run_index, run_index_rows, RUN_INDEX_FIELDNAMES, create_parents=True)
    write_csv(paths.results_dir / "policy_decision_events.csv", rows.policy_decision_rows, POLICY_DECISION_FIELDNAMES, create_parents=True)
    write_csv(paths.results_dir / "policy_update_events.csv", rows.policy_update_rows, POLICY_UPDATE_FIELDNAMES, create_parents=True)
    write_csv(paths.results_dir / "mask_projection_events.csv", rows.projection_rows, MASK_PROJECTION_FIELDNAMES, create_parents=True)
    write_csv(paths.results_dir / "no_lookahead_audit_events.csv", rows.no_lookahead_rows, NO_LOOKAHEAD_FIELDNAMES, create_parents=True)
    write_csv(paths.results_dir / "tower_lift_events.csv", rows.tower_lift_rows, TOWER_LIFT_FIELDNAMES, create_parents=True)
    write_csv(paths.results_dir / "tower_policy_events.csv", rows.tower_policy_rows, TOWER_POLICY_FIELDNAMES, create_parents=True)
    write_csv(paths.results_dir / "tower_realization_events.csv", rows.tower_realization_rows, TOWER_REALIZATION_FIELDNAMES, create_parents=True)
    write_csv(paths.results_dir / "tower_shape_events.csv", rows.tower_shape_rows, TOWER_SHAPE_FIELDNAMES, create_parents=True)


def _read_run_csvs(*, paths: EvaluationPaths, filename: str) -> list[dict[str, object]]:
    rows: list[dict[str, object]] = []
    for path in sorted(paths.runs_dir.glob(f"*/{filename}")):
        with path.open(newline="", encoding="utf-8") as handle:
            rows.extend(dict(row) for row in csv.DictReader(handle))
    return rows


def _extend_rows(target: _RunRows, source: _RunRows) -> None:
    for field in target.__dataclass_fields__:
        getattr(target, field).extend(getattr(source, field))


def _action_summary(vector: WarehouseFullActionVector) -> str:
    active = [
        f"{robot_id}:{command.value}"
        for robot_id, command in sorted(vector.commands.items())
        if command != command.STAY
    ]
    return "all_stay" if not active else "|".join(active)
