"""Schema-arm declarations for the second serious comparison."""

from __future__ import annotations

from dataclasses import dataclass

from big_boy_benchmarking.environments.counterpoint import ids
from big_boy_benchmarking.environments.counterpoint.second_serious_comparison.config import (
    SCHEMA0_CLASS_ID,
    SCHEMA1_CLASS_ID,
)


@dataclass(frozen=True)
class SchemaArm:
    schema_class_id: str
    display_name: str
    schema_id: str
    requires_candidate: bool
    claim_role: str


SCHEMA0_ARM = SchemaArm(
    schema_class_id=SCHEMA0_CLASS_ID,
    display_name="Schema 0: no contraction",
    schema_id=ids.EMPTY_SCHEMA_ID,
    requires_candidate=False,
    claim_role="matched total-space no-contraction condition",
)

SCHEMA1_ARM = SchemaArm(
    schema_class_id=SCHEMA1_CLASS_ID,
    display_name="Schema 1: one-drop noisy-rate quotient",
    schema_id=ids.NOISY_RATE_CONTRACTION_SCHEMA_ID,
    requires_candidate=True,
    claim_role="selected one-drop noisy-rate quotient condition",
)
