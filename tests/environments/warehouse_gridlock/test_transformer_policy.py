import json
from pathlib import Path

import pytest

from big_boy_benchmarking.cli.main import main
from big_boy_benchmarking.environments.warehouse_gridlock.docs_writer import (
    write_core_readiness_artifacts,
)
from big_boy_benchmarking.environments.warehouse_gridlock.docs_writer import (
    write_readout_source as write_warehouse_readiness_source,
)
from big_boy_benchmarking.environments.warehouse_gridlock.instances import load_instance
from big_boy_benchmarking.environments.warehouse_gridlock.policies import (
    config_from_instance_state,
)
from big_boy_benchmarking.environments.warehouse_gridlock.transformer_policy.config import (
    TOWER_ARM_ID,
    TransformerModelConfig,
)
from big_boy_benchmarking.environments.warehouse_gridlock.transformer_policy.encoding import (
    WarehouseEncodingContext,
    encode_warehouse_batch,
)
from big_boy_benchmarking.environments.warehouse_gridlock.transformer_policy.model import (
    build_model,
)
from big_boy_benchmarking.environments.warehouse_gridlock.transformer_policy.torch_runtime import (
    TorchUnavailableError,
    torch_is_available,
)


def test_transformer_policy_cli_help_does_not_require_torch(capsys) -> None:
    with pytest.raises(SystemExit) as exc:
        main(["warehouse-gridlock", "transformer-policy", "--help"])
    assert exc.value.code == 0
    assert "run" in capsys.readouterr().out


def test_transformer_policy_run_fails_clearly_without_torch(tmp_path: Path) -> None:
    if torch_is_available():
        pytest.skip("Torch is available; missing-Torch failure path is not active")
    with pytest.raises(TorchUnavailableError):
        main(
            [
                "warehouse-gridlock",
                "transformer-policy",
                "run",
                "--repo-root",
                str(tmp_path),
                "--artifact-root",
                str(tmp_path / "artifacts"),
                "--locked-by",
                "test",
                "--episodes",
                "1",
                "--no-progress",
            ]
        )


@pytest.mark.skipif(
    not torch_is_available(),
    reason="Torch optional ML dependency is not installed",
)
def test_transformer_encoding_and_forward_shapes() -> None:
    torch = pytest.importorskip("torch")
    instance = load_instance()
    config = config_from_instance_state(
        instance=instance,
        state=instance.start_state,
        max_seconds_per_episode=8,
    )
    encoded = encode_warehouse_batch(
        [config],
        [
            WarehouseEncodingContext(
                arm_id=TOWER_ARM_ID,
                second=0,
                max_seconds=8,
                tier=1,
                tier_state_id="cell",
                live_lift_out_count=4,
                candidate_count=4,
            )
        ],
    )
    model = build_model(TransformerModelConfig(d_model=32, n_layers=1, n_heads=4, mlp_hidden=64))
    output = model(encoded)

    assert output.robot_action_logits.shape == (1, len(instance.manifest.robot_ids), 5)
    assert output.value.shape == (1,)
    assert torch.isfinite(output.robot_action_logits).all()


@pytest.mark.skipif(
    not torch_is_available(),
    reason="Torch optional ML dependency is not installed",
)
def test_transformer_policy_cli_smoke_writes_checkpoints_and_selected_traces(
    tmp_path: Path,
    capsys,
) -> None:
    readiness_source = _write_readiness_source(tmp_path)
    artifact_root = (
        tmp_path
        / "docs"
        / "evaluations"
        / "warehouse_gridlock_001"
        / "transformer_policy"
        / "artifacts"
        / "tower_transformer_smoke_001"
    )

    assert (
        main(
            [
                "warehouse-gridlock",
                "transformer-policy",
                "run",
                "--repo-root",
                str(tmp_path),
                "--artifact-root",
                str(artifact_root),
                "--readiness-source",
                str(readiness_source),
                "--run-label",
                "tower_transformer_smoke_001",
                "--locked-by",
                "test",
                "--episodes",
                "1",
                "--replicates",
                "1",
                "--schema-seeds",
                "1",
                "--max-seconds-start",
                "2",
                "--max-seconds-end",
                "2",
                "--curriculum-ramp-episodes",
                "1",
                "--checkpoint-every-episodes",
                "1",
                "--trace-episode-index",
                "0",
                "--no-progress",
            ]
        )
        == 0
    )
    payload = json.loads(capsys.readouterr().out)
    assert payload["status"] == "success"

    assert (artifact_root / "checkpoint_manifest.json").exists()
    assert (artifact_root / "results" / "trace_episode_index.csv").exists()
    assert (artifact_root / "results" / "episode_summary.csv").exists()
    assert not (artifact_root / "step_events.csv").exists()

    assert (
        main(
            [
                "warehouse-gridlock",
                "transformer-policy",
                "summarize",
                "--repo-root",
                str(tmp_path),
                "--artifact-root",
                str(artifact_root),
            ]
        )
        == 0
    )
    readout_source = (
        tmp_path
        / "docs"
        / "evaluations"
        / "warehouse_gridlock_001"
        / "transformer_policy"
        / "readout_source.json"
    )
    assert readout_source.exists()

    movie = tmp_path / "tower_ep0.gif"
    assert (
        main(
            [
                "warehouse-gridlock",
                "transformer-policy",
                "render-episode",
                "--artifact-root",
                str(artifact_root),
                "--arm-id",
                TOWER_ARM_ID,
                "--replicate-index",
                "0",
                "--schema-seed",
                "0",
                "--episode-index",
                "0",
                "--output",
                str(movie),
                "--cell-pixels",
                "16",
                "--frame-ms",
                "20",
            ]
        )
        == 0
    )
    assert movie.exists()


def _write_readiness_source(tmp_path: Path) -> Path:
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
    return write_warehouse_readiness_source(
        repo_root=tmp_path,
        artifact_root=readiness_root,
        artifact_paths=artifact_paths,
        instance=instance,
    )
