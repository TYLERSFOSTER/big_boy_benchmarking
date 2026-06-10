import json
from pathlib import Path

from big_boy_benchmarking.cli.main import main
from big_boy_benchmarking.environments.warehouse_gridlock.actions import DirectionOrStay
from big_boy_benchmarking.environments.warehouse_gridlock.docs_writer import (
    write_core_readiness_artifacts,
    write_readout_source as write_warehouse_readiness_source,
)
from big_boy_benchmarking.environments.warehouse_gridlock.graph import GridNode
from big_boy_benchmarking.environments.warehouse_gridlock.instances import load_instance
from big_boy_benchmarking.environments.warehouse_gridlock.policies import (
    BoundedDeterministicWarehouseActionResolver,
    WarehouseFullActionVector,
    WarehouseLinearFactorizedSoftmaxPolicy,
    WarehouseMaskContext,
    WarehousePolicyRng,
    WarehousePolicyTransition,
    config_from_instance_state,
)
from big_boy_benchmarking.environments.warehouse_gridlock.state import WarehouseGridlockState


def _mask_context() -> WarehouseMaskContext:
    return WarehouseMaskContext(
        arm_id="warehouse_direct_full_state_policy_masked",
        run_id="run",
        episode_index=0,
        step_index=0,
        max_seconds_per_episode=8,
        projection_attempt_budget=64,
    )


def test_full_system_config_and_action_vector_contract() -> None:
    instance = load_instance()
    config = config_from_instance_state(
        instance=instance,
        state=instance.start_state,
        max_seconds_per_episode=128,
    )

    assert config.static.environment_instance_id == "warehouse_gridlock_16x16_v001"
    assert len(config.static.robot_ids) == 32
    assert len(config.static.box_ids) == 32
    assert config.dynamic.time_step == 0
    assert set(config.dynamic.robot_positions) == set(config.static.robot_ids)

    action = WarehouseFullActionVector.all_stay(config.static.robot_ids)
    assert action.validate(required_robot_ids=instance.manifest.robot_ids).ok
    assert action.stable_hash == WarehouseFullActionVector.all_stay(config.static.robot_ids).stable_hash

    missing = WarehouseFullActionVector(commands={"R01": DirectionOrStay.STAY})
    assert not missing.validate(required_robot_ids=instance.manifest.robot_ids).ok

    extra_commands = dict(action.commands)
    extra_commands["RX"] = DirectionOrStay.STAY
    extra = WarehouseFullActionVector(commands=extra_commands)
    assert not extra.validate(required_robot_ids=instance.manifest.robot_ids).ok


def test_linear_policy_emits_full_vector_and_updates_reusable_state() -> None:
    instance = load_instance()
    config = config_from_instance_state(
        instance=instance,
        state=instance.start_state,
        max_seconds_per_episode=8,
    )
    policy = WarehouseLinearFactorizedSoftmaxPolicy(policy_id="policy")
    decision = policy.act(
        full_system_config=config,
        second=0,
        rng=WarehousePolicyRng(seed=1),
        mask_context=_mask_context(),
    )

    assert set(decision.raw_action_vector.commands) == set(instance.manifest.robot_ids)
    before = policy.state_hash
    resolver = BoundedDeterministicWarehouseActionResolver()
    resolved = resolver.resolve(
        instance=instance,
        state=instance.start_state,
        raw_action_vector=decision.raw_action_vector,
        max_seconds=8,
        robot_command_margins=dict(decision.robot_command_margins),
    )
    post_config = config_from_instance_state(
        instance=instance,
        state=resolved.step_result.next_state,
        max_seconds_per_episode=8,
    )
    update = policy.update(
        transition=WarehousePolicyTransition(
            pre_config=config,
            pre_second=0,
            selected_full_action_vector=resolved.selected_action_vector,
            projection_trace=resolved.projection_trace,
            reward=resolved.step_result.reward,
            post_config=post_config,
            post_second=resolved.step_result.next_state.time_step,
            terminated=resolved.step_result.terminated,
            truncated=resolved.step_result.truncated,
            episode_index=0,
            step_index=0,
            step_result=resolved.step_result,
        )
    )

    assert update.non_noop_update
    assert policy.state_hash != before

    later = policy.act(
        full_system_config=post_config,
        second=post_config.dynamic.time_step,
        rng=WarehousePolicyRng(seed=2),
        mask_context=WarehouseMaskContext(
            arm_id="warehouse_direct_full_state_policy_masked",
            run_id="run",
            episode_index=0,
            step_index=1,
            max_seconds_per_episode=8,
            projection_attempt_budget=64,
        ),
    )
    assert later.prior_signal_used


def test_resolver_repairs_invalid_raw_vector_without_advancing_invalid_time() -> None:
    instance = load_instance()
    robots = dict(instance.start_state.robot_positions)
    robots["R01"] = GridNode(4, 3)
    state = WarehouseGridlockState(
        robot_positions=robots,
        box_positions=instance.start_state.box_positions,
        time_step=0,
    )
    commands = {robot_id: DirectionOrStay.STAY for robot_id in instance.manifest.robot_ids}
    commands["R01"] = DirectionOrStay.EAST
    raw = WarehouseFullActionVector(commands=commands)

    resolved = BoundedDeterministicWarehouseActionResolver().resolve(
        instance=instance,
        state=state,
        raw_action_vector=raw,
        max_seconds=8,
        robot_command_margins={"R01": -1.0},
    )

    assert not resolved.raw_step_result.valid
    assert resolved.raw_step_result.next_state.time_step == 0
    assert resolved.step_result.valid
    assert resolved.step_result.next_state.time_step == 1
    assert not resolved.projection_trace.successor_out_count_used_for_selection


def test_full_state_policy_cli_smoke_writes_learning_health(tmp_path: Path, capsys) -> None:
    readiness_root = (
        tmp_path
        / "docs"
        / "evaluations"
        / "warehouse_gridlock_001"
        / "environment_readiness"
        / "artifacts"
        / "smoke_001"
    )
    instance = load_instance()
    artifact_paths = write_core_readiness_artifacts(
        instance=instance,
        artifact_root=readiness_root,
        run_label="smoke_001",
    )
    readiness_source = write_warehouse_readiness_source(
        repo_root=tmp_path,
        artifact_root=readiness_root,
        artifact_paths=artifact_paths,
        instance=instance,
    )
    artifact_root = (
        tmp_path
        / "docs"
        / "evaluations"
        / "warehouse_gridlock_001"
        / "full_state_policy_comparison"
        / "artifacts"
        / "policy_contract_smoke_001"
    )

    assert (
        main(
            [
                "warehouse-gridlock",
                "full-state-policy-comparison",
                "run",
                "--repo-root",
                str(tmp_path),
                "--artifact-root",
                str(artifact_root),
                "--readiness-source",
                str(readiness_source),
                "--run-label",
                "policy_contract_smoke_001",
                "--locked-by",
                "test",
                "--episodes-per-arm",
                "1",
                "--replicates-per-arm",
                "1",
                "--schema-seeds",
                "1",
                "--max-seconds-per-episode",
                "2",
                "--projection-attempt-budget",
                "8",
                "--no-progress",
            ]
        )
        == 0
    )
    payload = json.loads(capsys.readouterr().out)
    assert payload["status"] == "success"

    learning_health = artifact_root / "results" / "learning_health_summary.csv"
    readout_source = (
        tmp_path
        / "docs"
        / "evaluations"
        / "warehouse_gridlock_001"
        / "full_state_policy_comparison"
        / "readout_source.json"
    )
    assert learning_health.exists()
    assert readout_source.exists()
    assert "real_learning_signal_present" in learning_health.read_text(encoding="utf-8")

    assert (
        main(
            [
                "warehouse-gridlock",
                "full-state-policy-comparison",
                "summarize",
                "--repo-root",
                str(tmp_path),
                "--artifact-root",
                str(artifact_root),
            ]
        )
        == 0
    )
