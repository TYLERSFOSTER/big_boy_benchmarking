from big_boy_benchmarking.seeds.bundles import generate_seed_bundles


def test_seed_bundle_generation_is_deterministic() -> None:
    first = generate_seed_bundles(base_seed=123, replicate_count=3)
    second = generate_seed_bundles(base_seed=123, replicate_count=3)

    assert first == second
    assert [bundle.replicate_index for bundle in first] == [0, 1, 2]


def test_seed_dimensions_are_separate_and_serializable() -> None:
    bundle = generate_seed_bundles(base_seed=123, replicate_count=1)[0]
    payload = bundle.to_dict()

    assert payload["environment_seed"] != payload["schema_seed"]
    assert payload["seed_bundle_id"].startswith("seed-")
