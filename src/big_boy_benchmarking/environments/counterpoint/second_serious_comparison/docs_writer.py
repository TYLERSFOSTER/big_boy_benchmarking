"""Human-facing docs seeds for the second serious schema comparison."""

from __future__ import annotations

import csv
import json
from collections import Counter
from pathlib import Path

from big_boy_benchmarking.environments.counterpoint.liftability import (
    STATE_COLLAPSER_V072_POINTWISE_LIFTABILITY_SEMANTICS_ID,
)
from big_boy_benchmarking.environments.counterpoint.second_serious_comparison.config import (
    EVALUATION_RUN_FAMILY_ID,
)
from big_boy_benchmarking.environments.counterpoint.second_serious_comparison.paths import (
    build_second_serious_comparison_paths,
    repo_readout_surface,
    validate_repo_resident_artifact_root,
)


def write_second_serious_comparison_docs(
    *,
    artifact_root: Path | str,
    docs_root: Path | str | None = None,
    command_lines: tuple[str, ...] = (),
) -> dict[str, str]:
    artifact_root = validate_repo_resident_artifact_root(artifact_root)
    docs_root = Path(docs_root) if docs_root is not None else repo_readout_surface()
    paths = build_second_serious_comparison_paths(artifact_root)
    results_dir = docs_root / "results"
    results_dir.mkdir(parents=True, exist_ok=True)

    aggregate_summary = _read_json(paths.evaluation_aggregate_summary)
    budget = _read_json(paths.evaluation_budget_lock)
    arm_rows = _read_csv(paths.results_dir / "arm_summary.csv")
    pair_rows = _read_csv(paths.results_dir / "paired_schema_comparison.csv")
    claim_rows = _read_csv(paths.results_dir / "comparison_claim_summary.csv")
    hit_rows = _read_csv(paths.results_dir / "first_sustained_hit_summary.csv")
    candidate_rows = _read_csv(paths.results_dir / "candidate_summary.csv")
    run_rows = _read_csv(paths.evaluation_run_index_csv)
    lift_failure_rows = _read_csv(paths.results_dir / "lift_failure_by_tier.csv")

    status = str(aggregate_summary.get("status", "unknown"))
    hit_counts = Counter(row.get("hit_status", "") for row in hit_rows)
    pair_count = len(pair_rows)
    unblocked_pairs = sum(row.get("claim_blocked") in {"False", "false", "0"} for row in pair_rows)
    invariant_status = _invariant_preflight_status(artifact_root, run_rows)
    lift_failure_count = _lift_failure_count(lift_failure_rows)
    badges = _write_badges(
        docs_root,
        status=status,
        candidate_count=sum(row.get("selected") in {"True", "true", "1"} for row in candidate_rows),
        sustained_count=int(hit_counts.get("sustained_hit", 0)),
        pair_count=pair_count,
        unblocked_pairs=unblocked_pairs,
        invariant_status=invariant_status,
        lift_failure_count=lift_failure_count,
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
            "second-serious-comparison summarize --artifact-root <artifact-root>"
        )
    )
    readme_path = docs_root / "README.md"
    _write_text(
        readme_path,
        _readme(
            badges=badges,
            status=status,
            artifact_root=artifact_root,
            budget=budget,
            arm_rows=arm_rows,
            pair_rows=pair_rows,
            claim_rows=claim_rows,
            hit_rows=hit_rows,
            invariant_status=invariant_status,
            lift_failure_count=lift_failure_count,
            readout_command=readout_command,
            turn_section=_turn_section_for_regeneration(readme_path),
        ),
        create_parents=True,
    )
    _write_text(
        docs_root / "method.md",
        _method(
            artifact_root=artifact_root,
            budget=budget,
            invariant_status=invariant_status,
            lift_failure_count=lift_failure_count,
        ),
    )
    _write_text(
        docs_root / "runbook.md",
        _runbook(summarize_command=summarize_command, readout_command=readout_command),
    )
    _write_text(docs_root / "artifact_index.md", _artifact_index(paths=paths))
    _write_text(docs_root / "glossary.md", _glossary())
    _write_text(
        docs_root / "result_readout.md",
        _result_readout(arm_rows=arm_rows, pair_rows=pair_rows, claim_rows=claim_rows),
    )
    _write_text(
        results_dir / "summary.md",
        _results_summary(arm_rows=arm_rows, hit_rows=hit_rows, pair_rows=pair_rows),
    )
    _write_text(
        results_dir / "human_summary.md",
        _human_summary(status=status, arm_rows=arm_rows, claim_rows=claim_rows),
    )
    _write_text(results_dir / "arm_readout_table.md", _arm_table(arm_rows))
    _write_text(results_dir / "diagnostic_findings.md", _diagnostic_findings(claim_rows))
    _write_text(results_dir / "paired_comparison_readout.md", _paired_table(pair_rows))
    _write_text(results_dir / "threshold_policy_readout.md", _threshold_policy(budget))
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
        "results/arm_readout_table.md": str(results_dir / "arm_readout_table.md"),
        "results/diagnostic_findings.md": str(results_dir / "diagnostic_findings.md"),
        "results/paired_comparison_readout.md": str(results_dir / "paired_comparison_readout.md"),
        "results/threshold_policy_readout.md": str(results_dir / "threshold_policy_readout.md"),
        "results/timing_readout.md": str(results_dir / "timing_readout.md"),
    }


def _readme(
    *,
    badges: list[str],
    status: str,
    artifact_root: Path,
    budget: dict[str, object],
    arm_rows: list[dict[str, str]],
    pair_rows: list[dict[str, str]],
    claim_rows: list[dict[str, str]],
    hit_rows: list[dict[str, str]],
    invariant_status: str,
    lift_failure_count: int,
    readout_command: str,
    turn_section: str,
) -> str:
    return (
        "# Counterpoint Second Serious Schema Comparison\n\n" + "\n".join(badges) + "\n\n"
        "This repository directory is the human-readable readout surface for the "
        "second serious counterpoint schema-comparison evaluation.\n\n"
        "## Status At A Glance\n\n"
        f"- Artifact evidence: `{status}`.\n"
        f"- Run mode: `{budget.get('run_mode', '')}`.\n"
        f"- Instance: `{budget.get('environment_instance_id', '')}`.\n"
        f"- Threshold value: `{budget.get('threshold_value', None)}`.\n"
        f"- Paired rows: `{len(pair_rows)}`.\n"
        f"- Sustained-hit rows: `{_sustained_hit_count(hit_rows)}`.\n\n"
        "## Liftability And Invariant Semantics\n\n"
        f"- Liftability semantics: `{STATE_COLLAPSER_V072_POINTWISE_LIFTABILITY_SEMANTICS_ID}`.\n"
        f"- Invariant preflight: `{invariant_status}`.\n"
        f"- Lift failure rows: `{lift_failure_count}`.\n"
        "- Tower action masks and tier executability use executable concrete "
        "lifts from the current base state. Quotient-level outgoing action "
        "cells remain diagnostic/shape evidence, not proof that an abstract "
        "action can execute at a particular concrete state.\n\n"
        "## Summary of Goals Behind this Evaluation\n\n"
        "The goal is to compare schema conditions, not old runner paths: "
        "`schema0_no_contraction` versus selected `schema1_noisy_rate_one_drop` "
        "candidates under a matched active-tier tower-control harness. The main "
        "measurement is first sustained total-space adequacy under a locked "
        "`episode_total_reward` threshold and a 4-of-5 persistence rule.\n\n"
        "## Summary of Methodology Behind this Evaluation\n\n"
        "Schema 1 candidates are loaded from the noisy-rate full-tower training "
        "readout source, preserving provenance back to the noisy-rate contraction "
        "diagnostic. For each selected Schema 1 candidate, the runner creates a "
        "paired Schema 0 no-contraction condition with the same seed bundle, "
        "episode budget, learner family, threshold policy, and linearization mode.\n\n"
        "## Schema Arms\n\n"
        f"{_arm_table(arm_rows)}\n\n"
        "## First Sustained Hit Summary\n\n"
        f"{_hit_table(hit_rows)}\n\n"
        "## Paired Comparison Summary\n\n"
        f"{_paired_table(pair_rows)}\n\n"
        "## Claim Boundary\n\n"
        "This readout may support a bounded speed-to-sustained-hit comparison only "
        "when paired rows are unblocked. It may not claim broad abstraction "
        "superiority, musical quality, direct-runner advantage, tensor-enabled "
        "behavior, or general schema dominance.\n\n"
        "## Current Claim Rows\n\n"
        f"{_claim_table(claim_rows)}\n\n"
        "To regenerate the human-readable readout, run:\n\n"
        "```text\n"
        f"{readout_command}\n"
        "```\n\n"
        f"Source artifact root:\n\n```text\n{artifact_root}\n```\n\n"
        f"{turn_section}"
    )


def _method(
    *,
    artifact_root: Path,
    budget: dict[str, object],
    invariant_status: str,
    lift_failure_count: int,
) -> str:
    return (
        "# Method\n\n"
        "This evaluation compares two schema classes inside the same active-tier "
        "tower-control training harness. Schema 0 is no contraction. Schema 1 is "
        "a selected one-drop noisy-rate quotient candidate from the existing "
        "full-tower training diagnostic source.\n\n"
        f"The run uses `{STATE_COLLAPSER_V072_POINTWISE_LIFTABILITY_SEMANTICS_ID}` "
        "semantics from `state_collapser` v0.7.2: tower action masks and tier "
        "executability are based on concrete lifts executable from the current "
        "base state, not merely quotient-level outgoing action cells. Quotient "
        "action availability still appears in shape and diagnostic tables as "
        "structural support evidence. Pointwise executable liftability is the "
        "runtime criterion.\n\n"
        f"Invariant preflight status: `{invariant_status}`. Lift failure rows "
        f"reported in the aggregate readout: `{lift_failure_count}`.\n\n"
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
        f"- Arm manifest: `{paths.evaluation_arm_manifest}`\n"
        f"- Budget lock: `{paths.evaluation_budget_lock}`\n"
        f"- Threshold policy: `{paths.threshold_policy_manifest}`\n"
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
        "- Schema 0: the matched no-contraction condition.\n"
        "- Schema 1: selected one-drop noisy-rate quotient candidate.\n"
        "- Candidate group: one Schema 1 candidate plus its paired Schema 0 condition.\n"
        "- Sustained hit: a rolling window where at least 4 of 5 episode rewards "
        "meet the locked threshold.\n"
        "- Claim-blocked pair: a pair that cannot support speed comparison because "
        "one side failed, never sustained, or hit a structural limit.\n"
    )


def _result_readout(
    *,
    arm_rows: list[dict[str, str]],
    pair_rows: list[dict[str, str]],
    claim_rows: list[dict[str, str]],
) -> str:
    return (
        "# Result Readout\n\n"
        "## Arm Summary\n\n"
        f"{_arm_table(arm_rows)}\n\n"
        "## Pair Summary\n\n"
        f"{_paired_table(pair_rows)}\n\n"
        "## Claim Summary\n\n"
        f"{_claim_table(claim_rows)}\n"
    )


def _results_summary(
    *,
    arm_rows: list[dict[str, str]],
    hit_rows: list[dict[str, str]],
    pair_rows: list[dict[str, str]],
) -> str:
    return (
        "# Results Summary\n\n"
        f"- Arm rows: `{len(arm_rows)}`.\n"
        f"- Hit rows: `{len(hit_rows)}`.\n"
        f"- Paired rows: `{len(pair_rows)}`.\n"
        f"- Hit statuses: `{dict(Counter(row.get('hit_status', '') for row in hit_rows))}`.\n"
    )


def _human_summary(
    *,
    status: str,
    arm_rows: list[dict[str, str]],
    claim_rows: list[dict[str, str]],
) -> str:
    claim = claim_rows[0]["bounded_claim_text"] if claim_rows else "No claim row available."
    return (
        "# Human Summary\n\n"
        f"The artifact set is `{status}`. It includes `{len(arm_rows)}` schema-arm "
        f"summary rows. Current bounded claim text: {claim}\n"
    )


def _diagnostic_findings(claim_rows: list[dict[str, str]]) -> str:
    if not claim_rows:
        return "# Diagnostic Findings\n\n- No comparison claim rows were available.\n"
    return (
        "# Diagnostic Findings\n\n"
        + "\n".join(
            f"- Claim status `{row['claim_status']}`: {row['bounded_claim_text']}"
            for row in claim_rows
        )
        + "\n"
    )


def _threshold_policy(budget: dict[str, object]) -> str:
    return (
        "# Threshold Policy Readout\n\n"
        f"- Threshold policy id: `{budget.get('threshold_policy_id', '')}`.\n"
        f"- Metric: `episode_total_reward`.\n"
        f"- Threshold value: `{budget.get('threshold_value', None)}`.\n"
        f"- Window length: `{budget.get('window_length', '')}`.\n"
        f"- Required count: `{budget.get('required_count', '')}`.\n"
        "- Comparison: `greater_than_or_equal`.\n"
    )


def _timing_readout(*, paths) -> str:
    return (
        "# Timing Readout\n\n"
        "Per-run timing evidence lives under each run directory as "
        "`timing_segments.csv` and `timing_summary.json`. Evaluation-level "
        "timing summary rows are in:\n\n"
        "```text\n"
        f"{paths.results_dir / 'timing_summary.csv'}\n"
        "```\n"
    )


def _arm_table(rows: list[dict[str, str]]) -> str:
    return _markdown_table(
        [
            "Schema",
            "Runs",
            "Sustained",
            "Transient",
            "Never",
            "Median Episodes",
        ],
        [
            [
                row.get("schema_class_id", ""),
                row.get("run_count", ""),
                row.get("sustained_hit_count", ""),
                row.get("transient_hit_count", ""),
                row.get("never_hit_count", ""),
                row.get("median_episodes_to_sustained_hit", ""),
            ]
            for row in rows
        ],
    )


def _hit_table(rows: list[dict[str, str]]) -> str:
    return _markdown_table(
        ["Run", "Schema", "Status", "First Sustained Episode"],
        [
            [
                row.get("run_id", ""),
                row.get("schema_class_id", ""),
                row.get("hit_status", ""),
                row.get("first_sustained_hit_episode_index", ""),
            ]
            for row in rows
        ],
    )


def _paired_table(rows: list[dict[str, str]]) -> str:
    return _markdown_table(
        ["Candidate Group", "Seed", "Pair Status", "Delta", "Blocked"],
        [
            [
                row.get("candidate_group_id", ""),
                row.get("seed_bundle_id", ""),
                row.get("pair_status", ""),
                row.get("schema1_minus_schema0_episodes_to_hit", ""),
                row.get("claim_blocked", ""),
            ]
            for row in rows
        ],
    )


def _claim_table(rows: list[dict[str, str]]) -> str:
    return _markdown_table(
        ["Claim Status", "Pairs", "Unblocked", "Schema1 Faster", "Schema1 Slower"],
        [
            [
                row.get("claim_status", ""),
                row.get("pair_count", ""),
                row.get("unblocked_pair_count", ""),
                row.get("schema1_faster_pair_count", ""),
                row.get("schema1_slower_pair_count", ""),
            ]
            for row in rows
        ],
    )


def _sustained_hit_count(rows: list[dict[str, str]]) -> int:
    return sum(row.get("hit_status") == "sustained_hit" for row in rows)


def _invariant_preflight_status(artifact_root: Path, run_rows: list[dict[str, str]]) -> str:
    successful_runs = [row for row in run_rows if row.get("status") == "success"]
    if not successful_runs:
        return "unknown"
    reports = [
        _read_json(_run_root(artifact_root, row["run_id"]) / "tower_invariant_report.json")
        for row in successful_runs
    ]
    if not reports:
        return "unknown"
    if all(report.get("ok") is True for report in reports):
        return "passed"
    return "failed_or_missing"


def _lift_failure_count(rows: list[dict[str, str]]) -> int:
    total = 0
    for row in rows:
        total += int(row.get("event_count") or row.get("failure_count") or 0)
    return total


def _run_root(artifact_root: Path, run_id: str) -> Path:
    return artifact_root / "runs" / EVALUATION_RUN_FAMILY_ID / "runs" / run_id


def _write_badges(
    docs_root: Path,
    *,
    status: str,
    candidate_count: int,
    sustained_count: int,
    pair_count: int,
    unblocked_pairs: int,
    invariant_status: str,
    lift_failure_count: int,
) -> list[str]:
    badges_dir = docs_root / "badges"
    badges_dir.mkdir(parents=True, exist_ok=True)
    specs = [
        (
            "artifacts_complete.svg",
            "Artifacts",
            "Complete" if status == "complete" else "Incomplete",
            "#2e7d32" if status == "complete" else "#c62828",
        ),
        ("candidates.svg", "Candidates", str(candidate_count), "#1565c0"),
        (
            "threshold_hits.svg",
            "Hits",
            str(sustained_count),
            "#2e7d32" if sustained_count else "#ef6c00",
        ),
        (
            "pairs.svg",
            "Pairs",
            f"{unblocked_pairs}/{pair_count} unblocked",
            "#2e7d32" if unblocked_pairs else "#ef6c00",
        ),
        ("scope_schema_comparison.svg", "Scope", "Schema Compare", "#1565c0"),
        ("provenance_repo_artifacts.svg", "Provenance", "Repo Artifacts", "#1565c0"),
        ("liftability_semantics.svg", "Liftability", "Pointwise v0.7.2", "#2e7d32"),
        (
            "invariant_preflight.svg",
            "Invariant",
            invariant_status,
            "#2e7d32" if invariant_status == "passed" else "#ef6c00",
        ),
        (
            "lift_failures.svg",
            "Lift Failures",
            str(lift_failure_count),
            "#2e7d32" if lift_failure_count == 0 else "#ef6c00",
        ),
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
    po_count = section.count("#### Project Owner / Evaluator Turn")
    codex_count = section.count("#### Embedded Engineering Consultant / Codex Turn")
    if po_count >= 1 and codex_count >= 1:
        return section
    return section.rstrip() + "\n\n" + _default_turn_pairs()


def _default_turn_section() -> str:
    return (
        "## Clarifying Questions And Turns\n\n"
        "_No active public clarification turns are recorded for this readout._\n"
    )


def _default_turn_pairs() -> str:
    pair = (
        "#### Project Owner / Evaluator Turn\n\n"
        "_Open for a future evaluator turn._\n\n"
        "#### Embedded Engineering Consultant / Codex Turn\n\n"
        "_Open for a future Codex turn._\n"
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
