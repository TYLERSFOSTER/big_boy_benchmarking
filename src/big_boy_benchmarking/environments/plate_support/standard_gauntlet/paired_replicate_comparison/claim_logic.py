"""Bounded claim classification for PlateSupport gauntlet Stage 6."""

from __future__ import annotations

from ..status import (
    CLAIM_STATUS_PAIRED_COMPARISON_INCONCLUSIVE,
    CLAIM_STATUS_PAIRED_COMPARISON_NEGATIVE_SIGNAL,
    CLAIM_STATUS_PAIRED_COMPARISON_POSITIVE_SIGNAL,
)
from .target_policy import CLAIM_BOUNDARY


def classify_paired_claim(
    *,
    paired_rows: list[dict[str, object]],
    direct_arm_id: str,
    candidate_arm_id: str,
) -> dict[str, object]:
    """Classify the paired comparison using only complete pairs."""

    deltas = [
        float(row["target_hit_rate_delta"])
        for row in paired_rows
        if row.get("baseline_arm_id") == direct_arm_id
        and row.get("candidate_arm_id") == candidate_arm_id
        and row.get("pair_complete") == "1"
    ]
    complete_pair_count = len(deltas)
    if complete_pair_count == 0:
        return {
            "claim_status": CLAIM_STATUS_PAIRED_COMPARISON_INCONCLUSIVE,
            "direction": "blocked_no_complete_pairs",
            "mean_target_hit_rate_delta": 0.0,
            "complete_pair_count": 0,
            "bounded_claim": (
                "Stage 6 produced no complete direct-vs-tower pairs, so it supports no "
                "directional comparison claim."
            ),
            "claim_boundary": CLAIM_BOUNDARY,
        }
    mean_delta = sum(deltas) / complete_pair_count
    if mean_delta > 0.0:
        status = CLAIM_STATUS_PAIRED_COMPARISON_POSITIVE_SIGNAL
        direction = "candidate_above_direct"
        claim = (
            "Under this smoke Stage 6 budget, the selected tower candidate shows a "
            "limited positive target-hit signal relative to the direct baseline."
        )
    elif mean_delta < 0.0:
        status = CLAIM_STATUS_PAIRED_COMPARISON_NEGATIVE_SIGNAL
        direction = "candidate_below_direct"
        claim = (
            "Under this smoke Stage 6 budget, the selected tower candidate is below "
            "the direct baseline on target-hit rate."
        )
    else:
        status = CLAIM_STATUS_PAIRED_COMPARISON_INCONCLUSIVE
        direction = "no_directional_delta"
        claim = (
            "Under this smoke Stage 6 budget, the selected tower candidate and direct "
            "baseline have no observed target-hit-rate separation."
        )
    return {
        "claim_status": status,
        "direction": direction,
        "mean_target_hit_rate_delta": mean_delta,
        "complete_pair_count": complete_pair_count,
        "bounded_claim": claim,
        "claim_boundary": CLAIM_BOUNDARY,
    }
