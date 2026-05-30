"""Arm contracts for the first serious counterpoint learning evaluation."""

from __future__ import annotations

from dataclasses import asdict, dataclass
from typing import Any

from big_boy_benchmarking.environments.counterpoint import ids


@dataclass(frozen=True)
class SeriousLearningArm:
    arm_id: str
    mode_id: str
    schema_id: str | None
    schema_family_id: str | None
    controller_regime: str
    training_surface: str
    learner_id: str
    purpose: str
    requires_tower: bool
    requires_schema_seed: bool
    online_eligible: bool

    def to_dict(self) -> dict[str, Any]:
        return asdict(self)


DIRECT_MASKED_RANDOM_ARM_ID = "direct_masked_random"
DIRECT_TABULAR_Q_ARM_ID = "direct_tabular_q"
TOWER_EMPTY_ARM_ID = "tower_empty_exploit_explore_tabular_q"
TOWER_RANDOM_BALANCED_ARM_ID = "tower_random_balanced_exploit_explore_tabular_q"
TOWER_RANDOM_UNBALANCED_ARM_ID = "tower_random_unbalanced_exploit_explore_tabular_q"
TOWER_MOTION_ARM_ID = "tower_motion_exploit_explore_tabular_q"
TOWER_BAD_ARM_ID = "tower_bad_exploit_explore_tabular_q"

REQUIRED_SERIOUS_LEARNING_ARM_IDS = (
    DIRECT_MASKED_RANDOM_ARM_ID,
    DIRECT_TABULAR_Q_ARM_ID,
    TOWER_EMPTY_ARM_ID,
    TOWER_RANDOM_BALANCED_ARM_ID,
    TOWER_RANDOM_UNBALANCED_ARM_ID,
    TOWER_MOTION_ARM_ID,
    TOWER_BAD_ARM_ID,
)

_ARMS: dict[str, SeriousLearningArm] = {
    DIRECT_MASKED_RANDOM_ARM_ID: SeriousLearningArm(
        arm_id=DIRECT_MASKED_RANDOM_ARM_ID,
        mode_id="direct_env_masked_random",
        schema_id=None,
        schema_family_id=None,
        controller_regime="none",
        training_surface="environment",
        learner_id="masked_random",
        purpose="non-learning direct environment floor",
        requires_tower=False,
        requires_schema_seed=False,
        online_eligible=True,
    ),
    DIRECT_TABULAR_Q_ARM_ID: SeriousLearningArm(
        arm_id=DIRECT_TABULAR_Q_ARM_ID,
        mode_id="direct_env_tabular",
        schema_id=None,
        schema_family_id=None,
        controller_regime="none",
        training_surface="environment",
        learner_id="tabular_q",
        purpose="direct environment upstream TabularQLearner baseline",
        requires_tower=False,
        requires_schema_seed=False,
        online_eligible=True,
    ),
    TOWER_EMPTY_ARM_ID: SeriousLearningArm(
        arm_id=TOWER_EMPTY_ARM_ID,
        mode_id="tower_exploit_explore",
        schema_id=ids.EMPTY_SCHEMA_ID,
        schema_family_id=ids.EMPTY_SCHEMA_ID,
        controller_regime="exploit_explore",
        training_surface="tower",
        learner_id="tabular_q",
        purpose="active-tier tower shell with no nontrivial contraction",
        requires_tower=True,
        requires_schema_seed=False,
        online_eligible=True,
    ),
    TOWER_RANDOM_BALANCED_ARM_ID: SeriousLearningArm(
        arm_id=TOWER_RANDOM_BALANCED_ARM_ID,
        mode_id="tower_exploit_explore",
        schema_id=ids.RANDOM_BALANCED_SCHEMA_FAMILY_ID,
        schema_family_id=ids.RANDOM_BALANCED_SCHEMA_FAMILY_ID,
        controller_regime="exploit_explore",
        training_surface="tower",
        learner_id="tabular_q",
        purpose="seeded balanced random contraction tower-control comparison",
        requires_tower=True,
        requires_schema_seed=True,
        online_eligible=True,
    ),
    TOWER_RANDOM_UNBALANCED_ARM_ID: SeriousLearningArm(
        arm_id=TOWER_RANDOM_UNBALANCED_ARM_ID,
        mode_id="tower_exploit_explore",
        schema_id=ids.RANDOM_UNBALANCED_SCHEMA_FAMILY_ID,
        schema_family_id=ids.RANDOM_UNBALANCED_SCHEMA_FAMILY_ID,
        controller_regime="exploit_explore",
        training_surface="tower",
        learner_id="tabular_q",
        purpose="seeded unbalanced random contraction pathology/control",
        requires_tower=True,
        requires_schema_seed=True,
        online_eligible=True,
    ),
    TOWER_MOTION_ARM_ID: SeriousLearningArm(
        arm_id=TOWER_MOTION_ARM_ID,
        mode_id="tower_exploit_explore",
        schema_id=ids.STRUCTURED_MOTION_SCHEMA_ID,
        schema_family_id=ids.STRUCTURED_MOTION_SCHEMA_ID,
        controller_regime="exploit_explore",
        training_surface="tower",
        learner_id="tabular_q",
        purpose="structured motion contraction tower-control arm",
        requires_tower=True,
        requires_schema_seed=False,
        online_eligible=True,
    ),
    TOWER_BAD_ARM_ID: SeriousLearningArm(
        arm_id=TOWER_BAD_ARM_ID,
        mode_id="tower_exploit_explore",
        schema_id=ids.BAD_SCHEMA_ID,
        schema_family_id=ids.BAD_SCHEMA_ID,
        controller_regime="exploit_explore",
        training_surface="tower",
        learner_id="tabular_q",
        purpose="bad/adversarial overcompression tower-control arm",
        requires_tower=True,
        requires_schema_seed=False,
        online_eligible=True,
    ),
}


def iter_serious_learning_arms() -> tuple[SeriousLearningArm, ...]:
    return tuple(_ARMS[arm_id] for arm_id in REQUIRED_SERIOUS_LEARNING_ARM_IDS)


def get_serious_learning_arm(arm_id: str) -> SeriousLearningArm:
    try:
        return _ARMS[arm_id]
    except KeyError as exc:
        raise KeyError(f"unknown serious learning arm: {arm_id}") from exc


def validate_serious_learning_arm_set(arm_ids: tuple[str, ...]) -> None:
    missing = tuple(arm_id for arm_id in REQUIRED_SERIOUS_LEARNING_ARM_IDS if arm_id not in arm_ids)
    unknown = tuple(arm_id for arm_id in arm_ids if arm_id not in _ARMS)
    if missing:
        raise ValueError(f"missing required serious learning arms: {missing}")
    if unknown:
        raise ValueError(f"unknown serious learning arms: {unknown}")
