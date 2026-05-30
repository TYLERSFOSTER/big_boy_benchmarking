import pytest

from big_boy_benchmarking.environments.counterpoint import ids
from big_boy_benchmarking.environments.counterpoint.serious_learning.arms import (
    REQUIRED_SERIOUS_LEARNING_ARM_IDS,
    get_serious_learning_arm,
    iter_serious_learning_arms,
)


def test_serious_learning_arm_contract_contains_required_arms() -> None:
    arms = iter_serious_learning_arms()

    assert tuple(arm.arm_id for arm in arms) == REQUIRED_SERIOUS_LEARNING_ARM_IDS
    assert len(arms) == 7


def test_direct_and_tower_arms_are_distinguishable() -> None:
    arms = {arm.arm_id: arm for arm in iter_serious_learning_arms()}

    assert arms["direct_masked_random"].requires_tower is False
    assert arms["direct_tabular_q"].requires_tower is False
    assert arms["direct_tabular_q"].mode_id == "direct_env_tabular"
    assert all(
        arm.mode_id == "tower_exploit_explore"
        for arm in arms.values()
        if arm.requires_tower
    )
    assert all(
        arm.controller_regime == "exploit_explore"
        for arm in arms.values()
        if arm.requires_tower
    )


def test_random_schema_arms_require_schema_seeds() -> None:
    arms = {arm.arm_id: arm for arm in iter_serious_learning_arms()}

    assert arms["tower_random_balanced_exploit_explore_tabular_q"].requires_schema_seed
    assert arms["tower_random_unbalanced_exploit_explore_tabular_q"].requires_schema_seed
    assert not arms["tower_motion_exploit_explore_tabular_q"].requires_schema_seed
    assert not arms["tower_empty_exploit_explore_tabular_q"].requires_schema_seed


def test_projection_audit_is_not_a_serious_learning_arm() -> None:
    schema_ids = {arm.schema_id for arm in iter_serious_learning_arms()}

    assert ids.PROJECTION_AUDIT_SCHEMA_ID not in schema_ids


def test_unknown_arm_fails_clearly() -> None:
    with pytest.raises(KeyError, match="unknown serious learning arm"):
        get_serious_learning_arm("projection_audit")
