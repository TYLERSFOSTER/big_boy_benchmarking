from big_boy_benchmarking.environments.plate_support import ids


def test_plate_support_ids_match_blueprint_values() -> None:
    assert ids.ENVIRONMENT_FAMILY_ID == "plate_support"
    assert ids.UPSTREAM_SMOKE_ID == "plate_support_env"
    assert ids.UPSTREAM_MODULE == "state_collapser.examples.plate_support_env"
    assert ids.DEFAULT_INSTANCE_ID == "plate_support_5x5_default_v001"
    assert ids.SMOKE_FIXTURE_ID == "plate_support_5x5_default_smoke_v001"
    assert ids.STRUCTURAL_FIXTURE_ID == "plate_support_5x5_default_v001"
    assert ids.READINESS_RUN_FAMILY_ID == "plate_support_environment_readiness_v001"
    assert ids.DEFAULT_SCHEMA_ID == "upstream_default_plate_support_schema_v001"
    assert ids.NO_CONTRACTION_SCHEMA_ID == "no_contraction_schema_v001"
    assert ids.REWARD_BUNDLE_ID == "plate_support_goal_self_loop_penalty_v001"
    assert ids.LEGALITY_CONTRACT_ID == "plate_support_validity_predicates_v001"
    assert ids.ACTION_LABEL_CONTRACT_ID == "plate_support_action_labels_v001"


def test_plate_support_ids_are_nonempty_and_role_distinct() -> None:
    values = [
        ids.ENVIRONMENT_FAMILY_ID,
        ids.UPSTREAM_SMOKE_ID,
        ids.UPSTREAM_MODULE,
        ids.DEFAULT_INSTANCE_ID,
        ids.SMOKE_FIXTURE_ID,
        ids.STRUCTURAL_FIXTURE_ID,
        ids.READINESS_RUN_FAMILY_ID,
        ids.DEFAULT_SCHEMA_ID,
        ids.NO_CONTRACTION_SCHEMA_ID,
        ids.REWARD_BUNDLE_ID,
        ids.LEGALITY_CONTRACT_ID,
        ids.ACTION_LABEL_CONTRACT_ID,
    ]
    assert all(isinstance(value, str) and value for value in values)
    assert ids.DEFAULT_SCHEMA_ID != ids.NO_CONTRACTION_SCHEMA_ID
    assert ids.SMOKE_FIXTURE_ID != ids.STRUCTURAL_FIXTURE_ID
