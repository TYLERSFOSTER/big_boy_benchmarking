"""Runner for one-third counterpoint tower diagnostics."""

from __future__ import annotations

import statistics
from collections import Counter, defaultdict
from collections.abc import Callable
from dataclasses import dataclass
from datetime import UTC, datetime
from pathlib import Path
from typing import Any

from state_collapser.tower.control import (
    ActiveTierController,
    ActiveTierState,
    ControllerDecision,
    FrozenLowerContext,
    TierControlConfig,
    TierSignalState,
    is_unclosed,
    productive_learning_pressure,
    select_lowest_unclosed_tier,
    should_descend,
    should_lift,
)
from state_collapser.tower.runtime import ExploitExploreTowerRuntime

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
    append_jsonl,
    ensure_artifact_dirs,
    write_csv,
    write_json,
)
from big_boy_benchmarking.environments.counterpoint import ids
from big_boy_benchmarking.environments.counterpoint.artifacts import (
    environment_instance_manifest,
)
from big_boy_benchmarking.environments.counterpoint.instances import (
    MEDIUM_INSTANCE_ID,
    SMALL_INSTANCE_ID,
    default_medium_spec,
    default_small_spec,
)
from big_boy_benchmarking.environments.counterpoint.liftability import (
    STATE_COLLAPSER_V072_POINTWISE_LIFTABILITY_SEMANTICS_ID,
)
from big_boy_benchmarking.environments.counterpoint.one_third_diagnostics.config import (
    DEFAULT_LINEARIZATION_MODE_ID,
    DEFAULT_MODE_ID,
    DEFAULT_SCHEMA_ID,
    DEFAULT_SCHEMA_SEEDS,
    EVALUATION_ID,
    EVALUATION_RUN_FAMILY_ID,
    NEAR_FULL_COLLAPSE_THRESHOLD,
    OneThirdDiagnosticsBudget,
)
from big_boy_benchmarking.environments.counterpoint.one_third_diagnostics.events import (
    ABCSelectionEventRow,
    ABCTierSignalEventRow,
    OneThirdControlEventRow,
    OneThirdEpisodeRow,
    OneThirdEvaluationRunIndexRow,
    OneThirdLiftFiberEventRow,
    OneThirdStepRow,
    SchemaBlockSummaryRow,
    TowerShapeSummaryRow,
)
from big_boy_benchmarking.environments.counterpoint.one_third_diagnostics.manifests import (
    budget_lock_payload,
    evaluation_manifest_payload,
)
from big_boy_benchmarking.environments.counterpoint.one_third_diagnostics.paths import (
    build_one_third_diagnostics_paths,
    validate_repo_resident_artifact_root,
)
from big_boy_benchmarking.environments.counterpoint.schemas import (
    build_schema_for_id,
    edge_key,
    state_key,
)
from big_boy_benchmarking.environments.counterpoint.serious_learning.config import (
    ExploitExploreControllerConfig,
    TabularQLearnerConfig,
)
from big_boy_benchmarking.environments.counterpoint.serious_learning.direct import (
    _state_repr,
)
from big_boy_benchmarking.environments.counterpoint.serious_learning.tower_control import (
    CounterpointLiftResolveExecutor,
    CounterpointTierLearner,
    CounterpointTowerControlAdapter,
    _parse_realized_action,
    build_tier_configs,
)
from big_boy_benchmarking.environments.counterpoint.specs import CounterpointInstanceSpec
from big_boy_benchmarking.environments.counterpoint.tower_adapter import (
    CounterpointTowerBuildResult,
    counterpoint_tower_invariant_artifact_payload,
)
from big_boy_benchmarking.metrics.timing import TimingRecorder, summarize_timing_segments
from big_boy_benchmarking.modes.registry import require_runnable_mode
from big_boy_benchmarking.runners.base import BenchmarkRunResult
from big_boy_benchmarking.seeds.bundles import SeedBundle, generate_seed_bundles
from big_boy_benchmarking.upstream.linearization import (
    REPORT_SOURCE,
    build_linearization_artifact_payload,
)
from big_boy_benchmarking.upstream.state_collapser import (
    STATE_COLLAPSER_DEPENDENCY_SPEC,
    collect_state_collapser_dependency_state,
)


@dataclass(frozen=True)
class ABCTierSignalSnapshot:
    tier_index: int
    executable: bool
    visit_count: int
    td_error_ema: float
    success_count: int
    failure_count: int
    success_rate: float
    reward_residual_ema: float
    has_reward_residual: bool
    pressure: float
    unclosed: bool


@dataclass(frozen=True)
class ABCDecisionSnapshot:
    active_tier_before: int
    deepest_known_tier: int
    selected_tier: int | None
    selected_tier_executable: bool | None
    predicted_movement_direction: str
    training_due: bool
    decision_action: str
    decision_pressure: float
    tier_signals: tuple[ABCTierSignalSnapshot, ...]


@dataclass(frozen=True)
class OneThirdEpisodeTrace:
    episode_row: OneThirdEpisodeRow
    step_rows: tuple[OneThirdStepRow, ...]
    control_rows: tuple[OneThirdControlEventRow, ...]
    lift_rows: tuple[OneThirdLiftFiberEventRow, ...]
    abc_selection_rows: tuple[ABCSelectionEventRow, ...]
    abc_tier_signal_rows: tuple[ABCTierSignalEventRow, ...]


@dataclass(frozen=True)
class OneThirdRunRecord:
    instance_id: str
    schema_seed: int
    seed_bundle: SeedBundle
    result: BenchmarkRunResult | None
    status: str
    failure_reason: str | None = None


class DiagnosticActiveTierController:
    """Record upstream ABC helper diagnostics and return the upstream decision."""

    def __init__(self, recorder: TimingRecorder) -> None:
        self._delegate = ActiveTierController()
        self._recorder = recorder
        self.snapshots: list[ABCDecisionSnapshot] = []

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
        del signal, config
        deepest_known_tier = (
            active_tier_state.active_tier
            if active_tier_state.deepest_known_tier is None
            else active_tier_state.deepest_known_tier
        )
        selected_tier = select_lowest_unclosed_tier(
            deepest_known_tier,
            signals_by_tier,
            tier_configs,
            tier_is_executable=tier_is_executable,
        )
        selected_executable = (
            None
            if selected_tier is None
            else _tier_executable(selected_tier, tier_is_executable)
        )
        if should_lift(active_tier_state.active_tier, selected_tier):
            movement = "lift"
        elif should_descend(active_tier_state.active_tier, selected_tier):
            movement = "descend"
        elif selected_tier is None:
            movement = "no_executable_unclosed"
        else:
            movement = "at_selected"

        tier_snapshots = tuple(
            _tier_signal_snapshot(
                tier_index=tier_index,
                signals_by_tier=signals_by_tier,
                tier_configs=tier_configs,
                tier_is_executable=tier_is_executable,
            )
            for tier_index in range(deepest_known_tier + 1)
        )
        with self._recorder.segment("controller_decision"):
            decision = self._delegate.decide(
                active_tier_state,
                signals_by_tier.setdefault(active_tier_state.active_tier, TierSignalState()),
                tier_configs[active_tier_state.active_tier],
                signals_by_tier=signals_by_tier,
                tier_configs=tier_configs,
                frozen_context=frozen_context,
                training_due=training_due,
                tier_is_executable=tier_is_executable,
            )
        self.snapshots.append(
            ABCDecisionSnapshot(
                active_tier_before=active_tier_state.active_tier,
                deepest_known_tier=deepest_known_tier,
                selected_tier=selected_tier,
                selected_tier_executable=selected_executable,
                predicted_movement_direction=movement,
                training_due=training_due,
                decision_action=decision.action.value,
                decision_pressure=decision.pressure,
                tier_signals=tier_snapshots,
            )
        )
        return decision


def counterpoint_one_third_spec_for_instance(instance_id: str) -> CounterpointInstanceSpec:
    if instance_id == "small" or instance_id == SMALL_INSTANCE_ID:
        return default_small_spec()
    if instance_id == "medium" or instance_id == MEDIUM_INSTANCE_ID:
        return default_medium_spec()
    if instance_id == "tiny" or instance_id.endswith("_tiny_v001"):
        raise ValueError("tiny is not part of one-third diagnostics")
    raise ValueError(f"unknown counterpoint one-third diagnostics instance: {instance_id}")


def run_one_third_diagnostics(
    *,
    artifact_root: Path | str,
    instance_ids: tuple[str, ...] = ("small", "medium"),
    schema_seeds: tuple[int, ...] = DEFAULT_SCHEMA_SEEDS,
    replicates_per_schema_seed: int = 4,
    episodes_per_replicate: int = 16,
    base_seed: int = 0,
    locked_by: str = "cli",
    horizon_override: int | None = None,
    controller_event_ceiling: int | None = None,
    linearization_mode_id: str = DEFAULT_LINEARIZATION_MODE_ID,
) -> dict[str, Any]:
    artifact_root = validate_repo_resident_artifact_root(artifact_root)
    specs = tuple(counterpoint_one_third_spec_for_instance(item) for item in instance_ids)
    budget = OneThirdDiagnosticsBudget(
        instance_ids=tuple(spec.environment_instance_id for spec in specs),
        schema_seeds=schema_seeds,
        replicates_per_schema_seed=replicates_per_schema_seed,
        episodes_per_replicate=episodes_per_replicate,
        horizon_by_instance_id={
            spec.environment_instance_id: horizon_override or spec.horizon_steps
            for spec in specs
        },
        controller_event_ceiling_override=controller_event_ceiling,
        linearization_mode_id=linearization_mode_id,
        base_seed=base_seed,
        locked_by=locked_by,
    )
    paths = build_one_third_diagnostics_paths(artifact_root)
    paths.root.mkdir(parents=True, exist_ok=True)
    paths.results_dir.mkdir(parents=True, exist_ok=True)
    write_json(
        paths.evaluation_manifest,
        evaluation_manifest_payload(budget=budget),
        create_parents=True,
    )
    write_json(paths.evaluation_budget_lock, budget_lock_payload(budget=budget))

    seed_bundles = generate_seed_bundles(
        base_seed=base_seed,
        replicate_count=replicates_per_schema_seed,
    )
    records: list[OneThirdRunRecord] = []
    for spec in specs:
        horizon = horizon_override or spec.horizon_steps
        for schema_seed in schema_seeds:
            for seed_bundle in seed_bundles:
                try:
                    result = run_one_third_diagnostic_run(
                        spec=spec,
                        schema_seed=schema_seed,
                        seed_bundle=seed_bundle,
                        artifact_root=artifact_root,
                        episode_count=episodes_per_replicate,
                        horizon=horizon,
                        max_controller_events=budget.max_controller_events(horizon),
                        linearization_mode_id=linearization_mode_id,
                    )
                    records.append(
                        OneThirdRunRecord(
                            instance_id=spec.environment_instance_id,
                            schema_seed=schema_seed,
                            seed_bundle=seed_bundle,
                            result=result,
                            status=result.status,
                        )
                    )
                except Exception as exc:  # pragma: no cover - failure recording boundary
                    records.append(
                        OneThirdRunRecord(
                            instance_id=spec.environment_instance_id,
                            schema_seed=schema_seed,
                            seed_bundle=seed_bundle,
                            result=None,
                            status="failed",
                            failure_reason=f"{type(exc).__name__}: {exc}",
                        )
                    )
    write_csv(
        paths.evaluation_run_index_csv,
        [_run_index_row(paths.root, artifact_root, record).to_flat_dict() for record in records],
        OneThirdEvaluationRunIndexRow.fieldnames(),
    )
    status = "complete" if all(record.status == "success" for record in records) else "incomplete"
    return {
        "status": status,
        "evaluation_id": EVALUATION_ID,
        "run_count": len(records),
        "evaluation_run_index": str(paths.evaluation_run_index_csv),
        "evaluation_budget_lock": str(paths.evaluation_budget_lock),
    }


def run_one_third_diagnostic_run(
    *,
    spec: CounterpointInstanceSpec,
    schema_seed: int,
    seed_bundle: SeedBundle,
    artifact_root: Path | str,
    episode_count: int,
    horizon: int,
    max_controller_events: int,
    linearization_mode_id: str = DEFAULT_LINEARIZATION_MODE_ID,
    controller_config: ExploitExploreControllerConfig | None = None,
    learner_config: TabularQLearnerConfig | None = None,
) -> BenchmarkRunResult:
    if linearization_mode_id != DEFAULT_LINEARIZATION_MODE_ID:
        raise ValueError(
            "one-third diagnostics use tensor_available_disabled; "
            f"reserved linearization mode rejected: {linearization_mode_id}"
        )
    if horizon <= 0:
        raise ValueError("horizon must be positive")
    if episode_count <= 0:
        raise ValueError("episode_count must be positive")
    config = ExploitExploreControllerConfig() if controller_config is None else controller_config
    learner_cfg = TabularQLearnerConfig() if learner_config is None else learner_config
    run_id = (
        f"{spec.environment_instance_id}-one-third-schema{schema_seed}-"
        f"rep{seed_bundle.replicate_index}"
    )
    started_at = _now()
    recorder = TimingRecorder.create(run_id)
    adapter = CounterpointTowerControlAdapter(
        spec=spec,
        schema_id=DEFAULT_SCHEMA_ID,
        schema_seed=schema_seed,
        recorder=recorder,
    )
    episodes = tuple(
        _run_one_third_episode(
            adapter=adapter,
            run_id=run_id,
            instance_id=spec.environment_instance_id,
            schema_seed=schema_seed,
            seed_bundle=seed_bundle,
            episode_index=episode_index,
            horizon=horizon,
            max_controller_events=max_controller_events,
            recorder=recorder,
            controller_config=config,
            learner_config=learner_cfg,
        )
        for episode_index in range(episode_count)
    )
    ended_at = _now()
    return _write_one_third_artifacts(
        spec=spec,
        build=adapter.build,
        artifact_root=artifact_root,
        run_id=run_id,
        schema_seed=schema_seed,
        linearization_mode_id=linearization_mode_id,
        seed_bundle=seed_bundle,
        budget={
            "episodes": episode_count,
            "horizon": horizon,
            "schema_seed": schema_seed,
            "max_controller_events": max_controller_events,
            "controller_event_ceiling_policy": "max(64, 8 * horizon)",
            "controller_config": config.to_dict(),
            "learner_config": learner_cfg.to_dict(),
        },
        recorder=recorder,
        episodes=episodes,
        max_action_count=_max_tier_action_count(adapter),
        started_at=started_at,
        ended_at=ended_at,
    )


def _run_one_third_episode(
    *,
    adapter: CounterpointTowerControlAdapter,
    run_id: str,
    instance_id: str,
    schema_seed: int,
    seed_bundle: SeedBundle,
    episode_index: int,
    horizon: int,
    max_controller_events: int,
    recorder: TimingRecorder,
    controller_config: ExploitExploreControllerConfig,
    learner_config: TabularQLearnerConfig,
) -> OneThirdEpisodeTrace:
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
    controller = DiagnosticActiveTierController(recorder)
    runtime = ExploitExploreTowerRuntime(
        active_tier_state=active_tier_state,
        tier_configs=build_tier_configs(adapter, controller_config),
        controller=controller,
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
    step_rows: list[OneThirdStepRow] = []
    control_rows: list[OneThirdControlEventRow] = []
    lift_rows: list[OneThirdLiftFiberEventRow] = []
    abc_selection_rows: list[ABCSelectionEventRow] = []
    abc_tier_signal_rows: list[ABCTierSignalEventRow] = []
    total_reward = 0.0
    controller_event_index = 0
    while adapter.step_index < horizon and controller_event_index < max_controller_events:
        before = runtime.active_tier_state
        source_state = adapter.current_state
        snapshot_count = len(controller.snapshots)
        pre_step_liftability_counts = _liftability_counts_by_tier(adapter)
        result = runtime.step()
        after = result.active_tier_state
        snapshot = (
            controller.snapshots[-1] if len(controller.snapshots) > snapshot_count else None
        )
        summary = result.learner_summary
        control_rows.append(
            OneThirdControlEventRow(
                evaluation_id=EVALUATION_ID,
                run_id=run_id,
                instance_id=instance_id,
                schema_id=DEFAULT_SCHEMA_ID,
                schema_seed=schema_seed,
                seed_bundle_id=seed_bundle.seed_bundle_id,
                replicate_index=seed_bundle.replicate_index,
                episode_index=episode_index,
                controller_event_index=controller_event_index,
                active_tier_before=before.active_tier,
                active_tier_after=after.active_tier,
                control_action=result.decision.value,
                pressure=None if snapshot is None else snapshot.decision_pressure,
                learner_updated=None if summary is None else summary.success,
                td_error=None if summary is None else summary.td_error,
                success=None if summary is None else summary.success,
            )
        )

        lift_trace = adapter.last_lift_trace if result.transition is not None else None
        if lift_trace is not None:
            lift_rows.append(
                OneThirdLiftFiberEventRow(
                    evaluation_id=EVALUATION_ID,
                    run_id=run_id,
                    instance_id=instance_id,
                    schema_id=DEFAULT_SCHEMA_ID,
                    schema_seed=schema_seed,
                    seed_bundle_id=seed_bundle.seed_bundle_id,
                    replicate_index=seed_bundle.replicate_index,
                    episode_index=episode_index,
                    controller_event_index=controller_event_index,
                    active_tier=lift_trace.active_tier,
                    abstract_action=lift_trace.abstract_action,
                    realized_action=lift_trace.realized_action,
                    candidate_count=lift_trace.candidate_count,
                    success=lift_trace.success,
                    failure_reason=lift_trace.failure_reason,
                    fiber_departure_reason=lift_trace.fiber_departure_reason,
                    liftability_semantics_id=lift_trace.liftability_semantics_id,
                    representative_candidate_count=(
                        lift_trace.representative_candidate_count
                    ),
                    pointwise_candidate_count=lift_trace.pointwise_candidate_count,
                    selected_lift_index=lift_trace.selected_lift_index,
                    selected_lift_source_matches_current=(
                        lift_trace.selected_lift_source_matches_current
                    ),
                    selected_lift_target_repr=lift_trace.selected_lift_target_repr,
                    quotient_action_cell_count=lift_trace.quotient_action_cell_count,
                    pointwise_executable_action_cell_count=(
                        lift_trace.pointwise_executable_action_cell_count
                    ),
                )
            )

        concrete_step_emitted = (
            lift_trace is not None
            and lift_trace.success
            and source_state is not None
            and adapter.current_state is not None
        )
        if snapshot is not None:
            abc_selection_rows.append(
                _abc_selection_row(
                    snapshot=snapshot,
                    run_id=run_id,
                    instance_id=instance_id,
                    schema_seed=schema_seed,
                    seed_bundle=seed_bundle,
                    episode_index=episode_index,
                    controller_event_index=controller_event_index,
                    active_tier_after=after.active_tier,
                    concrete_step_emitted=concrete_step_emitted,
                    lift_attempt_emitted=lift_trace is not None,
                    lift_success=None if lift_trace is None else lift_trace.success,
                    control_action=result.decision.value,
                )
            )
            abc_tier_signal_rows.extend(
                _abc_tier_signal_rows(
                    snapshot=snapshot,
                    run_id=run_id,
                    instance_id=instance_id,
                    schema_seed=schema_seed,
                    seed_bundle=seed_bundle,
                    episode_index=episode_index,
                    controller_event_index=controller_event_index,
                    liftability_counts_by_tier=pre_step_liftability_counts,
                )
            )

        if concrete_step_emitted:
            reward = adapter.last_transition_reward
            total_reward += reward
            assert source_state is not None
            assert adapter.current_state is not None
            action = _parse_realized_action(lift_trace.realized_action)
            step_rows.append(
                OneThirdStepRow(
                    evaluation_id=EVALUATION_ID,
                    run_id=run_id,
                    instance_id=instance_id,
                    schema_id=DEFAULT_SCHEMA_ID,
                    schema_seed=schema_seed,
                    seed_bundle_id=seed_bundle.seed_bundle_id,
                    replicate_index=seed_bundle.replicate_index,
                    episode_index=episode_index,
                    step_index=adapter.step_index - 1,
                    controller_event_index=controller_event_index,
                    source_state=_state_repr(source_state),
                    action_repr="" if action is None else str(action.deltas),
                    reward=reward,
                    target_state=_state_repr(adapter.current_state),
                    terminated=adapter.terminated,
                    truncated=adapter.truncated,
                    active_tier_before=before.active_tier,
                    active_tier_after=after.active_tier,
                )
            )
        if adapter.terminated or adapter.truncated:
            break
        controller_event_index += 1
    truncated = adapter.truncated or (not adapter.terminated and adapter.step_index >= horizon)
    final_state = _state_repr(adapter.current_state) if adapter.current_state is not None else ""
    episode_row = OneThirdEpisodeRow(
        evaluation_id=EVALUATION_ID,
        run_id=run_id,
        instance_id=instance_id,
        schema_id=DEFAULT_SCHEMA_ID,
        schema_seed=schema_seed,
        seed_bundle_id=seed_bundle.seed_bundle_id,
        replicate_index=seed_bundle.replicate_index,
        episode_index=episode_index,
        total_reward=total_reward,
        concrete_step_count=len(step_rows),
        controller_event_count=len(control_rows),
        terminated=adapter.terminated,
        truncated=truncated,
        final_state=final_state,
    )
    return OneThirdEpisodeTrace(
        episode_row=episode_row,
        step_rows=tuple(step_rows),
        control_rows=tuple(control_rows),
        lift_rows=tuple(lift_rows),
        abc_selection_rows=tuple(abc_selection_rows),
        abc_tier_signal_rows=tuple(abc_tier_signal_rows),
    )


def _write_one_third_artifacts(
    *,
    spec: CounterpointInstanceSpec,
    build: CounterpointTowerBuildResult,
    artifact_root: Path | str,
    run_id: str,
    schema_seed: int,
    linearization_mode_id: str,
    seed_bundle: SeedBundle,
    budget: dict[str, Any],
    recorder: TimingRecorder,
    episodes: tuple[OneThirdEpisodeTrace, ...],
    max_action_count: int,
    started_at: str,
    ended_at: str,
) -> BenchmarkRunResult:
    family_paths = build_run_family_paths(artifact_root, EVALUATION_RUN_FAMILY_ID)
    run_paths = build_run_paths(artifact_root, EVALUATION_RUN_FAMILY_ID, run_id)
    ensure_artifact_dirs(family_paths, run_paths)
    mode_contract = require_runnable_mode(DEFAULT_MODE_ID)
    dependency_state = collect_state_collapser_dependency_state(
        dependency_spec=STATE_COLLAPSER_DEPENDENCY_SPEC,
    )
    linearization_payload = build_linearization_artifact_payload(
        linearization_mode_id=linearization_mode_id,
        recorder=recorder,
        tower=build.tower,
        max_action_count=max_action_count,
        metadata={
            "runner": "counterpoint_one_third_diagnostics",
            "evaluation_id": EVALUATION_ID,
            "environment_instance_id": spec.environment_instance_id,
            "mode_id": DEFAULT_MODE_ID,
            "schema_id": DEFAULT_SCHEMA_ID,
        },
    )
    schema = build_schema_for_id(build.graph, schema_id=DEFAULT_SCHEMA_ID, schema_seed=schema_seed)
    schema_block_rows = _schema_block_summary_rows(
        build=build,
        schema_seed=schema_seed,
        run_id=run_id,
        replicate_index=seed_bundle.replicate_index,
    )
    tower_shape_rows = _tower_shape_summary_rows(
        build=build,
        schema_seed=schema_seed,
        run_id=run_id,
        replicate_index=seed_bundle.replicate_index,
    )

    write_json(
        family_paths.family_manifest,
        FamilyManifest(
            run_family_id=EVALUATION_RUN_FAMILY_ID,
            description="Counterpoint one-third schema tower diagnostics run family.",
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
            mode_id=DEFAULT_MODE_ID,
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
    write_json(run_paths.root / "schema_construction.json", schema.to_dict())
    write_json(
        run_paths.root / "quotient_summary.json",
        {
            "evaluation_id": EVALUATION_ID,
            "schema_id": schema.spec.schema_id,
            "schema_seed": schema_seed,
            "partition_tier_count": len(build.tower.state_layers),
            "state_cell_count_by_tier": [
                len(layer.all_cell_ids()) for layer in build.tower.state_layers
            ],
            "action_cell_count_by_tier": [
                _action_cell_count(layer) for layer in build.tower.action_layers
            ],
            "edge_count": len(build.graph.edges),
            "schema_block_summary": [
                row.to_flat_dict() for row in schema_block_rows
            ],
            "tower_shape_summary": [
                row.to_flat_dict() for row in tower_shape_rows
            ],
        },
    )
    write_json(
        run_paths.root / "tower_invariant_report.json",
        counterpoint_tower_invariant_artifact_payload(build),
    )

    write_csv(
        run_paths.episodes_csv,
        [episode.episode_row.to_flat_dict() for episode in episodes],
        OneThirdEpisodeRow.fieldnames(),
        create_parents=True,
    )
    write_csv(
        run_paths.step_events_csv,
        [
            row.to_flat_dict()
            for episode in episodes
            for row in episode.step_rows
        ],
        OneThirdStepRow.fieldnames(),
        create_parents=True,
    )
    write_csv(
        run_paths.control_events_csv,
        [
            row.to_flat_dict()
            for episode in episodes
            for row in episode.control_rows
        ],
        OneThirdControlEventRow.fieldnames(),
        create_parents=True,
    )
    write_csv(
        run_paths.root / "lift_fiber_events.csv",
        [
            row.to_flat_dict()
            for episode in episodes
            for row in episode.lift_rows
        ],
        OneThirdLiftFiberEventRow.fieldnames(),
        create_parents=True,
    )
    write_csv(
        run_paths.root / "abc_selection_events.csv",
        [
            row.to_flat_dict()
            for episode in episodes
            for row in episode.abc_selection_rows
        ],
        ABCSelectionEventRow.fieldnames(),
        create_parents=True,
    )
    write_csv(
        run_paths.root / "abc_tier_signal_events.csv",
        [
            row.to_flat_dict()
            for episode in episodes
            for row in episode.abc_tier_signal_rows
        ],
        ABCTierSignalEventRow.fieldnames(),
        create_parents=True,
    )
    write_csv(
        run_paths.timing_segments_csv,
        [row.to_flat_dict() for row in recorder.rows],
        recorder.rows[0].fieldnames() if recorder.rows else (),
        create_parents=True,
    )
    write_json(run_paths.timing_summary, summarize_timing_segments(recorder.rows))
    write_json(
        run_paths.run_manifest,
        RunManifest(
            run_id=run_id,
            run_family_id=EVALUATION_RUN_FAMILY_ID,
            environment_id=spec.environment_instance_id,
            mode_id=DEFAULT_MODE_ID,
            linearization_mode_id=linearization_mode_id,
            linearization_benchmark_label=linearization_payload.report.benchmark_label,
            linearization_enabled=linearization_payload.report.enabled,
            schema_id=DEFAULT_SCHEMA_ID,
            learner_id=mode_contract.learner_id,
            controller_id=mode_contract.controller_regime,
            seed_bundle_id=seed_bundle.seed_bundle_id,
            budget=budget,
            diagnostic_profile=mode_contract.diagnostic_profile.profile_id,
            timing_profile=mode_contract.timing_profile.profile_id,
            command=(
                "python -m big_boy_benchmarking.cli counterpoint "
                "one-third-diagnostics run"
            ),
            status="success",
        ).to_dict(),
        create_parents=True,
    )
    append_jsonl(
        family_paths.run_index,
        {
            "run_family_id": EVALUATION_RUN_FAMILY_ID,
            "run_id": run_id,
            "environment_id": spec.environment_instance_id,
            "mode_id": DEFAULT_MODE_ID,
            "status": "success",
            "started_at": started_at,
            "ended_at": ended_at,
            "artifact_schema_version": ARTIFACT_SCHEMA_VERSION,
        },
        create_parents=True,
    )
    run_paths.warnings_jsonl.touch()
    mean_return = (
        sum(episode.episode_row.total_reward for episode in episodes) / len(episodes)
        if episodes
        else 0.0
    )
    summary = {
        "evaluation_id": EVALUATION_ID,
        "run_family_id": EVALUATION_RUN_FAMILY_ID,
        "run_id": run_id,
        "environment_instance_id": spec.environment_instance_id,
        "mode_id": DEFAULT_MODE_ID,
        "schema_id": DEFAULT_SCHEMA_ID,
        "schema_seed": schema_seed,
        "linearization_mode_id": linearization_mode_id,
        "linearization_benchmark_label": linearization_payload.report.benchmark_label,
        "episode_count": len(episodes),
        "mean_return": mean_return,
        "concrete_step_count": sum(
            episode.episode_row.concrete_step_count for episode in episodes
        ),
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
            "abc_selection_events_csv": str(run_paths.root / "abc_selection_events.csv"),
            "abc_tier_signal_events_csv": str(run_paths.root / "abc_tier_signal_events.csv"),
            "schema_manifest": str(run_paths.root / "schema_manifest.json"),
            "schema_construction": str(run_paths.root / "schema_construction.json"),
            "quotient_summary": str(run_paths.root / "quotient_summary.json"),
            "tower_invariant_report": str(run_paths.root / "tower_invariant_report.json"),
        },
        summary_path=str(family_paths.summary_json),
        warning_count=0,
        started_at=started_at,
        ended_at=ended_at,
        failure_reason=None,
    )


def _run_index_row(
    source_evaluation_root: Path,
    artifact_root: Path,
    record: OneThirdRunRecord,
) -> OneThirdEvaluationRunIndexRow:
    result = record.result
    return OneThirdEvaluationRunIndexRow(
        evaluation_id=EVALUATION_ID,
        run_id="" if result is None else result.run_id,
        instance_id=record.instance_id,
        schema_id=DEFAULT_SCHEMA_ID,
        schema_seed=record.schema_seed,
        seed_bundle_id=record.seed_bundle.seed_bundle_id,
        replicate_index=record.seed_bundle.replicate_index,
        status=record.status,
        artifact_root=str(artifact_root),
        started_at="" if result is None else result.started_at,
        ended_at=None if result is None else result.ended_at,
        failure_reason=record.failure_reason,
    )


def _tier_signal_snapshot(
    *,
    tier_index: int,
    signals_by_tier: dict[int, TierSignalState],
    tier_configs: dict[int, TierControlConfig],
    tier_is_executable: Callable[[int], bool] | None,
) -> ABCTierSignalSnapshot:
    signal = signals_by_tier.get(tier_index, TierSignalState())
    config = tier_configs[tier_index]
    pressure = productive_learning_pressure(signal, config)
    return ABCTierSignalSnapshot(
        tier_index=tier_index,
        executable=_tier_executable(tier_index, tier_is_executable),
        visit_count=signal.visit_count,
        td_error_ema=signal.td_error_ema,
        success_count=signal.success_count,
        failure_count=signal.failure_count,
        success_rate=signal.success_rate,
        reward_residual_ema=signal.reward_residual_ema,
        has_reward_residual=signal.has_reward_residual,
        pressure=pressure,
        unclosed=is_unclosed(signal, config),
    )


def _tier_executable(
    tier_index: int,
    tier_is_executable: Callable[[int], bool] | None,
) -> bool:
    if tier_is_executable is None:
        return True
    return tier_is_executable(tier_index)


def _abc_selection_row(
    *,
    snapshot: ABCDecisionSnapshot,
    run_id: str,
    instance_id: str,
    schema_seed: int,
    seed_bundle: SeedBundle,
    episode_index: int,
    controller_event_index: int,
    active_tier_after: int | None,
    concrete_step_emitted: bool,
    lift_attempt_emitted: bool,
    lift_success: bool | None,
    control_action: str,
) -> ABCSelectionEventRow:
    action_consistent = _action_consistent(
        movement=snapshot.predicted_movement_direction,
        control_action=control_action,
    )
    blocked_reason = None
    if snapshot.selected_tier is None:
        blocked_reason = "no_executable_unclosed"
    elif snapshot.selected_tier_executable is False:
        blocked_reason = "selected_tier_non_executable"
    if control_action == "no_available_action":
        blocked_reason = "no_available_action"
    if lift_attempt_emitted and lift_success is False:
        blocked_reason = "lift_failure"
    if not action_consistent:
        blocked_reason = "abc_prediction_mismatch"
    return ABCSelectionEventRow(
        evaluation_id=EVALUATION_ID,
        run_id=run_id,
        instance_id=instance_id,
        schema_id=DEFAULT_SCHEMA_ID,
        schema_seed=schema_seed,
        seed_bundle_id=seed_bundle.seed_bundle_id,
        replicate_index=seed_bundle.replicate_index,
        episode_index=episode_index,
        controller_event_index=controller_event_index,
        active_tier_before=snapshot.active_tier_before,
        active_tier_after=active_tier_after,
        deepest_known_tier=snapshot.deepest_known_tier,
        selected_tier=snapshot.selected_tier,
        selected_tier_executable=snapshot.selected_tier_executable,
        predicted_movement_direction=snapshot.predicted_movement_direction,
        control_action=control_action,
        decision_pressure=snapshot.decision_pressure,
        training_due=snapshot.training_due,
        action_consistent=action_consistent,
        blocked_reason=blocked_reason,
        concrete_step_emitted=concrete_step_emitted,
        lift_attempt_emitted=lift_attempt_emitted,
    )


def _abc_tier_signal_rows(
    *,
    snapshot: ABCDecisionSnapshot,
    run_id: str,
    instance_id: str,
    schema_seed: int,
    seed_bundle: SeedBundle,
    episode_index: int,
    controller_event_index: int,
    liftability_counts_by_tier: dict[int, tuple[int, int]],
) -> tuple[ABCTierSignalEventRow, ...]:
    return tuple(
        ABCTierSignalEventRow(
            evaluation_id=EVALUATION_ID,
            run_id=run_id,
            instance_id=instance_id,
            schema_id=DEFAULT_SCHEMA_ID,
            schema_seed=schema_seed,
            seed_bundle_id=seed_bundle.seed_bundle_id,
            replicate_index=seed_bundle.replicate_index,
            episode_index=episode_index,
            controller_event_index=controller_event_index,
            active_tier_before=snapshot.active_tier_before,
            selected_tier=snapshot.selected_tier,
            tier_index=tier_signal.tier_index,
            executable=tier_signal.executable,
            visit_count=tier_signal.visit_count,
            td_error_ema=tier_signal.td_error_ema,
            success_count=tier_signal.success_count,
            failure_count=tier_signal.failure_count,
            success_rate=tier_signal.success_rate,
            reward_residual_ema=tier_signal.reward_residual_ema,
            has_reward_residual=tier_signal.has_reward_residual,
            productive_learning_pressure=tier_signal.pressure,
            unclosed=tier_signal.unclosed,
            selected=tier_signal.tier_index == snapshot.selected_tier,
            active=tier_signal.tier_index == snapshot.active_tier_before,
            liftability_semantics_id=(
                STATE_COLLAPSER_V072_POINTWISE_LIFTABILITY_SEMANTICS_ID
            ),
            executable_semantics="pointwise_current_base_state",
            quotient_action_cell_count=liftability_counts_by_tier.get(
                tier_signal.tier_index,
                (0, 0),
            )[0],
            pointwise_executable_action_cell_count=liftability_counts_by_tier.get(
                tier_signal.tier_index,
                (0, 0),
            )[1],
        )
        for tier_signal in snapshot.tier_signals
    )


def _liftability_counts_by_tier(
    adapter: CounterpointTowerControlAdapter,
) -> dict[int, tuple[int, int]]:
    return {
        tier: (
            adapter.quotient_action_cell_count(tier),
            adapter.pointwise_executable_action_cell_count(tier),
        )
        for tier in range(adapter.tower_depth)
    }


def _action_consistent(*, movement: str, control_action: str) -> bool:
    if movement == "lift":
        return control_action == "lift"
    if movement == "descend":
        return control_action == "descend"
    if movement in {"at_selected", "no_executable_unclosed"}:
        return control_action not in {"lift", "descend"}
    return False


def _schema_block_summary_rows(
    *,
    build: CounterpointTowerBuildResult,
    schema_seed: int,
    run_id: str,
    replicate_index: int,
) -> tuple[SchemaBlockSummaryRow, ...]:
    schema = build_schema_for_id(build.graph, schema_id=DEFAULT_SCHEMA_ID, schema_seed=schema_seed)
    del run_id, replicate_index
    counts = Counter(schema.edge_partition.values())
    source_counts: dict[str, Counter[str]] = defaultdict(Counter)
    for edge in build.graph.edges:
        block_id = schema.edge_partition[edge_key(edge)]
        source_counts[state_key(edge.source)][block_id] += 1
    total_edges = max(1, len(build.graph.edges))
    rows: list[SchemaBlockSummaryRow] = []
    for block_id in sorted(counts):
        local_counts = [
            source_counter[block_id]
            for source_counter in source_counts.values()
            if source_counter[block_id] > 0
        ]
        rows.append(
            SchemaBlockSummaryRow(
                evaluation_id=EVALUATION_ID,
                instance_id=build.graph.spec.environment_instance_id,
                schema_id=DEFAULT_SCHEMA_ID,
                schema_seed=schema_seed,
                block_id=block_id,
                scheduled_edge_count=counts[block_id],
                scheduled_edge_share=counts[block_id] / total_edges,
                source_count_with_block=len(local_counts),
                mean_source_local_edge_count=statistics.mean(local_counts)
                if local_counts
                else None,
                construction_rule="seeded_source_local_recursive_ceil_one_third",
            )
        )
    return tuple(rows)


def _tower_shape_summary_rows(
    *,
    build: CounterpointTowerBuildResult,
    schema_seed: int,
    run_id: str,
    replicate_index: int,
) -> tuple[TowerShapeSummaryRow, ...]:
    base_state_count = max(1, len(build.graph.states))
    base_edge_count = len(build.graph.edges)
    rows: list[TowerShapeSummaryRow] = []
    for tier_index, state_layer in enumerate(build.tower.state_layers):
        cell_ids = tuple(state_layer.all_cell_ids())
        member_counts = [len(state_layer.members(cell_id)) for cell_id in cell_ids]
        state_cell_count = len(cell_ids)
        largest_share = max(member_counts, default=0) / base_state_count
        singleton_share = sum(count for count in member_counts if count == 1) / base_state_count
        action_cell_count = (
            _action_cell_count(build.tower.action_layers[tier_index])
            if tier_index < len(build.tower.action_layers)
            else 0
        )
        rows.append(
            TowerShapeSummaryRow(
                evaluation_id=EVALUATION_ID,
                run_id=run_id,
                instance_id=build.graph.spec.environment_instance_id,
                schema_id=DEFAULT_SCHEMA_ID,
                schema_seed=schema_seed,
                replicate_index=replicate_index,
                tier_index=tier_index,
                state_cell_count=state_cell_count,
                action_cell_count=action_cell_count,
                base_state_count=base_state_count,
                base_edge_count=base_edge_count,
                state_compression_ratio=state_cell_count / base_state_count,
                largest_state_fiber_share=largest_share,
                singleton_state_fiber_share=singleton_share,
                degeneracy_class=_degeneracy_class(
                    tier_index=tier_index,
                    largest_share=largest_share,
                    state_cell_count=state_cell_count,
                    base_state_count=base_state_count,
                ),
                liftability_semantics_id=(
                    STATE_COLLAPSER_V072_POINTWISE_LIFTABILITY_SEMANTICS_ID
                ),
                executable_semantics="static_quotient_action_storage_not_pointwise",
                raw_action_cell_storage_count=action_cell_count,
            )
        )
    return tuple(rows)


def _action_cell_count(action_layer: object) -> int:
    action_cells = getattr(action_layer, "edge_ids_by_action_cell", {})
    return len(action_cells)


def _degeneracy_class(
    *,
    tier_index: int,
    largest_share: float,
    state_cell_count: int,
    base_state_count: int,
) -> str:
    if tier_index == 0 or state_cell_count == base_state_count:
        return "identity_or_base"
    if largest_share >= 1.0:
        return "full_collapse"
    if largest_share >= NEAR_FULL_COLLAPSE_THRESHOLD:
        return "near_full_collapse"
    return "compressed"


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


def _now() -> str:
    return datetime.now(UTC).isoformat()
