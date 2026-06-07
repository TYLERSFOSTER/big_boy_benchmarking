"""Stable candidate ids for PlateSupport gauntlet Stage 3."""

from __future__ import annotations

import hashlib
import json


def candidate_id_for_row(row: dict[str, object]) -> str:
    """Build a deterministic candidate id from stable schema row fields."""

    stable = {
        "schema_id": row["schema_id"],
        "schema_family_id": row["schema_family_id"],
        "schema_seed": row["schema_seed"],
        "schema_mode": row.get("schema_mode", ""),
        "ratio_numerator": row.get("ratio_numerator", ""),
        "ratio_denominator": row.get("ratio_denominator", ""),
        "max_iterations": row.get("max_iterations", ""),
        "selector_rule_id": row.get("selector_rule_id", ""),
        "selection_mode": row.get("selection_mode", ""),
        "structural_class": row.get("structural_class", ""),
    }
    digest = hashlib.sha1(
        json.dumps(stable, sort_keys=True, separators=(",", ":")).encode("utf-8")
    ).hexdigest()[:10]
    return f"plate_support_candidate:{row['schema_family_id']}:{row['schema_seed']}:{digest}"
