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
