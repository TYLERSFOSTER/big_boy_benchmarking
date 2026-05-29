"""Artifact schema constants."""

ARTIFACT_SCHEMA_VERSION = "bbb.v001"

FIRST_EVENT_TABLES = (
    "run_index.jsonl",
    "episodes.csv",
    "step_events.csv",
    "control_events.csv",
    "timing_segments.csv",
    "structural_diagnostics.jsonl",
    "warnings.jsonl",
)

REQUIRED_MANIFEST_CATEGORIES = (
    "family_manifest",
    "matrix_manifest",
    "environment_family_manifest",
    "dependency_manifest",
    "run_manifest",
    "mode_manifest",
    "linearization_manifest",
    "seed_bundle",
    "external_artifacts",
)
