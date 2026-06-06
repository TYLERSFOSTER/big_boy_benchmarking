"""Path helpers for PlateSupport environment-readiness artifacts."""

from __future__ import annotations

from pathlib import Path

from big_boy_benchmarking.environments.plate_support.ids import (
    DEFAULT_INSTANCE_ID,
)

REPO_ROOT = Path(__file__).resolve().parents[4]
DEFAULT_ENVIRONMENT_DOC = REPO_ROOT / "docs" / "environments" / f"{DEFAULT_INSTANCE_ID}.md"
DEFAULT_READINESS_ROOT = (
    REPO_ROOT / "docs" / "environments" / DEFAULT_INSTANCE_ID / "readiness"
)


def default_environment_doc_path() -> Path:
    return DEFAULT_ENVIRONMENT_DOC


def default_readiness_artifact_root(run_label: str = "dev_001") -> Path:
    return DEFAULT_READINESS_ROOT / run_label


def normalize_path(path: Path | str) -> Path:
    return Path(path).expanduser().resolve()


def validate_no_evaluation_path(path: Path | str) -> Path:
    target = normalize_path(path)
    if "docs/evaluations" in target.as_posix():
        raise ValueError(
            "PlateSupport environment readiness artifacts must not be written under "
            f"docs/evaluations: {target}"
        )
    return target
