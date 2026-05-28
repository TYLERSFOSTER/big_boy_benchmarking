from pathlib import Path

from big_boy_benchmarking.artifacts.schemas import ARTIFACT_SCHEMA_VERSION
from big_boy_benchmarking.artifacts.validators import (
    validate_artifact_schema_version,
    validate_json_safe,
    validate_required_run_files,
)


def test_schema_version_validator_accepts_current_version() -> None:
    validate_artifact_schema_version(ARTIFACT_SCHEMA_VERSION).require_valid()


def test_required_run_files_reports_missing(tmp_path: Path) -> None:
    result = validate_required_run_files(tmp_path, ("run_manifest.json",))

    assert not result.valid
    assert "run_manifest.json" in result.errors[0]


def test_json_safe_validator_rejects_unknown_object() -> None:
    result = validate_json_safe(object())

    assert not result.valid
