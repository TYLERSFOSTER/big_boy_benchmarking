"""Human-facing docs seeds for counterpoint noisy-rate contraction diagnostics."""

from __future__ import annotations

import csv
import json
from pathlib import Path

from big_boy_benchmarking.environments.counterpoint.noisy_rate_diagnostics.config import (
    DEFAULT_RATES,
    EVALUATION_ID,
    SMOKE_RATES,
)
from big_boy_benchmarking.environments.counterpoint.noisy_rate_diagnostics.paths import (
    build_noisy_rate_diagnostics_paths,
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


def _write_badges(
    docs_root: Path,
    *,
    status: str,
    verdict: str,
    min_selected_source_share: float | None,
    concrete_steps: int,
    consistency_ok: bool | None,
) -> list[str]:
    badges_dir = docs_root / "badges"
    badges_dir.mkdir(parents=True, exist_ok=True)
    artifact_value = "Complete" if status == "complete" else "Incomplete"
    artifact_color = "#2e7d32" if status == "complete" else "#c62828"
    sweep_value = {
        "no_collapse": "No Collapse",
        "low_rate_immediate_collapse": "Low-Rate Collapse",
        "coverage_threshold_found": "Coverage Threshold",
        "edge_rate_threshold_found": "Edge-Rate Threshold",
        "mixed_by_seed": "Mixed",
        "invalid_or_uninterpretable": "Invalid",
    }.get(verdict, "Unknown")
    sweep_color = "#c62828" if verdict == "invalid_or_uninterpretable" else "#ef6c00" if "collapse" in verdict else "#2e7d32"
    coverage_value = (
        "Unknown"
        if min_selected_source_share is None
        else f"Min {min_selected_source_share:.2f}"
    )
    coverage_color = "#2e7d32" if (min_selected_source_share or 0.0) > 0.0 else "#ef6c00"
    consistency_value = (
        "Consistent"
        if consistency_ok is True
        else "Mismatch"
        if consistency_ok is False
        else "Unknown"
    )
    consistency_color = "#2e7d32" if consistency_ok is True else "#c62828"
    runtime_value = "Executable" if concrete_steps > 0 else "No Concrete Steps"
    runtime_color = "#2e7d32" if concrete_steps > 0 else "#c62828"
    specs = [
        ("artifacts_complete.svg", "Artifacts", artifact_value, artifact_color),
        ("noisy_rate_sweep.svg", "Sweep", sweep_value, sweep_color),
        ("source_coverage.svg", "Coverage", coverage_value, coverage_color),
        ("selection_contract.svg", "Selection", consistency_value, consistency_color),
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
        "no_collapse": "no observed full collapse",
        "low_rate_immediate_collapse": "full collapse at the lowest requested noisy rate",
        "coverage_threshold_found": "collapse at or after high source coverage",
        "edge_rate_threshold_found": "collapse at a higher requested edge rate",
        "mixed_by_seed": "mixed by seed",
        "invalid_or_uninterpretable": "invalid or uninterpretable",
    }.get(verdict, "unknown")


def _int_or_none(value: str | None) -> int | None:
    if value in (None, ""):
        return None
    return int(value)


def _float_or_none(value: str | None) -> float | None:
    if value in (None, ""):
        return None
    return float(value)


def _csv_bool(value: str) -> bool | None:
    if value == "True":
        return True
    if value == "False":
        return False
    return None


def _run_scope_label(artifact_root: Path, budget: dict[str, object]) -> str:
    if artifact_root.name.startswith("smoke"):
        return "smoke"
    rates = tuple(
        (int(rate["numerator"]), int(rate["denominator"]))
        for rate in budget.get("rates", [])
        if isinstance(rate, dict)
    )
    instance_ids = tuple(budget.get("instance_ids", ()))
    schema_seeds = tuple(budget.get("schema_seeds", ()))
    replicates = budget.get("replicates_per_schema_seed")
    episodes = budget.get("episodes_per_replicate")
    full_shape = (
        rates == DEFAULT_RATES
        and len(instance_ids) >= 2
        and len(schema_seeds) >= 32
        and replicates == 4
        and episodes == 16
    )
    smoke_shape = rates == SMOKE_RATES and replicates == 1 and episodes == 1
    if full_shape:
        return "full validation"
    if smoke_shape:
        return "smoke"
    return "custom diagnostic"


def _join_config_values(values: object) -> str:
    if isinstance(values, list):
        return ", ".join(f"`{value}`" for value in values)
    if isinstance(values, tuple):
        return ", ".join(f"`{value}`" for value in values)
    if values in (None, ""):
        return "`unknown`"
    return f"`{values}`"


def _join_rates(values: object) -> str:
    if not isinstance(values, list):
        return "`unknown`"
    parts = []
    for value in values:
        if not isinstance(value, dict):
            continue
        parts.append(f"`{value.get('numerator')}/{value.get('denominator')}`")
    return ", ".join(parts) if parts else "`unknown`"


def write_noisy_rate_diagnostics_docs(
    *,
    artifact_root: Path | str,
    docs_root: Path | str | None = None,
    command_lines: tuple[str, ...] = (),
) -> dict[str, str]:
    artifact_root = validate_repo_resident_artifact_root(artifact_root)
    docs_root = Path(docs_root) if docs_root is not None else repo_readout_surface()
    paths = build_noisy_rate_diagnostics_paths(artifact_root)
    result_dir = docs_root / "results"
    result_dir.mkdir(parents=True, exist_ok=True)
    budget = _read_json(paths.evaluation_budget_lock)
    aggregate_summary = _read_json(paths.evaluation_aggregate_summary)
    threshold_rows = _read_csv(paths.results_dir / "noisy_rate_threshold_summary.csv")
    tower_rows = _read_csv(paths.results_dir / "tower_shape_summary.csv")
    selection_rows = _read_csv(paths.results_dir / "noisy_rate_selection_summary.csv")
    coverage_rows = _read_csv(paths.results_dir / "noisy_rate_source_coverage_summary.csv")
    consistency_rows = _read_csv(
        paths.results_dir / "noisy_rate_selection_consistency_summary.csv"
    )
    endpoint_rows = _read_csv(paths.results_dir / "endpoint_coalescence_summary.csv")
    concrete_rows = _read_csv(paths.results_dir / "concrete_step_summary.csv")
    status = str(aggregate_summary.get("status", "unknown"))
    verdict_values = {row["sweep_verdict"] for row in threshold_rows if row.get("sweep_verdict")}
    verdict = verdict_values.pop() if len(verdict_values) == 1 else "mixed_by_seed" if verdict_values else "unknown"
    first_full_values = [
        value
        for value in (_float_or_none(row.get("first_full_collapse_rate")) for row in threshold_rows)
        if value is not None
    ]
    first_near_values = [
        value
        for value in (_float_or_none(row.get("first_near_collapse_rate")) for row in threshold_rows)
        if value is not None
    ]
    last_nontrivial_values = [
        value
        for value in (_float_or_none(row.get("last_nontrivial_rate")) for row in threshold_rows)
        if value is not None
    ]
    first_full = min(first_full_values) if first_full_values else None
    first_near = min(first_near_values) if first_near_values else None
    last_nontrivial = max(last_nontrivial_values) if last_nontrivial_values else None
    source_shares = []
    for row in coverage_rows:
        if row.get("arm_id") == "no_contraction_control":
            continue
        value = _float_or_none(row.get("selected_source_share"))
        if value is not None:
            source_shares.append(value)
    min_source_share = min(source_shares) if source_shares else None
    zero_source_counts = [
        _int_or_none(row.get("zero_selected_source_count")) or 0 for row in coverage_rows
    ]
    concrete_steps = sum(int(row["concrete_step_count"]) for row in concrete_rows)
    consistency_ok = None
    if consistency_rows:
        consistency_ok = all(
            _csv_bool(row["selection_sets_equal"]) is True for row in consistency_rows
        )
    run_scope = _run_scope_label(artifact_root, budget)
    run_scope_noun = f"{run_scope} run"
    badge_links = _write_badges(
        docs_root,
        status=status,
        verdict=verdict,
        min_selected_source_share=min_source_share,
        concrete_steps=concrete_steps,
        consistency_ok=consistency_ok,
    )
    readout_command = (
        "execute docs/prime_directive/artifact_table_to_readable_document_protocol.md "
        f"at {docs_root / 'readout_source.json'}"
    )
    commands = command_lines or (
        "uv run python -m big_boy_benchmarking.cli counterpoint noisy-rate "
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
        "results/noisy_rate_thresholds.md": result_dir / "noisy_rate_thresholds.md",
        "results/source_coverage.md": result_dir / "source_coverage.md",
    }
    tier_lines = [
        "| Arm | Rate | Tier | State Cells | Active Action Cells | Raw Historical Action Records | Largest Cell Share | Class |",
        "| --- | ---: | ---: | ---: | ---: | ---: | ---: | --- |",
    ]
    for row in tower_rows:
        tier_lines.append(
            "| "
            + " | ".join(
                [
                    row["arm_id"],
                    f"{float(row['requested_rate']):.5f}",
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
    selection_lines = [
        "| Arm | Requested Rate | Selected Edges | Edge Share | Expected Edges | Residual |",
        "| --- | ---: | ---: | ---: | ---: | ---: |",
    ]
    for row in selection_rows:
        selection_lines.append(
            "| "
            + " | ".join(
                [
                    row["arm_id"],
                    f"{float(row['requested_rate']):.5f}",
                    row["selected_edge_count"],
                    f"{float(row['realized_selected_edge_share']):.5f}",
                    f"{float(row['expected_selected_edge_count']):.2f}",
                    f"{float(row['selected_edge_count_residual_from_expectation']):.2f}",
                ]
            )
            + " |"
        )
    coverage_lines = [
        "| Arm | Rate | Selected Sources | Zero-Selected Sources | Selected Source Share | Class |",
        "| --- | ---: | ---: | ---: | ---: | --- |",
    ]
    for row in coverage_rows:
        coverage_lines.append(
            "| "
            + " | ".join(
                [
                    row["arm_id"],
                    f"{float(row['requested_rate']):.5f}",
                    row["source_count_with_selected_edges"],
                    row["zero_selected_source_count"],
                    "none"
                    if row["selected_source_share"] == ""
                    else f"{float(row['selected_source_share']):.3f}",
                    row["source_coverage_class"],
                ]
            )
            + " |"
        )
    threshold_lines = [
        "| Instance | Schema Seed | First Full Rate | First Near Rate | Last Nontrivial Rate | First High Coverage Rate | Verdict |",
        "| --- | ---: | ---: | ---: | ---: | ---: | --- |",
    ]
    for row in threshold_rows:
        threshold_lines.append(
            "| "
            + " | ".join(
                [
                    row["instance_id"],
                    row["schema_seed"],
                    row["first_full_collapse_rate"] or "none",
                    row["first_near_collapse_rate"] or "none",
                    row["last_nontrivial_rate"] or "none",
                    row["first_high_source_coverage_rate"] or "none",
                    row["sweep_verdict"],
                ]
            )
            + " |"
        )
    endpoint_lines = [
        "| Arm | Rate | Processed Edges | Useful Coalescences | State Cells After Block | Source Coverage | First Singleton Edge Index |",
        "| --- | ---: | ---: | ---: | ---: | ---: | ---: |",
    ]
    for row in endpoint_rows:
        endpoint_lines.append(
            "| "
            + " | ".join(
                [
                    row["arm_id"],
                    f"{float(row['requested_rate']):.5f}",
                    row["processed_edge_count"],
                    row["useful_coalescence_count"],
                    row["state_cell_count_after_block"],
                    row["realized_source_coverage"] or "none",
                    row["processed_edge_index_at_first_singleton"] or "none",
                ]
            )
            + " |"
        )
    _write_text(
        files["README.md"],
        "\n".join(
            [
                "# Counterpoint Noisy-Rate Contraction Diagnostics",
                "",
                *badge_links,
                "",
                "This repository directory is the human-readable readout surface for the counterpoint noisy-rate contraction diagnostic.",
                "",
                "## Status At A Glance",
                "",
                f"- Artifact evidence: {status}.",
                f"- Sweep verdict: {_verdict_text(verdict)}.",
                f"- First full-collapse requested rate: `{first_full if first_full is not None else 'none observed'}`.",
                f"- First near-collapse requested rate: `{first_near if first_near is not None else 'none observed'}`.",
                f"- Last nontrivial requested rate: `{last_nontrivial if last_nontrivial is not None else 'none observed'}`.",
                f"- Minimum selected-source share across non-control arms: `{min_source_share if min_source_share is not None else 'unknown'}`.",
                f"- Maximum zero-selected-source count in an arm: `{max(zero_source_counts) if zero_source_counts else 'unknown'}`.",
                f"- Metadata/runtime selected-edge consistency: `{consistency_ok}`.",
                f"- Concrete steps emitted across this artifact run: `{concrete_steps}`.",
                "- Claim scope: diagnostic only; this is not a learning-performance comparison.",
                "",
                "## One-Screen Verdict",
                "",
                f"The {run_scope_noun} completed and produced the required machine-readable noisy-rate summary tables.",
                "",
                "The key diagnostic distinction is expected edge rate versus realized source coverage. A low requested rate may select a small number of edges overall while leaving many source states with zero selected outgoing edges. That behavior is intentional here; it is the direct contrast with the earlier source-local floor rule.",
                "",
                f"On this {run_scope_noun}, the observed sweep verdict is `{verdict}`.",
                "",
                "## Source Evaluation Root",
                "",
                "```text",
                str(paths.root),
                "```",
                "",
                "## Summary of Goals Behind this Evaluation",
                "",
                "This evaluation keeps the existing `counterpoint_symbolic_v001` environment fixed and varies only the contraction selector. It asks whether an edge-global noisy expected-rate selector avoids the immediate-collapse behavior seen in the source-local fraction diagnostic.",
                "",
                "A smoke-scoped artifact run is implementation evidence only. A full-validation artifact run can support broader structural diagnostic claims, but still cannot support learning-performance claims without a separate comparison evaluation.",
                "",
                "## Summary of Methodology Behind this Evaluation",
                "",
                "For each configured arm, BBB assigns every canonical counterpoint edge a stable SHA-256 score using the selector rule id, instance id, schema seed, and edge key. An edge is scheduled when that score is below the requested rate. No source-local minimum-one floor is used, so sources can contribute zero selected outgoing edges.",
                "",
                f"This {run_scope_noun} used instances {_join_config_values(budget.get('instance_ids'))}, schema seeds {_join_config_values(budget.get('schema_seeds'))}, rates {_join_rates(budget.get('rates'))}, replicates `{budget.get('replicates_per_schema_seed', 'unknown')}`, and episodes `{budget.get('episodes_per_replicate', 'unknown')}`.",
                "",
                "## Selection Table",
                "",
                *selection_lines,
                "",
                "## Source Coverage Table",
                "",
                *coverage_lines,
                "",
                "## Tier Shape Table",
                "",
                *tier_lines,
                "",
                "The tier table intentionally separates active action-cell count from raw "
                "action-cell storage count. A collapsed tier can have zero live executable "
                "action cells; if raw storage records are also zero, the upstream partition "
                "layer has already cleaned historical records. The active count is the live "
                "control surface.",
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
                "- [results/noisy_rate_thresholds.md](results/noisy_rate_thresholds.md): threshold details.",
                "- [results/source_coverage.md](results/source_coverage.md): source-coverage details.",
                "",
                "## Claim Boundary",
                "",
                f"This readout may claim that the {run_scope_noun} completed, produced repo-resident artifacts, checked metadata/runtime selected-edge consistency, reported source coverage, and reported collapse threshold fields shown above.",
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
                "_No active public clarification turns are recorded for this readout._",
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
                "The diagnostic runs the existing counterpoint hidden graph with one scheduled noisy-rate contraction block per rate arm.",
                "The selector is edge-global and threshold-based. It does not guarantee at least one selected outgoing edge per source.",
                "",
                f"Current scope: `{run_scope}`.",
                f"Instances: {_join_config_values(budget.get('instance_ids'))}.",
                f"Rates: {_join_rates(budget.get('rates'))}.",
                f"Schema seeds: {_join_config_values(budget.get('schema_seeds'))}.",
                f"Selector rule id: `{budget.get('selector_rule_id', 'unknown')}`.",
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
                "- `results/noisy_rate_selection_summary.csv`: selected edge counts and expected-rate residuals.",
                "- `results/noisy_rate_source_coverage_summary.csv`: selected-source and zero-selected-source evidence.",
                "- `results/noisy_rate_selection_consistency_summary.csv`: metadata/runtime selected-edge equality checks.",
                "- `results/noisy_rate_monotonicity_summary.csv`: coupled-rate nesting checks.",
                "- `results/noisy_rate_threshold_summary.csv`: first full collapse, first near collapse, last nontrivial rate, and sweep verdict.",
                "- `results/tower_shape_summary.csv`: tier state-cell shape, active "
                "action-cell counts, and raw action-cell storage counts.",
                "- `results/endpoint_coalescence_summary.csv`: endpoint-coalescence diagnostics for selected edges.",
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
                "- requested rate: the threshold probability for selecting each edge.",
                "- realized selected edge share: selected edges divided by all graph edges.",
                "- selected source share: source states with at least one selected outgoing edge divided by source states with outgoing edges.",
                "- zero-selected source: a source state whose outgoing edges all scored above the requested rate.",
                "- scheduled contraction block: the selected edge set for one noisy-rate arm.",
                "- repeated endpoint coalescence: the current tower operation applied to scheduled edges.",
                "- active action-cell count: action cells reachable from active state "
                "cells; this is the live control surface.",
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
                f"First full-collapse requested rate: `{first_full if first_full is not None else 'none observed'}`.",
                f"First near-collapse requested rate: `{first_near if first_near is not None else 'none observed'}`.",
                f"Last nontrivial requested rate: `{last_nontrivial if last_nontrivial is not None else 'none observed'}`.",
                f"Metadata/runtime selected-edge consistency: `{consistency_ok}`.",
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
                f"The {run_scope_noun} completed. The central diagnostic finding is `{_verdict_text(verdict)}`.",
                "",
                "This run is about structural behavior under noisy-rate contraction. It is not a learning-performance result.",
                "",
            ]
        ),
        create_parents=True,
    )
    _write_text(
        files["results/noisy_rate_thresholds.md"],
        "\n".join(["# Noisy-Rate Thresholds", "", *threshold_lines, ""]),
        create_parents=True,
    )
    _write_text(
        files["results/source_coverage.md"],
        "\n".join(["# Source Coverage", "", *coverage_lines, ""]),
        create_parents=True,
    )
    return {key: str(path) for key, path in files.items()}
