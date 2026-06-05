"""Candidate-source helpers for the threshold-frontier probe."""

from __future__ import annotations

from pathlib import Path

from big_boy_benchmarking.environments.counterpoint.second_serious_comparison.candidates import (
    CandidateSelection,
    load_schema1_candidates,
)


def load_frontier_candidates(
    candidate_readout_source: Path | str,
    *,
    instance_id: str,
    candidate_cap: int,
    target_candidate_ids: tuple[str, ...] = (),
) -> CandidateSelection:
    return load_schema1_candidates(
        candidate_readout_source,
        instance_id=instance_id,
        candidate_cap=candidate_cap,
        target_candidate_ids=target_candidate_ids,
    )
