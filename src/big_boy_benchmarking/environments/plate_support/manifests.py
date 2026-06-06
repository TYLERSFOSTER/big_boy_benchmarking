"""PlateSupport environment-specific manifest payloads."""

from __future__ import annotations

from pathlib import Path
from typing import Any

from big_boy_benchmarking.artifacts.schemas import ARTIFACT_SCHEMA_VERSION
from big_boy_benchmarking.environments.plate_support.ids import (
    ACTION_LABEL_CONTRACT_ID,
    DEFAULT_INSTANCE_ID,
    DEFAULT_SCHEMA_ID,
    ENVIRONMENT_FAMILY_ID,
    LEGALITY_CONTRACT_ID,
    NO_CONTRACTION_SCHEMA_ID,
    READINESS_RUN_FAMILY_ID,
    REWARD_BUNDLE_ID,
    SMOKE_FIXTURE_ID,
    STRUCTURAL_FIXTURE_ID,
    UPSTREAM_MODULE,
    UPSTREAM_SMOKE_ID,
)


def instance_manifest_payload(*, graph_summary: dict[str, object]) -> dict[str, Any]:
    return {
        "artifact_schema_version": ARTIFACT_SCHEMA_VERSION,
        "environment_family_id": ENVIRONMENT_FAMILY_ID,
        "environment_instance_id": DEFAULT_INSTANCE_ID,
        "upstream_smoke_id": UPSTREAM_SMOKE_ID,
        "upstream_module": UPSTREAM_MODULE,
        "fixture_roles": {
            "smoke_fixture_id": SMOKE_FIXTURE_ID,
            "structural_fixture_id": STRUCTURAL_FIXTURE_ID,
        },
        "contracts": {
            "legality_contract_id": LEGALITY_CONTRACT_ID,
            "reward_bundle_id": REWARD_BUNDLE_ID,
            "action_label_contract_id": ACTION_LABEL_CONTRACT_ID,
        },
        "schemas": {
            "default_schema_id": DEFAULT_SCHEMA_ID,
            "no_contraction_schema_id": NO_CONTRACTION_SCHEMA_ID,
        },
        "graph_summary": graph_summary,
    }


def schema_probe_manifest_payload() -> dict[str, Any]:
    return {
        "artifact_schema_version": ARTIFACT_SCHEMA_VERSION,
        "environment_instance_id": DEFAULT_INSTANCE_ID,
        "readiness_run_family_id": READINESS_RUN_FAMILY_ID,
        "schema_probes": [
            {
                "schema_id": DEFAULT_SCHEMA_ID,
                "upstream_schema_mode": "default",
                "claim_boundary": "tower depth only; not learning performance evidence",
            },
            {
                "schema_id": NO_CONTRACTION_SCHEMA_ID,
                "upstream_schema_mode": "none",
                "claim_boundary": "flat structural control only",
            },
        ],
    }


def readout_source_payload(
    *,
    artifact_root: Path,
    environment_doc: Path,
    run_family_summary: Path,
    artifact_index: Path,
    run_id: str,
) -> dict[str, Any]:
    return {
        "source_type": "environment_readiness",
        "environment_family_id": ENVIRONMENT_FAMILY_ID,
        "environment_instance_id": DEFAULT_INSTANCE_ID,
        "run_family_id": READINESS_RUN_FAMILY_ID,
        "run_id": run_id,
        "artifact_root": str(artifact_root),
        "environment_doc": str(environment_doc),
        "artifact_index": str(artifact_index),
        "run_family_summary": str(run_family_summary),
        "allowed_claims": [
            "environment surface imports",
            "structural graph sanity",
            "artifact completeness",
            "tower-readiness shape",
            "training surface availability",
        ],
        "blocked_claims": [
            "tower learning benefit",
            "flat-versus-tower performance comparison",
            "serious benchmark conclusion",
        ],
    }
