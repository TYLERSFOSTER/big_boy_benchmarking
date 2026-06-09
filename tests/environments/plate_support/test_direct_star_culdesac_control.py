import csv
import json
from pathlib import Path

from big_boy_benchmarking.cli.main import build_parser
from big_boy_benchmarking.environments.plate_support.direct_star_culdesac_control.aggregation import (
    build_direct_star_tables,
)
from big_boy_benchmarking.environments.plate_support.direct_star_culdesac_control.docs_writer import (
    write_direct_star_docs,
)
from big_boy_benchmarking.environments.plate_support.direct_star_culdesac_control.guards import (
    classify_primitive_transition,
    summarize_guard,
)
from big_boy_benchmarking.environments.plate_support.direct_star_culdesac_control.manifests import (
    build_direct_star_arms,
)
from big_boy_benchmarking.environments.plate_support.upstream import (
    import_plate_support_surface,
)


def test_direct_star_guards_mask_invalid_and_self_loop_actions() -> None:
    surface = import_plate_support_surface()

    raw = summarize_guard(surface, surface.START_STATE, "raw")
    invalid = summarize_guard(surface, surface.START_STATE, "invalid_guard")
    nonself = summarize_guard(surface, surface.START_STATE, "nonself_guard")

    assert raw.available_action_count_before_guard == surface.ACTION_COUNT
    assert raw.available_actions == tuple(range(surface.ACTION_COUNT))
    assert invalid.available_actions == (0, 1, 2, 3, 6, 8, 9, 10)
    assert invalid.invalid_guard_filtered_count == 4
    assert nonself.available_actions == invalid.available_actions
    assert nonself.self_loop_guard_filtered_count == 4

    blocked_action = classify_primitive_transition(surface, surface.START_STATE, 4)
    assert blocked_action.invalid_move is True
    assert blocked_action.self_loop is True
    assert blocked_action.valid_clipped_self_loop is False


def test_direct_star_guard_accepts_runtime_core_state_payload() -> None:
    surface = import_plate_support_surface()
    runtime = surface.create_runtime(schema=None)
    reset = runtime.reset(seed=0)

    core_state = reset.runtime_snapshot.current_base_state
    guarded = summarize_guard(surface, core_state, "nonself_guard")

    assert hasattr(core_state, "payload")
    assert guarded.available_actions == (0, 1, 2, 3, 6, 8, 9, 10)


def test_direct_star_arm_manifest_keeps_guarded_direct_separate() -> None:
    class Candidate:
        candidate_id = "candidate_a"
        schema_id = "plate_support_schema_source_local_ratio_iterated_1_over_144_i32_v001"
        schema_mode = "source_local_ratio_iterated"

    arms = build_direct_star_arms(Candidate())
    arm_ids = [arm.arm_id for arm in arms]

    assert arm_ids == [
        "direct_raw",
        "direct_invalid_guard",
        "direct_nonself_guard",
        "tower_selected_candidate",
    ]
    assert arms[1].information_mode == "oracle_one_step_local_transition"
    assert arms[2].information_mode == "oracle_one_step_local_transition"
    assert arms[3].information_mode == "executable_quotient_action_cells"


def test_direct_star_aggregation_handles_tower_guard_rows() -> None:
    class Candidate:
        candidate_id = "candidate_a"
        schema_id = "schema_a"
        schema_mode = "source_local_ratio_iterated"

    arms = build_direct_star_arms(Candidate())
    rows = build_direct_star_tables(
        arms=arms,
        seed_rows=[],
        run_index_rows=[],
        episode_rows=[],
        step_rows=[],
        guard_rows=[
            {
                "arm_id": "tower_selected_candidate",
                "guard_type": "tower_executable_action_cells",
                "information_mode": "executable_quotient_action_cells",
                "available_action_count_before_guard": 3,
                "available_action_count_after_guard": 3,
                "invalid_guard_filtered_count": 0,
                "self_loop_guard_filtered_count": 0,
                "all_actions_filtered_count": 0,
                "guard_fallback_used": False,
            }
        ],
        controller_rows=[],
        learner_rows=[],
        lift_rows=[],
        tier_rows=[],
        timing_rows=[],
    )

    assert rows["guard_filter_summary"][0]["mean_available_before_guard"] == 3.0
    assert rows["action_surface_summary"][0]["mean_available_action_count"] == 3.0


def test_direct_star_docs_escape_badge_text(tmp_path: Path) -> None:
    repo_root = tmp_path
    artifact_root = (
        tmp_path
        / "docs"
        / "evaluations"
        / "plate_support_5x5_default_v001"
        / "direct_star_culdesac_control"
        / "artifacts"
        / "guarded_001"
    )
    evaluation_root = artifact_root / "evaluations" / "plate_support_direct_star"
    output_paths = _write_minimal_readout_tables(tmp_path)
    docs = write_direct_star_docs(
        repo_root=repo_root,
        artifact_root=artifact_root,
        evaluation_root=evaluation_root,
        run_label="guarded_001",
        output_paths=output_paths,
        target={"target_policy_id": "target&policy"},
        interpretation_row={
            "interpretation_case": "tower_survives_nonself_guard",
            "tower_vs_raw_delta": 1.0,
            "tower_vs_invalid_guard_delta": 1.0,
            "tower_vs_nonself_guard_delta": 1.0,
            "allowed_claim": "bounded",
            "blocked_claim": "final",
        },
        badge_rows=[
            {
                "badge_id": "claim_boundary",
                "label": "Claim & Scope",
                "value": "Diagnostic <Only>",
                "color": "blue",
                "reason": "test",
                "source": "test",
            }
        ],
        parent_gauntlet_source=tmp_path / "parent" / "readout_source.json",
    )

    badge = Path(docs["badges/claim_boundary.svg"]).read_text(encoding="utf-8")
    source = json.loads(Path(docs["readout_source.json"]).read_text(encoding="utf-8"))
    assert "Claim &amp; Scope: Diagnostic &lt;Only&gt;" in badge
    assert "<rect" in badge
    assert 'fill="#555"' in badge
    assert source["information_parity_warning"]


def test_direct_star_cli_parser_accepts_run_and_summarize() -> None:
    parser = build_parser()

    run_args = parser.parse_args(
        [
            "plate-support",
            "direct-star-culdesac-control",
            "run",
            "--repo-root",
            ".",
            "--artifact-root",
            "docs/evaluations/plate_support_5x5_default_v001/direct_star_culdesac_control/artifacts/smoke_001",
            "--parent-gauntlet-source",
            "docs/evaluations/plate_support_5x5_default_v001/standard_gauntlet/readout_source.json",
            "--run-label",
            "smoke_001",
            "--locked-by",
            "pytest",
            "--smoke",
        ]
    )
    summarize_args = parser.parse_args(
        [
            "plate-support",
            "direct-star-culdesac-control",
            "summarize",
            "--repo-root",
            ".",
            "--artifact-root",
            "docs/evaluations/plate_support_5x5_default_v001/direct_star_culdesac_control/artifacts/smoke_001",
        ]
    )

    assert run_args.plate_support_command == "direct-star-culdesac-control"
    assert run_args.direct_star_culdesac_control_command == "run"
    assert run_args.smoke is True
    assert summarize_args.direct_star_culdesac_control_command == "summarize"


def _write_minimal_readout_tables(root: Path) -> dict[str, str]:
    results = root / "tables"
    results.mkdir()
    arm_fields = (
        "arm_id",
        "target_hit_rate",
        "mean_total_reward",
        "invalid_move_rate",
        "self_transition_rate",
        "invalid_move_count",
    )
    action_fields = ("arm_id", "mean_available_action_count")
    guard_fields = (
        "arm_id",
        "guard_type",
        "mean_available_before_guard",
        "mean_available_after_guard",
        "mean_invalid_filtered",
        "mean_self_loop_filtered",
    )
    timing_fields = ("arm_id", "run_id", "total_duration_seconds")
    arm_rows = [
        _arm_row("direct_raw", "0.1"),
        _arm_row("direct_invalid_guard", "0.2"),
        _arm_row("direct_nonself_guard", "0.3"),
        _arm_row("tower_selected_candidate", "0.4"),
    ]
    action_rows = [
        {"arm_id": row["arm_id"], "mean_available_action_count": "1.0"}
        for row in arm_rows
    ]
    guard_rows = [
        {
            "arm_id": row["arm_id"],
            "guard_type": "raw",
            "mean_available_before_guard": "1.0",
            "mean_available_after_guard": "1.0",
            "mean_invalid_filtered": "0.0",
            "mean_self_loop_filtered": "0.0",
        }
        for row in arm_rows
    ]
    timing_rows = [
        {"arm_id": row["arm_id"], "run_id": f"run-{index}", "total_duration_seconds": "0.1"}
        for index, row in enumerate(arm_rows)
    ]
    paths = {
        "arm_summary": results / "arm_summary.csv",
        "guard_filter_summary": results / "guard_filter_summary.csv",
        "action_surface_summary": results / "action_surface_summary.csv",
        "timing_summary": results / "timing_summary.csv",
    }
    _write_csv(paths["arm_summary"], arm_fields, arm_rows)
    _write_csv(paths["guard_filter_summary"], guard_fields, guard_rows)
    _write_csv(paths["action_surface_summary"], action_fields, action_rows)
    _write_csv(paths["timing_summary"], timing_fields, timing_rows)
    return {key: str(path) for key, path in paths.items()}


def _arm_row(arm_id: str, hit_rate: str) -> dict[str, str]:
    return {
        "arm_id": arm_id,
        "target_hit_rate": hit_rate,
        "mean_total_reward": "0.0",
        "invalid_move_rate": "0.0",
        "self_transition_rate": "0.0",
        "invalid_move_count": "0",
    }


def _write_csv(path: Path, fields: tuple[str, ...], rows: list[dict[str, str]]) -> None:
    with path.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=fields)
        writer.writeheader()
        writer.writerows(rows)
