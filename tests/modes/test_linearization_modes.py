import pytest

from big_boy_benchmarking.modes.linearization import (
    LinearizationModeContract,
    get_linearization_mode_contract,
    iter_linearization_mode_contracts,
    require_runnable_linearization_mode,
    validate_linearization_mode_contract,
)


def test_known_linearization_modes_validate() -> None:
    for contract in iter_linearization_mode_contracts():
        validate_linearization_mode_contract(contract, allow_reserved=True)


def test_unknown_linearization_mode_raises() -> None:
    with pytest.raises(KeyError):
        get_linearization_mode_contract("unknown")


def test_reserved_tensor_modes_are_not_runnable_by_default() -> None:
    cpu = get_linearization_mode_contract("tensor_enabled_cpu")
    cuda = get_linearization_mode_contract("tensor_enabled_cuda")

    assert not cpu.runnable
    assert not cuda.runnable
    with pytest.raises(ValueError, match="reserved"):
        require_runnable_linearization_mode(cpu.linearization_mode_id)
    with pytest.raises(ValueError, match="reserved"):
        require_runnable_linearization_mode(cuda.linearization_mode_id)


def test_disabled_linearization_mode_is_runnable() -> None:
    contract = require_runnable_linearization_mode("tensor_available_disabled")

    assert contract.linearization_state == "PRESENT_DISABLED"
    assert contract.expected_benchmark_label == "tensor_available_disabled"
    assert not contract.constructs_torch_batches


def test_cuda_requires_torch() -> None:
    contract = LinearizationModeContract(
        linearization_mode_id="bad_cuda",
        linearization_state="PRESENT_ENABLED",
        numeric_backend="TORCH",
        tensor_device_kind="CUDA",
        expected_benchmark_label="bad_cuda",
        requires_cuda=True,
        requires_torch=False,
    )

    with pytest.raises(ValueError, match="CUDA"):
        validate_linearization_mode_contract(contract, allow_reserved=True)
