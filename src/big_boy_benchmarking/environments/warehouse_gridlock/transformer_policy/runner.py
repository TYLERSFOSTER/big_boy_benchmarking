"""Runner for Warehouse Gridlock transformer policy training."""

from __future__ import annotations

import csv
import time
from dataclasses import dataclass
from pathlib import Path

from tqdm import tqdm

from big_boy_benchmarking.artifacts.writers import append_jsonl, write_json

from ..instances import load_instance
from ..masked_direct_vs_live_lift_tower.admissibility import mask_tower_action_candidates
from ..masked_direct_vs_live_lift_tower.readiness_source import (
    load_readiness_source,
    validate_readiness_source,
)
from ..masked_direct_vs_live_lift_tower.tower_surface import (
    build_tower_surface,
    select_live_lift,
)
from ..policies.contracts import (
    WarehouseFullActionVector,
    config_from_instance_state,
)
from ..policies.resolver import BoundedDeterministicWarehouseActionResolver
from ..replay import (
    EpisodeReplayResult,
    render_episode_gif,
)
from ..rewards import target_counts
from .action_selection import (
    decision_with_projection,
    select_direct_action,
    select_tower_candidate_action,
)
from .aggregation import write_result_tables
from .checkpoints import (
    CheckpointRecord,
    checkpoint_due,
    prune_checkpoint_records,
    save_checkpoint,
    write_checkpoint_manifest,
)
from .config import (
    DIRECT_ARM_ID,
    TOWER_ARM_ID,
    WarehouseTransformerPolicyRunConfig,
)
from .docs_writer import (
    write_human_docs,
    write_readout_source,
)
from .encoding import (
    WarehouseEncodingContext,
    encode_warehouse_batch,
)
from .manifests import write_initial_manifests
from .model import build_model
from .paths import TransformerEvaluationPaths
from .paths import run_id as build_run_id
from .torch_runtime import (
    require_torch,
    runtime_info,
)
from .trace_retention import (
    TraceRecord,
    should_retain_episode,
    write_artifact_retention_manifest,
    write_selected_trace,
)
from .training import (
    EpisodeRolloutBuffer,
    apply_actor_critic_update,
)


@dataclass(frozen=True)
class WarehouseTransformerPolicyResult:
    status: str
    artifact_paths: dict[str, str]
    summary: dict[str, object]


def run_transformer_policy(
    config: WarehouseTransformerPolicyRunConfig,
) -> WarehouseTransformerPolicyResult:
    started = time.perf_counter()
    torch = require_torch()
    runtime = runtime_info(requested_device=config.device)
    device = runtime.selected_device
    paths = TransformerEvaluationPaths(
        repo_root=config.repo_root,
        artifact_root=config.artifact_root,
    )
    paths.ensure()
    readiness_source = load_readiness_source(config.readiness_source)
    validate_readiness_source(readiness_source, expected_instance_id=config.instance_id)
    instance = load_instance(instance_id=config.instance_id)
    model = build_model(config.model).to(device)
    optimizer = torch.optim.AdamW(model.parameters(), lr=config.optimizer.learning_rate)
    manifest_paths = write_initial_manifests(
        paths=paths,
        config=config,
        instance=instance,
        model=model,
        runtime=runtime,
    )
    write_json(paths.artifact_root / "optimizer_state_manifest.json", {"optimizer_steps": 0})
    episode_rows: list[dict[str, object]] = []
    run_index_rows: list[dict[str, object]] = []
    resolver_rows: list[dict[str, object]] = []
    tower_rows: list[dict[str, object]] = []
    timing_rows: list[dict[str, object]] = []
    checkpoint_records: list[CheckpointRecord] = []
    trace_records: list[TraceRecord] = []
    optimizer_steps = 0
    total_episodes = (
        config.episodes
        * config.replicates
        * config.schema_seeds
        * len(config.active_arm_ids)
    )
    progress = tqdm(
        total=total_episodes,
        disable=config.progress_every_episodes == 0,
        file=None,
        desc=f"warehouse transformer {config.run_label}",
    )
    try:
        for schema_seed in range(config.schema_seeds):
            for replicate_index in range(config.replicates):
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
                    append_jsonl(
                        paths.progress_events,
                        {
                            "event_type": "run_start",
                            "run_id": current_run_id,
                            "arm_id": arm_id,
                            "replicate_index": replicate_index,
                            "schema_seed": schema_seed,
                        },
                        create_parents=True,
                    )
                    run_started = time.perf_counter()
                    run_episode_rows, optimizer_steps, run_checkpoints, run_traces = _run_arm(
                        instance=instance,
                        config=config,
                        paths=paths,
                        device=device,
                        model=model,
                        optimizer=optimizer,
                        arm_id=arm_id,
                        run_id=current_run_id,
                        replicate_index=replicate_index,
                        schema_seed=schema_seed,
                        seed=seed,
                        optimizer_steps=optimizer_steps,
                        progress=progress,
                        resolver_rows=resolver_rows,
                        tower_rows=tower_rows,
                    )
                    episode_rows.extend(run_episode_rows)
                    checkpoint_records.extend(run_checkpoints)
                    checkpoint_records = prune_checkpoint_records(
                        records=checkpoint_records,
                        keep_last_n=config.checkpoint.keep_last_n_checkpoints,
                        keep_best_n=config.checkpoint.keep_best_n_checkpoints,
                    )
                    trace_records.extend(run_traces)
                    duration = time.perf_counter() - run_started
                    timing_rows.append(
                        {
                            "run_id": current_run_id,
                            "arm_id": arm_id,
                            "duration_seconds": duration,
                            "episode_count": config.episodes,
                        }
                    )
                    run_index_rows.append(
                        {
                            "run_id": current_run_id,
                            "arm_id": arm_id,
                            "replicate_index": replicate_index,
                            "schema_seed": schema_seed,
                            "seed": seed,
                            "status": "success",
                            "run_root": str(run_root),
                        }
                    )
                    append_jsonl(
                        paths.progress_events,
                        {
                            "event_type": "run_complete",
                            "run_id": current_run_id,
                            "arm_id": arm_id,
                            "duration_seconds": duration,
                        },
                        create_parents=True,
                    )
    finally:
        progress.close()

    write_checkpoint_manifest(paths.checkpoint_manifest, checkpoint_records)
    artifact_retention = write_artifact_retention_manifest(
        path=paths.artifact_retention_manifest,
        artifact_root=paths.artifact_root,
        config=config.trace_retention,
        trace_records=trace_records,
    )
    summary = write_result_tables(
        results_dir=paths.results_dir,
        episode_rows=episode_rows,
        run_index_rows=run_index_rows,
        resolver_rows=resolver_rows,
        tower_rows=tower_rows,
        timing_rows=timing_rows,
        trace_records=trace_records,
        checkpoint_records=checkpoint_records,
        artifact_retention=artifact_retention,
    )
    readout_source = write_readout_source(paths=paths, run_label=config.run_label, summary=summary)
    docs = write_human_docs(paths=paths, run_label=config.run_label, summary=summary)
    elapsed = time.perf_counter() - started
    append_jsonl(
        paths.progress_events,
        {"event_type": "evaluation_complete", "status": "success", "duration_seconds": elapsed},
        create_parents=True,
    )
    return WarehouseTransformerPolicyResult(
        status="success",
        artifact_paths={
            **manifest_paths,
            "checkpoint_manifest": str(paths.checkpoint_manifest),
            "artifact_retention_manifest": str(paths.artifact_retention_manifest),
            "aggregate_summary": str(paths.aggregate_summary),
            "readout_source": str(readout_source),
            **docs,
        },
        summary={**summary, "duration_seconds": elapsed},
    )


def summarize_transformer_policy(
    *,
    repo_root: Path,
    artifact_root: Path,
) -> WarehouseTransformerPolicyResult:
    paths = TransformerEvaluationPaths(repo_root=repo_root, artifact_root=artifact_root)
    summary_path = paths.aggregate_summary
    if not summary_path.exists():
        raise FileNotFoundError(f"aggregate summary does not exist: {summary_path}")
    import json

    summary = json.loads(summary_path.read_text(encoding="utf-8"))
    readout_source = write_readout_source(
        paths=paths,
        run_label=artifact_root.name,
        summary=summary,
    )
    docs = write_human_docs(paths=paths, run_label=artifact_root.name, summary=summary)
    return WarehouseTransformerPolicyResult(
        status=str(summary.get("status", "complete")),
        artifact_paths={"readout_source": str(readout_source), **docs},
        summary=summary,
    )


def render_transformer_policy_episode(
    *,
    artifact_root: Path,
    arm_id: str,
    replicate_index: int,
    schema_seed: int,
    episode_index: int,
    output_path: Path | None = None,
    frame_ms: int = 140,
    cell_pixels: int = 36,
    max_frames: int | None = None,
) -> EpisodeReplayResult:
    trace_index = artifact_root / "results" / "trace_episode_index.csv"
    if not trace_index.exists():
        raise FileNotFoundError(f"trace_episode_index.csv does not exist: {trace_index}")
    with trace_index.open(newline="", encoding="utf-8") as handle:
        rows = list(csv.DictReader(handle))
    matches = [
        row
        for row in rows
        if row["arm_id"] == arm_id
        and int(row["replicate_index"]) == replicate_index
        and int(row["schema_seed"]) == schema_seed
        and int(row["episode_index"]) == episode_index
    ]
    if not matches:
        available = ", ".join(sorted({row["episode_index"] for row in rows})) or "none"
        raise FileNotFoundError(
            f"episode {episode_index} was not retained as a renderable trace. "
            f"Artifact root: {artifact_root}. "
            f"Available retained episodes: {available}. "
            "Rerun with --trace-episode-index for the requested episode or "
            "--trace-every-episodes to retain a regular sample."
        )
    trace_path = Path(matches[0]["trace_path"])
    return render_episode_gif(
        episode_index=episode_index,
        output_path=output_path,
        step_events_path=trace_path,
        frame_ms=frame_ms,
        cell_pixels=cell_pixels,
        max_frames=max_frames,
    )


def _run_arm(
    *,
    instance,
    config: WarehouseTransformerPolicyRunConfig,
    paths: TransformerEvaluationPaths,
    device: str,
    model,
    optimizer,
    arm_id: str,
    run_id: str,
    replicate_index: int,
    schema_seed: int,
    seed: int,
    optimizer_steps: int,
    progress,
    resolver_rows: list[dict[str, object]],
    tower_rows: list[dict[str, object]],
) -> tuple[list[dict[str, object]], int, list[CheckpointRecord], list[TraceRecord]]:
    episode_rows: list[dict[str, object]] = []
    checkpoint_records: list[CheckpointRecord] = []
    trace_records: list[TraceRecord] = []
    resolver = BoundedDeterministicWarehouseActionResolver(
        projection_attempt_budget=config.projection_attempt_budget
    )
    rolling_rewards: list[float] = []
    best_reward = float("-inf")
    final_episode_index = config.episodes - 1
    for episode_index in range(config.episodes):
        episode_max_seconds = config.curriculum.max_seconds_for_episode(episode_index)
        state = instance.start_state
        buffer = EpisodeRolloutBuffer()
        trace_rows: list[dict[str, object]] = []
        total_reward = 0.0
        failure_reason = ""
        last_counts = target_counts(
            state,
            robot_targets=instance.manifest.robot_target_map(),
            box_targets=instance.manifest.box_target_map(),
        )
        for step_index in range(episode_max_seconds):
            selected_payload = _select_step_action(
                instance=instance,
                config=config,
                model=model,
                arm_id=arm_id,
                state=state,
                run_id=run_id,
                episode_index=episode_index,
                step_index=step_index,
                schema_seed=schema_seed,
                seed=seed,
                max_seconds=episode_max_seconds,
                device=device,
                tower_rows=tower_rows,
            )
            if selected_payload is None:
                failure_reason = "no_policy_action_or_live_lift"
                break
            selected = selected_payload["selected"]
            resolved = resolver.resolve(
                instance=instance,
                state=state,
                raw_action_vector=selected.selected_action_vector,
                max_seconds=episode_max_seconds,
                robot_command_margins=selected.decision.robot_command_margins,
            )
            decision = decision_with_projection(
                selected=selected,
                raw_valid=resolved.projection_trace.raw_valid,
                selected_valid=resolved.projection_trace.selected_valid,
                projection_trace=resolved.projection_trace,
                selected_action_vector=resolved.selected_action_vector,
            )
            result = resolved.step_result
            total_reward += float(result.reward)
            buffer.append(
                log_probability=selected.log_probability,
                value=selected.value,
                reward=float(result.reward),
                entropy=selected.entropy,
            )
            resolver_rows.append(
                {
                    "run_id": run_id,
                    "arm_id": arm_id,
                    "raw_valid": resolved.projection_trace.raw_valid,
                    "selected_valid": resolved.projection_trace.selected_valid,
                    "fallback_used": resolved.projection_trace.fallback_used,
                    "projection_attempt_count": resolved.projection_trace.attempt_count,
                    "successor_out_count_used_for_selection": (
                        resolved.projection_trace.successor_out_count_used_for_selection
                    ),
                }
            )
            last_counts = target_counts(
                result.next_state,
                robot_targets=instance.manifest.robot_target_map(),
                box_targets=instance.manifest.box_target_map(),
            )
            trace_rows.append(
                _trace_row(
                    run_id=run_id,
                    arm_id=arm_id,
                    replicate_index=replicate_index,
                    schema_seed=schema_seed,
                    episode_index=episode_index,
                    step_index=step_index,
                    state_id=state.stable_id,
                    next_state_id=result.next_state.stable_id,
                    action_vector=(
                        decision.selected_action_vector
                        or WarehouseFullActionVector.all_stay(
                            tuple(sorted(instance.manifest.robot_ids))
                        )
                    ),
                    reward=float(result.reward),
                    counts=last_counts,
                    terminated=result.terminated,
                    truncated=result.truncated,
                )
            )
            state = result.next_state
            if result.terminated or result.truncated:
                break
        update = apply_actor_critic_update(
            model=model,
            optimizer=optimizer,
            buffer=buffer,
            config=config.optimizer,
            optimizer_steps_before=optimizer_steps,
        )
        if update is not None:
            optimizer_steps = update.optimizer_steps
        rolling_rewards.append(total_reward)
        rolling_reward = sum(rolling_rewards[-10:]) / len(rolling_rewards[-10:])
        if checkpoint_due(
            episode_index=episode_index,
            every=config.checkpoint.checkpoint_every_episodes,
            final_episode_index=final_episode_index,
        ):
            checkpoint_records.append(
                save_checkpoint(
                    path=paths.checkpoints_dir
                    / f"{run_id}-episode{episode_index:06d}-{optimizer_steps:06d}.pt",
                    model=model,
                    optimizer=optimizer,
                    config=config,
                    episode_index=episode_index,
                    optimizer_steps=optimizer_steps,
                    reason="final" if episode_index == final_episode_index else "periodic",
                    rolling_reward=rolling_reward,
                )
            )
        if total_reward > best_reward:
            best_reward = total_reward
            checkpoint_records.append(
                save_checkpoint(
                    path=paths.checkpoints_dir
                    / f"{run_id}-best-episode{episode_index:06d}-{optimizer_steps:06d}.pt",
                    model=model,
                    optimizer=optimizer,
                    config=config,
                    episode_index=episode_index,
                    optimizer_steps=optimizer_steps,
                    reason="best",
                    rolling_reward=rolling_reward,
                )
            )
        retain, reason = should_retain_episode(
            episode_index=episode_index,
            final_episode_index=final_episode_index,
            config=config.trace_retention,
        )
        if retain:
            trace_records.append(
                write_selected_trace(
                    trace_dir=paths.trace_episode_dir(run_id=run_id, episode_index=episode_index),
                    rows=trace_rows,
                    run_id=run_id,
                    arm_id=arm_id,
                    replicate_index=replicate_index,
                    schema_seed=schema_seed,
                    episode_index=episode_index,
                    reason=reason,
                )
            )
        episode_row = {
            "run_id": run_id,
            "arm_id": arm_id,
            "replicate_index": replicate_index,
            "schema_seed": schema_seed,
            "episode_index": episode_index,
            "max_seconds": episode_max_seconds,
            "step_count": buffer.step_count,
            "total_reward": total_reward,
            "terminated": bool(
                last_counts["correct_box_count"] == len(instance.manifest.box_ids)
                and last_counts["correct_robot_count"] == len(instance.manifest.robot_ids)
            ),
            "truncated": buffer.step_count >= episode_max_seconds,
            "failure_reason": failure_reason,
            "optimizer_steps": optimizer_steps,
            "policy_loss": "" if update is None else update.policy_loss,
            "value_loss": "" if update is None else update.value_loss,
            "entropy": "" if update is None else update.entropy,
            "grad_norm": "" if update is None else update.grad_norm,
            "correct_box_count": last_counts["correct_box_count"],
            "correct_robot_count": last_counts["correct_robot_count"],
        }
        episode_rows.append(episode_row)
        if config.progress_every_episodes > 0 and (
            episode_index % config.progress_every_episodes == 0
            or episode_index == final_episode_index
        ):
            progress.set_postfix_str(
                "reward="
                f"{total_reward:.3f} rolling={rolling_reward:.3f} "
                f"optimizer_steps={optimizer_steps} episode={episode_index + 1}/{config.episodes} "
                f"max_seconds={episode_max_seconds} arm={_short_arm(arm_id)}"
            )
        progress.update(1)
    return episode_rows, optimizer_steps, checkpoint_records, trace_records


def _select_step_action(
    *,
    instance,
    config: WarehouseTransformerPolicyRunConfig,
    model,
    arm_id: str,
    state,
    run_id: str,
    episode_index: int,
    step_index: int,
    schema_seed: int,
    seed: int,
    max_seconds: int,
    device: str,
    tower_rows: list[dict[str, object]],
) -> dict[str, object] | None:
    full_config = config_from_instance_state(
        instance=instance,
        state=state,
        max_seconds_per_episode=max_seconds,
    )
    if arm_id == TOWER_ARM_ID:
        surface = build_tower_surface(
            instance=instance,
            state=state,
            candidate_budget=config.candidate_proposals_per_step,
            seed=seed + episode_index * 10000 + step_index,
            schema_seed=schema_seed,
            max_seconds=max_seconds,
            max_active_robots=config.max_active_robots,
            candidate_mix_id=config.candidate_mix_id,
        )
        lift, failure_reason = select_live_lift(surface)
        candidates = surface.tower_action_candidates()
        _mask, admissible_candidates = mask_tower_action_candidates(
            instance=instance,
            state=state,
            candidates=candidates,
            max_seconds=max_seconds,
        )
        tower_rows.append(
            {
                "run_id": run_id,
                "arm_id": arm_id,
                "episode_index": episode_index,
                "step_index": step_index,
                "lift_failure": lift is None,
                "failure_reason": failure_reason if lift is None else "",
                "candidate_count": len(admissible_candidates),
                "live_out_count": surface.live_out_count,
            }
        )
        if lift is None or not admissible_candidates:
            return None
        context = WarehouseEncodingContext(
            arm_id=arm_id,
            second=state.time_step,
            max_seconds=max_seconds,
            tier=surface.tier,
            tier_state_id=surface.state_cell_id,
            live_lift_out_count=surface.live_out_count,
            candidate_count=len(admissible_candidates),
        )
        encoded = encode_warehouse_batch([full_config], [context], device=device)
        output = model(encoded)
        selected = select_tower_candidate_action(
            policy_id=f"{arm_id}_transformer",
            output=output,
            robot_ids=encoded.robot_ids,
            candidates=list(admissible_candidates),
            second=state.time_step,
            episode_index=episode_index,
            step_index=step_index,
            seed=seed,
            tier=surface.tier,
            tier_state_id=surface.state_cell_id,
        )
        if selected is None:
            return None
        return {"selected": selected}
    if arm_id == DIRECT_ARM_ID:
        context = WarehouseEncodingContext(
            arm_id=arm_id,
            second=state.time_step,
            max_seconds=max_seconds,
        )
        encoded = encode_warehouse_batch([full_config], [context], device=device)
        output = model(encoded)
        return {
            "selected": select_direct_action(
                policy_id=f"{arm_id}_transformer",
                output=output,
                robot_ids=encoded.robot_ids,
                second=state.time_step,
                episode_index=episode_index,
                step_index=step_index,
                seed=seed,
            )
        }
    raise ValueError(f"unknown Warehouse transformer arm id: {arm_id}")


def _trace_row(
    *,
    run_id: str,
    arm_id: str,
    replicate_index: int,
    schema_seed: int,
    episode_index: int,
    step_index: int,
    state_id: str,
    next_state_id: str,
    action_vector: WarehouseFullActionVector,
    reward: float,
    counts: dict[str, int],
    terminated: bool,
    truncated: bool,
) -> dict[str, object]:
    active = [
        f"{robot_id}:{command.value}"
        for robot_id, command in sorted(action_vector.commands.items())
        if command.value != "stay"
    ]
    return {
        "run_id": run_id,
        "arm_id": arm_id,
        "replicate_index": replicate_index,
        "schema_seed": schema_seed,
        "episode_index": episode_index,
        "step_index": step_index,
        "state_id": state_id,
        "next_state_id": next_state_id,
        "selected_action_id": action_vector.stable_id,
        "selected_action_summary": "all_stay" if not active else "|".join(active),
        "reward": reward,
        "correct_box_count": counts["correct_box_count"],
        "correct_robot_count": counts["correct_robot_count"],
        "terminated": terminated,
        "truncated": truncated,
    }


def _short_arm(arm_id: str) -> str:
    if arm_id == TOWER_ARM_ID:
        return "tower_transformer"
    if arm_id == DIRECT_ARM_ID:
        return "direct_transformer"
    return arm_id
