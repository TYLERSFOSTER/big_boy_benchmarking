"""Dependency-state capture for state_collapser."""

from __future__ import annotations

import importlib
import importlib.metadata
import inspect
import subprocess
from dataclasses import asdict, dataclass
from pathlib import Path
from typing import Any

STATE_COLLAPSER_DEPENDENCY_SPEC = (
    "state-collapser[rl] @ git+https://github.com/TYLERSFOSTER/state_collapser.git@v0.7.0"
)

REQUIRED_LINEARIZATION_SYMBOLS = (
    "EncodingRegistry",
    "LinearizationConfig",
    "LinearizationReport",
    "LinearizationState",
    "NumericBackend",
    "TensorDeviceKind",
    "build_linearization_report",
)


@dataclass(frozen=True)
class StateCollapserDependencyState:
    import_version: str
    source_path: str | None
    git_commit: str | None
    git_branch: str | None
    git_dirty: bool | None
    git_ahead_behind: str | None
    dependency_spec: str | None
    inspection_status: str
    linearization_import_status: str = "not_checked"
    linearization_symbols: tuple[str, ...] = ()
    torch_import_status: str = "not_checked"
    cuda_available: bool | None = None

    def to_dict(self) -> dict[str, Any]:
        return asdict(self)


def _run_git(path: Path, *args: str) -> str | None:
    result = subprocess.run(
        ["git", "-C", str(path), *args],
        check=False,
        capture_output=True,
        text=True,
    )
    if result.returncode != 0:
        return None
    return result.stdout.strip()


def _git_state(path: Path) -> tuple[str | None, str | None, bool | None, str | None]:
    commit = _run_git(path, "rev-parse", "HEAD")
    branch = _run_git(path, "branch", "--show-current")
    status = _run_git(path, "status", "--short", "--branch")
    dirty = None
    ahead_behind = None
    if status is not None:
        lines = status.splitlines()
        dirty = any(line and not line.startswith("##") for line in lines)
        ahead_behind = lines[0] if lines else None
    return commit, branch, dirty, ahead_behind


def _inspect_linearization_imports() -> tuple[str, tuple[str, ...]]:
    try:
        training_module = importlib.import_module("state_collapser.training")
    except Exception as exc:  # pragma: no cover - defensive import boundary
        return f"import_failed:{type(exc).__name__}:{exc}", ()

    present = tuple(
        symbol for symbol in REQUIRED_LINEARIZATION_SYMBOLS if hasattr(training_module, symbol)
    )
    missing = tuple(
        symbol for symbol in REQUIRED_LINEARIZATION_SYMBOLS if symbol not in present
    )
    if missing:
        return f"missing:{','.join(missing)}", present
    return "ok", present


def _inspect_torch_import_state() -> tuple[str, bool | None]:
    try:
        importlib.import_module("state_collapser.training.torch")
    except Exception as exc:  # pragma: no cover - defensive import boundary
        return f"state_collapser_torch_import_failed:{type(exc).__name__}:{exc}", None

    try:
        torch_module = importlib.import_module("torch")
    except ModuleNotFoundError:
        return "missing", None
    except Exception as exc:  # pragma: no cover - defensive import boundary
        return f"torch_import_failed:{type(exc).__name__}:{exc}", None
    return "ok", bool(torch_module.cuda.is_available())


def collect_state_collapser_dependency_state(
    *,
    local_path: Path | str | None = None,
    dependency_spec: str | None = None,
) -> StateCollapserDependencyState:
    try:
        import state_collapser
    except Exception as exc:  # pragma: no cover - defensive import boundary
        return StateCollapserDependencyState(
            import_version="",
            source_path=None,
            git_commit=None,
            git_branch=None,
            git_dirty=None,
            git_ahead_behind=None,
            dependency_spec=dependency_spec,
            inspection_status=f"import_failed:{type(exc).__name__}:{exc}",
            linearization_import_status="not_checked",
            linearization_symbols=(),
            torch_import_status="not_checked",
            cuda_available=None,
        )

    import_version = getattr(
        state_collapser,
        "__version__",
        importlib.metadata.version("state-collapser"),
    )
    source_file = inspect.getfile(state_collapser)
    source_path = str(Path(source_file).resolve().parent)

    git_root = Path(local_path).resolve() if local_path is not None else None
    commit = branch = ahead_behind = None
    dirty: bool | None = None
    inspection_status = "ok"

    if git_root is not None:
        commit, branch, dirty, ahead_behind = _git_state(git_root)
        if commit is None:
            inspection_status = "git_unavailable"

    linearization_status, linearization_symbols = _inspect_linearization_imports()
    torch_import_status, cuda_available = _inspect_torch_import_state()

    return StateCollapserDependencyState(
        import_version=str(import_version),
        source_path=source_path,
        git_commit=commit,
        git_branch=branch,
        git_dirty=dirty,
        git_ahead_behind=ahead_behind,
        dependency_spec=dependency_spec,
        inspection_status=inspection_status,
        linearization_import_status=linearization_status,
        linearization_symbols=linearization_symbols,
        torch_import_status=torch_import_status,
        cuda_available=cuda_available,
    )
