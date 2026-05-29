import json

from big_boy_benchmarking.artifacts.manifests import (
    DependencyManifest,
    FamilyManifest,
    LinearizationManifest,
    ModeManifest,
    RunManifest,
)
from big_boy_benchmarking.artifacts.schemas import ARTIFACT_SCHEMA_VERSION


def test_manifest_serializes_required_fields() -> None:
    manifest = RunManifest(
        run_id="run",
        run_family_id="family",
        environment_id="env",
        mode_id="mode",
        linearization_mode_id="tensor_available_disabled",
        linearization_benchmark_label="tensor_available_disabled",
        linearization_enabled=False,
        schema_id="schema",
        learner_id="learner",
        controller_id="controller",
        seed_bundle_id="seed",
        budget={"steps": 1},
        diagnostic_profile="smoke",
        timing_profile="default",
        command="cmd",
        status="success",
    )

    payload = manifest.to_dict()

    assert payload["artifact_schema_version"] == ARTIFACT_SCHEMA_VERSION
    assert payload["run_id"] == "run"
    assert payload["linearization_mode_id"] == "tensor_available_disabled"
    assert json.dumps(payload)


def test_dependency_manifest_handles_missing_optional_metadata() -> None:
    payload = DependencyManifest(
        state_collapser={"import_version": "0.6.0", "git_commit": None},
        repo_state={},
    ).to_dict()

    assert payload["state_collapser"]["git_commit"] is None


def test_family_manifest_is_json_safe() -> None:
    assert json.dumps(FamilyManifest("family", "description").to_dict())


def test_mode_manifest_records_execution_and_linearization_contracts() -> None:
    payload = ModeManifest(
        mode_id="mode",
        readout_requested=False,
        morphism_requested=False,
        uses_compatibility_readout=False,
        uses_morphism=False,
        mode_contract={"mode_id": "mode"},
        linearization_mode_contract={"linearization_mode_id": "tensor_available_disabled"},
    ).to_dict()

    assert payload["mode_contract"]["mode_id"] == "mode"
    assert (
        payload["linearization_mode_contract"]["linearization_mode_id"]
        == "tensor_available_disabled"
    )


def test_linearization_manifest_is_json_safe() -> None:
    payload = LinearizationManifest(
        run_id="run",
        linearization_mode_id="tensor_available_disabled",
        linearization_config={"linearization_state": "PRESENT_DISABLED"},
        linearization_report={"benchmark_label": "tensor_available_disabled"},
        report_source="state_collapser.training.build_linearization_report",
        conversion_records_exported=False,
    ).to_dict()

    assert payload["artifact_schema_version"] == ARTIFACT_SCHEMA_VERSION
    assert payload["linearization_report"]["benchmark_label"] == "tensor_available_disabled"
    assert json.dumps(payload)
