"""Runner for counterpoint contraction fraction sweep diagnostics."""

from __future__ import annotations

import json
import statistics
from collections import Counter
from dataclasses import dataclass
from datetime import UTC, datetime
from pathlib import Path
from typing import Any

from state_collapser.tower.control import FrozenLowerContext
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
from big_boy_benchmarking.environments.counterpoint.fraction_sweep_diagnostics.config import (
    DEFAULT_DENOMINATOR,
    DEFAULT_EPISODES_PER_REPLICATE,
    DEFAULT_INSTANCE_IDS,
    DEFAULT_LINEARIZATION_MODE_ID,
    DEFAULT_MODE_ID,
    DEFAULT_NUMERATORS,
    DEFAULT_REPLICATES_PER_SCHEMA_SEED,
    DEFAULT_SCHEMA_SEEDS,
    EVALUATION_ID,
    EVALUATION_RUN_FAMILY_ID,
    NEAR_FULL_COLLAPSE_THRESHOLD,
    NO_CONTRACTION_ARM_ID,
    FractionSweepDiagnosticsBudget,
    fraction_arm_id,
)
from big_boy_benchmarking.environments.counterpoint.fraction_sweep_diagnostics.events import (
    EndpointCoalescenceSummaryRow,
    FractionSweepABCSelectionEventRow,
    FractionSweepABCTierSignalEventRow,
    FractionSweepControlEventRow,
    FractionSweepEpisodeRow,
    FractionSweepEvaluationRunIndexRow,
    FractionSweepLiftFiberEventRow,
    FractionSweepStepRow,
    FractionSweepTowerShapeSummaryRow,
    LegacyOneThirdEquivalenceSummaryRow,
    SchemaFractionSummaryRow,
)
from big_boy_benchmarking.environments.counterpoint.fraction_sweep_diagnostics.manifests import (
    budget_lock_payload,
    evaluation_arm_manifest_payload,
    evaluation_manifest_payload,
)
from big_boy_benchmarking.environments.counterpoint.fraction_sweep_diagnostics.paths import (
    build_fraction_sweep_diagnostics_paths,
    validate_repo_resident_artifact_root,
)
from big_boy_benchmarking.environments.counterpoint.graph import (
    GraphEdge,
    enumerate_reachable_graph,
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
from big_boy_benchmarking.environments.counterpoint.one_third_diagnostics.runner import (
    DiagnosticActiveTierController,
)
from big_boy_benchmarking.environments.counterpoint.schemas import (
    build_empty_schema,
    build_outgoing_fraction_schema,
    edge_key,
    fraction_selection_monotonicity_report,
    legacy_one_third_equivalence_report,
    selected_fraction_edge_keys,
    source_local_fraction_selections,
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
    build_counterpoint_fraction_partition_tower,
    build_counterpoint_partition_tower,
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
class FractionArm:
    arm_id: str
    numerator: int
    denominator: int
    no_contraction: bool = False

    @property
    def schema_id(self) -> str:
        if self.no_contraction:
            return ids.EMPTY_SCHEMA_ID
        return f"{ids.OUTGOING_FRACTION_SWEEP_SCHEMA_ID}_{self.arm_id}"


@dataclass(frozen=True)
class FractionSweepEpisodeTrace:
    episode_row: FractionSweepEpisodeRow
    step_rows: tuple[FractionSweepStepRow, ...]
    control_rows: tuple[FractionSweepControlEventRow, ...]
    lift_rows: tuple[FractionSweepLiftFiberEventRow, ...]
    abc_selection_rows: tuple[FractionSweepABCSelectionEventRow, ...]
    abc_tier_signal_rows: tuple[FractionSweepABCTierSignalEventRow, ...]


@dataclass(frozen=True)
class FractionSweepRunRecord:
    instance_id: str
    arm: FractionArm
    schema_seed: int
    seed_bundle: SeedBundle
    result: BenchmarkRunResult | None
    status: str
    failure_reason: str | None = None


def fraction_sweep_spec_for_instance(instance_id: str) -> CounterpointInstanceSpec:
    if instance_id == "small" or instance_id == SMALL_INSTANCE_ID:
        return default_small_spec()
    if instance_id == "medium" or instance_id == MEDIUM_INSTANCE_ID:
        return default_medium_spec()
    if instance_id == "tiny" or instance_id.endswith("_tiny_v001"):
        raise ValueError("tiny is not part of fraction sweep diagnostics")
    raise ValueError(f"unknown counterpoint fraction sweep instance: {instance_id}")


def run_fraction_sweep_diagnostics(
    *,
    artifact_root: Path | str,
    instance_ids: tuple[str, ...] = DEFAULT_INSTANCE_IDS,
    numerators: tuple[int, ...] = DEFAULT_NUMERATORS,
    denominator: int = DEFAULT_DENOMINATOR,
    include_no_contraction_control: bool = True,
    schema_seeds: tuple[int, ...] = DEFAULT_SCHEMA_SEEDS,
    replicates_per_schema_seed: int = DEFAULT_REPLICATES_PER_SCHEMA_SEED,
    episodes_per_replicate: int = DEFAULT_EPISODES_PER_REPLICATE,
    base_seed: int = 0,
    locked_by: str = "cli",
    horizon_override: int | None = None,
    controller_event_ceiling: int | None = None,
    linearization_mode_id: str = DEFAULT_LINEARIZATION_MODE_ID,
) -> dict[str, Any]:
    artifact_root = validate_repo_resident_artifact_root(artifact_root)
    specs = tuple(fraction_sweep_spec_for_instance(item) for item in instance_ids)
    budget = FractionSweepDiagnosticsBudget(
        instance_ids=tuple(spec.environment_instance_id for spec in specs),
        numerators=numerators,
        denominator=denominator,
        include_no_contraction_control=include_no_contraction_control,
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
    paths = build_fraction_sweep_diagnostics_paths(artifact_root)
    paths.root.mkdir(parents=True, exist_ok=True)
    paths.results_dir.mkdir(parents=True, exist_ok=True)
    write_json(paths.evaluation_manifest, evaluation_manifest_payload(budget=budget))
    write_json(paths.evaluation_arm_manifest, evaluation_arm_manifest_payload(budget=budget))
    write_json(paths.evaluation_budget_lock, budget_lock_payload(budget=budget))

    seed_bundles = generate_seed_bundles(
        base_seed=base_seed,
        replicate_count=replicates_per_schema_seed,
    )
    arms = _arms_from_budget(budget)
    _validate_fraction_design_locks(specs=specs, budget=budget)
    records: list[FractionSweepRunRecord] = []
    for spec in specs:
        horizon = horizon_override or spec.horizon_steps
        for arm in arms:
            for schema_seed in schema_seeds:
                for seed_bundle in seed_bundles:
                    try:
                        result = run_fraction_sweep_diagnostic_run(
                            spec=spec,
                            arm=arm,
                            schema_seed=schema_seed,
                            seed_bundle=seed_bundle,
                            artifact_root=artifact_root,
                            episode_count=episodes_per_replicate,
                            horizon=horizon,
                            max_controller_events=budget.max_controller_events(horizon),
                            linearization_mode_id=linearization_mode_id,
                        )
                        records.append(
                            FractionSweepRunRecord(
                                instance_id=spec.environment_instance_id,
                                arm=arm,
                                schema_seed=schema_seed,
                                seed_bundle=seed_bundle,
                                result=result,
                                status=result.status,
                            )
                        )
                    except Exception as exc:  # pragma: no cover - failure recording boundary
                        records.append(
                            FractionSweepRunRecord(
                                instance_id=spec.environment_instance_id,
                                arm=arm,
                                schema_seed=schema_seed,
                                seed_bundle=seed_bundle,
                                result=None,
                                status="failed",
                                failure_reason=f"{type(exc).__name__}: {exc}",
                            )
                        )
    write_csv(
        paths.evaluation_run_index_csv,
        [_run_index_row(artifact_root, record).to_flat_dict() for record in records],
        FractionSweepEvaluationRunIndexRow.fieldnames(),
    )
    status = "complete" if all(record.status == "success" for record in records) else "incomplete"
    return {
        "status": status,
        "evaluation_id": EVALUATION_ID,
        "run_count": len(records),
        "evaluation_run_index": str(paths.evaluation_run_index_csv),
        "evaluation_budget_lock": str(paths.evaluation_budget_lock),
    }


def _validate_fraction_design_locks(
    *,
    specs: tuple[CounterpointInstanceSpec, ...],
    budget: FractionSweepDiagnosticsBudget,
) -> None:
    for spec in specs:
        graph = enumerate_reachable_graph(spec)
        for schema_seed in budget.schema_seeds:
            monotonicity_rows = fraction_selection_monotonicity_report(
                graph,
                numerators=budget.numerators,
                denominator=budget.denominator,
                schema_seed=schema_seed,
            )
            failed_monotonicity = [
                row for row in monotonicity_rows if not bool(row["subset_pass"])
            ]
            if failed_monotonicity:
                raise ValueError(
                    "fraction sweep selected-edge sets are not nested: "
                    f"{failed_monotonicity[0]}"
                )
            if 6 in budget.numerators and budget.denominator == 18:
                report = legacy_one_third_equivalence_report(
                    graph,
                    numerator=6,
                    denominator=18,
                    schema_seed=schema_seed,
                )
                if not bool(report["equivalent"]):
                    raise ValueError(
                        "fraction sweep n06_over_18 does not match old one-third "
                        f"first block: {report}"
                    )


def run_fraction_sweep_diagnostic_run(
    *,
    spec: CounterpointInstanceSpec,
    arm: FractionArm,
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
            "fraction sweep diagnostics use tensor_available_disabled; "
            f"reserved linearization mode rejected: {linearization_mode_id}"
        )
    if horizon <= 0:
        raise ValueError("horizon must be positive")
    if episode_count <= 0:
        raise ValueError("episode_count must be positive")
    config = ExploitExploreControllerConfig() if controller_config is None else controller_config
    learner_cfg = TabularQLearnerConfig() if learner_config is None else learner_config
    run_id = (
        f"{spec.environment_instance_id}-{arm.arm_id}-schema{schema_seed}-"
        f"rep{seed_bundle.replicate_index}"
    )
    started_at = _now()
    recorder = TimingRecorder.create(run_id)
    with recorder.segment("tower_reset"):
        build = _build_tower_for_arm(spec=spec, arm=arm, schema_seed=schema_seed)
    adapter = CounterpointTowerControlAdapter(
        spec=spec,
        schema_id=arm.schema_id,
        schema_seed=schema_seed,
        recorder=recorder,
        build_result=build,
    )
    episodes = tuple(
        _run_fraction_sweep_episode(
            adapter=adapter,
            arm=arm,
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
    return _write_fraction_sweep_artifacts(
        spec=spec,
        arm=arm,
        build=build,
        artifact_root=artifact_root,
        run_id=run_id,
        schema_seed=schema_seed,
        linearization_mode_id=linearization_mode_id,
        seed_bundle=seed_bundle,
        budget={
            "episodes": episode_count,
            "horizon": horizon,
            "arm_id": arm.arm_id,
            "numerator": arm.numerator,
            "denominator": arm.denominator,
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


def _run_fraction_sweep_episode(
    *,
    adapter: CounterpointTowerControlAdapter,
    arm: FractionArm,
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
) -> FractionSweepEpisodeTrace:
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
                metadata={"schema_id": adapter.schema_id, "arm_id": arm.arm_id},
            )
            for tier in range(adapter.tower_depth)
        },
        move_down=adapter.move_down,
        move_up=adapter.move_up,
        tier_is_executable=adapter.tier_is_executable,
    )
    step_rows: list[FractionSweepStepRow] = []
    control_rows: list[FractionSweepControlEventRow] = []
    lift_rows: list[FractionSweepLiftFiberEventRow] = []
    abc_selection_rows: list[FractionSweepABCSelectionEventRow] = []
    abc_tier_signal_rows: list[FractionSweepABCTierSignalEventRow] = []
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
            FractionSweepControlEventRow(
                evaluation_id=EVALUATION_ID,
                run_id=run_id,
                instance_id=instance_id,
                arm_id=arm.arm_id,
                numerator=arm.numerator,
                denominator=arm.denominator,
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
                FractionSweepLiftFiberEventRow(
                    evaluation_id=EVALUATION_ID,
                    run_id=run_id,
                    instance_id=instance_id,
                    arm_id=arm.arm_id,
                    numerator=arm.numerator,
                    denominator=arm.denominator,
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
                    arm=arm,
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
                    arm=arm,
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
                FractionSweepStepRow(
                    evaluation_id=EVALUATION_ID,
                    run_id=run_id,
                    instance_id=instance_id,
                    arm_id=arm.arm_id,
                    numerator=arm.numerator,
                    denominator=arm.denominator,
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
    episode_row = FractionSweepEpisodeRow(
        evaluation_id=EVALUATION_ID,
        run_id=run_id,
        instance_id=instance_id,
        arm_id=arm.arm_id,
        numerator=arm.numerator,
        denominator=arm.denominator,
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
    return FractionSweepEpisodeTrace(
        episode_row=episode_row,
        step_rows=tuple(step_rows),
        control_rows=tuple(control_rows),
        lift_rows=tuple(lift_rows),
        abc_selection_rows=tuple(abc_selection_rows),
        abc_tier_signal_rows=tuple(abc_tier_signal_rows),
    )


def _write_fraction_sweep_artifacts(
    *,
    spec: CounterpointInstanceSpec,
    arm: FractionArm,
    build: CounterpointTowerBuildResult,
    artifact_root: Path | str,
    run_id: str,
    schema_seed: int,
    linearization_mode_id: str,
    seed_bundle: SeedBundle,
    budget: dict[str, Any],
    recorder: TimingRecorder,
    episodes: tuple[FractionSweepEpisodeTrace, ...],
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
            "runner": "counterpoint_fraction_sweep_diagnostics",
            "evaluation_id": EVALUATION_ID,
            "environment_instance_id": spec.environment_instance_id,
            "mode_id": DEFAULT_MODE_ID,
            "schema_id": arm.schema_id,
            "arm_id": arm.arm_id,
        },
    )
    schema = (
        build_empty_schema(build.graph)
        if arm.no_contraction
        else build_outgoing_fraction_schema(
            build.graph,
            schema_seed=schema_seed,
            numerator=arm.numerator,
            denominator=arm.denominator,
        )
    )
    schema_fraction_rows = _schema_fraction_summary_rows(
        build=build,
        arm=arm,
        schema_seed=schema_seed,
    )
    tower_shape_rows = _tower_shape_summary_rows(
        build=build,
        arm=arm,
        schema_seed=schema_seed,
        run_id=run_id,
        replicate_index=seed_bundle.replicate_index,
    )
    endpoint_rows = _endpoint_coalescence_rows(
        build=build,
        arm=arm,
        schema_seed=schema_seed,
        run_id=run_id,
        replicate_index=seed_bundle.replicate_index,
    )
    legacy_rows = _legacy_equivalence_rows(
        build=build,
        arm=arm,
        schema_seed=schema_seed,
    )

    write_json(
        family_paths.family_manifest,
        FamilyManifest(
            run_family_id=EVALUATION_RUN_FAMILY_ID,
            description="Counterpoint contraction fraction sweep diagnostics run family.",
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
            repo_state={
                "bbb_repo": "runtime_repository_root",
                "path_policy": "absolute local path omitted from portable artifact manifests",
            },
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
    write_json(run_paths.external_artifacts, ExternalArtifactsManifest(run_id=run_id).to_dict())
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
            "arm_id": arm.arm_id,
            "numerator": arm.numerator,
            "denominator": arm.denominator,
            "schema_seed": schema_seed,
            "partition_tier_count": len(build.tower.state_layers),
            "state_cell_count_by_tier": [
                len(layer.all_cell_ids()) for layer in build.tower.state_layers
            ],
            "active_action_cell_count_by_tier": [
                _active_action_cell_count(build.tower, tier)
                for tier in range(len(build.tower.state_layers))
            ],
            "raw_historical_action_cell_record_count_by_tier": [
                _raw_action_cell_count(layer) for layer in build.tower.action_layers
            ],
            "edge_count": len(build.graph.edges),
            "schema_fraction_summary": [
                row.to_flat_dict() for row in schema_fraction_rows
            ],
            "tower_shape_summary": [
                row.to_flat_dict() for row in tower_shape_rows
            ],
            "endpoint_coalescence_summary": [
                row.to_flat_dict() for row in endpoint_rows
            ],
            "legacy_one_third_equivalence_summary": [
                row.to_flat_dict() for row in legacy_rows
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
        FractionSweepEpisodeRow.fieldnames(),
        create_parents=True,
    )
    write_csv(
        run_paths.step_events_csv,
        [row.to_flat_dict() for episode in episodes for row in episode.step_rows],
        FractionSweepStepRow.fieldnames(),
        create_parents=True,
    )
    write_csv(
        run_paths.control_events_csv,
        [row.to_flat_dict() for episode in episodes for row in episode.control_rows],
        FractionSweepControlEventRow.fieldnames(),
        create_parents=True,
    )
    write_csv(
        run_paths.root / "lift_fiber_events.csv",
        [row.to_flat_dict() for episode in episodes for row in episode.lift_rows],
        FractionSweepLiftFiberEventRow.fieldnames(),
        create_parents=True,
    )
    write_csv(
        run_paths.root / "abc_selection_events.csv",
        [row.to_flat_dict() for episode in episodes for row in episode.abc_selection_rows],
        FractionSweepABCSelectionEventRow.fieldnames(),
        create_parents=True,
    )
    write_csv(
        run_paths.root / "abc_tier_signal_events.csv",
        [row.to_flat_dict() for episode in episodes for row in episode.abc_tier_signal_rows],
        FractionSweepABCTierSignalEventRow.fieldnames(),
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
            schema_id=arm.schema_id,
            learner_id=mode_contract.learner_id,
            controller_id=mode_contract.controller_regime,
            seed_bundle_id=seed_bundle.seed_bundle_id,
            budget=budget,
            diagnostic_profile=mode_contract.diagnostic_profile.profile_id,
            timing_profile=mode_contract.timing_profile.profile_id,
            command="python -m big_boy_benchmarking.cli counterpoint fraction-sweep run",
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
        "schema_id": arm.schema_id,
        "arm_id": arm.arm_id,
        "numerator": arm.numerator,
        "denominator": arm.denominator,
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


def _arms_from_budget(budget: FractionSweepDiagnosticsBudget) -> tuple[FractionArm, ...]:
    arms = [
        FractionArm(
            arm_id=fraction_arm_id(numerator, budget.denominator),
            numerator=numerator,
            denominator=budget.denominator,
        )
        for numerator in budget.numerators
    ]
    if budget.include_no_contraction_control:
        return (
            FractionArm(
                arm_id=NO_CONTRACTION_ARM_ID,
                numerator=0,
                denominator=budget.denominator,
                no_contraction=True,
            ),
            *arms,
        )
    return tuple(arms)


def _build_tower_for_arm(
    *,
    spec: CounterpointInstanceSpec,
    arm: FractionArm,
    schema_seed: int,
) -> CounterpointTowerBuildResult:
    if arm.no_contraction:
        return build_counterpoint_partition_tower(
            spec,
            schema_id=ids.EMPTY_SCHEMA_ID,
            schema_seed=None,
        )
    return build_counterpoint_fraction_partition_tower(
        spec,
        numerator=arm.numerator,
        denominator=arm.denominator,
        schema_seed=schema_seed,
    )


def _run_index_row(
    artifact_root: Path,
    record: FractionSweepRunRecord,
) -> FractionSweepEvaluationRunIndexRow:
    result = record.result
    return FractionSweepEvaluationRunIndexRow(
        evaluation_id=EVALUATION_ID,
        run_id="" if result is None else result.run_id,
        instance_id=record.instance_id,
        arm_id=record.arm.arm_id,
        numerator=record.arm.numerator,
        denominator=record.arm.denominator,
        schema_seed=record.schema_seed,
        seed_bundle_id=record.seed_bundle.seed_bundle_id,
        replicate_index=record.seed_bundle.replicate_index,
        status=record.status,
        artifact_root=str(artifact_root),
        started_at="" if result is None else result.started_at,
        ended_at=None if result is None else result.ended_at,
        failure_reason=record.failure_reason,
    )


def _abc_selection_row(
    *,
    snapshot,
    arm: FractionArm,
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
) -> FractionSweepABCSelectionEventRow:
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
    return FractionSweepABCSelectionEventRow(
        evaluation_id=EVALUATION_ID,
        run_id=run_id,
        instance_id=instance_id,
        arm_id=arm.arm_id,
        numerator=arm.numerator,
        denominator=arm.denominator,
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
    snapshot,
    arm: FractionArm,
    run_id: str,
    instance_id: str,
    schema_seed: int,
    seed_bundle: SeedBundle,
    episode_index: int,
    controller_event_index: int,
    liftability_counts_by_tier: dict[int, tuple[int, int]],
) -> tuple[FractionSweepABCTierSignalEventRow, ...]:
    return tuple(
        FractionSweepABCTierSignalEventRow(
            evaluation_id=EVALUATION_ID,
            run_id=run_id,
            instance_id=instance_id,
            arm_id=arm.arm_id,
            numerator=arm.numerator,
            denominator=arm.denominator,
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


def _schema_fraction_summary_rows(
    *,
    build: CounterpointTowerBuildResult,
    arm: FractionArm,
    schema_seed: int,
) -> tuple[SchemaFractionSummaryRow, ...]:
    if arm.no_contraction:
        return (
            SchemaFractionSummaryRow(
                evaluation_id=EVALUATION_ID,
                instance_id=build.graph.spec.environment_instance_id,
                arm_id=arm.arm_id,
                numerator=arm.numerator,
                denominator=arm.denominator,
                schema_seed=schema_seed,
                base_state_count=len(build.graph.states),
                base_edge_count=len(build.graph.edges),
                scheduled_edge_count=0,
                scheduled_edge_share=0.0,
                scheduled_edges_per_state_minus_one=0.0,
                source_count_with_scheduled_edges=0,
                min_selected_edges_per_source=None,
                mean_selected_edges_per_source=None,
                max_selected_edges_per_source=None,
                min_source_out_degree=None,
                mean_source_out_degree=None,
                max_source_out_degree=None,
                quota_rule_id="no_contraction_control",
                monotonicity_pass=None,
                construction_rule="identity_no_contraction",
            ),
        )
    selections = source_local_fraction_selections(
        build.graph,
        numerator=arm.numerator,
        denominator=arm.denominator,
        schema_seed=schema_seed,
    )
    selected_counts = [selection.selected_count for selection in selections]
    out_degrees = [selection.out_degree for selection in selections]
    total_selected = sum(selected_counts)
    monotonicity_rows = fraction_selection_monotonicity_report(
        build.graph,
        numerators=tuple(range(1, arm.numerator + 1)),
        denominator=arm.denominator,
        schema_seed=schema_seed,
    )
    monotonicity_pass = all(bool(row["subset_pass"]) for row in monotonicity_rows)
    denominator_for_ratio = max(1, len(build.graph.states) - 1)
    return (
        SchemaFractionSummaryRow(
            evaluation_id=EVALUATION_ID,
            instance_id=build.graph.spec.environment_instance_id,
            arm_id=arm.arm_id,
            numerator=arm.numerator,
            denominator=arm.denominator,
            schema_seed=schema_seed,
            base_state_count=len(build.graph.states),
            base_edge_count=len(build.graph.edges),
            scheduled_edge_count=total_selected,
            scheduled_edge_share=total_selected / max(1, len(build.graph.edges)),
            scheduled_edges_per_state_minus_one=total_selected / denominator_for_ratio,
            source_count_with_scheduled_edges=sum(count > 0 for count in selected_counts),
            min_selected_edges_per_source=min(selected_counts) if selected_counts else None,
            mean_selected_edges_per_source=statistics.mean(selected_counts)
            if selected_counts
            else None,
            max_selected_edges_per_source=max(selected_counts) if selected_counts else None,
            min_source_out_degree=min(out_degrees) if out_degrees else None,
            mean_source_out_degree=statistics.mean(out_degrees) if out_degrees else None,
            max_source_out_degree=max(out_degrees) if out_degrees else None,
            quota_rule_id="max_1_ceil_out_degree_times_n_over_18",
            monotonicity_pass=monotonicity_pass,
            construction_rule="seeded_source_local_single_block_fraction",
        ),
    )


def _tower_shape_summary_rows(
    *,
    build: CounterpointTowerBuildResult,
    arm: FractionArm,
    schema_seed: int,
    run_id: str,
    replicate_index: int,
) -> tuple[FractionSweepTowerShapeSummaryRow, ...]:
    base_state_count = max(1, len(build.graph.states))
    base_edge_count = len(build.graph.edges)
    rows: list[FractionSweepTowerShapeSummaryRow] = []
    for tier_index, state_layer in enumerate(build.tower.state_layers):
        cell_ids = tuple(state_layer.all_cell_ids())
        member_counts = [len(state_layer.members(cell_id)) for cell_id in cell_ids]
        histogram = Counter(member_counts)
        state_cell_count = len(cell_ids)
        largest_size = max(member_counts, default=0)
        largest_share = largest_size / base_state_count
        singleton_count = sum(1 for count in member_counts if count == 1)
        singleton_share = singleton_count / base_state_count
        full_collapse = tier_index > 0 and state_cell_count == 1
        near_collapse = (
            tier_index > 0
            and not full_collapse
            and largest_share >= NEAR_FULL_COLLAPSE_THRESHOLD
        )
        rows.append(
            FractionSweepTowerShapeSummaryRow(
                evaluation_id=EVALUATION_ID,
                run_id=run_id,
                instance_id=build.graph.spec.environment_instance_id,
                arm_id=arm.arm_id,
                numerator=arm.numerator,
                denominator=arm.denominator,
                schema_seed=schema_seed,
                replicate_index=replicate_index,
                tier_index=tier_index,
                state_cell_count=state_cell_count,
                active_action_cell_count=_active_action_cell_count(build.tower, tier_index),
                raw_historical_action_cell_record_count=_raw_action_cell_count(
                    build.tower.action_layers[tier_index]
                )
                if tier_index < len(build.tower.action_layers)
                else 0,
                base_state_count=base_state_count,
                base_edge_count=base_edge_count,
                state_compression_ratio=state_cell_count / base_state_count,
                largest_state_cell_size=largest_size,
                largest_state_cell_share=largest_share,
                singleton_state_cell_count=singleton_count,
                singleton_base_state_share=singleton_share,
                state_cell_size_histogram=json.dumps(dict(sorted(histogram.items()))),
                full_collapse=full_collapse,
                near_collapse=near_collapse,
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
                raw_action_cell_storage_count=_raw_action_cell_count(
                    build.tower.action_layers[tier_index]
                )
                if tier_index < len(build.tower.action_layers)
                else 0,
            )
        )
    return tuple(rows)


def _endpoint_coalescence_rows(
    *,
    build: CounterpointTowerBuildResult,
    arm: FractionArm,
    schema_seed: int,
    run_id: str,
    replicate_index: int,
) -> tuple[EndpointCoalescenceSummaryRow, ...]:
    if arm.no_contraction:
        processed_edges: tuple[GraphEdge, ...] = ()
    else:
        selected = selected_fraction_edge_keys(
            build.graph,
            numerator=arm.numerator,
            denominator=arm.denominator,
            schema_seed=schema_seed,
        )
        processed_edges = tuple(edge for edge in build.graph.edges if edge_key(edge) in selected)
    summary = _endpoint_coalescence_summary(build.graph.states, processed_edges)
    return (
        EndpointCoalescenceSummaryRow(
            evaluation_id=EVALUATION_ID,
            run_id=run_id,
            instance_id=build.graph.spec.environment_instance_id,
            arm_id=arm.arm_id,
            numerator=arm.numerator,
            denominator=arm.denominator,
            schema_seed=schema_seed,
            replicate_index=replicate_index,
            **summary,
        ),
    )


def _legacy_equivalence_rows(
    *,
    build: CounterpointTowerBuildResult,
    arm: FractionArm,
    schema_seed: int,
) -> tuple[LegacyOneThirdEquivalenceSummaryRow, ...]:
    if arm.no_contraction or arm.numerator != 6 or arm.denominator != 18:
        return ()
    report = legacy_one_third_equivalence_report(
        build.graph,
        numerator=arm.numerator,
        denominator=arm.denominator,
        schema_seed=schema_seed,
    )
    return (
        LegacyOneThirdEquivalenceSummaryRow(
            evaluation_id=EVALUATION_ID,
            instance_id=build.graph.spec.environment_instance_id,
            arm_id=arm.arm_id,
            numerator=arm.numerator,
            denominator=arm.denominator,
            schema_seed=schema_seed,
            equivalent=bool(report["equivalent"]),
            fraction_edge_count=int(report["fraction_edge_count"]),
            legacy_edge_count=int(report["legacy_edge_count"]),
            missing_from_fraction_count=int(report["missing_from_fraction_count"]),
            extra_in_fraction_count=int(report["extra_in_fraction_count"]),
            missing_from_fraction_examples=str(report["missing_from_fraction_examples"]),
            extra_in_fraction_examples=str(report["extra_in_fraction_examples"]),
        ),
    )


def _endpoint_coalescence_summary(
    states: tuple[object, ...],
    edges: tuple[GraphEdge, ...],
) -> dict[str, Any]:
    parent = {state_key(state): state_key(state) for state in states}
    size = {state_key(state): 1 for state in states}
    component_count = len(parent)
    useful = 0
    singleton_index: int | None = None

    def find(item: str) -> str:
        while parent[item] != item:
            parent[item] = parent[parent[item]]
            item = parent[item]
        return item

    def union(left: str, right: str) -> bool:
        nonlocal component_count
        left_root = find(left)
        right_root = find(right)
        if left_root == right_root:
            return False
        if size[left_root] < size[right_root]:
            left_root, right_root = right_root, left_root
        parent[right_root] = left_root
        size[left_root] += size[right_root]
        component_count -= 1
        return True

    for index, edge in enumerate(edges, start=1):
        if union(state_key(edge.source), state_key(edge.target)):
            useful += 1
        if component_count == 1 and singleton_index is None:
            singleton_index = index
    component_sizes = Counter(find(item) for item in parent)
    largest = max(component_sizes.values(), default=0)
    processed = len(edges)
    return {
        "processed_edge_count": processed,
        "useful_coalescence_count": useful,
        "redundant_or_internal_edge_count": processed - useful,
        "state_cell_count_after_block": len(component_sizes),
        "largest_coalesced_cell_size": largest,
        "largest_coalesced_cell_share": largest / max(1, len(states)),
        "processed_edge_index_at_first_singleton": singleton_index,
        "collapse_required_most_of_block": None
        if singleton_index is None or processed == 0
        else singleton_index >= processed / 2,
    }


def _active_action_cell_count(tower: object, tier_index: int) -> int:
    if tier_index >= len(tower.state_layers):
        return 0
    state_layer = tower.state_layers[tier_index]
    active_cells = set()
    for state_cell in state_layer.all_cell_ids():
        active_cells.update(tower.outgoing_action_cells(tier_index, state_cell))
    return len(active_cells)


def _raw_action_cell_count(action_layer: object) -> int:
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
