"""Scoped tower surface for the Warehouse live-lift diagnostic."""

from __future__ import annotations

import hashlib
from dataclasses import dataclass

from big_boy_benchmarking.environments.warehouse_gridlock.instances import (
    WarehouseGridlockInstance,
)
from big_boy_benchmarking.environments.warehouse_gridlock.rewards import target_counts
from big_boy_benchmarking.environments.warehouse_gridlock.state import (
    WarehouseGridlockState,
)
from big_boy_benchmarking.environments.warehouse_gridlock.masked_direct_vs_live_lift_tower.admissibility import (
    MaskResult,
    mask_direct_candidates,
)
from big_boy_benchmarking.environments.warehouse_gridlock.masked_direct_vs_live_lift_tower.candidate_generation import (
    DirectActionCandidate,
    TowerActionCandidate,
    TowerLiftCandidate,
    generate_direct_candidates,
    tower_action_candidates_from_direct,
)
from big_boy_benchmarking.environments.warehouse_gridlock.masked_direct_vs_live_lift_tower.config import (
    LIVE_LIFT_POLICY_ID,
    TOWER_CANDIDATE_POLICY_ID,
    TOWER_SCHEMA_ID,
    TOWER_SURFACE_POLICY_ID,
)
from big_boy_benchmarking.environments.warehouse_gridlock.masked_direct_vs_live_lift_tower.warehouse_tower_adapter import (
    WarehouseGeneratedEdge,
    WarehouseGeneratedHiddenGraph,
)


@dataclass(frozen=True)
class WarehouseTowerSurface:
    current_state: WarehouseGridlockState
    tier: int
    state_cell_id: str
    direct_candidates: tuple[DirectActionCandidate, ...]
    mask_result: MaskResult
    valid_edges: tuple[WarehouseGeneratedEdge, ...]
    hidden_graph: WarehouseGeneratedHiddenGraph
    schema_seed: int
    candidate_budget: int
    max_active_robots: int
    candidate_mix_id: str
    complete_full_action_surface: bool = False
    complete_generated_candidate_surface: bool = True

    @property
    def live_out_count(self) -> int:
        return len(self.valid_edges)

    def lift_candidates(self) -> tuple[TowerLiftCandidate, ...]:
        digest = hashlib.sha256(
            f"{self.schema_seed}:{self.current_state.stable_id}".encode("utf-8")
        ).hexdigest()[:16]
        return (
            TowerLiftCandidate(
                candidate_id=f"lift-{self.schema_seed}-{digest}",
                downstairs_state_id=self.current_state.stable_id,
                lift_state=self.current_state,
                tier=self.tier,
                state_cell_id=self.state_cell_id,
                out_count=self.live_out_count,
                out_scope="generated_discovered_surface",
            ),
        )

    def tower_action_candidates(self) -> list[TowerActionCandidate]:
        return tower_action_candidates_from_direct(
            direct_candidates=list(self.direct_candidates),
            tier=self.tier,
            state_cell_id=self.state_cell_id,
            budget=self.candidate_budget,
        )

    def surface_scope_row(self, *, run_id: str) -> dict[str, object]:
        return {
            "run_id": run_id,
            "schema_seed": self.schema_seed,
            "surface_scope": "generated_discovered_surface",
            "surface_generation_policy_id": TOWER_SURFACE_POLICY_ID,
            "surface_generation_budget": self.candidate_budget,
            "max_active_robots": self.max_active_robots,
            "candidate_mix_id": self.candidate_mix_id,
            "state_count": len(
                {edge.source.stable_id for edge in self.valid_edges}
                | {edge.target.stable_id for edge in self.valid_edges}
            ),
            "generated_candidate_count": len(self.direct_candidates),
            "valid_edge_count": len(self.valid_edges),
            "invalid_candidate_count": self.mask_result.inadmissible_count,
            "complete_full_action_surface": self.complete_full_action_surface,
            "complete_generated_candidate_surface": self.complete_generated_candidate_surface,
        }

    def tower_shape_rows(self, *, run_id: str) -> list[dict[str, object]]:
        valid_action_ids = {edge.action.stable_id for edge in self.valid_edges}
        action_cells = {
            candidate.action_cell_id
            for candidate in self.tower_action_candidates()
            if candidate.concrete_candidate.action.stable_id in valid_action_ids
        }
        return [
            {
                "run_id": run_id,
                "schema_seed": self.schema_seed,
                "schema_id": TOWER_SCHEMA_ID,
                "schema_mode": "source_local_ratio_iterated_over_generated_surface",
                "ratio_numerator": 9,
                "ratio_denominator": 10,
                "max_iterations": 1,
                "tier_count": 2,
                "tier": 0,
                "state_cell_count": 1,
                "action_cell_count": len(self.valid_edges),
                "valid_edge_count": len(self.valid_edges),
                "surface_scope": "generated_discovered_surface",
                "complete_full_action_surface": False,
            },
            {
                "run_id": run_id,
                "schema_seed": self.schema_seed,
                "schema_id": TOWER_SCHEMA_ID,
                "schema_mode": "source_local_ratio_iterated_over_generated_surface",
                "ratio_numerator": 9,
                "ratio_denominator": 10,
                "max_iterations": 1,
                "tier_count": 2,
                "tier": self.tier,
                "state_cell_count": 1,
                "action_cell_count": len(action_cells),
                "valid_edge_count": len(self.valid_edges),
                "surface_scope": "generated_discovered_surface",
                "complete_full_action_surface": False,
            },
        ]


def build_tower_surface(
    *,
    instance: WarehouseGridlockInstance,
    state: WarehouseGridlockState,
    candidate_budget: int,
    seed: int,
    schema_seed: int,
    max_seconds: int,
    max_active_robots: int,
    candidate_mix_id: str,
) -> WarehouseTowerSurface:
    candidates = generate_direct_candidates(
        instance=instance,
        state=state,
        budget=candidate_budget,
        seed=seed,
        max_active_robots=max_active_robots,
        candidate_mix_id=candidate_mix_id,
    )
    mask_result = mask_direct_candidates(
        instance=instance,
        state=state,
        candidates=candidates,
        max_seconds=max_seconds,
    )
    by_id = {candidate.candidate_id: candidate for candidate in candidates}
    edges = []
    for query in mask_result.query_results:
        if not query.valid:
            continue
        candidate = by_id[query.candidate_id]
        edges.append(
            WarehouseGeneratedEdge(
                source=state,
                action=candidate.action,
                target=query.result.next_state,
                reward=query.result.reward,
                labels=(
                    "warehouse_gridlock_generated_transition",
                    ("candidate_policy_id", candidate.policy_id),
                    ("candidate_scope", candidate.generation_scope),
                    ("active_robot_count", candidate.active_robot_count),
                    ("valid_transition", True),
                ),
            )
        )
    state_cell_id = _state_cell_id(instance=instance, state=state)
    return WarehouseTowerSurface(
        current_state=state,
        tier=1,
        state_cell_id=state_cell_id,
        direct_candidates=tuple(candidates),
        mask_result=mask_result,
        valid_edges=tuple(edges),
        hidden_graph=WarehouseGeneratedHiddenGraph(edges),
        schema_seed=schema_seed,
        candidate_budget=candidate_budget,
        max_active_robots=max_active_robots,
        candidate_mix_id=candidate_mix_id,
    )


def select_live_lift(surface: WarehouseTowerSurface) -> tuple[TowerLiftCandidate | None, str]:
    candidates = surface.lift_candidates()
    live = [candidate for candidate in candidates if candidate.live]
    if not candidates:
        return None, "no_fiber_candidates"
    if not live:
        return None, "no_live_lift_candidates"
    return live[0], "deterministic_first_live_lift"


def tower_state_lift_event_row(
    *,
    run_id: str,
    arm_id: str,
    episode_index: int,
    step_index: int,
    surface: WarehouseTowerSurface,
    selected: TowerLiftCandidate | None,
    failure_reason: str,
) -> dict[str, object]:
    candidates = surface.lift_candidates()
    live = [candidate for candidate in candidates if candidate.live]
    return {
        "run_id": run_id,
        "arm_id": arm_id,
        "episode_index": episode_index,
        "step_index": step_index,
        "downstairs_state_id": surface.current_state.stable_id,
        "tier": surface.tier,
        "state_cell_id": surface.state_cell_id,
        "fiber_candidate_count": len(candidates),
        "live_lift_candidate_count": len(live),
        "dead_lift_candidate_count": len(candidates) - len(live),
        "selected_lift_state_id": selected.lift_state.stable_id if selected else None,
        "selected_lift_out_count": selected.out_count if selected else 0,
        "lift_failure": selected is None,
        "failure_reason": "" if selected else failure_reason,
        "out_scope": "generated_discovered_surface",
        "lift_policy_id": LIVE_LIFT_POLICY_ID,
    }


def _state_cell_id(*, instance: WarehouseGridlockInstance, state: WarehouseGridlockState) -> str:
    counts = target_counts(
        state,
        robot_targets=instance.manifest.robot_target_map(),
        box_targets=instance.manifest.box_target_map(),
    )
    return (
        "warehouse_tier1_progress_cell:"
        f"boxes={counts['correct_box_count']}:robots={counts['correct_robot_count']}"
    )
