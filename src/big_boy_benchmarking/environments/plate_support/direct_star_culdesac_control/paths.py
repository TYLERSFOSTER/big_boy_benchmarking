"""Path helpers for the PlateSupport direct-star diagnostic."""

from __future__ import annotations

from pathlib import Path

READOUT_RELATIVE_PATH = Path(
    "docs/evaluations/plate_support_5x5_default_v001/direct_star_culdesac_control"
)


def repo_readout_surface(repo_root: Path | str) -> Path:
    """Return the repo-side human-readable readout surface."""

    return Path(repo_root).expanduser().resolve() / READOUT_RELATIVE_PATH


def default_artifact_root(repo_root: Path | str, run_label: str) -> Path:
    """Return the default repo-resident artifact root for a run label."""

    return repo_readout_surface(repo_root) / "artifacts" / run_label


def evaluation_root(artifact_root: Path | str) -> Path:
    """Return the source evaluation root under an artifact root."""

    return Path(artifact_root).expanduser().resolve() / "evaluations" / (
        "plate_support_direct_star_culdesac_control_v001"
    )


def run_family_root(artifact_root: Path | str) -> Path:
    """Return the per-run event root under an artifact root."""

    return Path(artifact_root).expanduser().resolve() / "runs" / (
        "plate_support_direct_star_culdesac_control_v001"
    )


def repo_placeholder(path: Path, repo_root: Path) -> str:
    """Render a public-facing path with a repo-root placeholder."""

    resolved = path.expanduser().resolve()
    root = repo_root.expanduser().resolve()
    try:
        return "<repo-root>/" + str(resolved.relative_to(root))
    except ValueError:
        return str(resolved)


def resolve_repo_placeholder(value: object, repo_root: Path) -> Path:
    """Resolve a path that may use the public `<repo-root>` placeholder."""

    text = str(value)
    if text.startswith("<repo-root>/"):
        return (repo_root / text.removeprefix("<repo-root>/")).resolve()
    return Path(text).expanduser().resolve()

