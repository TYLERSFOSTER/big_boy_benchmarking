"""Manifest loading for Warehouse Gridlock."""

from __future__ import annotations

import json
from collections.abc import Mapping
from dataclasses import dataclass
from pathlib import Path
from typing import Any

from big_boy_benchmarking.environments.warehouse_gridlock.graph import (
    GridNode,
    WarehouseGraph,
    build_grid_graph,
)
from big_boy_benchmarking.environments.warehouse_gridlock.rewards import RewardPolicy


@dataclass(frozen=True)
class SourceDesignReference:
    source_design_note: str
    source_images: tuple[str, ...]


@dataclass(frozen=True)
class GridSpec:
    rows: int
    cols: int


@dataclass(frozen=True)
class RobotSpec:
    robot_id: str
    start: GridNode


@dataclass(frozen=True)
class BoxSpec:
    box_id: str
    start: GridNode


@dataclass(frozen=True)
class TargetSpec:
    entity_id: str
    target: GridNode


@dataclass(frozen=True)
class ColumnObstacleSpec:
    column_id: str
    blocked_node: GridNode
    source: str


@dataclass(frozen=True)
class CollisionPolicySpec:
    collision_policy_id: str
    shared_node_final_occupancy_invalid: bool
    head_on_edge_swaps_invalid: bool


@dataclass(frozen=True)
class TransitionPolicySpec:
    transition_policy_id: str
    invalid_ensemble_advances_time: bool
    partial_execution: bool
    push_only: bool


@dataclass(frozen=True)
class DiscoveryPolicySpec:
    discovery_policy_id: str
    cache_scope: str
    mask_policy: str
    query_policy: str


@dataclass(frozen=True)
class WarehouseGridlockInstanceManifest:
    environment_family_id: str
    implementation_family_id: str
    instance_id: str
    source: SourceDesignReference
    grid: GridSpec
    coordinate_convention: str
    graph_generation: Mapping[str, Any]
    columns: tuple[ColumnObstacleSpec, ...]
    robots: tuple[RobotSpec, ...]
    boxes: tuple[BoxSpec, ...]
    robot_targets: tuple[TargetSpec, ...]
    box_targets: tuple[TargetSpec, ...]
    collision_policy: CollisionPolicySpec
    transition_policy: TransitionPolicySpec
    reward_policy: RewardPolicy
    discovery_policy: DiscoveryPolicySpec
    claim_boundary: str

    @property
    def robot_ids(self) -> tuple[str, ...]:
        return tuple(robot.robot_id for robot in self.robots)

    @property
    def box_ids(self) -> tuple[str, ...]:
        return tuple(box.box_id for box in self.boxes)

    @property
    def blocked_nodes(self) -> frozenset[GridNode]:
        return frozenset(column.blocked_node for column in self.columns)

    def build_graph(self) -> WarehouseGraph:
        return build_grid_graph(
            rows=self.grid.rows,
            cols=self.grid.cols,
            blocked_nodes=self.blocked_nodes,
        )

    def robot_start_map(self) -> dict[str, GridNode]:
        return {robot.robot_id: robot.start for robot in self.robots}

    def box_start_map(self) -> dict[str, GridNode]:
        return {box.box_id: box.start for box in self.boxes}

    def robot_target_map(self) -> dict[str, GridNode]:
        return {target.entity_id: target.target for target in self.robot_targets}

    def box_target_map(self) -> dict[str, GridNode]:
        return {target.entity_id: target.target for target in self.box_targets}

    def to_dict(self) -> dict[str, Any]:
        return {
            "environment_family_id": self.environment_family_id,
            "implementation_family_id": self.implementation_family_id,
            "instance_id": self.instance_id,
            "source_design_note": self.source.source_design_note,
            "source_images": list(self.source.source_images),
            "grid": {"rows": self.grid.rows, "cols": self.grid.cols},
            "coordinate_convention": self.coordinate_convention,
            "nodes": self.graph_generation.get("nodes"),
            "edges": self.graph_generation.get("edges"),
            "blocked_nodes": [column.blocked_node.to_dict() for column in self.columns],
            "blocked_edges": [],
            "columns": [
                {
                    "column_id": column.column_id,
                    "blocked_node": column.blocked_node.to_dict(),
                    "source": column.source,
                }
                for column in self.columns
            ],
            "robots": {robot.robot_id: robot.start.to_dict() for robot in self.robots},
            "boxes": {box.box_id: box.start.to_dict() for box in self.boxes},
            "box_targets": {
                target.entity_id: target.target.to_dict() for target in self.box_targets
            },
            "robot_targets": {
                target.entity_id: target.target.to_dict() for target in self.robot_targets
            },
            "goal_policy": {
                "box_goal_required": True,
                "robot_goal_required": True,
                "exact_label_targets": True,
            },
            "collision_policy": self.collision_policy.__dict__,
            "transition_policy": self.transition_policy.__dict__,
            "reward_policy": self.reward_policy.to_dict(),
            "discovery_policy": self.discovery_policy.__dict__,
            "claim_boundary": self.claim_boundary,
        }


def default_manifest_path() -> Path:
    return (
        Path(__file__).resolve().parents[4]
        / "docs"
        / "environments"
        / "warehouse_gridlock_001"
        / "manifests"
        / "warehouse_gridlock_16x16_v001.json"
    )


def load_manifest(path: Path | str | None = None) -> WarehouseGridlockInstanceManifest:
    source = Path(path) if path is not None else default_manifest_path()
    payload = json.loads(source.read_text(encoding="utf-8"))
    return manifest_from_payload(payload)


def manifest_from_payload(payload: Mapping[str, Any]) -> WarehouseGridlockInstanceManifest:
    required = (
        "environment_family_id",
        "implementation_family_id",
        "instance_id",
        "source_design_note",
        "source_images",
        "grid",
        "coordinate_convention",
        "nodes",
        "edges",
        "columns",
        "robots",
        "boxes",
        "box_targets",
        "robot_targets",
        "collision_policy",
        "transition_policy",
        "reward_policy",
        "discovery_policy",
        "claim_boundary",
    )
    missing = [key for key in required if key not in payload]
    if missing:
        raise ValueError(f"missing Warehouse Gridlock manifest fields: {missing}")
    grid_payload = payload["grid"]
    reward_payload = payload["reward_policy"]
    return WarehouseGridlockInstanceManifest(
        environment_family_id=str(payload["environment_family_id"]),
        implementation_family_id=str(payload["implementation_family_id"]),
        instance_id=str(payload["instance_id"]),
        source=SourceDesignReference(
            source_design_note=str(payload["source_design_note"]),
            source_images=tuple(str(item) for item in payload["source_images"]),
        ),
        grid=GridSpec(rows=int(grid_payload["rows"]), cols=int(grid_payload["cols"])),
        coordinate_convention=str(payload["coordinate_convention"]),
        graph_generation={"nodes": payload["nodes"], "edges": payload["edges"]},
        columns=tuple(
            ColumnObstacleSpec(
                column_id=str(item["column_id"]),
                blocked_node=GridNode.from_dict(item["blocked_node"]),
                source=str(item.get("source", "manual_po_drawing_review")),
            )
            for item in payload["columns"]
        ),
        robots=tuple(
            RobotSpec(robot_id=str(robot_id), start=GridNode.from_dict(node))
            for robot_id, node in sorted(payload["robots"].items())
        ),
        boxes=tuple(
            BoxSpec(box_id=str(box_id), start=GridNode.from_dict(node))
            for box_id, node in sorted(payload["boxes"].items())
        ),
        robot_targets=tuple(
            TargetSpec(entity_id=str(robot_id), target=GridNode.from_dict(node))
            for robot_id, node in sorted(payload["robot_targets"].items())
        ),
        box_targets=tuple(
            TargetSpec(entity_id=str(box_id), target=GridNode.from_dict(node))
            for box_id, node in sorted(payload["box_targets"].items())
        ),
        collision_policy=CollisionPolicySpec(
            collision_policy_id=str(payload["collision_policy"]["collision_policy_id"]),
            shared_node_final_occupancy_invalid=bool(
                payload["collision_policy"]["shared_node_final_occupancy_invalid"]
            ),
            head_on_edge_swaps_invalid=bool(
                payload["collision_policy"]["head_on_edge_swaps_invalid"]
            ),
        ),
        transition_policy=TransitionPolicySpec(
            transition_policy_id=str(payload["transition_policy"]["transition_policy_id"]),
            invalid_ensemble_advances_time=bool(
                payload["transition_policy"]["invalid_ensemble_advances_time"]
            ),
            partial_execution=bool(payload["transition_policy"]["partial_execution"]),
            push_only=bool(payload["transition_policy"]["push_only"]),
        ),
        reward_policy=RewardPolicy(
            reward_policy_id=str(reward_payload["reward_policy_id"]),
            terminal_success_reward=float(reward_payload["terminal_success_reward"]),
            elapsed_time_penalty_per_second=float(
                reward_payload["elapsed_time_penalty_per_second"]
            ),
            correct_box_reward=float(reward_payload["correct_box_reward"]),
            correct_robot_reward=float(reward_payload["correct_robot_reward"]),
            invalid_action_penalty=float(reward_payload["invalid_action_penalty"]),
        ),
        discovery_policy=DiscoveryPolicySpec(
            discovery_policy_id=str(payload["discovery_policy"]["discovery_policy_id"]),
            cache_scope=str(payload["discovery_policy"]["cache_scope"]),
            mask_policy=str(payload["discovery_policy"]["mask_policy"]),
            query_policy=str(payload["discovery_policy"]["query_policy"]),
        ),
        claim_boundary=str(payload["claim_boundary"]),
    )
