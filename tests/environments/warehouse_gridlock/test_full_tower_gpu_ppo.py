import csv
import json
from pathlib import Path

import pytest

from big_boy_benchmarking.cli.main import main
from big_boy_benchmarking.environments.warehouse_gridlock.docs_writer import (
    write_core_readiness_artifacts,
    write_readout_source as write_warehouse_readiness_source,
)
from big_boy_benchmarking.environments.warehouse_gridlock.full_tower_gpu_ppo.config import (
    WarehouseFullTowerPPOConfig,
    WarehousePPOHyperparameters,
    WarehousePolicyCapacityConfig,
)
from big_boy_benchmarking.environments.warehouse_gridlock.full_tower_gpu_ppo.ids import (
    WAREHOUSE_GRIDLOCK_DIRECT_NO_CONTRACTION_ARM_ID,
    WAREHOUSE_GRIDLOCK_FULL_TOWER_GPU_PPO_EVALUATION_ID,
    WAREHOUSE_GRIDLOCK_TOWER_FIRST_NONTRIVIAL_ARM_ID,
)
from big_boy_benchmarking.environments.warehouse_gridlock.full_tower_gpu_ppo.models import (
    TierCandidateActorCritic,
)
from big_boy_benchmarking.environments.warehouse_gridlock.full_tower_gpu_ppo.policy_bank import (
    TierPolicyBank,
)
from big_boy_benchmarking.environments.warehouse_gridlock.full_tower_gpu_ppo.records import (
    DecisionContextRecord,
    GeometryRecordValidationError,
    RolloutSampleRecord,
    ensure_no_mutable_geometry_payload,
)
from big_boy_benchmarking.environments.warehouse_gridlock.full_tower_gpu_ppo.tokenization import (
    CANDIDATE_FEATURE_DIM,
    CONTEXT_FEATURE_DIM,
    EncodedDecisionSurface,
)
from big_boy_benchmarking.environments.warehouse_gridlock.instances import load_instance
from big_boy_benchmarking.environments.warehouse_gridlock.masked_direct_vs_live_lift_tower.warehouse_tower_adapter import (
    core_state_to_warehouse_state,
    primitive_action_to_warehouse_action,
    warehouse_action_to_primitive_action,
    warehouse_state_to_core_state,
)
from big_boy_benchmarking.environments.warehouse_gridlock.transition import action_from_overrides


def test_full_tower_ppo_ids_are_stable() -> None:
    assert (
        WAREHOUSE_GRIDLOCK_FULL_TOWER_GPU_PPO_EVALUATION_ID
        == "warehouse_gridlock_full_tower_gpu_ppo_v001"
    )
    assert WAREHOUSE_GRIDLOCK_DIRECT_NO_CONTRACTION_ARM_ID != (
        WAREHOUSE_GRIDLOCK_TOWER_FIRST_NONTRIVIAL_ARM_ID
    )


def test_serious_gpu_profile_requires_confirmation(tmp_path: Path) -> None:
    with pytest.raises(ValueError, match="serious_gpu requires confirm_long_run"):
        WarehouseFullTowerPPOConfig(
            repo_root=tmp_path,
            artifact_root=tmp_path / "artifacts",
            readiness_source=tmp_path / "readout_source.json",
            profile_id="serious_gpu",
            confirm_long_run=False,
        )


def test_warehouse_adapter_payloads_are_hashable_and_round_trip() -> None:
    instance = load_instance()
    action = action_from_overrides(instance.manifest.robot_ids, {})

    core_state = warehouse_state_to_core_state(instance.start_state)
    core_action = warehouse_action_to_primitive_action(action)

    assert isinstance(hash(core_state), int)
    assert isinstance(hash(core_action), int)
    assert core_state_to_warehouse_state(core_state).stable_id == instance.start_state.stable_id
    assert primitive_action_to_warehouse_action(core_action).stable_id == action.stable_id


def test_record_contract_rejects_mutable_geometry_payload() -> None:
    with pytest.raises(GeometryRecordValidationError):
        ensure_no_mutable_geometry_payload(
            {"geometry_record_id": "g0", "old_log_prob": -1.0}
        )


def test_decision_context_requires_nonempty_pointwise_surface() -> None:
    with pytest.raises(ValueError, match="nonempty candidate surface"):
        DecisionContextRecord(
            decision_context_id="d0",
            episode_id="e0",
            replicate_index=0,
            schema_seed=0,
            arm_id=WAREHOUSE_GRIDLOCK_DIRECT_NO_CONTRACTION_ARM_ID,
            tier_index=0,
            ppo_sample_index=0,
            controller_event_index_start=0,
            controller_event_index_end=0,
            environment_second=0,
            active_tier=0,
            current_concrete_state_digest="s",
            current_position_at_every_tier=("s",),
            tower_position_key="s",
            runtime_snapshot_id="r",
            schema_arm_id=WAREHOUSE_GRIDLOCK_DIRECT_NO_CONTRACTION_ARM_ID,
            graph_snapshot_id="g",
            tower_snapshot_id="t",
            state_geometry_record_id="sg",
            candidate_action_ids_ordered=(),
            candidate_local_indices=(),
            candidate_mask=(),
            mask_kind="pointwise_executable",
            mask_semantics_id="sem",
            state_collapser_source_ref="state_collapser.PartitionTower",
            controller_event_refs=(),
        )


def test_rollout_sample_rejects_masked_selected_candidate() -> None:
    with pytest.raises(ValueError, match="selected candidate is masked"):
        RolloutSampleRecord(
            rollout_sample_id="r0",
            decision_context_id="d0",
            tier_index=0,
            policy_snapshot_id="p0",
            rollout_policy_snapshot_id="rp0",
            state_history_ref="s",
            action_history_ref="a",
            candidate_action_ids_ordered=("a0", "a1"),
            candidate_mask=(True, False),
            selected_local_index=1,
            selected_action_cell_id="a1",
            old_log_prob=-0.5,
            value_estimate=0.0,
            entropy=0.0,
            resolved_concrete_action_digest="x",
            lift_candidate_id="l",
            lift_candidate_digest="ld",
            lift_semantics_id="sem",
            reward=0.0,
            next_decision_context_id=None,
            terminated=False,
            truncated=False,
            bootstrap_value=None,
            diagnostic_failure_code=None,
        )


def test_masked_candidate_model_zeroes_masked_probability() -> None:
    torch = pytest.importorskip("torch")
    model = TierCandidateActorCritic(hidden_dim=16)
    encoded = EncodedDecisionSurface(
        context_features=[0.0] * CONTEXT_FEATURE_DIM,
        candidate_features=[[0.0] * CANDIDATE_FEATURE_DIM for _ in range(3)],
        candidate_mask=[True, False, True],
        candidate_ids=["a0", "a1", "a2"],
    )

    output = model.forward_encoded(encoded)

    assert torch.isclose(output.probabilities[1], torch.tensor(0.0))
    assert torch.isfinite(output.probabilities).all()
    assert torch.isclose(output.probabilities.sum(), torch.tensor(1.0))


def test_policy_bank_creates_distinct_frozen_rollout_models_per_tier() -> None:
    pytest.importorskip("torch")
    bank = TierPolicyBank(
        capacity=WarehousePolicyCapacityConfig(capacity_0=16, min_capacity=8),
        ppo=WarehousePPOHyperparameters(),
    )

    tier0 = bank.entry_for_tier(0)
    tier1 = bank.entry_for_tier(1)

    assert tier0.policy is not tier0.rollout_policy
    assert tier0.policy is not tier1.policy
    assert all(not parameter.requires_grad for parameter in tier0.rollout_policy.parameters())


def test_full_tower_ppo_cli_smoke_writes_readout_updates_and_movie(
    tmp_path: Path,
    capsys,
) -> None:
    pytest.importorskip("torch", reason="Torch optional ML dependency is not installed")
    readiness_source = _write_readiness_source(tmp_path)
    artifact_root = (
        tmp_path
        / "docs"
        / "evaluations"
        / "warehouse_gridlock_001"
        / "full_tower_gpu_ppo"
        / "artifacts"
        / "smoke_cpu_001"
    )

    assert (
        main(
            [
                "warehouse-gridlock",
                "full-tower-gpu-ppo",
                "inspect",
                "--repo-root",
                str(tmp_path),
                "--artifact-root",
                str(artifact_root),
                "--readiness-source",
                str(readiness_source),
                "--run-label",
                "smoke_cpu_001",
                "--profile",
                "smoke_cpu",
            ]
        )
        == 0
    )
    inspect_payload = json.loads(capsys.readouterr().out)
    assert inspect_payload["status"] == "ok"
    assert inspect_payload["evaluation_id"] == WAREHOUSE_GRIDLOCK_FULL_TOWER_GPU_PPO_EVALUATION_ID

    assert (
        main(
            [
                "warehouse-gridlock",
                "full-tower-gpu-ppo",
                "run",
                "--repo-root",
                str(tmp_path),
                "--artifact-root",
                str(artifact_root),
                "--readiness-source",
                str(readiness_source),
                "--run-label",
                "smoke_cpu_001",
                "--locked-by",
                "test",
                "--profile",
                "smoke_cpu",
                "--episodes-per-arm",
                "1",
                "--replicates-per-arm",
                "1",
                "--schema-seeds",
                "1",
                "--max-seconds-per-episode",
                "4",
                "--no-progress",
            ]
        )
        == 0
    )
    run_payload = json.loads(capsys.readouterr().out)
    assert run_payload["status"] == "success"

    summary = json.loads((artifact_root / "evaluation_aggregate_summary.json").read_text())
    assert summary["optimizer_steps"] > 0
    assert summary["representative_fallback_count"] == 0
    assert summary["empty_actor_surface_count"] == 0

    update_rows = _csv_rows(artifact_root / "results" / "ppo_update_summary.csv")
    assert update_rows
    assert all(float(row["approx_kl"]) == float(row["approx_kl"]) for row in update_rows)
    assert (artifact_root / "results" / "trace_episode_index.csv").exists()
    full_debug_run_roots = list((artifact_root / "runs").glob("*"))
    assert full_debug_run_roots
    assert any((run_root / "step_events.csv").exists() for run_root in full_debug_run_roots)

    assert (
        main(
            [
                "warehouse-gridlock",
                "full-tower-gpu-ppo",
                "summarize",
                "--repo-root",
                str(tmp_path),
                "--artifact-root",
                str(artifact_root),
                "--run-label",
                "smoke_cpu_001",
            ]
        )
        == 0
    )
    readout_source = (
        tmp_path
        / "docs"
        / "evaluations"
        / "warehouse_gridlock_001"
        / "full_tower_gpu_ppo"
        / "readout_source.json"
    )
    assert readout_source.exists()

    movie = tmp_path / "direct_ep0.gif"
    assert (
        main(
            [
                "warehouse-gridlock",
                "full-tower-gpu-ppo",
                "render-episode",
                "--artifact-root",
                str(artifact_root),
                "--arm-id",
                WAREHOUSE_GRIDLOCK_DIRECT_NO_CONTRACTION_ARM_ID,
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


def test_full_tower_ppo_movie_only_retains_renderable_trace_without_full_debug_tables(
    tmp_path: Path,
    capsys,
) -> None:
    pytest.importorskip("torch", reason="Torch optional ML dependency is not installed")
    readiness_source = _write_readiness_source(tmp_path)
    artifact_root = (
        tmp_path
        / "docs"
        / "evaluations"
        / "warehouse_gridlock_001"
        / "full_tower_gpu_ppo"
        / "artifacts"
        / "movie_only_001"
    )

    assert (
        main(
            [
                "warehouse-gridlock",
                "full-tower-gpu-ppo",
                "run",
                "--repo-root",
                str(tmp_path),
                "--artifact-root",
                str(artifact_root),
                "--readiness-source",
                str(readiness_source),
                "--run-label",
                "movie_only_001",
                "--locked-by",
                "test",
                "--profile",
                "smoke_cpu",
                "--retention-profile",
                "movie_only",
                "--active-arm-id",
                WAREHOUSE_GRIDLOCK_DIRECT_NO_CONTRACTION_ARM_ID,
                "--episodes-per-arm",
                "1",
                "--replicates-per-arm",
                "1",
                "--schema-seeds",
                "1",
                "--max-seconds-per-episode",
                "2",
                "--no-progress",
            ]
        )
        == 0
    )
    run_payload = json.loads(capsys.readouterr().out)
    assert run_payload["status"] == "success"

    summary = json.loads((artifact_root / "evaluation_aggregate_summary.json").read_text())
    assert summary["retained_trace_count"] >= 1
    assert summary["pointwise_surface_row_count"] >= 1

    run_roots = list((artifact_root / "runs").glob("*"))
    assert len(run_roots) == 1
    assert (run_roots[0] / "episodes.csv").exists()
    assert not (run_roots[0] / "step_events.csv").exists()
    assert not (run_roots[0] / "control_events.csv").exists()
    assert not (run_roots[0] / "rollout_samples.csv").exists()

    assert _csv_rows(artifact_root / "results" / "step_summary.csv") == []
    assert _csv_rows(artifact_root / "results" / "pointwise_action_surface_summary.csv") == []
    trace_rows = _csv_rows(artifact_root / "results" / "trace_episode_index.csv")
    assert trace_rows
    assert Path(trace_rows[0]["trace_path"]).exists()

    movie = tmp_path / "movie_only_ep0.gif"
    assert (
        main(
            [
                "warehouse-gridlock",
                "full-tower-gpu-ppo",
                "render-episode",
                "--artifact-root",
                str(artifact_root),
                "--arm-id",
                WAREHOUSE_GRIDLOCK_DIRECT_NO_CONTRACTION_ARM_ID,
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


def _csv_rows(path: Path) -> list[dict[str, str]]:
    with path.open(newline="", encoding="utf-8") as handle:
        return list(csv.DictReader(handle))
