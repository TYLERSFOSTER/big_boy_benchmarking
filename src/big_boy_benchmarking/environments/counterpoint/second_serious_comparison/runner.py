"""Runner for the second serious counterpoint schema comparison."""

from __future__ import annotations

import json
import statistics
from dataclasses import dataclass
from datetime import UTC, datetime
from pathlib import Path
from typing import Any

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
    TINY_INSTANCE_ID,
    WIDE_SPAN18_INSTANCE_ID,
    default_medium_spec,
    default_small_spec,
    default_tiny_spec,
    default_wide_span18_spec,
)
from big_boy_benchmarking.environments.counterpoint.noisy_rate_full_training.runner import (
    _active_action_cell_count,
    _max_tier_action_count,
    _raw_action_cell_count,
    _run_persistent_training_episode,
)
from big_boy_benchmarking.environments.counterpoint.schemas import (
    SchemaConstruction,
    SchemaSpec,
    build_noisy_rate_contraction_schema,
    build_schema_for_id,
    state_key,
)
from big_boy_benchmarking.environments.counterpoint.second_serious_comparison.candidates import (
    CandidateSelection,
    SchemaCandidate,
    load_schema1_candidates,
    require_serious_medium_candidate_gate,
)
from big_boy_benchmarking.environments.counterpoint.second_serious_comparison.config import (
    CALIBRATION_MODE_ID,
    DEFAULT_LINEARIZATION_MODE_ID,
    DEFAULT_RUNTIME_MODE_ID,
    DEFAULT_TIER_JUMP_POLICY_ID,
    EVALUATION_ID,
    EVALUATION_RUN_FAMILY_ID,
    PERSISTENCE_RULE_ID,
    SCHEMA0_CLASS_ID,
    SCHEMA1_CLASS_ID,
    SCHEMA1_TOWER_SOURCE_FULL_ITERATED,
    SCHEMA1_TOWER_SOURCE_ONE_DROP,
    SERIOUS_MODE_ID,
    SMOKE_MODE_ID,
    SecondSeriousComparisonBudget,
)
from big_boy_benchmarking.environments.counterpoint.second_serious_comparison.events import (
    ComparisonABCSelectionEventRow,
    ComparisonABCTierSignalEventRow,
    ComparisonControlEventRow,
    ComparisonEpisodeRow,
    ComparisonLearnerUpdateEventRow,
    ComparisonLiftFiberEventRow,
    ComparisonRunIndexRow,
    ComparisonStepRow,
    ComparisonTierTransitionEventRow,
    ComparisonTowerShapeSummaryRow,
    FirstSustainedHitSummaryRow,
    ThresholdWindowEventRow,
)
from big_boy_benchmarking.environments.counterpoint.second_serious_comparison.manifests import (
    budget_lock_payload,
    candidate_manifest_payload,
    evaluation_arm_manifest_payload,
    evaluation_manifest_payload,
    parent_source_manifest_payload,
    threshold_policy_payload,
    tier_jump_policy_payload,
)
from big_boy_benchmarking.environments.counterpoint.second_serious_comparison.paths import (
    build_second_serious_comparison_paths,
    default_candidate_readout_source,
    validate_repo_resident_artifact_root,
)
from big_boy_benchmarking.environments.counterpoint.second_serious_comparison.thresholds import (
    ThresholdPolicy,
    TierJumpPolicy,
    compute_first_hit,
)
from big_boy_benchmarking.environments.counterpoint.serious_learning.config import (
    ExploitExploreControllerConfig,
    TabularQLearnerConfig,
)
from big_boy_benchmarking.environments.counterpoint.serious_learning.tower_control import (
    CounterpointLiftResolveExecutor,
    CounterpointTierLearner,
    CounterpointTowerControlAdapter,
)
from big_boy_benchmarking.environments.counterpoint.specs import CounterpointInstanceSpec
from big_boy_benchmarking.environments.counterpoint.tower_adapter import (
    CounterpointTowerBuildResult,
    base_edge_to_counterpoint_edge_key,
    build_counterpoint_iterated_noisy_rate_partition_tower,
    build_counterpoint_noisy_rate_partition_tower,
    build_counterpoint_partition_tower,
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
class RuntimeCandidate:
    candidate_id: str
    candidate_group_id: str
    schema_class_id: str
    instance_id: str
    arm_id: str
    numerator: int
    denominator: int
    requested_rate: float
    selector_rule_id: str
    schema_seed: int
    tier_state_cell_count_sequence: str
    tier_active_action_cell_count_sequence: str
    schema1_tower_source: str = SCHEMA1_TOWER_SOURCE_ONE_DROP


@dataclass(frozen=True)
class ComparisonRunRecord:
    candidate: RuntimeCandidate
    seed_bundle: SeedBundle
    result: BenchmarkRunResult | None
    status: str
    failure_reason: str | None = None


def run_second_serious_comparison(
    *,
    artifact_root: Path | str,
    candidate_readout_source: Path | str | None = None,
    instance_id: str = "small",
    candidate_cap: int = 1,
    target_candidate_ids: tuple[str, ...] = (),
    schema1_tower_source: str = SCHEMA1_TOWER_SOURCE_ONE_DROP,
    training_replicates_per_arm: int = 1,
    episodes_per_replicate: int = 8,
    threshold_value: float | None = None,
    threshold_policy_id: str = "counterpoint_total_space_sustained_reward_v001",
    window_length: int = 5,
    required_count: int = 4,
    run_mode: str = SMOKE_MODE_ID,
    base_seed: int = 0,
    locked_by: str = "cli",
    horizon_override: int | None = None,
    controller_event_ceiling: int | None = None,
    linearization_mode_id: str = DEFAULT_LINEARIZATION_MODE_ID,
    serious_run_authorized: bool = False,
) -> dict[str, Any]:
    artifact_root = validate_repo_resident_artifact_root(artifact_root)
    spec = comparison_spec_for_instance(instance_id)
    candidate_source = candidate_readout_source or default_candidate_readout_source()
    budget = SecondSeriousComparisonBudget(
        environment_instance_id=spec.environment_instance_id,
        candidate_readout_source=candidate_source,
        candidate_cap=candidate_cap,
        target_candidate_ids=target_candidate_ids,
        schema1_tower_source=schema1_tower_source,
        episodes_per_replicate=episodes_per_replicate,
        training_replicates_per_arm=training_replicates_per_arm,
        base_seed=base_seed,
        locked_by=locked_by,
        run_mode=run_mode,
        threshold_policy_id=threshold_policy_id,
        threshold_value=threshold_value,
        window_length=window_length,
        required_count=required_count,
        tier_jump_reward_cutoff=threshold_value,
        controller_event_ceiling_override=controller_event_ceiling,
        linearization_mode_id=linearization_mode_id,
        serious_run_authorized=serious_run_authorized,
    )
    threshold_policy = ThresholdPolicy(
        threshold_policy_id=threshold_policy_id,
        threshold_value=0.0 if threshold_value is None else threshold_value,
        window_length=window_length,
        required_count=required_count,
    )
    tier_jump_policy = TierJumpPolicy(
        tier_jump_policy_id=DEFAULT_TIER_JUMP_POLICY_ID,
        tier_jump_reward_cutoff=threshold_value,
        tier_jump_window_length=window_length,
    )
    paths = build_second_serious_comparison_paths(artifact_root)
    paths.root.mkdir(parents=True, exist_ok=True)
    paths.results_dir.mkdir(parents=True, exist_ok=True)
    selection = load_schema1_candidates(
        budget.candidate_readout_source,
        instance_id=spec.environment_instance_id,
        candidate_cap=budget.candidate_cap,
        target_candidate_ids=budget.target_candidate_ids,
    )
    if run_mode == SERIOUS_MODE_ID:
        require_serious_medium_candidate_gate(selection)
    if not selection.selected:
        raise ValueError(
            "candidate source yielded no eligible Schema 1 candidates for "
            f"{spec.environment_instance_id}; source={selection.candidate_readout_source}"
        )

    _write_evaluation_level_manifests(
        paths=paths,
        budget=budget,
        threshold_policy=threshold_policy,
        tier_jump_policy=tier_jump_policy,
        selection=selection,
    )

    seed_bundles = generate_seed_bundles(
        base_seed=base_seed,
        replicate_count=training_replicates_per_arm,
    )
    horizon = horizon_override or spec.horizon_steps
    records: list[ComparisonRunRecord] = []
    for schema1_candidate in selection.selected:
        for seed_bundle in seed_bundles:
            for runtime_candidate in (
                _schema0_runtime_candidate(schema1_candidate),
                _schema1_runtime_candidate(
                    schema1_candidate,
                    schema1_tower_source=budget.schema1_tower_source,
                ),
            ):
                try:
                    result = run_schema_condition(
                        spec=spec,
                        candidate=runtime_candidate,
                        seed_bundle=seed_bundle,
                        artifact_root=artifact_root,
                        run_mode=run_mode,
                        episode_count=episodes_per_replicate,
                        horizon=horizon,
                        max_controller_events=budget.max_controller_events(horizon),
                        threshold_policy=threshold_policy,
                        tier_jump_policy=tier_jump_policy,
                        linearization_mode_id=linearization_mode_id,
                    )
                    records.append(
                        ComparisonRunRecord(
                            candidate=runtime_candidate,
                            seed_bundle=seed_bundle,
                            result=result,
                            status=result.status,
                        )
                    )
                except Exception as exc:
                    records.append(
                        ComparisonRunRecord(
                            candidate=runtime_candidate,
                            seed_bundle=seed_bundle,
                            result=None,
                            status="failed",
                            failure_reason=f"{type(exc).__name__}: {exc}",
                        )
                    )
    write_csv(
        paths.evaluation_run_index_csv,
        [_run_index_row(artifact_root, run_mode, record).to_flat_dict() for record in records],
        ComparisonRunIndexRow.fieldnames(),
    )
    if run_mode == CALIBRATION_MODE_ID:
        _write_calibration_files(paths=paths, records=records, artifact_root=artifact_root)
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
        "calibration_summary": str(paths.calibration_summary)
        if run_mode == CALIBRATION_MODE_ID
        else None,
    }


def calibrate_second_serious_comparison(**kwargs: Any) -> dict[str, Any]:
    kwargs["run_mode"] = CALIBRATION_MODE_ID
    kwargs.setdefault("threshold_value", None)
    kwargs.setdefault("serious_run_authorized", False)
    return run_second_serious_comparison(**kwargs)


def run_schema_condition(
    *,
    spec: CounterpointInstanceSpec,
    candidate: RuntimeCandidate,
    seed_bundle: SeedBundle,
    artifact_root: Path | str,
    run_mode: str,
    episode_count: int,
    horizon: int,
    max_controller_events: int,
    threshold_policy: ThresholdPolicy,
    tier_jump_policy: TierJumpPolicy,
    linearization_mode_id: str = DEFAULT_LINEARIZATION_MODE_ID,
    controller_config: ExploitExploreControllerConfig | None = None,
    learner_config: TabularQLearnerConfig | None = None,
) -> BenchmarkRunResult:
    if linearization_mode_id != DEFAULT_LINEARIZATION_MODE_ID:
        raise ValueError(
            "second serious schema comparison uses tensor_available_disabled; "
            f"reserved linearization mode rejected: {linearization_mode_id}"
        )
    config = ExploitExploreControllerConfig() if controller_config is None else controller_config
    learner_cfg = TabularQLearnerConfig() if learner_config is None else learner_config
    run_id = (
        f"{candidate.candidate_group_id}-{candidate.schema_class_id}-"
        f"trainrep{seed_bundle.replicate_index}"
    )
    started_at = _now()
    recorder = TimingRecorder.create(run_id)
    with recorder.segment("tower_reset"):
        build = _build_candidate_tower(spec, candidate)
    _verify_candidate_tower(candidate, build)
    adapter = CounterpointTowerControlAdapter(
        spec=spec,
        schema_id=_runtime_schema_id(candidate),
        schema_seed=None
        if candidate.schema_class_id == SCHEMA0_CLASS_ID
        else candidate.schema_seed,
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
    full_training_episodes = tuple(
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
    episodes = tuple(
        _episode_row(
            episode.episode_row,
            run_mode=run_mode,
            candidate=candidate,
        )
        for episode in full_training_episodes
    )
    threshold_result = compute_first_hit(
        tuple(row.total_reward for row in episodes),
        threshold_policy=threshold_policy,
        steps_by_episode=tuple(row.concrete_step_count for row in episodes),
    )
    threshold_windows = tuple(
        ThresholdWindowEventRow(
            evaluation_id=EVALUATION_ID,
            run_id=run_id,
            run_mode=run_mode,
            candidate_group_id=candidate.candidate_group_id,
            schema_class_id=candidate.schema_class_id,
            candidate_id=candidate.candidate_id,
            training_replicate_index=seed_bundle.replicate_index,
            episode_window_start=window.episode_window_start,
            episode_window_end=window.episode_window_end,
            threshold_policy_id=threshold_policy.threshold_policy_id,
            threshold_value=threshold_policy.threshold_value,
            threshold_hit_count=window.threshold_hit_count,
            required_count=threshold_policy.required_count,
            window_length=threshold_policy.window_length,
            window_met=window.window_met,
            window_mean_total_reward=window.window_mean_total_reward,
            window_min_total_reward=window.window_min_total_reward,
        )
        for window in threshold_result.windows
    )
    first_hit = FirstSustainedHitSummaryRow(
        evaluation_id=EVALUATION_ID,
        run_id=run_id,
        run_mode=run_mode,
        candidate_group_id=candidate.candidate_group_id,
        schema_class_id=candidate.schema_class_id,
        candidate_id=candidate.candidate_id,
        instance_id=spec.environment_instance_id,
        arm_id=candidate.arm_id,
        schema_seed=candidate.schema_seed,
        training_replicate_index=seed_bundle.replicate_index,
        threshold_policy_id=threshold_policy.threshold_policy_id,
        hit_metric_id=threshold_policy.metric_id,
        hit_threshold_value=threshold_policy.threshold_value,
        hit_persistence_rule_id=PERSISTENCE_RULE_ID,
        hit_persistence_window_length=threshold_policy.window_length,
        hit_persistence_required_count=threshold_policy.required_count,
        first_hit_episode_index=threshold_result.first_hit_episode_index,
        first_sustained_hit_episode_index=threshold_result.first_sustained_hit_episode_index,
        first_sustained_hit_training_step=threshold_result.first_sustained_hit_training_step,
        hit_status=threshold_result.hit_status,
        episodes_to_sustained_hit=threshold_result.episodes_to_sustained_hit,
        training_steps_to_sustained_hit=threshold_result.training_steps_to_sustained_hit,
        post_hit_window_mean=threshold_result.post_hit_window_mean,
        post_hit_window_min=threshold_result.post_hit_window_min,
        post_hit_window_success_count=threshold_result.post_hit_window_success_count,
        hit_failure_reason=threshold_result.hit_failure_reason,
    )
    ended_at = _now()
    return _write_run_artifacts(
        spec=spec,
        build=build,
        candidate=candidate,
        seed_bundle=seed_bundle,
        artifact_root=Path(artifact_root),
        run_id=run_id,
        run_mode=run_mode,
        linearization_mode_id=linearization_mode_id,
        budget={
            "episodes": episode_count,
            "horizon": horizon,
            "candidate_group_id": candidate.candidate_group_id,
            "schema_class_id": candidate.schema_class_id,
            "candidate_id": candidate.candidate_id,
            "arm_id": candidate.arm_id,
            "schema_seed": candidate.schema_seed,
            "schema1_tower_source": candidate.schema1_tower_source,
            "max_controller_events": max_controller_events,
            "persistent_learner_across_episodes": True,
            "threshold_policy": threshold_policy.to_dict(),
            "tier_jump_policy": tier_jump_policy.to_dict(),
            "controller_config": config.to_dict(),
            "learner_config": learner_cfg.to_dict(),
        },
        recorder=recorder,
        full_training_episodes=full_training_episodes,
        episodes=episodes,
        threshold_windows=threshold_windows,
        first_hit=first_hit,
        threshold_policy=threshold_policy,
        tier_jump_policy=tier_jump_policy,
        max_action_count=_max_tier_action_count(adapter),
        started_at=started_at,
        ended_at=ended_at,
    )


def comparison_spec_for_instance(instance_id: str) -> CounterpointInstanceSpec:
    if instance_id in {"tiny", TINY_INSTANCE_ID}:
        return default_tiny_spec()
    if instance_id in {"small", SMALL_INSTANCE_ID}:
        return default_small_spec()
    if instance_id in {"medium", MEDIUM_INSTANCE_ID}:
        return default_medium_spec()
    if instance_id in {
        "wide_span18",
        "wide_20_108_span18",
        WIDE_SPAN18_INSTANCE_ID,
    }:
        return default_wide_span18_spec()
    raise ValueError(f"unknown counterpoint comparison instance id: {instance_id}")


def _write_evaluation_level_manifests(
    *,
    paths,
    budget: SecondSeriousComparisonBudget,
    threshold_policy: ThresholdPolicy,
    tier_jump_policy: TierJumpPolicy,
    selection: CandidateSelection,
) -> None:
    write_json(
        paths.evaluation_manifest, evaluation_manifest_payload(budget=budget), create_parents=True
    )
    write_json(
        paths.evaluation_arm_manifest, evaluation_arm_manifest_payload(), create_parents=True
    )
    write_json(
        paths.evaluation_budget_lock, budget_lock_payload(budget=budget), create_parents=True
    )
    write_json(
        paths.threshold_policy_manifest,
        threshold_policy_payload(threshold_policy),
        create_parents=True,
    )
    write_json(
        paths.tier_jump_policy_manifest,
        tier_jump_policy_payload(tier_jump_policy),
        create_parents=True,
    )
    write_json(
        paths.candidate_manifest,
        candidate_manifest_payload(selection=selection, budget=budget),
        create_parents=True,
    )
    write_json(
        paths.parent_source_manifest,
        parent_source_manifest_payload(selection=selection),
        create_parents=True,
    )


def _schema0_runtime_candidate(schema1_candidate: SchemaCandidate) -> RuntimeCandidate:
    return RuntimeCandidate(
        candidate_id=f"{schema1_candidate.candidate_id}-schema0",
        candidate_group_id=schema1_candidate.candidate_id,
        schema_class_id=SCHEMA0_CLASS_ID,
        instance_id=schema1_candidate.instance_id,
        arm_id=SCHEMA0_CLASS_ID,
        numerator=0,
        denominator=1,
        requested_rate=0.0,
        selector_rule_id="no_contraction_identity",
        schema_seed=schema1_candidate.schema_seed,
        tier_state_cell_count_sequence="[]",
        tier_active_action_cell_count_sequence="[]",
        schema1_tower_source=SCHEMA1_TOWER_SOURCE_ONE_DROP,
    )


def _schema1_runtime_candidate(
    schema1_candidate: SchemaCandidate,
    *,
    schema1_tower_source: str,
) -> RuntimeCandidate:
    return RuntimeCandidate(
        candidate_id=schema1_candidate.candidate_id,
        candidate_group_id=schema1_candidate.candidate_id,
        schema_class_id=SCHEMA1_CLASS_ID,
        instance_id=schema1_candidate.instance_id,
        arm_id=schema1_candidate.arm_id,
        numerator=schema1_candidate.numerator,
        denominator=schema1_candidate.denominator,
        requested_rate=schema1_candidate.requested_rate,
        selector_rule_id=schema1_candidate.selector_rule_id,
        schema_seed=schema1_candidate.schema_seed,
        tier_state_cell_count_sequence=schema1_candidate.tier_state_cell_count_sequence,
        tier_active_action_cell_count_sequence=schema1_candidate.tier_active_action_cell_count_sequence,
        schema1_tower_source=schema1_tower_source,
    )


def _build_candidate_tower(
    spec: CounterpointInstanceSpec,
    candidate: RuntimeCandidate,
) -> CounterpointTowerBuildResult:
    if candidate.schema_class_id == SCHEMA0_CLASS_ID:
        return build_counterpoint_partition_tower(spec, schema_id=ids.EMPTY_SCHEMA_ID)
    if candidate.schema1_tower_source == SCHEMA1_TOWER_SOURCE_FULL_ITERATED:
        return build_counterpoint_iterated_noisy_rate_partition_tower(
            spec,
            numerator=candidate.numerator,
            denominator=candidate.denominator,
            schema_seed=candidate.schema_seed,
            selector_rule_id=candidate.selector_rule_id,
        )
    return build_counterpoint_noisy_rate_partition_tower(
        spec,
        numerator=candidate.numerator,
        denominator=candidate.denominator,
        schema_seed=candidate.schema_seed,
        selector_rule_id=candidate.selector_rule_id,
    )


def _runtime_schema_id(candidate: RuntimeCandidate) -> str:
    if candidate.schema_class_id == SCHEMA0_CLASS_ID:
        return ids.EMPTY_SCHEMA_ID
    if candidate.schema1_tower_source == SCHEMA1_TOWER_SOURCE_FULL_ITERATED:
        return (
            f"{ids.NOISY_RATE_CONTRACTION_SCHEMA_ID}_{candidate.arm_id}_"
            "full_iterated"
        )
    return f"{ids.NOISY_RATE_CONTRACTION_SCHEMA_ID}_{candidate.arm_id}"


def _verify_candidate_tower(
    candidate: RuntimeCandidate,
    build: CounterpointTowerBuildResult,
) -> None:
    if candidate.schema_class_id == SCHEMA0_CLASS_ID:
        if len(build.tower.state_layers) != 1:
            raise ValueError("Schema 0 no-contraction tower should have one active tier")
        return
    expected = json.loads(candidate.tier_state_cell_count_sequence)
    observed = [len(layer.all_cell_ids()) for layer in build.tower.state_layers]
    if candidate.schema1_tower_source == SCHEMA1_TOWER_SOURCE_FULL_ITERATED:
        if observed[: len(expected)] != expected:
            raise ValueError(
                "full-iterated candidate tower prefix mismatch: "
                f"candidate={candidate.candidate_id} expected_prefix={expected} "
                f"observed={observed}"
            )
        if len(observed) <= len(expected):
            raise ValueError(
                "full-iterated candidate tower did not extend source one-drop tower: "
                f"candidate={candidate.candidate_id} observed={observed}"
            )
        return
    if observed != expected:
        raise ValueError(
            "candidate tower shape mismatch: "
            f"candidate={candidate.candidate_id} expected={expected} observed={observed}"
        )


def _schema_construction_for_candidate(
    *,
    build: CounterpointTowerBuildResult,
    candidate: RuntimeCandidate,
) -> SchemaConstruction:
    if candidate.schema_class_id == SCHEMA0_CLASS_ID:
        return build_schema_for_id(build.graph, schema_id=ids.EMPTY_SCHEMA_ID, schema_seed=None)
    if candidate.schema1_tower_source != SCHEMA1_TOWER_SOURCE_FULL_ITERATED:
        return build_noisy_rate_contraction_schema(
            build.graph,
            schema_seed=candidate.schema_seed,
            numerator=candidate.numerator,
            denominator=candidate.denominator,
            selector_rule_id=candidate.selector_rule_id,
        )

    one_drop = build_noisy_rate_contraction_schema(
        build.graph,
        schema_seed=candidate.schema_seed,
        numerator=candidate.numerator,
        denominator=candidate.denominator,
        selector_rule_id=candidate.selector_rule_id,
    )
    edge_partition = {}
    for edge_id in build.tower.registry.edge_ids:
        block_id = build.tower.schema_assignment_store.assignment_by_edge_id.get(edge_id)
        edge_key = build.tower.registry.edge_for_id(edge_id)
        edge_partition[base_edge_to_counterpoint_edge_key(edge_key)] = (
            "iterated_unscheduled" if block_id is None else repr(block_id.value)
        )
    return SchemaConstruction(
        spec=SchemaSpec(
            schema_id=_runtime_schema_id(candidate),
            schema_family_id=one_drop.spec.schema_family_id,
            schema_version=one_drop.spec.schema_version,
            environment_family_id=one_drop.spec.environment_family_id,
            environment_instance_id=one_drop.spec.environment_instance_id,
            schema_seed=candidate.schema_seed,
            construction_method=(
                "seeded_edge_global_noisy_rate_iterated_quotient_contraction"
            ),
            source_label_families=one_drop.spec.source_label_families,
            state_partition_description=(
                "identity state keys at tier 0; runtime contraction is edge-driven"
            ),
            action_partition_description=(
                "ordered iterated noisy-rate blocks; tier 1 matches the one-drop "
                "source selection and later tiers resample quotient representatives"
            ),
            expected_tower_depth=len(build.tower.state_layers),
            expected_compression_target=(
                f"iterated {candidate.numerator}/{candidate.denominator} quotient "
                "blocks until degenerate or terminal tier"
            ),
            leakage_risk_statement=one_drop.spec.leakage_risk_statement,
            intended_role="second_serious_full_iterated_schema1_comparison",
            online_eligible=True,
            diagnostic_only=False,
        ),
        state_partition={state_key(state): state_key(state) for state in build.graph.states},
        edge_partition=edge_partition,
    )


def _write_run_artifacts(
    *,
    spec: CounterpointInstanceSpec,
    build: CounterpointTowerBuildResult,
    candidate: RuntimeCandidate,
    seed_bundle: SeedBundle,
    artifact_root: Path,
    run_id: str,
    run_mode: str,
    linearization_mode_id: str,
    budget: dict[str, Any],
    recorder: TimingRecorder,
    full_training_episodes,
    episodes: tuple[ComparisonEpisodeRow, ...],
    threshold_windows: tuple[ThresholdWindowEventRow, ...],
    first_hit: FirstSustainedHitSummaryRow,
    threshold_policy: ThresholdPolicy,
    tier_jump_policy: TierJumpPolicy,
    max_action_count: int,
    started_at: str,
    ended_at: str,
) -> BenchmarkRunResult:
    family_paths = build_run_family_paths(artifact_root, EVALUATION_RUN_FAMILY_ID)
    run_paths = build_run_paths(artifact_root, EVALUATION_RUN_FAMILY_ID, run_id)
    ensure_artifact_dirs(family_paths, run_paths)
    mode_contract = require_runnable_mode(DEFAULT_RUNTIME_MODE_ID)
    dependency_state = collect_state_collapser_dependency_state(
        dependency_spec=STATE_COLLAPSER_DEPENDENCY_SPEC,
    )
    linearization_payload = build_linearization_artifact_payload(
        linearization_mode_id=linearization_mode_id,
        recorder=recorder,
        tower=build.tower,
        max_action_count=max_action_count,
        metadata={
            "runner": "counterpoint_second_serious_schema_comparison",
            "evaluation_id": EVALUATION_ID,
            "environment_instance_id": spec.environment_instance_id,
            "run_mode": run_mode,
            "schema_class_id": candidate.schema_class_id,
            "candidate_id": candidate.candidate_id,
            "schema_id": _runtime_schema_id(candidate),
            "schema1_tower_source": candidate.schema1_tower_source,
        },
    )
    schema = _schema_construction_for_candidate(build=build, candidate=candidate)
    write_json(
        family_paths.family_manifest,
        FamilyManifest(
            run_family_id=EVALUATION_RUN_FAMILY_ID,
            description="Counterpoint second serious schema-comparison family.",
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
            mode_id=DEFAULT_RUNTIME_MODE_ID,
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
    write_json(run_paths.root / "threshold_policy_manifest.json", threshold_policy.to_dict())
    write_json(run_paths.root / "tier_jump_policy_manifest.json", tier_jump_policy.to_dict())
    tower_shape_rows = _tower_shape_summary_rows(
        build=build,
        candidate=candidate,
        run_id=run_id,
        run_mode=run_mode,
        replicate_index=seed_bundle.replicate_index,
    )
    write_json(
        run_paths.root / "quotient_summary.json",
        {
            "evaluation_id": EVALUATION_ID,
            "run_mode": run_mode,
            "candidate_group_id": candidate.candidate_group_id,
            "candidate_id": candidate.candidate_id,
            "schema_class_id": candidate.schema_class_id,
            "schema_id": schema.spec.schema_id,
            "arm_id": candidate.arm_id,
            "numerator": candidate.numerator,
            "denominator": candidate.denominator,
            "requested_rate": candidate.requested_rate,
            "selector_rule_id": candidate.selector_rule_id,
            "schema_seed": candidate.schema_seed,
            "schema1_tower_source": candidate.schema1_tower_source,
            "partition_tier_count": len(build.tower.state_layers),
            "state_cell_count_by_tier": [
                len(layer.all_cell_ids()) for layer in build.tower.state_layers
            ],
            "active_action_cell_count_by_tier": [
                _active_action_cell_count(build.tower, tier)
                for tier in range(len(build.tower.state_layers))
            ],
            "persistent_learner_across_episodes": True,
            "tower_shape_summary": [row.to_flat_dict() for row in tower_shape_rows],
        },
    )
    write_csv(
        run_paths.episodes_csv,
        [row.to_flat_dict() for row in episodes],
        ComparisonEpisodeRow.fieldnames(),
        create_parents=True,
    )
    write_csv(
        run_paths.step_events_csv,
        [
            _step_row(row, run_mode=run_mode, candidate=candidate).to_flat_dict()
            for episode in full_training_episodes
            for row in episode.step_rows
        ],
        ComparisonStepRow.fieldnames(),
        create_parents=True,
    )
    control_rows = tuple(
        _control_row(row, run_mode=run_mode, candidate=candidate)
        for episode in full_training_episodes
        for row in episode.control_rows
    )
    write_csv(
        run_paths.control_events_csv,
        [row.to_flat_dict() for row in control_rows],
        ComparisonControlEventRow.fieldnames(),
        create_parents=True,
    )
    write_csv(
        run_paths.root / "tier_transition_events.csv",
        [
            _tier_transition_row(
                row, candidate=candidate, tier_jump_policy=tier_jump_policy
            ).to_flat_dict()
            for row in control_rows
            if row.active_tier_before != row.active_tier_after
        ],
        ComparisonTierTransitionEventRow.fieldnames(),
    )
    write_csv(
        run_paths.root / "lift_fiber_events.csv",
        [
            _lift_row(row, run_mode=run_mode, candidate=candidate).to_flat_dict()
            for episode in full_training_episodes
            for row in episode.lift_rows
        ],
        ComparisonLiftFiberEventRow.fieldnames(),
    )
    write_csv(
        run_paths.root / "abc_selection_events.csv",
        [
            _abc_selection_row(row, run_mode=run_mode, candidate=candidate).to_flat_dict()
            for episode in full_training_episodes
            for row in episode.abc_selection_rows
        ],
        ComparisonABCSelectionEventRow.fieldnames(),
    )
    write_csv(
        run_paths.root / "abc_tier_signal_events.csv",
        [
            _abc_tier_signal_row(row, run_mode=run_mode, candidate=candidate).to_flat_dict()
            for episode in full_training_episodes
            for row in episode.abc_tier_signal_rows
        ],
        ComparisonABCTierSignalEventRow.fieldnames(),
    )
    write_csv(
        run_paths.root / "learner_update_events.csv",
        [
            _learner_update_row(row, run_mode=run_mode, candidate=candidate).to_flat_dict()
            for episode in full_training_episodes
            for row in episode.learner_update_rows
        ],
        ComparisonLearnerUpdateEventRow.fieldnames(),
    )
    write_csv(
        run_paths.root / "threshold_window_events.csv",
        [row.to_flat_dict() for row in threshold_windows],
        ThresholdWindowEventRow.fieldnames(),
    )
    write_json(run_paths.root / "first_hit_summary.json", first_hit.to_flat_dict())
    write_csv(
        run_paths.root / "first_sustained_hit_summary.csv",
        [first_hit.to_flat_dict()],
        FirstSustainedHitSummaryRow.fieldnames(),
    )
    write_csv(
        run_paths.root / "tower_shape_summary.csv",
        [row.to_flat_dict() for row in tower_shape_rows],
        ComparisonTowerShapeSummaryRow.fieldnames(),
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
            mode_id=DEFAULT_RUNTIME_MODE_ID,
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
            command="python -m big_boy_benchmarking.cli counterpoint second-serious-comparison run",
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
            "mode_id": DEFAULT_RUNTIME_MODE_ID,
            "status": "success",
            "started_at": started_at,
            "ended_at": ended_at,
            "artifact_schema_version": ARTIFACT_SCHEMA_VERSION,
        },
        create_parents=True,
    )
    run_paths.warnings_jsonl.touch()
    write_json(
        family_paths.summary_json,
        {
            "evaluation_id": EVALUATION_ID,
            "run_family_id": EVALUATION_RUN_FAMILY_ID,
            "run_id": run_id,
            "candidate_group_id": candidate.candidate_group_id,
            "schema_class_id": candidate.schema_class_id,
            "environment_instance_id": spec.environment_instance_id,
            "mode_id": DEFAULT_RUNTIME_MODE_ID,
            "episode_count": len(episodes),
            "mean_return": statistics.mean(row.total_reward for row in episodes)
            if episodes
            else 0.0,
            "hit_status": first_hit.hit_status,
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
            "threshold_window_events_csv": str(run_paths.root / "threshold_window_events.csv"),
            "first_hit_summary": str(run_paths.root / "first_hit_summary.json"),
            "first_sustained_hit_summary_csv": str(
                run_paths.root / "first_sustained_hit_summary.csv"
            ),
            "tower_shape_summary_csv": str(run_paths.root / "tower_shape_summary.csv"),
        },
        summary_path=str(family_paths.summary_json),
        warning_count=0,
        started_at=started_at,
        ended_at=ended_at,
    )


def _episode_row(row, *, run_mode: str, candidate: RuntimeCandidate) -> ComparisonEpisodeRow:
    return ComparisonEpisodeRow(
        evaluation_id=EVALUATION_ID,
        run_id=row.run_id,
        run_mode=run_mode,
        candidate_group_id=candidate.candidate_group_id,
        schema_class_id=candidate.schema_class_id,
        candidate_id=candidate.candidate_id,
        instance_id=row.instance_id,
        arm_id=candidate.arm_id,
        schema_seed=candidate.schema_seed,
        seed_bundle_id=row.seed_bundle_id,
        training_replicate_index=row.training_replicate_index,
        episode_index=row.episode_index,
        total_reward=row.total_reward,
        concrete_step_count=row.concrete_step_count,
        controller_event_count=row.controller_event_count,
        lift_attempt_count=row.lift_attempt_count,
        lift_success_count=row.lift_success_count,
        learner_update_count=row.learner_update_count,
        terminated=row.terminated,
        truncated=row.truncated,
        final_state=row.final_state,
    )


def _step_row(row, *, run_mode: str, candidate: RuntimeCandidate) -> ComparisonStepRow:
    return ComparisonStepRow(
        evaluation_id=EVALUATION_ID,
        run_id=row.run_id,
        run_mode=run_mode,
        candidate_group_id=candidate.candidate_group_id,
        schema_class_id=candidate.schema_class_id,
        candidate_id=candidate.candidate_id,
        instance_id=row.instance_id,
        arm_id=candidate.arm_id,
        schema_seed=candidate.schema_seed,
        seed_bundle_id=row.seed_bundle_id,
        training_replicate_index=row.training_replicate_index,
        episode_index=row.episode_index,
        step_index=row.step_index,
        controller_event_index=row.controller_event_index,
        source_state=row.source_state,
        action_repr=row.action_repr,
        reward=row.reward,
        target_state=row.target_state,
        terminated=row.terminated,
        truncated=row.truncated,
        active_tier_before=row.active_tier_before,
        active_tier_after=row.active_tier_after,
    )


def _control_row(row, *, run_mode: str, candidate: RuntimeCandidate) -> ComparisonControlEventRow:
    return ComparisonControlEventRow(
        evaluation_id=EVALUATION_ID,
        run_id=row.run_id,
        run_mode=run_mode,
        candidate_group_id=candidate.candidate_group_id,
        schema_class_id=candidate.schema_class_id,
        candidate_id=candidate.candidate_id,
        instance_id=row.instance_id,
        arm_id=candidate.arm_id,
        schema_seed=candidate.schema_seed,
        seed_bundle_id=row.seed_bundle_id,
        training_replicate_index=row.training_replicate_index,
        episode_index=row.episode_index,
        controller_event_index=row.controller_event_index,
        active_tier_before=row.active_tier_before,
        active_tier_after=row.active_tier_after,
        control_action=row.control_action,
        pressure=row.pressure,
        learner_updated=row.learner_updated,
        td_error=row.td_error,
        success=row.success,
    )


def _lift_row(row, *, run_mode: str, candidate: RuntimeCandidate) -> ComparisonLiftFiberEventRow:
    return ComparisonLiftFiberEventRow(
        evaluation_id=EVALUATION_ID,
        run_id=row.run_id,
        run_mode=run_mode,
        candidate_group_id=candidate.candidate_group_id,
        schema_class_id=candidate.schema_class_id,
        candidate_id=candidate.candidate_id,
        instance_id=row.instance_id,
        arm_id=candidate.arm_id,
        schema_seed=candidate.schema_seed,
        seed_bundle_id=row.seed_bundle_id,
        training_replicate_index=row.training_replicate_index,
        episode_index=row.episode_index,
        controller_event_index=row.controller_event_index,
        active_tier=row.active_tier,
        abstract_action=row.abstract_action,
        realized_action=row.realized_action,
        candidate_count=row.candidate_count,
        success=row.success,
        failure_reason=row.failure_reason,
        fiber_departure_reason=row.fiber_departure_reason,
    )


def _abc_selection_row(
    row,
    *,
    run_mode: str,
    candidate: RuntimeCandidate,
) -> ComparisonABCSelectionEventRow:
    return ComparisonABCSelectionEventRow(
        evaluation_id=EVALUATION_ID,
        run_id=row.run_id,
        run_mode=run_mode,
        candidate_group_id=candidate.candidate_group_id,
        schema_class_id=candidate.schema_class_id,
        candidate_id=candidate.candidate_id,
        instance_id=row.instance_id,
        arm_id=candidate.arm_id,
        schema_seed=candidate.schema_seed,
        seed_bundle_id=row.seed_bundle_id,
        training_replicate_index=row.training_replicate_index,
        episode_index=row.episode_index,
        controller_event_index=row.controller_event_index,
        active_tier_before=row.active_tier_before,
        active_tier_after=row.active_tier_after,
        deepest_known_tier=row.deepest_known_tier,
        selected_tier=row.selected_tier,
        selected_tier_executable=row.selected_tier_executable,
        predicted_movement_direction=row.predicted_movement_direction,
        control_action=row.control_action,
        decision_pressure=row.decision_pressure,
        training_due=row.training_due,
        action_consistent=row.action_consistent,
        blocked_reason=row.blocked_reason,
        concrete_step_emitted=row.concrete_step_emitted,
        lift_attempt_emitted=row.lift_attempt_emitted,
    )


def _abc_tier_signal_row(
    row,
    *,
    run_mode: str,
    candidate: RuntimeCandidate,
) -> ComparisonABCTierSignalEventRow:
    return ComparisonABCTierSignalEventRow(
        evaluation_id=EVALUATION_ID,
        run_id=row.run_id,
        run_mode=run_mode,
        candidate_group_id=candidate.candidate_group_id,
        schema_class_id=candidate.schema_class_id,
        candidate_id=candidate.candidate_id,
        instance_id=row.instance_id,
        arm_id=candidate.arm_id,
        schema_seed=candidate.schema_seed,
        seed_bundle_id=row.seed_bundle_id,
        training_replicate_index=row.training_replicate_index,
        episode_index=row.episode_index,
        controller_event_index=row.controller_event_index,
        active_tier_before=row.active_tier_before,
        selected_tier=row.selected_tier,
        tier_index=row.tier_index,
        executable=row.executable,
        visit_count=row.visit_count,
        td_error_ema=row.td_error_ema,
        success_count=row.success_count,
        failure_count=row.failure_count,
        success_rate=row.success_rate,
        reward_residual_ema=row.reward_residual_ema,
        has_reward_residual=row.has_reward_residual,
        productive_learning_pressure=row.productive_learning_pressure,
        unclosed=row.unclosed,
        selected=row.selected,
        active=row.active,
    )


def _learner_update_row(
    row,
    *,
    run_mode: str,
    candidate: RuntimeCandidate,
) -> ComparisonLearnerUpdateEventRow:
    return ComparisonLearnerUpdateEventRow(
        evaluation_id=EVALUATION_ID,
        run_id=row.run_id,
        run_mode=run_mode,
        candidate_group_id=candidate.candidate_group_id,
        schema_class_id=candidate.schema_class_id,
        candidate_id=candidate.candidate_id,
        instance_id=row.instance_id,
        arm_id=candidate.arm_id,
        schema_seed=candidate.schema_seed,
        seed_bundle_id=row.seed_bundle_id,
        training_replicate_index=row.training_replicate_index,
        episode_index=row.episode_index,
        controller_event_index=row.controller_event_index,
        active_tier=row.active_tier,
        success=row.success,
        td_error=row.td_error,
        update_reason=row.update_reason,
    )


def _tier_transition_row(
    row: ComparisonControlEventRow,
    *,
    candidate: RuntimeCandidate,
    tier_jump_policy: TierJumpPolicy,
) -> ComparisonTierTransitionEventRow:
    return ComparisonTierTransitionEventRow(
        evaluation_id=EVALUATION_ID,
        run_id=row.run_id,
        run_mode=row.run_mode,
        candidate_group_id=candidate.candidate_group_id,
        schema_class_id=candidate.schema_class_id,
        candidate_id=candidate.candidate_id,
        episode_index=row.episode_index,
        controller_event_index=row.controller_event_index,
        active_tier_before=row.active_tier_before,
        active_tier_after=row.active_tier_after,
        tier_jump_policy_id=tier_jump_policy.tier_jump_policy_id,
        tier_jump_reward_cutoff=tier_jump_policy.tier_jump_reward_cutoff,
        transition_observed=True,
        applicability="not_applicable_schema0"
        if candidate.schema_class_id == SCHEMA0_CLASS_ID
        else "observed_active_tier_controller_transition",
    )


def _tower_shape_summary_rows(
    *,
    build: CounterpointTowerBuildResult,
    candidate: RuntimeCandidate,
    run_id: str,
    run_mode: str,
    replicate_index: int,
) -> tuple[ComparisonTowerShapeSummaryRow, ...]:
    base_state_count = max(1, len(build.graph.states))
    rows = []
    for tier_index, state_layer in enumerate(build.tower.state_layers):
        cell_ids = tuple(state_layer.all_cell_ids())
        member_counts = [len(state_layer.members(cell_id)) for cell_id in cell_ids]
        state_cell_count = len(cell_ids)
        largest_share = max(member_counts, default=0) / base_state_count
        rows.append(
            ComparisonTowerShapeSummaryRow(
                evaluation_id=EVALUATION_ID,
                run_id=run_id,
                run_mode=run_mode,
                candidate_group_id=candidate.candidate_group_id,
                schema_class_id=candidate.schema_class_id,
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
            )
        )
    return tuple(rows)


def _run_index_row(
    artifact_root: Path,
    run_mode: str,
    record: ComparisonRunRecord,
) -> ComparisonRunIndexRow:
    result = record.result
    candidate = record.candidate
    return ComparisonRunIndexRow(
        evaluation_id=EVALUATION_ID,
        run_id="" if result is None else result.run_id,
        run_mode=run_mode,
        candidate_group_id=candidate.candidate_group_id,
        schema_class_id=candidate.schema_class_id,
        candidate_id=candidate.candidate_id,
        instance_id=candidate.instance_id,
        arm_id=candidate.arm_id,
        schema_seed=candidate.schema_seed,
        seed_bundle_id=record.seed_bundle.seed_bundle_id,
        training_replicate_index=record.seed_bundle.replicate_index,
        status=record.status,
        artifact_root=str(artifact_root),
        started_at="" if result is None else result.started_at,
        ended_at=None if result is None else result.ended_at,
        failure_reason=record.failure_reason,
    )


def _write_calibration_files(
    *,
    paths,
    records: list[ComparisonRunRecord],
    artifact_root: Path,
) -> None:
    run_rows = [_run_index_row(artifact_root, CALIBRATION_MODE_ID, record) for record in records]
    write_csv(
        paths.calibration_run_index_csv,
        [row.to_flat_dict() for row in run_rows],
        ComparisonRunIndexRow.fieldnames(),
    )
    rewards: list[float] = []
    for row in run_rows:
        if row.status != "success":
            continue
        run_root = _run_root(artifact_root, row.run_id)
        episode_path = run_root / "episodes.csv"
        if not episode_path.exists():
            continue
        import csv

        rewards.extend(
            float(item["total_reward"])
            for item in csv.DictReader(episode_path.open(encoding="utf-8"))
        )
    summary = {
        "evaluation_id": EVALUATION_ID,
        "run_mode": CALIBRATION_MODE_ID,
        "reward_count": len(rewards),
        "min_episode_total_reward": min(rewards) if rewards else None,
        "median_episode_total_reward": statistics.median(rewards) if rewards else None,
        "mean_episode_total_reward": statistics.mean(rewards) if rewards else None,
        "max_episode_total_reward": max(rewards) if rewards else None,
        "recommended_threshold_value": statistics.median(rewards) if rewards else None,
        "recommendation_rule": "median episode_total_reward across calibration runs",
    }
    write_json(paths.calibration_summary, summary, create_parents=True)
    text = (
        "# Calibration Recommendation\n\n"
        "This calibration file is advisory only. The serious run still requires an "
        "explicit locked `--threshold-value` before execution.\n\n"
        "```json\n"
        f"{json.dumps(summary, indent=2, sort_keys=True)}\n"
        "```\n"
    )
    paths.calibration_recommendation.write_text(text, encoding="utf-8")


def _run_root(artifact_root: Path, run_id: str) -> Path:
    return artifact_root / "runs" / EVALUATION_RUN_FAMILY_ID / "runs" / run_id


def _now() -> str:
    return datetime.now(UTC).isoformat()
