import json

from big_boy_benchmarking.artifacts.manifests import (
    DependencyManifest,
    FamilyManifest,
    RunManifest,
)
from big_boy_benchmarking.artifacts.schemas import ARTIFACT_SCHEMA_VERSION


def test_manifest_serializes_required_fields() -> None:
    manifest = RunManifest(
        run_id="run",
        run_family_id="family",
        environment_id="env",
        mode_id="mode",
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
    assert json.dumps(payload)


def test_dependency_manifest_handles_missing_optional_metadata() -> None:
    payload = DependencyManifest(
        state_collapser={"import_version": "0.6.0", "git_commit": None},
        repo_state={},
    ).to_dict()

    assert payload["state_collapser"]["git_commit"] is None


def test_family_manifest_is_json_safe() -> None:
    assert json.dumps(FamilyManifest("family", "description").to_dict())
