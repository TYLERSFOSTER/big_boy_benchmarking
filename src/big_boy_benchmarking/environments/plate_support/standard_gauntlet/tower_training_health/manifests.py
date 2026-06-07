"""Manifest payloads for PlateSupport gauntlet Stage 4."""

from __future__ import annotations

from datetime import UTC, datetime
from pathlib import Path

from big_boy_benchmarking.artifacts.schemas import ARTIFACT_SCHEMA_VERSION

from ..ids import SUITE_ID, TOWER_TRAINING_HEALTH_STAGE_ID
from .candidate_source import (
    Stage3CandidateSource,
)
from .config import (
    TowerTrainingHealthConfig,
)


def stage_manifest(config: TowerTrainingHealthConfig) -> dict[str, object]:
    return {
        "artifact_schema_version": ARTIFACT_SCHEMA_VERSION,
        "suite_id": SUITE_ID,
        "stage_id": TOWER_TRAINING_HEALTH_STAGE_ID,
        "stage_number": 4,
        "short_name": "tower_training_health",
        "status": "run_requested",
        "run_label": config.run_label,
        "locked_by": config.locked_by,
        "created_at": _now(),
        "claim_boundary": "tower-only training health evidence, not comparison evidence",
    }


def stage_budget_lock(config: TowerTrainingHealthConfig) -> dict[str, object]:
    return {
        "artifact_schema_version": ARTIFACT_SCHEMA_VERSION,
        "stage_id": TOWER_TRAINING_HEALTH_STAGE_ID,
        "run_label": config.run_label,
        "candidate_cap": config.candidate_cap,
        "training_replicates_per_candidate": config.training_replicates_per_candidate,
        "episodes_per_replicate": config.episodes_per_replicate,
        "max_steps_per_episode": config.max_steps_per_episode,
        "base_seed": config.base_seed,
        "allow_warning_candidates": config.allow_warning_candidates,
        "learning_rate": config.learning_rate,
        "discount": config.discount,
        "epsilon": config.epsilon,
        "linearization_mode_id": config.linearization_mode_id,
    }


def stage_input_manifest(source: Stage3CandidateSource) -> dict[str, object]:
    return {
        "artifact_schema_version": ARTIFACT_SCHEMA_VERSION,
        "stage_id": TOWER_TRAINING_HEALTH_STAGE_ID,
        "candidate_source": str(source.path),
        "candidate_manifest": str(source.candidate_manifest_path),
        "source_artifact_root": str(source.source_artifact_root),
        "selected_candidate_count": len(source.selected_candidates),
        "source_files": {key: str(path) for key, path in source.source_files.items()},
    }


def candidate_manifest(source: Stage3CandidateSource) -> dict[str, object]:
    return {
        "artifact_schema_version": ARTIFACT_SCHEMA_VERSION,
        "stage_id": TOWER_TRAINING_HEALTH_STAGE_ID,
        "candidates": [
            {
                "candidate_id": candidate.candidate_id,
                "schema_id": candidate.schema_id,
                "schema_family_id": candidate.schema_family_id,
                "schema_seed": candidate.schema_seed,
                "selection_status": candidate.selection_status,
                "allowed_downstream_stage": candidate.allowed_downstream_stage,
                "source_artifact_root": str(candidate.source_artifact_root),
                "schema_mode": candidate.schema_mode,
                "selection_rate": candidate.selection_rate,
                "ratio_numerator": candidate.ratio_numerator,
                "ratio_denominator": candidate.ratio_denominator,
                "max_iterations": candidate.max_iterations,
                "selector_rule_id": candidate.selector_rule_id,
                "selection_mode": candidate.selection_mode,
                "max_depth": candidate.max_depth,
                "nontrivial_tier_count": candidate.nontrivial_tier_count,
            }
            for candidate in source.selected_candidates
        ],
    }


def parent_candidate_manifest(source: Stage3CandidateSource) -> dict[str, object]:
    return {
        "artifact_schema_version": ARTIFACT_SCHEMA_VERSION,
        "stage_id": TOWER_TRAINING_HEALTH_STAGE_ID,
        "parent_stage_id": "plate_support_gauntlet_candidate_discovery_v001",
        "parent_readout_source": str(source.path),
        "parent_candidate_manifest": str(source.candidate_manifest_path),
    }


def training_config_manifest(config: TowerTrainingHealthConfig) -> dict[str, object]:
    return {
        "artifact_schema_version": ARTIFACT_SCHEMA_VERSION,
        "training_strategy": "tower_action_cell_tabular_q_health_probe",
        "episodes_per_replicate": config.episodes_per_replicate,
        "max_steps_per_episode": config.max_steps_per_episode,
        "learning_rate": config.learning_rate,
        "discount": config.discount,
        "epsilon": config.epsilon,
    }


def training_surface_manifest(
    *,
    strategy_id: str,
    event_observability: dict[str, str],
) -> dict[str, object]:
    return {
        "artifact_schema_version": ARTIFACT_SCHEMA_VERSION,
        "stage_id": TOWER_TRAINING_HEALTH_STAGE_ID,
        "runner_strategy": strategy_id,
        "event_observability": event_observability,
    }


def stage_output_manifest(output_paths: dict[str, str]) -> dict[str, object]:
    return {
        "artifact_schema_version": ARTIFACT_SCHEMA_VERSION,
        "stage_id": TOWER_TRAINING_HEALTH_STAGE_ID,
        "output_paths": output_paths,
    }


def seed_bundle_payload(
    *,
    run_id: str,
    candidate_id: str,
    replicate_index: int,
    base_seed: int,
) -> dict[str, object]:
    return {
        "artifact_schema_version": ARTIFACT_SCHEMA_VERSION,
        "run_id": run_id,
        "candidate_id": candidate_id,
        "replicate_index": replicate_index,
        "base_seed": base_seed,
        "replicate_seed": base_seed + replicate_index,
    }


def require_repo_path(path: Path, repo_root: Path, label: str) -> None:
    try:
        path.resolve().relative_to(repo_root.resolve())
    except ValueError as exc:
        raise ValueError(f"{label} is outside repository: {path}") from exc


def _now() -> str:
    return datetime.now(UTC).isoformat()
