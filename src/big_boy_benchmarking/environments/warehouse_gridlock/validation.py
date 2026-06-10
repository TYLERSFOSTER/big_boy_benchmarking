"""Readiness validation for Warehouse Gridlock."""

from __future__ import annotations

from dataclasses import dataclass

from big_boy_benchmarking.environments.warehouse_gridlock.actions import (
    stay_action,
    validate_action,
)
from big_boy_benchmarking.environments.warehouse_gridlock.graph import (
    graph_summary,
    validate_graph,
)
from big_boy_benchmarking.environments.warehouse_gridlock.instances import (
    WarehouseGridlockInstance,
)
from big_boy_benchmarking.environments.warehouse_gridlock.state import validate_state


@dataclass(frozen=True)
class ReadinessValidationReport:
    status: str
    graph_report: dict[str, object]
    start_state_report: dict[str, object]
    target_state_report: dict[str, object]
    action_surface_report: dict[str, object]
    summary: dict[str, object]

    def to_dict(self) -> dict[str, object]:
        return {
            "status": self.status,
            "graph_report": self.graph_report,
            "start_state_report": self.start_state_report,
            "target_state_report": self.target_state_report,
            "action_surface_report": self.action_surface_report,
            "summary": self.summary,
        }


def validate_readiness(instance: WarehouseGridlockInstance) -> ReadinessValidationReport:
    manifest = instance.manifest
    graph_report = validate_graph(instance.graph)
    start_report = validate_state(
        instance.start_state,
        graph=instance.graph,
        required_robot_ids=manifest.robot_ids,
        required_box_ids=manifest.box_ids,
    )
    target_report = validate_state(
        instance.target_state,
        graph=instance.graph,
        required_robot_ids=manifest.robot_ids,
        required_box_ids=manifest.box_ids,
    )
    action_report = validate_action(
        stay_action(manifest.robot_ids), required_robot_ids=manifest.robot_ids
    )
    status = (
        "ok"
        if all((graph_report.ok, start_report.ok, target_report.ok, action_report.ok))
        else "error"
    )
    summary = {
        "environment_family_id": manifest.environment_family_id,
        "implementation_family_id": manifest.implementation_family_id,
        "instance_id": manifest.instance_id,
        "robot_count": len(manifest.robot_ids),
        "box_count": len(manifest.box_ids),
        "robot_target_count": len(manifest.robot_target_map()),
        "box_target_count": len(manifest.box_target_map()),
        "column_count": len(manifest.columns),
        "claim_boundary": manifest.claim_boundary,
        **graph_summary(instance.graph),
    }
    return ReadinessValidationReport(
        status=status,
        graph_report=graph_report.to_dict(),
        start_state_report=start_report.to_dict(),
        target_state_report=target_report.to_dict(),
        action_surface_report=action_report.to_dict(),
        summary=summary,
    )


def readiness_table_rows(instance: WarehouseGridlockInstance) -> dict[str, list[dict[str, object]]]:
    report = validate_readiness(instance)
    summary = report.summary
    return {
        "readiness_summary": [
            {
                "environment_family_id": summary["environment_family_id"],
                "instance_id": summary["instance_id"],
                "status": report.status,
                "source_design_note": instance.manifest.source.source_design_note,
                "claim_boundary": summary["claim_boundary"],
            }
        ],
        "graph_summary": [summary],
        "state_validation_summary": [
            {"state_role": "start", **report.start_state_report},
            {"state_role": "target", **report.target_state_report},
        ],
        "target_validation_summary": [
            {
                "status": report.target_state_report["status"],
                "robot_target_count": summary["robot_target_count"],
                "box_target_count": summary["box_target_count"],
                "claim_boundary": summary["claim_boundary"],
            }
        ],
    }
