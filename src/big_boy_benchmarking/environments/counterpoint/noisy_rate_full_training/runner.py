"""Runner for noisy-rate full-tower training health diagnostics."""

from __future__ import annotations

import json
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
from big_boy_benchmarking.environments.counterpoint.liftability import (
    STATE_COLLAPSER_V072_POINTWISE_LIFTABILITY_SEMANTICS_ID,
)
from big_boy_benchmarking.environments.counterpoint.noisy_rate_diagnostics.runner import (
    noisy_rate_spec_for_instance,
)
from big_boy_benchmarking.environments.counterpoint.noisy_rate_full_training import (
    candidate_selection,
)
from big_boy_benchmarking.environments.counterpoint.noisy_rate_full_training.config import (
    DEFAULT_LINEARIZATION_MODE_ID,
    DEFAULT_MODE_ID,
    EVALUATION_ID,
    EVALUATION_RUN_FAMILY_ID,
    NoisyRateFullTrainingBudget,
)
from big_boy_benchmarking.environments.counterpoint.noisy_rate_full_training.events import (
    FullTrainingABCSelectionEventRow,
    FullTrainingABCTierSignalEventRow,
    FullTrainingControlEventRow,
    FullTrainingEpisodeRow,
    FullTrainingEvaluationRunIndexRow,
    FullTrainingLearnerUpdateEventRow,
    FullTrainingLiftFiberEventRow,
    FullTrainingStepRow,
    FullTrainingTowerShapeSummaryRow,
)
from big_boy_benchmarking.environments.counterpoint.noisy_rate_full_training.manifests import (
    budget_lock_payload,
    candidate_manifest_payload,
    evaluation_manifest_payload,
)
from big_boy_benchmarking.environments.counterpoint.noisy_rate_full_training.paths import (
    build_noisy_rate_full_training_paths,
    default_parent_candidate_readout_source,
    validate_repo_resident_artifact_root,
)
from big_boy_benchmarking.environments.counterpoint.one_third_diagnostics.runner import (
    DiagnosticActiveTierController,
)
from big_boy_benchmarking.environments.counterpoint.schemas import (
    build_noisy_rate_contraction_schema,
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
    build_counterpoint_noisy_rate_partition_tower,
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
class FullTrainingEpisodeTrace:
    episode_row: FullTrainingEpisodeRow
    step_rows: tuple[FullTrainingStepRow, ...]
    control_rows: tuple[FullTrainingControlEventRow, ...]
    lift_rows: tuple[FullTrainingLiftFiberEventRow, ...]
    abc_selection_rows: tuple[FullTrainingABCSelectionEventRow, ...]
    abc_tier_signal_rows: tuple[FullTrainingABCTierSignalEventRow, ...]
    learner_update_rows: tuple[FullTrainingLearnerUpdateEventRow, ...]


@dataclass(frozen=True)
class FullTrainingRunRecord:
    candidate: Any
    seed_bundle: SeedBundle
    result: BenchmarkRunResult | None
    status: str
    failure_reason: str | None = None


def run_noisy_rate_full_training(
    *,
    artifact_root: Path | str,
    parent_candidate_readout_source: Path | str | None = None,
    include_runtime_anchor: bool = False,
    candidate_cap: int | None = None,
    training_replicates_per_candidate: int = 4,
    episodes_per_replicate: int = 64,
    base_seed: int = 0,
    locked_by: str = "cli",
    horizon_override: int | None = None,
    controller_event_ceiling: int | None = None,
    linearization_mode_id: str = DEFAULT_LINEARIZATION_MODE_ID,
) -> dict[str, Any]:
    artifact_root = validate_repo_resident_artifact_root(artifact_root)
    parent_source = parent_candidate_readout_source or default_parent_candidate_readout_source()
    budget = NoisyRateFullTrainingBudget(
        parent_candidate_readout_source=parent_source,
        include_runtime_anchor=include_runtime_anchor,
        candidate_cap=candidate_cap,
        training_replicates_per_candidate=training_replicates_per_candidate,
        episodes_per_replicate=episodes_per_replicate,
        horizon_by_instance_id=None,
        controller_event_ceiling_override=controller_event_ceiling,
        linearization_mode_id=linearization_mode_id,
        base_seed=base_seed,
        locked_by=locked_by,
    )
    paths = build_noisy_rate_full_training_paths(artifact_root)
    paths.root.mkdir(parents=True, exist_ok=True)
    paths.results_dir.mkdir(parents=True, exist_ok=True)
    selection = candidate_selection.load_candidate_selection(
        budget.parent_candidate_readout_source,
        include_runtime_anchor=budget.include_runtime_anchor,
        candidate_cap=budget.candidate_cap,
    )
    write_json(paths.evaluation_manifest, evaluation_manifest_payload(budget=budget))
    write_json(paths.evaluation_budget_lock, budget_lock_payload(budget=budget))
    write_json(
        paths.candidate_manifest,
        candidate_manifest_payload(
            selected_candidates=[
                candidate_selection.candidate_to_manifest_dict(row)
                for row in selection.selected
            ],
            excluded_candidates=[
                candidate_selection.candidate_to_manifest_dict(row)
                for row in selection.excluded
            ],
            parent_readout_source=selection.parent_readout_source,
            parent_source_files=selection.parent_source_files,
            budget=budget,
        ),
    )

    seed_bundles = generate_seed_bundles(
        base_seed=base_seed,
        replicate_count=training_replicates_per_candidate,
    )
    records: list[FullTrainingRunRecord] = []
    for candidate in selection.selected:
        spec = noisy_rate_spec_for_instance(candidate.instance_id)
        horizon = horizon_override or spec.horizon_steps
        for seed_bundle in seed_bundles:
            try:
                result = run_noisy_rate_full_training_candidate(
                    spec=spec,
                    candidate=candidate,
                    seed_bundle=seed_bundle,
                    selection=selection,
                    artifact_root=artifact_root,
                    episode_count=episodes_per_replicate,
                    horizon=horizon,
                    max_controller_events=budget.max_controller_events(horizon),
                    linearization_mode_id=linearization_mode_id,
                )
                records.append(
                    FullTrainingRunRecord(
                        candidate=candidate,
                        seed_bundle=seed_bundle,
                        result=result,
                        status=result.status,
                    )
                )
            except Exception as exc:
                records.append(
                    FullTrainingRunRecord(
                        candidate=candidate,
                        seed_bundle=seed_bundle,
                        result=None,
                        status="failed",
                        failure_reason=f"{type(exc).__name__}: {exc}",
                    )
                )
    write_csv(
        paths.evaluation_run_index_csv,
        [_run_index_row(artifact_root, record).to_flat_dict() for record in records],
        FullTrainingEvaluationRunIndexRow.fieldnames(),
    )
    status = (
        "complete"
        if records and all(record.status == "success" for record in records)
        else "incomplete"
    )
    return {
        "status": status,
        "run_count": len(records),
        "evaluation_run_index": str(paths.evaluation_run_index_csv),
        "candidate_manifest": str(paths.candidate_manifest),
        "evaluation_budget_lock": str(paths.evaluation_budget_lock),
    }


def run_noisy_rate_full_training_candidate(
    *,
    spec: CounterpointInstanceSpec,
    candidate: Any,
    seed_bundle: SeedBundle,
    selection: candidate_selection.CandidateSelectionResult,
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
            "noisy-rate full-tower training uses tensor_available_disabled; "
            f"reserved linearization mode rejected: {linearization_mode_id}"
        )
    if episode_count <= 0:
        raise ValueError("episode_count must be positive")
    if horizon <= 0:
        raise ValueError("horizon must be positive")
    config = ExploitExploreControllerConfig() if controller_config is None else controller_config
    learner_cfg = TabularQLearnerConfig() if learner_config is None else learner_config
    run_id = f"{candidate.candidate_id}-trainrep{seed_bundle.replicate_index}"
    started_at = _now()
    recorder = TimingRecorder.create(run_id)
    with recorder.segment("tower_reset"):
        build = build_counterpoint_noisy_rate_partition_tower(
            spec,
            numerator=candidate.numerator,
            denominator=candidate.denominator,
            schema_seed=candidate.schema_seed,
            selector_rule_id=candidate.selector_rule_id,
        )
    _verify_candidate_tower(candidate, build)
    adapter = CounterpointTowerControlAdapter(
        spec=spec,
        schema_id=f"{ids.NOISY_RATE_CONTRACTION_SCHEMA_ID}_{candidate.arm_id}",
        schema_seed=candidate.schema_seed,
        recorder=recorder,
        build_result=build,
    )
    learner = CounterpointTierLearner(
        adapter=adapter,
        learner_config=learner_cfg,
        controller_config=config,
        seed=seed_bundle.learner_seed,
        recorder=recorder,
    )
    executor = CounterpointLiftResolveExecutor(adapter=adapter, recorder=recorder)
    episodes = tuple(
        _run_persistent_training_episode(
            adapter=adapter,
            learner=learner,
            executor=executor,
            candidate=candidate,
            run_id=run_id,
            spec=spec,
            seed_bundle=seed_bundle,
            episode_index=episode_index,
            horizon=horizon,
            max_controller_events=max_controller_events,
            recorder=recorder,
            controller_config=config,
        )
        for episode_index in range(episode_count)
    )
    ended_at = _now()
    return _write_full_training_artifacts(
        spec=spec,
        candidate=candidate,
        selection=selection,
        build=build,
        artifact_root=artifact_root,
        run_id=run_id,
        seed_bundle=seed_bundle,
        linearization_mode_id=linearization_mode_id,
        budget={
            "episodes": episode_count,
            "horizon": horizon,
            "candidate_id": candidate.candidate_id,
            "arm_id": candidate.arm_id,
            "numerator": candidate.numerator,
            "denominator": candidate.denominator,
            "requested_rate": candidate.requested_rate,
            "selector_rule_id": candidate.selector_rule_id,
            "schema_seed": candidate.schema_seed,
            "max_controller_events": max_controller_events,
            "persistent_learner_across_episodes": True,
            "controller_config": config.to_dict(),
            "learner_config": learner_cfg.to_dict(),
        },
        recorder=recorder,
        episodes=episodes,
        max_action_count=_max_tier_action_count(adapter),
        started_at=started_at,
        ended_at=ended_at,
    )


def _run_persistent_training_episode(
    *,
    adapter: CounterpointTowerControlAdapter,
    learner: CounterpointTierLearner,
    executor: CounterpointLiftResolveExecutor,
    candidate: Any,
    run_id: str,
    spec: CounterpointInstanceSpec,
    seed_bundle: SeedBundle,
    episode_index: int,
    horizon: int,
    max_controller_events: int,
    recorder: TimingRecorder,
    controller_config: ExploitExploreControllerConfig,
) -> FullTrainingEpisodeTrace:
    with recorder.segment("environment_reset"):
        active_tier_state = adapter.reset(seed_bundle=seed_bundle, episode_index=episode_index)
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
                metadata={"schema_id": adapter.schema_id, "candidate_id": candidate.candidate_id},
            )
            for tier in range(adapter.tower_depth)
        },
        move_down=adapter.move_down,
        move_up=adapter.move_up,
        tier_is_executable=adapter.tier_is_executable,
    )
    step_rows: list[FullTrainingStepRow] = []
    control_rows: list[FullTrainingControlEventRow] = []
    lift_rows: list[FullTrainingLiftFiberEventRow] = []
    abc_selection_rows: list[FullTrainingABCSelectionEventRow] = []
    abc_tier_signal_rows: list[FullTrainingABCTierSignalEventRow] = []
    learner_update_rows: list[FullTrainingLearnerUpdateEventRow] = []
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
            FullTrainingControlEventRow(
                evaluation_id=EVALUATION_ID,
                run_id=run_id,
                candidate_id=candidate.candidate_id,
                instance_id=spec.environment_instance_id,
                arm_id=candidate.arm_id,
                schema_seed=candidate.schema_seed,
                seed_bundle_id=seed_bundle.seed_bundle_id,
                training_replicate_index=seed_bundle.replicate_index,
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
        if summary is not None:
            learner_update_rows.append(
                FullTrainingLearnerUpdateEventRow(
                    evaluation_id=EVALUATION_ID,
                    run_id=run_id,
                    candidate_id=candidate.candidate_id,
                    instance_id=spec.environment_instance_id,
                    arm_id=candidate.arm_id,
                    schema_seed=candidate.schema_seed,
                    seed_bundle_id=seed_bundle.seed_bundle_id,
                    training_replicate_index=seed_bundle.replicate_index,
                    episode_index=episode_index,
                    controller_event_index=controller_event_index,
                    active_tier=before.active_tier,
                    success=bool(summary.success),
                    td_error=summary.td_error,
                    update_reason="runtime_learner_summary",
                )
            )
        lift_trace = adapter.last_lift_trace if result.transition is not None else None
        if lift_trace is not None:
            lift_rows.append(
                FullTrainingLiftFiberEventRow(
                    evaluation_id=EVALUATION_ID,
                    run_id=run_id,
                    candidate_id=candidate.candidate_id,
                    instance_id=spec.environment_instance_id,
                    arm_id=candidate.arm_id,
                    schema_seed=candidate.schema_seed,
                    seed_bundle_id=seed_bundle.seed_bundle_id,
                    training_replicate_index=seed_bundle.replicate_index,
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
                    candidate=candidate,
                    run_id=run_id,
                    instance_id=spec.environment_instance_id,
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
                    candidate=candidate,
                    run_id=run_id,
                    instance_id=spec.environment_instance_id,
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
                FullTrainingStepRow(
                    evaluation_id=EVALUATION_ID,
                    run_id=run_id,
                    candidate_id=candidate.candidate_id,
                    instance_id=spec.environment_instance_id,
                    arm_id=candidate.arm_id,
                    schema_seed=candidate.schema_seed,
                    seed_bundle_id=seed_bundle.seed_bundle_id,
                    training_replicate_index=seed_bundle.replicate_index,
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
    episode_row = FullTrainingEpisodeRow(
        evaluation_id=EVALUATION_ID,
        run_id=run_id,
        candidate_id=candidate.candidate_id,
        instance_id=spec.environment_instance_id,
        arm_id=candidate.arm_id,
        schema_seed=candidate.schema_seed,
        seed_bundle_id=seed_bundle.seed_bundle_id,
        training_replicate_index=seed_bundle.replicate_index,
        episode_index=episode_index,
        total_reward=total_reward,
        concrete_step_count=len(step_rows),
        controller_event_count=len(control_rows),
        lift_attempt_count=len(lift_rows),
        lift_success_count=sum(row.success for row in lift_rows),
        learner_update_count=sum(row.success for row in learner_update_rows),
        terminated=adapter.terminated,
        truncated=truncated,
        final_state=final_state,
    )
    return FullTrainingEpisodeTrace(
        episode_row=episode_row,
        step_rows=tuple(step_rows),
        control_rows=tuple(control_rows),
        lift_rows=tuple(lift_rows),
        abc_selection_rows=tuple(abc_selection_rows),
        abc_tier_signal_rows=tuple(abc_tier_signal_rows),
        learner_update_rows=tuple(learner_update_rows),
    )


def _write_full_training_artifacts(
    *,
    spec: CounterpointInstanceSpec,
    candidate: Any,
    selection: candidate_selection.CandidateSelectionResult,
    build: CounterpointTowerBuildResult,
    artifact_root: Path | str,
    run_id: str,
    seed_bundle: SeedBundle,
    linearization_mode_id: str,
    budget: dict[str, Any],
    recorder: TimingRecorder,
    episodes: tuple[FullTrainingEpisodeTrace, ...],
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
            "runner": "counterpoint_noisy_rate_full_training",
            "evaluation_id": EVALUATION_ID,
            "environment_instance_id": spec.environment_instance_id,
            "mode_id": DEFAULT_MODE_ID,
            "candidate_id": candidate.candidate_id,
            "schema_id": f"{ids.NOISY_RATE_CONTRACTION_SCHEMA_ID}_{candidate.arm_id}",
        },
    )
    schema = build_noisy_rate_contraction_schema(
        build.graph,
        schema_seed=candidate.schema_seed,
        numerator=candidate.numerator,
        denominator=candidate.denominator,
        selector_rule_id=candidate.selector_rule_id,
    )
    write_json(
        family_paths.family_manifest,
        FamilyManifest(
            run_family_id=EVALUATION_RUN_FAMILY_ID,
            description="Counterpoint noisy-rate full-tower training diagnostic family.",
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
    tower_shape_rows = _tower_shape_summary_rows(
        build=build,
        candidate=candidate,
        run_id=run_id,
        replicate_index=seed_bundle.replicate_index,
    )
    write_json(
        run_paths.root / "quotient_summary.json",
        {
            "evaluation_id": EVALUATION_ID,
            "candidate_id": candidate.candidate_id,
            "parent_evaluation_id": selection.parent_evaluation_id,
            "parent_artifact_run_label": selection.parent_artifact_run_label,
            "parent_readout_source": str(selection.parent_readout_source),
            "schema_id": schema.spec.schema_id,
            "arm_id": candidate.arm_id,
            "numerator": candidate.numerator,
            "denominator": candidate.denominator,
            "requested_rate": candidate.requested_rate,
            "selector_rule_id": candidate.selector_rule_id,
            "schema_seed": candidate.schema_seed,
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
            "persistent_learner_across_episodes": True,
            "parent_selected_edge_count": candidate.selected_edge_count,
            "parent_selected_source_share": candidate.selected_source_share,
            "tower_shape_summary": [row.to_flat_dict() for row in tower_shape_rows],
        },
    )
    write_json(
        run_paths.root / "tower_invariant_report.json",
        counterpoint_tower_invariant_artifact_payload(build),
    )
    write_csv(
        run_paths.episodes_csv,
        [episode.episode_row.to_flat_dict() for episode in episodes],
        FullTrainingEpisodeRow.fieldnames(),
        create_parents=True,
    )
    write_csv(
        run_paths.step_events_csv,
        [row.to_flat_dict() for episode in episodes for row in episode.step_rows],
        FullTrainingStepRow.fieldnames(),
        create_parents=True,
    )
    write_csv(
        run_paths.control_events_csv,
        [row.to_flat_dict() for episode in episodes for row in episode.control_rows],
        FullTrainingControlEventRow.fieldnames(),
        create_parents=True,
    )
    write_csv(
        run_paths.root / "lift_fiber_events.csv",
        [row.to_flat_dict() for episode in episodes for row in episode.lift_rows],
        FullTrainingLiftFiberEventRow.fieldnames(),
    )
    write_csv(
        run_paths.root / "abc_selection_events.csv",
        [row.to_flat_dict() for episode in episodes for row in episode.abc_selection_rows],
        FullTrainingABCSelectionEventRow.fieldnames(),
    )
    write_csv(
        run_paths.root / "abc_tier_signal_events.csv",
        [row.to_flat_dict() for episode in episodes for row in episode.abc_tier_signal_rows],
        FullTrainingABCTierSignalEventRow.fieldnames(),
    )
    write_csv(
        run_paths.root / "learner_update_events.csv",
        [row.to_flat_dict() for episode in episodes for row in episode.learner_update_rows],
        FullTrainingLearnerUpdateEventRow.fieldnames(),
    )
    write_csv(
        run_paths.timing_segments_csv,
        [row.to_flat_dict() for row in recorder.rows],
        recorder.rows[0].fieldnames() if recorder.rows else (),
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
            schema_id=schema.spec.schema_id,
            learner_id=mode_contract.learner_id,
            controller_id=mode_contract.controller_regime,
            seed_bundle_id=seed_bundle.seed_bundle_id,
            budget=budget,
            diagnostic_profile=mode_contract.diagnostic_profile.profile_id,
            timing_profile=mode_contract.timing_profile.profile_id,
            command="python -m big_boy_benchmarking.cli counterpoint noisy-rate-full-train run",
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
    write_json(
        family_paths.summary_json,
        {
            "evaluation_id": EVALUATION_ID,
            "run_family_id": EVALUATION_RUN_FAMILY_ID,
            "run_id": run_id,
            "candidate_id": candidate.candidate_id,
            "environment_instance_id": spec.environment_instance_id,
            "mode_id": DEFAULT_MODE_ID,
            "episode_count": len(episodes),
            "mean_return": mean_return,
            "concrete_step_count": sum(
                episode.episode_row.concrete_step_count for episode in episodes
            ),
            "learner_update_count": sum(
                episode.episode_row.learner_update_count for episode in episodes
            ),
            "artifact_schema_version": ARTIFACT_SCHEMA_VERSION,
        },
        create_parents=True,
    )
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
            "learner_update_events_csv": str(run_paths.root / "learner_update_events.csv"),
            "schema_manifest": str(run_paths.root / "schema_manifest.json"),
            "schema_construction": str(run_paths.root / "schema_construction.json"),
            "quotient_summary": str(run_paths.root / "quotient_summary.json"),
            "tower_invariant_report": str(run_paths.root / "tower_invariant_report.json"),
        },
        summary_path=str(family_paths.summary_json),
        warning_count=0,
        started_at=started_at,
        ended_at=ended_at,
    )


def _run_index_row(
    artifact_root: Path,
    record: FullTrainingRunRecord,
) -> FullTrainingEvaluationRunIndexRow:
    result = record.result
    candidate = record.candidate
    return FullTrainingEvaluationRunIndexRow(
        evaluation_id=EVALUATION_ID,
        run_id="" if result is None else result.run_id,
        candidate_id=candidate.candidate_id,
        instance_id=candidate.instance_id,
        arm_id=candidate.arm_id,
        numerator=candidate.numerator,
        denominator=candidate.denominator,
        requested_rate=candidate.requested_rate,
        selector_rule_id=candidate.selector_rule_id,
        schema_seed=candidate.schema_seed,
        seed_bundle_id=record.seed_bundle.seed_bundle_id,
        training_replicate_index=record.seed_bundle.replicate_index,
        status=record.status,
        artifact_root=str(artifact_root),
        started_at="" if result is None else result.started_at,
        ended_at=None if result is None else result.ended_at,
        failure_reason=record.failure_reason,
    )


def _abc_selection_row(
    *,
    snapshot,
    candidate: Any,
    run_id: str,
    instance_id: str,
    seed_bundle: SeedBundle,
    episode_index: int,
    controller_event_index: int,
    active_tier_after: int | None,
    concrete_step_emitted: bool,
    lift_attempt_emitted: bool,
    lift_success: bool | None,
    control_action: str,
) -> FullTrainingABCSelectionEventRow:
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
    return FullTrainingABCSelectionEventRow(
        evaluation_id=EVALUATION_ID,
        run_id=run_id,
        candidate_id=candidate.candidate_id,
        instance_id=instance_id,
        arm_id=candidate.arm_id,
        schema_seed=candidate.schema_seed,
        seed_bundle_id=seed_bundle.seed_bundle_id,
        training_replicate_index=seed_bundle.replicate_index,
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
    candidate: Any,
    run_id: str,
    instance_id: str,
    seed_bundle: SeedBundle,
    episode_index: int,
    controller_event_index: int,
    liftability_counts_by_tier: dict[int, tuple[int, int]],
) -> tuple[FullTrainingABCTierSignalEventRow, ...]:
    return tuple(
        FullTrainingABCTierSignalEventRow(
            evaluation_id=EVALUATION_ID,
            run_id=run_id,
            candidate_id=candidate.candidate_id,
            instance_id=instance_id,
            arm_id=candidate.arm_id,
            schema_seed=candidate.schema_seed,
            seed_bundle_id=seed_bundle.seed_bundle_id,
            training_replicate_index=seed_bundle.replicate_index,
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


def _verify_candidate_tower(candidate: Any, build: CounterpointTowerBuildResult) -> None:
    expected = json.loads(candidate.tier_state_cell_count_sequence)
    observed = [len(layer.all_cell_ids()) for layer in build.tower.state_layers]
    if observed != expected:
        raise ValueError(
            "candidate tower shape mismatch: "
            f"candidate={candidate.candidate_id} expected={expected} observed={observed}"
        )


def _tower_shape_summary_rows(
    *,
    build: CounterpointTowerBuildResult,
    candidate: Any,
    run_id: str,
    replicate_index: int,
) -> tuple[FullTrainingTowerShapeSummaryRow, ...]:
    base_state_count = max(1, len(build.graph.states))
    rows = []
    for tier_index, state_layer in enumerate(build.tower.state_layers):
        cell_ids = tuple(state_layer.all_cell_ids())
        member_counts = [len(state_layer.members(cell_id)) for cell_id in cell_ids]
        state_cell_count = len(cell_ids)
        largest_share = max(member_counts, default=0) / base_state_count
        rows.append(
            FullTrainingTowerShapeSummaryRow(
                evaluation_id=EVALUATION_ID,
                run_id=run_id,
                candidate_id=candidate.candidate_id,
                instance_id=build.graph.spec.environment_instance_id,
                arm_id=candidate.arm_id,
                schema_seed=candidate.schema_seed,
                training_replicate_index=replicate_index,
                tier_index=tier_index,
                state_cell_count=state_cell_count,
                active_action_cell_count=_active_action_cell_count(build.tower, tier_index),
                raw_historical_action_cell_record_count=_raw_action_cell_count(
                    build.tower.action_layers[tier_index]
                )
                if tier_index < len(build.tower.action_layers)
                else 0,
                largest_state_cell_share=largest_share,
                full_collapse=tier_index > 0 and state_cell_count == 1,
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
