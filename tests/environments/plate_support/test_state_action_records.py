import json

from big_boy_benchmarking.environments.plate_support.actions import (
    ACTION_RECORDS,
    action_label,
)
from big_boy_benchmarking.environments.plate_support.states import (
    state_id,
    state_to_record,
)
from big_boy_benchmarking.environments.plate_support.upstream import (
    import_plate_support_surface,
)


def test_plate_support_action_contract_is_complete_and_stable() -> None:
    assert len(ACTION_RECORDS) == 12
    assert [record.action_index for record in ACTION_RECORDS] == list(range(12))
    assert len({record.action_label for record in ACTION_RECORDS}) == 12
    assert action_label(0) == "plate_x_plus"
    assert action_label(11) == "arm3_retract"
    assert all(record.action_category for record in ACTION_RECORDS)
    assert all(record.upstream_identity for record in ACTION_RECORDS)


def test_plate_support_state_record_is_json_safe_and_contract_rich() -> None:
    surface = import_plate_support_surface()
    record = state_to_record(surface.START_STATE, role="start", surface=surface)

    assert record.state_id == state_id(surface.START_STATE)
    assert record.role == "start"
    assert record.valid_state is True
    assert json.loads(record.support_pattern) == [1, 1, 1]
    assert json.loads(record.reachability_pattern) == [True, True, True]
    assert isinstance(json.loads(record.socket_positions), list)
