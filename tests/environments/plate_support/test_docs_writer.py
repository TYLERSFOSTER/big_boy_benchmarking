from pathlib import Path

from big_boy_benchmarking.environments.plate_support.docs_writer import (
    write_artifact_index,
    write_plate_support_environment_docs,
)


def test_plate_support_docs_writer_creates_environment_doc_and_artifact_index(
    tmp_path: Path,
) -> None:
    summary = {
        "graph_summary": {
            "candidate_state_count": 2700,
            "valid_state_count": 89,
            "reachable_state_count": 89,
            "action_count": 12,
            "valid_nonself_edge_count": 388,
            "invalid_move_count": 496,
            "valid_self_transition_count": 184,
            "shortest_path_length": 6,
            "goal_one_step_from_start": False,
        },
        "random_policy_recon": {
            "episode_count": 1,
            "success_count": 0,
            "success_rate": 0.0,
            "mean_total_reward": -50.0,
            "invalid_move_rate": 0.5,
        },
        "tower_probe": [
            {
                "schema_id": "upstream_default_plate_support_schema_v001",
                "upstream_schema_mode": "default",
                "max_depth": 2,
                "scheduled_assignment_count": 84,
            }
        ],
        "training_surface_availability": {"run_tower_training": True},
    }
    docs_path = write_plate_support_environment_docs(
        docs_path=tmp_path / "plate_support.md",
        artifact_root=tmp_path / "artifacts",
        summary=summary,
        artifact_index_path=tmp_path / "artifact_index.md",
        readout_source_path=tmp_path / "readout_source.json",
        command_line="uv run python -m big_boy_benchmarking.cli plate-support readiness",
    )
    index_path = write_artifact_index(
        artifact_index_path=tmp_path / "artifact_index.md",
        artifact_paths={"graph_summary": str(tmp_path / "graph_summary.json")},
    )

    assert docs_path.exists()
    assert index_path.exists()
    text = docs_path.read_text()
    assert "not an evaluation readout" in text
    assert "plate_support_5x5_default_v001" in text
