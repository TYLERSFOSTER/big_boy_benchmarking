"""Immediate-admissibility resolver for full Warehouse action vectors."""

from __future__ import annotations

from dataclasses import dataclass

from big_boy_benchmarking.environments.warehouse_gridlock.actions import DirectionOrStay
from big_boy_benchmarking.environments.warehouse_gridlock.instances import (
    WarehouseGridlockInstance,
)
from big_boy_benchmarking.environments.warehouse_gridlock.policies.contracts import (
    WarehouseFullActionVector,
    WarehouseProjectionTrace,
)
from big_boy_benchmarking.environments.warehouse_gridlock.state import WarehouseGridlockState
from big_boy_benchmarking.environments.warehouse_gridlock.transition import (
    WarehouseGridlockStepResult,
    step,
)

PROJECTION_STRATEGY_ID = "bounded_deterministic_repair_with_all_stay_fallback_v001"


@dataclass(frozen=True)
class ResolvedWarehouseAction:
    selected_action_vector: WarehouseFullActionVector
    step_result: WarehouseGridlockStepResult
    projection_trace: WarehouseProjectionTrace
    raw_step_result: WarehouseGridlockStepResult


@dataclass(frozen=True)
class BoundedDeterministicWarehouseActionResolver:
    projection_attempt_budget: int = 64
    projection_strategy_id: str = PROJECTION_STRATEGY_ID

    def resolve(
        self,
        *,
        instance: WarehouseGridlockInstance,
        state: WarehouseGridlockState,
        raw_action_vector: WarehouseFullActionVector,
        max_seconds: int,
        robot_command_margins: dict[str, float] | None = None,
    ) -> ResolvedWarehouseAction:
        invalid_reasons_seen: set[str] = set()
        raw_result = step(
            instance=instance,
            state=state,
            action=raw_action_vector.to_action(),
            max_seconds=max_seconds,
        )
        invalid_reasons_seen.update(raw_result.invalid_reasons)
        if raw_result.valid:
            return ResolvedWarehouseAction(
                selected_action_vector=raw_action_vector,
                step_result=raw_result,
                raw_step_result=raw_result,
                projection_trace=WarehouseProjectionTrace(
                    projection_strategy_id=self.projection_strategy_id,
                    projection_attempt_budget=self.projection_attempt_budget,
                    attempt_count=1,
                    raw_valid=True,
                    selected_valid=True,
                    fallback_used=False,
                    invalid_reasons_seen=tuple(sorted(invalid_reasons_seen)),
                    selected_reason="raw_valid",
                    successor_out_count_used_for_selection=False,
                ),
            )

        attempts = 1
        ordered_robots = self._repair_order(raw_action_vector, robot_command_margins or {})
        moving_robots = [
            robot_id
            for robot_id in ordered_robots
            if raw_action_vector.commands[robot_id] != DirectionOrStay.STAY
        ]

        for robot_id in moving_robots:
            if attempts >= self.projection_attempt_budget:
                break
            commands = dict(raw_action_vector.commands)
            commands[robot_id] = DirectionOrStay.STAY
            candidate = WarehouseFullActionVector(commands=commands)
            result = step(
                instance=instance,
                state=state,
                action=candidate.to_action(),
                max_seconds=max_seconds,
            )
            attempts += 1
            invalid_reasons_seen.update(result.invalid_reasons)
            if result.valid:
                return self._resolved(
                    vector=candidate,
                    result=result,
                    raw_result=raw_result,
                    attempts=attempts,
                    raw_valid=False,
                    fallback=False,
                    invalid_reasons_seen=invalid_reasons_seen,
                    selected_reason=f"single_robot_repair:{robot_id}",
                )

        commands = dict(raw_action_vector.commands)
        for index, robot_id in enumerate(moving_robots, start=1):
            if attempts >= self.projection_attempt_budget:
                break
            commands[robot_id] = DirectionOrStay.STAY
            candidate = WarehouseFullActionVector(commands=dict(commands))
            result = step(
                instance=instance,
                state=state,
                action=candidate.to_action(),
                max_seconds=max_seconds,
            )
            attempts += 1
            invalid_reasons_seen.update(result.invalid_reasons)
            if result.valid:
                return self._resolved(
                    vector=candidate,
                    result=result,
                    raw_result=raw_result,
                    attempts=attempts,
                    raw_valid=False,
                    fallback=False,
                    invalid_reasons_seen=invalid_reasons_seen,
                    selected_reason=f"prefix_repair:{index}",
                )

        all_stay = WarehouseFullActionVector.all_stay(tuple(sorted(instance.manifest.robot_ids)))
        stay_result = step(
            instance=instance,
            state=state,
            action=all_stay.to_action(),
            max_seconds=max_seconds,
        )
        attempts += 1
        invalid_reasons_seen.update(stay_result.invalid_reasons)
        if not stay_result.valid:
            raise RuntimeError("Warehouse all-stay fallback was invalid; environment invariant failed")
        return self._resolved(
            vector=all_stay,
            result=stay_result,
            raw_result=raw_result,
            attempts=attempts,
            raw_valid=False,
            fallback=True,
            invalid_reasons_seen=invalid_reasons_seen,
            selected_reason="all_stay_fallback",
        )

    def _resolved(
        self,
        *,
        vector: WarehouseFullActionVector,
        result: WarehouseGridlockStepResult,
        raw_result: WarehouseGridlockStepResult,
        attempts: int,
        raw_valid: bool,
        fallback: bool,
        invalid_reasons_seen: set[str],
        selected_reason: str,
    ) -> ResolvedWarehouseAction:
        return ResolvedWarehouseAction(
            selected_action_vector=vector,
            step_result=result,
            raw_step_result=raw_result,
            projection_trace=WarehouseProjectionTrace(
                projection_strategy_id=self.projection_strategy_id,
                projection_attempt_budget=self.projection_attempt_budget,
                attempt_count=attempts,
                raw_valid=raw_valid,
                selected_valid=result.valid,
                fallback_used=fallback,
                invalid_reasons_seen=tuple(sorted(invalid_reasons_seen)),
                selected_reason=selected_reason,
                successor_out_count_used_for_selection=False,
            ),
        )

    def _repair_order(
        self,
        raw_action_vector: WarehouseFullActionVector,
        margins: dict[str, float],
    ) -> list[str]:
        return sorted(
            raw_action_vector.commands,
            key=lambda robot_id: (
                margins.get(robot_id, 0.0),
                robot_id,
            ),
        )
