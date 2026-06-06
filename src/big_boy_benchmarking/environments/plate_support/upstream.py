"""Centralized upstream PlateSupport imports."""

from __future__ import annotations

from dataclasses import dataclass
from importlib import import_module
from typing import Any

from big_boy_benchmarking.environments.plate_support.ids import (
    UPSTREAM_MODULE,
    UPSTREAM_SMOKE_ID,
)


class PlateSupportSurfaceImportError(RuntimeError):
    """Raised when the installed upstream PlateSupport surface is incomplete."""


REQUIRED_SURFACE_NAMES: tuple[str, ...] = (
    "PlateSupportEnv",
    "PlateSupportState",
    "PlateSupportEnvRuntime",
    "PlateSupportExploitExploreRuntime",
    "PlateSupportLiftResolveExecutor",
    "PlateSupportTierLearner",
    "TowerTrainingConfig",
    "ExploitExploreTrainingConfig",
    "run_tower_training",
    "run_exploit_explore_training",
    "default_plate_support_schema",
    "ACTION_COUNT",
    "MAX_STEPS",
    "START_STATE",
    "CANDIDATE_GOAL_STATE",
    "all_candidate_states",
    "all_valid_states",
    "valid_outgoing_transitions",
    "primitive_transition",
    "transition_reward",
    "transition_terminated",
    "transition_truncated",
    "is_valid_state",
    "ordered_socket_world_positions",
    "engaged_arm_reachability",
    "has_minimum_engaged_supports",
    "has_stable_support_pattern",
    "all_sockets_in_bounds",
    "coarse_plate_support_position",
    "fine_plate_support_position",
)


@dataclass(frozen=True)
class ImportedPlateSupportSurface:
    module: Any
    smoke_id: str
    PlateSupportEnv: type[Any]
    PlateSupportState: type[Any]
    PlateSupportEnvRuntime: type[Any]
    PlateSupportExploitExploreRuntime: type[Any]
    PlateSupportLiftResolveExecutor: type[Any]
    PlateSupportTierLearner: type[Any]
    TowerTrainingConfig: type[Any]
    ExploitExploreTrainingConfig: type[Any]
    run_tower_training: Any
    run_exploit_explore_training: Any
    default_plate_support_schema: Any
    ACTION_COUNT: int
    MAX_STEPS: int
    START_STATE: Any
    CANDIDATE_GOAL_STATE: Any
    all_candidate_states: Any
    all_valid_states: Any
    valid_outgoing_transitions: Any
    primitive_transition: Any
    transition_reward: Any
    transition_terminated: Any
    transition_truncated: Any
    is_valid_state: Any
    ordered_socket_world_positions: Any
    engaged_arm_reachability: Any
    has_minimum_engaged_supports: Any
    has_stable_support_pattern: Any
    all_sockets_in_bounds: Any
    coarse_plate_support_position: Any
    fine_plate_support_position: Any

    def create_env(self) -> Any:
        return self.PlateSupportEnv()

    def create_runtime(self, *, schema: Any | None = None) -> Any:
        if schema is None:
            return self.PlateSupportEnvRuntime(self.create_env())
        return self.PlateSupportEnvRuntime(self.create_env(), contraction_schema=schema)

    def training_surface_availability(self) -> dict[str, bool]:
        return {
            "PlateSupportEnvRuntime": self.PlateSupportEnvRuntime is not None,
            "PlateSupportExploitExploreRuntime": self.PlateSupportExploitExploreRuntime
            is not None,
            "PlateSupportLiftResolveExecutor": self.PlateSupportLiftResolveExecutor
            is not None,
            "PlateSupportTierLearner": self.PlateSupportTierLearner is not None,
            "TowerTrainingConfig": self.TowerTrainingConfig is not None,
            "ExploitExploreTrainingConfig": self.ExploitExploreTrainingConfig is not None,
            "run_tower_training": self.run_tower_training is not None,
            "run_exploit_explore_training": self.run_exploit_explore_training is not None,
        }


def import_plate_support_surface() -> ImportedPlateSupportSurface:
    try:
        module = import_module(UPSTREAM_MODULE)
    except Exception as exc:
        raise PlateSupportSurfaceImportError(
            f"failed to import upstream PlateSupport module {UPSTREAM_MODULE}: {exc}"
        ) from exc

    missing = tuple(name for name in REQUIRED_SURFACE_NAMES if not hasattr(module, name))
    if missing:
        raise PlateSupportSurfaceImportError(
            "installed state_collapser PlateSupport surface is missing: "
            + ", ".join(missing)
        )

    kwargs = {name: getattr(module, name) for name in REQUIRED_SURFACE_NAMES}
    return ImportedPlateSupportSurface(
        module=module,
        smoke_id=UPSTREAM_SMOKE_ID,
        **kwargs,
    )
