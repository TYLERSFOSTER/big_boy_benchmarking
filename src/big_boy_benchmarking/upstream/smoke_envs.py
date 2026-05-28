"""Smoke environment adapters for upstream state_collapser examples."""

from __future__ import annotations

from dataclasses import dataclass
from importlib import import_module
from typing import Any


class SmokeEnvironmentImportError(RuntimeError):
    """Raised when an expected upstream smoke surface is unavailable."""


@dataclass(frozen=True)
class SmokeEnvironmentSpec:
    smoke_id: str
    module_name: str
    env_class_name: str
    runtime_class_name: str
    action_count_name: str = "ACTION_COUNT"


SMOKE_ENVIRONMENT_SPECS: dict[str, SmokeEnvironmentSpec] = {
    "plate_support_env": SmokeEnvironmentSpec(
        smoke_id="plate_support_env",
        module_name="state_collapser.examples.plate_support_env",
        env_class_name="PlateSupportEnv",
        runtime_class_name="PlateSupportEnvRuntime",
    ),
    "rl_counterpoint_v3": SmokeEnvironmentSpec(
        smoke_id="rl_counterpoint_v3",
        module_name="state_collapser.examples.rl_counterpoint_v3",
        env_class_name="RlCounterpointEnv",
        runtime_class_name="RlCounterpointEnvRuntime",
    ),
}


@dataclass(frozen=True)
class ImportedSmokeEnvironment:
    spec: SmokeEnvironmentSpec
    module: Any
    env_class: type[Any]
    runtime_class: type[Any]
    action_count: int

    def create_env(self) -> Any:
        return self.env_class()

    def create_runtime(self) -> Any:
        return self.runtime_class(self.create_env())


def iter_smoke_environment_specs() -> tuple[SmokeEnvironmentSpec, ...]:
    return tuple(SMOKE_ENVIRONMENT_SPECS.values())


def get_smoke_environment_spec(smoke_id: str) -> SmokeEnvironmentSpec:
    try:
        return SMOKE_ENVIRONMENT_SPECS[smoke_id]
    except KeyError as exc:
        raise KeyError(f"unknown smoke environment: {smoke_id}") from exc


def import_smoke_environment(smoke_id: str) -> ImportedSmokeEnvironment:
    spec = get_smoke_environment_spec(smoke_id)
    try:
        module = import_module(spec.module_name)
        env_class = getattr(module, spec.env_class_name)
        runtime_class = getattr(module, spec.runtime_class_name)
        action_count = int(getattr(module, spec.action_count_name))
    except Exception as exc:
        message = (
            f"missing upstream smoke surface for {smoke_id}: "
            f"{spec.module_name}.{spec.env_class_name}/{spec.runtime_class_name}"
        )
        raise SmokeEnvironmentImportError(message) from exc
    return ImportedSmokeEnvironment(
        spec=spec,
        module=module,
        env_class=env_class,
        runtime_class=runtime_class,
        action_count=action_count,
    )
