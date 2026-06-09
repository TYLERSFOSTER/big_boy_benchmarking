from pathlib import Path

from big_boy_benchmarking.cli.main import build_parser
from big_boy_benchmarking.environments.plate_support.tower_star.config import (
    CURRENT_LIFT_EXECUTABLE_GUARD,
    DIRECT_INVALID_GUARD_ARM_ID,
    DIRECT_NONSELF_GUARD_ARM_ID,
    DIRECT_RAW_ARM_ID,
    INVALID_GUARD,
    NONSELF_GUARD,
    TOWER_INVALID_GUARD_ARM_ID,
    TOWER_LIFT_EXECUTABLE_CURRENT_ARM_ID,
    TOWER_NONSELF_GUARD_ARM_ID,
)
from big_boy_benchmarking.environments.plate_support.tower_star.manifests import (
    build_tower_star_arms,
)
from big_boy_benchmarking.environments.plate_support.tower_star.tower_lifts import (
    TowerActionCellSurface,
    TowerStarActionChoice,
    TowerLiftCandidate,
    lift_surface_rows,
)


class _Candidate:
    candidate_id = "candidate_a"
    schema_id = "plate_support_schema_source_local_ratio_iterated_1_over_144_i32_v001"
    schema_mode = "source_local_ratio_iterated"


class _Bundle:
    pair_id = "pair-0000"
    replicate_index = 0


class _Edge:
    source = "s0"
    target = "s1"


def test_tower_star_arm_manifest_has_direct_and_tower_star_controls() -> None:
    arms = build_tower_star_arms(_Candidate())
    arm_ids = [arm.arm_id for arm in arms]

    assert arm_ids == [
        DIRECT_RAW_ARM_ID,
        DIRECT_INVALID_GUARD_ARM_ID,
        DIRECT_NONSELF_GUARD_ARM_ID,
        TOWER_LIFT_EXECUTABLE_CURRENT_ARM_ID,
        TOWER_INVALID_GUARD_ARM_ID,
        TOWER_NONSELF_GUARD_ARM_ID,
    ]
    assert [arm.arm_type for arm in arms] == [
        "direct_concrete_baseline",
        "direct_guarded_baseline",
        "direct_guarded_baseline",
        "tower_candidate",
        "tower_candidate",
        "tower_candidate",
    ]
    assert arms[3].guard_type == CURRENT_LIFT_EXECUTABLE_GUARD
    assert arms[4].guard_type == INVALID_GUARD
    assert arms[5].guard_type == NONSELF_GUARD


def test_tower_star_surface_filters_lifts_before_action_cell_selection() -> None:
    invalid_lift = _lift(
        edge_id="bad-invalid",
        action_index=4,
        invalid=True,
        self_loop=True,
        nonself=False,
    )
    self_loop_lift = _lift(
        edge_id="bad-self",
        action_index=5,
        invalid=False,
        self_loop=True,
        nonself=False,
    )
    clean_lift = _lift(
        edge_id="clean",
        action_index=0,
        invalid=False,
        self_loop=False,
        nonself=True,
    )
    surface = TowerActionCellSurface(
        tier=2,
        state_cell_id="state-cell",
        action_cell_id="action-cell",
        candidate_lift_count=3,
        executable_lift_count=3,
        lifts=(invalid_lift, self_loop_lift, clean_lift),
    )

    assert surface.guarded_lifts(CURRENT_LIFT_EXECUTABLE_GUARD) == (
        invalid_lift,
        self_loop_lift,
        clean_lift,
    )
    assert surface.guarded_lifts(INVALID_GUARD) == (self_loop_lift, clean_lift)
    assert surface.guarded_lifts(NONSELF_GUARD) == (clean_lift,)


def test_tower_star_lift_rows_distinguish_current_tower_from_tower_star() -> None:
    arms = build_tower_star_arms(_Candidate())
    current_arm = arms[3]
    star_arm = arms[5]
    surface = TowerActionCellSurface(
        tier=1,
        state_cell_id="state-cell",
        action_cell_id="action-cell",
        candidate_lift_count=2,
        executable_lift_count=2,
        lifts=(
            _lift(
                edge_id="bad-self",
                action_index=0,
                invalid=False,
                self_loop=True,
                nonself=False,
            ),
            _lift(
                edge_id="clean",
                action_index=5,
                invalid=False,
                self_loop=False,
                nonself=True,
            ),
        ),
    )

    current_rows = lift_surface_rows(
        arm=current_arm,
        bundle=_Bundle(),
        run_id="current-run",
        episode_index=0,
        step_index=0,
        surfaces=[surface],
        selected_choice=_choice(surface=surface, selected_lift=surface.lifts[0]),
    )
    star_rows = lift_surface_rows(
        arm=star_arm,
        bundle=_Bundle(),
        run_id="star-run",
        episode_index=0,
        step_index=0,
        surfaces=[surface],
        selected_choice=_choice(surface=surface, selected_lift=surface.lifts[1]),
    )

    assert current_rows[0]["selected_by_current_tower"] is True
    assert current_rows[0]["selected_by_tower_star"] is False
    assert current_rows[0]["selected_lift_self_loop"] is True
    assert star_rows[0]["selected_by_current_tower"] is False
    assert star_rows[0]["selected_by_tower_star"] is True
    assert star_rows[0]["selected_lift_nonself_transition"] is True
    assert star_rows[0]["action_cell_available_after_nonself_star"] is True


def test_tower_star_cli_parser_accepts_run_and_summarize() -> None:
    parser = build_parser()
    artifact_root = (
        "docs/evaluations/plate_support_5x5_default_v001/tower_star/"
        "artifacts/tower_star_001"
    )

    run_args = parser.parse_args(
        [
            "plate-support",
            "tower-star",
            "run",
            "--repo-root",
            ".",
            "--artifact-root",
            artifact_root,
            "--parent-gauntlet-source",
            "docs/evaluations/plate_support_5x5_default_v001/standard_gauntlet/readout_source.json",
            "--direct-star-source",
            "docs/evaluations/plate_support_5x5_default_v001/direct_star_culdesac_control/readout_source.json",
            "--run-label",
            "tower_star_001",
            "--locked-by",
            "pytest",
            "--smoke",
        ]
    )
    summarize_args = parser.parse_args(
        [
            "plate-support",
            "tower-star",
            "summarize",
            "--repo-root",
            ".",
            "--artifact-root",
            artifact_root,
        ]
    )

    assert run_args.plate_support_command == "tower-star"
    assert run_args.tower_star_command == "run"
    assert run_args.direct_star_source == Path(
        "docs/evaluations/plate_support_5x5_default_v001/direct_star_culdesac_control/"
        "readout_source.json"
    )
    assert run_args.smoke is True
    assert summarize_args.tower_star_command == "summarize"


def _lift(
    *,
    edge_id: str,
    action_index: int,
    invalid: bool,
    self_loop: bool,
    nonself: bool,
) -> TowerLiftCandidate:
    return TowerLiftCandidate(
        tier=0,
        state_cell_id="state-cell",
        action_cell_id="action-cell",
        edge_id=edge_id,
        action_index=action_index,
        source_state_id="s0",
        next_state_id="s1",
        primitive_invalid_move=invalid,
        primitive_self_loop=self_loop,
        primitive_valid_clipped_self_loop=self_loop and not invalid,
        primitive_nonself_transition=nonself,
        invalid_guard_compatible=not invalid,
        nonself_guard_compatible=nonself,
        edge=_Edge(),
    )


def _choice(
    *,
    surface: TowerActionCellSurface,
    selected_lift: TowerLiftCandidate,
) -> TowerStarActionChoice:
    return TowerStarActionChoice(
        tier=surface.tier,
        state_cell_id=surface.state_cell_id,
        action_cell_id=surface.action_cell_id,
        action_index=selected_lift.action_index,
        candidate_lift_count=surface.candidate_lift_count,
        executable_lift_count=surface.executable_lift_count,
        guarded_lift_count=1,
        selected_lift=selected_lift,
        selected_edge=selected_lift.edge,
        q_key=(str(surface.tier), str(surface.state_cell_id), str(surface.action_cell_id)),
        q_value=0.0,
        surface=surface,
    )
