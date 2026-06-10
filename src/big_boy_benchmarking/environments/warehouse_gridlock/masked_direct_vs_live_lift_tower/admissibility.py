"""Immediate-admissibility masks for Warehouse Gridlock candidates."""

from __future__ import annotations

from dataclasses import dataclass

from big_boy_benchmarking.environments.warehouse_gridlock.instances import (
    WarehouseGridlockInstance,
)
from big_boy_benchmarking.environments.warehouse_gridlock.state import (
    WarehouseGridlockState,
)
from big_boy_benchmarking.environments.warehouse_gridlock.transition import (
    WarehouseGridlockStepResult,
    step,
)
from big_boy_benchmarking.environments.warehouse_gridlock.masked_direct_vs_live_lift_tower.candidate_generation import (
    DirectActionCandidate,
    TowerActionCandidate,
)
from big_boy_benchmarking.environments.warehouse_gridlock.masked_direct_vs_live_lift_tower.config import (
    DIRECT_MASK_POLICY_ID,
    TOWER_MASK_POLICY_ID,
)


@dataclass(frozen=True)
class CandidateAdmissibility:
    candidate_id: str
    valid: bool
    invalid_reasons: tuple[str, ...]
    result: WarehouseGridlockStepResult
    cache_hit: bool = False


@dataclass(frozen=True)
class MaskResult:
    candidates_before: int
    candidates_after: int
    inadmissible_count: int
    query_count: int
    cache_hit_count: int
    admissible_direct_candidates: tuple[DirectActionCandidate, ...]
    query_results: tuple[CandidateAdmissibility, ...]
    mask_scope: str = "candidate_set"


def query_direct_candidate_admissibility(
    *,
    instance: WarehouseGridlockInstance,
    state: WarehouseGridlockState,
    candidate: DirectActionCandidate,
    max_seconds: int,
) -> CandidateAdmissibility:
    result = step(
        instance=instance,
        state=state,
        action=candidate.action,
        max_seconds=max_seconds,
    )
    return CandidateAdmissibility(
        candidate_id=candidate.candidate_id,
        valid=result.valid,
        invalid_reasons=result.invalid_reasons,
        result=result,
    )


def mask_direct_candidates(
    *,
    instance: WarehouseGridlockInstance,
    state: WarehouseGridlockState,
    candidates: list[DirectActionCandidate],
    max_seconds: int,
) -> MaskResult:
    query_results = tuple(
        query_direct_candidate_admissibility(
            instance=instance,
            state=state,
            candidate=candidate,
            max_seconds=max_seconds,
        )
        for candidate in candidates
    )
    valid_ids = {result.candidate_id for result in query_results if result.valid}
    admissible = tuple(candidate for candidate in candidates if candidate.candidate_id in valid_ids)
    return MaskResult(
        candidates_before=len(candidates),
        candidates_after=len(admissible),
        inadmissible_count=len(candidates) - len(admissible),
        query_count=len(candidates),
        cache_hit_count=0,
        admissible_direct_candidates=admissible,
        query_results=query_results,
    )


def mask_tower_action_candidates(
    *,
    instance: WarehouseGridlockInstance,
    state: WarehouseGridlockState,
    candidates: list[TowerActionCandidate],
    max_seconds: int,
) -> tuple[MaskResult, tuple[TowerActionCandidate, ...]]:
    direct_candidates = [candidate.concrete_candidate for candidate in candidates]
    direct_mask = mask_direct_candidates(
        instance=instance,
        state=state,
        candidates=direct_candidates,
        max_seconds=max_seconds,
    )
    valid_ids = {candidate.candidate_id for candidate in direct_mask.admissible_direct_candidates}
    tower_candidates = tuple(
        candidate
        for candidate in candidates
        if candidate.concrete_candidate.candidate_id in valid_ids
    )
    return direct_mask, tower_candidates


def direct_mask_event_row(
    *,
    run_id: str,
    arm_id: str,
    episode_index: int,
    step_index: int,
    state_id: str,
    candidate_generation_policy_id: str,
    mask_result: MaskResult,
    selected_action_id: str | None,
) -> dict[str, object]:
    return {
        "run_id": run_id,
        "arm_id": arm_id,
        "episode_index": episode_index,
        "step_index": step_index,
        "state_id": state_id,
        "candidate_generation_policy_id": candidate_generation_policy_id,
        "candidate_count_before_mask": mask_result.candidates_before,
        "candidate_count_after_mask": mask_result.candidates_after,
        "inadmissible_candidate_count": mask_result.inadmissible_count,
        "admissibility_query_count": mask_result.query_count,
        "cache_hit_count": mask_result.cache_hit_count,
        "selected_action_id": selected_action_id,
        "selected_action_admissible": selected_action_id is not None,
        "mask_scope": mask_result.mask_scope,
        "mask_policy_id": DIRECT_MASK_POLICY_ID,
        "successor_out_count_used_for_selection": False,
    }


def tower_action_mask_event_row(
    *,
    run_id: str,
    arm_id: str,
    episode_index: int,
    step_index: int,
    tier: int,
    state_cell_id: str,
    mask_result: MaskResult,
    selected_tower_action_id: str | None,
    selected_concrete_action_id: str | None,
) -> dict[str, object]:
    return {
        "run_id": run_id,
        "arm_id": arm_id,
        "episode_index": episode_index,
        "step_index": step_index,
        "tier": tier,
        "state_cell_id": state_cell_id,
        "tower_candidate_action_count_before_mask": mask_result.candidates_before,
        "tower_candidate_action_count_after_mask": mask_result.candidates_after,
        "inadmissible_tower_action_count": mask_result.inadmissible_count,
        "selected_tower_action_id": selected_tower_action_id,
        "selected_concrete_action_id": selected_concrete_action_id,
        "selected_concrete_action_admissible": selected_concrete_action_id is not None,
        "mask_scope": mask_result.mask_scope,
        "mask_policy_id": TOWER_MASK_POLICY_ID,
        "successor_out_count_used_for_selection": False,
    }
