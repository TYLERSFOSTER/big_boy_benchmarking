"""Source-binding builders for PlateSupport gauntlet human readouts."""

from __future__ import annotations

import json
from collections.abc import Sequence
from pathlib import Path

from big_boy_benchmarking.artifacts.schemas import ARTIFACT_SCHEMA_VERSION
from big_boy_benchmarking.artifacts.writers import write_json
from big_boy_benchmarking.environments.plate_support.standard_gauntlet.ids import (
    ENVIRONMENT_FAMILY_ID,
    ENVIRONMENT_INSTANCE_ID,
    STAGE_DEFINITIONS,
    SUITE_ID,
)
from big_boy_benchmarking.environments.plate_support.standard_gauntlet.paths import (
    suite_artifact_root,
    suite_evaluation_root,
    suite_readout_surface,
)


def build_suite_readout_source(
    repo_root: Path | str,
    run_label: str,
    *,
    stage_readout_source_paths: Sequence[Path | str] = (),
) -> dict[str, object]:
    """Build a JSON-serializable suite-level readout source binding."""

    readout_surface = suite_readout_surface(repo_root)
    artifact_root = suite_artifact_root(repo_root, run_label)
    evaluation_root = suite_evaluation_root(repo_root, run_label, SUITE_ID)
    stage_paths = [str(Path(path)) for path in stage_readout_source_paths]
    expected_after_run = [
        "evaluation_manifest.json",
        "evaluation_stage_manifest.json",
        "evaluation_budget_lock.json",
        "environment_source_manifest.json",
        "readiness_source_manifest.json",
        "stage_run_index.csv",
        "stage_status_summary.csv",
    ]

    return {
        "artifact_schema_version": ARTIFACT_SCHEMA_VERSION,
        "source_binding_type": "evaluation_readout_source",
        "repo_readout_surface": str(readout_surface),
        "source_artifact_root": str(artifact_root),
        "source_evaluation_root": str(evaluation_root),
        "evaluation_id": SUITE_ID,
        "environment_family_id": ENVIRONMENT_FAMILY_ID,
        "environment_instance_id": ENVIRONMENT_INSTANCE_ID,
        "artifact_run_label": run_label,
        "run_mode": "not_yet_run",
        "stage_readout_source_paths": stage_paths,
        "source_files": {
            "aggregate_table": str(evaluation_root / "stage_status_summary.csv"),
            "run_index": str(evaluation_root / "stage_run_index.csv"),
        },
        "expected_files": {
            "required": [],
            "expected_absent_is_gap": [],
            "conditional": {"after_suite_run": expected_after_run},
            "not_applicable": [],
            "pending_not_yet_run": expected_after_run,
            "expectation_sources": [
                "docs/design/first_plate_support_environment/standard_gauntlet_suite/"
                "00_suite_architecture/"
                "01_001_plate_support_standard_gauntlet_suite_architecture_blueprint.md",
                "docs/prime_directive/evaluation_construction_for_readable_artifacts_protocol.md",
            ],
        },
        "goal_criteria": [
            {
                "goal_id": "plate_support_standard_gauntlet_stage_progression",
                "question": (
                    "Can PlateSupport move from readiness through staged diagnostic, "
                    "candidate, training-health, calibration, and comparison evidence?"
                ),
                "success_signal": "stage_status_summary.csv shows all enabled stages complete",
                "partial_signal": "one or more early diagnostic stages complete before a gate blocks",
                "failure_signal": "required stage source artifacts are missing or protocol-blocked",
                "claim_if_met": "PlateSupport has completed the standard gauntlet run mode",
                "claim_if_not_met": (
                    "PlateSupport has not completed the standard gauntlet; inspect the "
                    "first blocked stage"
                ),
            }
        ],
        "badge_policy": {
            "dimensions": [
                "artifact_status",
                "behavioral_status",
                "goal_status",
                "claim_scope",
                "provenance_status",
            ]
        },
        "goal_summary_sources": [
            "docs/design/first_plate_support_environment/standard_gauntlet_suite/"
            "00_suite_architecture/"
            "01_001_plate_support_standard_gauntlet_suite_architecture_blueprint.md",
            "docs/evaluations/plate_support_5x5_default_v001/standard_gauntlet/method.md",
        ],
        "methodology_summary_sources": [
            "docs/design/first_plate_support_environment/standard_gauntlet_suite/"
            "00_suite_architecture/"
            "01_001_plate_support_standard_gauntlet_suite_architecture_blueprint.md",
            "docs/evaluations/plate_support_5x5_default_v001/standard_gauntlet/method.md",
            "docs/evaluations/plate_support_5x5_default_v001/standard_gauntlet/runbook.md",
        ],
        "structural_limit_checks": [
            {
                "check_id": "stage_gate_block",
                "trigger": "stage_status_summary.csv records protocol_blocked or artifact_incomplete",
                "interpretation_if_triggered": (
                    "The suite produced useful diagnostic evidence but cannot support "
                    "later-stage claims until the blocked gate is resolved."
                ),
                "claim_effect": "blocks claims owned by downstream stages",
            }
        ],
        "claim_boundary": [
            "Architecture scaffold and future gauntlet source binding only until run artifacts exist",
            "No tower-performance claim is supported by the not-yet-run source binding",
        ],
        "stage_definitions": [
            {
                "stage_number": stage.stage_number,
                "stage_id": stage.stage_id,
                "short_name": stage.short_name,
                "required_predecessor_stage_ids": list(stage.required_predecessor_stage_ids),
            }
            for stage in STAGE_DEFINITIONS
        ],
    }


def write_suite_readout_source(
    repo_root: Path | str,
    run_label: str,
    *,
    stage_readout_source_paths: Sequence[Path | str] = (),
) -> Path:
    """Write the suite-level readout source binding to the repo readout surface."""

    target = suite_readout_surface(repo_root) / "readout_source.json"
    payload = build_suite_readout_source(
        repo_root,
        run_label,
        stage_readout_source_paths=stage_readout_source_paths,
    )
    write_json(target, json.loads(json.dumps(payload, sort_keys=True)))
    return target
