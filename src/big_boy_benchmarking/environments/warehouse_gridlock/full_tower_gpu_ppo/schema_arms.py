"""Schema arm definitions for Warehouse full-tower PPO."""

from __future__ import annotations

import hashlib
import math
import random
from dataclasses import dataclass

from state_collapser.tower.partition.base_registry import BaseGraphRegistry
from state_collapser.tower.partition.ids import EdgeId, SchemaBlockId, StateId
from state_collapser.tower.partition.schema import NoContractionSchema

from .config import WarehouseFullTowerPPOArmConfig
from .ids import (
    WAREHOUSE_GRIDLOCK_DIRECT_NO_CONTRACTION_ARM_ID,
    WAREHOUSE_GRIDLOCK_NO_CONTRACTION_SCHEMA_ID,
    WAREHOUSE_GRIDLOCK_SOURCE_LOCAL_RATIO_SCHEMA_ID,
    WAREHOUSE_GRIDLOCK_TOWER_FIRST_NONTRIVIAL_ARM_ID,
)


@dataclass(frozen=True, slots=True)
class WarehouseSourceLocalOutgoingRatioSchema:
    """Select a stable catch-prefix of outgoing edges per source."""

    numerator: int = 9
    denominator: int = 10
    seed: int = 0
    min_selected_per_source: int = 1

    def __post_init__(self) -> None:
        if self.numerator <= 0:
            raise ValueError("numerator must be positive")
        if self.denominator <= 0:
            raise ValueError("denominator must be positive")
        if self.numerator > self.denominator:
            raise ValueError("numerator must be <= denominator")
        if self.min_selected_per_source < 0:
            raise ValueError("min_selected_per_source must be nonnegative")

    @property
    def block_id(self) -> SchemaBlockId:
        return SchemaBlockId(
            ("warehouse-source-local-ratio", self.numerator, self.denominator, self.seed)
        )

    def assign_edge(
        self,
        edge_id: EdgeId,
        registry: BaseGraphRegistry,
    ) -> SchemaBlockId | None:
        source_id = registry.source_state_id(edge_id)
        outgoing = tuple(registry.outgoing_edge_ids(source_id))
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
            _stable_shuffled_prefix(outgoing, selected_count, self.seed, source_id)
        )
        return self.block_id if edge_id in selected else None

    def ordered_blocks(self) -> tuple[SchemaBlockId, ...]:
        return (self.block_id,)

    def to_manifest(self) -> dict[str, object]:
        return {
            "schema_id": WAREHOUSE_GRIDLOCK_SOURCE_LOCAL_RATIO_SCHEMA_ID,
            "schema_mode": "source_local_ratio",
            "ratio_numerator": self.numerator,
            "ratio_denominator": self.denominator,
            "seed": self.seed,
            "min_selected_per_source": self.min_selected_per_source,
            "selector_rule_id": "warehouse_source_local_stable_rate_v001",
        }


def schema_for_arm(arm: WarehouseFullTowerPPOArmConfig, *, schema_seed: int) -> object:
    if arm.arm_id == WAREHOUSE_GRIDLOCK_DIRECT_NO_CONTRACTION_ARM_ID:
        if arm.schema_id != WAREHOUSE_GRIDLOCK_NO_CONTRACTION_SCHEMA_ID:
            raise ValueError("direct arm must use no-contraction schema")
        return NoContractionSchema()
    if arm.arm_id == WAREHOUSE_GRIDLOCK_TOWER_FIRST_NONTRIVIAL_ARM_ID:
        return WarehouseSourceLocalOutgoingRatioSchema(seed=schema_seed)
    raise ValueError(f"unknown full-tower PPO arm: {arm.arm_id!r}")


def schema_manifest_for_arm(
    arm: WarehouseFullTowerPPOArmConfig,
    *,
    schema_seed: int,
) -> dict[str, object]:
    schema = schema_for_arm(arm, schema_seed=schema_seed)
    if isinstance(schema, WarehouseSourceLocalOutgoingRatioSchema):
        return {
            "arm_id": arm.arm_id,
            "schema_id": arm.schema_id,
            "schema_kind": "nontrivial_source_local_ratio",
            "nontrivial_schema": True,
            **schema.to_manifest(),
        }
    return {
        "arm_id": arm.arm_id,
        "schema_id": arm.schema_id,
        "schema_kind": "no_contraction",
        "nontrivial_schema": False,
        "schema_seed": schema_seed,
    }


def _stable_shuffled_prefix(
    edge_ids: tuple[EdgeId, ...],
    selected_count: int,
    seed: int,
    source_id: StateId,
) -> tuple[EdgeId, ...]:
    decorated = []
    for edge_id in edge_ids:
        digest = hashlib.sha256(
            f"warehouse-source-local:{seed}:{source_id.value}:{edge_id.value}".encode(
                "utf-8"
            )
        ).hexdigest()
        decorated.append((digest, edge_id))
    decorated.sort(key=lambda item: item[0])
    selected = [edge_id for _, edge_id in decorated[:selected_count]]
    rng = random.Random(f"warehouse-source-local-order:{seed}:{source_id.value}")
    rng.shuffle(selected)
    return tuple(selected)
