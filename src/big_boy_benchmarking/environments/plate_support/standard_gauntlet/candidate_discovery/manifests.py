"""Manifest payloads for Stage 3 candidate discovery."""

from __future__ import annotations

from big_boy_benchmarking.artifacts.schemas import ARTIFACT_SCHEMA_VERSION
from big_boy_benchmarking.environments.plate_support.standard_gauntlet.candidate_discovery.config import (
    CandidateDiscoveryConfig,
)
from big_boy_benchmarking.environments.plate_support.standard_gauntlet.candidate_discovery.policy import (
    candidate_selection_policy_manifest,
)
from big_boy_benchmarking.environments.plate_support.standard_gauntlet.candidate_discovery.stage2_source import (
    Stage2Source,
)
from big_boy_benchmarking.environments.plate_support.standard_gauntlet.ids import (
    CANDIDATE_DISCOVERY_STAGE_ID,
    ENVIRONMENT_FAMILY_ID,
    ENVIRONMENT_INSTANCE_ID,
    LINEARIZATION_MODE_ID,
    SUITE_ID,
)


def stage_manifest(config: CandidateDiscoveryConfig) -> dict[str, object]:
    return {
        "artifact_schema_version": ARTIFACT_SCHEMA_VERSION,
        "suite_id": SUITE_ID,
        "stage_id": CANDIDATE_DISCOVERY_STAGE_ID,
        "run_label": config.run_label,
        "environment_family_id": ENVIRONMENT_FAMILY_ID,
        "environment_instance_id": ENVIRONMENT_INSTANCE_ID,
        "linearization_mode_id": LINEARIZATION_MODE_ID,
        "claim_boundary": "candidate discovery only; no training evidence",
    }


def stage_budget_lock(config: CandidateDiscoveryConfig) -> dict[str, object]:
    return {
        "artifact_schema_version": ARTIFACT_SCHEMA_VERSION,
        "suite_id": SUITE_ID,
        "stage_id": CANDIDATE_DISCOVERY_STAGE_ID,
        "run_label": config.run_label,
        "locked_by": config.locked_by,
        "clean_candidate_cap": config.clean_candidate_cap,
        "warning_candidate_cap": config.warning_candidate_cap,
        "degeneracy_anchor_cap": config.degeneracy_anchor_cap,
        "allow_warning_selection": config.allow_warning_selection,
        "linearization_mode_id": config.linearization_mode_id,
    }


def stage_input_manifest(source: Stage2Source) -> dict[str, object]:
    return {
        "artifact_schema_version": ARTIFACT_SCHEMA_VERSION,
        "suite_id": SUITE_ID,
        "stage_id": CANDIDATE_DISCOVERY_STAGE_ID,
        "schema_sweep_readout_source": str(source.path),
        "schema_sweep_artifact_root": str(source.source_artifact_root),
        "schema_sweep_source_files": {
            key: str(path) for key, path in sorted(source.source_files.items())
        },
    }


def parent_schema_sweep_manifest(source: Stage2Source) -> dict[str, object]:
    return {
        "artifact_schema_version": ARTIFACT_SCHEMA_VERSION,
        "parent_stage_id": "plate_support_gauntlet_contraction_schema_sweep_v001",
        "parent_readout_source": str(source.path),
        "parent_artifact_root": str(source.source_artifact_root),
    }


def selection_policy_manifest() -> dict[str, object]:
    payload = candidate_selection_policy_manifest()
    return {"artifact_schema_version": ARTIFACT_SCHEMA_VERSION, **payload}


def stage_output_manifest(output_paths: dict[str, str]) -> dict[str, object]:
    return {
        "artifact_schema_version": ARTIFACT_SCHEMA_VERSION,
        "suite_id": SUITE_ID,
        "stage_id": CANDIDATE_DISCOVERY_STAGE_ID,
        "outputs": output_paths,
    }
