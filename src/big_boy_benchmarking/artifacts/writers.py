"""Boring artifact writers for JSON, JSONL, and CSV."""

from __future__ import annotations

import csv
import json
from collections.abc import Iterable, Mapping, Sequence
from pathlib import Path
from typing import Any

from big_boy_benchmarking.artifacts.manifests import to_json_dict
from big_boy_benchmarking.artifacts.paths import RunFamilyPaths, RunPaths


def _prepare_parent(path: Path, *, create_parents: bool) -> None:
    if create_parents:
        path.parent.mkdir(parents=True, exist_ok=True)


def write_json(
    path: Path | str,
    payload: Mapping[str, Any],
    *,
    create_parents: bool = False,
) -> None:
    target = Path(path)
    _prepare_parent(target, create_parents=create_parents)
    target.write_text(
        json.dumps(to_json_dict(payload), indent=2, sort_keys=True) + "\n",
        encoding="utf-8",
    )


def append_jsonl(
    path: Path | str,
    payload: Mapping[str, Any],
    *,
    create_parents: bool = False,
) -> None:
    target = Path(path)
    _prepare_parent(target, create_parents=create_parents)
    with target.open("a", encoding="utf-8") as handle:
        handle.write(json.dumps(to_json_dict(payload), sort_keys=True) + "\n")


def write_csv(
    path: Path | str,
    rows: Iterable[Mapping[str, Any]],
    fieldnames: Sequence[str],
    *,
    create_parents: bool = False,
) -> None:
    target = Path(path)
    _prepare_parent(target, create_parents=create_parents)
    with target.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=list(fieldnames), lineterminator="\n")
        writer.writeheader()
        for row in rows:
            writer.writerow({key: row.get(key) for key in fieldnames})


def append_csv_row(
    path: Path | str,
    row: Mapping[str, Any],
    fieldnames: Sequence[str],
    *,
    create_parents: bool = False,
) -> None:
    target = Path(path)
    _prepare_parent(target, create_parents=create_parents)
    should_write_header = not target.exists() or target.stat().st_size == 0
    with target.open("a", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=list(fieldnames), lineterminator="\n")
        if should_write_header:
            writer.writeheader()
        writer.writerow({key: row.get(key) for key in fieldnames})


def ensure_artifact_dirs(
    family_paths: RunFamilyPaths,
    run_paths: RunPaths | None = None,
) -> None:
    family_paths.root.mkdir(parents=True, exist_ok=True)
    family_paths.summaries_dir.mkdir(parents=True, exist_ok=True)
    family_paths.runs_dir.mkdir(parents=True, exist_ok=True)
    if run_paths is not None:
        run_paths.root.mkdir(parents=True, exist_ok=True)
