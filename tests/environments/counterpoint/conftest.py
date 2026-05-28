import pytest

from big_boy_benchmarking.environments.counterpoint.specs import (
    CounterpointInstanceSpec,
    make_instance_spec,
)


@pytest.fixture
def tiny_spec() -> CounterpointInstanceSpec:
    return make_instance_spec(
        environment_instance_id="counterpoint_symbolic_n3_tiny_test",
        voice_count=3,
        pitch_min=60,
        pitch_max=67,
        measure_size=4,
        horizon_steps=4,
        max_step_size=2,
        max_outer_span=8,
    )
