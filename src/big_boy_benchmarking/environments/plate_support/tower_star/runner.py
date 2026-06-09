"""Runner for the PlateSupport tower-star guarded lift diagnostic."""

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
from big_boy_benchmarking.environments.plate_support.standard_gauntlet.paired_replicate_comparison.seed_bundles import (
    PairedSeedBundle,
    build_paired_seed_bundles,
)
from big_boy_benchmarking.environments.plate_support.standard_gauntlet.paired_replicate_comparison.target_policy import (
    target_hit,
)
from big_boy_benchmarking.environments.plate_support.standard_gauntlet.tower_training_health.training_surfaces import (
    build_training_surface,
    cell_text,
    state_payload_text,
)
from big_boy_benchmarking.environments.plate_support.upstream import (
    import_plate_support_surface,
)

from .aggregation import RESULT_TABLE_FIELDNAMES, build_tower_star_tables
from .config import (
    CLAIM_BOUNDARY,
    TOWER_STAR_GUARDED_LIFT_COMPARISON_EVALUATION_ID,
    ENVIRONMENT_FAMILY_ID,
    ENVIRONMENT_INSTANCE_ID,
    TowerStarGuardedLiftComparisonConfig,
)
from .docs_writer import write_tower_star_docs
from .events import (
    CONTROLLER_FIELDS,
    EPISODE_FIELDS,
    GUARD_EVENT_FIELDS,
    LEARNER_FIELDS,
    LIFT_FIELDS,
    STEP_FIELDS,
    TIER_FIELDS,
    TIMING_FIELDS,
)
from .guards import classify_primitive_transition, summarize_guard
from .manifests import TowerStarArm, build_tower_star_arms
from .parent_source import TowerStarParentSourceError, load_tower_star_parent_sources
from .paths import evaluation_root, repo_placeholder, repo_readout_surface, run_family_root
from .tower_lifts import (
    available_tower_star_action_choices,
    enumerate_tower_action_cell_surfaces,
    lift_surface_rows,
    next_state_best_tower_star_value,
)


@dataclass(frozen=True)
class TowerStarGuardedLiftComparisonResult:
    """Run result for the tower-star diagnostic."""

    status: str
    evaluation_root: Path
    readout_source_path: Path
    artifact_paths: dict[str, str]
    interpretation_case: str
    failure_reason: str | None = None


def run_tower_star(
    config: TowerStarGuardedLiftComparisonConfig,
) -> TowerStarGuardedLiftComparisonResult:
    """Run the tower-star diagnostic and write artifacts."""

    repo_root = Path(config.repo_root).expanduser().resolve()
    artifact_root = Path(config.artifact_root).expanduser().resolve()
    eval_root = evaluation_root(artifact_root)
    eval_root.mkdir(parents=True, exist_ok=True)
    try:
        parent = load_tower_star_parent_sources(
            parent_gauntlet_source=config.parent_gauntlet_source,
            direct_star_source=config.direct_star_source,
            repo_root=repo_root,
        )
    except TowerStarParentSourceError as exc:
        return _write_blocked_result(config, repo_root, eval_root, str(exc))

    episodes = config.resolved_episodes_per_replicate(parent.parent_episodes_per_replicate)
    replicates = config.resolved_replicates_per_arm(parent.parent_replicates_per_arm)
    arms = build_tower_star_arms(parent.selected_candidate)
    seed_bundles = build_paired_seed_bundles(
        base_seed=config.base_seed,
        replicate_count=replicates,
    )
    raw = _run_active_arms(
        config=config,
        repo_root=repo_root,
        artifact_root=artifact_root,
        arms=arms,
        parent=parent,
        seed_bundles=seed_bundles,
        episodes_per_replicate=episodes,
    )
    tables = build_tower_star_tables(
        arms=arms,
        seed_rows=[bundle.to_row() for bundle in seed_bundles],
        run_index_rows=raw["run_index_rows"],
        episode_rows=raw["episode_rows"],
        step_rows=raw["step_rows"],
        guard_rows=raw["guard_rows"],
        controller_rows=raw["controller_rows"],
        learner_rows=raw["learner_rows"],
        lift_rows=raw["lift_rows"],
        tier_rows=raw["tier_rows"],
        timing_rows=raw["timing_rows"],
    )
    if tables["interpretation_summary"]:
        tables["interpretation_summary"][0]["run_label"] = config.run_label
    output_paths = _write_result_tables(eval_root, tables)
    interpretation_row = tables["interpretation_summary"][0]
    all_paths = _write_manifests(
        config=config,
        repo_root=repo_root,
        artifact_root=artifact_root,
        eval_root=eval_root,
        parent=parent,
        arms=arms,
        episodes_per_replicate=episodes,
        replicates_per_arm=replicates,
        output_paths=output_paths,
        interpretation_row=interpretation_row,
        badge_rows=tables["badge_summary"],
    )
    return TowerStarGuardedLiftComparisonResult(
        status="complete",
        evaluation_root=eval_root,
        readout_source_path=repo_readout_surface(repo_root) / "readout_source.json",
        artifact_paths=all_paths,
        interpretation_case=str(interpretation_row["interpretation_case"]),
    )


def summarize_tower_star(
    *,
    repo_root: Path | str,
    artifact_root: Path | str,
) -> TowerStarGuardedLiftComparisonResult:
    """Regenerate docs from existing tower-star result tables."""

    root = Path(repo_root).expanduser().resolve()
    artifact = Path(artifact_root).expanduser().resolve()
    eval_root = evaluation_root(artifact)
    interpretation_rows = _read_csv(eval_root / "results" / "interpretation_summary.csv")
    badge_rows = _read_csv(eval_root / "results" / "badge_summary.csv")
    budget = _read_json(eval_root / "evaluation_budget_lock.json")
    target = _read_json(eval_root / "target_policy_manifest.json")["target"]
    if not interpretation_rows:
        return _write_blocked_result(
            TowerStarGuardedLiftComparisonConfig(
                repo_root=root,
                artifact_root=artifact,
                parent_gauntlet_source=Path(str(budget.get("parent_gauntlet_source", ""))),
                direct_star_source=Path(str(budget.get("direct_star_source", ""))),
                run_label=str(budget.get("run_label", "unknown")),
                locked_by=str(budget.get("locked_by", "unknown")),
            ),
            root,
            eval_root,
            "interpretation_summary.csv is empty",
        )
    output_paths = {
        table_name: str(eval_root / "results" / f"{table_name}.csv")
        for table_name in RESULT_TABLE_FIELDNAMES
        if (eval_root / "results" / f"{table_name}.csv").exists()
    }
    docs = write_tower_star_docs(
        repo_root=root,
        artifact_root=artifact,
        evaluation_root=eval_root,
        run_label=str(budget.get("run_label", "unknown")),
        output_paths=output_paths,
        target=target if isinstance(target, dict) else {},
        interpretation_row=interpretation_rows[0],
        badge_rows=badge_rows,
        parent_gauntlet_source=Path(str(budget.get("parent_gauntlet_source", ""))),
        direct_star_source=Path(str(budget.get("direct_star_source", ""))),
    )
    return TowerStarGuardedLiftComparisonResult(
        status="complete",
        evaluation_root=eval_root,
        readout_source_path=repo_readout_surface(root) / "readout_source.json",
        artifact_paths=docs,
        interpretation_case=str(interpretation_rows[0].get("interpretation_case", "")),
    )


def _run_active_arms(
    *,
    config: TowerStarGuardedLiftComparisonConfig,
    repo_root: Path,
    artifact_root: Path,
    arms: tuple[TowerStarArm, ...],
    parent: Any,
    seed_bundles: tuple[PairedSeedBundle, ...],
    episodes_per_replicate: int,
) -> dict[str, Any]:
    episode_rows: list[dict[str, object]] = []
    step_rows: list[dict[str, object]] = []
    guard_rows: list[dict[str, object]] = []
    controller_rows: list[dict[str, object]] = []
    learner_rows: list[dict[str, object]] = []
    lift_rows: list[dict[str, object]] = []
    tier_rows: list[dict[str, object]] = []
    timing_rows: list[dict[str, object]] = []
    run_index_rows: list[dict[str, object]] = []
    run_root = run_family_root(artifact_root)
    for arm in arms:
        for bundle in seed_bundles:
            started = time.perf_counter()
            run_id = _run_id(config.run_label, arm, bundle)
            run_dir = run_root / "runs" / run_id
            if arm.arm_type == "tower_candidate":
                run = _run_tower_replicate(
                    config=config,
                    arm=arm,
                    candidate=parent.selected_candidate,
                    bundle=bundle,
                    run_id=run_id,
                    target=parent.target,
                    episodes_per_replicate=episodes_per_replicate,
                )
            else:
                run = _run_direct_replicate(
                    config=config,
                    arm=arm,
                    bundle=bundle,
                    run_id=run_id,
                    target=parent.target,
                    episodes_per_replicate=episodes_per_replicate,
                )
            timing_row = {
                "pair_id": bundle.pair_id,
                "arm_id": arm.arm_id,
                "arm_type": arm.arm_type,
                "guard_type": arm.guard_type,
                "candidate_id": arm.candidate_id,
                "schema_id": arm.schema_id,
                "run_id": run_id,
                "segment_name": "run_total",
                "duration_seconds": time.perf_counter() - started,
            }
            timing_rows.append(timing_row)
            required, present = _write_run_artifacts(
                run_dir=run_dir,
                arm=arm,
                bundle=bundle,
                run_id=run_id,
                config=config,
                target=parent.target,
                episode_rows=run["episode_rows"],
                step_rows=run["step_rows"],
                guard_rows=run["guard_rows"],
                controller_rows=run["controller_rows"],
                learner_rows=run["learner_rows"],
                lift_rows=run["lift_rows"],
                tier_rows=run["tier_rows"],
                timing_rows=[timing_row],
            )
            episode_rows.extend(run["episode_rows"])
            step_rows.extend(run["step_rows"])
            guard_rows.extend(run["guard_rows"])
            controller_rows.extend(run["controller_rows"])
            learner_rows.extend(run["learner_rows"])
            lift_rows.extend(run["lift_rows"])
            tier_rows.extend(run["tier_rows"])
            run_index_rows.append(
                {
                    "run_id": run_id,
                    "pair_id": bundle.pair_id,
                    "arm_id": arm.arm_id,
                    "arm_type": arm.arm_type,
                    "guard_type": arm.guard_type,
                    "candidate_id": arm.candidate_id,
                    "schema_id": arm.schema_id,
                    "replicate_index": bundle.replicate_index,
                    "status": "complete",
                    "episode_count": len(run["episode_rows"]),
                    "target_hit_count": sum(
                        _truthy(row["target_hit"]) for row in run["episode_rows"]
                    ),
                    "artifact_root": repo_placeholder(run_dir, repo_root),
                    "required_file_count": required,
                    "present_file_count": present,
                    "artifact_complete": "1" if required == present else "0",
                }
            )
    return {
        "episode_rows": episode_rows,
        "step_rows": step_rows,
        "guard_rows": guard_rows,
        "controller_rows": controller_rows,
        "learner_rows": learner_rows,
        "lift_rows": lift_rows,
        "tier_rows": tier_rows,
        "timing_rows": timing_rows,
        "run_index_rows": run_index_rows,
    }


def _run_direct_replicate(
    *,
    config: TowerStarGuardedLiftComparisonConfig,
    arm: TowerStarArm,
    bundle: PairedSeedBundle,
    run_id: str,
    target: dict[str, object],
    episodes_per_replicate: int,
) -> dict[str, list[dict[str, object]]]:
    surface = import_plate_support_surface()
    runtime = surface.create_runtime(schema=None)
    q_table: dict[tuple[str, str], float] = {}
    rng = random.Random(bundle.exploration_seed)
    result = _empty_run()
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
        _extend_run(result, episode)
    return result


def _run_direct_episode(
    *,
    config: TowerStarGuardedLiftComparisonConfig,
    surface: Any,
    runtime: Any,
    arm: TowerStarArm,
    bundle: PairedSeedBundle,
    run_id: str,
    episode_index: int,
    target: dict[str, object],
    q_table: dict[tuple[str, str], float],
    rng: random.Random,
) -> dict[str, list[dict[str, object]]]:
    reset = runtime.reset(seed=bundle.episode_seed(episode_index))
    snapshot = reset.runtime_snapshot
    total_reward = 0.0
    step_count = 0
    goal_reached = False
    terminated = False
    truncated = False
    blocked_reason = ""
    result = _empty_episode()
    for step_index in range(config.max_steps_per_episode):
        source_state = snapshot.current_base_state
        state_key = state_payload_text(source_state)
        guard = summarize_guard(surface, source_state, arm.guard_type)
        if not guard.available_actions:
            blocked_reason = f"all_actions_filtered_by_{arm.guard_type}"
            result["guard_rows"].append(
                _guard_event_row(
                    arm=arm,
                    bundle=bundle,
                    run_id=run_id,
                    episode_index=episode_index,
                    step_index=step_index,
                    state_id=state_key,
                    guard_summary=guard,
                    guard_fallback_used=True,
                    chosen_action="",
                    classification=None,
                    next_state_id="",
                    reward=0.0,
                    done=True,
                )
            )
            break
        action_index, selection_mode = _choose_direct_action(
            available_actions=guard.available_actions,
            state_key=state_key,
            q_table=q_table,
            rng=rng,
            epsilon=config.epsilon,
        )
        classification = classify_primitive_transition(surface, source_state, action_index)
        q_key = (state_key, str(action_index))
        q_value_before = q_table.get(q_key, 0.0)
        result["controller_rows"].append(
            _controller_row(
                arm=arm,
                bundle=bundle,
                run_id=run_id,
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
        target_key = state_payload_text(target_state)
        result["guard_rows"].append(
            _guard_event_row(
                arm=arm,
                bundle=bundle,
                run_id=run_id,
                episode_index=episode_index,
                step_index=step_index,
                state_id=state_key,
                guard_summary=guard,
                guard_fallback_used=False,
                chosen_action=action_index,
                classification=classification,
                next_state_id=target_key,
                reward=reward,
                done=terminated or truncated,
            )
        )
        result["step_rows"].append(
            _step_row(
                arm=arm,
                bundle=bundle,
                run_id=run_id,
                episode_index=episode_index,
                step_index=step_index,
                source_state=state_key,
                action_index=action_index,
                target_state=target_key,
                reward=reward,
                terminated=terminated,
                truncated=truncated,
                valid_transition=bool(info.get("valid_transition", True)),
                invalid_move=bool(info.get("invalid_move", False)),
                self_transition=state_key == target_key,
                valid_clipped_self_transition=state_key == target_key
                and not bool(info.get("invalid_move", False)),
                lift_status="not_applicable",
            )
        )
        next_best = (
            0.0
            if terminated or truncated
            else _direct_next_best(surface, target_state, arm.guard_type, q_table)
        )
        td_error = reward + config.discount * next_best - q_value_before
        new_value = q_value_before + config.learning_rate * td_error
        q_table[q_key] = new_value
        result["learner_rows"].append(
            _learner_row(
                arm=arm,
                bundle=bundle,
                run_id=run_id,
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
    result["episode_rows"].append(
        _episode_row(
            arm=arm,
            bundle=bundle,
            run_id=run_id,
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
    )
    return result


def _run_tower_replicate(
    *,
    config: TowerStarGuardedLiftComparisonConfig,
    arm: TowerStarArm,
    candidate: Any,
    bundle: PairedSeedBundle,
    run_id: str,
    target: dict[str, object],
    episodes_per_replicate: int,
) -> dict[str, list[dict[str, object]]]:
    training_surface = build_training_surface(candidate)
    q_table: dict[tuple[str, str, str], float] = {}
    rng = random.Random(bundle.exploration_seed)
    result = _empty_run()
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
        _extend_run(result, episode)
    return result


def _run_tower_episode(
    *,
    config: TowerStarGuardedLiftComparisonConfig,
    arm: TowerStarArm,
    bundle: PairedSeedBundle,
    run_id: str,
    episode_index: int,
    target: dict[str, object],
    training_surface: Any,
    q_table: dict[tuple[str, str, str], float],
    rng: random.Random,
) -> dict[str, list[dict[str, object]]]:
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
    result = _empty_episode()
    for step_index in range(config.max_steps_per_episode):
        source_state = snapshot.current_base_state
        state_key = state_payload_text(source_state)
        surfaces = enumerate_tower_action_cell_surfaces(
            snapshot=snapshot,
            surface=surface,
        )
        choices = available_tower_star_action_choices(
            snapshot=snapshot,
            surface=surface,
            q_table=q_table,
            guard_type=arm.guard_type,
        )
        if not choices:
            blocked_reason = "no_executable_tower_action"
            result["lift_rows"].extend(
                lift_surface_rows(
                    arm=arm,
                    bundle=bundle,
                    run_id=run_id,
                    episode_index=episode_index,
                    step_index=step_index,
                    surfaces=surfaces,
                    selected_choice=None,
                )
            )
            result["guard_rows"].append(
                _tower_guard_event_row(
                    arm=arm,
                    bundle=bundle,
                    run_id=run_id,
                    episode_index=episode_index,
                    step_index=step_index,
                    state_id=state_key,
                    available_count_before=len(surfaces),
                    available_count_after=0,
                    invalid_filtered_count=_removed_by_invalid_star(surfaces),
                    self_loop_filtered_count=_removed_by_nonself_star(surfaces),
                    chosen_action="",
                    classification=None,
                    next_state_id="",
                    reward=0.0,
                    done=True,
                    fallback=True,
                )
            )
            result["tier_rows"].append(
                _tier_row(
                    arm=arm,
                    bundle=bundle,
                    run_id=run_id,
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
        deepest_tier = max(choice.tier for choice in choices)
        tier_choices = [choice for choice in choices if choice.tier == deepest_tier]
        tier_surfaces = [
            action_surface for action_surface in surfaces if action_surface.tier == deepest_tier
        ]
        if rng.random() < config.epsilon:
            choice = rng.choice(tier_choices)
            selection_mode = "epsilon_explore"
        else:
            choice = max(
                tier_choices,
                key=lambda item: (item.q_value, repr(item.action_cell_id), -item.action_index),
            )
            selection_mode = "greedy"
        classification = classify_primitive_transition(surface, source_state, choice.action_index)
        q_value_before = q_table.get(choice.q_key, 0.0)
        result["controller_rows"].append(
            _controller_row(
                arm=arm,
                bundle=bundle,
                run_id=run_id,
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
        result["lift_rows"].extend(
            lift_surface_rows(
                arm=arm,
                bundle=bundle,
                run_id=run_id,
                episode_index=episode_index,
                step_index=step_index,
                surfaces=surfaces,
                selected_choice=choice,
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
        target_key = state_payload_text(target_state)
        result["guard_rows"].append(
            _tower_guard_event_row(
                arm=arm,
                bundle=bundle,
                run_id=run_id,
                episode_index=episode_index,
                step_index=step_index,
                state_id=state_key,
                available_count_before=len(tier_surfaces),
                available_count_after=len(tier_choices),
                invalid_filtered_count=_removed_by_invalid_star(tier_surfaces),
                self_loop_filtered_count=_removed_by_nonself_star(tier_surfaces),
                chosen_action=choice.action_index,
                classification=classification,
                next_state_id=target_key,
                reward=reward,
                done=terminated or truncated,
                fallback=False,
            )
        )
        result["step_rows"].append(
            _step_row(
                arm=arm,
                bundle=bundle,
                run_id=run_id,
                episode_index=episode_index,
                step_index=step_index,
                source_state=state_key,
                action_index=choice.action_index,
                target_state=target_key,
                reward=reward,
                terminated=terminated,
                truncated=truncated,
                valid_transition=bool(info.get("valid_transition", True)),
                invalid_move=bool(info.get("invalid_move", False)),
                self_transition=state_key == target_key,
                valid_clipped_self_transition=state_key == target_key
                and not bool(info.get("invalid_move", False)),
                lift_status="success",
            )
        )
        result["tier_rows"].append(
            _tier_row(
                arm=arm,
                bundle=bundle,
                run_id=run_id,
                episode_index=episode_index,
                step_index=step_index,
                tier_before=choice.tier,
                tier_after=choice.tier,
                state_cell_before=cell_text(choice.state_cell_id),
                state_cell_after=cell_text(_tier_after(choice.tier, next_snapshot)),
                active_action_cell_count=len(tier_choices),
                blocked_reason="",
            )
        )
        next_best = (
            0.0
            if terminated or truncated
            else next_state_best_tower_star_value(
                snapshot=next_snapshot,
                surface=surface,
                q_table=q_table,
                guard_type=arm.guard_type,
            )
        )
        td_error = reward + config.discount * next_best - q_value_before
        new_value = q_value_before + config.learning_rate * td_error
        q_table[choice.q_key] = new_value
        result["learner_rows"].append(
            _learner_row(
                arm=arm,
                bundle=bundle,
                run_id=run_id,
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
    result["episode_rows"].append(
        _episode_row(
            arm=arm,
            bundle=bundle,
            run_id=run_id,
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
    )
    return result


def _choose_direct_action(
    *,
    available_actions: tuple[int, ...],
    state_key: str,
    q_table: dict[tuple[str, str], float],
    rng: random.Random,
    epsilon: float,
) -> tuple[int, str]:
    if rng.random() < epsilon:
        return rng.choice(available_actions), "epsilon_explore"
    return max(
        available_actions,
        key=lambda action: (q_table.get((state_key, str(action)), 0.0), -action),
    ), "greedy"


def _direct_next_best(
    surface: Any,
    state: Any,
    guard_type: str,
    q_table: dict[tuple[str, str], float],
) -> float:
    state_key = state_payload_text(state)
    actions = summarize_guard(surface, state, guard_type).available_actions
    if not actions:
        return 0.0
    return max(q_table.get((state_key, str(action)), 0.0) for action in actions)


def _write_result_tables(
    eval_root: Path,
    tables: dict[str, list[dict[str, object]]],
) -> dict[str, str]:
    output_paths: dict[str, str] = {}
    results_dir = eval_root / "results"
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


def _write_manifests(
    *,
    config: TowerStarGuardedLiftComparisonConfig,
    repo_root: Path,
    artifact_root: Path,
    eval_root: Path,
    parent: Any,
    arms: tuple[TowerStarArm, ...],
    episodes_per_replicate: int,
    replicates_per_arm: int,
    output_paths: dict[str, str],
    interpretation_row: dict[str, object],
    badge_rows: list[dict[str, object]],
) -> dict[str, str]:
    write_json(
        eval_root / "evaluation_manifest.json",
        {
            "artifact_schema_version": ARTIFACT_SCHEMA_VERSION,
            "evaluation_id": TOWER_STAR_GUARDED_LIFT_COMPARISON_EVALUATION_ID,
            "environment_family_id": ENVIRONMENT_FAMILY_ID,
            "environment_instance_id": ENVIRONMENT_INSTANCE_ID,
            "run_label": config.run_label,
            "status": "complete",
            "claim_boundary": CLAIM_BOUNDARY,
        },
        create_parents=True,
    )
    write_json(
        eval_root / "evaluation_budget_lock.json",
        {
            "artifact_schema_version": ARTIFACT_SCHEMA_VERSION,
            "evaluation_id": TOWER_STAR_GUARDED_LIFT_COMPARISON_EVALUATION_ID,
            "run_label": config.run_label,
            "locked_by": config.locked_by,
            "parent_gauntlet_source": str(Path(config.parent_gauntlet_source)),
            "direct_star_source": str(Path(config.direct_star_source)),
            "selected_candidate_id": parent.selected_candidate.candidate_id,
            "selected_schema_id": parent.selected_candidate.schema_id,
            "episodes_per_replicate": episodes_per_replicate,
            "replicates_per_arm": replicates_per_arm,
            "max_steps_per_episode": config.max_steps_per_episode,
            "base_seed": config.base_seed,
            "learning_rate": config.learning_rate,
            "discount": config.discount,
            "epsilon": config.epsilon,
            "guard_information_mode": "oracle_one_step_local_transition",
            "information_parity_warning_required": True,
        },
        create_parents=True,
    )
    write_json(
        eval_root / "parent_source_manifest.json",
        {
            "parent_suite_source": repo_placeholder(parent.suite_source_path, repo_root),
            "direct_star_source": repo_placeholder(parent.direct_star_source_path, repo_root),
            "stage3_source": repo_placeholder(parent.stage3.path, repo_root),
            "stage4_source": repo_placeholder(parent.stage4.path, repo_root),
            "stage5_source": repo_placeholder(parent.stage5.path, repo_root),
            "stage6_source": repo_placeholder(parent.stage6.path, repo_root),
        },
        create_parents=True,
    )
    write_json(
        eval_root / "evaluation_arm_manifest.json",
        {"arms": [arm.to_row() for arm in arms]},
        create_parents=True,
    )
    write_json(eval_root / "target_policy_manifest.json", {"target": parent.target})
    write_json(eval_root / "dependency_manifest.json", _public_dependency_state(parent.dependency_state))
    write_json(
        eval_root / "evaluation_aggregate_summary.json",
        {
            "status": "complete",
            "interpretation_case": interpretation_row["interpretation_case"],
            "claim_boundary": CLAIM_BOUNDARY,
        },
    )
    write_csv(
        eval_root / "evaluation_aggregate_table.csv",
        [
            {
                "evaluation_id": TOWER_STAR_GUARDED_LIFT_COMPARISON_EVALUATION_ID,
                "status": "complete",
                "run_label": config.run_label,
                "interpretation_case": interpretation_row["interpretation_case"],
                "claim_boundary": CLAIM_BOUNDARY,
            }
        ],
        ("evaluation_id", "status", "run_label", "interpretation_case", "claim_boundary"),
    )
    docs = write_tower_star_docs(
        repo_root=repo_root,
        artifact_root=artifact_root,
        evaluation_root=eval_root,
        run_label=config.run_label,
        output_paths=output_paths,
        target=parent.target,
        interpretation_row=interpretation_row,
        badge_rows=badge_rows,
        parent_gauntlet_source=Path(config.parent_gauntlet_source),
        direct_star_source=Path(config.direct_star_source),
    )
    return {
        **output_paths,
        "evaluation_manifest": str(eval_root / "evaluation_manifest.json"),
        "evaluation_budget_lock": str(eval_root / "evaluation_budget_lock.json"),
        "parent_source_manifest": str(eval_root / "parent_source_manifest.json"),
        "evaluation_arm_manifest_json": str(eval_root / "evaluation_arm_manifest.json"),
        "target_policy_manifest": str(eval_root / "target_policy_manifest.json"),
        "dependency_manifest": str(eval_root / "dependency_manifest.json"),
        "evaluation_aggregate_summary": str(eval_root / "evaluation_aggregate_summary.json"),
        "evaluation_aggregate_table": str(eval_root / "evaluation_aggregate_table.csv"),
        **docs,
    }


def _write_run_artifacts(
    *,
    run_dir: Path,
    arm: TowerStarArm,
    bundle: PairedSeedBundle,
    run_id: str,
    config: TowerStarGuardedLiftComparisonConfig,
    target: dict[str, object],
    episode_rows: list[dict[str, object]],
    step_rows: list[dict[str, object]],
    guard_rows: list[dict[str, object]],
    controller_rows: list[dict[str, object]],
    learner_rows: list[dict[str, object]],
    lift_rows: list[dict[str, object]],
    tier_rows: list[dict[str, object]],
    timing_rows: list[dict[str, object]],
) -> tuple[int, int]:
    write_json(
        run_dir / "run_manifest.json",
        {
            "artifact_schema_version": ARTIFACT_SCHEMA_VERSION,
            "run_id": run_id,
            "pair_id": bundle.pair_id,
            "arm_id": arm.arm_id,
            "arm_type": arm.arm_type,
            "guard_type": arm.guard_type,
            "candidate_id": arm.candidate_id,
            "schema_id": arm.schema_id,
            "target_policy_id": target.get("target_policy_id", ""),
            "max_steps_per_episode": config.max_steps_per_episode,
            "information_mode": arm.information_mode,
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
    write_csv(run_dir / "episodes.csv", episode_rows, EPISODE_FIELDS)
    write_csv(run_dir / "step_events.csv", step_rows, STEP_FIELDS)
    write_csv(run_dir / "guard_events.csv", guard_rows, GUARD_EVENT_FIELDS)
    write_csv(run_dir / "controller_action_events.csv", controller_rows, CONTROLLER_FIELDS)
    write_csv(run_dir / "learner_update_events.csv", learner_rows, LEARNER_FIELDS)
    write_csv(run_dir / "lift_fiber_events.csv", lift_rows, LIFT_FIELDS)
    write_csv(run_dir / "tier_transition_events.csv", tier_rows, TIER_FIELDS)
    write_csv(run_dir / "timing_segments.csv", timing_rows, TIMING_FIELDS)
    write_json(run_dir / "timing_summary.json", {"timing_segments": timing_rows})
    if arm.arm_type == "tower_candidate":
        write_json(
            run_dir / "schema_manifest.json",
            {"schema_id": arm.schema_id, "schema_source": "parent_selected_candidate"},
        )
    required = [
        "run_manifest.json",
        "seed_bundle.json",
        "episodes.csv",
        "step_events.csv",
        "guard_events.csv",
        "controller_action_events.csv",
        "learner_update_events.csv",
        "lift_fiber_events.csv",
        "tier_transition_events.csv",
        "timing_segments.csv",
        "timing_summary.json",
    ]
    if arm.arm_type == "tower_candidate":
        required.append("schema_manifest.json")
    present = sum((run_dir / name).exists() for name in required)
    return len(required), present


def _public_dependency_state(dependency_state: dict[str, object]) -> dict[str, object]:
    public_state = dict(dependency_state)
    if public_state.get("source_path"):
        public_state["source_path"] = "<local-python-environment>/state_collapser"
        public_state["source_path_note"] = (
            "Local dependency provenance path redacted for repo/public hygiene."
        )
    return public_state


def _episode_row(
    *,
    arm: TowerStarArm,
    bundle: PairedSeedBundle,
    run_id: str,
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
        "pair_id": bundle.pair_id,
        "arm_id": arm.arm_id,
        "arm_type": arm.arm_type,
        "guard_type": arm.guard_type,
        "candidate_id": arm.candidate_id,
        "schema_id": arm.schema_id,
        "run_id": run_id,
        "replicate_index": bundle.replicate_index,
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
    arm: TowerStarArm,
    bundle: PairedSeedBundle,
    run_id: str,
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
    valid_clipped_self_transition: bool,
    lift_status: str,
) -> dict[str, object]:
    return {
        "pair_id": bundle.pair_id,
        "arm_id": arm.arm_id,
        "arm_type": arm.arm_type,
        "guard_type": arm.guard_type,
        "candidate_id": arm.candidate_id,
        "schema_id": arm.schema_id,
        "run_id": run_id,
        "replicate_index": bundle.replicate_index,
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
        "valid_clipped_self_transition": valid_clipped_self_transition,
        "lift_status": lift_status,
    }


def _guard_event_row(
    *,
    arm: TowerStarArm,
    bundle: PairedSeedBundle,
    run_id: str,
    episode_index: int,
    step_index: int,
    state_id: str,
    guard_summary: Any,
    guard_fallback_used: bool,
    chosen_action: object,
    classification: Any | None,
    next_state_id: str,
    reward: float,
    done: bool,
) -> dict[str, object]:
    return {
        "run_id": run_id,
        "pair_id": bundle.pair_id,
        "episode_index": episode_index,
        "replicate_index": bundle.replicate_index,
        "step_index": step_index,
        "arm_id": arm.arm_id,
        "arm_type": arm.arm_type,
        "guard_type": arm.guard_type,
        "state_id": state_id,
        "available_action_count_before_guard": guard_summary.available_action_count_before_guard,
        "available_action_count_after_guard": guard_summary.available_action_count_after_guard,
        "guarded_action_count": guard_summary.guarded_action_count,
        "invalid_guard_filtered_count": guard_summary.invalid_guard_filtered_count,
        "self_loop_guard_filtered_count": guard_summary.self_loop_guard_filtered_count,
        "all_actions_filtered_count": guard_summary.all_actions_filtered_count,
        "guard_fallback_used": guard_fallback_used,
        "chosen_action": chosen_action,
        "chosen_action_would_have_been_invalid": (
            "" if classification is None else classification.invalid_move
        ),
        "chosen_action_would_have_been_self_loop": (
            "" if classification is None else classification.self_loop
        ),
        "chosen_action_transition_was_invalid": (
            "" if classification is None else classification.invalid_move
        ),
        "chosen_action_transition_was_self_loop": (
            "" if classification is None else classification.self_loop
        ),
        "chosen_action_transition_was_valid_clipped_self_loop": (
            "" if classification is None else classification.valid_clipped_self_loop
        ),
        "next_state_id": next_state_id,
        "reward": reward,
        "done": done,
        "information_mode": arm.information_mode,
    }


def _tower_guard_event_row(
    *,
    arm: TowerStarArm,
    bundle: PairedSeedBundle,
    run_id: str,
    episode_index: int,
    step_index: int,
    state_id: str,
    available_count_before: int,
    available_count_after: int,
    invalid_filtered_count: int,
    self_loop_filtered_count: int,
    chosen_action: object,
    classification: Any | None,
    next_state_id: str,
    reward: float,
    done: bool,
    fallback: bool,
) -> dict[str, object]:
    return {
        "run_id": run_id,
        "pair_id": bundle.pair_id,
        "episode_index": episode_index,
        "replicate_index": bundle.replicate_index,
        "step_index": step_index,
        "arm_id": arm.arm_id,
        "arm_type": arm.arm_type,
        "guard_type": arm.guard_type,
        "state_id": state_id,
        "available_action_count_before_guard": available_count_before,
        "available_action_count_after_guard": available_count_after,
        "guarded_action_count": available_count_after,
        "invalid_guard_filtered_count": invalid_filtered_count,
        "self_loop_guard_filtered_count": self_loop_filtered_count,
        "all_actions_filtered_count": 1 if fallback else 0,
        "guard_fallback_used": fallback,
        "chosen_action": chosen_action,
        "chosen_action_would_have_been_invalid": (
            "" if classification is None else classification.invalid_move
        ),
        "chosen_action_would_have_been_self_loop": (
            "" if classification is None else classification.self_loop
        ),
        "chosen_action_transition_was_invalid": (
            "" if classification is None else classification.invalid_move
        ),
        "chosen_action_transition_was_self_loop": (
            "" if classification is None else classification.self_loop
        ),
        "chosen_action_transition_was_valid_clipped_self_loop": (
            "" if classification is None else classification.valid_clipped_self_loop
        ),
        "next_state_id": next_state_id,
        "reward": reward,
        "done": done,
        "information_mode": arm.information_mode,
    }


def _removed_by_invalid_star(surfaces: list[Any]) -> int:
    return sum(
        1
        for action_surface in surfaces
        if action_surface.executable_lift_count > 0
        and len(action_surface.invalid_guard_lifts) == 0
    )


def _removed_by_nonself_star(surfaces: list[Any]) -> int:
    return sum(
        1
        for action_surface in surfaces
        if action_surface.executable_lift_count > 0
        and len(action_surface.nonself_guard_lifts) == 0
    )


def _controller_row(
    *,
    arm: TowerStarArm,
    bundle: PairedSeedBundle,
    run_id: str,
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
        "pair_id": bundle.pair_id,
        "arm_id": arm.arm_id,
        "arm_type": arm.arm_type,
        "guard_type": arm.guard_type,
        "candidate_id": arm.candidate_id,
        "schema_id": arm.schema_id,
        "run_id": run_id,
        "replicate_index": bundle.replicate_index,
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
    arm: TowerStarArm,
    bundle: PairedSeedBundle,
    run_id: str,
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
        "pair_id": bundle.pair_id,
        "arm_id": arm.arm_id,
        "arm_type": arm.arm_type,
        "guard_type": arm.guard_type,
        "candidate_id": arm.candidate_id,
        "schema_id": arm.schema_id,
        "run_id": run_id,
        "replicate_index": bundle.replicate_index,
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
    arm: TowerStarArm,
    bundle: PairedSeedBundle,
    run_id: str,
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
        "pair_id": bundle.pair_id,
        "arm_id": arm.arm_id,
        "arm_type": arm.arm_type,
        "guard_type": arm.guard_type,
        "candidate_id": arm.candidate_id,
        "schema_id": arm.schema_id,
        "run_id": run_id,
        "replicate_index": bundle.replicate_index,
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
    arm: TowerStarArm,
    bundle: PairedSeedBundle,
    run_id: str,
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
        "pair_id": bundle.pair_id,
        "arm_id": arm.arm_id,
        "arm_type": arm.arm_type,
        "guard_type": arm.guard_type,
        "candidate_id": arm.candidate_id,
        "schema_id": arm.schema_id,
        "run_id": run_id,
        "replicate_index": bundle.replicate_index,
        "episode_index": episode_index,
        "step_index": step_index,
        "tier_before": tier_before,
        "tier_after": tier_after,
        "state_cell_before": state_cell_before,
        "state_cell_after": state_cell_after,
        "active_action_cell_count": active_action_cell_count,
        "blocked_reason": blocked_reason,
    }


def _empty_run() -> dict[str, list[dict[str, object]]]:
    return {
        "episode_rows": [],
        "step_rows": [],
        "guard_rows": [],
        "controller_rows": [],
        "learner_rows": [],
        "lift_rows": [],
        "tier_rows": [],
    }


def _empty_episode() -> dict[str, list[dict[str, object]]]:
    return _empty_run()


def _extend_run(
    target: dict[str, list[dict[str, object]]],
    source: dict[str, list[dict[str, object]]],
) -> None:
    for key in target:
        target[key].extend(source[key])


def _tier_after(tier: int, snapshot: object) -> object:
    positions = getattr(snapshot, "current_position_at_every_tier", ())
    if tier < len(positions):
        return positions[tier]
    return ""


def _select_fields(row: dict[str, object], fieldnames: tuple[str, ...]) -> dict[str, object]:
    return {field: row.get(field, "") for field in fieldnames}


def _run_id(run_label: str, arm: TowerStarArm, bundle: PairedSeedBundle) -> str:
    safe_arm = "".join(character if character.isalnum() else "-" for character in arm.arm_id)
    return f"{run_label}-{bundle.pair_id}-{safe_arm.strip('-')}"


def _write_blocked_result(
    config: TowerStarGuardedLiftComparisonConfig,
    repo_root: Path,
    eval_root: Path,
    reason: str,
) -> TowerStarGuardedLiftComparisonResult:
    readout_source_path = repo_readout_surface(repo_root) / "readout_source.json"
    payload = {
        "artifact_schema_version": ARTIFACT_SCHEMA_VERSION,
        "evaluation_id": TOWER_STAR_GUARDED_LIFT_COMPARISON_EVALUATION_ID,
        "status": "blocked",
        "blocking_reason": reason,
        "run_label": config.run_label,
    }
    write_json(eval_root / "evaluation_aggregate_summary.json", payload, create_parents=True)
    return TowerStarGuardedLiftComparisonResult(
        status="blocked",
        evaluation_root=eval_root,
        readout_source_path=readout_source_path,
        artifact_paths={"evaluation_aggregate_summary": str(eval_root / "evaluation_aggregate_summary.json")},
        interpretation_case="blocked",
        failure_reason=reason,
    )


def _read_json(path: Path) -> dict[str, object]:
    with path.open(encoding="utf-8") as handle:
        payload = json.load(handle)
    return payload if isinstance(payload, dict) else {}


def _read_csv(path: Path) -> list[dict[str, str]]:
    with path.open(encoding="utf-8", newline="") as handle:
        return list(csv.DictReader(handle))


def _truthy(value: object) -> bool:
    if isinstance(value, bool):
        return value
    return str(value).strip().lower() in {"1", "true", "yes", "y"}
