"""Source-local outgoing-edge ratio schema for PlateSupport diagnostics."""

from __future__ import annotations

import hashlib
import math
import random
from dataclasses import dataclass, field

from state_collapser.tower.partition.base_registry import BaseGraphRegistry
from state_collapser.tower.partition.ids import EdgeId, SchemaBlockId, StateId


DEFAULT_ITERATED_SOURCE_LOCAL_SELECTOR_RULE_ID = (
    "plate_support_source_local_iterated_stable_rate_v001"
)
DEFAULT_ITERATED_SOURCE_LOCAL_SELECTION_MODE = (
    "quotient_source_representative_stable_rate"
)
SUPPORTED_ITERATED_SOURCE_LOCAL_SELECTION_MODES = (
    DEFAULT_ITERATED_SOURCE_LOCAL_SELECTION_MODE,
)


@dataclass(frozen=True, slots=True)
class SourceLocalOutgoingRatioSchema:
    """Select a stable catch-prefix of valid non-self outgoing edges per source."""

    numerator: int
    denominator: int
    seed: int = 0
    min_selected_per_source: int = 1

    def __post_init__(self) -> None:
        if self.numerator <= 0:
            raise ValueError("SourceLocalOutgoingRatioSchema.numerator must be positive.")
        if self.denominator <= 0:
            raise ValueError("SourceLocalOutgoingRatioSchema.denominator must be positive.")
        if self.min_selected_per_source < 0:
            raise ValueError(
                "SourceLocalOutgoingRatioSchema.min_selected_per_source must be nonnegative."
            )

    @property
    def block_id(self) -> SchemaBlockId:
        return SchemaBlockId(
            ("plate-support-source-local-ratio", self.numerator, self.denominator, self.seed)
        )

    def assign_edge(
        self,
        edge_id: EdgeId,
        registry: BaseGraphRegistry,
    ) -> SchemaBlockId | None:
        if _is_self_edge(edge_id, registry):
            return None
        source_id = registry.source_state_id(edge_id)
        outgoing = tuple(
            candidate
            for candidate in registry.outgoing_edge_ids(source_id)
            if not _is_self_edge(candidate, registry)
        )
        if not outgoing:
            return None
        selected_count = min(
            len(outgoing),
            max(
                self.min_selected_per_source,
                math.ceil(len(outgoing) * self.numerator / self.denominator),
            ),
        )
        selected = set(
            _stable_shuffled_prefix(outgoing, selected_count, self.seed, source_id.value)
        )
        return self.block_id if edge_id in selected else None

    def ordered_blocks(self) -> tuple[SchemaBlockId, ...]:
        return (self.block_id,)


def source_local_ratio_schema_id(numerator: int, denominator: int) -> str:
    return (
        "plate_support_schema_source_local_ratio_"
        f"{numerator:03d}_over_{denominator:03d}_v001"
    )


def source_local_ratio_iterated_schema_id(
    numerator: int,
    denominator: int,
    max_iterations: int,
) -> str:
    return (
        "plate_support_schema_source_local_ratio_iterated_"
        f"{numerator:03d}_over_{denominator:03d}_i{max_iterations:03d}_v001"
    )


@dataclass(slots=True)
class IteratedSourceLocalOutgoingRatioSchema:
    """Select stable quotient-local contraction blocks over multiple tiers."""

    numerator: int
    denominator: int
    seed: int = 0
    selector_rule_id: str = DEFAULT_ITERATED_SOURCE_LOCAL_SELECTOR_RULE_ID
    max_iterations: int = 32
    selection_mode: str = DEFAULT_ITERATED_SOURCE_LOCAL_SELECTION_MODE
    _planned_edge_signature: tuple[int, ...] = field(
        default=(),
        init=False,
        repr=False,
        compare=False,
    )
    _assignment_by_edge_id: dict[EdgeId, SchemaBlockId | None] = field(
        default_factory=dict,
        init=False,
        repr=False,
        compare=False,
    )
    _ordered_blocks: tuple[SchemaBlockId, ...] = field(
        default=(),
        init=False,
        repr=False,
        compare=False,
    )
    _plan_diagnostics: tuple[dict[str, object], ...] = field(
        default=(),
        init=False,
        repr=False,
        compare=False,
    )
    _stop_summary: dict[str, object] = field(
        default_factory=dict,
        init=False,
        repr=False,
        compare=False,
    )

    def __post_init__(self) -> None:
        if self.numerator <= 0:
            raise ValueError(
                "IteratedSourceLocalOutgoingRatioSchema.numerator must be positive."
            )
        if self.denominator <= 0:
            raise ValueError(
                "IteratedSourceLocalOutgoingRatioSchema.denominator must be positive."
            )
        if self.numerator > self.denominator:
            raise ValueError(
                "IteratedSourceLocalOutgoingRatioSchema.numerator must be less "
                "than or equal to denominator."
            )
        if not self.selector_rule_id:
            raise ValueError(
                "IteratedSourceLocalOutgoingRatioSchema.selector_rule_id must be nonempty."
            )
        if self.max_iterations <= 0:
            raise ValueError(
                "IteratedSourceLocalOutgoingRatioSchema.max_iterations must be positive."
            )
        if self.selection_mode not in SUPPORTED_ITERATED_SOURCE_LOCAL_SELECTION_MODES:
            raise ValueError(
                "IteratedSourceLocalOutgoingRatioSchema.selection_mode is unsupported: "
                f"{self.selection_mode!r}."
            )

    def assign_edge(
        self,
        edge_id: EdgeId,
        registry: BaseGraphRegistry,
    ) -> SchemaBlockId | None:
        self._ensure_plan(registry)
        return self._assignment_by_edge_id.get(edge_id)

    def ordered_blocks(self) -> tuple[SchemaBlockId, ...]:
        return self._ordered_blocks

    def plan_diagnostics(self) -> tuple[dict[str, object], ...]:
        return self._plan_diagnostics

    def stop_summary(self) -> dict[str, object]:
        return dict(self._stop_summary)

    def _ensure_plan(self, registry: BaseGraphRegistry) -> None:
        edge_signature = tuple(edge_id.value for edge_id in registry.edge_ids)
        if edge_signature == self._planned_edge_signature:
            return
        plan = _iterated_source_local_ratio_plan(
            registry=registry,
            numerator=self.numerator,
            denominator=self.denominator,
            seed=self.seed,
            selector_rule_id=self.selector_rule_id,
            max_iterations=self.max_iterations,
            selection_mode=self.selection_mode,
        )
        self._planned_edge_signature = edge_signature
        self._assignment_by_edge_id = plan.assignment_by_edge_id
        self._ordered_blocks = plan.ordered_blocks
        self._plan_diagnostics = plan.plan_diagnostics
        self._stop_summary = plan.stop_summary


@dataclass(frozen=True, slots=True)
class IteratedSourceLocalRatioPlan:
    assignment_by_edge_id: dict[EdgeId, SchemaBlockId | None]
    ordered_blocks: tuple[SchemaBlockId, ...]
    plan_diagnostics: tuple[dict[str, object], ...]
    stop_summary: dict[str, object]


def _stable_shuffled_prefix(
    edge_ids: tuple[EdgeId, ...],
    selected_count: int,
    seed: int,
    source_value: int,
) -> tuple[EdgeId, ...]:
    ordered = list(sorted(edge_ids, key=lambda edge_id: edge_id.value))
    rng = random.Random(f"plate-support-source-local-ratio:{seed}:{source_value}")
    rng.shuffle(ordered)
    return tuple(ordered[:selected_count])


def _is_self_edge(edge_id: EdgeId, registry: BaseGraphRegistry) -> bool:
    return registry.source_state_id(edge_id) == registry.target_state_id(edge_id)


def _iterated_source_local_ratio_plan(
    *,
    registry: BaseGraphRegistry,
    numerator: int,
    denominator: int,
    seed: int,
    selector_rule_id: str,
    max_iterations: int,
    selection_mode: str,
) -> IteratedSourceLocalRatioPlan:
    edge_ids = tuple(sorted(registry.edge_ids, key=lambda edge_id: edge_id.value))
    state_ids = tuple(registry.state_ids)
    parent: dict[StateId, StateId] = {state_id: state_id for state_id in state_ids}
    assignment: dict[EdgeId, SchemaBlockId | None] = {
        edge_id: None for edge_id in edge_ids
    }
    ordered_blocks: list[SchemaBlockId] = []
    diagnostic_rows: list[dict[str, object]] = []
    stop_reason = "max_iterations_reached"
    total_selected = 0
    total_changed = 0

    for iteration_index in range(max_iterations):
        component_count_before = _component_count(parent)
        if component_count_before <= 1:
            stop_reason = "component_count_leq_one"
            break
        candidates = _quotient_source_local_representative_edges(
            registry=registry,
            edge_ids=edge_ids,
            parent=parent,
        )
        if not candidates:
            stop_reason = "no_candidate_edges"
            diagnostic_rows.append(
                _iterated_plan_row(
                    iteration_index=iteration_index,
                    component_count_before=component_count_before,
                    candidate_edge_count=0,
                    selected_edge_count=0,
                    changed_union_count=0,
                    component_count_after=component_count_before,
                    block_id="",
                    iteration_status="stopped",
                    stop_reason=stop_reason,
                )
            )
            break
        selected = _selected_iterated_source_local_edges(
            registry=registry,
            candidates=candidates,
            parent=parent,
            numerator=numerator,
            denominator=denominator,
            seed=seed,
            selector_rule_id=selector_rule_id,
            selection_mode=selection_mode,
            iteration_index=iteration_index,
        )
        if not selected:
            stop_reason = "no_selected_edges"
            diagnostic_rows.append(
                _iterated_plan_row(
                    iteration_index=iteration_index,
                    component_count_before=component_count_before,
                    candidate_edge_count=len(candidates),
                    selected_edge_count=0,
                    changed_union_count=0,
                    component_count_after=component_count_before,
                    block_id="",
                    iteration_status="stopped",
                    stop_reason=stop_reason,
                )
            )
            break
        block_id = _iterated_source_local_ratio_block_id(
            numerator=numerator,
            denominator=denominator,
            selector_rule_id=selector_rule_id,
            seed=seed,
            iteration_index=iteration_index,
        )
        changed_count = 0
        for edge_id in selected:
            assignment[edge_id] = block_id
            if _union(
                parent,
                registry.source_state_id(edge_id),
                registry.target_state_id(edge_id),
            ):
                changed_count += 1
        component_count_after = _component_count(parent)
        total_selected += len(selected)
        total_changed += changed_count
        if changed_count == 0:
            stop_reason = "no_component_change"
            diagnostic_rows.append(
                _iterated_plan_row(
                    iteration_index=iteration_index,
                    component_count_before=component_count_before,
                    candidate_edge_count=len(candidates),
                    selected_edge_count=len(selected),
                    changed_union_count=0,
                    component_count_after=component_count_after,
                    block_id=repr(block_id.value),
                    iteration_status="stopped",
                    stop_reason=stop_reason,
                )
            )
            break
        ordered_blocks.append(block_id)
        diagnostic_rows.append(
            _iterated_plan_row(
                iteration_index=iteration_index,
                component_count_before=component_count_before,
                candidate_edge_count=len(candidates),
                selected_edge_count=len(selected),
                changed_union_count=changed_count,
                component_count_after=component_count_after,
                block_id=repr(block_id.value),
                iteration_status="completed",
                stop_reason="",
            )
        )
    else:
        stop_reason = "max_iterations_reached"

    final_component_count = _component_count(parent)
    stop_summary: dict[str, object] = {
        "max_iterations": max_iterations,
        "completed_iteration_count": len(ordered_blocks),
        "ordered_block_count": len(ordered_blocks),
        "final_component_count": final_component_count,
        "stop_reason": stop_reason,
        "selected_edge_count_total": total_selected,
        "changed_union_count_total": total_changed,
        "diagnostic_status": "ok",
    }
    return IteratedSourceLocalRatioPlan(
        assignment_by_edge_id=assignment,
        ordered_blocks=tuple(ordered_blocks),
        plan_diagnostics=tuple(diagnostic_rows),
        stop_summary=stop_summary,
    )


def _quotient_source_local_representative_edges(
    *,
    registry: BaseGraphRegistry,
    edge_ids: tuple[EdgeId, ...],
    parent: dict[StateId, StateId],
) -> tuple[EdgeId, ...]:
    representatives: dict[tuple[int, int, int], EdgeId] = {}
    representative_keys: dict[tuple[int, int, int], tuple[int, int, int, int]] = {}
    for edge_id in edge_ids:
        source_root = _find(parent, registry.source_state_id(edge_id))
        target_root = _find(parent, registry.target_state_id(edge_id))
        if source_root == target_root:
            continue
        action_id = registry.action_id_for_edge_id(edge_id)
        group_key = (source_root.value, target_root.value, action_id.value)
        edge_key = _edge_sort_key(registry=registry, edge_id=edge_id)
        current_key = representative_keys.get(group_key)
        if current_key is None or edge_key < current_key:
            representatives[group_key] = edge_id
            representative_keys[group_key] = edge_key
    return tuple(
        representatives[group_key]
        for group_key in sorted(
            representatives,
            key=lambda key: representative_keys[key],
        )
    )


def _selected_iterated_source_local_edges(
    *,
    registry: BaseGraphRegistry,
    candidates: tuple[EdgeId, ...],
    parent: dict[StateId, StateId],
    numerator: int,
    denominator: int,
    seed: int,
    selector_rule_id: str,
    selection_mode: str,
    iteration_index: int,
) -> tuple[EdgeId, ...]:
    selected: list[EdgeId] = []
    for edge_id in candidates:
        source_root = _find(parent, registry.source_state_id(edge_id))
        target_root = _find(parent, registry.target_state_id(edge_id))
        action_id = registry.action_id_for_edge_id(edge_id)
        score = stable_iterated_source_local_score(
            selector_rule_id=selector_rule_id,
            seed=seed,
            selection_mode=selection_mode,
            iteration_index=iteration_index,
            source_component_key=source_root.value,
            target_component_key=target_root.value,
            action_key=action_id.value,
            edge_key=_edge_sort_key(registry=registry, edge_id=edge_id),
        )
        if score < numerator / denominator:
            selected.append(edge_id)
    return tuple(selected)


def stable_iterated_source_local_score(
    *,
    selector_rule_id: str,
    seed: int,
    selection_mode: str,
    iteration_index: int,
    source_component_key: int,
    target_component_key: int,
    action_key: int,
    edge_key: tuple[int, int, int, int],
) -> float:
    payload = "|".join(
        (
            selector_rule_id,
            str(seed),
            selection_mode,
            str(iteration_index),
            str(source_component_key),
            str(target_component_key),
            str(action_key),
            ".".join(str(part) for part in edge_key),
        )
    )
    digest = hashlib.sha256(payload.encode("utf-8")).digest()
    integer = int.from_bytes(digest[:8], byteorder="big", signed=False)
    return integer / 2**64


def _edge_sort_key(
    *,
    registry: BaseGraphRegistry,
    edge_id: EdgeId,
) -> tuple[int, int, int, int]:
    return (
        registry.source_state_id(edge_id).value,
        registry.target_state_id(edge_id).value,
        registry.action_id_for_edge_id(edge_id).value,
        edge_id.value,
    )


def _iterated_source_local_ratio_block_id(
    *,
    numerator: int,
    denominator: int,
    selector_rule_id: str,
    seed: int,
    iteration_index: int,
) -> SchemaBlockId:
    return SchemaBlockId(
        (
            "plate-support-source-local-ratio-iterated",
            numerator,
            denominator,
            selector_rule_id,
            seed,
            iteration_index,
        )
    )


def _iterated_plan_row(
    *,
    iteration_index: int,
    component_count_before: int,
    candidate_edge_count: int,
    selected_edge_count: int,
    changed_union_count: int,
    component_count_after: int,
    block_id: str,
    iteration_status: str,
    stop_reason: str,
) -> dict[str, object]:
    return {
        "iteration_index": iteration_index,
        "component_count_before": component_count_before,
        "candidate_edge_count": candidate_edge_count,
        "selected_edge_count": selected_edge_count,
        "changed_union_count": changed_union_count,
        "component_count_after": component_count_after,
        "block_id": block_id,
        "iteration_status": iteration_status,
        "stop_reason": stop_reason,
        "diagnostic_status": "ok",
    }


def _find(parent: dict[StateId, StateId], item: StateId) -> StateId:
    current = item
    while parent[current] != current:
        parent[current] = parent[parent[current]]
        current = parent[current]
    return current


def _union(parent: dict[StateId, StateId], left: StateId, right: StateId) -> bool:
    left_root = _find(parent, left)
    right_root = _find(parent, right)
    if left_root == right_root:
        return False
    if right_root.value < left_root.value:
        left_root, right_root = right_root, left_root
    parent[right_root] = left_root
    return True


def _component_count(parent: dict[StateId, StateId]) -> int:
    return len({_find(parent, state_id) for state_id in parent})
