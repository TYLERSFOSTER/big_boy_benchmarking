"""Threshold-source resolution for the small paired replicate probe."""

from __future__ import annotations

import csv
import json
from dataclasses import dataclass
from pathlib import Path
from typing import Any

from big_boy_benchmarking.environments.counterpoint.small_paired_replicate_probe.paths import (
    validate_repo_resident_path,
)


@dataclass(frozen=True)
class ResolvedThreshold:
    threshold_value: float
    threshold_source_type: str
    threshold_source_readout: str | None
    threshold_source_field: str

    def to_dict(self) -> dict[str, Any]:
        return {
            "threshold_value": self.threshold_value,
            "threshold_source_type": self.threshold_source_type,
            "threshold_source_readout": self.threshold_source_readout,
            "threshold_source_field": self.threshold_source_field,
        }


def resolve_threshold(
    *,
    threshold_value: float | None,
    threshold_frontier_readout_source: Path | str | None,
) -> ResolvedThreshold:
    if threshold_value is not None:
        return ResolvedThreshold(
            threshold_value=float(threshold_value),
            threshold_source_type="explicit_cli_threshold",
            threshold_source_readout=None,
            threshold_source_field="--threshold-value",
        )
    if threshold_frontier_readout_source is None:
        raise ValueError(
            "small paired replicate probe requires --threshold-value for smoke "
            "or --threshold-frontier-readout-source for a meaningful run"
        )
    source_path = validate_repo_resident_path(threshold_frontier_readout_source)
    if source_path.name != "readout_source.json":
        raise ValueError("threshold frontier source must be a repo-side readout_source.json")
    if not source_path.exists():
        raise FileNotFoundError(f"missing threshold frontier readout source: {source_path}")
    source = json.loads(source_path.read_text(encoding="utf-8"))
    candidates = _candidate_values_from_source(source_path=source_path, source=source)
    distinct = {value for value, _field in candidates}
    if not distinct:
        raise ValueError(
            "threshold frontier readout did not expose a recommended replicate probe threshold"
        )
    if len(distinct) > 1:
        raise ValueError(
            "threshold frontier readout exposed ambiguous recommended thresholds: "
            + ", ".join(str(value) for value in sorted(distinct))
        )
    value, field = candidates[0]
    return ResolvedThreshold(
        threshold_value=value,
        threshold_source_type="threshold_frontier_readout",
        threshold_source_readout=str(source_path),
        threshold_source_field=field,
    )


def _candidate_values_from_source(
    *,
    source_path: Path,
    source: dict[str, Any],
) -> list[tuple[float, str]]:
    fields = (
        "recommended_replicate_probe_threshold",
        "recommended_threshold_value",
        "selected_threshold_value",
    )
    found: list[tuple[float, str]] = []
    for field in fields:
        if source.get(field) not in (None, ""):
            found.append((float(source[field]), field))
    policy = source.get("threshold_frontier_policy")
    if isinstance(policy, dict):
        for field in fields:
            if policy.get(field) not in (None, ""):
                found.append((float(policy[field]), f"threshold_frontier_policy.{field}"))
    source_files = dict(source.get("source_files", {}))
    for key in ("frontier_summary", "aggregate_table"):
        if key not in source_files:
            continue
        path = validate_repo_resident_path(source_files[key])
        if not path.exists():
            continue
        found.extend(_candidate_values_from_csv(path, source_key=key))
    if not found:
        return []
    first_by_value: dict[float, str] = {}
    for value, field in found:
        first_by_value.setdefault(value, field)
    return [(value, field) for value, field in first_by_value.items()]


def _candidate_values_from_csv(path: Path, *, source_key: str) -> list[tuple[float, str]]:
    result: list[tuple[float, str]] = []
    for row in csv.DictReader(path.open(encoding="utf-8")):
        for field in (
            "recommended_replicate_probe_threshold",
            "recommended_threshold_value",
            "selected_threshold_value",
        ):
            if row.get(field) not in (None, ""):
                result.append((float(row[field]), f"source_files.{source_key}.{field}"))
    return result
