"""Helpers for recording state_collapser linearization reports in BBB artifacts."""

from __future__ import annotations

from collections.abc import Mapping
from dataclasses import dataclass
from typing import Any

from state_collapser.training import (
    EncodingRegistry,
    LinearizationConfig,
    LinearizationReport,
    LinearizationState,
    NumericBackend,
    TensorDeviceKind,
    build_linearization_report,
)

from big_boy_benchmarking.metrics.timing import TimingRecorder
from big_boy_benchmarking.modes.linearization import (
    LinearizationModeContract,
    get_linearization_mode_contract,
    require_runnable_linearization_mode,
)

REPORT_SOURCE = "state_collapser.training.build_linearization_report"


@dataclass(frozen=True)
class LinearizationArtifactPayload:
    contract: LinearizationModeContract
    config: LinearizationConfig
    report: LinearizationReport

    @property
    def config_dict(self) -> dict[str, Any]:
        return self.config.to_dict()

    @property
    def report_dict(self) -> dict[str, Any]:
        return self.report.to_dict()


def _max_tower_depth(tower: Any | None) -> int | None:
    if tower is None:
        return None
    state_layers = getattr(tower, "state_layers", None)
    if state_layers is None:
        return None
    return len(state_layers)


def _build_config(
    contract: LinearizationModeContract,
    *,
    registry: EncodingRegistry | None,
    tower: Any | None,
    max_action_count: int | None,
) -> LinearizationConfig:
    return LinearizationConfig(
        linearization_state=LinearizationState(contract.linearization_state),
        numeric_backend=NumericBackend(contract.numeric_backend),
        device_kind=TensorDeviceKind(contract.tensor_device_kind),
        max_tower_depth=_max_tower_depth(tower),
        max_action_count=max_action_count,
        encoder_registry_id=None if registry is None else registry.registry_id,
    )


def build_linearization_artifact_payload(
    *,
    linearization_mode_id: str,
    recorder: TimingRecorder,
    tower: Any | None = None,
    max_action_count: int | None = None,
    metadata: Mapping[str, object] | None = None,
    allow_reserved: bool = False,
) -> LinearizationArtifactPayload:
    """Build upstream config/report payloads for one BBB run."""

    contract = (
        get_linearization_mode_contract(linearization_mode_id)
        if allow_reserved
        else require_runnable_linearization_mode(linearization_mode_id)
    )

    registry = None
    if tower is not None and contract.linearization_mode_id == "tensor_available_disabled":
        with recorder.segment("encoding_registry_build"):
            registry = EncodingRegistry.from_tower(tower)

    config = _build_config(
        contract,
        registry=registry,
        tower=tower,
        max_action_count=max_action_count,
    )
    with recorder.segment("linearization_report_build"):
        report = build_linearization_report(
            config=config,
            registry=registry,
            tower=tower,
            metadata=metadata,
        )
    if report.benchmark_label != contract.expected_benchmark_label:
        raise ValueError(
            "linearization report label mismatch: "
            f"{report.benchmark_label} != {contract.expected_benchmark_label}"
        )
    return LinearizationArtifactPayload(
        contract=contract,
        config=config,
        report=report,
    )
