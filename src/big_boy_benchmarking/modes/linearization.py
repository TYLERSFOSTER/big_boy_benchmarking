"""Linearization mode contracts for state_collapser tensorization conditions."""

from __future__ import annotations

from dataclasses import asdict, dataclass
from typing import Any


@dataclass(frozen=True)
class LinearizationModeContract:
    linearization_mode_id: str
    linearization_state: str
    numeric_backend: str
    tensor_device_kind: str
    expected_benchmark_label: str
    runnable: bool = True
    reserved_reason: str | None = None
    requires_numpy: bool = False
    requires_torch: bool = False
    requires_cuda: bool = False
    constructs_linearized_records: bool = False
    constructs_torch_batches: bool = False
    report_required: bool = True
    conversion_timing_required: bool = False
    debug_record_export_allowed: bool = False
    artifact_claim_level: str = "smoke"

    def to_dict(self) -> dict[str, Any]:
        return asdict(self)


_LINEARIZATION_MODES: dict[str, LinearizationModeContract] = {
    "none_control_flow": LinearizationModeContract(
        linearization_mode_id="none_control_flow",
        linearization_state="ABSENT",
        numeric_backend="NONE",
        tensor_device_kind="NONE",
        expected_benchmark_label="none_control_flow",
        artifact_claim_level="object_native_control_flow_baseline",
    ),
    "tensor_available_disabled": LinearizationModeContract(
        linearization_mode_id="tensor_available_disabled",
        linearization_state="PRESENT_DISABLED",
        numeric_backend="NUMPY",
        tensor_device_kind="NONE",
        expected_benchmark_label="tensor_available_disabled",
        requires_numpy=True,
        conversion_timing_required=True,
        artifact_claim_level="tensor_capable_disabled_smoke",
    ),
    "tensor_enabled_cpu": LinearizationModeContract(
        linearization_mode_id="tensor_enabled_cpu",
        linearization_state="PRESENT_ENABLED",
        numeric_backend="TORCH",
        tensor_device_kind="CPU",
        expected_benchmark_label="tensor_enabled_cpu",
        runnable=False,
        reserved_reason=(
            "BBB does not yet have a real tensor-consuming CPU learner/model path"
        ),
        requires_torch=True,
        constructs_linearized_records=True,
        constructs_torch_batches=True,
        conversion_timing_required=True,
        artifact_claim_level="reserved_cpu_tensor_smoke",
    ),
    "tensor_enabled_cuda": LinearizationModeContract(
        linearization_mode_id="tensor_enabled_cuda",
        linearization_state="PRESENT_ENABLED",
        numeric_backend="TORCH",
        tensor_device_kind="CUDA",
        expected_benchmark_label="tensor_enabled_cuda",
        runnable=False,
        reserved_reason="BBB has not validated a local CUDA tensor path",
        requires_torch=True,
        requires_cuda=True,
        constructs_linearized_records=True,
        constructs_torch_batches=True,
        conversion_timing_required=True,
        artifact_claim_level="reserved_cuda_tensor_smoke",
    ),
}


def validate_linearization_mode_contract(
    contract: LinearizationModeContract, *, allow_reserved: bool = False
) -> None:
    errors: list[str] = []

    if not contract.runnable and not allow_reserved:
        errors.append(f"linearization mode is reserved: {contract.linearization_mode_id}")

    if not contract.runnable and not contract.reserved_reason:
        errors.append("reserved linearization mode must include reserved_reason")

    if contract.linearization_mode_id != contract.expected_benchmark_label:
        errors.append("linearization_mode_id must match expected_benchmark_label")

    if contract.linearization_state == "ABSENT":
        if contract.numeric_backend != "NONE":
            errors.append("ABSENT linearization requires NumericBackend.NONE")
        if contract.tensor_device_kind != "NONE":
            errors.append("ABSENT linearization requires TensorDeviceKind.NONE")

    if contract.linearization_state == "PRESENT_ENABLED" and contract.numeric_backend == "NONE":
        errors.append("PRESENT_ENABLED linearization requires a numeric backend")

    if contract.tensor_device_kind == "CUDA" and contract.numeric_backend != "TORCH":
        errors.append("CUDA linearization requires NumericBackend.TORCH")

    if contract.requires_cuda and not contract.requires_torch:
        errors.append("CUDA linearization must require Torch")

    if contract.constructs_torch_batches and not contract.requires_torch:
        errors.append("Torch batch construction must require Torch")

    if errors:
        raise ValueError("; ".join(errors))


def iter_linearization_mode_contracts() -> tuple[LinearizationModeContract, ...]:
    return tuple(_LINEARIZATION_MODES.values())


def get_linearization_mode_contract(linearization_mode_id: str) -> LinearizationModeContract:
    try:
        return _LINEARIZATION_MODES[linearization_mode_id]
    except KeyError as exc:
        raise KeyError(f"unknown linearization mode: {linearization_mode_id}") from exc


def require_runnable_linearization_mode(
    linearization_mode_id: str,
) -> LinearizationModeContract:
    contract = get_linearization_mode_contract(linearization_mode_id)
    validate_linearization_mode_contract(contract)
    return contract


for _contract in _LINEARIZATION_MODES.values():
    validate_linearization_mode_contract(_contract, allow_reserved=True)
