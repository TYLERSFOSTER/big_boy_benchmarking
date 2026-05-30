from big_boy_benchmarking.environments.counterpoint.serious_learning.events import (
    ArmSummaryRow,
    ControllerEventRow,
    EvaluationRunIndexRow,
    LiftFiberEventRow,
    SeriousEpisodeRow,
    SeriousStepRow,
)


def test_serious_episode_row_serializes_with_stable_field_order() -> None:
    row = SeriousEpisodeRow(
        evaluation_id="eval",
        run_id="run",
        arm_id="direct_tabular_q",
        mode_id="direct_env_tabular",
        schema_id=None,
        schema_seed=None,
        seed_bundle_id="seed",
        replicate_index=0,
        episode_index=0,
        total_reward=1.0,
        step_count=2,
        terminated=True,
        truncated=False,
        success=True,
        final_state="state",
    )

    assert row.fieldnames()[0] == "evaluation_id"
    assert row.to_flat_dict()["schema_id"] is None


def test_direct_step_row_does_not_require_tower_fields() -> None:
    row = SeriousStepRow(
        evaluation_id="eval",
        run_id="run",
        arm_id="direct_masked_random",
        episode_index=0,
        step_index=0,
        source_state="s",
        action_id=1,
        action_repr="(0, 1, 0)",
        reward=0.5,
        target_state="t",
        terminated=False,
        truncated=False,
    )

    assert row.to_flat_dict()["active_tier_before"] is None
    assert row.to_flat_dict()["active_tier_after"] is None


def test_controller_and_lift_rows_include_tower_fields() -> None:
    controller = ControllerEventRow(
        evaluation_id="eval",
        run_id="run",
        arm_id="tower_motion_exploit_explore_tabular_q",
        episode_index=0,
        step_index=0,
        active_tier_before=1,
        active_tier_after=0,
        control_action="lift",
        pressure=0.2,
        learner_updated=False,
        td_error=None,
        success=None,
    )
    lift = LiftFiberEventRow(
        evaluation_id="eval",
        run_id="run",
        arm_id="tower_motion_exploit_explore_tabular_q",
        episode_index=0,
        step_index=0,
        active_tier=0,
        abstract_action="cell",
        realized_action="(0, 1, 0)",
        candidate_count=3,
        success=True,
        failure_reason=None,
        fiber_departure_reason=None,
    )

    assert controller.to_flat_dict()["control_action"] == "lift"
    assert lift.to_flat_dict()["candidate_count"] == 3


def test_run_index_and_arm_summary_rows_serialize() -> None:
    run_index = EvaluationRunIndexRow(
        evaluation_id="eval",
        run_id="run",
        arm_id="direct_tabular_q",
        mode_id="direct_env_tabular",
        schema_id=None,
        schema_seed=None,
        seed_bundle_id="seed",
        replicate_index=0,
        status="success",
        artifact_root="/tmp/artifacts",
        started_at="2026-05-29T00:00:00+00:00",
        ended_at=None,
    )
    summary = ArmSummaryRow(
        evaluation_id="eval",
        arm_id="direct_tabular_q",
        mode_id="direct_env_tabular",
        schema_family_id=None,
        run_count=1,
        episode_count=1,
        mean_return=1.0,
        std_return=0.0,
        mean_step_count=2.0,
        success_rate=1.0,
        status="complete",
    )

    assert run_index.fieldnames()[-1] == "ended_at"
    assert summary.to_flat_dict()["mean_return"] == 1.0
