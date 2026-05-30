"""Human-facing docs writer for serious counterpoint learning evaluations."""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any

from big_boy_benchmarking.environments.counterpoint.serious_learning.evaluation_paths import (
    build_serious_learning_evaluation_paths,
)


def write_serious_learning_docs(
    *,
    artifact_root: Path | str,
    docs_root: Path | str | None = None,
    command_lines: tuple[str, ...] = (),
) -> dict[str, str]:
    artifact_root = Path(artifact_root)
    paths = build_serious_learning_evaluation_paths(artifact_root)
    docs_root = paths.docs_dir if docs_root is None else Path(docs_root)
    docs_root.mkdir(parents=True, exist_ok=True)
    (docs_root / "results").mkdir(parents=True, exist_ok=True)
    aggregate = _read_json(paths.evaluation_aggregate_summary)
    calibration = _read_json(paths.calibration_summary)
    files = {
        "README.md": _readme(aggregate, calibration),
        "method.md": _method(),
        "runbook.md": _runbook(artifact_root, command_lines),
        "artifact_index.md": _artifact_index(paths, artifact_root),
        "results/summary.md": _results_summary(aggregate, calibration, artifact_root),
    }
    written: dict[str, str] = {}
    for relative_path, content in files.items():
        target = docs_root / relative_path
        target.parent.mkdir(parents=True, exist_ok=True)
        target.write_text(content, encoding="utf-8")
        written[relative_path] = str(target)
    return written


def _readme(
    aggregate: dict[str, Any],
    calibration: dict[str, Any],
) -> str:
    status = aggregate.get("status") or calibration.get("status") or "not_run"
    return "\n".join(
        [
            "# Counterpoint First Serious Learning Evaluation",
            "",
            "Artifact root: supplied at run time as `<artifact-root>`.",
            f"Status: `{status}`",
            "",
            "Claim boundary: this document summarizes one counterpoint symbolic v001 "
            "learning/control evaluation artifact set. It does not make a tensor-enabled, "
            "GPU, musical-quality, or general method claim.",
            "",
            "Primary fixture: `counterpoint_symbolic_n3_small_v001`.",
            "",
        ]
    )


def _method() -> str:
    return "\n".join(
        [
            "# Method",
            "",
            "The first serious evaluation compares direct environment arms against "
            "active-tier exploit/explore tower-control arms under shared seed, budget, "
            "mask, artifact, timing, and linearization discipline.",
            "",
            "Default linearization condition: `tensor_available_disabled`.",
            "",
            "Direct arms:",
            "",
            "- `direct_masked_random`",
            "- `direct_tabular_q`",
            "",
            "Tower-control arms:",
            "",
            "- `tower_empty_exploit_explore_tabular_q`",
            "- `tower_random_balanced_exploit_explore_tabular_q`",
            "- `tower_random_unbalanced_exploit_explore_tabular_q`",
            "- `tower_motion_exploit_explore_tabular_q`",
            "- `tower_bad_exploit_explore_tabular_q`",
            "",
            "Artifacts are read from `<artifact-root>`.",
            "",
        ]
    )


def _runbook(artifact_root: Path, command_lines: tuple[str, ...]) -> str:
    commands = command_lines or (
        "uv run python -m big_boy_benchmarking.cli counterpoint serious-learning calibrate "
        "--artifact-root <artifact-root> --instance-id small",
        "uv run python -m big_boy_benchmarking.cli counterpoint serious-learning summarize "
        "--artifact-root <artifact-root>",
    )
    lines = ["# Runbook", ""]
    for command in commands:
        command = _display_command(command, artifact_root)
        lines.extend(["```bash", command, "```", ""])
    return "\n".join(lines)


def _artifact_index(paths, artifact_root: Path) -> str:
    entries = [
        ("evaluation manifest", paths.evaluation_manifest),
        ("arm manifest", paths.evaluation_arm_manifest),
        ("budget lock", paths.evaluation_budget_lock),
        ("calibration summary", paths.calibration_summary),
        ("calibration run index", paths.calibration_run_index_csv),
        ("calibration recommendation", paths.calibration_recommendation_md),
        ("aggregate summary", paths.evaluation_aggregate_summary),
        ("aggregate table", paths.evaluation_aggregate_table_csv),
        ("learning curves", paths.results_dir / "learning_curves.csv"),
        ("timing summary", paths.results_dir / "timing_summary.csv"),
        ("controller summary", paths.results_dir / "controller_summary.csv"),
        ("schema diagnostic summary", paths.results_dir / "schema_diagnostic_summary.csv"),
    ]
    lines = ["# Artifact Index", ""]
    for label, path in entries:
        lines.append(f"- {label}: `{_display_path(path, artifact_root)}`")
    lines.append("")
    return "\n".join(lines)


def _results_summary(
    aggregate: dict[str, Any],
    calibration: dict[str, Any],
    artifact_root: Path,
) -> str:
    lines = ["# Results Summary", ""]
    if aggregate:
        table_path = aggregate.get("table_path")
        displayed_table_path = (
            _display_path(Path(table_path), artifact_root) if table_path else None
        )
        lines.extend(
            [
                f"Aggregate status: `{aggregate.get('status')}`",
                "Complete arms: "
                f"`{aggregate.get('complete_arm_count')}` / `{aggregate.get('arm_count')}`",
                f"Aggregate table: `{displayed_table_path}`",
                "",
            ]
        )
    if calibration:
        lines.extend(
            [
                f"Calibration status: `{calibration.get('status')}`",
                f"Calibration runs: `{calibration.get('run_count')}`",
                "",
            ]
        )
    if not aggregate and not calibration:
        lines.extend(["No calibration or aggregate artifacts were found.", ""])
    return "\n".join(lines)


def _display_path(path: Path, artifact_root: Path) -> str:
    try:
        relative = path.relative_to(artifact_root)
    except ValueError:
        return str(path)
    return f"<artifact-root>/{relative.as_posix()}"


def _display_command(command: str, artifact_root: Path) -> str:
    return command.replace(str(artifact_root), "<artifact-root>")


def _read_json(path: Path) -> dict[str, Any]:
    if not path.exists():
        return {}
    return json.loads(path.read_text())
