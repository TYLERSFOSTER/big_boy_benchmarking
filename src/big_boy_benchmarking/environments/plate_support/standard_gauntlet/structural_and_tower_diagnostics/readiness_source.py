"""Readiness source loading and validation for PlateSupport gauntlet Stage 1."""

from __future__ import annotations

import json
from dataclasses import dataclass
from pathlib import Path

from big_boy_benchmarking.environments.plate_support.standard_gauntlet.ids import (
    ENVIRONMENT_FAMILY_ID,
    ENVIRONMENT_INSTANCE_ID,
)


@dataclass(frozen=True)
class ReadinessSource:
    """Validated environment-readiness source binding."""

    path: Path
    repo_root: Path
    repo_readout_surface: Path
    source_artifact_root: Path
    environment_doc: Path
    run_family_summary: Path
    environment_family_id: str
    environment_instance_id: str
    source_type: str
    payload: dict[str, object]


class ReadinessSourceError(ValueError):
    """Raised when a readiness source cannot safely feed Stage 1."""


def load_readiness_source(path: Path | str, *, repo_root: Path | str) -> ReadinessSource:
    """Load and validate an environment-readiness `readout_source.json`."""

    root = Path(repo_root).expanduser().resolve()
    source_path = Path(path).expanduser().resolve()
    _require_under_repo(source_path, root, "readiness source")
    if not source_path.exists():
        raise ReadinessSourceError(f"readiness source does not exist: {source_path}")

    with source_path.open(encoding="utf-8") as handle:
        payload = json.load(handle)

    source_type = str(payload.get("source_type", ""))
    family_id = str(payload.get("environment_family_id", ""))
    instance_id = str(payload.get("environment_instance_id", ""))
    artifact_root = _resolve_repo_path(payload.get("artifact_root", ""), root)
    environment_doc = _resolve_repo_path(payload.get("environment_doc", ""), root)
    run_family_summary = _resolve_repo_path(payload.get("run_family_summary", ""), root)

    if source_type != "environment_readiness":
        raise ReadinessSourceError(f"expected environment_readiness source, got {source_type!r}")
    if family_id != ENVIRONMENT_FAMILY_ID:
        raise ReadinessSourceError(f"expected family {ENVIRONMENT_FAMILY_ID}, got {family_id!r}")
    if instance_id != ENVIRONMENT_INSTANCE_ID:
        raise ReadinessSourceError(
            f"expected instance {ENVIRONMENT_INSTANCE_ID}, got {instance_id!r}"
        )
    _require_under_repo(artifact_root, root, "readiness artifact root")
    _require_under_repo(environment_doc, root, "environment doc")
    _require_under_repo(run_family_summary, root, "readiness summary")
    if "docs/environments" not in artifact_root.as_posix():
        raise ReadinessSourceError(
            f"readiness artifacts must live under docs/environments: {artifact_root}"
        )
    if "docs/evaluations" in artifact_root.as_posix():
        raise ReadinessSourceError(
            f"readiness artifacts must not live under docs/evaluations: {artifact_root}"
        )
    if not artifact_root.exists():
        raise ReadinessSourceError(f"readiness artifact root does not exist: {artifact_root}")
    if not environment_doc.exists():
        raise ReadinessSourceError(f"environment doc does not exist: {environment_doc}")
    if not run_family_summary.exists():
        raise ReadinessSourceError(f"readiness summary does not exist: {run_family_summary}")

    return ReadinessSource(
        path=source_path,
        repo_root=root,
        repo_readout_surface=source_path.parent,
        source_artifact_root=artifact_root,
        environment_doc=environment_doc,
        run_family_summary=run_family_summary,
        environment_family_id=family_id,
        environment_instance_id=instance_id,
        source_type=source_type,
        payload=payload,
    )


def _require_under_repo(path: Path, repo_root: Path, label: str) -> None:
    try:
        path.relative_to(repo_root)
    except ValueError as exc:
        raise ReadinessSourceError(f"{label} is outside repository: {path}") from exc


def _resolve_repo_path(value: object, repo_root: Path) -> Path:
    text = str(value)
    if text == "<repo-root>":
        return repo_root
    if text.startswith("<repo-root>/"):
        return (repo_root / text.removeprefix("<repo-root>/")).resolve()
    path = Path(text).expanduser()
    if not path.is_absolute():
        path = repo_root / path
    return path.resolve()
