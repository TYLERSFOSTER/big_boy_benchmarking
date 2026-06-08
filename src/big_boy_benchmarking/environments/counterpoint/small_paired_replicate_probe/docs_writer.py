"""Human-facing docs seeds for the small paired replicate probe."""

from __future__ import annotations

import csv
import json
from pathlib import Path

from big_boy_benchmarking.environments.counterpoint.liftability import (
    STATE_COLLAPSER_V072_POINTWISE_LIFTABILITY_SEMANTICS_ID,
)
from big_boy_benchmarking.environments.counterpoint.small_paired_replicate_probe.paths import (
    build_small_paired_replicate_probe_paths,
    repo_readout_surface,
    validate_repo_resident_artifact_root,
)


def write_small_paired_replicate_probe_docs(
    *,
    artifact_root: Path | str,
    docs_root: Path | str | None = None,
    command_lines: tuple[str, ...] = (),
) -> dict[str, str]:
    artifact_root = validate_repo_resident_artifact_root(artifact_root)
    docs_root = Path(docs_root) if docs_root is not None else repo_readout_surface()
    paths = build_small_paired_replicate_probe_paths(artifact_root)
    results_dir = docs_root / "results"
    results_dir.mkdir(parents=True, exist_ok=True)

    aggregate_summary = _read_json(paths.evaluation_aggregate_summary)
    budget = _read_json(paths.evaluation_budget_lock)
    threshold_policy = _read_json(paths.threshold_policy_manifest)
    pair_rows = _read_csv(paths.results_dir / "replicate_pair_summary.csv")
    delta_rows = _read_csv(paths.results_dir / "paired_delta_distribution.csv")
    arm_rows = _read_csv(paths.results_dir / "schema_arm_distribution.csv")
    margin_rows = _read_csv(paths.results_dir / "post_hit_margin_distribution.csv")
    hit_rate_rows = _read_csv(paths.results_dir / "sustained_hit_rate_summary.csv")
    seed_rows = _read_csv(paths.results_dir / "seed_bundle_summary.csv")
    lift_failure_rows = _read_csv(paths.results_dir / "lift_failure_by_tier.csv")

    status = str(aggregate_summary.get("status", "unknown"))
    pair_count = int(aggregate_summary.get("pair_count") or len(pair_rows))
    unblocked_pairs = int(
        aggregate_summary.get("unblocked_pair_count")
        or sum(row.get("claim_blocked") in {"False", "false", "0"} for row in pair_rows)
    )
    margin_wins = int(
        aggregate_summary.get("schema1_margin_win_count")
        or _first_int(delta_rows, "schema1_margin_win_count")
    )
    lift_failure_count = int(
        aggregate_summary.get("lift_failure_count") or _lift_failure_count(lift_failure_rows)
    )
    hit_rate_delta = _hit_rate_delta(hit_rate_rows)
    badges = _write_badges(
        docs_root,
        status=status,
        pair_count=pair_count,
        unblocked_pairs=unblocked_pairs,
        margin_wins=margin_wins,
        hit_rate_delta=hit_rate_delta,
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
            "paired-replicate-probe summarize --artifact-root <artifact-root>"
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
            threshold_policy=threshold_policy,
            pair_rows=pair_rows,
            delta_rows=delta_rows,
            arm_rows=arm_rows,
            hit_rate_rows=hit_rate_rows,
            seed_rows=seed_rows,
            lift_failure_count=lift_failure_count,
            readout_command=readout_command,
            turn_section=_turn_section_for_regeneration(readme_path),
        ),
        create_parents=True,
    )
    _write_text(
        docs_root / "method.md",
        _method(artifact_root=artifact_root, budget=budget, threshold_policy=threshold_policy),
    )
    _write_text(
        docs_root / "runbook.md",
        _runbook(summarize_command=summarize_command, readout_command=readout_command),
    )
    _write_text(docs_root / "artifact_index.md", _artifact_index(paths=paths))
    _write_text(docs_root / "glossary.md", _glossary())
    _write_text(
        docs_root / "result_readout.md",
        _result_readout(pair_rows=pair_rows, delta_rows=delta_rows, arm_rows=arm_rows),
    )
    _write_text(results_dir / "summary.md", _results_summary(pair_rows, delta_rows, arm_rows))
    _write_text(results_dir / "human_summary.md", _human_summary(status, delta_rows))
    _write_text(results_dir / "paired_replicate_readout.md", _pair_table(pair_rows))
    _write_text(results_dir / "margin_distribution_readout.md", _margin_table(margin_rows))
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
        "results/paired_replicate_readout.md": str(results_dir / "paired_replicate_readout.md"),
        "results/margin_distribution_readout.md": str(
            results_dir / "margin_distribution_readout.md"
        ),
        "results/timing_readout.md": str(results_dir / "timing_readout.md"),
    }


def _readme(
    *,
    badges: list[str],
    status: str,
    artifact_root: Path,
    budget: dict[str, object],
    threshold_policy: dict[str, object],
    pair_rows: list[dict[str, str]],
    delta_rows: list[dict[str, str]],
    arm_rows: list[dict[str, str]],
    hit_rate_rows: list[dict[str, str]],
    seed_rows: list[dict[str, str]],
    lift_failure_count: int,
    readout_command: str,
    turn_section: str,
) -> str:
    unblocked_pair_count = sum(
        row.get("claim_blocked") in {"False", "false", "0"} for row in pair_rows
    )
    return (
        "# Counterpoint Small Paired Replicate Probe\n\n" + "\n".join(badges) + "\n\n"
        "This repository directory is the human-readable readout surface for the "
        "small paired replicate probe. The probe repeats the corrected Schema 0 "
        "versus Schema 1 comparison across matched seed bundles for one selected "
        "candidate and one locked threshold.\n\n"
        "## Status At A Glance\n\n"
        f"- Artifact evidence: `{status}`.\n"
        f"- Run mode: `{budget.get('run_mode', '')}`.\n"
        f"- Instance: `{budget.get('environment_instance_id', '')}`.\n"
        f"- Threshold value: `{threshold_policy.get('threshold_value', None)}`.\n"
        f"- Threshold source: `{threshold_policy.get('threshold_source_type', '')}`.\n"
        f"- Pair rows: `{len(pair_rows)}`.\n"
        f"- Unblocked pairs: `{unblocked_pair_count}`.\n"
        f"- Lift failure rows: `{lift_failure_count}`.\n\n"
        "## Liftability And Invariant Semantics\n\n"
        f"- Liftability semantics: `{STATE_COLLAPSER_V072_POINTWISE_LIFTABILITY_SEMANTICS_ID}`.\n"
        "- Runtime action availability is pointwise: an abstract action must "
        "have a concrete lift executable from the current base state.\n\n"
        "## Summary of Goals Behind this Evaluation\n\n"
        "The goal is to see whether Schema 1's small post-hit reward-margin "
        "signal survives across matched seed bundles. This is a next-measure "
        "probe, not a final serious comparison or statistical significance test.\n\n"
        "## Summary of Methodology Behind this Evaluation\n\n"
        "For each selected corrected Schema 1 candidate, the runner creates "
        "matched Schema 0 and Schema 1 arm runs for each seed bundle. Pair-level "
        "tables join the two arm runs by `candidate_group_id`, `seed_bundle_id`, "
        "and `training_replicate_index`.\n\n"
        "## Pair Distribution\n\n"
        f"{_delta_table(delta_rows)}\n\n"
        "## Pair-Level Rows\n\n"
        f"{_pair_table(pair_rows)}\n\n"
        "## Schema-Arm Distribution\n\n"
        f"{_arm_table(arm_rows)}\n\n"
        "## Sustained-Hit Rate Rows\n\n"
        f"{_hit_rate_table(hit_rate_rows)}\n\n"
        "## Seed Bundle Evidence\n\n"
        f"{_seed_table(seed_rows)}\n\n"
        "## Claim Boundary\n\n"
        "This readout may support only a bounded single-candidate paired-seed "
        "pattern under the locked threshold. It may not claim broad abstraction "
        "superiority, statistical significance, tensor-enabled behavior, or "
        "musical quality.\n\n"
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
    threshold_policy: dict[str, object],
) -> str:
    return (
        "# Method\n\n"
        "This evaluation reuses the corrected second-serious per-arm tower-control "
        "runtime while giving the run a paired-replicate-specific evaluation "
        "identity and result surface.\n\n"
        f"The run uses `{STATE_COLLAPSER_V072_POINTWISE_LIFTABILITY_SEMANTICS_ID}` "
        "semantics. Schema 0 and Schema 1 are paired by seed bundle for each "
        "training replicate.\n\n"
        "Threshold policy:\n\n"
        "```json\n"
        f"{json.dumps(threshold_policy, indent=2, sort_keys=True)}\n"
        "```\n\n"
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
        f"- Replicate policy: `{paths.replicate_probe_policy_manifest}`\n"
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
        "- Schema 1: selected noisy-rate quotient candidate using full-iterated "
        "tower construction.\n"
        "- Seed bundle: the shared random-seed identity used by both schema arms "
        "inside a pair.\n"
        "- Post-hit margin: reward above or below the locked threshold inside the "
        "first sustained-hit window.\n"
        "- Claim-blocked pair: a pair that cannot support comparison because one "
        "arm failed, missed sustained hit, or has incomplete artifacts.\n"
    )


def _result_readout(
    *,
    pair_rows: list[dict[str, str]],
    delta_rows: list[dict[str, str]],
    arm_rows: list[dict[str, str]],
) -> str:
    return (
        "# Result Readout\n\n"
        "## Paired Delta Distribution\n\n"
        f"{_delta_table(delta_rows)}\n\n"
        "## Pair Rows\n\n"
        f"{_pair_table(pair_rows)}\n\n"
        "## Arm Rows\n\n"
        f"{_arm_table(arm_rows)}\n"
    )


def _results_summary(
    pair_rows: list[dict[str, str]],
    delta_rows: list[dict[str, str]],
    arm_rows: list[dict[str, str]],
) -> str:
    return (
        "# Results Summary\n\n"
        f"- Pair rows: `{len(pair_rows)}`.\n"
        f"- Distribution rows: `{len(delta_rows)}`.\n"
        f"- Arm rows: `{len(arm_rows)}`.\n"
        f"- Pair statuses: `{_counts(pair_rows, 'pair_status')}`.\n"
    )


def _human_summary(status: str, delta_rows: list[dict[str, str]]) -> str:
    claim = (
        delta_rows[0].get("bounded_claim_text", "No bounded claim row available.")
        if delta_rows
        else "No bounded claim row available."
    )
    return f"# Human Summary\n\nThe artifact set is `{status}`. {claim}\n"


def _timing_readout(*, paths) -> str:
    return (
        "# Timing Readout\n\n"
        "Evaluation-level timing summary rows are in:\n\n"
        "```text\n"
        f"{paths.results_dir / 'timing_summary.csv'}\n"
        "```\n"
    )


def _pair_table(rows: list[dict[str, str]]) -> str:
    return _markdown_table(
        ["Candidate Group", "Seed", "Rep", "Pair Status", "Mean Delta", "Blocked"],
        [
            [
                row.get("candidate_group_id", ""),
                row.get("seed_bundle_id", ""),
                row.get("training_replicate_index", ""),
                row.get("pair_status", ""),
                row.get("schema1_minus_schema0_post_hit_window_mean", ""),
                row.get("claim_blocked", ""),
            ]
            for row in rows
        ],
    )


def _delta_table(rows: list[dict[str, str]]) -> str:
    return _markdown_table(
        ["Candidate Group", "Pairs", "Unblocked", "Margin Wins", "Margin Losses", "Claim"],
        [
            [
                row.get("candidate_group_id", ""),
                row.get("pair_count", ""),
                row.get("unblocked_pair_count", ""),
                row.get("schema1_margin_win_count", ""),
                row.get("schema1_margin_loss_count", ""),
                row.get("claim_status", ""),
            ]
            for row in rows
        ],
    )


def _arm_table(rows: list[dict[str, str]]) -> str:
    return _markdown_table(
        ["Schema", "Runs", "Sustained", "Rate", "Median Episodes", "Median Mean"],
        [
            [
                row.get("schema_class_id", ""),
                row.get("run_count", ""),
                row.get("sustained_hit_count", ""),
                row.get("sustained_hit_rate", ""),
                row.get("median_episodes_to_sustained_hit", ""),
                row.get("median_post_hit_window_mean", ""),
            ]
            for row in rows
        ],
    )


def _hit_rate_table(rows: list[dict[str, str]]) -> str:
    return _markdown_table(
        ["Schema", "Run Count", "Sustained", "Rate", "Schema1 - Schema0"],
        [
            [
                row.get("schema_class_id", ""),
                row.get("run_count", ""),
                row.get("sustained_hit_count", ""),
                row.get("sustained_hit_rate", ""),
                row.get("schema1_minus_schema0_sustained_hit_rate", ""),
            ]
            for row in rows
        ],
    )


def _seed_table(rows: list[dict[str, str]]) -> str:
    return _markdown_table(
        ["Candidate Group", "Seed", "Rep", "Schema0 Run", "Schema1 Run", "Status"],
        [
            [
                row.get("candidate_group_id", ""),
                row.get("seed_bundle_id", ""),
                row.get("training_replicate_index", ""),
                row.get("schema0_run_id", ""),
                row.get("schema1_run_id", ""),
                row.get("pair_status", ""),
            ]
            for row in rows
        ],
    )


def _margin_table(rows: list[dict[str, str]]) -> str:
    return _markdown_table(
        ["Seed", "Schema", "Mean", "Mean Margin", "Pair Mean Delta"],
        [
            [
                row.get("seed_bundle_id", ""),
                row.get("schema_class_id", ""),
                row.get("post_hit_window_mean", ""),
                row.get("threshold_margin_mean", ""),
                row.get("schema1_minus_schema0_post_hit_window_mean", ""),
            ]
            for row in rows
        ],
    )


def _write_badges(
    docs_root: Path,
    *,
    status: str,
    pair_count: int,
    unblocked_pairs: int,
    margin_wins: int,
    hit_rate_delta: str,
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
        ("pair_count.svg", "Pairs", str(pair_count), "#1565c0"),
        (
            "unblocked_pairs.svg",
            "Unblocked",
            f"{unblocked_pairs}/{pair_count}",
            "#2e7d32" if unblocked_pairs == pair_count and pair_count else "#ef6c00",
        ),
        (
            "schema1_margin_wins.svg",
            "S1 Margin Wins",
            str(margin_wins),
            "#2e7d32" if margin_wins else "#ef6c00",
        ),
        ("hit_rate_delta.svg", "Hit Rate Delta", hit_rate_delta, "#1565c0"),
        ("liftability_semantics.svg", "Liftability", "Pointwise v0.7.2", "#2e7d32"),
        (
            "lift_failures.svg",
            "Lift Failures",
            str(lift_failure_count),
            "#2e7d32" if lift_failure_count == 0 else "#ef6c00",
        ),
        ("provenance_repo_artifacts.svg", "Provenance", "Repo Artifacts", "#1565c0"),
    ]
    links = []
    for filename, label, value, color in specs:
        _write_text(badges_dir / filename, _badge_svg(label, value, color))
        links.append(f"![{label}: {value}](badges/{filename})")
    return links


def _badge_svg(label: str, value: str, color: str) -> str:
    label_width = max(74, 7 * len(label) + 12)
    value_width = max(74, 7 * len(value) + 12)
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


def _counts(rows: list[dict[str, str]], field: str) -> dict[str, int]:
    counts: dict[str, int] = {}
    for row in rows:
        value = row.get(field, "")
        counts[value] = counts.get(value, 0) + 1
    return counts


def _first_int(rows: list[dict[str, str]], field: str) -> int:
    if not rows:
        return 0
    value = rows[0].get(field)
    return int(float(value)) if value not in (None, "") else 0


def _hit_rate_delta(rows: list[dict[str, str]]) -> str:
    if not rows:
        return "n/a"
    value = rows[0].get("schema1_minus_schema0_sustained_hit_rate")
    return "n/a" if value in (None, "") else str(value)


def _lift_failure_count(rows: list[dict[str, str]]) -> int:
    return sum(int(float(row.get("event_count") or 0)) for row in rows)


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
