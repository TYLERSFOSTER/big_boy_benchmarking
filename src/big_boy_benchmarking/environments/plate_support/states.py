"""State-record helpers for PlateSupport."""

from __future__ import annotations

import json
from typing import Any

from big_boy_benchmarking.environments.plate_support.types import StateRecord
from big_boy_benchmarking.environments.plate_support.upstream import (
    ImportedPlateSupportSurface,
    import_plate_support_surface,
)


def _json_text(value: Any) -> str:
    return json.dumps(value, sort_keys=True, separators=(",", ":"))


def state_id(state: Any) -> str:
    return (
        "plate_support_state:"
        f"x{state.x_idx}:y{state.y_idx}:theta{state.theta_idx}:"
        f"e{state.e1}-{state.e2}-{state.e3}"
    )


def support_pattern(state: Any) -> tuple[int, int, int]:
    return (int(state.e1 > 0), int(state.e2 > 0), int(state.e3 > 0))


def state_to_record(
    state: Any,
    *,
    role: str = "",
    surface: ImportedPlateSupportSurface | None = None,
) -> StateRecord:
    surface = surface or import_plate_support_surface()
    return StateRecord(
        state_id=state_id(state),
        x_idx=int(state.x_idx),
        y_idx=int(state.y_idx),
        theta_idx=int(state.theta_idx),
        e1=int(state.e1),
        e2=int(state.e2),
        e3=int(state.e3),
        support_pattern=_json_text(support_pattern(state)),
        socket_positions=_json_text(surface.ordered_socket_world_positions(state)),
        reachability_pattern=_json_text(surface.engaged_arm_reachability(state)),
        minimum_engaged_supports=bool(surface.has_minimum_engaged_supports(state)),
        stable_support_pattern=bool(surface.has_stable_support_pattern(state)),
        sockets_in_bounds=bool(surface.all_sockets_in_bounds(state)),
        valid_state=bool(surface.is_valid_state(state)),
        coarse_position=_json_text(surface.coarse_plate_support_position(state)),
        fine_position=_json_text(surface.fine_plate_support_position(state)),
        role=role,
    )


def valid_state_records(
    *,
    surface: ImportedPlateSupportSurface | None = None,
) -> list[StateRecord]:
    surface = surface or import_plate_support_surface()
    return [state_to_record(state, surface=surface) for state in surface.all_valid_states()]


def candidate_state_records(
    *,
    surface: ImportedPlateSupportSurface | None = None,
) -> list[StateRecord]:
    surface = surface or import_plate_support_surface()
    return [state_to_record(state, surface=surface) for state in surface.all_candidate_states()]
