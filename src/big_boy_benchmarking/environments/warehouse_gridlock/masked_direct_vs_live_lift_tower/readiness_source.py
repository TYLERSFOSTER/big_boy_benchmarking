"""Readiness-source loading for the Warehouse masked direct/live-lift diagnostic."""

from __future__ import annotations

import json
from dataclasses import dataclass
from pathlib import Path
from typing import Any


@dataclass(frozen=True)
class ReadinessSource:
    path: Path
    payload: dict[str, Any]

    @property
    def environment_instance_id(self) -> str:
        return str(self.payload.get("environment_instance_id", ""))

    @property
    def source_artifact_root(self) -> str:
        return str(self.payload.get("source_artifact_root", ""))

    @property
    def status(self) -> str:
        return str(self.payload.get("status", self.payload.get("readiness_status", "unknown")))

    @property
    def artifact_tables(self) -> dict[str, Any]:
        tables = self.payload.get("artifact_tables", {})
        return dict(tables) if isinstance(tables, dict) else {}


def load_readiness_source(path: Path | str) -> ReadinessSource:
    source_path = Path(path)
    if not source_path.exists():
        raise FileNotFoundError(f"Warehouse readiness source not found: {source_path}")
    payload = json.loads(source_path.read_text(encoding="utf-8"))
    if not isinstance(payload, dict):
        raise ValueError(f"Warehouse readiness source must be a JSON object: {source_path}")
    return ReadinessSource(path=source_path, payload=payload)


def validate_readiness_source(
    source: ReadinessSource,
    *,
    expected_instance_id: str,
) -> None:
    if source.environment_instance_id != expected_instance_id:
        raise ValueError(
            "Warehouse readiness source instance mismatch: "
            f"expected={expected_instance_id!r} observed={source.environment_instance_id!r}"
        )
    if not source.artifact_tables:
        raise ValueError("Warehouse readiness source is missing artifact_tables")
