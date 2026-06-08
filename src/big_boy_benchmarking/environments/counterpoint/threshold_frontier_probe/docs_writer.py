"""Human-facing docs seeds for the threshold-frontier probe."""

from __future__ import annotations

import csv
import json
from pathlib import Path

from big_boy_benchmarking.environments.counterpoint.liftability import (
    STATE_COLLAPSER_V072_POINTWISE_LIFTABILITY_SEMANTICS_ID,
)

from .paths import (
    build_threshold_frontier_probe_paths,
    repo_readout_surface,
    validate_repo_resident_artifact_root,
)


def write_threshold_frontier_probe_docs(
    *,
    artifact_root: Path | str,
    docs_root: Path | str | None = None,
    command_lines: tuple[str, ...] = (),
) -> dict[str, str]:
    artifact_root = validate_repo_resident_artifact_root(artifact_root)
    docs_root = Path(docs_root) if docs_root is not None else repo_readout_surface()
    paths = build_threshold_frontier_probe_paths(artifact_root)
    results_dir = docs_root / "results"
    results_dir.mkdir(parents=True, exist_ok=True)

    aggregate_summary = _read_json(paths.evaluation_aggregate_summary)
    budget = _read_json(paths.evaluation_budget_lock)
    threshold_runs = _read_json(paths.threshold_run_manifest).get("threshold_runs", [])
    frontier_rows = _read_csv(paths.results_dir / "frontier_summary.csv")
    arm_rows = _read_csv(paths.results_dir / "threshold_arm_summary.csv")
    pair_rows = _read_csv(paths.results_dir / "threshold_pair_summary.csv")
    first_failure_rows = _read_csv(paths.results_dir / "first_failure_frontier_summary.csv")
    margin_rows = _read_csv(paths.results_dir / "post_hit_margin_summary.csv")
    lift_failure_rows = _read_csv(paths.results_dir / "lift_failure_by_tier.csv")
    frontier = frontier_rows[0] if frontier_rows else {}
    badges = _write_badges(
        docs_root,
        status=str(aggregate_summary.get("status", "unknown")),
        threshold_count=int(aggregate_summary.get("threshold_count") or len(threshold_runs)),
        claim_status=str(frontier.get("claim_status", "frontier_inconclusive")),
        highest_shared=frontier.get("highest_shared_passing_threshold", ""),
        schema1_only=frontier.get("schema1_only_passing_thresholds", ""),
        recommended=frontier.get("recommended_replicate_probe_threshold", ""),
        lift_failure_count=_lift_failure_count(lift_failure_rows),
    )
    readout_command = (
        "execute docs/prime_directive/artifact_table_to_readable_document_protocol.md at "
        f"{docs_root / 'readout_source.json'}"
    )
    summarize_command = (
        command_lines[0]
        if command_lines
        else (
            "uv run python -m big_boy_benchmarking.cli counterpoint "
            "threshold-frontier summarize --artifact-root <artifact-root>"
        )
    )
    readme_path = docs_root / "README.md"
    _write_text(
        readme_path,
        _readme(
            badges=badges,
            status=str(aggregate_summary.get("status", "unknown")),
            artifact_root=artifact_root,
            budget=budget,
            frontier=frontier,
            threshold_runs=threshold_runs,
            arm_rows=arm_rows,
            pair_rows=pair_rows,
            first_failure_rows=first_failure_rows,
            readout_command=readout_command,
            turn_section=_turn_section_for_regeneration(readme_path),
        ),
        create_parents=True,
    )
    _write_text(docs_root / "method.md", _method(artifact_root=artifact_root, budget=budget))
    _write_text(
        docs_root / "runbook.md",
        _runbook(summarize_command=summarize_command, readout_command=readout_command),
    )
    _write_text(docs_root / "artifact_index.md", _artifact_index(paths=paths))
    _write_text(docs_root / "glossary.md", _glossary())
    _write_text(
        docs_root / "result_readout.md",
        _result_readout(frontier=frontier, first_failure_rows=first_failure_rows),
    )
    _write_text(results_dir / "summary.md", _results_summary(frontier, threshold_runs))
    _write_text(results_dir / "human_summary.md", _human_summary(frontier))
    _write_text(results_dir / "frontier_readout.md", _frontier_table(frontier_rows))
    _write_text(results_dir / "threshold_table.md", _arm_table(arm_rows))
    _write_text(results_dir / "paired_threshold_table.md", _pair_table(pair_rows))
    _write_text(results_dir / "margin_readout.md", _margin_table(margin_rows))
    _write_text(results_dir / "timing_readout.md", _timing_readout(paths=paths))
    return {
        "README.md": str(docs_root / "README.md"),
        "method.md": str(docs_root / "method.md"),
        "runbook.md": str(docs_root / "runbook.md"),
        "artifact_index.md": str(docs_root / "artifact_index.md"),
        "glossary.md": str(docs_root / "glossary.md"),
        "result_readout.md": str(docs_root / "result_readout.md"),
        "results/summary.md": str(results_dir / "summary.md"),
        "results/human_summary.md": str(results_dir / "human_summary.md"),
        "results/frontier_readout.md": str(results_dir / "frontier_readout.md"),
        "results/threshold_table.md": str(results_dir / "threshold_table.md"),
        "results/paired_threshold_table.md": str(results_dir / "paired_threshold_table.md"),
        "results/margin_readout.md": str(results_dir / "margin_readout.md"),
        "results/timing_readout.md": str(results_dir / "timing_readout.md"),
    }


def _readme(
    *,
    badges: list[str],
    status: str,
    artifact_root: Path,
    budget: dict[str, object],
    frontier: dict[str, str],
    threshold_runs: list[dict[str, object]],
    arm_rows: list[dict[str, str]],
    pair_rows: list[dict[str, str]],
    first_failure_rows: list[dict[str, str]],
    readout_command: str,
    turn_section: str,
) -> str:
    return (
        "# Counterpoint Threshold Frontier Probe\n\n" + "\n".join(badges) + "\n\n"
        "This repository directory is the human-readable readout surface for the "
        "threshold-frontier probe. The probe reruns the corrected Schema 0 versus "
        "Schema 1 comparison over a locked reward-threshold grid while holding "
        "candidate, seed policy, and small budget fixed.\n\n"
        "## Status At A Glance\n\n"
        f"- Artifact evidence: `{status}`.\n"
        f"- Run mode: `{budget.get('run_mode', '')}`.\n"
        f"- Instance: `{budget.get('environment_instance_id', '')}`.\n"
        f"- Threshold count: `{len(threshold_runs)}`.\n"
        f"- Pair rows: `{len(pair_rows)}`.\n"
        f"- Claim status: `{frontier.get('claim_status', 'frontier_inconclusive')}`.\n"
        "- Recommended paired-replicate threshold: "
        f"`{frontier.get('recommended_replicate_probe_threshold', '')}`.\n\n"
        "## Liftability And Invariant Semantics\n\n"
        f"- Liftability semantics: `{STATE_COLLAPSER_V072_POINTWISE_LIFTABILITY_SEMANTICS_ID}`.\n"
        "- Runtime action availability is pointwise: an abstract action must "
        "have a concrete lift executable from the current base state.\n\n"
        "## Summary of Goals Behind this Evaluation\n\n"
        "The goal is to locate the sustained-hit threshold frontier for Schema 0 "
        "and Schema 1 under one corrected widened candidate. This is a "
        "next-measure probe, not a final serious comparison.\n\n"
        "## Summary of Methodology Behind this Evaluation\n\n"
        "For each threshold value, the runner executes the existing corrected "
        "second-serious schema comparison under matched candidate, seed, budget, "
        "and persistence settings. The frontier layer then promotes each "
        "threshold's arm, pair, tower, lift, and timing evidence into top-level "
        "frontier tables.\n\n"
        "## Frontier Summary\n\n"
        f"{_frontier_table([frontier] if frontier else [])}\n\n"
        "## First Failure By Schema\n\n"
        f"{_first_failure_table(first_failure_rows)}\n\n"
        "## Threshold Arm Rows\n\n"
        f"{_arm_table(arm_rows)}\n\n"
        "## Paired Threshold Rows\n\n"
        f"{_pair_table(pair_rows)}\n\n"
        "## Claim Boundary\n\n"
        "This readout may support only a bounded single-candidate "
        "threshold-frontier interpretation. It may not claim broad abstraction "
        "superiority, statistical significance, tensor-enabled behavior, or "
        "musical quality.\n\n"
        "To regenerate the human-readable readout, run:\n\n"
        "```text\n"
        f"{readout_command}\n"
        "```\n\n"
        f"Source artifact root:\n\n```text\n{artifact_root}\n```\n\n"
        f"{turn_section}"
    )


def _method(*, artifact_root: Path, budget: dict[str, object]) -> str:
    return (
        "# Method\n\n"
        "This evaluation composes second-serious schema-comparison subruns, one "
        "per threshold. Each subrun writes its own raw artifacts under "
        "`threshold_runs/<threshold-label>/`; the top-level threshold-frontier "
        "evaluation writes the human-facing frontier tables.\n\n"
        f"The run uses `{STATE_COLLAPSER_V072_POINTWISE_LIFTABILITY_SEMANTICS_ID}` "
        "semantics and `tensor_available_disabled` linearization.\n\n"
        "Locked budget:\n\n"
        "```json\n"
        f"{json.dumps(budget, indent=2, sort_keys=True)}\n"
        "```\n\n"
        "Artifact root:\n\n"
        "```text\n"
        f"{artifact_root}\n"
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
        f"- Arm manifest: `{paths.evaluation_arm_manifest}`\n"
        f"- Budget lock: `{paths.evaluation_budget_lock}`\n"
        f"- Threshold-frontier policy: `{paths.threshold_frontier_policy_manifest}`\n"
        f"- Threshold run manifest: `{paths.threshold_run_manifest}`\n"
        f"- Candidate manifest: `{paths.candidate_manifest}`\n"
        f"- Parent source manifest: `{paths.parent_source_manifest}`\n"
        f"- Run index: `{paths.evaluation_run_index_csv}`\n"
        f"- Aggregate table: `{paths.evaluation_aggregate_table_csv}`\n"
        f"- Aggregate summary: `{paths.evaluation_aggregate_summary}`\n"
        f"- Results directory: `{paths.results_dir}`\n"
    )


def _glossary() -> str:
    return (
        "# Glossary\n\n"
        "- threshold frontier: the highest tested reward threshold where an arm "
        "still reaches sustained-hit.\n"
        "- sustained-hit: the configured persistence rule over episode total "
        "reward, here 4 of 5 windows by default.\n"
        "- Schema 0: no-contraction total-space condition.\n"
        "- Schema 1: corrected full-iterated noisy-rate tower condition.\n"
        "- next-measure probe: evidence strong enough to steer the next run, not "
        "a final statistical comparison.\n"
    )


def _result_readout(
    *,
    frontier: dict[str, str],
    first_failure_rows: list[dict[str, str]],
) -> str:
    return (
        "# Result Readout\n\n"
        f"{_human_summary(frontier)}\n\n"
        "## Frontier\n\n"
        f"{_frontier_table([frontier] if frontier else [])}\n\n"
        "## First Failure\n\n"
        f"{_first_failure_table(first_failure_rows)}\n"
    )


def _results_summary(frontier: dict[str, str], threshold_runs: list[dict[str, object]]) -> str:
    return (
        "# Results Summary\n\n"
        f"- Thresholds tested: `{len(threshold_runs)}`.\n"
        f"- Claim status: `{frontier.get('claim_status', 'frontier_inconclusive')}`.\n"
        "- Recommended paired-replicate threshold: "
        f"`{frontier.get('recommended_replicate_probe_threshold', '')}`.\n"
    )


def _human_summary(frontier: dict[str, str]) -> str:
    claim = frontier.get("claim_status", "frontier_inconclusive")
    text = frontier.get("bounded_claim_text", "No bounded claim text was generated.")
    return f"# Human Summary\n\n`{claim}`: {text}\n"


def _frontier_table(rows: list[dict[str, str]]) -> str:
    return _markdown_table(
        rows,
        (
            "highest_shared_passing_threshold",
            "highest_schema0_passing_threshold",
            "highest_schema1_passing_threshold",
            "schema1_only_passing_thresholds",
            "recommended_replicate_probe_threshold",
            "claim_status",
        ),
    )


def _first_failure_table(rows: list[dict[str, str]]) -> str:
    return _markdown_table(
        rows,
        (
            "schema_class_id",
            "first_failure_threshold",
            "highest_passing_threshold",
            "frontier_classification",
        ),
    )


def _arm_table(rows: list[dict[str, str]]) -> str:
    return _markdown_table(
        rows,
        (
            "threshold_value",
            "schema_class_id",
            "sustained_hit_count",
            "run_count",
            "sustained_hit_rate",
            "post_hit_window_mean",
            "threshold_margin_mean",
            "passes_frontier_threshold",
        ),
    )


def _pair_table(rows: list[dict[str, str]]) -> str:
    return _markdown_table(
        rows,
        (
            "threshold_value",
            "schema0_hit_status",
            "schema1_hit_status",
            "schema1_minus_schema0_episodes_to_hit",
            "schema1_minus_schema0_post_hit_window_mean",
            "pair_status",
            "claim_blocked",
        ),
    )


def _margin_table(rows: list[dict[str, str]]) -> str:
    return _markdown_table(
        rows,
        (
            "threshold_value",
            "schema_class_id",
            "post_hit_window_mean",
            "post_hit_window_min",
            "threshold_margin_mean",
            "threshold_margin_min",
        ),
    )


def _timing_readout(*, paths) -> str:
    return (
        "# Timing Readout\n\n"
        "Timing evidence is preserved in:\n\n"
        "```text\n"
        f"{paths.results_dir / 'timing_summary.csv'}\n"
        "```\n"
    )


def _markdown_table(rows: list[dict[str, str]], columns: tuple[str, ...]) -> str:
    if not rows:
        return "_No rows._"
    header = "| " + " | ".join(columns) + " |"
    sep = "| " + " | ".join("---" for _ in columns) + " |"
    lines = [header, sep]
    for row in rows:
        lines.append("| " + " | ".join(str(row.get(col, "")) for col in columns) + " |")
    return "\n".join(lines)


def _write_badges(
    docs_root: Path,
    *,
    status: str,
    threshold_count: int,
    claim_status: str,
    highest_shared: object,
    schema1_only: object,
    recommended: object,
    lift_failure_count: int,
) -> list[str]:
    badges_dir = docs_root / "badges"
    badges_dir.mkdir(parents=True, exist_ok=True)
    specs = (
        (
            "artifacts_complete",
            "Artifacts",
            status,
            "#2e7d32" if status == "complete" else "#c62828",
        ),
        ("thresholds_tested", "Thresholds", str(threshold_count), "#1565c0"),
        ("frontier_status", "Frontier", claim_status, _claim_color(claim_status)),
        ("highest_shared", "Shared", str(highest_shared or "none"), "#1565c0"),
        (
            "schema1_only",
            "S1 Only",
            str(schema1_only or "none"),
            "#ef6c00" if schema1_only else "#616161",
        ),
        ("recommended_threshold", "Recommend", str(recommended or "none"), "#1565c0"),
        ("liftability_semantics", "Lift", "v0.7.2 pointwise", "#1565c0"),
        (
            "lift_failures",
            "Lift Fail",
            str(lift_failure_count),
            "#2e7d32" if lift_failure_count == 0 else "#c62828",
        ),
        ("provenance_repo_artifacts", "Provenance", "repo", "#1565c0"),
    )
    links = []
    for filename, label, value, color in specs:
        target = badges_dir / f"{filename}.svg"
        target.write_text(_badge_svg(label, value, color), encoding="utf-8")
        links.append(f"![{label}](badges/{filename}.svg)")
    return links


def _claim_color(claim_status: str) -> str:
    if "advantage" in claim_status:
        return "#2e7d32"
    if "blocked" in claim_status or "disadvantage" in claim_status:
        return "#c62828"
    if "inconclusive" in claim_status:
        return "#ef6c00"
    return "#1565c0"


def _badge_svg(label: str, value: str, color: str) -> str:
    safe_label = _escape_xml(label)
    safe_value = _escape_xml(value)
    width = max(120, 8 * (len(label) + len(value)) + 40)
    split = max(58, 7 * len(label) + 18)
    return (
        f'<svg xmlns="http://www.w3.org/2000/svg" width="{width}" height="20">'
        f'<rect width="{split}" height="20" fill="#555"/>'
        f'<rect x="{split}" width="{width - split}" height="20" fill="{color}"/>'
        f'<text x="{split / 2}" y="14" fill="#fff" font-family="Verdana" '
        f'font-size="11" text-anchor="middle">{safe_label}</text>'
        f'<text x="{split + (width - split) / 2}" y="14" fill="#fff" '
        f'font-family="Verdana" font-size="11" text-anchor="middle">{safe_value}</text>'
        "</svg>\n"
    )


def _escape_xml(value: object) -> str:
    return (
        str(value)
        .replace("&", "&amp;")
        .replace("<", "&lt;")
        .replace(">", "&gt;")
        .replace('"', "&quot;")
    )


def _turn_section_for_regeneration(readme_path: Path) -> str:
    marker = "## Clarifying Questions And Turns"
    if readme_path.exists():
        text = readme_path.read_text(encoding="utf-8")
        if marker in text:
            return text[text.index(marker) :].rstrip() + "\n"
    return (
        "## Clarifying Questions And Turns\n\n"
        "_No active public clarification turns are recorded for this readout._\n"
    )


def _lift_failure_count(rows: list[dict[str, str]]) -> int:
    total = 0
    for row in rows:
        for key in ("event_count", "lift_event_count", "count"):
            if row.get(key) not in (None, ""):
                total += int(float(row[key]))
                break
    return total


def _read_csv(path: Path) -> list[dict[str, str]]:
    with path.open(newline="", encoding="utf-8") as handle:
        return list(csv.DictReader(handle))


def _read_json(path: Path) -> dict[str, object]:
    return json.loads(path.read_text(encoding="utf-8"))


def _write_text(path: Path, text: str, *, create_parents: bool = False) -> None:
    if create_parents:
        path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(text, encoding="utf-8")
