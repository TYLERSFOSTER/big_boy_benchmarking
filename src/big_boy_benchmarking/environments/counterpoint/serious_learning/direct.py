"""Direct serious-learning runners for counterpoint symbolic v001."""

from __future__ import annotations

import random
from dataclasses import dataclass
from datetime import UTC, datetime
from pathlib import Path
from typing import Any

from state_collapser.core.rewards import PathRewardSummary
from state_collapser.graph.explored_graph import ExploredGraph
from state_collapser.graph.vista_graph import VistaGraph
from state_collapser.tower.snapshot import LiveRuntimeView
from state_collapser.training import (
    ActionSelectionInput,
    TabularQLearner,
    TrainingTransition,
)

from big_boy_benchmarking.artifacts.manifests import (
    DependencyManifest,
    EnvironmentFamilyManifest,
    ExternalArtifactsManifest,
    FamilyManifest,
    LinearizationManifest,
    ModeManifest,
    RunManifest,
)
from big_boy_benchmarking.artifacts.paths import build_run_family_paths, build_run_paths
from big_boy_benchmarking.artifacts.schemas import ARTIFACT_SCHEMA_VERSION
from big_boy_benchmarking.artifacts.writers import (
    append_csv_row,
    append_jsonl,
    ensure_artifact_dirs,
    write_csv,
    write_json,
)
from big_boy_benchmarking.environments.counterpoint import ids
from big_boy_benchmarking.environments.counterpoint.actions import (
    CounterpointAction,
    enumerate_raw_actions,
)
from big_boy_benchmarking.environments.counterpoint.artifacts import (
    action_mask_manifest,
    edge_label_manifest,
    environment_instance_manifest,
    legality_manifest,
    reward_bundle_manifest,
)
from big_boy_benchmarking.environments.counterpoint.instances import initial_states
from big_boy_benchmarking.environments.counterpoint.masks import legal_action_mask
from big_boy_benchmarking.environments.counterpoint.serious_learning.arms import (
    DIRECT_MASKED_RANDOM_ARM_ID,
    DIRECT_TABULAR_Q_ARM_ID,
    get_serious_learning_arm,
)
from big_boy_benchmarking.environments.counterpoint.serious_learning.config import (
    TabularQLearnerConfig,
)
from big_boy_benchmarking.environments.counterpoint.serious_learning.events import (
    SeriousEpisodeRow,
    SeriousStepRow,
)
from big_boy_benchmarking.environments.counterpoint.specs import CounterpointInstanceSpec
from big_boy_benchmarking.environments.counterpoint.state import CounterpointState
from big_boy_benchmarking.environments.counterpoint.tower_adapter import CounterpointHiddenGraph
from big_boy_benchmarking.environments.counterpoint.transition import evaluate_transition
from big_boy_benchmarking.metrics.timing import TimingRecorder, summarize_timing_segments
from big_boy_benchmarking.modes.registry import require_runnable_mode
from big_boy_benchmarking.runners.base import BenchmarkRunResult
from big_boy_benchmarking.seeds.bundles import SeedBundle
from big_boy_benchmarking.upstream.linearization import (
    REPORT_SOURCE,
    build_linearization_artifact_payload,
)
from big_boy_benchmarking.upstream.state_collapser import (
    STATE_COLLAPSER_DEPENDENCY_SPEC,
    collect_state_collapser_dependency_state,
)

SERIOUS_DIRECT_RUN_FAMILY_ID = "counterpoint_symbolic_v001_first_serious_learning_direct_v001"
SERIOUS_EVALUATION_ID = "counterpoint_first_serious_learning_v001"


@dataclass(frozen=True)
class DirectRuntimeContext:
    spec: CounterpointInstanceSpec
    raw_actions: tuple[CounterpointAction, ...]
    hidden_graph: CounterpointHiddenGraph


@dataclass(frozen=True)
class DirectStepTrace:
    episode_index: int
    step_index: int
    source_state: CounterpointState
    action_id: int
    action: CounterpointAction
    reward: float
    target_state: CounterpointState
    terminated: bool
    truncated: bool


@dataclass(frozen=True)
class DirectEpisodeTrace:
    episode_index: int
    seed_bundle_id: str
    replicate_index: int
    total_reward: float
    steps: tuple[DirectStepTrace, ...]
    terminated: bool
    truncated: bool


def _now() -> str:
    return datetime.now(UTC).isoformat()


def build_direct_runtime_context(spec: CounterpointInstanceSpec) -> DirectRuntimeContext:
    return DirectRuntimeContext(
        spec=spec,
        raw_actions=enumerate_raw_actions(spec),
        hidden_graph=CounterpointHiddenGraph(spec),
    )


def direct_state_key(action_input: ActionSelectionInput) -> tuple[object | None, ...]:
    state = action_input.current_base_state
    if not isinstance(state, CounterpointState):
        return ("counterpoint_state", repr(state))
    return ("counterpoint_state", state.pitches, state.beat_index)


def action_id_to_counterpoint_action(
    context: DirectRuntimeContext,
    action_id: int,
) -> CounterpointAction:
    try:
        return context.raw_actions[action_id]
    except IndexError as exc:
        raise ValueError(f"unknown counterpoint action id: {action_id}") from exc


def counterpoint_action_to_action_id(
    context: DirectRuntimeContext,
    action: CounterpointAction,
) -> int:
    try:
        return context.raw_actions.index(action)
    except ValueError as exc:
        raise ValueError(f"action is not in raw action vocabulary: {action}") from exc


def build_direct_action_selection_input(
    context: DirectRuntimeContext,
    state: CounterpointState,
    *,
    diagnostics: dict[str, object] | None = None,
) -> ActionSelectionInput:
    mask = legal_action_mask(context.spec, state)
    explored_graph = ExploredGraph()
    vista_graph = VistaGraph(context.hidden_graph, explored_graph)
    runtime_snapshot = LiveRuntimeView(
        current_base_state=state,
        explored_graph=explored_graph,
        vista_graph=vista_graph,
        ordered_quotient_tiers=(),
        current_position_at_every_tier=(),
        current_step_reward=None,
        cumulative_path_reward=PathRewardSummary(),
        quotient_tier_reward_summaries=(),
        active_control_tier=None,
        last_control_action=None,
        partition_tower_view=None,
        tower_update_result=None,
    )
    return ActionSelectionInput(
        observation=state,
        current_base_state=state,
        runtime_snapshot=runtime_snapshot,
        tower_position_key=(),
        action_mask=mask.mask,
        diagnostics={} if diagnostics is None else diagnostics,
    )


def build_direct_training_transition(
    *,
    source_input: ActionSelectionInput,
    chosen_action: int,
    reward: float,
    target_input: ActionSelectionInput,
    terminated: bool,
    truncated: bool,
    diagnostics: dict[str, object] | None = None,
) -> TrainingTransition:
    bootstrap_allowed = not terminated and not truncated
    return TrainingTransition(
        source_input=source_input,
        chosen_action=chosen_action,
        reward=reward,
        target_input=target_input,
        terminated=terminated,
        truncated=truncated,
        bootstrap_allowed=bootstrap_allowed,
        diagnostics={} if diagnostics is None else diagnostics,
        bootstrap_input=target_input,
        bootstrap_reason="target_available" if bootstrap_allowed else "terminal_or_truncated",
        tower_position_key=target_input.tower_position_key,
        active_tier=None,
    )


def _choose_start_state(
    spec: CounterpointInstanceSpec,
    rng: random.Random,
) -> CounterpointState:
    starts = initial_states(spec)
    if not starts:
        raise ValueError("initial state policy produced no legal start states")
    return rng.choice(starts)


def _run_masked_random_episode(
    context: DirectRuntimeContext,
    *,
    seed_bundle: SeedBundle,
    episode_index: int,
    horizon: int,
    recorder: TimingRecorder,
) -> DirectEpisodeTrace:
    rng = random.Random(
        f"{seed_bundle.environment_seed}:{seed_bundle.learner_seed}:{episode_index}"
    )
    with recorder.segment("environment_reset"):
        state = _choose_start_state(context.spec, rng)
    steps: list[DirectStepTrace] = []
    total_reward = 0.0
    terminated = False
    truncated = False
    for step_index in range(horizon):
        source_state = state
        with recorder.segment("learner_act"):
            mask = legal_action_mask(context.spec, state)
            legal_action_ids = [
                action_id for action_id, is_legal in enumerate(mask.mask) if is_legal
            ]
            if not legal_action_ids:
                truncated = True
                break
            action_id = rng.choice(legal_action_ids)
            action = action_id_to_counterpoint_action(context, action_id)
        with recorder.segment("environment_step"):
            transition = evaluate_transition(
                context.spec,
                state,
                action,
                step_index=step_index,
            )
        reward = 0.0 if transition.reward is None else transition.reward.total_reward
        total_reward += reward
        state = transition.next_state
        terminated = transition.terminated
        truncated = transition.truncated
        steps.append(
            DirectStepTrace(
                episode_index=episode_index,
                step_index=step_index,
                source_state=source_state,
                action_id=action_id,
                action=action,
                reward=reward,
                target_state=state,
                terminated=terminated,
                truncated=truncated,
            )
        )
        if terminated or truncated:
            break
    return DirectEpisodeTrace(
        episode_index=episode_index,
        seed_bundle_id=seed_bundle.seed_bundle_id,
        replicate_index=seed_bundle.replicate_index,
        total_reward=total_reward,
        steps=tuple(steps),
        terminated=terminated,
        truncated=truncated,
    )


def _run_upstream_tabular_episode(
    context: DirectRuntimeContext,
    *,
    learner: TabularQLearner,
    seed_bundle: SeedBundle,
    episode_index: int,
    horizon: int,
    recorder: TimingRecorder,
) -> DirectEpisodeTrace:
    rng = random.Random(
        f"{seed_bundle.environment_seed}:{seed_bundle.learner_seed}:{episode_index}"
    )
    with recorder.segment("environment_reset"):
        state = _choose_start_state(context.spec, rng)
    steps: list[DirectStepTrace] = []
    total_reward = 0.0
    terminated = False
    truncated = False
    for step_index in range(horizon):
        source_state = state
        source_input = build_direct_action_selection_input(context, source_state)
        with recorder.segment("learner_act"):
            decision = learner.act(source_input, mode="train")
        action_id = int(decision.chosen_action)
        action = action_id_to_counterpoint_action(context, action_id)
        with recorder.segment("environment_step"):
            transition = evaluate_transition(
                context.spec,
                source_state,
                action,
                step_index=step_index,
            )
        reward = 0.0 if transition.reward is None else transition.reward.total_reward
        target_input = build_direct_action_selection_input(context, transition.next_state)
        upstream_transition = build_direct_training_transition(
            source_input=source_input,
            chosen_action=action_id,
            reward=reward,
            target_input=target_input,
            terminated=transition.terminated,
            truncated=transition.truncated,
            diagnostics={"counterpoint_action": action.deltas},
        )
        learner.observe(upstream_transition)
        with recorder.segment("learner_update"):
            learner.update()
        total_reward += reward
        state = transition.next_state
        terminated = transition.terminated
        truncated = transition.truncated
        steps.append(
            DirectStepTrace(
                episode_index=episode_index,
                step_index=step_index,
                source_state=source_state,
                action_id=action_id,
                action=action,
                reward=reward,
                target_state=state,
                terminated=terminated,
                truncated=truncated,
            )
        )
        if terminated or truncated:
            break
    return DirectEpisodeTrace(
        episode_index=episode_index,
        seed_bundle_id=seed_bundle.seed_bundle_id,
        replicate_index=seed_bundle.replicate_index,
        total_reward=total_reward,
        steps=tuple(steps),
        terminated=terminated,
        truncated=truncated,
    )


def run_serious_direct_masked_random(
    *,
    spec: CounterpointInstanceSpec,
    seed_bundle: SeedBundle,
    artifact_root: Path | str,
    horizon: int | None = None,
    episode_count: int = 1,
    linearization_mode_id: str = "tensor_available_disabled",
    run_family_id: str = SERIOUS_DIRECT_RUN_FAMILY_ID,
    run_id: str | None = None,
) -> BenchmarkRunResult:
    context = build_direct_runtime_context(spec)
    active_horizon = spec.horizon_steps if horizon is None else horizon
    _validate_direct_budget(active_horizon, episode_count)
    arm = get_serious_learning_arm(DIRECT_MASKED_RANDOM_ARM_ID)
    run_id = run_id or _direct_run_id(spec.environment_instance_id, arm.arm_id, seed_bundle)
    recorder = TimingRecorder.create(run_id)
    episodes = tuple(
        _run_masked_random_episode(
            context,
            seed_bundle=seed_bundle,
            episode_index=episode_index,
            horizon=active_horizon,
            recorder=recorder,
        )
        for episode_index in range(episode_count)
    )
    return _write_direct_serious_artifacts(
        spec=spec,
        artifact_root=artifact_root,
        run_family_id=run_family_id,
        run_id=run_id,
        arm_id=arm.arm_id,
        mode_id=arm.mode_id,
        linearization_mode_id=linearization_mode_id,
        learner_id=arm.learner_id,
        seed_bundle=seed_bundle,
        budget={"episodes": episode_count, "horizon": active_horizon},
        recorder=recorder,
        episodes=episodes,
        command="python -m big_boy_benchmarking.cli counterpoint serious-learning run",
        max_action_count=len(context.raw_actions),
    )


def run_serious_direct_tabular_q(
    *,
    spec: CounterpointInstanceSpec,
    seed_bundle: SeedBundle,
    artifact_root: Path | str,
    learner_config: TabularQLearnerConfig | None = None,
    horizon: int | None = None,
    episode_count: int = 1,
    linearization_mode_id: str = "tensor_available_disabled",
    run_family_id: str = SERIOUS_DIRECT_RUN_FAMILY_ID,
    run_id: str | None = None,
) -> BenchmarkRunResult:
    context = build_direct_runtime_context(spec)
    active_horizon = spec.horizon_steps if horizon is None else horizon
    _validate_direct_budget(active_horizon, episode_count)
    arm = get_serious_learning_arm(DIRECT_TABULAR_Q_ARM_ID)
    config = TabularQLearnerConfig() if learner_config is None else learner_config
    learner = TabularQLearner(
        action_count=len(context.raw_actions),
        alpha=config.alpha,
        gamma=config.gamma,
        epsilon=config.epsilon,
        seed=seed_bundle.learner_seed,
        key_fn=direct_state_key,
    )
    run_id = run_id or _direct_run_id(spec.environment_instance_id, arm.arm_id, seed_bundle)
    recorder = TimingRecorder.create(run_id)
    episodes = tuple(
        _run_upstream_tabular_episode(
            context,
            learner=learner,
            seed_bundle=seed_bundle,
            episode_index=episode_index,
            horizon=active_horizon,
            recorder=recorder,
        )
        for episode_index in range(episode_count)
    )
    return _write_direct_serious_artifacts(
        spec=spec,
        artifact_root=artifact_root,
        run_family_id=run_family_id,
        run_id=run_id,
        arm_id=arm.arm_id,
        mode_id=arm.mode_id,
        linearization_mode_id=linearization_mode_id,
        learner_id=arm.learner_id,
        seed_bundle=seed_bundle,
        budget={
            "episodes": episode_count,
            "horizon": active_horizon,
            "learner_config": config.to_dict(),
            "upstream_learner": "state_collapser.training.TabularQLearner",
        },
        recorder=recorder,
        episodes=episodes,
        command="python -m big_boy_benchmarking.cli counterpoint serious-learning run",
        max_action_count=len(context.raw_actions),
    )


def _validate_direct_budget(horizon: int, episode_count: int) -> None:
    if horizon <= 0:
        raise ValueError("horizon must be positive")
    if episode_count <= 0:
        raise ValueError("episode_count must be positive")


def _direct_run_id(
    environment_instance_id: str,
    arm_id: str,
    seed_bundle: SeedBundle,
) -> str:
    return f"{environment_instance_id}-{arm_id}-rep{seed_bundle.replicate_index}"


def _state_repr(state: CounterpointState) -> str:
    return f"beat{state.beat_index}:pitches{state.pitches}"


def _artifact_path_dict(run_paths: Any) -> dict[str, str]:
    return {
        "run_manifest": str(run_paths.run_manifest),
        "seed_bundle": str(run_paths.seed_bundle),
        "mode_manifest": str(run_paths.mode_manifest),
        "linearization_manifest": str(run_paths.linearization_manifest),
        "timing_summary": str(run_paths.timing_summary),
        "episodes_csv": str(run_paths.episodes_csv),
        "step_events_csv": str(run_paths.step_events_csv),
        "timing_segments_csv": str(run_paths.timing_segments_csv),
        "external_artifacts": str(run_paths.external_artifacts),
    }


def _write_direct_serious_artifacts(
    *,
    spec: CounterpointInstanceSpec,
    artifact_root: Path | str,
    run_family_id: str,
    run_id: str,
    arm_id: str,
    mode_id: str,
    linearization_mode_id: str,
    learner_id: str,
    seed_bundle: SeedBundle,
    budget: dict[str, Any],
    recorder: TimingRecorder,
    episodes: tuple[DirectEpisodeTrace, ...],
    command: str,
    max_action_count: int,
) -> BenchmarkRunResult:
    started_at = _now()
    family_paths = build_run_family_paths(artifact_root, run_family_id)
    run_paths = build_run_paths(artifact_root, run_family_id, run_id)
    ensure_artifact_dirs(family_paths, run_paths)
    mode_contract = require_runnable_mode(mode_id)
    dependency_state = collect_state_collapser_dependency_state(
        dependency_spec=STATE_COLLAPSER_DEPENDENCY_SPEC,
    )
    linearization_payload = build_linearization_artifact_payload(
        linearization_mode_id=linearization_mode_id,
        recorder=recorder,
        max_action_count=max_action_count,
        metadata={
            "runner": "counterpoint_serious_direct",
            "evaluation_id": SERIOUS_EVALUATION_ID,
            "environment_instance_id": spec.environment_instance_id,
            "arm_id": arm_id,
            "mode_id": mode_id,
        },
    )

    write_json(
        family_paths.family_manifest,
        FamilyManifest(
            run_family_id=run_family_id,
            description="Counterpoint symbolic first serious learning direct family.",
        ).to_dict(),
        create_parents=True,
    )
    write_json(
        family_paths.environment_family_manifest,
        EnvironmentFamilyManifest(
            environment_family_id=ids.ENVIRONMENT_FAMILY_ID,
            environment_ids=(spec.environment_instance_id,),
            description="Counterpoint hidden graph benchmark family.",
        ).to_dict(),
        create_parents=True,
    )
    write_json(
        family_paths.dependency_manifest,
        DependencyManifest(
            state_collapser=dependency_state.to_dict(),
            repo_state={"bbb_repo": "/Users/foster/big_boy_benchmarking"},
        ).to_dict(),
        create_parents=True,
    )
    write_json(run_paths.seed_bundle, seed_bundle.to_dict(), create_parents=True)
    write_json(
        run_paths.linearization_manifest,
        LinearizationManifest(
            run_id=run_id,
            linearization_mode_id=linearization_mode_id,
            linearization_config=linearization_payload.config_dict,
            linearization_report=linearization_payload.report_dict,
            report_source=REPORT_SOURCE,
            conversion_records_exported=False,
        ).to_dict(),
        create_parents=True,
    )
    write_json(
        run_paths.external_artifacts,
        ExternalArtifactsManifest(
            run_id=run_id,
            artifacts=(
                {
                    "artifact_id": "counterpoint_environment_instance_manifest",
                    "kind": "environment_contract",
                },
            ),
        ).to_dict(),
        create_parents=True,
    )
    write_json(
        run_paths.root / "environment_instance_manifest.json",
        environment_instance_manifest(spec),
        create_parents=True,
    )
    write_json(run_paths.root / "legality_manifest.json", legality_manifest(spec))
    write_json(run_paths.root / "reward_bundle_manifest.json", reward_bundle_manifest(spec))
    write_json(run_paths.root / "edge_label_manifest.json", edge_label_manifest(spec))
    write_json(run_paths.root / "action_mask_manifest.json", action_mask_manifest(spec))

    for episode in episodes:
        append_csv_row(
            run_paths.episodes_csv,
            SeriousEpisodeRow(
                evaluation_id=SERIOUS_EVALUATION_ID,
                run_id=run_id,
                arm_id=arm_id,
                mode_id=mode_id,
                schema_id=None,
                schema_seed=None,
                seed_bundle_id=seed_bundle.seed_bundle_id,
                replicate_index=seed_bundle.replicate_index,
                episode_index=episode.episode_index,
                total_reward=episode.total_reward,
                step_count=len(episode.steps),
                terminated=episode.terminated,
                truncated=episode.truncated,
                success=episode.terminated and not episode.truncated,
                final_state=_state_repr(episode.steps[-1].target_state)
                if episode.steps
                else "",
            ).to_flat_dict(),
            SeriousEpisodeRow.fieldnames(),
            create_parents=True,
        )
        for step in episode.steps:
            append_csv_row(
                run_paths.step_events_csv,
                SeriousStepRow(
                    evaluation_id=SERIOUS_EVALUATION_ID,
                    run_id=run_id,
                    arm_id=arm_id,
                    episode_index=episode.episode_index,
                    step_index=step.step_index,
                    source_state=_state_repr(step.source_state),
                    action_id=step.action_id,
                    action_repr=str(step.action.deltas),
                    reward=step.reward,
                    target_state=_state_repr(step.target_state),
                    terminated=step.terminated,
                    truncated=step.truncated,
                ).to_flat_dict(),
                SeriousStepRow.fieldnames(),
                create_parents=True,
            )

    write_csv(
        run_paths.timing_segments_csv,
        [row.to_flat_dict() for row in recorder.rows],
        recorder.rows[0].fieldnames() if recorder.rows else (),
        create_parents=True,
    )
    write_json(
        run_paths.timing_summary,
        summarize_timing_segments(recorder.rows),
        create_parents=True,
    )
    write_json(
        run_paths.mode_manifest,
        ModeManifest(
            mode_id=mode_id,
            readout_requested=False,
            morphism_requested=False,
            uses_compatibility_readout=False,
            uses_morphism=False,
            mode_contract=mode_contract.to_dict(),
            linearization_mode_contract=linearization_payload.contract.to_dict(),
        ).to_dict(),
        create_parents=True,
    )
    ended_at = _now()
    write_json(
        run_paths.run_manifest,
        RunManifest(
            run_id=run_id,
            run_family_id=run_family_id,
            environment_id=spec.environment_instance_id,
            mode_id=mode_id,
            linearization_mode_id=linearization_mode_id,
            linearization_benchmark_label=linearization_payload.report.benchmark_label,
            linearization_enabled=linearization_payload.report.enabled,
            schema_id="none",
            learner_id=learner_id,
            controller_id=mode_contract.controller_regime,
            seed_bundle_id=seed_bundle.seed_bundle_id,
            budget=budget,
            diagnostic_profile=mode_contract.diagnostic_profile.profile_id,
            timing_profile=mode_contract.timing_profile.profile_id,
            command=command,
            status="success",
        ).to_dict(),
        create_parents=True,
    )
    append_jsonl(
        family_paths.run_index,
        {
            "run_family_id": run_family_id,
            "run_id": run_id,
            "environment_id": spec.environment_instance_id,
            "arm_id": arm_id,
            "mode_id": mode_id,
            "status": "success",
            "started_at": started_at,
            "ended_at": ended_at,
            "artifact_schema_version": ARTIFACT_SCHEMA_VERSION,
        },
        create_parents=True,
    )
    run_paths.warnings_jsonl.touch()
    mean_return = (
        sum(episode.total_reward for episode in episodes) / len(episodes) if episodes else 0.0
    )
    summary = {
        "evaluation_id": SERIOUS_EVALUATION_ID,
        "run_family_id": run_family_id,
        "run_id": run_id,
        "environment_instance_id": spec.environment_instance_id,
        "arm_id": arm_id,
        "mode_id": mode_id,
        "linearization_mode_id": linearization_mode_id,
        "linearization_benchmark_label": linearization_payload.report.benchmark_label,
        "learner_id": learner_id,
        "episode_count": len(episodes),
        "mean_return": mean_return,
        "uses_compatibility_readout": False,
        "uses_morphism": False,
        "artifact_schema_version": ARTIFACT_SCHEMA_VERSION,
    }
    write_json(family_paths.summary_json, summary, create_parents=True)
    return BenchmarkRunResult(
        run_id=run_id,
        status="success",
        artifact_paths=_artifact_path_dict(run_paths),
        summary_path=str(family_paths.summary_json),
        warning_count=0,
        started_at=started_at,
        ended_at=ended_at,
        failure_reason=None,
    )
