import json

from big_boy_benchmarking.environments.plate_support.ids import (
    DEFAULT_SCHEMA_ID,
    NO_CONTRACTION_SCHEMA_ID,
)
from big_boy_benchmarking.environments.plate_support.tower_probe import (
    run_plate_support_tower_probe,
)


def test_plate_support_tower_probe_records_default_and_flat_schema() -> None:
    rows = run_plate_support_tower_probe(steps=5, seed=0, sample_size=10)
    by_schema = {row.schema_id: row for row in rows}

    assert set(by_schema) == {DEFAULT_SCHEMA_ID, NO_CONTRACTION_SCHEMA_ID}
    assert by_schema[DEFAULT_SCHEMA_ID].max_depth >= 2
    assert by_schema[DEFAULT_SCHEMA_ID].scheduled_assignment_count > 0
    assert by_schema[NO_CONTRACTION_SCHEMA_ID].max_depth == 1
    assert by_schema[NO_CONTRACTION_SCHEMA_ID].scheduled_assignment_count == 0
    assert isinstance(json.loads(by_schema[DEFAULT_SCHEMA_ID].depth_curve), list)
