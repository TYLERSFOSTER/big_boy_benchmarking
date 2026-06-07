"""Source-local outgoing-edge ratio schema for PlateSupport diagnostics."""

from __future__ import annotations

import math
import random
from dataclasses import dataclass

from state_collapser.tower.partition.base_registry import BaseGraphRegistry
from state_collapser.tower.partition.ids import EdgeId, SchemaBlockId


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
    return f"plate_support_schema_source_local_ratio_{numerator:03d}_over_{denominator:03d}_v001"


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
