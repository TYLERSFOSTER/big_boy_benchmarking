"""Full-state token encoding for Warehouse Gridlock transformer policies."""

from __future__ import annotations

from dataclasses import dataclass
from typing import Any

from ..policies.contracts import (
    WarehouseFullSystemConfig,
)
from .torch_runtime import require_torch

TOKEN_TYPE_GLOBAL = 0
TOKEN_TYPE_ROBOT = 1
TOKEN_TYPE_BOX = 2
TOKEN_TYPE_BLOCKED = 3
TOKEN_TYPE_TOWER_CONTEXT = 4

TOKEN_TYPE_NAMES = {
    TOKEN_TYPE_GLOBAL: "global",
    TOKEN_TYPE_ROBOT: "robot",
    TOKEN_TYPE_BOX: "box",
    TOKEN_TYPE_BLOCKED: "blocked_column",
    TOKEN_TYPE_TOWER_CONTEXT: "tower_context",
}


@dataclass(frozen=True)
class WarehouseEncodingContext:
    arm_id: str
    second: int
    max_seconds: int
    tier: int | None = None
    tier_state_id: str | None = None
    live_lift_out_count: int = 0
    candidate_count: int = 0

    @property
    def is_tower(self) -> bool:
        return self.tier is not None


@dataclass(frozen=True)
class EncodedWarehouseBatch:
    token_type_ids: Any
    entity_id_ids: Any
    row_ids: Any
    col_ids: Any
    target_row_ids: Any
    target_col_ids: Any
    scalar_features: Any
    robot_token_indices: Any
    robot_ids: tuple[str, ...]
    token_type_names: dict[int, str]

    def to(self, device: str) -> EncodedWarehouseBatch:
        return EncodedWarehouseBatch(
            token_type_ids=self.token_type_ids.to(device),
            entity_id_ids=self.entity_id_ids.to(device),
            row_ids=self.row_ids.to(device),
            col_ids=self.col_ids.to(device),
            target_row_ids=self.target_row_ids.to(device),
            target_col_ids=self.target_col_ids.to(device),
            scalar_features=self.scalar_features.to(device),
            robot_token_indices=self.robot_token_indices.to(device),
            robot_ids=self.robot_ids,
            token_type_names=self.token_type_names,
        )


def encode_warehouse_batch(
    configs: list[WarehouseFullSystemConfig],
    contexts: list[WarehouseEncodingContext],
    *,
    device: str = "cpu",
) -> EncodedWarehouseBatch:
    if len(configs) != len(contexts):
        raise ValueError("configs and contexts must have the same length")
    if not configs:
        raise ValueError("expected at least one config")
    torch = require_torch()
    token_rows = [
        _token_rows(config=config, context=context)
        for config, context in zip(configs, contexts, strict=True)
    ]
    max_tokens = max(len(rows) for rows in token_rows)
    padded = [_pad_rows(rows, max_tokens=max_tokens) for rows in token_rows]
    robot_ids = tuple(sorted(configs[0].static.robot_ids))
    robot_indices = []
    for rows in padded:
        indices = []
        for robot_id in robot_ids:
            matches = [
                index
                for index, row in enumerate(rows)
                if row["token_type_id"] == TOKEN_TYPE_ROBOT and row["entity_label"] == robot_id
            ]
            if len(matches) != 1:
                raise ValueError(f"expected exactly one token for robot {robot_id}")
            indices.append(matches[0])
        robot_indices.append(indices)
    return EncodedWarehouseBatch(
        token_type_ids=torch.tensor(
            [[row["token_type_id"] for row in rows] for rows in padded],
            dtype=torch.long,
            device=device,
        ),
        entity_id_ids=torch.tensor(
            [[row["entity_id_id"] for row in rows] for rows in padded],
            dtype=torch.long,
            device=device,
        ),
        row_ids=torch.tensor(
            [[row["row_id"] for row in rows] for rows in padded],
            dtype=torch.long,
            device=device,
        ),
        col_ids=torch.tensor(
            [[row["col_id"] for row in rows] for rows in padded],
            dtype=torch.long,
            device=device,
        ),
        target_row_ids=torch.tensor(
            [[row["target_row_id"] for row in rows] for rows in padded],
            dtype=torch.long,
            device=device,
        ),
        target_col_ids=torch.tensor(
            [[row["target_col_id"] for row in rows] for rows in padded],
            dtype=torch.long,
            device=device,
        ),
        scalar_features=torch.tensor(
            [[row["scalar_features"] for row in rows] for rows in padded],
            dtype=torch.float32,
            device=device,
        ),
        robot_token_indices=torch.tensor(robot_indices, dtype=torch.long, device=device),
        robot_ids=robot_ids,
        token_type_names=TOKEN_TYPE_NAMES,
    )


def _token_rows(
    *,
    config: WarehouseFullSystemConfig,
    context: WarehouseEncodingContext,
) -> list[dict[str, object]]:
    max_seconds = max(1, context.max_seconds)
    time_fraction = min(max(context.second / max_seconds, 0.0), 1.0)
    remaining_fraction = min(max((max_seconds - context.second) / max_seconds, 0.0), 1.0)
    rows: list[dict[str, object]] = [
        _row(
            token_type_id=TOKEN_TYPE_GLOBAL,
            entity_label="global",
            entity_id_id=0,
            row=0,
            col=0,
            target_row=0,
            target_col=0,
            scalar_features=[
                time_fraction,
                remaining_fraction,
                float(config.dynamic.terminal),
                1.0 if context.is_tower else 0.0,
                float(context.candidate_count),
                float(context.live_lift_out_count),
            ],
        )
    ]
    robot_targets = config.static.robot_target_map
    box_targets = config.static.box_target_map
    for index, robot_id in enumerate(sorted(config.static.robot_ids), start=1):
        node = _parse_node(config.dynamic.robot_positions[robot_id])
        target = _parse_node(robot_targets[robot_id])
        rows.append(
            _row(
                token_type_id=TOKEN_TYPE_ROBOT,
                entity_label=robot_id,
                entity_id_id=index,
                row=node[0],
                col=node[1],
                target_row=target[0],
                target_col=target[1],
                scalar_features=[
                    time_fraction,
                    remaining_fraction,
                    float(node == target),
                    1.0 if context.is_tower else 0.0,
                    float(context.candidate_count),
                    float(context.live_lift_out_count),
                ],
            )
        )
    offset = len(config.static.robot_ids) + 1
    for index, box_id in enumerate(sorted(config.static.box_ids), start=offset):
        node = _parse_node(config.dynamic.box_positions[box_id])
        target = _parse_node(box_targets[box_id])
        rows.append(
            _row(
                token_type_id=TOKEN_TYPE_BOX,
                entity_label=box_id,
                entity_id_id=index,
                row=node[0],
                col=node[1],
                target_row=target[0],
                target_col=target[1],
                scalar_features=[
                    time_fraction,
                    remaining_fraction,
                    float(node == target),
                    1.0 if context.is_tower else 0.0,
                    float(context.candidate_count),
                    float(context.live_lift_out_count),
                ],
            )
        )
    blocked_offset = offset + len(config.static.box_ids)
    for index, node_key in enumerate(sorted(config.static.blocked_nodes), start=blocked_offset):
        row, col = _parse_node(node_key)
        rows.append(
            _row(
                token_type_id=TOKEN_TYPE_BLOCKED,
                entity_label=f"blocked:{node_key}",
                entity_id_id=index,
                row=row,
                col=col,
                target_row=row,
                target_col=col,
                scalar_features=[
                    time_fraction,
                    remaining_fraction,
                    0.0,
                    1.0 if context.is_tower else 0.0,
                    float(context.candidate_count),
                    float(context.live_lift_out_count),
                ],
            )
        )
    if context.is_tower:
        rows.append(
            _row(
                token_type_id=TOKEN_TYPE_TOWER_CONTEXT,
                entity_label=context.tier_state_id or "tower_context",
                entity_id_id=blocked_offset + len(config.static.blocked_nodes) + 1,
                row=0,
                col=0,
                target_row=0,
                target_col=0,
                scalar_features=[
                    time_fraction,
                    remaining_fraction,
                    float(context.tier or 0),
                    1.0,
                    float(context.candidate_count),
                    float(context.live_lift_out_count),
                ],
            )
        )
    return rows


def _row(
    *,
    token_type_id: int,
    entity_label: str,
    entity_id_id: int,
    row: int,
    col: int,
    target_row: int,
    target_col: int,
    scalar_features: list[float],
) -> dict[str, object]:
    return {
        "token_type_id": token_type_id,
        "entity_label": entity_label,
        "entity_id_id": entity_id_id,
        "row_id": max(0, row),
        "col_id": max(0, col),
        "target_row_id": max(0, target_row),
        "target_col_id": max(0, target_col),
        "scalar_features": scalar_features,
    }


def _pad_rows(rows: list[dict[str, object]], *, max_tokens: int) -> list[dict[str, object]]:
    padded = list(rows)
    while len(padded) < max_tokens:
        padded.append(
            _row(
                token_type_id=TOKEN_TYPE_GLOBAL,
                entity_label="pad",
                entity_id_id=0,
                row=0,
                col=0,
                target_row=0,
                target_col=0,
                scalar_features=[0.0, 0.0, 0.0, 0.0, 0.0, 0.0],
            )
        )
    return padded


def _parse_node(node_key: str) -> tuple[int, int]:
    return int(node_key[1:3]), int(node_key[4:6])
