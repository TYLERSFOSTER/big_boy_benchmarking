"""Manifest payloads for PlateSupport gauntlet Stage 6."""

from __future__ import annotations

from datetime import UTC, datetime

from big_boy_benchmarking.artifacts.schemas import ARTIFACT_SCHEMA_VERSION

from ..ids import PAIRED_REPLICATE_COMPARISON_STAGE_ID, SUITE_ID
from .config import PairedReplicateComparisonConfig


def stage_manifest(config: PairedReplicateComparisonConfig) -> dict[str, object]:
    return {
        "artifact_schema_version": ARTIFACT_SCHEMA_VERSION,
        "suite_id": SUITE_ID,
        "stage_id": PAIRED_REPLICATE_COMPARISON_STAGE_ID,
        "stage_number": 6,
        "short_name": "paired_replicate_comparison",
        "status": "run_requested",
        "run_label": config.run_label,
        "locked_by": config.locked_by,
        "created_at": _now(),
        "claim_boundary": "bounded paired comparison evidence only",
    }


def stage_budget_lock(
    config: PairedReplicateComparisonConfig,
    *,
    episodes_per_replicate: int,
    replicates_per_arm: int,
) -> dict[str, object]:
    return {
        "artifact_schema_version": ARTIFACT_SCHEMA_VERSION,
        "stage_id": PAIRED_REPLICATE_COMPARISON_STAGE_ID,
        "run_label": config.run_label,
        "candidate_cap": config.candidate_cap,
        "episodes_per_replicate": episodes_per_replicate,
        "replicates_per_arm": replicates_per_arm,
        "max_steps_per_episode": config.max_steps_per_episode,
        "base_seed": config.base_seed,
        "allow_warning_candidates": config.allow_warning_candidates,
        "allow_legacy_dependency": config.allow_legacy_dependency,
        "learning_rate": config.learning_rate,
        "discount": config.discount,
        "epsilon": config.epsilon,
        "linearization_mode_id": config.linearization_mode_id,
    }


def stage_input_manifest(
    *,
    candidate_source_path: str,
    training_health_source_path: str,
    threshold_source_path: str,
    selected_candidate_id: str,
) -> dict[str, object]:
    return {
        "artifact_schema_version": ARTIFACT_SCHEMA_VERSION,
        "stage_id": PAIRED_REPLICATE_COMPARISON_STAGE_ID,
        "candidate_source": candidate_source_path,
        "training_health_source": training_health_source_path,
        "threshold_source": threshold_source_path,
        "selected_candidate_id": selected_candidate_id,
    }


def comparison_arm_manifest(arm_rows: list[dict[str, object]]) -> dict[str, object]:
    return {
        "artifact_schema_version": ARTIFACT_SCHEMA_VERSION,
        "stage_id": PAIRED_REPLICATE_COMPARISON_STAGE_ID,
        "arms": arm_rows,
    }


def target_policy_manifest(target: dict[str, object]) -> dict[str, object]:
    return {
        "artifact_schema_version": ARTIFACT_SCHEMA_VERSION,
        "stage_id": PAIRED_REPLICATE_COMPARISON_STAGE_ID,
        "target": target,
    }


def stage_output_manifest(output_paths: dict[str, str]) -> dict[str, object]:
    return {
        "artifact_schema_version": ARTIFACT_SCHEMA_VERSION,
        "stage_id": PAIRED_REPLICATE_COMPARISON_STAGE_ID,
        "output_paths": output_paths,
    }


def _now() -> str:
    return datetime.now(UTC).isoformat()
