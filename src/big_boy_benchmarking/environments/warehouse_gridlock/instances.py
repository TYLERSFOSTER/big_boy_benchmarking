"""Instance loading for Warehouse Gridlock."""

from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path

from big_boy_benchmarking.environments.warehouse_gridlock.graph import WarehouseGraph
from big_boy_benchmarking.environments.warehouse_gridlock.ids import (
    WAREHOUSE_GRIDLOCK_FULL_INSTANCE_ID,
)
from big_boy_benchmarking.environments.warehouse_gridlock.manifests import (
    WarehouseGridlockInstanceManifest,
    load_manifest,
)
from big_boy_benchmarking.environments.warehouse_gridlock.state import (
    WarehouseGridlockState,
)


@dataclass(frozen=True)
class WarehouseGridlockInstance:
    manifest: WarehouseGridlockInstanceManifest
    graph: WarehouseGraph
    start_state: WarehouseGridlockState
    target_state: WarehouseGridlockState


def load_instance(
    *,
    instance_id: str = WAREHOUSE_GRIDLOCK_FULL_INSTANCE_ID,
    manifest_path: Path | str | None = None,
) -> WarehouseGridlockInstance:
    manifest = load_manifest(manifest_path)
    if instance_id != manifest.instance_id:
        raise ValueError(f"unsupported Warehouse Gridlock instance id: {instance_id}")
    graph = manifest.build_graph()
    start_state = WarehouseGridlockState(
        robot_positions=manifest.robot_start_map(),
        box_positions=manifest.box_start_map(),
        time_step=0,
    )
    target_state = WarehouseGridlockState(
        robot_positions=manifest.robot_target_map(),
        box_positions=manifest.box_target_map(),
        time_step=0,
    )
    return WarehouseGridlockInstance(
        manifest=manifest,
        graph=graph,
        start_state=start_state,
        target_state=target_state,
    )
