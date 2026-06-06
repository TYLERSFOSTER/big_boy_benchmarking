"""Manifest payloads for PlateSupport gauntlet Stage 1."""

from __future__ import annotations

from pathlib import Path

from big_boy_benchmarking.artifacts.schemas import ARTIFACT_SCHEMA_VERSION
from big_boy_benchmarking.environments.plate_support.standard_gauntlet.ids import (
    ENVIRONMENT_FAMILY_ID,
    ENVIRONMENT_INSTANCE_ID,
    LINEARIZATION_MODE_ID,
    STRUCTURAL_TOWER_DIAGNOSTICS_STAGE_ID,
    SUITE_ID,
)
from big_boy_benchmarking.environments.plate_support.standard_gauntlet.structural_and_tower_diagnostics.config import (
    StructuralDiagnosticsConfig,
)
from big_boy_benchmarking.environments.plate_support.standard_gauntlet.structural_and_tower_diagnostics.readiness_source import (
    ReadinessSource,
)


def stage_manifest(config: StructuralDiagnosticsConfig) -> dict[str, object]:
    return {
        "artifact_schema_version": ARTIFACT_SCHEMA_VERSION,
        "suite_id": SUITE_ID,
        "stage_id": STRUCTURAL_TOWER_DIAGNOSTICS_STAGE_ID,
        "run_label": config.run_label,
        "environment_family_id": ENVIRONMENT_FAMILY_ID,
        "environment_instance_id": ENVIRONMENT_INSTANCE_ID,
        "linearization_mode_id": LINEARIZATION_MODE_ID,
        "claim_boundary": "diagnostic-only structural and tower readiness evidence",
    }


def stage_budget_lock(config: StructuralDiagnosticsConfig) -> dict[str, object]:
    return {
        "artifact_schema_version": ARTIFACT_SCHEMA_VERSION,
        "suite_id": SUITE_ID,
        "stage_id": STRUCTURAL_TOWER_DIAGNOSTICS_STAGE_ID,
        "run_label": config.run_label,
        "locked_by": config.locked_by,
        "random_policy_seed": config.random_policy_seed,
        "random_policy_episode_count": config.random_policy_episode_count,
        "tower_probe_steps": config.tower_probe_steps,
        "tower_probe_sample_size": config.tower_probe_sample_size,
        "linearization_mode_id": config.linearization_mode_id,
    }


def stage_input_manifest(
    *,
    config: StructuralDiagnosticsConfig,
    readiness: ReadinessSource,
    dependency_state: dict[str, object],
) -> dict[str, object]:
    return {
        "artifact_schema_version": ARTIFACT_SCHEMA_VERSION,
        "suite_id": SUITE_ID,
        "stage_id": STRUCTURAL_TOWER_DIAGNOSTICS_STAGE_ID,
        "readiness_source": str(readiness.path),
        "readiness_artifact_root": str(readiness.source_artifact_root),
        "readiness_run_family_summary": str(readiness.run_family_summary),
        "environment_doc": str(readiness.environment_doc),
        "state_collapser_dependency_state": dependency_state,
        "artifact_root": str(Path(config.artifact_root).resolve()),
    }


def readiness_source_manifest(readiness: ReadinessSource) -> dict[str, object]:
    return {
        "artifact_schema_version": ARTIFACT_SCHEMA_VERSION,
        "source_type": readiness.source_type,
        "readiness_source": str(readiness.path),
        "readiness_artifact_root": str(readiness.source_artifact_root),
        "environment_doc": str(readiness.environment_doc),
        "run_family_summary": str(readiness.run_family_summary),
    }


def stage_output_manifest(output_paths: dict[str, str]) -> dict[str, object]:
    return {
        "artifact_schema_version": ARTIFACT_SCHEMA_VERSION,
        "suite_id": SUITE_ID,
        "stage_id": STRUCTURAL_TOWER_DIAGNOSTICS_STAGE_ID,
        "outputs": output_paths,
    }
