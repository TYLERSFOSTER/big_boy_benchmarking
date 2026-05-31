"""Active-tier tower-control binding for serious counterpoint learning."""

from __future__ import annotations

import random
from collections.abc import Callable
from dataclasses import dataclass, replace
from datetime import UTC, datetime
from pathlib import Path
from typing import Any

from state_collapser.tower.control import (
    ActiveTierController,
    ActiveTierState,
    ActiveTierTransition,
    ControllerDecision,
    FrozenLowerContext,
    TierControlConfig,
    TierSignalState,
)
from state_collapser.tower.control import (
    LearnerUpdateSummary as ControlLearnerUpdateSummary,
)
from state_collapser.tower.runtime import ExploitExploreTowerRuntime
from state_collapser.training import ActionSelectionInput, TabularQLearner, TrainingTransition

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
from big_boy_benchmarking.environments.counterpoint.actions import CounterpointAction
from big_boy_benchmarking.environments.counterpoint.artifacts import environment_instance_manifest
from big_boy_benchmarking.environments.counterpoint.instances import initial_states
from big_boy_benchmarking.environments.counterpoint.masks import legal_action_mask
from big_boy_benchmarking.environments.counterpoint.schemas import build_schema_for_id
from big_boy_benchmarking.environments.counterpoint.serious_learning.arms import (
    get_serious_learning_arm,
)
from big_boy_benchmarking.environments.counterpoint.serious_learning.config import (
    ExploitExploreControllerConfig,
    TabularQLearnerConfig,
)
from big_boy_benchmarking.environments.counterpoint.serious_learning.direct import (
    SERIOUS_EVALUATION_ID,
    _state_repr,
)
from big_boy_benchmarking.environments.counterpoint.serious_learning.events import (
    ControllerEventRow,
    LiftFiberEventRow,
    SeriousEpisodeRow,
    SeriousStepRow,
)
from big_boy_benchmarking.environments.counterpoint.specs import CounterpointInstanceSpec
from big_boy_benchmarking.environments.counterpoint.state import CounterpointState
from big_boy_benchmarking.environments.counterpoint.tower_adapter import (
    CounterpointTowerBuildResult,
    build_counterpoint_partition_tower,
    counterpoint_state_to_core_state,
    primitive_action_to_counterpoint_action,
)
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

SERIOUS_TOWER_RUN_FAMILY_ID = "counterpoint_symbolic_v001_first_serious_learning_tower_v001"


@dataclass(frozen=True)
class LiftResolveTrace:
    active_tier: int | None
    abstract_action: str
    realized_action: str | None
    candidate_count: int
    success: bool
    failure_reason: str | None
    fiber_departure_reason: str | None = None


@dataclass(frozen=True)
class TowerControlStepTrace:
    episode_index: int
    step_index: int
    source_state: CounterpointState
    action_id: int | None
    action: CounterpointAction | None
    reward: float
    target_state: CounterpointState
    terminated: bool
    truncated: bool
    active_tier_before: int | None
    active_tier_after: int | None


@dataclass(frozen=True)
class TowerControlEpisodeTrace:
    episode_index: int
    seed_bundle_id: str
    replicate_index: int
    total_reward: float
    steps: tuple[TowerControlStepTrace, ...]
    controller_rows: tuple[ControllerEventRow, ...]
    lift_rows: tuple[LiftFiberEventRow, ...]
    terminated: bool
    truncated: bool


class CounterpointTowerControlAdapter:
    """Mutable episode-local adapter between counterpoint and active-tier control."""

    def __init__(
        self,
        *,
        spec: CounterpointInstanceSpec,
        schema_id: str,
        schema_seed: int | None,
        recorder: TimingRecorder | None = None,
    ) -> None:
        self.spec = spec
        self.schema_id = schema_id
        self.schema_seed = schema_seed
        if recorder is None:
            self.build = build_counterpoint_partition_tower(
                spec,
                schema_id=schema_id,
                schema_seed=schema_seed,
            )
        else:
            with recorder.segment("tower_reset"):
                self.build = build_counterpoint_partition_tower(
                    spec,
                    schema_id=schema_id,
                    schema_seed=schema_seed,
                )
        self.current_state: CounterpointState | None = None
        self.current_core_state = None
        self.step_index = 0
        self.terminated = False
        self.truncated = False
        self.last_transition_reward = 0.0
        self.last_lift_trace: LiftResolveTrace | None = None

    @property
    def tower_depth(self) -> int:
        return len(self.build.tower.state_layers)

    @property
    def deepest_known_tier(self) -> int:
        return max(0, self.tower_depth - 1)

    def reset(self, *, seed_bundle: SeedBundle, episode_index: int) -> ActiveTierState:
        rng = random.Random(
            f"{seed_bundle.environment_seed}:{seed_bundle.controller_seed}:{episode_index}"
        )
        starts = initial_states(self.spec)
        if not starts:
            raise ValueError("initial state policy produced no legal start states")
        self.current_state = rng.choice(starts)
        self.current_core_state = counterpoint_state_to_core_state(self.current_state)
        self.step_index = 0
        self.terminated = False
        self.truncated = False
        self.last_transition_reward = 0.0
        self.last_lift_trace = None
        return ActiveTierState(
            active_tier=0,
            tier_state=self.current_tier_state(0),
            context_version=self.schema_id,
            event_index=0,
            deepest_known_tier=self.deepest_known_tier,
        )

    def current_tier_state(self, tier: int) -> object | None:
        if self.current_core_state is None:
            return None
        return self.build.tower.current_state_cell(tier, self.current_core_state)

    def tier_is_executable(self, tier: int) -> bool:
        if tier < 0 or tier >= self.tower_depth:
            return False
        state_cell = self.current_tier_state(tier)
        if state_cell is None:
            return False
        return bool(self.build.tower.outgoing_action_cells(tier, state_cell))

    def move_down(self, active_tier_state: ActiveTierState) -> ActiveTierState:
        next_tier = active_tier_state.downstairs_tier()
        return replace(
            active_tier_state,
            active_tier=next_tier,
            tier_state=self.current_tier_state(next_tier),
            deepest_known_tier=self.deepest_known_tier,
        )

    def move_up(self, active_tier_state: ActiveTierState) -> ActiveTierState:
        next_tier = active_tier_state.upstairs_tier()
        return replace(
            active_tier_state,
            active_tier=next_tier,
            tier_state=self.current_tier_state(next_tier),
            deepest_known_tier=self.deepest_known_tier,
        )

    def trace_fields(self, active_tier_state: ActiveTierState) -> dict[str, object]:
        return {
            "active_tier": active_tier_state.active_tier,
            "tier_state": repr(active_tier_state.tier_state),
            "event_index": active_tier_state.event_index,
            "deepest_known_tier": active_tier_state.deepest_known_tier,
        }


class TimedActiveTierController:
    """Controller wrapper that records only controller-decision time."""

    def __init__(self, recorder: TimingRecorder) -> None:
        self._delegate = ActiveTierController()
        self._recorder = recorder

    def decide(
        self,
        active_tier_state: ActiveTierState,
        signal: TierSignalState,
        config: TierControlConfig,
        *,
        signals_by_tier: dict[int, TierSignalState],
        tier_configs: dict[int, TierControlConfig],
        frozen_context: FrozenLowerContext,
        training_due: bool,
        tier_is_executable: Callable[[int], bool] | None = None,
    ) -> ControllerDecision:
        with self._recorder.segment("controller_decision"):
            return self._delegate.decide(
                active_tier_state,
                signal,
                config,
                signals_by_tier=signals_by_tier,
                tier_configs=tier_configs,
                frozen_context=frozen_context,
                training_due=training_due,
                tier_is_executable=tier_is_executable,
            )


class CounterpointTierLearner:
    """TierLearner adapter wrapping upstream TabularQLearner instances."""

    def __init__(
        self,
        *,
        adapter: CounterpointTowerControlAdapter,
        learner_config: TabularQLearnerConfig,
        controller_config: ExploitExploreControllerConfig,
        seed: int,
        recorder: TimingRecorder,
    ) -> None:
        self.adapter = adapter
        self.learner_config = learner_config
        self.controller_config = controller_config
        self.recorder = recorder
        self.learners: dict[int, TabularQLearner] = {}
        self.last_source_input_by_tier: dict[int, ActionSelectionInput] = {}
        self.last_action_by_tier: dict[int, int] = {}
        self.last_observed_tier: int | None = None
        for tier in range(adapter.tower_depth):
            self.learners[tier] = TabularQLearner(
                action_count=self._tier_action_count(tier),
                alpha=learner_config.alpha,
                gamma=learner_config.gamma,
                epsilon=learner_config.epsilon,
                seed=seed + tier,
                key_fn=_tier_state_key,
            )

    def behavior_action(self, state: object | None, *, mode: str) -> object:
        tier = self._tier_for_state(state)
        action_input = self._action_input(tier, state)
        self.last_source_input_by_tier[tier] = action_input
        if not action_input.action_mask or not any(action_input.action_mask):
            self.last_action_by_tier[tier] = -1
            return -1
        with self.recorder.segment("learner_act"):
            decision = self.learners[tier].act(action_input, mode=mode)
        action_id = int(decision.chosen_action)
        self.last_action_by_tier[tier] = action_id
        return action_id

    def observe(
        self,
        transition: ActiveTierTransition,
        *,
        frozen_context: FrozenLowerContext,
    ) -> ControlLearnerUpdateSummary:
        del frozen_context
        tier = transition.tier_index
        chosen_action = self.last_action_by_tier.get(tier, -1)
        if chosen_action < 0:
            return ControlLearnerUpdateSummary(
                td_error=0.0,
                success=False,
                reward_residual=None,
            )
        source_input = self.last_source_input_by_tier[tier]
        target_input = self._action_input(tier, transition.target_state)
        self.learners[tier].observe(
            TrainingTransition(
                source_input=source_input,
                chosen_action=chosen_action,
                reward=transition.aggregated_reward,
                target_input=target_input,
                terminated=self.adapter.terminated,
                truncated=self.adapter.truncated,
                bootstrap_allowed=not self.adapter.terminated and not self.adapter.truncated,
                bootstrap_input=target_input,
                bootstrap_reason="tower_target_available",
                active_tier=tier,
                frozen_context_version=transition.context_version,
                diagnostics={
                    "tower_mode": True,
                    "transition_success": transition.success,
                },
            )
        )
        self.last_observed_tier = tier
        return ControlLearnerUpdateSummary(
            td_error=0.0,
            success=transition.success,
            reward_residual=None,
        )

    def should_train(self, event_index: int) -> bool:
        interval = self.controller_config.training_interval
        return (
            event_index > 0
            and event_index % interval == 0
            and self.last_observed_tier is not None
        )

    def train(self, *, frozen_context: FrozenLowerContext) -> ControlLearnerUpdateSummary:
        del frozen_context
        tier = self.last_observed_tier
        if tier is None:
            return ControlLearnerUpdateSummary(td_error=0.0, success=False)
        with self.recorder.segment("learner_update"):
            summary = self.learners[tier].update()
        return ControlLearnerUpdateSummary(
            td_error=0.0 if summary.td_error is None else float(summary.td_error),
            success=summary.updated,
            reward_residual=None,
        )

    def _tier_action_count(self, tier: int) -> int:
        layer = self.adapter.build.tower.state_layers[tier]
        counts = [
            len(self.adapter.build.tower.outgoing_action_cells(tier, cell_id))
            for cell_id in layer.all_cell_ids()
        ]
        return max(1, max(counts, default=0))

    def _tier_for_state(self, state: object | None) -> int:
        for tier in range(self.adapter.tower_depth):
            if state == self.adapter.current_tier_state(tier):
                return tier
        return 0

    def _action_input(self, tier: int, state: object | None) -> ActionSelectionInput:
        vocabulary = self._action_vocabulary(tier, state)
        action_count = self._tier_action_count(tier)
        action_mask = tuple(index < len(vocabulary) for index in range(action_count))
        return ActionSelectionInput(
            observation=state,
            current_base_state=self.adapter.current_state,
            runtime_snapshot=_minimal_runtime_snapshot(self.adapter),
            tower_position_key=tuple(
                self.adapter.current_tier_state(index)
                for index in range(self.adapter.tower_depth)
            ),
            action_mask=action_mask,
            active_tier_state=state,
            diagnostics={
                "tier_index": tier,
                "action_vocabulary": tuple(map(repr, vocabulary)),
            },
        )

    def _action_vocabulary(self, tier: int, state: object | None) -> tuple[object, ...]:
        if state is None:
            return ()
        return self.adapter.build.tower.outgoing_action_cells(tier, state)


class CounterpointLiftResolveExecutor:
    """Lift/resolve executor for counterpoint primitive actions."""

    def __init__(
        self,
        *,
        adapter: CounterpointTowerControlAdapter,
        recorder: TimingRecorder,
    ) -> None:
        self.adapter = adapter
        self.recorder = recorder

    def execute(
        self,
        active_tier_state: ActiveTierState,
        action: object,
        *,
        frozen_context: FrozenLowerContext,
        mode: str,
    ) -> ActiveTierTransition:
        del frozen_context, mode
        with self.recorder.segment("lift_resolve"):
            return self._execute(active_tier_state, action)

    def _execute(
        self,
        active_tier_state: ActiveTierState,
        action: object,
    ) -> ActiveTierTransition:
        tier = active_tier_state.active_tier
        source_tier_state = active_tier_state.tier_state
        if self.adapter.current_state is None or self.adapter.current_core_state is None:
            return self._failure(tier, source_tier_state, action, "missing_current_state", 0)
        if not isinstance(action, int) or action < 0:
            return self._failure(tier, source_tier_state, action, "invalid_action_index", 0)
        vocabulary = self.adapter.build.tower.outgoing_action_cells(tier, source_tier_state)
        if action >= len(vocabulary):
            return self._failure(
                tier,
                source_tier_state,
                action,
                "action_index_out_of_range",
                len(vocabulary),
            )
        action_cell = vocabulary[action]
        candidates = self.adapter.build.tower.lift_candidates(
            tier,
            action_cell,
            self.adapter.current_core_state,
        )
        executable = tuple(
            edge for edge in candidates if edge.source == self.adapter.current_core_state
        )
        if not executable:
            members = self.adapter.build.tower.action_cell_members(tier, action_cell)
            executable = tuple(
                edge for edge in members if edge.source == self.adapter.current_core_state
            )
        if not executable:
            return self._failure(
                tier,
                source_tier_state,
                action_cell,
                "no_lift_candidate_from_current_state",
                len(candidates),
            )
        edge = executable[0]
        counterpoint_action = primitive_action_to_counterpoint_action(edge.action)
        mask = legal_action_mask(self.adapter.spec, self.adapter.current_state)
        if counterpoint_action not in mask.legal_actions():
            return self._failure(
                tier,
                source_tier_state,
                action_cell,
                "realized_action_illegal",
                len(executable),
            )
        source_state = self.adapter.current_state
        with self.recorder.segment("environment_step"):
            transition = evaluate_transition(
                self.adapter.spec,
                source_state,
                counterpoint_action,
                step_index=self.adapter.step_index,
            )
        reward = 0.0 if transition.reward is None else transition.reward.total_reward
        self.adapter.current_state = transition.next_state
        self.adapter.current_core_state = counterpoint_state_to_core_state(transition.next_state)
        self.adapter.step_index += 1
        self.adapter.terminated = transition.terminated
        self.adapter.truncated = transition.truncated
        self.adapter.last_transition_reward = reward
        target_tier_state = self.adapter.current_tier_state(tier)
        self.adapter.last_lift_trace = LiftResolveTrace(
            active_tier=tier,
            abstract_action=repr(action_cell),
            realized_action=str(counterpoint_action.deltas),
            candidate_count=len(executable),
            success=True,
            failure_reason=None,
        )
        return ActiveTierTransition(
            tier_index=tier,
            source_state=source_tier_state,
            action=action_cell,
            target_state=target_tier_state,
            aggregated_reward=reward,
            context_version=active_tier_state.context_version,
            representative_jump=edge,
            success=True,
        )

    def _failure(
        self,
        tier: int,
        source_tier_state: object | None,
        action: object,
        reason: str,
        candidate_count: int,
    ) -> ActiveTierTransition:
        self.adapter.last_lift_trace = LiftResolveTrace(
            active_tier=tier,
            abstract_action=repr(action),
            realized_action=None,
            candidate_count=candidate_count,
            success=False,
            failure_reason=reason,
            fiber_departure_reason=reason,
        )
        return ActiveTierTransition(
            tier_index=tier,
            source_state=source_tier_state,
            action=action,
            target_state=source_tier_state,
            aggregated_reward=0.0,
            context_version=None,
            representative_jump=None,
            success=False,
        )


def build_tier_configs(
    adapter: CounterpointTowerControlAdapter,
    config: ExploitExploreControllerConfig,
) -> dict[int, TierControlConfig]:
    return {
        tier: TierControlConfig(
            epsilon=config.epsilon,
            min_visit_count=config.min_visit_count,
            td_error_threshold=config.td_error_threshold,
            success_threshold=config.success_threshold,
            reward_residual_threshold=config.reward_residual_threshold,
            training_interval=config.training_interval,
            batch_size=config.batch_size,
        )
        for tier in range(adapter.tower_depth)
    }


def _max_tier_action_count(adapter: CounterpointTowerControlAdapter) -> int:
    max_count = 1
    for tier in range(adapter.tower_depth):
        layer = adapter.build.tower.state_layers[tier]
        for cell_id in layer.all_cell_ids():
            max_count = max(
                max_count,
                len(adapter.build.tower.outgoing_action_cells(tier, cell_id)),
            )
    return max_count


def run_serious_tower_control(
    *,
    spec: CounterpointInstanceSpec,
    arm_id: str,
    seed_bundle: SeedBundle,
    artifact_root: Path | str,
    schema_seed: int | None = None,
    controller_config: ExploitExploreControllerConfig | None = None,
    learner_config: TabularQLearnerConfig | None = None,
    horizon: int | None = None,
    episode_count: int = 1,
    linearization_mode_id: str = "tensor_available_disabled",
    run_family_id: str = SERIOUS_TOWER_RUN_FAMILY_ID,
    run_id: str | None = None,
) -> BenchmarkRunResult:
    arm = get_serious_learning_arm(arm_id)
    if not arm.requires_tower:
        raise ValueError("tower-control runner requires a tower arm")
    if arm.schema_id is None:
        raise ValueError("tower-control arm requires schema_id")
    active_horizon = spec.horizon_steps if horizon is None else horizon
    if active_horizon <= 0:
        raise ValueError("horizon must be positive")
    if episode_count <= 0:
        raise ValueError("episode_count must be positive")
    active_schema_seed = seed_bundle.schema_seed if schema_seed is None else schema_seed
    config = ExploitExploreControllerConfig() if controller_config is None else controller_config
    learner_cfg = TabularQLearnerConfig() if learner_config is None else learner_config
    run_id = run_id or (
        f"{spec.environment_instance_id}-{arm.arm_id}-schema{active_schema_seed}-"
        f"rep{seed_bundle.replicate_index}"
    )
    recorder = TimingRecorder.create(run_id)
    adapter = CounterpointTowerControlAdapter(
        spec=spec,
        schema_id=arm.schema_id,
        schema_seed=active_schema_seed if arm.requires_schema_seed else None,
        recorder=recorder,
    )
    episodes = tuple(
        _run_tower_control_episode(
            adapter=adapter,
            arm_id=arm.arm_id,
            mode_id=arm.mode_id,
            seed_bundle=seed_bundle,
            episode_index=episode_index,
            horizon=active_horizon,
            recorder=recorder,
            controller_config=config,
            learner_config=learner_cfg,
        )
        for episode_index in range(episode_count)
    )
    return _write_tower_serious_artifacts(
        spec=spec,
        build=adapter.build,
        artifact_root=artifact_root,
        run_family_id=run_family_id,
        run_id=run_id,
        arm_id=arm.arm_id,
        mode_id=arm.mode_id,
        schema_id=arm.schema_id,
        schema_seed=active_schema_seed if arm.requires_schema_seed else None,
        linearization_mode_id=linearization_mode_id,
        seed_bundle=seed_bundle,
        budget={
            "episodes": episode_count,
            "horizon": active_horizon,
            "schema_seed": active_schema_seed if arm.requires_schema_seed else None,
            "controller_config": config.to_dict(),
            "learner_config": learner_cfg.to_dict(),
        },
        recorder=recorder,
        episodes=episodes,
        command="python -m big_boy_benchmarking.cli counterpoint serious-learning run",
        max_action_count=_max_tier_action_count(adapter),
    )


def _run_tower_control_episode(
    *,
    adapter: CounterpointTowerControlAdapter,
    arm_id: str,
    mode_id: str,
    seed_bundle: SeedBundle,
    episode_index: int,
    horizon: int,
    recorder: TimingRecorder,
    controller_config: ExploitExploreControllerConfig,
    learner_config: TabularQLearnerConfig,
) -> TowerControlEpisodeTrace:
    with recorder.segment("environment_reset"):
        active_tier_state = adapter.reset(seed_bundle=seed_bundle, episode_index=episode_index)
    learner = CounterpointTierLearner(
        adapter=adapter,
        learner_config=learner_config,
        controller_config=controller_config,
        seed=seed_bundle.learner_seed,
        recorder=recorder,
    )
    executor = CounterpointLiftResolveExecutor(adapter=adapter, recorder=recorder)
    runtime = ExploitExploreTowerRuntime(
        active_tier_state=active_tier_state,
        tier_configs=build_tier_configs(adapter, controller_config),
        controller=TimedActiveTierController(recorder),
        learner=learner,
        executor=executor,
        frozen_contexts={
            tier: FrozenLowerContext(
                supporting_tier=tier + 1 if tier + 1 < adapter.tower_depth else None,
                version=0,
                metadata={"schema_id": adapter.schema_id},
            )
            for tier in range(adapter.tower_depth)
        },
        move_down=adapter.move_down,
        move_up=adapter.move_up,
        tier_is_executable=adapter.tier_is_executable,
    )
    steps: list[TowerControlStepTrace] = []
    controller_rows: list[ControllerEventRow] = []
    lift_rows: list[LiftFiberEventRow] = []
    total_reward = 0.0
    max_controller_events = max(8, horizon * 8)
    event_index = 0
    while adapter.step_index < horizon and event_index < max_controller_events:
        before = runtime.active_tier_state
        source_state = adapter.current_state
        result = runtime.step()
        after = result.active_tier_state
        summary = result.learner_summary
        controller_rows.append(
            ControllerEventRow(
                evaluation_id=SERIOUS_EVALUATION_ID,
                run_id="pending",
                arm_id=arm_id,
                episode_index=episode_index,
                step_index=event_index,
                active_tier_before=before.active_tier,
                active_tier_after=after.active_tier,
                control_action=result.decision.value,
                pressure=None,
                learner_updated=None if summary is None else summary.success,
                td_error=None if summary is None else summary.td_error,
                success=None if summary is None else summary.success,
            )
        )
        if result.transition is not None and adapter.last_lift_trace is not None:
            trace = adapter.last_lift_trace
            lift_rows.append(
                LiftFiberEventRow(
                    evaluation_id=SERIOUS_EVALUATION_ID,
                    run_id="pending",
                    arm_id=arm_id,
                    episode_index=episode_index,
                    step_index=event_index,
                    active_tier=trace.active_tier,
                    abstract_action=trace.abstract_action,
                    realized_action=trace.realized_action,
                    candidate_count=trace.candidate_count,
                    success=trace.success,
                    failure_reason=trace.failure_reason,
                    fiber_departure_reason=trace.fiber_departure_reason,
                )
            )
            if trace.success and source_state is not None and adapter.current_state is not None:
                reward = adapter.last_transition_reward
                total_reward += reward
                steps.append(
                    TowerControlStepTrace(
                        episode_index=episode_index,
                        step_index=adapter.step_index - 1,
                        source_state=source_state,
                        action_id=None,
                        action=_parse_realized_action(trace.realized_action),
                        reward=reward,
                        target_state=adapter.current_state,
                        terminated=adapter.terminated,
                        truncated=adapter.truncated,
                        active_tier_before=before.active_tier,
                        active_tier_after=after.active_tier,
                    )
                )
        if adapter.terminated or adapter.truncated:
            break
        event_index += 1
    truncated = adapter.truncated or (not adapter.terminated and adapter.step_index >= horizon)
    return TowerControlEpisodeTrace(
        episode_index=episode_index,
        seed_bundle_id=seed_bundle.seed_bundle_id,
        replicate_index=seed_bundle.replicate_index,
        total_reward=total_reward,
        steps=tuple(steps),
        controller_rows=tuple(controller_rows),
        lift_rows=tuple(lift_rows),
        terminated=adapter.terminated,
        truncated=truncated,
    )


def _minimal_runtime_snapshot(adapter: CounterpointTowerControlAdapter):
    from state_collapser.core.rewards import PathRewardSummary
    from state_collapser.graph.explored_graph import ExploredGraph
    from state_collapser.graph.vista_graph import VistaGraph
    from state_collapser.tower.snapshot import LiveRuntimeView

    explored_graph = ExploredGraph()
    vista_graph = VistaGraph(adapter.build.hidden_graph, explored_graph)
    return LiveRuntimeView(
        current_base_state=adapter.current_state,
        explored_graph=explored_graph,
        vista_graph=vista_graph,
        ordered_quotient_tiers=(),
        current_position_at_every_tier=tuple(
            adapter.current_tier_state(tier) for tier in range(adapter.tower_depth)
        ),
        current_step_reward=None,
        cumulative_path_reward=PathRewardSummary(),
        quotient_tier_reward_summaries=(),
        active_control_tier=None,
        last_control_action=None,
        partition_tower_view=adapter.build.tower,
        tower_update_result=None,
    )


def _tier_state_key(action_input: ActionSelectionInput) -> tuple[object | None, ...]:
    return (
        "tower_tier_state",
        action_input.diagnostics.get("tier_index"),
        repr(action_input.observation),
    )


def _parse_realized_action(realized_action: str | None) -> CounterpointAction | None:
    if realized_action is None:
        return None
    stripped = realized_action.strip("()")
    if not stripped:
        return None
    return CounterpointAction(tuple(int(part.strip()) for part in stripped.split(",")))


def _write_tower_serious_artifacts(
    *,
    spec: CounterpointInstanceSpec,
    build: CounterpointTowerBuildResult,
    artifact_root: Path | str,
    run_family_id: str,
    run_id: str,
    arm_id: str,
    mode_id: str,
    schema_id: str,
    schema_seed: int | None,
    linearization_mode_id: str,
    seed_bundle: SeedBundle,
    budget: dict[str, Any],
    recorder: TimingRecorder,
    episodes: tuple[TowerControlEpisodeTrace, ...],
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
        tower=build.tower,
        max_action_count=max_action_count,
        metadata={
            "runner": "counterpoint_serious_tower_control",
            "evaluation_id": SERIOUS_EVALUATION_ID,
            "environment_instance_id": spec.environment_instance_id,
            "arm_id": arm_id,
            "mode_id": mode_id,
            "schema_id": schema_id,
        },
    )
    schema = build_schema_for_id(build.graph, schema_id=schema_id, schema_seed=schema_seed)

    write_json(
        family_paths.family_manifest,
        FamilyManifest(
            run_family_id=run_family_id,
            description="Counterpoint symbolic first serious learning tower-control family.",
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
    write_json(
        run_paths.external_artifacts,
        ExternalArtifactsManifest(run_id=run_id).to_dict(),
        create_parents=True,
    )
    write_json(
        run_paths.root / "environment_instance_manifest.json",
        environment_instance_manifest(spec),
        create_parents=True,
    )
    write_json(run_paths.root / "schema_manifest.json", schema.spec.to_dict())
    write_json(
        run_paths.root / "quotient_summary.json",
        {
            "schema_id": schema.spec.schema_id,
            "partition_tier_count": len(build.tower.state_layers),
            "state_cell_count_by_tier": [
                len(layer.all_cell_ids()) for layer in build.tower.state_layers
            ],
            "edge_count": len(build.graph.edges),
        },
    )

    for episode in episodes:
        append_csv_row(
            run_paths.episodes_csv,
            SeriousEpisodeRow(
                evaluation_id=SERIOUS_EVALUATION_ID,
                run_id=run_id,
                arm_id=arm_id,
                mode_id=mode_id,
                schema_id=schema_id,
                schema_seed=schema_seed,
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
                    action_repr="" if step.action is None else str(step.action.deltas),
                    reward=step.reward,
                    target_state=_state_repr(step.target_state),
                    terminated=step.terminated,
                    truncated=step.truncated,
                    active_tier_before=step.active_tier_before,
                    active_tier_after=step.active_tier_after,
                ).to_flat_dict(),
                SeriousStepRow.fieldnames(),
                create_parents=True,
            )
        for row in episode.controller_rows:
            append_csv_row(
                run_paths.control_events_csv,
                replace(row, run_id=run_id).to_flat_dict(),
                ControllerEventRow.fieldnames(),
                create_parents=True,
            )
        for row in episode.lift_rows:
            append_csv_row(
                run_paths.root / "lift_fiber_events.csv",
                replace(row, run_id=run_id).to_flat_dict(),
                LiftFiberEventRow.fieldnames(),
                create_parents=True,
            )

    write_csv(
        run_paths.timing_segments_csv,
        [row.to_flat_dict() for row in recorder.rows],
        recorder.rows[0].fieldnames() if recorder.rows else (),
        create_parents=True,
    )
    write_json(run_paths.timing_summary, summarize_timing_segments(recorder.rows))
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
            schema_id=schema_id,
            learner_id=mode_contract.learner_id,
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
        "schema_id": schema_id,
        "schema_seed": schema_seed,
        "linearization_mode_id": linearization_mode_id,
        "linearization_benchmark_label": linearization_payload.report.benchmark_label,
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
        artifact_paths={
            "run_manifest": str(run_paths.run_manifest),
            "seed_bundle": str(run_paths.seed_bundle),
            "mode_manifest": str(run_paths.mode_manifest),
            "linearization_manifest": str(run_paths.linearization_manifest),
            "timing_summary": str(run_paths.timing_summary),
            "episodes_csv": str(run_paths.episodes_csv),
            "step_events_csv": str(run_paths.step_events_csv),
            "control_events_csv": str(run_paths.control_events_csv),
            "timing_segments_csv": str(run_paths.timing_segments_csv),
            "external_artifacts": str(run_paths.external_artifacts),
            "lift_fiber_events_csv": str(run_paths.root / "lift_fiber_events.csv"),
            "schema_manifest": str(run_paths.root / "schema_manifest.json"),
            "quotient_summary": str(run_paths.root / "quotient_summary.json"),
        },
        summary_path=str(family_paths.summary_json),
        warning_count=0,
        started_at=started_at,
        ended_at=ended_at,
        failure_reason=None,
    )


def _now() -> str:
    return datetime.now(UTC).isoformat()
