"""Manifest builders for the PlateSupport standard gauntlet suite."""

from __future__ import annotations

from collections.abc import Mapping, Sequence
from dataclasses import dataclass
from pathlib import Path

from big_boy_benchmarking.artifacts.schemas import ARTIFACT_SCHEMA_VERSION
from big_boy_benchmarking.environments.plate_support.standard_gauntlet.ids import (
    ENVIRONMENT_FAMILY_ID,
    ENVIRONMENT_INSTANCE_ID,
    LINEARIZATION_MODE_ID,
    STAGE_DEFINITIONS,
    SUITE_ID,
    SUITE_RUN_FAMILY_ID,
)
from big_boy_benchmarking.environments.plate_support.standard_gauntlet.paths import (
    default_readiness_source_path,
    suite_artifact_root,
    suite_readout_surface,
)


@dataclass(frozen=True)
class SuiteManifestInputs:
    """Explicit context required to build suite-level manifests."""

    repo_root: Path
    run_label: str
    stage_ids_included: tuple[str, ...]
    locked_by: str
    state_collapser_dependency_state: Mapping[str, object]
    seed_bundle_policy: Mapping[str, object]
    replicate_policy: Mapping[str, object]
    episode_step_budget: Mapping[str, object]
    threshold_or_success_rule: Mapping[str, object]
    candidate_source: Mapping[str, object]
    readiness_run_label: str = "dev_001"


def build_suite_manifests(inputs: SuiteManifestInputs) -> dict[str, dict[str, object]]:
    """Build suite-level manifest payloads without writing files."""

    readout_surface = suite_readout_surface(inputs.repo_root)
    artifact_root = suite_artifact_root(inputs.repo_root, inputs.run_label)
    readiness_source = default_readiness_source_path(
        inputs.repo_root,
        readiness_run_label=inputs.readiness_run_label,
    )
    stage_manifest_rows = [
        {
            "stage_number": stage.stage_number,
            "stage_id": stage.stage_id,
            "short_name": stage.short_name,
            "required_predecessor_stage_ids": list(stage.required_predecessor_stage_ids),
            "included": stage.stage_id in inputs.stage_ids_included,
        }
        for stage in STAGE_DEFINITIONS
    ]

    return {
        "evaluation_manifest": {
            "artifact_schema_version": ARTIFACT_SCHEMA_VERSION,
            "suite_id": SUITE_ID,
            "suite_run_family_id": SUITE_RUN_FAMILY_ID,
            "environment_family_id": ENVIRONMENT_FAMILY_ID,
            "environment_instance_id": ENVIRONMENT_INSTANCE_ID,
            "run_label": inputs.run_label,
            "repo_readout_surface": str(readout_surface),
            "artifact_root": str(artifact_root),
            "stage_ids_included": list(inputs.stage_ids_included),
            "linearization_mode_id": LINEARIZATION_MODE_ID,
        },
        "evaluation_stage_manifest": {
            "artifact_schema_version": ARTIFACT_SCHEMA_VERSION,
            "suite_id": SUITE_ID,
            "stages": stage_manifest_rows,
        },
        "evaluation_budget_lock": build_budget_lock(inputs),
        "environment_source_manifest": {
            "artifact_schema_version": ARTIFACT_SCHEMA_VERSION,
            "environment_family_id": ENVIRONMENT_FAMILY_ID,
            "environment_instance_id": ENVIRONMENT_INSTANCE_ID,
            "environment_doc": str(
                inputs.repo_root
                / "docs"
                / "environments"
                / f"{ENVIRONMENT_INSTANCE_ID}.md"
            ),
        },
        "readiness_source_manifest": {
            "artifact_schema_version": ARTIFACT_SCHEMA_VERSION,
            "source_type": "environment_readiness",
            "readiness_run_label": inputs.readiness_run_label,
            "readiness_source": str(readiness_source),
        },
    }


def build_budget_lock(inputs: SuiteManifestInputs) -> dict[str, object]:
    """Build the shared gauntlet budget-lock shape."""

    return {
        "artifact_schema_version": ARTIFACT_SCHEMA_VERSION,
        "suite_id": SUITE_ID,
        "run_label": inputs.run_label,
        "stage_ids_included": list(inputs.stage_ids_included),
        "environment_instance_id": ENVIRONMENT_INSTANCE_ID,
        "state_collapser_dependency_state": dict(inputs.state_collapser_dependency_state),
        "seed_bundle_policy": dict(inputs.seed_bundle_policy),
        "replicate_policy": dict(inputs.replicate_policy),
        "episode_step_budget": dict(inputs.episode_step_budget),
        "threshold_or_success_rule": dict(inputs.threshold_or_success_rule),
        "candidate_source": dict(inputs.candidate_source),
        "linearization_mode_id": LINEARIZATION_MODE_ID,
        "locked_by": inputs.locked_by,
    }


def required_budget_lock_keys() -> tuple[str, ...]:
    """Return required budget-lock fields for tests and validators."""

    return (
        "run_label",
        "stage_ids_included",
        "environment_instance_id",
        "state_collapser_dependency_state",
        "seed_bundle_policy",
        "replicate_policy",
        "episode_step_budget",
        "threshold_or_success_rule",
        "candidate_source",
        "linearization_mode_id",
        "locked_by",
    )


def stage_readout_source_entries(stage_paths: Sequence[Path | str]) -> list[str]:
    """Normalize child-stage readout source paths for manifest/readout builders."""

    return [str(Path(path)) for path in stage_paths]
