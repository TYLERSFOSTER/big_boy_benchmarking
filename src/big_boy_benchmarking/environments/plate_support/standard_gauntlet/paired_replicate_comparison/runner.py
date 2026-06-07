"""Runner for PlateSupport gauntlet Stage 6 paired replicate comparison."""

from __future__ import annotations

import csv
import json
import random
import time
from dataclasses import dataclass
from datetime import UTC, datetime
from pathlib import Path
from typing import Any

from big_boy_benchmarking.artifacts.schemas import ARTIFACT_SCHEMA_VERSION
from big_boy_benchmarking.artifacts.writers import write_csv, write_json
from big_boy_benchmarking.environments.plate_support.upstream import (
    import_plate_support_surface,
)

from ..ids import (
    ENVIRONMENT_FAMILY_ID,
    ENVIRONMENT_INSTANCE_ID,
    PAIRED_REPLICATE_COMPARISON_STAGE_ID,
    STAGE_DEFINITIONS,
    SUITE_ID,
)
from ..paths import suite_evaluation_root, suite_readout_surface
from ..status import STAGE_STATUS_FIELDS
from ..tower_training_health.candidate_source import TrainingCandidate
from ..tower_training_health.training_surfaces import (
    build_training_surface,
    cell_text,
    choose_executable_tower_action,
    next_state_best_value,
    state_payload_text,
)
from .aggregation import (
    RESULT_TABLE_FIELDNAMES,
    build_stage6_aggregate_row,
    build_stage6_summary,
    build_stage6_tables,
)
from .arms import (
    DIRECT_BASELINE_ARM_ID,
    ComparisonArm,
    build_comparison_arms,
)
from .config import PairedReplicateComparisonConfig
from .docs_writer import write_paired_replicate_comparison_docs
from .events import (
    COMPARISON_CONTROLLER_FIELDS,
    COMPARISON_EPISODE_FIELDS,
    COMPARISON_LEARNER_FIELDS,
    COMPARISON_LIFT_FIELDS,
    COMPARISON_STEP_FIELDS,
    COMPARISON_TIER_FIELDS,
    COMPARISON_TIMING_FIELDS,
)
from .manifests import (
    comparison_arm_manifest,
    stage_budget_lock,
    stage_input_manifest,
    stage_manifest,
    stage_output_manifest,
    target_policy_manifest,
)
from .seed_bundles import PairedSeedBundle, build_paired_seed_bundles
from .stage_sources import Stage6SourceError, Stage6Sources, load_stage6_sources
from .target_policy import target_hit


@dataclass(frozen=True)
class PairedReplicateComparisonResult:
    """Run result for Stage 6."""

    status: str
    stage_root: Path
    readout_source_path: Path
    artifact_paths: dict[str, str]
    claim_status: str
    failure_reason: str | None = None


def run_paired_replicate_comparison(
    config: PairedReplicateComparisonConfig,
    *,
    repo_root: Path | str,
) -> PairedReplicateComparisonResult:
    """Run Stage 6 and write paired comparison artifacts."""

    repo_root = Path(repo_root).expanduser().resolve()
    artifact_root = Path(config.artifact_root).expanduser().resolve()
    stage_root = artifact_root / "stages" / "paired_replicate_comparison"
    stage_root.mkdir(parents=True, exist_ok=True)
    try:
        sources = load_stage6_sources(
            candidate_source_path=config.candidate_source_path,
            training_health_source_path=config.training_health_source_path,
            threshold_source_path=config.threshold_source_path,
            repo_root=repo_root,
            candidate_cap=config.candidate_cap,
            allow_warning_candidates=config.allow_warning_candidates,
            allow_legacy_dependency=config.allow_legacy_dependency,
        )
    except Stage6SourceError as exc:
        return _write_blocked_result(
            config=config,
            repo_root=repo_root,
            stage_root=stage_root,
            reason=str(exc),
        )

    target = sources.stage5_source.recommended_target
    episodes_per_replicate = (
        config.episodes_per_replicate
        if config.episodes_per_replicate is not None
        else sources.stage5_source.episodes_per_replicate
    )
    replicates_per_arm = (
        config.replicates_per_arm
        if config.replicates_per_arm is not None
        else sources.stage5_source.replicates_per_arm
    )
    arms = build_comparison_arms(
        candidate=sources.selected_candidate,
        include_direct_baseline=config.include_direct_baseline,
        include_no_contraction_control=config.include_no_contraction_control,
    )
    seed_bundles = build_paired_seed_bundles(
        base_seed=config.base_seed,
        replicate_count=replicates_per_arm,
    )
    raw = _run_active_arms(
        config=config,
        stage_root=stage_root,
        sources=sources,
        target=target,
        arms=arms,
        seed_bundles=seed_bundles,
        episodes_per_replicate=episodes_per_replicate,
    )
    candidate_arm_id = _candidate_arm_id(arms)
    tables = build_stage6_tables(
        arms=arms,
        seed_rows=[bundle.to_row() for bundle in seed_bundles],
        episode_rows=raw["episode_rows"],
        step_rows=raw["step_rows"],
        controller_rows=raw["controller_rows"],
        learner_rows=raw["learner_rows"],
        lift_rows=raw["lift_rows"],
        tier_rows=raw["tier_rows"],
        timing_rows=raw["timing_rows"],
        run_index_rows=raw["run_index_rows"],
        health_rows=sources.stage4_source.tables["candidate_training_health_summary"],
        target_policy_id=str(target["target_policy_id"]),
        direct_arm_id=DIRECT_BASELINE_ARM_ID,
        candidate_arm_id=candidate_arm_id,
    )
    output_paths = _write_result_tables(stage_root=stage_root, tables=tables)
    dependency_status = str(sources.dependency_state.get("inspection_status", "unknown"))
    aggregate_row = build_stage6_aggregate_row(
        artifact_root=str(stage_root),
        tables=tables,
        source_paths=(
            str(sources.stage3_source.path),
            str(sources.stage4_source.path),
            str(sources.stage5_source.path),
        ),
        state_collapser_dependency_status=dependency_status,
    )
    aggregate_summary = build_stage6_summary(aggregate_row)
    claim_row = tables["comparison_claim_summary"][0]
    arm_rows = [arm.to_row() for arm in arms]

    write_json(stage_root / "stage_manifest.json", stage_manifest(config), create_parents=True)
    write_json(
        stage_root / "stage_budget_lock.json",
        stage_budget_lock(
            config,
            episodes_per_replicate=episodes_per_replicate,
            replicates_per_arm=replicates_per_arm,
        ),
        create_parents=True,
    )
    write_json(
        stage_root / "stage_input_manifest.json",
        stage_input_manifest(
            candidate_source_path=str(sources.stage3_source.path),
            training_health_source_path=str(sources.stage4_source.path),
            threshold_source_path=str(sources.stage5_source.path),
            selected_candidate_id=sources.selected_candidate.candidate_id,
        ),
        create_parents=True,
    )
    write_json(
        stage_root / "comparison_arm_manifest.json",
        comparison_arm_manifest(arm_rows),
        create_parents=True,
    )
    write_json(
        stage_root / "target_policy_manifest.json",
        target_policy_manifest(target),
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
                "stage_id": PAIRED_REPLICATE_COMPARISON_STAGE_ID,
                "run_label": config.run_label,
                "status": aggregate_row["status"],
                "started_at": raw["started_at"],
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
    readout_surface = suite_readout_surface(repo_root) / "paired_replicate_comparison"
    readout_source_path = readout_surface / "readout_source.json"
    write_json(
        readout_source_path,
        _stage6_readout_source(
            readout_surface=readout_surface,
            stage_root=stage_root,
            config=config,
            output_paths=output_paths,
            target=target,
            claim_row=claim_row,
        ),
        create_parents=True,
    )
    doc_paths = write_paired_replicate_comparison_docs(
        readout_surface=readout_surface,
        artifact_root=artifact_root,
        stage_root=stage_root,
        aggregate_summary=aggregate_summary,
        claim_row=claim_row,
        target=target,
        readout_source_path=readout_source_path,
        output_paths=output_paths,
    )
    _update_suite_readout_source(
        repo_root=repo_root,
        run_label=config.run_label,
        stage6_readout_source=readout_source_path,
        claim_row=claim_row,
    )
    all_paths = {
        **output_paths,
        "stage_manifest": str(stage_root / "stage_manifest.json"),
        "stage_budget_lock": str(stage_root / "stage_budget_lock.json"),
        "stage_input_manifest": str(stage_root / "stage_input_manifest.json"),
        "comparison_arm_manifest": str(stage_root / "comparison_arm_manifest.json"),
        "target_policy_manifest": str(stage_root / "target_policy_manifest.json"),
        "stage_output_manifest": str(stage_root / "stage_output_manifest.json"),
        "stage_aggregate_summary": str(stage_root / "stage_aggregate_summary.json"),
        "stage_aggregate_table": str(stage_root / "stage_aggregate_table.csv"),
        "stage_run_index": str(stage_root / "stage_run_index.csv"),
        "readout_source": str(readout_source_path),
        **doc_paths,
    }
    return PairedReplicateComparisonResult(
        status=str(aggregate_row["status"]),
        stage_root=stage_root,
        readout_source_path=readout_source_path,
        artifact_paths=all_paths,
        claim_status=str(claim_row["claim_status"]),
        failure_reason=None,
    )


def _run_active_arms(
    *,
    config: PairedReplicateComparisonConfig,
    stage_root: Path,
    sources: Stage6Sources,
    target: dict[str, object],
    arms: tuple[ComparisonArm, ...],
    seed_bundles: tuple[PairedSeedBundle, ...],
    episodes_per_replicate: int,
) -> dict[str, Any]:
    started_at = _now()
    episode_rows: list[dict[str, object]] = []
    step_rows: list[dict[str, object]] = []
    controller_rows: list[dict[str, object]] = []
    learner_rows: list[dict[str, object]] = []
    lift_rows: list[dict[str, object]] = []
    tier_rows: list[dict[str, object]] = []
    timing_rows: list[dict[str, object]] = []
    run_index_rows: list[dict[str, object]] = []
    for arm in arms:
        if arm.status != "active":
            continue
        for bundle in seed_bundles:
            run_start = time.perf_counter()
            run_id = _run_id(config, arm, bundle)
            run_dir = stage_root / "runs" / run_id
            run_dir.mkdir(parents=True, exist_ok=True)
            if arm.arm_type == "direct_concrete_baseline":
                run = _run_direct_replicate(
                    config=config,
                    arm=arm,
                    bundle=bundle,
                    run_id=run_id,
                    target=target,
                    episodes_per_replicate=episodes_per_replicate,
                )
            else:
                run = _run_tower_replicate(
                    config=config,
                    arm=arm,
                    candidate=sources.selected_candidate,
                    bundle=bundle,
                    run_id=run_id,
                    target=target,
                    episodes_per_replicate=episodes_per_replicate,
                )
            episode_rows.extend(run["episode_rows"])
            step_rows.extend(run["step_rows"])
            controller_rows.extend(run["controller_rows"])
            learner_rows.extend(run["learner_rows"])
            lift_rows.extend(run["lift_rows"])
            tier_rows.extend(run["tier_rows"])
            timing_row = {
                "pair_id": bundle.pair_id,
                "arm_id": arm.arm_id,
                "arm_type": arm.arm_type,
                "candidate_id": arm.candidate_id,
                "schema_id": arm.schema_id,
                "run_id": run_id,
                "segment_name": "run_total",
                "duration_seconds": time.perf_counter() - run_start,
            }
            timing_rows.append(timing_row)
            required_file_count, present_file_count = _write_run_artifacts(
                run_dir=run_dir,
                config=config,
                arm=arm,
                bundle=bundle,
                run_id=run_id,
                episode_rows=run["episode_rows"],
                step_rows=run["step_rows"],
                controller_rows=run["controller_rows"],
                learner_rows=run["learner_rows"],
                lift_rows=run["lift_rows"],
                tier_rows=run["tier_rows"],
                timing_rows=[timing_row],
                target=target,
            )
            run_index_rows.append(
                {
                    "run_id": run_id,
                    "pair_id": bundle.pair_id,
                    "arm_id": arm.arm_id,
                    "arm_type": arm.arm_type,
                    "candidate_id": arm.candidate_id,
                    "schema_id": arm.schema_id,
                    "replicate_index": bundle.replicate_index,
                    "status": "complete",
                    "episode_count": len(run["episode_rows"]),
                    "target_hit_count": sum(
                        _truthy(row["target_hit"]) for row in run["episode_rows"]
                    ),
                    "artifact_root": str(run_dir),
                    "required_file_count": required_file_count,
                    "present_file_count": present_file_count,
                    "artifact_complete": "1"
                    if present_file_count == required_file_count
                    else "0",
                }
            )
    return {
        "started_at": started_at,
        "episode_rows": episode_rows,
        "step_rows": step_rows,
        "controller_rows": controller_rows,
        "learner_rows": learner_rows,
        "lift_rows": lift_rows,
        "tier_rows": tier_rows,
        "timing_rows": timing_rows,
        "run_index_rows": run_index_rows,
    }


def _run_direct_replicate(
    *,
    config: PairedReplicateComparisonConfig,
    arm: ComparisonArm,
    bundle: PairedSeedBundle,
    run_id: str,
    target: dict[str, object],
    episodes_per_replicate: int,
) -> dict[str, list[dict[str, object]]]:
    surface = import_plate_support_surface()
    runtime = surface.create_runtime(schema=None)
    q_table: dict[tuple[str, str], float] = {}
    rng = random.Random(bundle.exploration_seed)
    episode_rows: list[dict[str, object]] = []
    step_rows: list[dict[str, object]] = []
    controller_rows: list[dict[str, object]] = []
    learner_rows: list[dict[str, object]] = []
    for episode_index in range(episodes_per_replicate):
        episode = _run_direct_episode(
            config=config,
            surface=surface,
            runtime=runtime,
            arm=arm,
            bundle=bundle,
            run_id=run_id,
            episode_index=episode_index,
            target=target,
            q_table=q_table,
            rng=rng,
        )
        episode_rows.append(episode["episode_row"])
        step_rows.extend(episode["step_rows"])
        controller_rows.extend(episode["controller_rows"])
        learner_rows.extend(episode["learner_rows"])
    return {
        "episode_rows": episode_rows,
        "step_rows": step_rows,
        "controller_rows": controller_rows,
        "learner_rows": learner_rows,
        "lift_rows": [],
        "tier_rows": [],
    }


def _run_direct_episode(
    *,
    config: PairedReplicateComparisonConfig,
    surface: Any,
    runtime: Any,
    arm: ComparisonArm,
    bundle: PairedSeedBundle,
    run_id: str,
    episode_index: int,
    target: dict[str, object],
    q_table: dict[tuple[str, str], float],
    rng: random.Random,
) -> dict[str, object]:
    reset = runtime.reset(seed=bundle.episode_seed(episode_index))
    snapshot = reset.runtime_snapshot
    total_reward = 0.0
    step_count = 0
    goal_reached = False
    terminated = False
    truncated = False
    step_rows = []
    controller_rows = []
    learner_rows = []
    for step_index in range(config.max_steps_per_episode):
        source_state = snapshot.current_base_state
        state_key = state_payload_text(source_state)
        action_index, selection_mode = _choose_direct_action(
            surface=surface,
            state_key=state_key,
            q_table=q_table,
            rng=rng,
            epsilon=config.epsilon,
        )
        q_key = (state_key, str(action_index))
        q_value_before = q_table.get(q_key, 0.0)
        controller_rows.append(
            _controller_row(
                pair_id=bundle.pair_id,
                arm=arm,
                run_id=run_id,
                replicate_index=bundle.replicate_index,
                episode_index=episode_index,
                step_index=step_index,
                tier=0,
                state_cell_id=state_key,
                action_cell_id=f"action:{action_index}",
                action_index=action_index,
                selection_mode=selection_mode,
                q_value_before=q_value_before,
            )
        )
        step = runtime.step(action_index)
        next_snapshot = step.runtime_snapshot
        reward = float(step.reward)
        total_reward += reward
        step_count += 1
        terminated = bool(step.terminated)
        truncated = bool(step.truncated)
        info = step.info or {}
        goal_reached = goal_reached or bool(info.get("goal_reached", False))
        target_state = next_snapshot.current_base_state
        step_rows.append(
            _step_row(
                pair_id=bundle.pair_id,
                arm=arm,
                run_id=run_id,
                replicate_index=bundle.replicate_index,
                episode_index=episode_index,
                step_index=step_index,
                source_state=state_payload_text(source_state),
                action_index=action_index,
                target_state=state_payload_text(target_state),
                reward=reward,
                terminated=terminated,
                truncated=truncated,
                valid_transition=bool(info.get("valid_transition", True)),
                invalid_move=bool(info.get("invalid_move", False)),
                self_transition=state_payload_text(source_state)
                == state_payload_text(target_state),
                lift_status="not_applicable",
            )
        )
        next_key = state_payload_text(target_state)
        next_best = 0.0 if terminated or truncated else _direct_next_best(
            surface=surface,
            state_key=next_key,
            q_table=q_table,
        )
        td_error = reward + config.discount * next_best - q_value_before
        new_value = q_value_before + config.learning_rate * td_error
        q_table[q_key] = new_value
        learner_rows.append(
            _learner_row(
                pair_id=bundle.pair_id,
                arm=arm,
                run_id=run_id,
                replicate_index=bundle.replicate_index,
                episode_index=episode_index,
                step_index=step_index,
                learner_state_key=state_key,
                learner_action_key=str(action_index),
                reward=reward,
                next_state_best_value=next_best,
                td_error=td_error,
                old_value=q_value_before,
                new_value=new_value,
            )
        )
        snapshot = next_snapshot
        if terminated or truncated:
            break
    episode_row = _episode_row(
        pair_id=bundle.pair_id,
        arm=arm,
        run_id=run_id,
        replicate_index=bundle.replicate_index,
        episode_index=episode_index,
        episode_seed=bundle.episode_seed(episode_index),
        status="complete",
        step_count=step_count,
        total_reward=total_reward,
        terminated=terminated,
        truncated=truncated,
        goal_reached=goal_reached,
        blocked_reason="",
        target=target,
    )
    return {
        "episode_row": episode_row,
        "step_rows": step_rows,
        "controller_rows": controller_rows,
        "learner_rows": learner_rows,
    }


def _run_tower_replicate(
    *,
    config: PairedReplicateComparisonConfig,
    arm: ComparisonArm,
    candidate: TrainingCandidate,
    bundle: PairedSeedBundle,
    run_id: str,
    target: dict[str, object],
    episodes_per_replicate: int,
) -> dict[str, list[dict[str, object]]]:
    training_surface = build_training_surface(candidate)
    q_table: dict[tuple[str, str, str], float] = {}
    rng = random.Random(bundle.exploration_seed)
    episode_rows: list[dict[str, object]] = []
    step_rows: list[dict[str, object]] = []
    controller_rows: list[dict[str, object]] = []
    learner_rows: list[dict[str, object]] = []
    lift_rows: list[dict[str, object]] = []
    tier_rows: list[dict[str, object]] = []
    for episode_index in range(episodes_per_replicate):
        episode = _run_tower_episode(
            config=config,
            arm=arm,
            bundle=bundle,
            run_id=run_id,
            episode_index=episode_index,
            target=target,
            training_surface=training_surface,
            q_table=q_table,
            rng=rng,
        )
        episode_rows.append(episode["episode_row"])
        step_rows.extend(episode["step_rows"])
        controller_rows.extend(episode["controller_rows"])
        learner_rows.extend(episode["learner_rows"])
        lift_rows.extend(episode["lift_rows"])
        tier_rows.extend(episode["tier_rows"])
    return {
        "episode_rows": episode_rows,
        "step_rows": step_rows,
        "controller_rows": controller_rows,
        "learner_rows": learner_rows,
        "lift_rows": lift_rows,
        "tier_rows": tier_rows,
    }


def _run_tower_episode(
    *,
    config: PairedReplicateComparisonConfig,
    arm: ComparisonArm,
    bundle: PairedSeedBundle,
    run_id: str,
    episode_index: int,
    target: dict[str, object],
    training_surface: Any,
    q_table: dict[tuple[str, str, str], float],
    rng: random.Random,
) -> dict[str, object]:
    runtime = training_surface.runtime
    surface = training_surface.surface
    reset = runtime.reset(seed=bundle.episode_seed(episode_index))
    snapshot = reset.runtime_snapshot
    total_reward = 0.0
    step_count = 0
    blocked_reason = ""
    goal_reached = False
    terminated = False
    truncated = False
    step_rows = []
    controller_rows = []
    learner_rows = []
    lift_rows = []
    tier_rows = []
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
                _tier_row(
                    pair_id=bundle.pair_id,
                    arm=arm,
                    run_id=run_id,
                    replicate_index=bundle.replicate_index,
                    episode_index=episode_index,
                    step_index=step_index,
                    tier_before="",
                    tier_after="",
                    state_cell_before="",
                    state_cell_after="",
                    active_action_cell_count=0,
                    blocked_reason=blocked_reason,
                )
            )
            break
        source_state = snapshot.current_base_state
        q_value_before = q_table.get(choice.q_key, 0.0)
        controller_rows.append(
            _controller_row(
                pair_id=bundle.pair_id,
                arm=arm,
                run_id=run_id,
                replicate_index=bundle.replicate_index,
                episode_index=episode_index,
                step_index=step_index,
                tier=choice.tier,
                state_cell_id=cell_text(choice.state_cell_id),
                action_cell_id=cell_text(choice.action_cell_id),
                action_index=choice.action_index,
                selection_mode=selection_mode,
                q_value_before=q_value_before,
            )
        )
        lift_rows.append(
            _lift_row(
                pair_id=bundle.pair_id,
                arm=arm,
                run_id=run_id,
                replicate_index=bundle.replicate_index,
                episode_index=episode_index,
                step_index=step_index,
                tier=choice.tier,
                state_cell_id=cell_text(choice.state_cell_id),
                action_cell_id=cell_text(choice.action_cell_id),
                candidate_lift_count=choice.candidate_lift_count,
                executable_lift_count=choice.executable_lift_count,
                selected_lift_source=state_payload_text(choice.selected_edge.source),
                selected_lift_target=state_payload_text(choice.selected_edge.target),
                selected_action_index=choice.action_index,
                lift_status="success",
                failure_reason="",
            )
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
        step_rows.append(
            _step_row(
                pair_id=bundle.pair_id,
                arm=arm,
                run_id=run_id,
                replicate_index=bundle.replicate_index,
                episode_index=episode_index,
                step_index=step_index,
                source_state=state_payload_text(source_state),
                action_index=choice.action_index,
                target_state=state_payload_text(target_state),
                reward=reward,
                terminated=terminated,
                truncated=truncated,
                valid_transition=bool(info.get("valid_transition", True)),
                invalid_move=bool(info.get("invalid_move", False)),
                self_transition=state_payload_text(source_state)
                == state_payload_text(target_state),
                lift_status="success",
            )
        )
        tier_after = _tier_after(choice.tier, next_snapshot)
        tier_rows.append(
            _tier_row(
                pair_id=bundle.pair_id,
                arm=arm,
                run_id=run_id,
                replicate_index=bundle.replicate_index,
                episode_index=episode_index,
                step_index=step_index,
                tier_before=choice.tier,
                tier_after=choice.tier,
                state_cell_before=cell_text(choice.state_cell_id),
                state_cell_after=cell_text(tier_after),
                active_action_cell_count=choice.executable_lift_count,
                blocked_reason="",
            )
        )
        next_best = 0.0 if terminated or truncated else next_state_best_value(
            snapshot=next_snapshot,
            surface=surface,
            q_table=q_table,
        )
        td_error = reward + config.discount * next_best - q_value_before
        new_value = q_value_before + config.learning_rate * td_error
        q_table[choice.q_key] = new_value
        learner_rows.append(
            _learner_row(
                pair_id=bundle.pair_id,
                arm=arm,
                run_id=run_id,
                replicate_index=bundle.replicate_index,
                episode_index=episode_index,
                step_index=step_index,
                learner_state_key=choice.q_key[1],
                learner_action_key=choice.q_key[2],
                reward=reward,
                next_state_best_value=next_best,
                td_error=td_error,
                old_value=q_value_before,
                new_value=new_value,
            )
        )
        snapshot = next_snapshot
        if terminated or truncated:
            break
    episode_row = _episode_row(
        pair_id=bundle.pair_id,
        arm=arm,
        run_id=run_id,
        replicate_index=bundle.replicate_index,
        episode_index=episode_index,
        episode_seed=bundle.episode_seed(episode_index),
        status="complete" if not blocked_reason else "controller_blocked",
        step_count=step_count,
        total_reward=total_reward,
        terminated=terminated,
        truncated=truncated,
        goal_reached=goal_reached,
        blocked_reason=blocked_reason,
        target=target,
    )
    return {
        "episode_row": episode_row,
        "step_rows": step_rows,
        "controller_rows": controller_rows,
        "learner_rows": learner_rows,
        "lift_rows": lift_rows,
        "tier_rows": tier_rows,
    }


def _choose_direct_action(
    *,
    surface: Any,
    state_key: str,
    q_table: dict[tuple[str, str], float],
    rng: random.Random,
    epsilon: float,
) -> tuple[int, str]:
    actions = tuple(range(int(surface.ACTION_COUNT)))
    if rng.random() < epsilon:
        return rng.choice(actions), "epsilon_explore"
    return max(actions, key=lambda action: (q_table.get((state_key, str(action)), 0.0), -action)), (
        "greedy"
    )


def _direct_next_best(
    *,
    surface: Any,
    state_key: str,
    q_table: dict[tuple[str, str], float],
) -> float:
    return max(
        q_table.get((state_key, str(action)), 0.0)
        for action in range(int(surface.ACTION_COUNT))
    )


def _episode_row(
    *,
    pair_id: str,
    arm: ComparisonArm,
    run_id: str,
    replicate_index: int,
    episode_index: int,
    episode_seed: int,
    status: str,
    step_count: int,
    total_reward: float,
    terminated: bool,
    truncated: bool,
    goal_reached: bool,
    blocked_reason: str,
    target: dict[str, object],
) -> dict[str, object]:
    row = {
        "pair_id": pair_id,
        "arm_id": arm.arm_id,
        "arm_type": arm.arm_type,
        "candidate_id": arm.candidate_id,
        "schema_id": arm.schema_id,
        "run_id": run_id,
        "replicate_index": replicate_index,
        "episode_index": episode_index,
        "episode_seed": episode_seed,
        "status": status,
        "step_count": step_count,
        "total_reward": total_reward,
        "terminated": terminated,
        "truncated": truncated,
        "goal_reached": goal_reached,
        "blocked_reason": blocked_reason,
    }
    return {**row, "target_hit": target_hit(row, target)}


def _step_row(
    *,
    pair_id: str,
    arm: ComparisonArm,
    run_id: str,
    replicate_index: int,
    episode_index: int,
    step_index: int,
    source_state: str,
    action_index: int,
    target_state: str,
    reward: float,
    terminated: bool,
    truncated: bool,
    valid_transition: bool,
    invalid_move: bool,
    self_transition: bool,
    lift_status: str,
) -> dict[str, object]:
    return {
        "pair_id": pair_id,
        "arm_id": arm.arm_id,
        "arm_type": arm.arm_type,
        "candidate_id": arm.candidate_id,
        "schema_id": arm.schema_id,
        "run_id": run_id,
        "replicate_index": replicate_index,
        "episode_index": episode_index,
        "step_index": step_index,
        "source_state": source_state,
        "action_index": action_index,
        "target_state": target_state,
        "reward": reward,
        "terminated": terminated,
        "truncated": truncated,
        "valid_transition": valid_transition,
        "invalid_move": invalid_move,
        "self_transition": self_transition,
        "lift_status": lift_status,
    }


def _controller_row(
    *,
    pair_id: str,
    arm: ComparisonArm,
    run_id: str,
    replicate_index: int,
    episode_index: int,
    step_index: int,
    tier: int,
    state_cell_id: str,
    action_cell_id: str,
    action_index: int,
    selection_mode: str,
    q_value_before: float,
) -> dict[str, object]:
    return {
        "pair_id": pair_id,
        "arm_id": arm.arm_id,
        "arm_type": arm.arm_type,
        "candidate_id": arm.candidate_id,
        "schema_id": arm.schema_id,
        "run_id": run_id,
        "replicate_index": replicate_index,
        "episode_index": episode_index,
        "step_index": step_index,
        "tier": tier,
        "state_cell_id": state_cell_id,
        "action_cell_id": action_cell_id,
        "action_index": action_index,
        "selection_mode": selection_mode,
        "q_value_before": q_value_before,
    }


def _learner_row(
    *,
    pair_id: str,
    arm: ComparisonArm,
    run_id: str,
    replicate_index: int,
    episode_index: int,
    step_index: int,
    learner_state_key: str,
    learner_action_key: str,
    reward: float,
    next_state_best_value: float,
    td_error: float,
    old_value: float,
    new_value: float,
) -> dict[str, object]:
    return {
        "pair_id": pair_id,
        "arm_id": arm.arm_id,
        "arm_type": arm.arm_type,
        "candidate_id": arm.candidate_id,
        "schema_id": arm.schema_id,
        "run_id": run_id,
        "replicate_index": replicate_index,
        "episode_index": episode_index,
        "step_index": step_index,
        "learner_state_key": learner_state_key,
        "learner_action_key": learner_action_key,
        "reward": reward,
        "next_state_best_value": next_state_best_value,
        "td_error": td_error,
        "old_value": old_value,
        "new_value": new_value,
        "update_applied": True,
    }


def _lift_row(
    *,
    pair_id: str,
    arm: ComparisonArm,
    run_id: str,
    replicate_index: int,
    episode_index: int,
    step_index: int,
    tier: int,
    state_cell_id: str,
    action_cell_id: str,
    candidate_lift_count: int,
    executable_lift_count: int,
    selected_lift_source: str,
    selected_lift_target: str,
    selected_action_index: int,
    lift_status: str,
    failure_reason: str,
) -> dict[str, object]:
    return {
        "pair_id": pair_id,
        "arm_id": arm.arm_id,
        "arm_type": arm.arm_type,
        "candidate_id": arm.candidate_id,
        "schema_id": arm.schema_id,
        "run_id": run_id,
        "replicate_index": replicate_index,
        "episode_index": episode_index,
        "step_index": step_index,
        "tier": tier,
        "state_cell_id": state_cell_id,
        "action_cell_id": action_cell_id,
        "candidate_lift_count": candidate_lift_count,
        "executable_lift_count": executable_lift_count,
        "selected_lift_source": selected_lift_source,
        "selected_lift_target": selected_lift_target,
        "selected_action_index": selected_action_index,
        "lift_status": lift_status,
        "failure_reason": failure_reason,
    }


def _tier_row(
    *,
    pair_id: str,
    arm: ComparisonArm,
    run_id: str,
    replicate_index: int,
    episode_index: int,
    step_index: int,
    tier_before: object,
    tier_after: object,
    state_cell_before: object,
    state_cell_after: object,
    active_action_cell_count: int,
    blocked_reason: str,
) -> dict[str, object]:
    return {
        "pair_id": pair_id,
        "arm_id": arm.arm_id,
        "arm_type": arm.arm_type,
        "candidate_id": arm.candidate_id,
        "schema_id": arm.schema_id,
        "run_id": run_id,
        "replicate_index": replicate_index,
        "episode_index": episode_index,
        "step_index": step_index,
        "tier_before": tier_before,
        "tier_after": tier_after,
        "state_cell_before": state_cell_before,
        "state_cell_after": state_cell_after,
        "active_action_cell_count": active_action_cell_count,
        "blocked_reason": blocked_reason,
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
    config: PairedReplicateComparisonConfig,
    arm: ComparisonArm,
    bundle: PairedSeedBundle,
    run_id: str,
    episode_rows: list[dict[str, object]],
    step_rows: list[dict[str, object]],
    controller_rows: list[dict[str, object]],
    learner_rows: list[dict[str, object]],
    lift_rows: list[dict[str, object]],
    tier_rows: list[dict[str, object]],
    timing_rows: list[dict[str, object]],
    target: dict[str, object],
) -> tuple[int, int]:
    write_json(
        run_dir / "run_manifest.json",
        {
            "artifact_schema_version": ARTIFACT_SCHEMA_VERSION,
            "run_id": run_id,
            "pair_id": bundle.pair_id,
            "arm_id": arm.arm_id,
            "arm_type": arm.arm_type,
            "candidate_id": arm.candidate_id,
            "schema_id": arm.schema_id,
            "replicate_index": bundle.replicate_index,
            "target_policy_id": target.get("target_policy_id", ""),
            "max_steps_per_episode": config.max_steps_per_episode,
        },
        create_parents=True,
    )
    write_json(
        run_dir / "seed_bundle.json",
        {
            "artifact_schema_version": ARTIFACT_SCHEMA_VERSION,
            **bundle.to_row(),
            "run_id": run_id,
            "arm_id": arm.arm_id,
        },
        create_parents=True,
    )
    write_csv(run_dir / "episodes.csv", episode_rows, COMPARISON_EPISODE_FIELDS)
    write_csv(run_dir / "step_events.csv", step_rows, COMPARISON_STEP_FIELDS)
    write_csv(
        run_dir / "controller_action_events.csv",
        controller_rows,
        COMPARISON_CONTROLLER_FIELDS,
    )
    write_csv(run_dir / "learner_update_events.csv", learner_rows, COMPARISON_LEARNER_FIELDS)
    write_csv(run_dir / "lift_fiber_events.csv", lift_rows, COMPARISON_LIFT_FIELDS)
    write_csv(run_dir / "tier_transition_events.csv", tier_rows, COMPARISON_TIER_FIELDS)
    write_csv(run_dir / "timing_segments.csv", timing_rows, COMPARISON_TIMING_FIELDS)
    write_json(run_dir / "timing_summary.json", {"timing_segments": timing_rows})
    if arm.arm_type == "selected_tower_candidate":
        write_json(
            run_dir / "schema_manifest.json",
            {
                "artifact_schema_version": ARTIFACT_SCHEMA_VERSION,
                "schema_id": arm.schema_id,
                "schema_source": "stage3_selected_candidate",
            },
        )
    required = [
        "run_manifest.json",
        "seed_bundle.json",
        "episodes.csv",
        "step_events.csv",
        "controller_action_events.csv",
        "learner_update_events.csv",
        "lift_fiber_events.csv",
        "tier_transition_events.csv",
        "timing_segments.csv",
        "timing_summary.json",
    ]
    if arm.arm_type == "selected_tower_candidate":
        required.append("schema_manifest.json")
    present = sum((run_dir / name).exists() for name in required)
    return len(required), present


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
        if row.get("stage_id") != PAIRED_REPLICATE_COMPARISON_STAGE_ID
    ]
    stage_status_row = {field: aggregate_row[field] for field in STAGE_STATUS_FIELDS}
    write_csv(status_path, [*filtered, stage_status_row], STAGE_STATUS_FIELDS, create_parents=True)

    run_index_path = suite_root / "stage_run_index.csv"
    run_rows: list[dict[str, str]] = []
    if run_index_path.exists():
        with run_index_path.open(encoding="utf-8", newline="") as handle:
            run_rows = list(csv.DictReader(handle))
    run_rows = [
        row
        for row in run_rows
        if row.get("stage_id") != PAIRED_REPLICATE_COMPARISON_STAGE_ID
    ]
    run_rows.append(
        {
            "suite_id": SUITE_ID,
            "stage_id": PAIRED_REPLICATE_COMPARISON_STAGE_ID,
            "run_label": run_label,
            "artifact_root": str(artifact_root),
            "status": aggregate_row["status"],
        }
    )
    write_csv(
        run_index_path,
        run_rows,
        ("suite_id", "stage_id", "run_label", "artifact_root", "status"),
        create_parents=True,
    )


def _stage6_readout_source(
    *,
    readout_surface: Path,
    stage_root: Path,
    config: PairedReplicateComparisonConfig,
    output_paths: dict[str, str],
    target: dict[str, object],
    claim_row: dict[str, object],
) -> dict[str, object]:
    required = tuple(RESULT_TABLE_FIELDNAMES)
    return {
        "artifact_schema_version": ARTIFACT_SCHEMA_VERSION,
        "source_binding_type": "evaluation_readout_source",
        "repo_readout_surface": str(readout_surface),
        "source_artifact_root": str(stage_root),
        "source_evaluation_root": str(stage_root),
        "evaluation_id": PAIRED_REPLICATE_COMPARISON_STAGE_ID,
        "environment_family_id": ENVIRONMENT_FAMILY_ID,
        "environment_instance_id": ENVIRONMENT_INSTANCE_ID,
        "artifact_run_label": config.run_label,
        "run_mode": "stage6_paired_replicate_comparison",
        "calibrated_target": target,
        "comparison_claim": claim_row,
        "source_files": {key: output_paths[key] for key in required},
        "expected_files": {
            "required": [output_paths[key] for key in required],
            "expected_absent_is_gap": [],
            "conditional": {},
            "not_applicable": [],
            "expectation_sources": [
                "docs/design/first_plate_support_environment/standard_gauntlet_suite/"
                "06_paired_replicate_comparison/"
                "01_001_plate_support_paired_replicate_comparison_blueprint.md"
            ],
        },
        "goal_criteria": [
            {
                "goal_id": "plate_support_stage6_paired_comparison",
                "question": (
                    "Does the selected PlateSupport tower candidate show a bounded "
                    "paired signal against the direct baseline?"
                ),
                "success_signal": "comparison_claim_summary.csv has positive signal",
                "partial_signal": "paired tables complete but claim is inconclusive",
                "failure_signal": "no complete pairs or negative signal",
                "claim_if_met": "bounded smoke positive signal under this target",
                "claim_if_not_met": "no bounded positive signal under this target",
            }
        ],
        "claim_boundary": [
            "Stage 6 may claim only bounded paired smoke comparison signal",
            "Stage 6 may not claim broad tower superiority or environment-general benefit",
        ],
        "goal_summary_sources": [
            "docs/design/first_plate_support_environment/standard_gauntlet_suite/"
            "06_paired_replicate_comparison/"
            "01_001_plate_support_paired_replicate_comparison_blueprint.md",
            str(readout_surface / "method.md"),
        ],
        "methodology_summary_sources": [
            "docs/design/first_plate_support_environment/standard_gauntlet_suite/"
            "06_paired_replicate_comparison/"
            "01_001_plate_support_paired_replicate_comparison_blueprint.md",
            str(readout_surface / "method.md"),
            str(readout_surface / "runbook.md"),
        ],
    }


def _update_suite_readout_source(
    *,
    repo_root: Path,
    run_label: str,
    stage6_readout_source: Path,
    claim_row: dict[str, object],
) -> None:
    path = suite_readout_surface(repo_root) / "readout_source.json"
    payload: dict[str, object]
    if path.exists():
        with path.open(encoding="utf-8") as handle:
            loaded = json.load(handle)
        payload = loaded if isinstance(loaded, dict) else {}
    else:
        payload = {}
    stage_paths = [
        str(item)
        for item in payload.get("stage_readout_source_paths", [])
        if str(item) != str(stage6_readout_source)
    ]
    stage_paths.append(str(stage6_readout_source))
    payload.update(
        {
            "artifact_schema_version": ARTIFACT_SCHEMA_VERSION,
            "source_binding_type": "evaluation_readout_source",
            "repo_readout_surface": str(suite_readout_surface(repo_root)),
            "source_artifact_root": str(
                Path(suite_readout_surface(repo_root)) / "artifacts" / run_label
            ),
            "source_evaluation_root": str(suite_evaluation_root(repo_root, run_label, SUITE_ID)),
            "evaluation_id": SUITE_ID,
            "environment_family_id": ENVIRONMENT_FAMILY_ID,
            "environment_instance_id": ENVIRONMENT_INSTANCE_ID,
            "artifact_run_label": run_label,
            "run_mode": "smoke_stage_1_to_6_before_stage7_readout",
            "stage_readout_source_paths": stage_paths,
            "stage_definitions": [
                {
                    "stage_number": stage.stage_number,
                    "stage_id": stage.stage_id,
                    "short_name": stage.short_name,
                    "required_predecessor_stage_ids": list(stage.required_predecessor_stage_ids),
                }
                for stage in STAGE_DEFINITIONS
            ],
            "claim_boundary": [
                "Smoke-suite evidence currently supports PlateSupport standard-gauntlet "
                "progression through Stage 6",
                str(claim_row.get("bounded_claim", "")),
                "Stage 7 readout/system-learning synthesis has not yet run",
            ],
        }
    )
    source_eval_root = suite_evaluation_root(repo_root, run_label, SUITE_ID)
    payload["source_files"] = {
        "aggregate_table": str(source_eval_root / "stage_status_summary.csv"),
        "run_index": str(source_eval_root / "stage_run_index.csv"),
    }
    write_json(path, payload, create_parents=True)


def _write_blocked_result(
    *,
    config: PairedReplicateComparisonConfig,
    repo_root: Path,
    stage_root: Path,
    reason: str,
) -> PairedReplicateComparisonResult:
    readout_source_path = (
        suite_readout_surface(repo_root) / "paired_replicate_comparison" / "readout_source.json"
    )
    payload = {
        "artifact_schema_version": ARTIFACT_SCHEMA_VERSION,
        "suite_id": SUITE_ID,
        "stage_id": PAIRED_REPLICATE_COMPARISON_STAGE_ID,
        "status": "blocked",
        "claim_status": "protocol_blocked",
        "blocking_reason": reason,
        "run_label": config.run_label,
    }
    write_json(stage_root / "stage_aggregate_summary.json", payload, create_parents=True)
    return PairedReplicateComparisonResult(
        status="blocked",
        stage_root=stage_root,
        readout_source_path=readout_source_path,
        artifact_paths={
            "stage_aggregate_summary": str(stage_root / "stage_aggregate_summary.json")
        },
        claim_status="protocol_blocked",
        failure_reason=reason,
    )


def _candidate_arm_id(arms: tuple[ComparisonArm, ...]) -> str:
    for arm in arms:
        if arm.baseline_role == "candidate":
            return arm.arm_id
    raise ValueError("Stage 6 requires a selected tower candidate arm")


def _run_id(
    config: PairedReplicateComparisonConfig,
    arm: ComparisonArm,
    bundle: PairedSeedBundle,
) -> str:
    safe_arm = "".join(character if character.isalnum() else "-" for character in arm.arm_id)
    safe_arm = safe_arm.strip("-")
    return f"{config.run_label}-{bundle.pair_id}-{safe_arm}"


def _tier_after(tier: int, snapshot: object) -> object:
    positions = getattr(snapshot, "current_position_at_every_tier", ())
    if tier < len(positions):
        return positions[tier]
    return ""


def _select_fields(row: dict[str, object], fieldnames: tuple[str, ...]) -> dict[str, object]:
    return {field: row.get(field, "") for field in fieldnames}


def _truthy(value: object) -> bool:
    if isinstance(value, bool):
        return value
    return str(value).strip().lower() in {"1", "true", "yes", "y"}


def _now() -> str:
    return datetime.now(UTC).isoformat()
