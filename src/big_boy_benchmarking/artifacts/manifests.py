"""Manifest dataclasses for benchmark artifacts."""

from __future__ import annotations

from collections.abc import Mapping
from dataclasses import asdict, dataclass, is_dataclass
from pathlib import Path
from typing import Any

from big_boy_benchmarking.artifacts.schemas import ARTIFACT_SCHEMA_VERSION


def to_json_dict(value: Any) -> Any:
    """Convert supported manifest values into JSON-safe objects."""

    if is_dataclass(value) and not isinstance(value, type):
        return to_json_dict(asdict(value))
    if isinstance(value, Mapping):
        return {str(key): to_json_dict(item) for key, item in value.items()}
    if isinstance(value, tuple | list):
        return [to_json_dict(item) for item in value]
    if isinstance(value, Path):
        return str(value)
    if value is None or isinstance(value, str | int | float | bool):
        return value
    raise TypeError(f"Object of type {type(value).__name__} is not JSON safe")


@dataclass(frozen=True)
class FamilyManifest:
    run_family_id: str
    description: str
    artifact_schema_version: str = ARTIFACT_SCHEMA_VERSION

    def to_dict(self) -> dict[str, Any]:
        return to_json_dict(self)


@dataclass(frozen=True)
class MatrixManifest:
    matrix_id: str
    run_family_id: str
    environment_ids: tuple[str, ...]
    mode_ids: tuple[str, ...]
    seed_bundle_ids: tuple[str, ...]
    artifact_schema_version: str = ARTIFACT_SCHEMA_VERSION

    def to_dict(self) -> dict[str, Any]:
        return to_json_dict(self)


@dataclass(frozen=True)
class EnvironmentFamilyManifest:
    environment_family_id: str
    environment_ids: tuple[str, ...]
    description: str
    artifact_schema_version: str = ARTIFACT_SCHEMA_VERSION

    def to_dict(self) -> dict[str, Any]:
        return to_json_dict(self)


@dataclass(frozen=True)
class DependencyManifest:
    state_collapser: Mapping[str, Any]
    repo_state: Mapping[str, Any]
    artifact_schema_version: str = ARTIFACT_SCHEMA_VERSION

    def to_dict(self) -> dict[str, Any]:
        return to_json_dict(self)


@dataclass(frozen=True)
class RunManifest:
    run_id: str
    run_family_id: str
    environment_id: str
    mode_id: str
    schema_id: str
    learner_id: str
    controller_id: str
    seed_bundle_id: str
    budget: Mapping[str, Any]
    diagnostic_profile: str
    timing_profile: str
    command: str
    status: str
    artifact_schema_version: str = ARTIFACT_SCHEMA_VERSION

    def to_dict(self) -> dict[str, Any]:
        return to_json_dict(self)


@dataclass(frozen=True)
class ModeManifest:
    mode_id: str
    readout_requested: bool
    morphism_requested: bool
    uses_compatibility_readout: bool
    uses_morphism: bool
    mode_contract: Mapping[str, Any]
    artifact_schema_version: str = ARTIFACT_SCHEMA_VERSION

    def to_dict(self) -> dict[str, Any]:
        return to_json_dict(self)


@dataclass(frozen=True)
class ExternalArtifactsManifest:
    run_id: str
    artifacts: tuple[Mapping[str, Any], ...] = ()
    artifact_schema_version: str = ARTIFACT_SCHEMA_VERSION

    def to_dict(self) -> dict[str, Any]:
        return to_json_dict(self)
