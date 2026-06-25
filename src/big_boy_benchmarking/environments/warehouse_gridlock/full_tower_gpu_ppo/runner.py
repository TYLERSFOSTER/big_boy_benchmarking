"""Runner for Warehouse Gridlock full-tower PPO."""

from __future__ import annotations

import hashlib
import random
import time
from dataclasses import dataclass
from pathlib import Path
from typing import Any

from tqdm import tqdm

from big_boy_benchmarking.artifacts.writers import append_jsonl, write_csv, write_json
from big_boy_benchmarking.environments.warehouse_gridlock.instances import load_instance
from big_boy_benchmarking.environments.warehouse_gridlock.masked_direct_vs_live_lift_tower.readiness_source import (
    load_readiness_source,
    validate_readiness_source,
)
from big_boy_benchmarking.environments.warehouse_gridlock.rewards import target_counts

from .aggregation import summarize_existing, write_evaluation_tables
from .config import WarehouseFullTowerPPOConfig
from .docs_writer import write_human_docs, write_readout_source
from .events import (
    CONTROLLER_EVENT_FIELDNAMES,
    EPISODE_FIELDNAMES,
    ROLLOUT_SAMPLE_FIELDNAMES,
    STEP_FIELDNAMES,
)
from .ids import WAREHOUSE_GRIDLOCK_POINTWISE_LIFTABILITY_SEMANTICS_ID
from .manifests import write_initial_manifests
from .paths import FullTowerPPOPaths, run_id as build_run_id
from .policy_bank import TierPolicyBank
from .ppo import PPOSample, TierRolloutBuffer, update_tier_policy
from .records import DecisionContextRecord, RolloutSampleRecord
from .state_collapser_runtime import (
    build_decision_surface,
    selected_warehouse_action,
)
from .tokenization import encode_surface
from .trace_retention import (
    TraceRecord,
    base_retention_reason,
    write_selected_trace,
)


@dataclass(frozen=True)
class WarehouseFullTowerPPOResult:
    status: str
    artifact_paths: dict[str, str]
    summary: dict[str, object]


def inspect_full_tower_gpu_ppo(config: WarehouseFullTowerPPOConfig) -> WarehouseFullTowerPPOResult:
    started = time.perf_counter()
    actual_device = _select_device(config)
    readiness = load_readiness_source(config.readiness_source)
    validate_readiness_source(readiness, expected_instance_id=config.instance_id)
    load_instance(instance_id=config.instance_id)
    summary = {
        "status": "ok",
        "evaluation_id": config.evaluation_id,
        "instance_id": config.instance_id,
        "actual_device": actual_device,
        "state_collapser_version": _version("state_collapser"),
        "torch_version": _version("torch"),
        "duration_seconds": time.perf_counter() - started,
    }
    return WarehouseFullTowerPPOResult(status="ok", artifact_paths={}, summary=summary)


def run_full_tower_gpu_ppo(config: WarehouseFullTowerPPOConfig) -> WarehouseFullTowerPPOResult:
    started = time.perf_counter()
    actual_device = _select_device(config)
    paths = FullTowerPPOPaths(repo_root=config.repo_root, artifact_root=config.artifact_root)
    paths.ensure()
    readiness_source = load_readiness_source(config.readiness_source)
    validate_readiness_source(readiness_source, expected_instance_id=config.instance_id)
    instance = load_instance(instance_id=config.instance_id)
    manifest_paths = write_initial_manifests(
        paths=paths,
        config=config,
        actual_device=actual_device,
    )
    append_jsonl(
        paths.progress_events,
        {"event_type": "evaluation_start", "run_label": config.run_label},
        create_parents=True,
    )
    run_index_rows: list[dict[str, object]] = []
    episode_rows: list[dict[str, object]] = []
    step_rows: list[dict[str, object]] = []
    surface_rows: list[dict[str, object]] = []
    update_rows: list[dict[str, object]] = []
    tier_policy_rows: list[dict[str, object]] = []
    timing_rows: list[dict[str, object]] = []
    trace_records: list[TraceRecord] = []
    total_episodes = (
        config.episodes_per_arm
        * config.replicates_per_arm
        * config.schema_seeds
        * len(config.active_arm_ids)
    )
    progress = tqdm(
        total=total_episodes,
        disable=config.progress_every_episodes == 0,
        desc=f"warehouse full-tower PPO {config.run_label}",
    )
    try:
        for schema_seed in range(config.schema_seeds):
            for replicate_index in range(config.replicates_per_arm):
                for arm in config.active_arms():
                    current_run_id = build_run_id(
                        arm_id=arm.arm_id,
                        replicate_index=replicate_index,
                        schema_seed=schema_seed,
                        run_label=config.run_label,
                    )
                    run_root = paths.run_root(current_run_id)
                    run_root.mkdir(parents=True, exist_ok=True)
                    seed = config.seed + schema_seed * 1000 + replicate_index * 100
                    run_started = time.perf_counter()
                    run_result = _run_arm(
                        instance=instance,
                        config=config,
                        paths=paths,
                        arm=arm,
                        run_id=current_run_id,
                        replicate_index=replicate_index,
                        schema_seed=schema_seed,
                        seed=seed,
                        actual_device=actual_device,
                        progress=progress,
                    )
                    _write_run_tables(
                        run_root=run_root,
                        run_result=run_result,
                        write_full_debug_tables=config.retention.writes_full_debug_tables,
                    )
                    episode_rows.extend(run_result["episode_rows"])
                    step_rows.extend(run_result["step_rows"])
                    surface_rows.extend(run_result["surface_rows"])
                    update_rows.extend(run_result["update_rows"])
                    tier_policy_rows.extend(run_result["tier_policy_rows"])
                    trace_records.extend(run_result["trace_records"])
                    duration = time.perf_counter() - run_started
                    timing_rows.append(
                        {
                            "run_id": current_run_id,
                            "arm_id": arm.arm_id,
                            "duration_seconds": duration,
                            "episode_count": config.episodes_per_arm,
                        }
                    )
                    run_index_rows.append(
                        {
                            "run_id": current_run_id,
                            "arm_id": arm.arm_id,
                            "replicate_index": replicate_index,
                            "schema_seed": schema_seed,
                            "seed": seed,
                            "status": "success",
                            "run_root": str(run_root),
                        }
                    )
    finally:
        progress.close()
    summary = write_evaluation_tables(
        paths=paths,
        run_index_rows=run_index_rows,
        episode_rows=episode_rows,
        step_rows=step_rows,
        surface_rows=surface_rows,
        update_rows=update_rows,
        tier_policy_rows=tier_policy_rows,
        timing_rows=timing_rows,
        trace_records=trace_records,
    )
    readout_source = write_readout_source(
        paths=paths,
        run_label=config.run_label,
        summary=summary,
    )
    docs = write_human_docs(paths=paths, run_label=config.run_label, summary=summary)
    elapsed = time.perf_counter() - started
    append_jsonl(
        paths.progress_events,
        {"event_type": "evaluation_complete", "status": "success", "duration_seconds": elapsed},
        create_parents=True,
    )
    return WarehouseFullTowerPPOResult(
        status="success",
        artifact_paths={
            **manifest_paths,
            "run_index": str(paths.run_index),
            "aggregate_summary": str(paths.aggregate_summary),
            "readout_source": str(readout_source),
            **docs,
        },
        summary={**summary, "duration_seconds": elapsed},
    )


def summarize_full_tower_gpu_ppo(
    *,
    repo_root: Path,
    artifact_root: Path,
    run_label: str | None = None,
) -> WarehouseFullTowerPPOResult:
    paths = FullTowerPPOPaths(repo_root=repo_root, artifact_root=artifact_root)
    summary = summarize_existing(paths)
    label = run_label or artifact_root.name
    readout_source = write_readout_source(paths=paths, run_label=label, summary=summary)
    docs = write_human_docs(paths=paths, run_label=label, summary=summary)
    return WarehouseFullTowerPPOResult(
        status="complete",
        artifact_paths={
            "aggregate_summary": str(paths.aggregate_summary),
            "readout_source": str(readout_source),
            **docs,
        },
        summary=summary,
    )


def _run_arm(
    *,
    instance: Any,
    config: WarehouseFullTowerPPOConfig,
    paths: FullTowerPPOPaths,
    arm: Any,
    run_id: str,
    replicate_index: int,
    schema_seed: int,
    seed: int,
    actual_device: str,
    progress: tqdm,
) -> dict[str, Any]:
    rng = random.Random(seed)
    policy_bank = TierPolicyBank(capacity=config.capacity, ppo=config.ppo, device=actual_device)
    buffers: dict[int, TierRolloutBuffer] = {}
    episode_rows: list[dict[str, object]] = []
    step_rows: list[dict[str, object]] = []
    controller_rows: list[dict[str, object]] = []
    surface_rows: list[dict[str, object]] = []
    sample_rows: list[dict[str, object]] = []
    update_rows: list[dict[str, object]] = []
    trace_records: list[TraceRecord] = []
    global_update_index = 0
    ppo_sample_index = 0
    controller_event_index = 0
    best_reward = float("-inf")
    best_trace_rows: list[dict[str, object]] = []
    best_episode_index = -1
    first_success_retained = False
    retained_trace_keys: set[tuple[int, str]] = set()
    final_episode_index = config.episodes_per_arm - 1
    for episode_index in range(config.episodes_per_arm):
        state = instance.start_state
        total_reward = 0.0
        failure_reason = ""
        terminated = False
        truncated = False
        episode_step_count = 0
        episode_sample_count = 0
        episode_controller_count = 0
        episode_step_rows: list[dict[str, object]] = []
        episode_controller_rows: list[dict[str, object]] = []
        episode_surface_rows: list[dict[str, object]] = []
        episode_sample_rows: list[dict[str, object]] = []
        for step_index in range(config.max_seconds_per_episode * 4):
            if state.time_step >= config.max_seconds_per_episode:
                truncated = True
                break
            surface = build_decision_surface(
                instance=instance,
                state=state,
                arm=arm,
                config=config,
                schema_seed=schema_seed,
                generation_seed=rng.randrange(2**31),
            )
            surface_row = surface.to_summary_row(
                run_id=run_id,
                episode_index=episode_index,
                step_index=step_index,
            )
            episode_surface_rows.append(surface_row)
            controller_row = {
                "run_id": run_id,
                "arm_id": arm.arm_id,
                "episode_index": episode_index,
                "controller_event_index": controller_event_index,
                "event_type": "pointwise_surface",
                "tier_index": surface.tier_index,
                "state_cell_id": surface.state_cell_id,
                "candidate_action_count": len(surface.action_choices),
                "details": surface.semantics_id,
            }
            episode_controller_rows.append(controller_row)
            controller_event_index += 1
            episode_controller_count += 1
            if not surface.actor_callable:
                failure_reason = "NO_AVAILABLE_ACTION"
                break
            context = _decision_context(
                surface=surface,
                run_id=run_id,
                episode_index=episode_index,
                replicate_index=replicate_index,
                schema_seed=schema_seed,
                ppo_sample_index=ppo_sample_index,
                controller_event_index=controller_event_index,
                arm_id=arm.arm_id,
            )
            encoded = encode_surface(
                surface=surface,
                context=context,
                max_seconds=config.max_seconds_per_episode,
            )
            entry = policy_bank.entry_for_tier(surface.tier_index)
            output = entry.rollout_policy.forward_encoded(encoded)
            selected_index = int(output.probabilities.multinomial(1).item())
            choice = surface.action_choices[selected_index]
            old_log_prob = float(output.log_probs[selected_index].detach().cpu())
            value = float(output.value.detach().cpu())
            entropy = float(output.entropy.detach().cpu())
            action = selected_warehouse_action(choice)
            result = choice.target_state
            reward = float(choice.selected_edge.labels and 0.0)
            # The generated edge already came from transition validation; use its target.
            reward = float(
                next(
                    (
                        edge.reward
                        for edge in surface.valid_edges
                        if edge.action.stable_id == action.stable_id
                    ),
                    0.0,
                )
            )
            terminated = _terminal(instance, result)
            truncated = result.time_step >= config.max_seconds_per_episode and not terminated
            next_state = result
            total_reward += reward
            counts = target_counts(
                next_state,
                robot_targets=instance.manifest.robot_target_map(),
                box_targets=instance.manifest.box_target_map(),
            )
            sample = RolloutSampleRecord(
                rollout_sample_id=_stable_id(run_id, str(episode_index), str(ppo_sample_index)),
                decision_context_id=context.decision_context_id,
                tier_index=surface.tier_index,
                policy_snapshot_id=entry.policy_snapshot_id,
                rollout_policy_snapshot_id=entry.rollout_policy_snapshot_id,
                state_history_ref=f"{run_id}:episode{episode_index}:tier{surface.tier_index}",
                action_history_ref=f"{run_id}:episode{episode_index}:tier{surface.tier_index}",
                candidate_action_ids_ordered=context.candidate_action_ids_ordered,
                candidate_mask=context.candidate_mask,
                selected_local_index=selected_index,
                selected_action_cell_id=choice.action_cell_id,
                old_log_prob=old_log_prob,
                value_estimate=value,
                entropy=entropy,
                resolved_concrete_action_digest=_stable_id(action.stable_id),
                lift_candidate_id=f"{choice.action_cell_id}:{selected_index}",
                lift_candidate_digest=_stable_id(choice.action_id, next_state.stable_id),
                lift_semantics_id=WAREHOUSE_GRIDLOCK_POINTWISE_LIFTABILITY_SEMANTICS_ID,
                reward=reward,
                next_decision_context_id=None,
                terminated=terminated,
                truncated=truncated,
                bootstrap_value=None,
                diagnostic_failure_code=None,
            )
            ppo_sample = PPOSample(context=context, encoded=encoded, sample=sample)
            buffer = buffers.setdefault(surface.tier_index, TierRolloutBuffer(surface.tier_index))
            buffer.append(ppo_sample)
            episode_sample_rows.append(
                {
                    **sample.to_dict(),
                    "run_id": run_id,
                    "arm_id": arm.arm_id,
                    "episode_index": episode_index,
                }
            )
            episode_step_rows.append(
                {
                    "run_id": run_id,
                    "arm_id": arm.arm_id,
                    "replicate_index": replicate_index,
                    "schema_seed": schema_seed,
                    "episode_index": episode_index,
                    "step_index": step_index,
                    "state_id": state.stable_id,
                    "selected_action_id": action.stable_id,
                    "selected_action_vector_hash": _stable_id(action.stable_id),
                    "selected_action_summary": _action_summary(action),
                    "reward": reward,
                    "valid": True,
                    "terminated": terminated,
                    "truncated": truncated,
                    "next_state_id": next_state.stable_id,
                    "correct_box_count": counts["correct_box_count"],
                    "correct_robot_count": counts["correct_robot_count"],
                    "invalid_reasons": "",
                    "tier_index": surface.tier_index,
                    "selected_local_index": selected_index,
                    "candidate_action_count": len(surface.action_choices),
                }
            )
            ppo_sample_index += 1
            episode_sample_count += 1
            episode_step_count += 1
            state = next_state
            if buffer.ready_count() >= config.ppo.update_interval_samples:
                update_rows.extend(
                    _update_ready_buffers(
                        buffers=buffers,
                        policy_bank=policy_bank,
                        config=config,
                        run_id=run_id,
                        arm_id=arm.arm_id,
                        actual_device=actual_device,
                        global_update_index_start=global_update_index,
                    )
                )
                global_update_index += 1
            if terminated or truncated:
                break
        progress.update(1)
        progress.set_postfix(
            reward=round(total_reward, 3),
            updates=sum(row.get("optimizer_steps", 0) for row in update_rows),
            arm=arm.arm_id[:18],
        )
        if config.retention.writes_full_debug_tables:
            step_rows.extend(episode_step_rows)
            controller_rows.extend(episode_controller_rows)
            surface_rows.extend(episode_surface_rows)
            sample_rows.extend(episode_sample_rows)
        retained_count_before = len(trace_records)
        if total_reward > best_reward:
            best_reward = total_reward
            best_episode_index = episode_index
            best_trace_rows = list(episode_step_rows)
        base_reason = base_retention_reason(
            episode_index=episode_index,
            final_episode_index=final_episode_index,
            config=config.retention,
        )
        if base_reason:
            _retain_trace_once(
                paths=paths,
                records=trace_records,
                retained_keys=retained_trace_keys,
                rows=episode_step_rows,
                run_id=run_id,
                arm_id=arm.arm_id,
                replicate_index=replicate_index,
                schema_seed=schema_seed,
                episode_index=episode_index,
                reason=base_reason,
            )
        if (
            config.retention.writes_selected_traces
            and config.retention.retain_first_success
            and terminated
            and not first_success_retained
        ):
            first_success_retained = True
            _retain_trace_once(
                paths=paths,
                records=trace_records,
                retained_keys=retained_trace_keys,
                rows=episode_step_rows,
                run_id=run_id,
                arm_id=arm.arm_id,
                replicate_index=replicate_index,
                schema_seed=schema_seed,
                episode_index=episode_index,
                reason="first_success",
            )
        retained_trace_count = len(trace_records) - retained_count_before
        tier_indices_seen = sorted(
            {
                int(row["tier_index"])
                for row in episode_surface_rows
                if row.get("tier_index") is not None
            }
        )
        episode_rows.append(
            {
                "run_id": run_id,
                "arm_id": arm.arm_id,
                "replicate_index": replicate_index,
                "schema_seed": schema_seed,
                "episode_index": episode_index,
                "max_seconds": config.max_seconds_per_episode,
                "seconds_elapsed": state.time_step,
                "step_count": episode_step_count,
                "total_reward": total_reward,
                "terminated": terminated,
                "truncated": truncated,
                "failure_reason": failure_reason,
                "ppo_sample_count": episode_sample_count,
                "controller_event_count": episode_controller_count,
                "pointwise_surface_count": len(episode_surface_rows),
                "empty_actor_surface_count": sum(
                    1
                    for row in episode_surface_rows
                    if int(row.get("candidate_action_count", 0) or 0) <= 0
                ),
                "tier_indices_seen": "|".join(str(index) for index in tier_indices_seen),
                "retained_trace_count": retained_trace_count,
                "optimizer_steps": sum(entry.optimizer_steps for entry in policy_bank.entries.values()),
            }
        )
    if (
        config.retention.writes_selected_traces
        and config.retention.retain_best_reward
        and best_episode_index >= 0
    ):
        _retain_trace_once(
            paths=paths,
            records=trace_records,
            retained_keys=retained_trace_keys,
            rows=best_trace_rows,
            run_id=run_id,
            arm_id=arm.arm_id,
            replicate_index=replicate_index,
            schema_seed=schema_seed,
            episode_index=best_episode_index,
            reason="best_reward",
        )
    for tier_index, buffer in sorted(buffers.items()):
        if buffer.ready_count() > 0:
            update_rows.extend(
                _update_ready_buffers(
                    buffers={tier_index: buffer},
                    policy_bank=policy_bank,
                    config=config,
                    run_id=run_id,
                    arm_id=arm.arm_id,
                    actual_device=actual_device,
                    global_update_index_start=global_update_index,
                    force=True,
                )
            )
            global_update_index += 1
    tier_policy_rows = [
        {
            "run_id": run_id,
            "arm_id": arm.arm_id,
            **entry.to_manifest(),
        }
        for _, entry in sorted(policy_bank.entries.items())
    ]
    return {
        "episode_rows": episode_rows,
        "step_rows": step_rows,
        "controller_rows": controller_rows,
        "surface_rows": surface_rows,
        "sample_rows": sample_rows,
        "update_rows": update_rows,
        "tier_policy_rows": tier_policy_rows,
        "trace_records": trace_records,
    }


def _update_ready_buffers(
    *,
    buffers: dict[int, TierRolloutBuffer],
    policy_bank: TierPolicyBank,
    config: WarehouseFullTowerPPOConfig,
    run_id: str,
    arm_id: str,
    actual_device: str,
    global_update_index_start: int,
    force: bool = False,
) -> list[dict[str, object]]:
    rows: list[dict[str, object]] = []
    for tier_index, buffer in sorted(buffers.items()):
        if not force and buffer.ready_count() < config.ppo.min_tier_update_samples:
            buffer.carry_forward()
            continue
        samples = buffer.take_ready_samples()
        entry = policy_bank.entry_for_tier(tier_index)
        result = update_tier_policy(
            entry=entry,
            samples=samples,
            gamma=config.ppo.gamma,
            gae_lambda=config.ppo.gae_lambda,
            clip_epsilon=config.ppo.clip_epsilon,
            value_coef=config.ppo.value_coef,
            entropy_coef=config.ppo.entropy_coef,
            max_grad_norm=config.ppo.max_grad_norm,
            ppo_epochs=config.ppo.ppo_epochs,
            minibatch_size=config.ppo.minibatch_size,
        )
        entry.refresh_rollout_snapshot(update_index=entry.optimizer_steps)
        rows.append(
            result.to_row(
                run_id=run_id,
                arm_id=arm_id,
                global_update_index=global_update_index_start,
                device=actual_device,
            )
        )
    return rows


def _decision_context(
    *,
    surface: Any,
    run_id: str,
    episode_index: int,
    replicate_index: int,
    schema_seed: int,
    ppo_sample_index: int,
    controller_event_index: int,
    arm_id: str,
) -> DecisionContextRecord:
    decision_id = _stable_id(run_id, str(episode_index), str(ppo_sample_index), surface.current_state.stable_id)
    return DecisionContextRecord(
        decision_context_id=decision_id,
        episode_id=f"{run_id}:episode:{episode_index}",
        replicate_index=replicate_index,
        schema_seed=schema_seed,
        arm_id=arm_id,
        tier_index=surface.tier_index,
        ppo_sample_index=ppo_sample_index,
        controller_event_index_start=controller_event_index,
        controller_event_index_end=controller_event_index,
        environment_second=surface.current_state.time_step,
        active_tier=surface.tier_index,
        current_concrete_state_digest=_stable_id(surface.current_state.stable_id),
        current_position_at_every_tier=surface.current_position_at_every_tier,
        tower_position_key="|".join("" if item is None else str(item) for item in surface.current_position_at_every_tier),
        runtime_snapshot_id=_stable_id(surface.schema_id, surface.current_state.stable_id),
        schema_arm_id=arm_id,
        graph_snapshot_id=_stable_id(run_id, surface.current_state.stable_id),
        tower_snapshot_id=_stable_id(run_id, surface.schema_id, surface.current_state.stable_id),
        state_geometry_record_id=_stable_id(surface.state_cell_id, surface.current_state.stable_id),
        candidate_action_ids_ordered=surface.candidate_action_ids,
        candidate_local_indices=tuple(range(len(surface.action_choices))),
        candidate_mask=surface.candidate_mask,
        mask_kind=surface.mask_kind,
        mask_semantics_id=surface.semantics_id,
        state_collapser_source_ref="state_collapser.PartitionTower",
        controller_event_refs=(f"{run_id}:controller:{controller_event_index}",),
    )


def _retain_trace_once(
    *,
    paths: FullTowerPPOPaths,
    records: list[TraceRecord],
    retained_keys: set[tuple[int, str]],
    rows: list[dict[str, object]],
    run_id: str,
    arm_id: str,
    replicate_index: int,
    schema_seed: int,
    episode_index: int,
    reason: str,
) -> None:
    if not rows:
        return
    key = (episode_index, reason)
    if key in retained_keys:
        return
    retained_keys.add(key)
    records.append(
        write_selected_trace(
            trace_dir=paths.trace_episode_dir(
                run_id=run_id,
                episode_index=episode_index,
            ),
            rows=rows,
            run_id=run_id,
            arm_id=arm_id,
            replicate_index=replicate_index,
            schema_seed=schema_seed,
            episode_index=episode_index,
            reason=reason,
        )
    )


def _write_run_tables(
    *,
    run_root: Path,
    run_result: dict[str, Any],
    write_full_debug_tables: bool,
) -> None:
    write_csv(
        run_root / "episodes.csv",
        run_result["episode_rows"],
        EPISODE_FIELDNAMES,
        create_parents=True,
    )
    if write_full_debug_tables:
        write_csv(run_root / "step_events.csv", run_result["step_rows"], STEP_FIELDNAMES)
        write_csv(
            run_root / "control_events.csv",
            run_result["controller_rows"],
            CONTROLLER_EVENT_FIELDNAMES,
        )
        write_csv(
            run_root / "rollout_samples.csv",
            run_result["sample_rows"],
            ROLLOUT_SAMPLE_FIELDNAMES,
        )
    write_json(
        run_root / "run_manifest.json",
        {
            "run_id": run_root.name,
            "write_full_debug_tables": write_full_debug_tables,
        },
        create_parents=True,
    )


def _select_device(config: WarehouseFullTowerPPOConfig) -> str:
    torch = _require_torch()
    requested = config.device.device
    if requested == "cpu":
        return "cpu"
    if requested == "auto":
        return "cuda" if torch.cuda.is_available() else "cpu"
    if requested == "cuda":
        if torch.cuda.is_available():
            return "cuda"
        if config.device.allow_cuda_fallback:
            return "cpu"
        raise RuntimeError("CUDA requested but not available")
    raise ValueError(f"unknown device request: {requested}")


def _terminal(instance: Any, state: Any) -> bool:
    return (
        all(state.box_positions[box_id] == target for box_id, target in instance.manifest.box_target_map().items())
        and all(state.robot_positions[robot_id] == target for robot_id, target in instance.manifest.robot_target_map().items())
    )


def _version(package: str) -> str:
    import importlib.metadata as metadata

    try:
        return metadata.version(package)
    except metadata.PackageNotFoundError:
        return "not_installed"


def _stable_id(*parts: str) -> str:
    return hashlib.sha256("|".join(parts).encode("utf-8")).hexdigest()[:24]


def _action_summary(action: Any) -> str:
    commands = getattr(action, "commands", {})
    if not commands:
        return action.stable_id
    moving = [
        f"{robot_id}:{command.value}"
        for robot_id, command in sorted(commands.items())
        if getattr(command, "value", str(command)) != "stay"
    ]
    if not moving:
        return "all stay"
    return ";".join(moving[:8]) + (";..." if len(moving) > 8 else "")


def _require_torch() -> Any:
    try:
        import torch
    except ImportError as exc:  # pragma: no cover
        raise RuntimeError("torch is required for Warehouse full-tower PPO") from exc
    return torch
