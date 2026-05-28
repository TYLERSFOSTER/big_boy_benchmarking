from big_boy_benchmarking.upstream.smoke_envs import (
    import_smoke_environment,
    iter_smoke_environment_specs,
)


def test_smoke_registry_contains_required_ids() -> None:
    ids = {spec.smoke_id for spec in iter_smoke_environment_specs()}

    assert {"plate_support_env", "rl_counterpoint_v3"} <= ids


def test_required_smoke_envs_import() -> None:
    plate = import_smoke_environment("plate_support_env")
    counterpoint = import_smoke_environment("rl_counterpoint_v3")

    assert plate.env_class.__name__ == "PlateSupportEnv"
    assert counterpoint.env_class.__name__ == "RlCounterpointEnv"
