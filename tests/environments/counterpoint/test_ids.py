from big_boy_benchmarking.environments.counterpoint import ids


def test_canonical_ids_are_locked_and_unique() -> None:
    assert ids.CANONICAL_IDS["environment_family_id"] == "counterpoint_symbolic_v001"
    assert ids.CANONICAL_IDS["reward_bundle_id"] == "counterpoint_reward_local_v001"
    assert len(set(ids.CANONICAL_IDS.values())) == len(ids.CANONICAL_IDS)
