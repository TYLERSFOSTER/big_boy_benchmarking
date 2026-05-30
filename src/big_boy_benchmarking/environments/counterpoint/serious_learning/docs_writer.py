"""Human-facing docs writer for serious counterpoint learning evaluations."""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any

from big_boy_benchmarking.environments.counterpoint.serious_learning.evaluation_paths import (
    build_serious_learning_evaluation_paths,
)

DEFAULT_COUNTERPOINT_SERIOUS_LEARNING_DOCS = (
    Path("docs")
    / "evaluations"
    / "counterpoint_symbolic_v001"
    / "first_serious_learning"
)


def write_serious_learning_docs(
    *,
    artifact_root: Path | str,
    docs_root: Path | str = DEFAULT_COUNTERPOINT_SERIOUS_LEARNING_DOCS,
    command_lines: tuple[str, ...] = (),
) -> dict[str, str]:
    artifact_root = Path(artifact_root)
    docs_root = Path(docs_root)
    docs_root.mkdir(parents=True, exist_ok=True)
    (docs_root / "results").mkdir(parents=True, exist_ok=True)
    paths = build_serious_learning_evaluation_paths(artifact_root)
    aggregate = _read_json(paths.evaluation_aggregate_summary)
    calibration = _read_json(paths.calibration_summary)
    files = {
        "README.md": _readme(artifact_root, aggregate, calibration),
        "method.md": _method(artifact_root),
        "runbook.md": _runbook(artifact_root, command_lines),
        "artifact_index.md": _artifact_index(paths),
        "results/summary.md": _results_summary(aggregate, calibration),
    }
    written: dict[str, str] = {}
    for relative_path, content in files.items():
        target = docs_root / relative_path
        target.parent.mkdir(parents=True, exist_ok=True)
        target.write_text(content, encoding="utf-8")
        written[relative_path] = str(target)
    return written


def _readme(
    artifact_root: Path,
    aggregate: dict[str, Any],
    calibration: dict[str, Any],
) -> str:
    status = aggregate.get("status") or calibration.get("status") or "not_run"
    return "\n".join(
        [
            "# Counterpoint First Serious Learning Evaluation",
            "",
            f"Artifact root: `{artifact_root}`",
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


def _method(artifact_root: Path) -> str:
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
            f"Artifacts are read from `{artifact_root}`.",
            "",
        ]
    )


def _runbook(artifact_root: Path, command_lines: tuple[str, ...]) -> str:
    commands = command_lines or (
        "uv run python -m big_boy_benchmarking.cli counterpoint serious-learning calibrate "
        f"--artifact-root {artifact_root} --instance-id small",
        "uv run python -m big_boy_benchmarking.cli counterpoint serious-learning summarize "
        f"--artifact-root {artifact_root}",
    )
    lines = ["# Runbook", ""]
    for command in commands:
        lines.extend(["```bash", command, "```", ""])
    return "\n".join(lines)


def _artifact_index(paths) -> str:
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
        lines.append(f"- {label}: `{path}`")
    lines.append("")
    return "\n".join(lines)


def _results_summary(
    aggregate: dict[str, Any],
    calibration: dict[str, Any],
) -> str:
    lines = ["# Results Summary", ""]
    if aggregate:
        lines.extend(
            [
                f"Aggregate status: `{aggregate.get('status')}`",
                "Complete arms: "
                f"`{aggregate.get('complete_arm_count')}` / `{aggregate.get('arm_count')}`",
                f"Aggregate table: `{aggregate.get('table_path')}`",
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


def _read_json(path: Path) -> dict[str, Any]:
    if not path.exists():
        return {}
    return json.loads(path.read_text())
