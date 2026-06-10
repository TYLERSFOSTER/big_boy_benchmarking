import csv
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
from big_boy_benchmarking.environments.warehouse_gridlock.state import WarehouseGridlockState
from big_boy_benchmarking.environments.warehouse_gridlock.transition import action_from_overrides
from big_boy_benchmarking.environments.warehouse_gridlock.masked_direct_vs_live_lift_tower.admissibility import (
    mask_direct_candidates,
)
from big_boy_benchmarking.environments.warehouse_gridlock.masked_direct_vs_live_lift_tower.candidate_generation import (
    generate_direct_candidates,
)
from big_boy_benchmarking.environments.warehouse_gridlock.masked_direct_vs_live_lift_tower.config import (
    CANDIDATE_MIX_COORDINATION_READY,
    DIRECT_ARM_ID,
    TOWER_ARM_ID,
)
from big_boy_benchmarking.environments.warehouse_gridlock.masked_direct_vs_live_lift_tower.tower_surface import (
    build_tower_surface,
    select_live_lift,
)
from big_boy_benchmarking.environments.warehouse_gridlock.masked_direct_vs_live_lift_tower.warehouse_tower_adapter import (
    core_state_to_warehouse_state,
    primitive_action_to_warehouse_action,
    warehouse_action_to_primitive_action,
    warehouse_state_to_core_state,
)


def test_direct_candidate_generator_is_bounded_and_sparse() -> None:
    instance = load_instance()
    candidates = generate_direct_candidates(
        instance=instance,
        state=instance.start_state,
        budget=64,
        seed=0,
    )

    assert len(candidates) == 64
    assert candidates[0].is_all_stay
    assert max(candidate.active_robot_count for candidate in candidates) >= 2
    assert all(candidate.active_robot_count <= 3 for candidate in candidates)
    assert {candidate.metadata["candidate_family"] for candidate in candidates} >= {
        "all_stay",
        "one_active",
        "two_active",
        "three_active",
    }
    assert len(candidates) < 5 ** len(instance.manifest.robot_ids)


def test_direct_candidate_generator_respects_max_active_robot_knob() -> None:
    instance = load_instance()
    candidates = generate_direct_candidates(
        instance=instance,
        state=instance.start_state,
        budget=32,
        seed=0,
        max_active_robots=1,
        candidate_mix_id=CANDIDATE_MIX_COORDINATION_READY,
    )

    assert candidates[0].is_all_stay
    assert all(candidate.active_robot_count <= 1 for candidate in candidates)


def test_direct_immediate_mask_removes_currently_invalid_candidates() -> None:
    instance = load_instance()
    robots = dict(instance.start_state.robot_positions)
    robots["R01"] = GridNode(4, 3)
    state = WarehouseGridlockState(
        robot_positions=robots,
        box_positions=instance.start_state.box_positions,
        time_step=0,
    )
    candidates = [
        *generate_direct_candidates(instance=instance, state=state, budget=5, seed=0),
        generate_direct_candidates(instance=instance, state=state, budget=1, seed=1)[0],
    ]
    blocked = action_from_overrides(instance.manifest.robot_ids, {"R01": DirectionOrStay.EAST})
    candidates.append(
        candidates[0].__class__(
            candidate_id="manual-blocked",
            action=blocked,
            rank=999,
            generation_budget=999,
            generation_seed=0,
        )
    )

    mask = mask_direct_candidates(
        instance=instance,
        state=state,
        candidates=candidates,
        max_seconds=8,
    )

    assert mask.candidates_before == len(candidates)
    assert mask.inadmissible_count >= 1
    assert "manual-blocked" not in {
        candidate.candidate_id for candidate in mask.admissible_direct_candidates
    }


def test_tower_surface_has_live_lift_without_full_action_enumeration() -> None:
    instance = load_instance()
    surface = build_tower_surface(
        instance=instance,
        state=instance.start_state,
        candidate_budget=16,
        seed=0,
        schema_seed=0,
        max_seconds=8,
        max_active_robots=3,
        candidate_mix_id=CANDIDATE_MIX_COORDINATION_READY,
    )

    selected, reason = select_live_lift(surface)

    assert selected is not None, reason
    assert selected.out_count > 0
    assert not surface.complete_full_action_surface
    assert len(surface.direct_candidates) == 16


def test_warehouse_tower_adapter_round_trips_generated_state_and_action() -> None:
    instance = load_instance()
    action = action_from_overrides(instance.manifest.robot_ids, {"R17": DirectionOrStay.SOUTH})

    core_state = warehouse_state_to_core_state(instance.start_state)
    core_action = warehouse_action_to_primitive_action(action)

    assert core_state_to_warehouse_state(core_state).stable_id == instance.start_state.stable_id
    assert primitive_action_to_warehouse_action(core_action).stable_id == action.stable_id


def test_cli_smoke_writes_readout_and_no_lookahead_audit(tmp_path: Path, capsys) -> None:
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
        / "masked_direct_vs_live_lift_tower"
        / "artifacts"
        / "smoke_001"
    )

    assert (
        main(
            [
                "warehouse-gridlock",
                "masked-direct-vs-live-lift-tower",
                "run",
                "--repo-root",
                str(tmp_path),
                "--artifact-root",
                str(artifact_root),
                "--readiness-source",
                str(readiness_source),
                "--run-label",
                "smoke_001",
                "--locked-by",
                "test",
                "--episodes-per-arm",
                "1",
                "--replicates-per-arm",
                "1",
                "--max-seconds-per-episode",
                "2",
                "--candidate-proposals-per-step",
                "8",
                "--max-active-robots",
                "3",
                "--candidate-mix-id",
                CANDIDATE_MIX_COORDINATION_READY,
                "--progress-every-episodes",
                "1",
                "--schema-seeds",
                "1",
                "--smoke",
            ]
        )
        == 0
    )
    captured = capsys.readouterr()
    payload = json.loads(captured.out)
    assert payload["status"] == "success"
    assert "warehouse smoke_001" in captured.err
    assert "episode" in captured.err

    readout_source_path = (
        tmp_path
        / "docs"
        / "evaluations"
        / "warehouse_gridlock_001"
        / "masked_direct_vs_live_lift_tower"
        / "readout_source.json"
    )
    assert readout_source_path.exists()
    readout = json.loads(readout_source_path.read_text())
    assert readout["evaluation_id"].startswith("warehouse_gridlock_masked_direct")
    assert readout["summary"]["candidate_family_status"] == "coordination_ready"

    audit_path = artifact_root / "results" / "no_lookahead_audit_summary.csv"
    with audit_path.open(newline="", encoding="utf-8") as handle:
        rows = list(csv.DictReader(handle))
    assert {row["arm_id"] for row in rows} == {DIRECT_ARM_ID, TOWER_ARM_ID}
    assert all(row["successor_out_used_for_selection_count"] == "0.0" for row in rows)

    candidate_family_path = artifact_root / "results" / "candidate_family_summary.csv"
    with candidate_family_path.open(newline="", encoding="utf-8") as handle:
        candidate_family_rows = list(csv.DictReader(handle))
    assert {row["candidate_family"] for row in candidate_family_rows} >= {
        "one_active",
        "two_active",
        "three_active",
    }

    progress_path = artifact_root / "progress_events.jsonl"
    progress_rows = [
        json.loads(line)
        for line in progress_path.read_text(encoding="utf-8").splitlines()
        if line.strip()
    ]
    assert progress_rows[0]["event_type"] == "evaluation_start"
    assert any(row["event_type"] == "episode_complete" for row in progress_rows)
    assert progress_rows[-1]["event_type"] == "evaluation_complete"
