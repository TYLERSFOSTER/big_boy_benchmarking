"""Lightweight artifact contract validators."""

from __future__ import annotations

from collections.abc import Iterable
from dataclasses import dataclass
from pathlib import Path
from typing import Any

from big_boy_benchmarking.artifacts.manifests import to_json_dict
from big_boy_benchmarking.artifacts.schemas import ARTIFACT_SCHEMA_VERSION


@dataclass(frozen=True)
class ValidationResult:
    valid: bool
    errors: tuple[str, ...] = ()

    def require_valid(self) -> None:
        if not self.valid:
            raise ValueError("; ".join(self.errors))


def validate_artifact_schema_version(version: str) -> ValidationResult:
    if version == ARTIFACT_SCHEMA_VERSION:
        return ValidationResult(valid=True)
    return ValidationResult(valid=False, errors=(f"unsupported schema version: {version}",))


def validate_required_run_files(
    run_dir: Path | str,
    required_names: Iterable[str],
) -> ValidationResult:
    root = Path(run_dir)
    missing = tuple(name for name in required_names if not (root / name).exists())
    if not missing:
        return ValidationResult(valid=True)
    return ValidationResult(
        valid=False,
        errors=tuple(f"missing required file: {name}" for name in missing),
    )


def validate_json_safe(payload: Any) -> ValidationResult:
    try:
        to_json_dict(payload)
    except TypeError as exc:
        return ValidationResult(valid=False, errors=(str(exc),))
    return ValidationResult(valid=True)
