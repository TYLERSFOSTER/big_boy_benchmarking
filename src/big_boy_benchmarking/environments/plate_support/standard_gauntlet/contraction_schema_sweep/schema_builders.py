"""Schema construction status for Stage 2 arms."""

from __future__ import annotations

from dataclasses import dataclass

from big_boy_benchmarking.environments.plate_support.standard_gauntlet.contraction_schema_sweep.schema_families import (
    SchemaArm,
)


@dataclass(frozen=True)
class SchemaConstructionResult:
    """Structured construction result for one schema arm."""

    schema_id: str
    schema_family_id: str
    schema_seed: int
    construction_status: str
    schema_mode: str
    builder_surface: str
    blocking_reason: str

    def to_dict(self) -> dict[str, object]:
        return {
            "schema_id": self.schema_id,
            "schema_family_id": self.schema_family_id,
            "schema_seed": self.schema_seed,
            "construction_status": self.construction_status,
            "schema_mode": self.schema_mode,
            "builder_surface": self.builder_surface,
            "blocking_reason": self.blocking_reason,
        }


def construct_schema_arm(arm: SchemaArm) -> SchemaConstructionResult:
    """Construct or explicitly block a schema arm."""

    if arm.construction_supported:
        return SchemaConstructionResult(
            schema_id=arm.schema_id,
            schema_family_id=arm.schema_family_id,
            schema_seed=arm.schema_seed,
            construction_status="constructed",
            schema_mode=arm.schema_mode,
            builder_surface="state_collapser.examples.tower_depth_probe.schema_mode",
            blocking_reason="",
        )
    return SchemaConstructionResult(
        schema_id=arm.schema_id,
        schema_family_id=arm.schema_family_id,
        schema_seed=arm.schema_seed,
        construction_status="not_supported",
        schema_mode=arm.schema_mode,
        builder_surface="not_available",
        blocking_reason=arm.unsupported_reason,
    )
