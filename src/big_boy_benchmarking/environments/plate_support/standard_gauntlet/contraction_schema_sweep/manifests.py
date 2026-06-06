"""Manifest payloads for Stage 2 schema sweep."""

from __future__ import annotations

from big_boy_benchmarking.artifacts.schemas import ARTIFACT_SCHEMA_VERSION
from big_boy_benchmarking.environments.plate_support.standard_gauntlet.contraction_schema_sweep.config import (
    SchemaSweepConfig,
)
from big_boy_benchmarking.environments.plate_support.standard_gauntlet.contraction_schema_sweep.schema_families import (
    SchemaArm,
)
from big_boy_benchmarking.environments.plate_support.standard_gauntlet.contraction_schema_sweep.stage1_source import (
    Stage1Source,
)
from big_boy_benchmarking.environments.plate_support.standard_gauntlet.ids import (
    CONTRACTION_SCHEMA_SWEEP_STAGE_ID,
    ENVIRONMENT_FAMILY_ID,
    ENVIRONMENT_INSTANCE_ID,
    LINEARIZATION_MODE_ID,
    SUITE_ID,
)


def stage_manifest(config: SchemaSweepConfig) -> dict[str, object]:
    return {
        "artifact_schema_version": ARTIFACT_SCHEMA_VERSION,
        "suite_id": SUITE_ID,
        "stage_id": CONTRACTION_SCHEMA_SWEEP_STAGE_ID,
        "run_label": config.run_label,
        "environment_family_id": ENVIRONMENT_FAMILY_ID,
        "environment_instance_id": ENVIRONMENT_INSTANCE_ID,
        "linearization_mode_id": LINEARIZATION_MODE_ID,
        "claim_boundary": "schema sweep diagnostics and candidate signals only",
    }


def stage_budget_lock(config: SchemaSweepConfig) -> dict[str, object]:
    return {
        "artifact_schema_version": ARTIFACT_SCHEMA_VERSION,
        "suite_id": SUITE_ID,
        "stage_id": CONTRACTION_SCHEMA_SWEEP_STAGE_ID,
        "run_label": config.run_label,
        "locked_by": config.locked_by,
        "schema_families": list(config.schema_families),
        "schema_seeds": list(config.schema_seeds),
        "edge_global_numerators": list(config.edge_global_numerators),
        "near_full_collapse_threshold": config.near_full_collapse_threshold,
        "tower_probe_steps": config.tower_probe_steps,
        "tower_probe_sample_size": config.tower_probe_sample_size,
        "linearization_mode_id": config.linearization_mode_id,
    }


def stage_input_manifest(source: Stage1Source) -> dict[str, object]:
    return {
        "artifact_schema_version": ARTIFACT_SCHEMA_VERSION,
        "suite_id": SUITE_ID,
        "stage_id": CONTRACTION_SCHEMA_SWEEP_STAGE_ID,
        "stage1_readout_source": str(source.path),
        "stage1_artifact_root": str(source.source_artifact_root),
        "stage1_source_files": {
            key: str(path) for key, path in sorted(source.source_files.items())
        },
    }


def schema_family_manifest(arms: tuple[SchemaArm, ...]) -> dict[str, object]:
    families = sorted({arm.schema_family_id for arm in arms})
    return {
        "artifact_schema_version": ARTIFACT_SCHEMA_VERSION,
        "suite_id": SUITE_ID,
        "stage_id": CONTRACTION_SCHEMA_SWEEP_STAGE_ID,
        "schema_family_ids": families,
    }


def stage_output_manifest(output_paths: dict[str, str]) -> dict[str, object]:
    return {
        "artifact_schema_version": ARTIFACT_SCHEMA_VERSION,
        "suite_id": SUITE_ID,
        "stage_id": CONTRACTION_SCHEMA_SWEEP_STAGE_ID,
        "outputs": output_paths,
    }
