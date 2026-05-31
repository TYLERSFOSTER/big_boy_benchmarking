"""Human-facing docs seeds for one-third counterpoint tower diagnostics."""

from __future__ import annotations

import csv
import json
from pathlib import Path
from typing import Any

from big_boy_benchmarking.environments.counterpoint.one_third_diagnostics.config import (
    EVALUATION_ID,
    NEAR_FULL_COLLAPSE_THRESHOLD,
)
from big_boy_benchmarking.environments.counterpoint.one_third_diagnostics.paths import (
    build_one_third_diagnostics_paths,
    repo_readout_surface,
    validate_repo_resident_artifact_root,
)


def write_one_third_diagnostics_docs(
    *,
    artifact_root: Path | str,
    docs_root: Path | str | None = None,
    command_lines: tuple[str, ...] = (),
) -> dict[str, str]:
    artifact_root = validate_repo_resident_artifact_root(artifact_root)
    paths = build_one_third_diagnostics_paths(artifact_root)
    docs_root = repo_readout_surface() if docs_root is None else Path(docs_root)
    docs_root.mkdir(parents=True, exist_ok=True)
    (docs_root / "results").mkdir(parents=True, exist_ok=True)
    (docs_root / "badges").mkdir(parents=True, exist_ok=True)
    aggregate = _read_json(paths.evaluation_aggregate_summary)
    budget = _read_json(paths.evaluation_budget_lock)
    source = _read_json(docs_root / "readout_source.json")
    aggregate_rows = _read_csv(paths.evaluation_aggregate_table_csv)
    evidence = _evidence_snapshot(source)
    badges = _derive_badges(aggregate=aggregate, aggregate_rows=aggregate_rows, source=source)
    files = {
        "README.md": _readme(aggregate, budget, badges, evidence, artifact_root),
        "method.md": _method(budget),
        "runbook.md": _runbook(artifact_root, command_lines),
        "artifact_index.md": _artifact_index(source, artifact_root),
        "glossary.md": _glossary(),
        "result_readout.md": _result_readout(aggregate, aggregate_rows, evidence),
        "results/summary.md": _results_summary(aggregate, aggregate_rows, evidence),
        "badges/status.json": json.dumps(badges, indent=2, sort_keys=True) + "\n",
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
    budget: dict[str, Any],
    badges: dict[str, Any],
    evidence: dict[str, Any],
    artifact_root: Path,
) -> str:
    status = aggregate.get("status", "not_run")
    badge_line = " ".join(
        f"`{item['label']}: {item['status']}`" for item in badges.get("badges", [])
    )
    return "\n".join(
        [
            "# Counterpoint One-Third Schema Tower Diagnostics",
            "",
            badge_line,
            "",
            f"Status: `{status}`",
            f"Evaluation id: `{EVALUATION_ID}`",
            f"Artifact root: `{artifact_root}`",
            "",
            "This readout is for the source-local one-third contraction schema on the "
            "existing `counterpoint_symbolic_v001` environment. It observes tower "
            "geometry, upstream ABC tier selection, lift/executability behavior, and "
            "concrete step emission. It is not a direct-vs-tower performance comparison.",
            "",
            "Near full collapse means a single tier-1 quotient state cell contains at "
            f"least `{NEAR_FULL_COLLAPSE_THRESHOLD:.2f}` of all base states. When that "
            "happens, the run can still be diagnostically useful, but ordinary "
            "performance language is blocked because the first projection preserved too "
            "little state structure.",
            "",
            "Current evidence headline:",
            "",
            *evidence["headline_lines"],
            "",
            "Locked budget:",
            "",
            f"- instances: `{', '.join(budget.get('instance_ids', []))}`",
            f"- schema seeds: `{budget.get('schema_seeds', [])}`",
            f"- replicates per schema seed: `{budget.get('replicates_per_schema_seed')}`",
            f"- episodes per replicate: `{budget.get('episodes_per_replicate')}`",
            f"- linearization mode: `{budget.get('linearization_mode_id')}`",
            "",
            "Open Questions For Project Owner",
            "",
            "- Are the diagnostic categories sufficient for deciding the next schema "
            "variant to study?",
            "- Should future readouts add compact plots once the table semantics stabilize?",
            "",
            "Consultant-authored notes",
            "",
            "- Generated readouts must not invent Project Owner turns. Use this section "
            "for model-authored interpretation or questions.",
            "",
        ]
    )


def _method(budget: dict[str, Any]) -> str:
    return "\n".join(
        [
            "# Method",
            "",
            "This evaluation runs upstream `state_collapser` active-tier ABC control "
            "through BBB's counterpoint tower adapter. The only schema under test is "
            "`counterpoint_one_third_outgoing_schema_v001`.",
            "",
            "The schema samples outgoing edges source-locally. For each source state, "
            "outgoing edges are deterministically shuffled by schema seed, then assigned "
            "through three recursive one-third contraction blocks using "
            "`ceil(remaining / 3)` block sizes. Leftovers are reported explicitly.",
            "",
            "BBB records ordinary control events and additional ABC diagnostic rows. The "
            "additional rows are computed from upstream helper functions on the exact "
            "inputs passed to upstream `ActiveTierController.decide(...)`; BBB does not "
            "substitute a new controller policy.",
            "",
            "Budget summary:",
            "",
            f"- controller event ceiling policy: `{budget.get('controller_event_ceiling_policy')}`",
            f"- horizon by instance id: `{budget.get('horizon_by_instance_id')}`",
            "",
        ]
    )


def _runbook(artifact_root: Path, command_lines: tuple[str, ...]) -> str:
    commands = command_lines or (
        "uv run python -m big_boy_benchmarking.cli counterpoint one-third-diagnostics run "
        "--artifact-root <artifact-root> --instance-ids small,medium",
        "uv run python -m big_boy_benchmarking.cli counterpoint one-third-diagnostics "
        "summarize --artifact-root <artifact-root>",
        "execute docs/prime_directive/artifact_table_to_readable_document_protocol.md at "
        "docs/evaluations/counterpoint_symbolic_v001/"
        "one_third_schema_tower_diagnostics/readout_source.json",
    )
    lines = ["# Runbook", ""]
    for command in commands:
        lines.extend(["```bash", command.replace(str(artifact_root), "<artifact-root>"), "```", ""])
    return "\n".join(lines)


def _artifact_index(source: dict[str, Any], artifact_root: Path) -> str:
    lines = ["# Artifact Index", ""]
    source_files = source.get("source_files", {})
    if not source_files:
        lines.extend(["No source binding was found.", ""])
        return "\n".join(lines)
    for label, path_text in sorted(source_files.items()):
        lines.append(f"- {label}: `{_display_path(Path(path_text), artifact_root)}`")
    lines.append("")
    return "\n".join(lines)


def _glossary() -> str:
    return "\n".join(
        [
            "# Glossary",
            "",
            "- ABC: upstream active-tier controller behavior that decides whether to "
            "lift, descend, train, explore, or exploit/execute.",
            "- source-local one-third: contraction assignment computed separately for "
            "each source state's outgoing edges.",
            "- selected tier: the lowest executable unclosed tier selected by upstream "
            "ABC helper logic.",
            "- executable tier: a tier whose current quotient state has outgoing action "
            "cells available.",
            "- concrete step: an abstract tower action successfully lifted to a base "
            "counterpoint transition.",
            "- near full collapse: tier-1 largest state fiber share is at least 0.90.",
            "",
        ]
    )


def _result_readout(
    aggregate: dict[str, Any],
    aggregate_rows: list[dict[str, str]],
    evidence: dict[str, Any],
) -> str:
    lines = ["# Result Readout", ""]
    lines.extend(_high_level_result_lines(aggregate, aggregate_rows, evidence))
    lines.extend(
        [
            "",
            "Structural classifications are evidence labels. They are not failures by "
            "themselves; they say which interpretations are blocked or need extra care.",
            "",
        ]
    )
    return "\n".join(lines)


def _results_summary(
    aggregate: dict[str, Any],
    aggregate_rows: list[dict[str, str]],
    evidence: dict[str, Any],
) -> str:
    lines = ["# Results Summary", ""]
    lines.extend(_high_level_result_lines(aggregate, aggregate_rows, evidence))
    lines.append("")
    return "\n".join(lines)


def _high_level_result_lines(
    aggregate: dict[str, Any],
    aggregate_rows: list[dict[str, str]],
    evidence: dict[str, Any],
) -> list[str]:
    run_count = aggregate.get("run_count", 0)
    complete = aggregate.get("complete_run_count", 0)
    classifications = aggregate.get("classification_counts", {})
    zero_step = sum(row.get("zero_concrete_steps") == "True" for row in aggregate_rows)
    no_available = sum(int(row.get("no_available_action_count") or 0) for row in aggregate_rows)
    lines = [
        f"- runs represented: `{complete}` / `{run_count}` complete",
        f"- zero-concrete-step runs: `{zero_step}`",
        f"- no-available-action events: `{no_available}`",
        f"- classification counts: `{json.dumps(classifications, sort_keys=True)}`",
    ]
    lines.extend(evidence["detail_lines"])
    table_path = aggregate.get("table_path")
    if table_path:
        lines.append(f"- aggregate table: `{table_path}`")
    return lines


def _evidence_snapshot(source: dict[str, Any]) -> dict[str, Any]:
    files = source.get("source_files", {})
    aggregate_rows = _read_source_csv(files, "aggregate_table")
    control_rows = _read_source_csv(files, "control_action_summary")
    concrete_rows = _read_source_csv(files, "concrete_step_summary")
    lift_rows = _read_source_csv(files, "lift_failure_by_tier")
    abc_rows = _read_source_csv(files, "abc_selection_summary")

    run_count = len(aggregate_rows)
    full_collapse_runs = sum(
        row.get("full_first_projection_collapse") == "True" for row in aggregate_rows
    )
    concrete_steps = sum(int(row.get("concrete_step_count") or 0) for row in concrete_rows)
    terminated = sum(int(row.get("terminated_count") or 0) for row in concrete_rows)
    truncated = sum(int(row.get("truncated_count") or 0) for row in concrete_rows)
    lift_attempts = sum(int(row.get("lift_attempt_count") or 0) for row in lift_rows)
    lift_successes = sum(int(row.get("lift_success_count") or 0) for row in lift_rows)
    lift_failures = sum(int(row.get("lift_failure_count") or 0) for row in lift_rows)
    action_counts: dict[str, int] = {}
    for row in control_rows:
        action = row.get("control_action", "")
        action_counts[action] = action_counts.get(action, 0) + int(row.get("event_count") or 0)
    consistent_events = sum(int(row.get("action_consistent_count") or 0) for row in abc_rows)
    abc_events = sum(int(row.get("event_count") or 0) for row in abc_rows)
    action_text = ", ".join(
        f"{action}={count}" for action, count in sorted(action_counts.items())
    )
    headline_lines = [
        (
            "- `24` expected runs are represented as complete."
            if run_count == 24
            else f"- `{run_count}` runs are represented."
        ),
        (
            f"- `{full_collapse_runs}` / `{run_count}` runs show full tier-1 "
            "projection collapse."
        ),
        (
            f"- Runtime execution did not stall: `{concrete_steps}` concrete steps, "
            f"`{lift_successes}` / `{lift_attempts}` lift attempts succeeded, "
            f"and `{lift_failures}` lift attempts failed."
        ),
        f"- Episodes terminated/truncated: `{terminated}` terminated, `{truncated}` truncated.",
    ]
    detail_lines = [
        f"- concrete steps: `{concrete_steps}`",
        (
            f"- lift attempts/successes/failures: `{lift_attempts}` / "
            f"`{lift_successes}` / `{lift_failures}`"
        ),
        f"- control action counts: `{action_text}`",
        f"- ABC action consistency: `{consistent_events}` / `{abc_events}` events",
    ]
    return {"headline_lines": headline_lines, "detail_lines": detail_lines}


def _read_source_csv(files: dict[str, Any], key: str) -> list[dict[str, str]]:
    path_text = files.get(key)
    if not path_text:
        return []
    return _read_csv(Path(path_text))


def _derive_badges(
    *,
    aggregate: dict[str, Any],
    aggregate_rows: list[dict[str, str]],
    source: dict[str, Any],
) -> dict[str, Any]:
    required = source.get("expected_files", {}).get("required", [])
    source_root = Path(source.get("source_evaluation_root", "")) if source else None
    missing = []
    if source_root is not None:
        for relative in required:
            if not (source_root / relative).exists():
                missing.append(relative)
    complete = aggregate.get("status") == "complete"
    zero_step = any(row.get("zero_concrete_steps") == "True" for row in aggregate_rows)
    near_collapse = any(
        row.get("near_full_first_projection_collapse") == "True"
        or row.get("full_first_projection_collapse") == "True"
        for row in aggregate_rows
    )
    no_available = any(int(row.get("no_available_action_count") or 0) > 0 for row in aggregate_rows)
    badges = [
        _badge(
            "artifact_status",
            "green" if not missing else "red",
            "complete" if not missing else "missing",
        ),
        _badge(
            "schema_geometry_status",
            "yellow" if near_collapse else "green",
            "structural-limit" if near_collapse else "observed",
        ),
        _badge(
            "abc_runtime_status",
            "green" if complete else "yellow",
            "complete" if complete else "partial",
        ),
        _badge(
            "lift_executability_status",
            "yellow" if zero_step or no_available else "green",
            "limited" if zero_step or no_available else "observed",
        ),
        _badge("claim_scope", "yellow", "diagnostic-only"),
        _badge(
            "provenance_status",
            "green" if source else "red",
            "repo-bound" if source else "missing",
        ),
    ]
    return {"badges": badges, "missing_required_files": missing}


def _badge(label: str, color: str, status: str) -> dict[str, str]:
    return {"label": label, "color": color, "status": status}


def _display_path(path: Path, artifact_root: Path) -> str:
    try:
        relative = path.relative_to(artifact_root)
    except ValueError:
        return str(path)
    return f"<artifact-root>/{relative.as_posix()}"


def _read_json(path: Path) -> dict[str, Any]:
    if not path.exists():
        return {}
    return json.loads(path.read_text())


def _read_csv(path: Path) -> list[dict[str, str]]:
    if not path.exists():
        return []
    return list(csv.DictReader(path.open()))
