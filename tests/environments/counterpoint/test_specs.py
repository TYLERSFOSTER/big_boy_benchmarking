import pytest

from big_boy_benchmarking.environments.counterpoint import ids
from big_boy_benchmarking.environments.counterpoint.specs import make_instance_spec


def test_spec_serializes_to_json_safe_dict(tiny_spec) -> None:
    payload = tiny_spec.to_dict()

    assert payload["environment_family_id"] == ids.ENVIRONMENT_FAMILY_ID
    assert payload["allowed_adjacent_interval_classes"] == (3, 4, 5, 7, 8, 9)


@pytest.mark.parametrize(
    ("field_name", "kwargs"),
    [
        ("voice_count", {"voice_count": 1}),
        ("pitch_min", {"pitch_min": 70, "pitch_max": 60}),
        ("measure_size", {"measure_size": 0}),
        ("horizon_steps", {"horizon_steps": 0}),
        ("max_step_size", {"max_step_size": 0}),
        ("tonic_pitch_class", {"tonic_pitch_class": 12}),
        ("allowed_adjacent_interval_classes", {"allowed_adjacent_interval_classes": ()}),
    ],
)
def test_spec_validation_rejects_invalid_fields(field_name: str, kwargs: dict[str, int]) -> None:
    params = {
        "environment_instance_id": "bad",
        "voice_count": 3,
        "pitch_min": 60,
        "pitch_max": 67,
        "measure_size": 4,
        "horizon_steps": 4,
        "max_step_size": 2,
    }
    params.update(kwargs)

    with pytest.raises(ValueError, match=field_name):
        make_instance_spec(**params)
