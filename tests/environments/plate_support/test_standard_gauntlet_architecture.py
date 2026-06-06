from pathlib import Path

import pytest

from big_boy_benchmarking.environments.plate_support.standard_gauntlet import gates
from big_boy_benchmarking.environments.plate_support.standard_gauntlet.ids import (
    CANDIDATE_DISCOVERY_STAGE_ID,
    CONTRACTION_SCHEMA_SWEEP_STAGE_ID,
    ENVIRONMENT_FAMILY_ID,
    ENVIRONMENT_INSTANCE_ID,
    LINEARIZATION_MODE_ID,
    PAIRED_REPLICATE_COMPARISON_STAGE_ID,
    READOUT_SYSTEM_LEARNING_STAGE_ID,
    STAGE_DEFINITIONS,
    STAGE_IDS,
    STRUCTURAL_TOWER_DIAGNOSTICS_STAGE_ID,
    SUITE_ID,
    SUITE_RUN_FAMILY_ID,
    THRESHOLD_FRONTIER_CALIBRATION_STAGE_ID,
    TOWER_TRAINING_HEALTH_STAGE_ID,
)
from big_boy_benchmarking.environments.plate_support.standard_gauntlet.manifests import (
    SuiteManifestInputs,
    build_suite_manifests,
    required_budget_lock_keys,
)
from big_boy_benchmarking.environments.plate_support.standard_gauntlet.paths import (
    default_readiness_source_path,
    suite_artifact_root,
    suite_readout_surface,
)
from big_boy_benchmarking.environments.plate_support.standard_gauntlet.readout_source import (
    build_suite_readout_source,
)
from big_boy_benchmarking.environments.plate_support.standard_gauntlet.status import (
    CLAIM_STATUS_CANDIDATE_FOUND,
    CLAIM_STATUS_DIAGNOSTIC_COMPLETE,
    CLAIM_STATUS_THRESHOLD_CALIBRATED,
    CLAIM_STATUS_TRAINABLE_WARNING,
    CLAIM_STATUS_VOCABULARY,
    STAGE_STATUS_FIELDS,
    StageStatusRow,
    validate_claim_status,
)


def test_standard_gauntlet_ids_match_blueprint() -> None:
    assert SUITE_ID == "plate_support_standard_gauntlet_v001"
    assert SUITE_RUN_FAMILY_ID == "plate_support_standard_gauntlet_v001"
    assert ENVIRONMENT_FAMILY_ID == "plate_support"
    assert ENVIRONMENT_INSTANCE_ID == "plate_support_5x5_default_v001"
    assert LINEARIZATION_MODE_ID == "tensor_available_disabled"
    assert STAGE_IDS == (
        STRUCTURAL_TOWER_DIAGNOSTICS_STAGE_ID,
        CONTRACTION_SCHEMA_SWEEP_STAGE_ID,
        CANDIDATE_DISCOVERY_STAGE_ID,
        TOWER_TRAINING_HEALTH_STAGE_ID,
        THRESHOLD_FRONTIER_CALIBRATION_STAGE_ID,
        PAIRED_REPLICATE_COMPARISON_STAGE_ID,
        READOUT_SYSTEM_LEARNING_STAGE_ID,
    )


def test_stage_order_preserves_dependency_chain() -> None:
    assert [stage.stage_number for stage in STAGE_DEFINITIONS] == [1, 2, 3, 4, 5, 6, 7]
    assert STAGE_DEFINITIONS[1].required_predecessor_stage_ids == (
        STRUCTURAL_TOWER_DIAGNOSTICS_STAGE_ID,
    )
    assert STAGE_DEFINITIONS[2].required_predecessor_stage_ids == (
        CONTRACTION_SCHEMA_SWEEP_STAGE_ID,
    )
    assert STAGE_DEFINITIONS[3].required_predecessor_stage_ids == (
        CANDIDATE_DISCOVERY_STAGE_ID,
    )
    assert STAGE_DEFINITIONS[4].required_predecessor_stage_ids == (
        STRUCTURAL_TOWER_DIAGNOSTICS_STAGE_ID,
        TOWER_TRAINING_HEALTH_STAGE_ID,
    )
    assert STAGE_DEFINITIONS[5].required_predecessor_stage_ids == (
        CANDIDATE_DISCOVERY_STAGE_ID,
        TOWER_TRAINING_HEALTH_STAGE_ID,
        THRESHOLD_FRONTIER_CALIBRATION_STAGE_ID,
    )


def test_path_helpers_keep_readout_artifact_and_readiness_roles_separate() -> None:
    repo_root = Path(__file__).resolve().parents[3]
    surface = suite_readout_surface(repo_root)
    artifact_root = suite_artifact_root(repo_root, "smoke_001")
    readiness_source = default_readiness_source_path(repo_root)

    assert surface == (
        repo_root
        / "docs"
        / "evaluations"
        / "plate_support_5x5_default_v001"
        / "standard_gauntlet"
    )
    assert artifact_root == surface / "artifacts" / "smoke_001"
    assert "docs/evaluations" in artifact_root.as_posix()
    assert readiness_source == (
        repo_root
        / "docs"
        / "environments"
        / "plate_support_5x5_default_v001"
        / "readiness"
        / "dev_001"
        / "readout_source.json"
    )
    assert "docs/environments" in readiness_source.as_posix()


def test_path_helpers_do_not_use_current_working_directory(tmp_path: Path, monkeypatch) -> None:
    repo_root = Path(__file__).resolve().parents[3]
    monkeypatch.chdir(tmp_path)

    assert suite_artifact_root(repo_root, "dev_001") == (
        repo_root
        / "docs"
        / "evaluations"
        / "plate_support_5x5_default_v001"
        / "standard_gauntlet"
        / "artifacts"
        / "dev_001"
    )


def test_status_vocabulary_and_row_shape_match_blueprint() -> None:
    for status in (
        "environment_ready",
        "diagnostic_complete",
        "diagnostic_blocked",
        "candidate_found",
        "candidate_not_found",
        "trainable_clean",
        "trainable_warning",
        "training_health_blocked",
        "threshold_calibrated",
        "threshold_unresolved",
        "paired_comparison_positive_signal",
        "paired_comparison_negative_signal",
        "paired_comparison_inconclusive",
        "artifact_incomplete",
        "protocol_blocked",
    ):
        assert status in CLAIM_STATUS_VOCABULARY
        assert validate_claim_status(status) == status

    row = StageStatusRow(
        suite_id=SUITE_ID,
        stage_id=STRUCTURAL_TOWER_DIAGNOSTICS_STAGE_ID,
        environment_family_id=ENVIRONMENT_FAMILY_ID,
        environment_instance_id=ENVIRONMENT_INSTANCE_ID,
        artifact_root="/tmp/artifacts",
        status="complete",
        claim_status=CLAIM_STATUS_DIAGNOSTIC_COMPLETE,
        claim_boundary="diagnostic-only",
        source_stage_ids=(),
        source_artifact_paths=("readiness.json",),
        linearization_mode_id=LINEARIZATION_MODE_ID,
        state_collapser_dependency_status="available",
    )
    assert tuple(row.to_row().keys()) == STAGE_STATUS_FIELDS


def test_gate_dependency_contracts() -> None:
    assert not gates.gate_for_stage(CONTRACTION_SCHEMA_SWEEP_STAGE_ID).can_run(
        completed_statuses={},
        available_artifact_roles={"stage1_structural_tables", "stage1_tower_tables"},
    )
    assert gates.gate_for_stage(CONTRACTION_SCHEMA_SWEEP_STAGE_ID).can_run(
        completed_statuses={
            STRUCTURAL_TOWER_DIAGNOSTICS_STAGE_ID: CLAIM_STATUS_DIAGNOSTIC_COMPLETE,
        },
        available_artifact_roles={"stage1_structural_tables", "stage1_tower_tables"},
    )
    assert gates.gate_for_stage(CANDIDATE_DISCOVERY_STAGE_ID).required_predecessor_statuses == {
        CONTRACTION_SCHEMA_SWEEP_STAGE_ID: (CLAIM_STATUS_DIAGNOSTIC_COMPLETE,),
    }
    assert gates.gate_for_stage(TOWER_TRAINING_HEALTH_STAGE_ID).required_predecessor_statuses == {
        CANDIDATE_DISCOVERY_STAGE_ID: (CLAIM_STATUS_CANDIDATE_FOUND,),
    }
    assert gates.gate_for_stage(THRESHOLD_FRONTIER_CALIBRATION_STAGE_ID).can_run(
        completed_statuses={
            STRUCTURAL_TOWER_DIAGNOSTICS_STAGE_ID: CLAIM_STATUS_DIAGNOSTIC_COMPLETE,
            TOWER_TRAINING_HEALTH_STAGE_ID: CLAIM_STATUS_TRAINABLE_WARNING,
        },
        available_artifact_roles={
            "stage1_reward_scale_tables",
            "stage4_training_health_tables",
        },
    )
    assert gates.gate_for_stage(PAIRED_REPLICATE_COMPARISON_STAGE_ID).can_run(
        completed_statuses={
            CANDIDATE_DISCOVERY_STAGE_ID: CLAIM_STATUS_CANDIDATE_FOUND,
            TOWER_TRAINING_HEALTH_STAGE_ID: CLAIM_STATUS_TRAINABLE_WARNING,
            THRESHOLD_FRONTIER_CALIBRATION_STAGE_ID: CLAIM_STATUS_THRESHOLD_CALIBRATED,
        },
        available_artifact_roles={
            "stage3_candidate_manifest",
            "stage4_training_health_summary",
            "stage5_threshold_policy",
            "matched_seed_policy",
        },
    )
    assert gates.gate_for_stage(READOUT_SYSTEM_LEARNING_STAGE_ID).can_run(
        completed_statuses={},
        available_artifact_roles={"stage1_structural_tables"},
    )


def test_suite_manifest_builders_require_explicit_context() -> None:
    repo_root = Path(__file__).resolve().parents[3]
    inputs = SuiteManifestInputs(
        repo_root=repo_root,
        run_label="smoke_001",
        stage_ids_included=STAGE_IDS[:1],
        locked_by="pytest",
        state_collapser_dependency_state={"status": "available"},
        seed_bundle_policy={"policy": "stage-local"},
        replicate_policy={"replicates": 1},
        episode_step_budget={"episodes": 0, "max_steps": 0},
        threshold_or_success_rule={"status": "not_yet_calibrated"},
        candidate_source={"status": "not_yet_selected"},
    )
    manifests = build_suite_manifests(inputs)
    assert set(manifests) == {
        "evaluation_manifest",
        "evaluation_stage_manifest",
        "evaluation_budget_lock",
        "environment_source_manifest",
        "readiness_source_manifest",
    }
    budget = manifests["evaluation_budget_lock"]
    for key in required_budget_lock_keys():
        assert key in budget


def test_suite_readout_source_distinguishes_surface_and_artifact_root() -> None:
    repo_root = Path(__file__).resolve().parents[3]
    source = build_suite_readout_source(repo_root, "smoke_001")

    readout_surface = Path(str(source["repo_readout_surface"]))
    artifact_root = Path(str(source["source_artifact_root"]))
    evaluation_root = Path(str(source["source_evaluation_root"]))

    assert readout_surface.name == "standard_gauntlet"
    assert artifact_root == readout_surface / "artifacts" / "smoke_001"
    assert evaluation_root == artifact_root / "evaluations" / SUITE_ID
    assert source["run_mode"] == "not_yet_run"
    assert source["expected_files"]["required"] == []
    assert source["expected_files"]["pending_not_yet_run"]
    assert source["goal_summary_sources"]
    assert source["methodology_summary_sources"]


def test_unknown_claim_status_is_rejected() -> None:
    with pytest.raises(ValueError):
        validate_claim_status("made_up_status")
