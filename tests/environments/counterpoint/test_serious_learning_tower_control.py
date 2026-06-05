import csv
import json
from pathlib import Path

from state_collapser.tower.control import LiftResolveExecutor, TierLearner

from big_boy_benchmarking.environments.counterpoint import ids
from big_boy_benchmarking.environments.counterpoint.instances import default_tiny_spec
from big_boy_benchmarking.environments.counterpoint.serious_learning.arms import (
    TOWER_EMPTY_ARM_ID,
    TOWER_MOTION_ARM_ID,
)
from big_boy_benchmarking.environments.counterpoint.serious_learning.config import (
    ExploitExploreControllerConfig,
    TabularQLearnerConfig,
)
from big_boy_benchmarking.environments.counterpoint.serious_learning.tower_control import (
    STATE_COLLAPSER_V072_POINTWISE_LIFTABILITY_SEMANTICS_ID,
    CounterpointLiftResolveExecutor,
    CounterpointTierLearner,
    CounterpointTowerControlAdapter,
    build_tier_configs,
    run_serious_tower_control,
)
from big_boy_benchmarking.metrics.timing import TimingRecorder
from big_boy_benchmarking.seeds.bundles import generate_seed_bundles


def test_active_tier_adapter_initializes_for_empty_schema() -> None:
    seed_bundle = generate_seed_bundles(base_seed=21, replicate_count=1)[0]
    adapter = CounterpointTowerControlAdapter(
        spec=default_tiny_spec(),
        schema_id=ids.EMPTY_SCHEMA_ID,
        schema_seed=None,
    )
    state = adapter.reset(seed_bundle=seed_bundle, episode_index=0)

    assert adapter.tower_depth >= 1
    assert state.active_tier == 0
    assert adapter.trace_fields(state)["active_tier"] == 0


def test_active_tier_adapter_initializes_for_motion_schema_and_moves_bounds() -> None:
    seed_bundle = generate_seed_bundles(base_seed=22, replicate_count=1)[0]
    adapter = CounterpointTowerControlAdapter(
        spec=default_tiny_spec(),
        schema_id=ids.STRUCTURED_MOTION_SCHEMA_ID,
        schema_seed=None,
    )
    state = adapter.reset(seed_bundle=seed_bundle, episode_index=0)

    if state.has_downstairs():
        down = adapter.move_down(state)
        assert down.active_tier == state.active_tier + 1
        up = adapter.move_up(down)
        assert up.active_tier == state.active_tier
    assert adapter.tier_is_executable(state.active_tier)
    assert not all(
        adapter.tier_is_executable(tier) for tier in range(1, adapter.tower_depth)
    )
    assert adapter.tier_is_executable(-1) is False
    assert adapter.tier_is_executable(adapter.tower_depth) is False


def test_tier_executable_delegates_to_pointwise_upstream_semantics() -> None:
    seed_bundle = generate_seed_bundles(base_seed=220, replicate_count=1)[0]
    adapter = CounterpointTowerControlAdapter(
        spec=default_tiny_spec(),
        schema_id=ids.STRUCTURED_MOTION_SCHEMA_ID,
        schema_seed=None,
    )
    adapter.reset(seed_bundle=seed_bundle, episode_index=0)

    assert adapter.current_core_state is not None
    for tier in range(adapter.tower_depth):
        assert adapter.tier_is_executable(tier) is bool(
            adapter.build.tower.tier_is_executable_from_state(
                tier,
                adapter.current_core_state,
            )
        )


def test_pointwise_vocabulary_is_ordered_subset_of_quotient_vocabulary() -> None:
    seed_bundle = generate_seed_bundles(base_seed=221, replicate_count=1)[0]
    adapter = CounterpointTowerControlAdapter(
        spec=default_tiny_spec(),
        schema_id=ids.STRUCTURED_MOTION_SCHEMA_ID,
        schema_seed=None,
    )
    adapter.reset(seed_bundle=seed_bundle, episode_index=0)

    for tier in range(adapter.tower_depth):
        quotient = adapter.quotient_action_cells(tier)
        pointwise = adapter.pointwise_executable_action_cells(tier)

        assert set(pointwise) <= set(quotient)
        assert pointwise == tuple(cell for cell in quotient if cell in pointwise)


def test_tier_learner_mask_uses_pointwise_vocabulary(monkeypatch) -> None:
    seed_bundle = generate_seed_bundles(base_seed=222, replicate_count=1)[0]
    recorder = TimingRecorder.create("tower-pointwise-mask-test")
    adapter = CounterpointTowerControlAdapter(
        spec=default_tiny_spec(),
        schema_id=ids.EMPTY_SCHEMA_ID,
        schema_seed=None,
        recorder=recorder,
    )
    active = adapter.reset(seed_bundle=seed_bundle, episode_index=0)
    learner = CounterpointTierLearner(
        adapter=adapter,
        learner_config=TabularQLearnerConfig(epsilon=0.0),
        controller_config=ExploitExploreControllerConfig(),
        seed=seed_bundle.learner_seed,
        recorder=recorder,
    )

    monkeypatch.setattr(adapter, "quotient_action_cells", lambda tier, state=None: ("q0",))
    monkeypatch.setattr(
        adapter,
        "pointwise_executable_action_cells",
        lambda tier, state=None: (),
    )

    action_input = learner._action_input(active.active_tier, active.tier_state)

    assert any(action_input.action_mask) is False
    assert action_input.diagnostics["quotient_action_cell_count"] == 1
    assert action_input.diagnostics["pointwise_executable_action_cell_count"] == 0
    assert (
        action_input.diagnostics["liftability_semantics_id"]
        == STATE_COLLAPSER_V072_POINTWISE_LIFTABILITY_SEMANTICS_ID
    )


def test_tier_learner_adapter_satisfies_protocol_and_trains() -> None:
    seed_bundle = generate_seed_bundles(base_seed=23, replicate_count=1)[0]
    recorder = TimingRecorder.create("tower-learner-test")
    adapter = CounterpointTowerControlAdapter(
        spec=default_tiny_spec(),
        schema_id=ids.EMPTY_SCHEMA_ID,
        schema_seed=None,
        recorder=recorder,
    )
    active = adapter.reset(seed_bundle=seed_bundle, episode_index=0)
    learner = CounterpointTierLearner(
        adapter=adapter,
        learner_config=TabularQLearnerConfig(epsilon=0.0),
        controller_config=ExploitExploreControllerConfig(training_interval=1),
        seed=seed_bundle.learner_seed,
        recorder=recorder,
    )
    executor = CounterpointLiftResolveExecutor(adapter=adapter, recorder=recorder)

    assert isinstance(learner, TierLearner)
    action = learner.behavior_action(active.tier_state, mode="explore")
    transition = executor.execute(
        active,
        action,
        frozen_context=__frozen_context(),
        mode="explore",
    )
    observed = learner.observe(transition, frozen_context=__frozen_context())
    trained = learner.train(frozen_context=__frozen_context())

    assert observed.td_error == 0.0
    assert trained.td_error is not None


def test_lift_resolve_executor_satisfies_protocol_and_records_trace() -> None:
    seed_bundle = generate_seed_bundles(base_seed=24, replicate_count=1)[0]
    recorder = TimingRecorder.create("tower-executor-test")
    adapter = CounterpointTowerControlAdapter(
        spec=default_tiny_spec(),
        schema_id=ids.EMPTY_SCHEMA_ID,
        schema_seed=None,
        recorder=recorder,
    )
    active = adapter.reset(seed_bundle=seed_bundle, episode_index=0)
    learner = CounterpointTierLearner(
        adapter=adapter,
        learner_config=TabularQLearnerConfig(epsilon=0.0),
        controller_config=ExploitExploreControllerConfig(),
        seed=seed_bundle.learner_seed,
        recorder=recorder,
    )
    executor = CounterpointLiftResolveExecutor(adapter=adapter, recorder=recorder)

    assert isinstance(executor, LiftResolveExecutor)
    transition = executor.execute(
        active,
        learner.behavior_action(active.tier_state, mode="explore"),
        frozen_context=__frozen_context(),
        mode="explore",
    )

    assert transition.success
    assert adapter.last_lift_trace is not None
    assert adapter.last_lift_trace.failure_reason is None


def test_lift_resolve_executor_does_not_use_representative_fallback(monkeypatch) -> None:
    seed_bundle = generate_seed_bundles(base_seed=240, replicate_count=1)[0]
    recorder = TimingRecorder.create("tower-executor-pointwise-test")
    adapter = CounterpointTowerControlAdapter(
        spec=default_tiny_spec(),
        schema_id=ids.EMPTY_SCHEMA_ID,
        schema_seed=None,
        recorder=recorder,
    )
    active = adapter.reset(seed_bundle=seed_bundle, episode_index=0)
    executor = CounterpointLiftResolveExecutor(adapter=adapter, recorder=recorder)
    strict_query_called = False

    def strict_candidates(tier, action_cell):  # noqa: ANN001
        nonlocal strict_query_called
        strict_query_called = True
        return ()

    monkeypatch.setattr(adapter, "quotient_action_cells", lambda tier, state=None: ("q0",))
    monkeypatch.setattr(
        adapter,
        "pointwise_executable_action_cells",
        lambda tier, state=None: ("q0",),
    )
    monkeypatch.setattr(
        adapter,
        "representative_lift_candidates",
        lambda tier, action_cell: ("representative_only",),
    )
    monkeypatch.setattr(adapter, "executable_lift_candidates", strict_candidates)
    monkeypatch.setattr(
        type(adapter.build.tower),
        "action_cell_members",
        lambda self, tier, action_cell: (_ for _ in ()).throw(
            AssertionError("representative fallback should not be used")
        ),
        raising=False,
    )

    transition = executor.execute(
        active,
        0,
        frozen_context=__frozen_context(),
        mode="explore",
    )

    assert strict_query_called
    assert transition.success is False
    assert adapter.last_lift_trace is not None
    assert adapter.last_lift_trace.failure_reason == "no_lift_candidate_from_current_state"
    assert adapter.last_lift_trace.representative_candidate_count == 1
    assert adapter.last_lift_trace.pointwise_candidate_count == 0
    assert (
        adapter.last_lift_trace.liftability_semantics_id
        == STATE_COLLAPSER_V072_POINTWISE_LIFTABILITY_SEMANTICS_ID
    )


def test_tower_control_episode_loop_writes_empty_schema_controller_rows(tmp_path) -> None:
    seed_bundle = generate_seed_bundles(base_seed=25, replicate_count=1)[0]
    result = run_serious_tower_control(
        spec=default_tiny_spec(),
        arm_id=TOWER_EMPTY_ARM_ID,
        seed_bundle=seed_bundle,
        artifact_root=tmp_path,
        episode_count=1,
    )
    control_rows = list(
        csv.DictReader(Path(result.artifact_paths["control_events_csv"]).open())
    )
    mode_manifest = json.loads(Path(result.artifact_paths["mode_manifest"]).read_text())

    assert result.status == "success"
    assert control_rows
    assert mode_manifest["mode_id"] == "tower_exploit_explore"
    assert mode_manifest["uses_compatibility_readout"] is False
    assert Path(result.artifact_paths["tower_invariant_report"]).exists()


def test_tower_control_motion_schema_writes_controller_or_lift_rows(tmp_path) -> None:
    seed_bundle = generate_seed_bundles(base_seed=26, replicate_count=1)[0]
    result = run_serious_tower_control(
        spec=default_tiny_spec(),
        arm_id=TOWER_MOTION_ARM_ID,
        seed_bundle=seed_bundle,
        artifact_root=tmp_path,
        episode_count=1,
    )
    control_rows = list(
        csv.DictReader(Path(result.artifact_paths["control_events_csv"]).open())
    )
    lift_path = Path(result.artifact_paths["lift_fiber_events_csv"])

    assert result.status == "success"
    assert control_rows
    assert lift_path.exists()


def test_build_tier_configs_covers_all_tiers() -> None:
    adapter = CounterpointTowerControlAdapter(
        spec=default_tiny_spec(),
        schema_id=ids.STRUCTURED_MOTION_SCHEMA_ID,
        schema_seed=None,
    )
    configs = build_tier_configs(adapter, ExploitExploreControllerConfig())

    assert set(configs) == set(range(adapter.tower_depth))


def __frozen_context():
    from state_collapser.tower.control import FrozenLowerContext

    return FrozenLowerContext(supporting_tier=None)
