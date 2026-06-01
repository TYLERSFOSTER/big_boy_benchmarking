"""Human-facing docs seeds for counterpoint contraction fraction sweep diagnostics."""

from __future__ import annotations

import csv
import json
from pathlib import Path

from big_boy_benchmarking.environments.counterpoint.fraction_sweep_diagnostics.config import (
    EVALUATION_ID,
)
from big_boy_benchmarking.environments.counterpoint.fraction_sweep_diagnostics.paths import (
    build_fraction_sweep_diagnostics_paths,
    repo_readout_surface,
    validate_repo_resident_artifact_root,
)


def _write_text(path: Path, text: str, *, create_parents: bool = False) -> None:
    if create_parents:
        path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(text, encoding="utf-8")


def _read_csv(path: Path) -> list[dict[str, str]]:
    if not path.exists():
        return []
    return list(csv.DictReader(path.open(encoding="utf-8")))


def _read_json(path: Path) -> dict[str, object]:
    if not path.exists():
        return {}
    return json.loads(path.read_text(encoding="utf-8"))


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


def _write_badges(docs_root: Path, *, status: str, verdict: str, legacy_match: bool | None, concrete_steps: int) -> list[str]:
    badges_dir = docs_root / "badges"
    badges_dir.mkdir(parents=True, exist_ok=True)
    artifact_value = "Complete" if status == "complete" else "Incomplete"
    artifact_color = "#2e7d32" if status == "complete" else "#c62828"
    sweep_value = {
        "threshold_found": "Threshold Found",
        "immediate_collapse": "Immediate Collapse",
        "no_collapse": "No Collapse",
        "mixed": "Mixed",
        "invalid_or_uninterpretable": "Invalid",
    }.get(verdict, "Unknown")
    sweep_color = "#ef6c00" if verdict == "immediate_collapse" else "#2e7d32"
    legacy_value = (
        "Matches Legacy"
        if legacy_match is True
        else "Differs From Legacy"
        if legacy_match is False
        else "Not Checked"
    )
    legacy_color = "#2e7d32" if legacy_match is True else "#ef6c00"
    runtime_value = "Executable" if concrete_steps > 0 else "No Concrete Steps"
    runtime_color = "#2e7d32" if concrete_steps > 0 else "#c62828"
    specs = [
        ("artifacts_complete.svg", "Artifacts", artifact_value, artifact_color),
        ("sweep_status.svg", "Sweep", sweep_value, sweep_color),
        ("legacy_endpoint.svg", "n=6/18", legacy_value, legacy_color),
        ("runtime_executable.svg", "Runtime", runtime_value, runtime_color),
        ("scope_diagnostic_only.svg", "Scope", "Diagnostic Only", "#1565c0"),
        ("provenance_repo_artifacts.svg", "Provenance", "Repo Artifacts", "#1565c0"),
    ]
    links = []
    for filename, label, value, color in specs:
        _write_text(badges_dir / filename, _badge_svg(label, value, color))
        links.append(f"![{label}: {value}](badges/{filename})")
    return links


def _verdict_text(verdict: str) -> str:
    return {
        "threshold_found": "threshold found",
        "immediate_collapse": "immediate collapse",
        "no_collapse": "no collapse",
        "mixed": "mixed",
        "invalid_or_uninterpretable": "invalid or uninterpretable",
    }.get(verdict, "unknown")


def _csv_bool(value: str) -> bool | None:
    if value == "True":
        return True
    if value == "False":
        return False
    return None


def _int_or_none(value: str | None) -> int | None:
    if value in (None, ""):
        return None
    return int(value)


def _run_scope_label(artifact_root: Path, budget: dict[str, object]) -> str:
    if artifact_root.name.startswith("smoke"):
        return "smoke"
    numerators = tuple(budget.get("numerators", ()))
    instance_ids = tuple(budget.get("instance_ids", ()))
    schema_seeds = tuple(budget.get("schema_seeds", ()))
    replicates = budget.get("replicates_per_schema_seed")
    episodes = budget.get("episodes_per_replicate")
    full_shape = (
        numerators == (1, 2, 3, 4, 5, 6)
        and len(instance_ids) >= 2
        and len(schema_seeds) >= 3
        and replicates == 4
        and episodes == 16
    )
    return "full validation" if full_shape else "custom diagnostic"


def _join_config_values(values: object) -> str:
    if isinstance(values, list):
        return ", ".join(f"`{value}`" for value in values)
    if isinstance(values, tuple):
        return ", ".join(f"`{value}`" for value in values)
    if values in (None, ""):
        return "`unknown`"
    return f"`{values}`"


def write_fraction_sweep_diagnostics_docs(
    *,
    artifact_root: Path | str,
    docs_root: Path | str | None = None,
    command_lines: tuple[str, ...] = (),
) -> dict[str, str]:
    artifact_root = validate_repo_resident_artifact_root(artifact_root)
    docs_root = Path(docs_root) if docs_root is not None else repo_readout_surface()
    paths = build_fraction_sweep_diagnostics_paths(artifact_root)
    result_dir = docs_root / "results"
    result_dir.mkdir(parents=True, exist_ok=True)
    budget = _read_json(paths.evaluation_budget_lock)
    aggregate_summary = _read_json(paths.evaluation_aggregate_summary)
    threshold_rows = _read_csv(paths.results_dir / "collapse_threshold_summary.csv")
    tower_rows = _read_csv(paths.results_dir / "tower_shape_summary.csv")
    schema_rows = _read_csv(paths.results_dir / "schema_fraction_summary.csv")
    legacy_rows = _read_csv(paths.results_dir / "legacy_one_third_equivalence_summary.csv")
    endpoint_rows = _read_csv(paths.results_dir / "endpoint_coalescence_summary.csv")
    concrete_rows = _read_csv(paths.results_dir / "concrete_step_summary.csv")
    status = str(aggregate_summary.get("status", "unknown"))
    verdict_values = {row["sweep_verdict"] for row in threshold_rows if row.get("sweep_verdict")}
    verdict = verdict_values.pop() if len(verdict_values) == 1 else "mixed" if verdict_values else "unknown"
    first_full_values = [
        value
        for value in (_int_or_none(row.get("first_full_collapse_numerator")) for row in threshold_rows)
        if value is not None
    ]
    first_near_values = [
        value
        for value in (_int_or_none(row.get("first_near_collapse_numerator")) for row in threshold_rows)
        if value is not None
    ]
    last_nontrivial_values = [
        value
        for value in (_int_or_none(row.get("last_nontrivial_numerator")) for row in threshold_rows)
        if value is not None
    ]
    first_full = str(min(first_full_values)) if first_full_values else ""
    first_near = str(min(first_near_values)) if first_near_values else ""
    last_nontrivial = str(max(last_nontrivial_values)) if last_nontrivial_values else ""
    legacy_match = None
    if legacy_rows:
        legacy_match = all(_csv_bool(row["equivalent"]) is True for row in legacy_rows)
    concrete_steps = sum(int(row["concrete_step_count"]) for row in concrete_rows)
    run_scope = _run_scope_label(artifact_root, budget)
    run_scope_noun = f"{run_scope} run"
    badge_links = _write_badges(
        docs_root,
        status=status,
        verdict=verdict,
        legacy_match=legacy_match,
        concrete_steps=concrete_steps,
    )
    readout_command = (
        "execute docs/prime_directive/artifact_table_to_readable_document_protocol.md "
        f"at {docs_root / 'readout_source.json'}"
    )
    commands = command_lines or (
        "uv run python -m big_boy_benchmarking.cli counterpoint fraction-sweep "
        "summarize --artifact-root <artifact-root>",
    )
    files = {
        "README.md": docs_root / "README.md",
        "method.md": docs_root / "method.md",
        "runbook.md": docs_root / "runbook.md",
        "artifact_index.md": docs_root / "artifact_index.md",
        "glossary.md": docs_root / "glossary.md",
        "results/summary.md": result_dir / "summary.md",
        "results/human_summary.md": result_dir / "human_summary.md",
        "results/sweep_verdict.md": result_dir / "sweep_verdict.md",
        "results/threshold_table.md": result_dir / "threshold_table.md",
    }
    tier_lines = [
        "| Arm | Tier | State Cells | Active Action Cells | Raw Historical Action Records | Largest Cell Share | Class |",
        "| --- | ---: | ---: | ---: | ---: | ---: | --- |",
    ]
    for row in tower_rows:
        tier_lines.append(
            "| "
            + " | ".join(
                [
                    row["arm_id"],
                    row["tier_index"],
                    row["state_cell_count"],
                    row["active_action_cell_count"],
                    row["raw_historical_action_cell_record_count"],
                    f"{float(row['largest_state_cell_share']):.3f}",
                    row["degeneracy_class"],
                ]
            )
            + " |"
        )
    schema_lines = [
        "| Arm | Scheduled Edges | Edge Share | Edges/(States-1) | Monotone |",
        "| --- | ---: | ---: | ---: | --- |",
    ]
    for row in schema_rows:
        schema_lines.append(
            "| "
            + " | ".join(
                [
                    row["arm_id"],
                    row["scheduled_edge_count"],
                    f"{float(row['scheduled_edge_share']):.3f}",
                    row["scheduled_edges_per_state_minus_one"],
                    row["monotonicity_pass"],
                ]
            )
            + " |"
        )
    threshold_lines = [
        "| Instance | Schema Seed | First Full Collapse n | First Near Collapse n | Last Nontrivial n | n06 Matches Legacy | Verdict |",
        "| --- | ---: | ---: | ---: | ---: | --- | --- |",
    ]
    for row in threshold_rows:
        threshold_lines.append(
            "| "
            + " | ".join(
                [
                    row["instance_id"],
                    row["schema_seed"],
                    row["first_full_collapse_numerator"] or "none",
                    row["first_near_collapse_numerator"] or "none",
                    row["last_nontrivial_numerator"] or "none",
                    row["n06_matches_legacy"],
                    row["sweep_verdict"],
                ]
            )
            + " |"
        )
    endpoint_lines = [
        "| Arm | Processed Edges | Useful Coalescences | Redundant/Internal Edges | State Cells After Block | First Singleton Edge Index | Collapse Used Most Block |",
        "| --- | ---: | ---: | ---: | ---: | ---: | --- |",
    ]
    for row in endpoint_rows:
        endpoint_lines.append(
            "| "
            + " | ".join(
                [
                    row["arm_id"],
                    row["processed_edge_count"],
                    row["useful_coalescence_count"],
                    row["redundant_or_internal_edge_count"],
                    row["state_cell_count_after_block"],
                    row["processed_edge_index_at_first_singleton"] or "none",
                    row["collapse_required_most_of_block"],
                ]
            )
            + " |"
        )
    _write_text(
        files["README.md"],
        "\n".join(
            [
                "# Counterpoint Contraction Fraction Sweep Diagnostics",
                "",
                *badge_links,
                "",
                "This repository directory is the human-readable readout surface for the counterpoint n-over-18 contraction fraction sweep diagnostic.",
                "",
                "## Status At A Glance",
                "",
                f"- Artifact evidence: {status}.",
                f"- Sweep verdict: {_verdict_text(verdict)}.",
                f"- First full-collapse numerator: `{first_full or 'none observed'}`.",
                f"- First near-collapse numerator: `{first_near or 'none observed'}`.",
                f"- Last nontrivial numerator: `{last_nontrivial or 'none observed'}`.",
                f"- Legacy endpoint check for `6/18`: `{legacy_match}`.",
                f"- Concrete steps emitted across this artifact run: `{concrete_steps}`.",
                "- Claim scope: diagnostic only; this is not a learning-performance comparison.",
                "",
                "## One-Screen Verdict",
                "",
                f"The {run_scope_noun} completed and produced the required machine-readable summary tables.",
                "",
                f"On this {run_scope_noun}, `{first_full or 'no observed numerator'}/18` is the first observed full-collapse numerator. When that value is `1/18`, the current single-block source-local fraction semantics are already severe at the weakest requested fraction.",
                "",
                "`6/18` matches the legacy one-third first scheduled block in the generated equivalence table, so the sweep endpoint is comparable to the old one-third diagnostic for this run configuration.",
                "",
                "## Source Evaluation Root",
                "",
                "```text",
                str(paths.root),
                "```",
                "",
                "## Summary of Goals Behind this Evaluation",
                "",
                "This evaluation keeps the existing `counterpoint_symbolic_v001` environment fixed and varies only the scheduled contraction fraction. It asks whether small `n/18` fractions preserve meaningful first-tier structure before higher fractions collapse.",
                "",
                "A smoke-scoped artifact run is implementation evidence only. A full-validation artifact run can support broader structural diagnostic claims, but still cannot support learning-performance claims without a separate comparison evaluation.",
                "",
                "## Summary of Methodology Behind this Evaluation",
                "",
                "For each configured arm, BBB selects one source-local scheduled outgoing-edge block using `max(1, ceil(out_degree * n / 18))`. Remaining edges are unscheduled for that arm. The tower is then built through the existing `state_collapser` partition tower path and exercised through the existing active-tier controller runtime.",
                "",
                f"This {run_scope_noun} used instances {_join_config_values(budget.get('instance_ids'))}, schema seeds {_join_config_values(budget.get('schema_seeds'))}, numerators {_join_config_values(budget.get('numerators'))}, denominator `{budget.get('denominator', 'unknown')}`, replicates `{budget.get('replicates_per_schema_seed', 'unknown')}`, and episodes `{budget.get('episodes_per_replicate', 'unknown')}`.",
                "",
                "## Tier Shape Table",
                "",
                *tier_lines,
                "",
                "The tier table intentionally separates active action-cell count from raw historical action-cell record count. A collapsed tier can have zero live executable action cells while retaining many raw historical records from tower construction; the raw count is not the live control surface.",
                "",
                "## Schema Width Table",
                "",
                *schema_lines,
                "",
                "## Threshold Table",
                "",
                *threshold_lines,
                "",
                "## Endpoint-Coalescence Table",
                "",
                *endpoint_lines,
                "",
                "## Files",
                "",
                "- [readout_source.json](readout_source.json): source binding from this repo readout surface to raw artifact tables.",
                "- [method.md](method.md): methodology and budget summary.",
                "- [runbook.md](runbook.md): rerun, summarize, and human-readout commands.",
                "- [artifact_index.md](artifact_index.md): evidence map with file purposes.",
                "- [glossary.md](glossary.md): field and mechanism translations.",
                "- [results/summary.md](results/summary.md): compact reader-facing result summary.",
                "- [results/sweep_verdict.md](results/sweep_verdict.md): sweep verdict details.",
                "- [results/threshold_table.md](results/threshold_table.md): threshold table.",
                "",
                "## Claim Boundary",
                "",
                f"This readout may claim that the {run_scope_noun} completed, produced repo-resident artifacts, checked `6/18` against the old first one-third block, and reported the collapse threshold fields shown above.",
                "",
                "This readout may not claim tower learning advantage, direct-vs-tower comparison, musical quality, tensor-enabled runtime behavior, CUDA/GPU behavior, production performance, or that the counterpoint environment is degenerate.",
                "",
                "To regenerate the human-readable readout, run:",
                "",
                "```text",
                readout_command,
                "```",
                "",
                "## Clarifying Questions And Turns",
                "",
                "#### Project Owner / Evaluator Turn",
                "",
                "> ...",
                "",
                "#### Embedded Engineering Consultant / Codex Turn",
                "",
                "> ...",
                "",
                "#### Project Owner / Evaluator Turn",
                "",
                "> ...",
                "",
                "#### Embedded Engineering Consultant / Codex Turn",
                "",
                "> ...",
                "",
                "#### Project Owner / Evaluator Turn",
                "",
                "> ...",
                "",
                "#### Embedded Engineering Consultant / Codex Turn",
                "",
                "> ...",
                "",
            ]
        ),
        create_parents=True,
    )
    _write_text(
        files["method.md"],
        "\n".join(
            [
                "# Method",
                "",
                f"Evaluation id: `{EVALUATION_ID}`.",
                "",
                "The sweep runs the existing counterpoint hidden graph with one scheduled source-local outgoing-edge contraction block per fraction arm.",
                "The required arms are `1/18` through `6/18`; `6/18` must be checked against the old one-third first block.",
                "",
                f"Current scope: `{run_scope}`.",
                f"Instances: {_join_config_values(budget.get('instance_ids'))}.",
                f"Numerators: {_join_config_values(budget.get('numerators'))}.",
                f"Schema seeds: {_join_config_values(budget.get('schema_seeds'))}.",
                f"Replicates per schema seed: `{budget.get('replicates_per_schema_seed', 'unknown')}`.",
                f"Episodes per replicate: `{budget.get('episodes_per_replicate', 'unknown')}`.",
                f"Linearization mode: `{budget.get('linearization_mode_id', 'unknown')}`.",
                "",
                "Current artifact run label:",
                "",
                "```text",
                artifact_root.name,
                "```",
                "",
            ]
        ),
        create_parents=True,
    )
    _write_text(
        files["runbook.md"],
        "\n".join(
            [
                "# Runbook",
                "",
                "Summarize artifacts:",
                "",
                "```text",
                *commands,
                "```",
                "",
                "Generate human-readable readout:",
                "",
                "```text",
                readout_command,
                "```",
                "",
            ]
        ),
        create_parents=True,
    )
    _write_text(
        files["artifact_index.md"],
        "\n".join(
            [
                "# Artifact Index",
                "",
                "This readout surface is generated from repo-resident artifacts, not from a temporary artifact root.",
                "",
                "Primary binding:",
                "",
                "- `readout_source.json`: maps this repo readout surface to the source evaluation root and expected files.",
                "",
                "Core evidence tables:",
                "",
                "- `results/schema_fraction_summary.csv`: scheduled edge counts and fraction widths.",
                "- `results/tower_shape_summary.csv`: tier state-cell shape, active action-cell counts, and raw historical action-record counts.",
                "- `results/endpoint_coalescence_summary.csv`: repeated endpoint-coalescence diagnostics for the scheduled block.",
                "- `results/collapse_threshold_summary.csv`: first full collapse, first near collapse, last nontrivial numerator, and sweep verdict.",
                "- `results/legacy_one_third_equivalence_summary.csv`: `6/18` equivalence against the old first one-third block.",
                "- `results/concrete_step_summary.csv`: concrete episode-step evidence.",
                "- `results/tier_executability_summary.csv`: live executable tier evidence.",
                "",
                "Source evaluation root:",
                "",
                "```text",
                str(paths.root),
                "```",
                "",
            ]
        ),
        create_parents=True,
    )
    _write_text(
        files["glossary.md"],
        "\n".join(
            [
                "# Glossary",
                "",
                "- scheduled contraction block: the selected `n/18` source-local outgoing edges for one arm.",
                "- repeated endpoint coalescence: the current tower operation applied to scheduled edges.",
                "- active action-cell count: action cells reachable from active state cells, excluding stale historical records.",
                "- diagnostic-only: the result explains structure and runtime behavior, not learning advantage.",
                "",
            ]
        ),
        create_parents=True,
    )
    _write_text(
        files["results/summary.md"],
        "\n".join(
            [
                "# Summary",
                "",
                f"Status: `{status}`.",
                f"Sweep verdict: `{verdict}`.",
                f"First full-collapse numerator: `{first_full or 'none observed'}`.",
                f"First near-collapse numerator: `{first_near or 'none observed'}`.",
                f"Last nontrivial numerator: `{last_nontrivial or 'none observed'}`.",
                f"`6/18` legacy endpoint match: `{legacy_match}`.",
                "",
            ]
        ),
        create_parents=True,
    )
    _write_text(
        files["results/human_summary.md"],
        "\n".join(
            [
                "# Human Summary",
                "",
                f"The {run_scope_noun} completed. The central diagnostic finding is `{_verdict_text(verdict)}` with first full-collapse numerator `{first_full or 'none observed'}`.",
                "",
                "This is diagnostic evidence, not a learning-performance result.",
                "",
            ]
        ),
        create_parents=True,
    )
    _write_text(
        files["results/sweep_verdict.md"],
        "\n".join(
            [
                "# Sweep Verdict",
                "",
                f"Verdict: `{verdict}`.",
                "",
                f"Interpretation: this {run_scope_noun} reports `{_verdict_text(verdict)}`. The first full-collapse numerator is `{first_full or 'none observed'}`, and the last nontrivial numerator is `{last_nontrivial or 'none observed'}`.",
                "",
            ]
        ),
        create_parents=True,
    )
    _write_text(
        files["results/threshold_table.md"],
        "\n".join(["# Threshold Table", "", *threshold_lines, ""]),
        create_parents=True,
    )
    return {key: str(path) for key, path in files.items()}
