"""Geometry and validity summaries for PlateSupport."""

from __future__ import annotations

from collections import Counter
from collections.abc import Iterable
from typing import Any

from big_boy_benchmarking.environments.plate_support.states import support_pattern
from big_boy_benchmarking.environments.plate_support.types import StateRecord
from big_boy_benchmarking.environments.plate_support.upstream import (
    ImportedPlateSupportSurface,
)


def _counter_rows(
    counts: Counter[Any],
    *,
    key_name: str,
    count_name: str = "valid_state_count",
) -> list[dict[str, object]]:
    total = sum(counts.values())
    rows: list[dict[str, object]] = []
    for key in sorted(counts, key=lambda item: str(item)):
        count = int(counts[key])
        rows.append(
            {
                key_name: str(key),
                count_name: count,
                "share": 0.0 if total == 0 else count / total,
            }
        )
    return rows


def support_pattern_summary(records: Iterable[StateRecord]) -> list[dict[str, object]]:
    return _counter_rows(
        Counter(record.support_pattern for record in records),
        key_name="support_pattern",
    )


def reachability_pattern_summary(records: Iterable[StateRecord]) -> list[dict[str, object]]:
    return _counter_rows(
        Counter(record.reachability_pattern for record in records),
        key_name="reachability_pattern",
    )


def orientation_summary(records: Iterable[StateRecord]) -> list[dict[str, object]]:
    return _counter_rows(
        Counter(record.theta_idx for record in records),
        key_name="theta_idx",
    )


def position_summary(records: Iterable[StateRecord]) -> list[dict[str, object]]:
    counts = Counter((record.x_idx, record.y_idx) for record in records)
    total = sum(counts.values())
    rows: list[dict[str, object]] = []
    for (x_idx, y_idx), count in sorted(counts.items()):
        rows.append(
            {
                "x_idx": x_idx,
                "y_idx": y_idx,
                "valid_state_count": count,
                "share": 0.0 if total == 0 else count / total,
            }
        )
    return rows


def validity_predicate_summary(
    *,
    candidate_states: Iterable[Any],
    valid_states: Iterable[Any],
    surface: ImportedPlateSupportSurface,
) -> list[dict[str, object]]:
    predicates = (
        ("sockets_in_bounds", surface.all_sockets_in_bounds),
        ("minimum_engaged_supports", surface.has_minimum_engaged_supports),
        ("stable_support_pattern", surface.has_stable_support_pattern),
        ("candidate_valid_state", surface.is_valid_state),
        (
            "all_engaged_arms_reachable",
            lambda state: all(
                reachable
                for engaged, reachable in zip(
                    support_pattern(state),
                    surface.engaged_arm_reachability(state),
                    strict=True,
                )
                if engaged
            ),
        ),
    )
    candidate_states = tuple(candidate_states)
    valid_states = tuple(valid_states)
    rows: list[dict[str, object]] = []
    for predicate_name, predicate in predicates:
        ambient_true = sum(1 for state in candidate_states if bool(predicate(state)))
        valid_true = sum(1 for state in valid_states if bool(predicate(state)))
        rows.append(
            {
                "predicate_name": predicate_name,
                "valid_state_true_count": valid_true,
                "valid_state_false_count": len(valid_states) - valid_true,
                "ambient_true_count": ambient_true,
                "ambient_false_count": len(candidate_states) - ambient_true,
                "interpretation": _predicate_interpretation(predicate_name),
            }
        )
    return rows


def _predicate_interpretation(predicate_name: str) -> str:
    return {
        "sockets_in_bounds": "all support sockets must remain inside the finite workspace",
        "minimum_engaged_supports": "the support pattern must engage enough arms",
        "stable_support_pattern": "engaged supports must satisfy the upstream stability rule",
        "candidate_valid_state": "complete upstream validity predicate",
        "all_engaged_arms_reachable": "engaged arms must be able to reach their sockets",
    }[predicate_name]
