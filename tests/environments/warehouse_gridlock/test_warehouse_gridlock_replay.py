import csv
import json
from pathlib import Path

from big_boy_benchmarking.cli.main import main
from big_boy_benchmarking.environments.warehouse_gridlock.actions import DirectionOrStay
from big_boy_benchmarking.environments.warehouse_gridlock.instances import load_instance
from big_boy_benchmarking.environments.warehouse_gridlock.masked_direct_vs_live_lift_tower import (
    events as masked_events,
)
from big_boy_benchmarking.environments.warehouse_gridlock.replay import (
    parse_state_id,
    render_episode_gif,
)
from big_boy_benchmarking.environments.warehouse_gridlock.transition import (
    action_from_overrides,
    step,
)


def test_parse_state_id_round_trips_stable_id() -> None:
    state = load_instance().start_state

    parsed = parse_state_id(state.stable_id)

    assert parsed.stable_id == state.stable_id


def test_render_episode_gif_from_step_events_path(tmp_path: Path) -> None:
    step_events = _write_recorded_episode(tmp_path / "step_events.csv")
    output = tmp_path / "episode.gif"

    result = render_episode_gif(
        step_events_path=step_events,
        episode_index=0,
        output_path=output,
        frame_ms=20,
        cell_pixels=16,
    )

    assert result.status == "success"
    assert result.frame_count == 3
    assert result.state_trajectory_hash
    assert result.action_trajectory_hash
    assert output.read_bytes()[:6] in {b"GIF87a", b"GIF89a"}


def test_cli_render_episode_selects_run_from_artifact_root(
    tmp_path: Path,
    capsys,
) -> None:
    artifact_root = tmp_path / "artifacts" / "movie_001"
    run_id = "warehouse-gridlock-test-run"
    run_root = artifact_root / "runs" / run_id
    step_events = _write_recorded_episode(run_root / "step_events.csv")
    _write_run_index(artifact_root / "run_index.csv", run_id=run_id, run_root=run_root)

    assert (
        main(
            [
                "warehouse-gridlock",
                "render-episode",
                "--artifact-root",
                str(artifact_root),
                "--arm-id",
                "warehouse_direct_admissible_masked",
                "--replicate-index",
                "0",
                "--schema-seed",
                "0",
                "--episode-index",
                "0",
                "--frame-ms",
                "20",
                "--cell-pixels",
                "16",
            ]
        )
        == 0
    )

    payload = json.loads(capsys.readouterr().out)
    output = Path(payload["output_path"])
    assert payload["status"] == "success"
    assert payload["step_events_path"] == str(step_events)
    assert payload["state_trajectory_hash"]
    assert payload["action_trajectory_hash"]
    assert output.exists()
    assert output.parent == artifact_root / "replays"


def _write_recorded_episode(path: Path) -> Path:
    instance = load_instance()
    first_action = action_from_overrides(
        instance.manifest.robot_ids,
        {"R17": DirectionOrStay.SOUTH},
    )
    first = step(instance=instance, state=instance.start_state, action=first_action)
    second_action = action_from_overrides(
        instance.manifest.robot_ids,
        {"R18": DirectionOrStay.SOUTH},
    )
    second = step(instance=instance, state=first.next_state, action=second_action)
    rows = [
        _step_row(
            state_id=instance.start_state.stable_id,
            action_id=first_action.stable_id,
            result_state_id=first.next_state.stable_id,
            reward=first.reward,
            step_index=0,
        ),
        _step_row(
            state_id=first.next_state.stable_id,
            action_id=second_action.stable_id,
            result_state_id=second.next_state.stable_id,
            reward=second.reward,
            step_index=1,
        ),
    ]
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=masked_events.STEP_FIELDNAMES)
        writer.writeheader()
        writer.writerows(rows)
    return path


def _step_row(
    *,
    state_id: str,
    action_id: str,
    result_state_id: str,
    reward: float,
    step_index: int,
) -> dict[str, object]:
    return {
        "run_id": "warehouse-gridlock-test-run",
        "arm_id": "warehouse_direct_admissible_masked",
        "replicate_index": 0,
        "schema_seed": 0,
        "episode_index": 0,
        "step_index": step_index,
        "state_id": state_id,
        "selected_action_id": action_id,
        "selected_action_summary": action_id,
        "valid": True,
        "reward": reward,
        "terminated": False,
        "truncated": False,
        "next_state_id": result_state_id,
        "correct_box_count": 0,
        "correct_robot_count": 0,
        "invalid_reasons": "",
    }


def _write_run_index(path: Path, *, run_id: str, run_root: Path) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=masked_events.RUN_INDEX_FIELDNAMES)
        writer.writeheader()
        writer.writerow(
            {
                "run_id": run_id,
                "arm_id": "warehouse_direct_admissible_masked",
                "replicate_index": 0,
                "schema_seed": 0,
                "episode_count": 1,
                "max_seconds_per_episode": 128,
                "candidate_proposals_per_step": 16,
                "max_active_robots": 8,
                "candidate_mix_id": "test",
                "run_root": str(run_root),
                "status": "success",
                "failure_reason": "",
            }
        )
