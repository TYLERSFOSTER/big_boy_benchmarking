"""Human-facing docs seeds for noisy-rate full-tower training diagnostics."""

from __future__ import annotations

import csv
import json
from collections import Counter
from pathlib import Path

from big_boy_benchmarking.environments.counterpoint.noisy_rate_full_training.paths import (
    build_noisy_rate_full_training_paths,
    repo_readout_surface,
    validate_repo_resident_artifact_root,
)


def write_noisy_rate_full_training_docs(
    *,
    artifact_root: Path | str,
    docs_root: Path | str | None = None,
    command_lines: tuple[str, ...] = (),
) -> dict[str, str]:
    artifact_root = validate_repo_resident_artifact_root(artifact_root)
    docs_root = Path(docs_root) if docs_root is not None else repo_readout_surface()
    paths = build_noisy_rate_full_training_paths(artifact_root)
    results_dir = docs_root / "results"
    results_dir.mkdir(parents=True, exist_ok=True)

    aggregate_summary = _read_json(paths.evaluation_aggregate_summary)
    budget = _read_json(paths.evaluation_budget_lock)
    candidate_rows = _read_csv(paths.results_dir / "candidate_summary.csv")
    health_rows = _read_csv(paths.results_dir / "training_health_summary.csv")
    concrete_rows = _read_csv(paths.results_dir / "concrete_step_summary.csv")
    learner_rows = _read_csv(paths.results_dir / "learner_update_summary.csv")
    tower_rows = _read_csv(paths.results_dir / "tower_shape_summary.csv")

    status = str(aggregate_summary.get("status", "unknown"))
    health_counts = aggregate_summary.get("health_class_counts", {})
    concrete_steps = sum(int(row.get("concrete_step_count") or 0) for row in concrete_rows)
    learner_updates = sum(int(row.get("successful_update_count") or 0) for row in learner_rows)
    badges = _write_badges(
        docs_root,
        status=status,
        candidate_count=len(candidate_rows),
        health_counts=health_counts if isinstance(health_counts, dict) else {},
        concrete_steps=concrete_steps,
        learner_updates=learner_updates,
    )
    readout_command = (
        "execute docs/prime_directive/artifact_table_to_readable_document_protocol.md at "
        f"{docs_root / 'readout_source.json'}"
    )
    if command_lines:
        summarize_command = command_lines[0]
    else:
        summarize_command = (
            "uv run python -m big_boy_benchmarking.cli counterpoint "
            "noisy-rate-full-train summarize --artifact-root <artifact-root>"
        )
    readme_path = docs_root / "README.md"

    _write_text(
        readme_path,
        _readme(
            badges=badges,
            status=status,
            artifact_root=artifact_root,
            candidate_rows=candidate_rows,
            health_rows=health_rows,
            concrete_steps=concrete_steps,
            learner_updates=learner_updates,
            readout_command=readout_command,
            turn_section=_turn_section_for_regeneration(readme_path),
        ),
        create_parents=True,
    )
    _write_text(
        docs_root / "method.md",
        _method(artifact_root=artifact_root, budget=budget),
    )
    _write_text(
        docs_root / "runbook.md",
        _runbook(
            summarize_command=summarize_command,
            readout_command=readout_command,
        ),
    )
    _write_text(
        docs_root / "artifact_index.md",
        _artifact_index(paths=paths),
    )
    _write_text(docs_root / "glossary.md", _glossary())
    _write_text(
        docs_root / "result_readout.md",
        _result_readout(
            candidate_rows=candidate_rows,
            health_rows=health_rows,
            concrete_steps=concrete_steps,
            learner_updates=learner_updates,
        ),
    )
    _write_text(
        results_dir / "summary.md",
        _results_summary(
            health_rows=health_rows,
            concrete_steps=concrete_steps,
            learner_updates=learner_updates,
            tower_rows=tower_rows,
        ),
    )
    _write_text(
        results_dir / "human_summary.md",
        _human_summary(
            status=status,
            candidate_rows=candidate_rows,
            health_rows=health_rows,
            concrete_steps=concrete_steps,
            learner_updates=learner_updates,
        ),
    )
    _write_text(
        results_dir / "arm_readout_table.md",
        _candidate_readout_table(candidate_rows=candidate_rows, health_rows=health_rows),
    )
    _write_text(
        results_dir / "diagnostic_findings.md",
        _diagnostic_findings(health_rows=health_rows),
    )
    _write_text(
        results_dir / "timing_readout.md",
        _timing_readout(paths=paths),
    )
    return {
        "README.md": str(docs_root / "README.md"),
        "method.md": str(docs_root / "method.md"),
        "runbook.md": str(docs_root / "runbook.md"),
        "artifact_index.md": str(docs_root / "artifact_index.md"),
        "glossary.md": str(docs_root / "glossary.md"),
        "result_readout.md": str(docs_root / "result_readout.md"),
        "results/summary.md": str(results_dir / "summary.md"),
        "results/human_summary.md": str(results_dir / "human_summary.md"),
        "results/arm_readout_table.md": str(results_dir / "arm_readout_table.md"),
        "results/diagnostic_findings.md": str(results_dir / "diagnostic_findings.md"),
        "results/timing_readout.md": str(results_dir / "timing_readout.md"),
    }


def _readme(
    *,
    badges: list[str],
    status: str,
    artifact_root: Path,
    candidate_rows: list[dict[str, str]],
    health_rows: list[dict[str, str]],
    concrete_steps: int,
    learner_updates: int,
    readout_command: str,
    turn_section: str,
) -> str:
    candidate_table = _markdown_table(
        ["Candidate", "Arm", "Seed", "Tier Cells", "Active Cells"],
        [
            [
                row["candidate_id"],
                row["arm_id"],
                row["schema_seed"],
                row["tier_state_cell_count_sequence"],
                row["tier_active_action_cell_count_sequence"],
            ]
            for row in candidate_rows
        ],
    )
    health_table = _markdown_table(
        ["Candidate", "Status", "Concrete Steps", "Learner Updates", "Zero-Step Share"],
        [
            [
                row["candidate_id"],
                row["training_health_class"],
                row["concrete_steps_positive"],
                row["learner_updates_positive"],
                row["zero_step_episode_share"],
            ]
            for row in health_rows
        ],
    )
    return (
        "# Counterpoint Noisy-Rate Full-Tower Training Diagnostic\n\n"
        + "\n".join(badges)
        + "\n\n"
        "This repository directory is the human-readable readout surface for the "
        "counterpoint noisy-rate full-tower training health diagnostic.\n\n"
        "## Status At A Glance\n\n"
        f"- Artifact evidence: `{status}`.\n"
        f"- Candidate count: `{len(candidate_rows)}`.\n"
        f"- Concrete steps emitted: `{concrete_steps}`.\n"
        f"- Successful learner updates: `{learner_updates}`.\n"
        "- Claim scope: diagnostic only; this is not a direct-vs-tower comparison.\n\n"
        "## One-Screen Verdict\n\n"
        "This evaluation trains only on selected non-collapsed noisy-rate towers. "
        "It does not run a direct baseline and it does not support tower-advantage "
        "claims. It checks whether each selected tower can execute a real "
        "tower-only training budget with coherent lift, concrete-step, tier, "
        "controller, and learner-update traces.\n\n"
        "For the current noisy-rate schema, the full available tower is the base "
        "tier plus one noisy-rate quotient tier.\n\n"
        "## Source Evaluation Root\n\n"
        "```text\n"
        f"{artifact_root}\n"
        "```\n\n"
        "## Candidate Towers\n\n"
        f"{candidate_table}\n\n"
        "## Training Health\n\n"
        f"{health_table}\n\n"
        "## Claim Boundary\n\n"
        "This readout may claim that the selected non-collapsed noisy-rate towers "
        "did or did not train cleanly under the locked budget. It may not claim "
        "direct-vs-tower advantage, schema superiority, deep tower validation, "
        "tensor-enabled behavior, or musical quality.\n\n"
        "To regenerate the human-readable readout, run:\n\n"
        "```text\n"
        f"{readout_command}\n"
        "```\n\n"
        f"{turn_section}"
    )


def _method(*, artifact_root: Path, budget: dict[str, object]) -> str:
    return (
        "# Method\n\n"
        "This diagnostic selects candidates from the parent noisy-rate contraction "
        "diagnostic readout. It excludes `no_contraction_control` by default, "
        "rebuilds each selected candidate tower, verifies the tier state-cell "
        "sequence, and runs tower-only active-tier training.\n\n"
        "A real training replicate preserves learner state across all episodes "
        "inside that replicate while resetting the environment/runtime episode "
        "state between episodes.\n\n"
        "Artifact root:\n\n"
        "```text\n"
        f"{artifact_root}\n"
        "```\n\n"
        "Locked budget:\n\n"
        "```json\n"
        f"{json.dumps(budget, indent=2, sort_keys=True)}\n"
        "```\n"
    )


def _runbook(*, summarize_command: str, readout_command: str) -> str:
    return (
        "# Runbook\n\n"
        "Summarize artifacts:\n\n"
        "```text\n"
        f"{summarize_command}\n"
        "```\n\n"
        "Generate human-readable readout:\n\n"
        "```text\n"
        f"{readout_command}\n"
        "```\n"
    )


def _artifact_index(*, paths) -> str:
    return (
        "# Artifact Index\n\n"
        f"- Evaluation manifest: `{paths.evaluation_manifest}`\n"
        f"- Budget lock: `{paths.evaluation_budget_lock}`\n"
        f"- Candidate manifest: `{paths.candidate_manifest}`\n"
        f"- Run index: `{paths.evaluation_run_index_csv}`\n"
        f"- Aggregate table: `{paths.evaluation_aggregate_table_csv}`\n"
        f"- Aggregate summary: `{paths.evaluation_aggregate_summary}`\n"
        f"- Results directory: `{paths.results_dir}`\n"
    )


def _glossary() -> str:
    return (
        "# Glossary\n\n"
        "- Candidate: a non-collapsed noisy-rate tower selected from the parent readout.\n"
        "- Full available tower: all tiers produced by the current noisy-rate schema.\n"
        "- Concrete step: a lifted abstract tower action that realizes a base transition.\n"
        "- Learner update: an update summary emitted by the tower learner.\n"
        "- Training health: whether execution, lift, concrete steps, tier use, and learner updates are coherent.\n"
    )


def _results_summary(
    *,
    health_rows: list[dict[str, str]],
    concrete_steps: int,
    learner_updates: int,
    tower_rows: list[dict[str, str]],
) -> str:
    classes = Counter(row["training_health_class"] for row in health_rows)
    tier_sequences: dict[str, list[str]] = {}
    for row in tower_rows:
        tier_sequences.setdefault(row["candidate_id"], []).append(row["state_cell_count"])
    return (
        "# Results Summary\n\n"
        f"- Concrete steps: `{concrete_steps}`.\n"
        f"- Successful learner updates: `{learner_updates}`.\n"
        f"- Health classes: `{dict(classes)}`.\n"
        f"- Candidate tier sequences: `{tier_sequences}`.\n"
    )


def _result_readout(
    *,
    candidate_rows: list[dict[str, str]],
    health_rows: list[dict[str, str]],
    concrete_steps: int,
    learner_updates: int,
) -> str:
    return (
        "# Result Readout\n\n"
        "This diagnostic is a tower-only training-health check for selected "
        "non-collapsed noisy-rate counterpoint towers. It is not a direct "
        "baseline comparison and does not rank contraction schemas.\n\n"
        "## What Happened\n\n"
        f"- Selected candidates: `{len(candidate_rows)}`.\n"
        f"- Concrete base steps emitted: `{concrete_steps}`.\n"
        f"- Successful learner updates: `{learner_updates}`.\n"
        f"- Health classes: `{dict(Counter(row['training_health_class'] for row in health_rows))}`.\n\n"
        "## How We Know\n\n"
        "The evidence comes from the evaluation aggregate table plus candidate, "
        "tower-shape, concrete-step, lift, controller, tier, and learner-update "
        "summary tables listed in `readout_source.json`.\n\n"
        "## What This Means\n\n"
        "A clean health result means the selected tower executed, lifted actions "
        "to concrete transitions, and emitted learner-update evidence under the "
        "locked smoke budget.\n\n"
        "## What This Does Not Mean\n\n"
        "This run does not establish tower advantage, direct baseline performance, "
        "schema superiority, deep repeated-contraction behavior, tensor-enabled "
        "runtime behavior, or musical quality.\n"
    )


def _human_summary(
    *,
    status: str,
    candidate_rows: list[dict[str, str]],
    health_rows: list[dict[str, str]],
    concrete_steps: int,
    learner_updates: int,
) -> str:
    classes = Counter(row["training_health_class"] for row in health_rows)
    return (
        "# Human Summary\n\n"
        f"The artifact set is `{status}`. It covers `{len(candidate_rows)}` "
        "selected non-collapsed noisy-rate tower candidates. In this run, those "
        f"candidates emitted `{concrete_steps}` concrete steps and "
        f"`{learner_updates}` successful learner updates. The observed training "
        f"health classes were `{dict(classes)}`.\n\n"
        "Interpret this as an executability-and-training-health diagnostic, not "
        "as a performance comparison.\n"
    )


def _candidate_readout_table(
    *,
    candidate_rows: list[dict[str, str]],
    health_rows: list[dict[str, str]],
) -> str:
    health_by_candidate = {row["candidate_id"]: row for row in health_rows}
    rows = []
    for candidate in candidate_rows:
        health = health_by_candidate.get(candidate["candidate_id"], {})
        rows.append(
            [
                candidate["candidate_id"],
                candidate["arm_id"],
                candidate["schema_seed"],
                candidate["tier_state_cell_count_sequence"],
                health.get("training_health_class", ""),
                health.get("zero_step_episode_share", ""),
            ]
        )
    return (
        "# Candidate Readout Table\n\n"
        + _markdown_table(
            [
                "Candidate",
                "Arm",
                "Seed",
                "Tier Cells",
                "Health",
                "Zero-Step Share",
            ],
            rows,
        )
        + "\n"
    )


def _diagnostic_findings(*, health_rows: list[dict[str, str]]) -> str:
    findings = []
    for row in health_rows:
        if row["training_health_class"] == "trainable_clean":
            findings.append(
                f"- `{row['candidate_id']}` trained cleanly under this locked budget."
            )
        else:
            findings.append(
                f"- `{row['candidate_id']}` returned `{row['training_health_class']}`; inspect the result tables before making any stronger claim."
            )
    if not findings:
        findings.append("- No health rows were available.")
    return (
        "# Diagnostic Findings\n\n"
        + "\n".join(findings)
        + "\n\n"
        "These findings are bounded to the tower-only diagnostic scope.\n"
    )


def _timing_readout(*, paths) -> str:
    return (
        "# Timing Readout\n\n"
        "This generated readout does not aggregate timing into a separate "
        "evaluation-level timing table. Per-run timing evidence lives under each "
        "run directory as `timing_segments.csv` and `timing_summary.json`.\n\n"
        "Run index:\n\n"
        "```text\n"
        f"{paths.evaluation_run_index_csv}\n"
        "```\n"
    )


def _write_badges(
    docs_root: Path,
    *,
    status: str,
    candidate_count: int,
    health_counts: dict[str, object],
    concrete_steps: int,
    learner_updates: int,
) -> list[str]:
    badges_dir = docs_root / "badges"
    badges_dir.mkdir(parents=True, exist_ok=True)
    clean = int(health_counts.get("trainable_clean", 0) or 0)
    warnings = int(health_counts.get("trainable_with_warnings", 0) or 0)
    failed = sum(int(value or 0) for key, value in health_counts.items() if "untrainable" in key)
    specs = [
        ("artifacts_complete.svg", "Artifacts", "Complete" if status == "complete" else "Incomplete", "#2e7d32" if status == "complete" else "#c62828"),
        ("candidates.svg", "Candidates", str(candidate_count), "#1565c0"),
        ("training_health.svg", "Training", f"{clean} clean/{warnings} warn/{failed} fail", "#2e7d32" if failed == 0 else "#ef6c00"),
        ("runtime_executable.svg", "Runtime", "Concrete Steps" if concrete_steps > 0 else "No Concrete Steps", "#2e7d32" if concrete_steps > 0 else "#c62828"),
        ("lift_status.svg", "Learner", "Updates" if learner_updates > 0 else "No Updates", "#2e7d32" if learner_updates > 0 else "#ef6c00"),
        ("scope_diagnostic_only.svg", "Scope", "Diagnostic Only", "#1565c0"),
        ("provenance_repo_artifacts.svg", "Provenance", "Repo Artifacts", "#1565c0"),
    ]
    links = []
    for filename, label, value, color in specs:
        _write_text(badges_dir / filename, _badge_svg(label, value, color))
        links.append(f"![{label}: {value}](badges/{filename})")
    return links


def _badge_svg(label: str, value: str, color: str) -> str:
    label_width = max(70, 7 * len(label) + 12)
    value_width = max(70, 7 * len(value) + 12)
    total = label_width + value_width
    return (
        '<svg xmlns="http://www.w3.org/2000/svg" width="'
        f'{total}" height="20" role="img" aria-label="{label}: {value}">'
        f'<rect width="{label_width}" height="20" fill="#555"/>'
        f'<rect x="{label_width}" width="{value_width}" height="20" fill="{color}"/>'
        f'<text x="{label_width / 2}" y="14" fill="#fff" text-anchor="middle" '
        'font-family="Verdana,Geneva,sans-serif" font-size="11">'
        f"{label}</text>"
        f'<text x="{label_width + value_width / 2}" y="14" fill="#fff" text-anchor="middle" '
        'font-family="Verdana,Geneva,sans-serif" font-size="11">'
        f"{value}</text></svg>\n"
    )


def _markdown_table(headers: list[str], rows: list[list[object]]) -> str:
    if not rows:
        return "_No rows._"
    lines = [
        "| " + " | ".join(headers) + " |",
        "| " + " | ".join("---" for _ in headers) + " |",
    ]
    for row in rows:
        lines.append("| " + " | ".join(str(value) for value in row) + " |")
    return "\n".join(lines)


def _turn_section_for_regeneration(readme_path: Path) -> str:
    if not readme_path.exists():
        return _default_turn_section()
    text = readme_path.read_text(encoding="utf-8")
    marker = "## Clarifying Questions And Turns"
    index = text.find(marker)
    if index < 0:
        return _default_turn_section()
    section = text[index:].rstrip() + "\n"
    old_single_pair = (
        "## Clarifying Questions And Turns\n\n"
        "#### Project Owner / Evaluator Turn\n\n"
        "> ...\n\n"
        "#### Embedded Engineering Consultant / Codex Turn\n\n"
        "> ...\n"
    )
    if section == old_single_pair:
        return _default_turn_section()
    po_count = section.count("#### Project Owner / Evaluator Turn")
    codex_count = section.count("#### Embedded Engineering Consultant / Codex Turn")
    if po_count >= 1 and codex_count >= 1:
        return section
    return section.rstrip() + "\n\n" + _default_turn_pairs()


def _default_turn_section() -> str:
    return "## Clarifying Questions And Turns\n\n" + _default_turn_pairs()


def _default_turn_pairs() -> str:
    pair = (
        "#### Project Owner / Evaluator Turn\n\n"
        "> ...\n\n"
        "#### Embedded Engineering Consultant / Codex Turn\n\n"
        "> ...\n"
    )
    return "\n".join(pair for _ in range(3))


def _read_csv(path: Path) -> list[dict[str, str]]:
    if not path.exists():
        return []
    return list(csv.DictReader(path.open(encoding="utf-8")))


def _read_json(path: Path) -> dict[str, object]:
    if not path.exists():
        return {}
    return json.loads(path.read_text(encoding="utf-8"))


def _write_text(path: Path, text: str, *, create_parents: bool = False) -> None:
    if create_parents:
        path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(text, encoding="utf-8")
