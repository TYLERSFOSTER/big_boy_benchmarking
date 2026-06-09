"""Docs and source-binding writer for the PlateSupport tower-star diagnostic."""

from __future__ import annotations

import csv
from html import escape
from pathlib import Path

from big_boy_benchmarking.artifacts.schemas import ARTIFACT_SCHEMA_VERSION
from big_boy_benchmarking.artifacts.writers import write_csv, write_json

from .aggregation import RESULT_TABLE_FIELDNAMES
from .config import (
    CLAIM_BOUNDARY,
    ENVIRONMENT_FAMILY_ID,
    ENVIRONMENT_INSTANCE_ID,
    TOWER_STAR_GUARDED_LIFT_COMPARISON_EVALUATION_ID,
)
from .paths import repo_placeholder, repo_readout_surface


def write_tower_star_docs(
    *,
    repo_root: Path,
    artifact_root: Path,
    evaluation_root: Path,
    run_label: str,
    output_paths: dict[str, str],
    target: dict[str, object],
    interpretation_row: dict[str, object],
    badge_rows: list[dict[str, object]],
    parent_gauntlet_source: Path,
    direct_star_source: Path,
) -> dict[str, str]:
    """Write seed human docs and the checked-in readout source binding."""

    readout_surface = repo_readout_surface(repo_root)
    readout_surface.mkdir(parents=True, exist_ok=True)
    (readout_surface / "results").mkdir(parents=True, exist_ok=True)
    (readout_surface / "badges").mkdir(parents=True, exist_ok=True)

    badge_paths = _write_badges(readout_surface / "badges", badge_rows)
    source_files = {
        key: repo_placeholder(Path(value), repo_root)
        for key, value in output_paths.items()
        if key in RESULT_TABLE_FIELDNAMES
    }
    readout_source_path = readout_surface / "readout_source.json"
    readout_source = {
        "artifact_schema_version": ARTIFACT_SCHEMA_VERSION,
        "source_binding_type": "evaluation_readout_source",
        "repo_readout_surface": repo_placeholder(readout_surface, repo_root),
        "source_artifact_root": repo_placeholder(artifact_root, repo_root),
        "source_evaluation_root": repo_placeholder(evaluation_root, repo_root),
        "evaluation_id": TOWER_STAR_GUARDED_LIFT_COMPARISON_EVALUATION_ID,
        "environment_family_id": ENVIRONMENT_FAMILY_ID,
        "environment_instance_id": ENVIRONMENT_INSTANCE_ID,
        "artifact_run_label": run_label,
        "run_mode": "tower_star_guarded_lift_comparison_diagnostic",
        "parent_gauntlet_source": repo_placeholder(parent_gauntlet_source, repo_root),
        "direct_star_source": repo_placeholder(direct_star_source, repo_root),
        "calibrated_target": target,
        "interpretation_summary": interpretation_row,
        "information_parity_warning": (
            "Direct-star filters primitive actions. Tower-star filters concrete "
            "lift candidates inside quotient action cells before the tower "
            "chooses among those cells. Both are one-step oracle local controls, "
            "not final deployable fairness proofs."
        ),
        "source_files": source_files,
        "expected_files": {
            "required": list(source_files.values()),
            "expected_absent_is_gap": [],
            "conditional": {},
            "not_applicable": [],
            "expectation_sources": [
                "docs/design/first_plate_support_environment/standard_gauntlet_suite/"
                "10_tower_star/"
                "01_001_plate_support_tower_star_guarded_lift_comparison_blueprint.md",
                "docs/prime_directive/evaluation_construction_for_readable_artifacts_protocol.md",
            ],
        },
        "goal_criteria": [
            {
                "goal_id": "plate_support_tower_star_guarded_lift_comparison",
                "question": (
                    "Does the selected PlateSupport tower candidate survive when "
                    "both direct and tower are normalized against one-step local "
                    "invalid/self-loop star controls?"
                ),
                "success_signal": (
                    "interpretation_summary.csv reports tower_survives_star_control"
                ),
                "partial_signal": (
                    "tower-star surfaces are implemented but margins are small or "
                    "surface blockage limits comparison"
                ),
                "failure_signal": (
                    "direct_nonself_guard remains above tower_nonself_guard under "
                    "the checked-in budget"
                ),
                "claim_if_met": (
                    "bounded smoke evidence for tower value beyond local "
                    "cul-de-sac filtering"
                ),
                "claim_if_not_met": (
                    "the prior PlateSupport signal remains unseparated from "
                    "one-step local action filtering"
                ),
            }
        ],
        "badge_policy": {
            "dimensions": [
                "artifact_status",
                "direct_star_status",
                "tower_star_status",
                "primary_interpretation",
                "tower_surface_blockage",
                "claim_scope",
                "provenance_status",
            ]
        },
        "goal_summary_sources": [
            "docs/design/first_plate_support_environment/standard_gauntlet_suite/"
            "10_tower_star/"
            "01_001_plate_support_tower_star_guarded_lift_comparison_blueprint.md",
            repo_placeholder(readout_surface / "method.md", repo_root),
        ],
        "methodology_summary_sources": [
            "docs/design/first_plate_support_environment/standard_gauntlet_suite/"
            "10_tower_star/"
            "01_001_plate_support_tower_star_guarded_lift_comparison_blueprint.md",
            repo_placeholder(readout_surface / "method.md", repo_root),
            repo_placeholder(readout_surface / "runbook.md", repo_root),
        ],
        "structural_limit_checks": [
            {
                "check_id": "tower_star_preselection_lift_filtering",
                "trigger": "tower-star guard is implemented after tower action selection",
                "interpretation_if_triggered": (
                    "The diagnostic is invalid because tower-star must remove "
                    "lift candidates and empty action cells before selection."
                ),
                "claim_effect": "blocks tower-star comparison claims",
            }
        ],
        "claim_boundary": [
            CLAIM_BOUNDARY,
            "This evaluation may compare direct-star and tower-star one-step local controls.",
            "This evaluation may not claim broad tower superiority or broad tower failure.",
        ],
        "readout_badges": {
            str(row["badge_id"]): {
                "label": row["label"],
                "value": row["value"],
                "color": row["color"],
                "reason": row["reason"],
                "source": row["source"],
            }
            for row in badge_rows
        },
    }
    write_json(readout_source_path, readout_source, create_parents=True)
    write_csv(
        readout_surface / "results" / "badge_summary.csv",
        badge_rows,
        ("badge_id", "label", "value", "color", "reason", "source"),
        create_parents=True,
    )
    _write_readme(
        readout_surface=readout_surface,
        run_label=run_label,
        interpretation_row=interpretation_row,
        badge_rows=badge_rows,
        badge_paths=badge_paths,
        output_paths=output_paths,
    )
    _write_method(readout_surface)
    _write_runbook(readout_surface)
    _write_glossary(readout_surface)
    _write_artifact_index(
        readout_surface=readout_surface,
        output_paths=output_paths,
        badge_paths=badge_paths,
        readout_source_path=readout_source_path,
        repo_root=repo_root,
    )
    _write_result_readout(readout_surface, interpretation_row)
    _write_protocol_result_docs(readout_surface, output_paths, interpretation_row)
    docs = {
        "README.md": str(readout_surface / "README.md"),
        "method.md": str(readout_surface / "method.md"),
        "runbook.md": str(readout_surface / "runbook.md"),
        "artifact_index.md": str(readout_surface / "artifact_index.md"),
        "glossary.md": str(readout_surface / "glossary.md"),
        "result_readout.md": str(readout_surface / "result_readout.md"),
        "readout_source.json": str(readout_source_path),
        "results/badge_summary.csv": str(readout_surface / "results" / "badge_summary.csv"),
        "results/summary.md": str(readout_surface / "results" / "summary.md"),
        "results/human_summary.md": str(readout_surface / "results" / "human_summary.md"),
        "results/arm_readout_table.md": str(readout_surface / "results" / "arm_readout_table.md"),
        "results/diagnostic_findings.md": str(readout_surface / "results" / "diagnostic_findings.md"),
        "results/tower_star_findings.md": str(readout_surface / "results" / "tower_star_findings.md"),
        "results/timing_readout.md": str(readout_surface / "results" / "timing_readout.md"),
    }
    docs.update({f"badges/{path.name}": str(path) for path in badge_paths.values()})
    return docs


def _write_readme(
    *,
    readout_surface: Path,
    run_label: str,
    interpretation_row: dict[str, object],
    badge_rows: list[dict[str, object]],
    badge_paths: dict[str, Path],
    output_paths: dict[str, str],
) -> None:
    arm_rows = _read_csv(Path(output_paths["arm_summary"]))
    comparison_rows = _read_csv(Path(output_paths["paired_star_comparison"]))
    surface_rows = _read_csv(Path(output_paths["tower_action_cell_surface_summary"]))
    mixing_rows = _read_csv(Path(output_paths["lift_pool_mixing_summary"]))
    arm_by_id = {row.get("arm_id", ""): row for row in arm_rows}
    badges = " ".join(
        f"![{_badge_alt(row)}](badges/{badge_paths[str(row['badge_id'])].name})"
        for row in badge_rows
        if str(row.get("badge_id", "")) in badge_paths
    )
    primary_case = str(
        interpretation_row.get(
            "primary_interpretation_case",
            interpretation_row.get("interpretation_case", "unknown"),
        )
    )
    direct_nonself = arm_by_id.get("direct_nonself_guard", {})
    tower_nonself = arm_by_id.get("tower_nonself_guard", {})
    tower_current = arm_by_id.get("tower_lift_executable_current", {})
    lines = [
        "# PlateSupport Tower-Star Guarded Lift Comparison Readout",
        "",
        badges,
        "",
        "## Status At A Glance",
        "",
        "- Artifact evidence: complete; the required run and summary tables exist in the repo-resident artifact root.",
        f"- Run label: `{run_label}`.",
        f"- Primary interpretation: `{primary_case}`.",
        (
            "- Primary comparison: `direct_nonself_guard` versus "
            "`tower_nonself_guard`."
        ),
        "- Claim scope: diagnostic smoke/calibration evidence only.",
        "",
        "## Summary of Goals Behind this Evaluation",
        "",
        (
            "This evaluation follows Abdul Malik's PlateSupport cul-de-sac "
            "observation and the Project Owner's later clarification that "
            "direct-star alone is not enough: the tower side should also be "
            "explicitly starred. The purpose is to test whether the selected "
            "PlateSupport tower candidate still carries signal when direct and "
            "tower are both normalized against one-step local invalid/self-loop "
            "mechanisms."
        ),
        "",
        "## Summary of Methodology Behind this Evaluation",
        "",
        (
            "Direct-star filters primitive actions before direct action "
            "selection. Tower-star filters concrete lift candidates inside "
            "quotient action cells before tower action-cell selection. If a "
            "tower action cell has no surviving guarded lift candidates, that "
            "action cell is removed from the tower action surface for that arm."
        ),
        "",
        "The six arms are:",
        "",
        "- `direct_raw`;",
        "- `direct_invalid_guard`;",
        "- `direct_nonself_guard`;",
        "- `tower_lift_executable_current`;",
        "- `tower_invalid_guard`;",
        "- `tower_nonself_guard`.",
        "",
        "## One-Screen Verdict",
        "",
        (
            f"The primary target delta "
            f"(`tower_nonself_guard - direct_nonself_guard`) is "
            f"`{interpretation_row.get('primary_target_delta', '')}`."
        ),
        (
            f"`direct_nonself_guard` target-hit rate: "
            f"`{_cell(direct_nonself, 'target_hit_rate')}`."
        ),
        (
            f"`tower_nonself_guard` target-hit rate: "
            f"`{_cell(tower_nonself, 'target_hit_rate')}`."
        ),
        (
            f"`tower_lift_executable_current` target-hit rate: "
            f"`{_cell(tower_current, 'target_hit_rate')}`."
        ),
        "",
        "## Key Arm Results",
        "",
        "| Arm | Target Hit Rate | Mean Reward | Invalid Rate | Self-Transition Rate | Blocked Episodes |",
        "| --- | ---: | ---: | ---: | ---: | ---: |",
    ]
    for arm in arm_rows:
        lines.append(
            "| "
            f"`{arm.get('arm_id', '')}` | "
            f"{_cell(arm, 'target_hit_rate')} | "
            f"{_cell(arm, 'mean_total_reward')} | "
            f"{_cell(arm, 'invalid_move_rate')} | "
            f"{_cell(arm, 'self_transition_rate')} | "
            f"{_cell(arm, 'blocked_episode_count')} |"
        )
    lines.extend(
        [
            "",
            "## Direct-Star Versus Tower-Star Comparisons",
            "",
            "| Comparison | Left Arm | Right Arm | Delta Right Minus Left | Flag |",
            "| --- | --- | --- | ---: | --- |",
        ]
    )
    for row in comparison_rows:
        lines.append(
            "| "
            f"`{row.get('comparison_id', '')}` | "
            f"`{row.get('left_arm_id', '')}` | "
            f"`{row.get('right_arm_id', '')}` | "
            f"{row.get('delta_right_minus_left', '')} | "
            f"`{row.get('interpretation_flag', '')}` |"
        )
    lines.extend(
        [
            "",
            "## Tower Action-Cell And Lift-Pool Findings",
            "",
            (
                f"- Surface summary rows: `{len(surface_rows)}`; lift-pool mixing "
                f"summary rows: `{len(mixing_rows)}`."
            ),
            (
                "- Inspect `tower_lift_guard_summary.csv`, "
                "`tower_action_cell_surface_summary.csv`, and "
                "`lift_pool_mixing_summary.csv` to see which action cells were "
                "removed by invalid-star or nonself-star filtering."
            ),
            "",
            "## Information Parity Warning",
            "",
            (
                "Both direct-star and tower-star use oracle one-step local "
                "transition information. This is a diagnostic control for the "
                "cul-de-sac confound, not a final proof of deployable direct/tower "
                "fairness."
            ),
            "",
            "## Attribution",
            "",
            (
                "- Abdul Malik, project PM, raised the original cul-de-sac / "
                "validity-filtering concern."
            ),
            (
                "- The Project Owner requested the `tower_star` follow-up and "
                "the detailed implementation workplan."
            ),
            (
                "- Codex authored the concrete arm matrix, artifact contract, "
                "and implementation details unless revised by the Project Owner."
            ),
            "",
            "## Claim Boundary",
            "",
            "- This readout may compare direct-star and tower-star diagnostic controls.",
            "- This readout may not claim broad tower superiority or broad tower failure.",
            "- This readout may not claim final robotics benchmark significance.",
            "",
            "## Inspection Map",
            "",
            "- Main arm table: `artifacts/"
            f"{run_label}/evaluations/{TOWER_STAR_GUARDED_LIFT_COMPARISON_EVALUATION_ID}/results/arm_summary.csv`",
            "- Star comparisons: `artifacts/"
            f"{run_label}/evaluations/{TOWER_STAR_GUARDED_LIFT_COMPARISON_EVALUATION_ID}/results/paired_star_comparison.csv`",
            "- Tower lift table: `artifacts/"
            f"{run_label}/evaluations/{TOWER_STAR_GUARDED_LIFT_COMPARISON_EVALUATION_ID}/results/tower_lift_guard_summary.csv`",
            "- Interpretation table: `artifacts/"
            f"{run_label}/evaluations/{TOWER_STAR_GUARDED_LIFT_COMPARISON_EVALUATION_ID}/results/interpretation_summary.csv`",
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
        ]
    )
    (readout_surface / "README.md").write_text("\n".join(lines) + "\n", encoding="utf-8")


def _write_method(readout_surface: Path) -> None:
    (readout_surface / "method.md").write_text(
        "\n".join(
            [
                "# PlateSupport Tower-Star Guarded Lift Comparison Method",
                "",
                "The diagnostic reruns direct-star arms and tower-star arms under one paired seed policy.",
                "",
                "Direct-star filters primitive actions before direct selection.",
                "Tower-star filters concrete lift candidates inside quotient action cells before tower selection.",
                "The primary comparison is `direct_nonself_guard` versus `tower_nonself_guard`.",
            ]
        )
        + "\n",
        encoding="utf-8",
    )


def _write_runbook(readout_surface: Path) -> None:
    (readout_surface / "runbook.md").write_text(
        "\n".join(
            [
                "# PlateSupport Tower-Star Guarded Lift Comparison Runbook",
                "",
                "```bash",
                "uv run python -m big_boy_benchmarking.cli plate-support tower-star run \\",
                "  --repo-root \"$BBB_ROOT\" \\",
                "  --artifact-root \"$BBB_ROOT/docs/evaluations/plate_support_5x5_default_v001/tower_star/artifacts/tower_star_001\" \\",
                "  --parent-gauntlet-source \"$BBB_ROOT/docs/evaluations/plate_support_5x5_default_v001/standard_gauntlet/readout_source.json\" \\",
                "  --direct-star-source \"$BBB_ROOT/docs/evaluations/plate_support_5x5_default_v001/direct_star_culdesac_control/readout_source.json\" \\",
                "  --run-label tower_star_001 \\",
                "  --locked-by foster",
                "",
                "uv run python -m big_boy_benchmarking.cli plate-support tower-star summarize \\",
                "  --repo-root \"$BBB_ROOT\" \\",
                "  --artifact-root \"$BBB_ROOT/docs/evaluations/plate_support_5x5_default_v001/tower_star/artifacts/tower_star_001\"",
                "```",
            ]
        )
        + "\n",
        encoding="utf-8",
    )


def _write_glossary(readout_surface: Path) -> None:
    (readout_surface / "glossary.md").write_text(
        "\n".join(
            [
                "# PlateSupport Tower-Star Glossary",
                "",
                "- `direct_raw`: direct PlateSupport learner over the primitive action alphabet.",
                "- `direct_invalid_guard`: direct learner with one-step invalid primitive actions removed before selection.",
                "- `direct_nonself_guard`: direct learner with one-step self-loop primitive actions removed before selection.",
                "- `tower_lift_executable_current`: current tower learner using executable quotient action cells.",
                "- `tower_invalid_guard`: tower learner after removing lift candidates whose primitive action is invalid.",
                "- `tower_nonself_guard`: tower learner after removing lift candidates whose primitive action is a self-loop.",
                "- `tower-star`: the diagnostic rule that filters concrete lift candidates before tower action-cell selection.",
                "- `action cell`: a quotient action option exposed by the contracted tower tier.",
                "- `lift candidate`: a concrete primitive action inside a quotient action cell.",
                "- `diagnostic smoke/calibration evidence`: evidence useful for debugging and calibration, not final benchmark proof.",
            ]
        )
        + "\n",
        encoding="utf-8",
    )


def _write_artifact_index(
    *,
    readout_surface: Path,
    output_paths: dict[str, str],
    badge_paths: dict[str, Path],
    readout_source_path: Path,
    repo_root: Path,
) -> None:
    lines = [
        "# PlateSupport Tower-Star Guarded Lift Comparison Artifact Index",
        "",
        f"- Readout source: `{repo_placeholder(readout_source_path, repo_root)}`",
        "",
        "## Result Tables",
        "",
    ]
    for key, path in sorted(output_paths.items()):
        lines.append(f"- `{key}`: `{repo_placeholder(Path(path), repo_root)}`")
    lines.extend(["", "## Badges", ""])
    for key, path in sorted(badge_paths.items()):
        lines.append(f"- `{key}`: `{repo_placeholder(path, repo_root)}`")
    (readout_surface / "artifact_index.md").write_text("\n".join(lines) + "\n", encoding="utf-8")


def _write_result_readout(
    readout_surface: Path,
    interpretation_row: dict[str, object],
) -> None:
    (readout_surface / "result_readout.md").write_text(
        "\n".join(
            [
                "# PlateSupport Tower-Star Guarded Lift Comparison Result Readout",
                "",
                f"- Primary interpretation: `{interpretation_row.get('primary_interpretation_case', '')}`.",
                f"- Primary target delta: `{interpretation_row.get('primary_target_delta', '')}`.",
                f"- Allowed claim: {interpretation_row.get('allowed_claim', '')}.",
                f"- Blocked claim: {interpretation_row.get('blocked_claim', '')}.",
            ]
        )
        + "\n",
        encoding="utf-8",
    )


def _write_protocol_result_docs(
    readout_surface: Path,
    output_paths: dict[str, str],
    interpretation_row: dict[str, object],
) -> None:
    results_dir = readout_surface / "results"
    arm_rows = _read_csv(Path(output_paths["arm_summary"]))
    comparison_rows = _read_csv(Path(output_paths["paired_star_comparison"]))
    (results_dir / "summary.md").write_text(
        f"# Summary\n\nPrimary interpretation: `{interpretation_row.get('primary_interpretation_case', '')}`.\n",
        encoding="utf-8",
    )
    (results_dir / "human_summary.md").write_text(
        "# Human Summary\n\nTower-star compares direct-star controls against tower lift-candidate controls.\n",
        encoding="utf-8",
    )
    arm_lines = [
        "# Arm Readout Table",
        "",
        "| Arm | Target Hit Rate | Mean Reward |",
        "| --- | ---: | ---: |",
    ]
    for row in arm_rows:
        arm_lines.append(
            f"| `{row.get('arm_id', '')}` | {row.get('target_hit_rate', '')} | {row.get('mean_total_reward', '')} |"
        )
    (results_dir / "arm_readout_table.md").write_text("\n".join(arm_lines) + "\n", encoding="utf-8")
    finding_lines = [
        "# Tower-Star Findings",
        "",
        "| Comparison | Delta | Flag |",
        "| --- | ---: | --- |",
    ]
    for row in comparison_rows:
        finding_lines.append(
            f"| `{row.get('comparison_id', '')}` | {row.get('delta_right_minus_left', '')} | `{row.get('interpretation_flag', '')}` |"
        )
    (results_dir / "tower_star_findings.md").write_text(
        "\n".join(finding_lines) + "\n",
        encoding="utf-8",
    )
    (results_dir / "diagnostic_findings.md").write_text(
        "\n".join(finding_lines) + "\n",
        encoding="utf-8",
    )
    (results_dir / "timing_readout.md").write_text(
        "# Timing Readout\n\nSee `timing_summary.csv` in the source artifact tree.\n",
        encoding="utf-8",
    )


def _write_badges(badge_dir: Path, rows: list[dict[str, object]]) -> dict[str, Path]:
    for stale in badge_dir.glob("*.svg"):
        stale.unlink()
    paths: dict[str, Path] = {}
    for row in rows:
        badge_id = str(row["badge_id"])
        path = badge_dir / f"{badge_id}.svg"
        label = str(row.get("label", badge_id))
        value = str(row.get("value", ""))
        color = _badge_color(str(row.get("color", "blue")))
        path.write_text(_badge_svg(label, value, color), encoding="utf-8")
        paths[badge_id] = path
    return paths


def _badge_svg(label: str, value: str, color: str) -> str:
    label_width = max(55, 7 * len(label) + 10)
    value_width = max(55, 7 * len(value) + 10)
    total = label_width + value_width
    return (
        f'<svg xmlns="http://www.w3.org/2000/svg" width="{total}" height="20" role="img" '
        f'aria-label="{escape(label)}: {escape(value)}">'
        f'<rect width="{label_width}" height="20" fill="#555"/>'
        f'<rect x="{label_width}" width="{value_width}" height="20" fill="{color}"/>'
        f'<text x="{label_width / 2}" y="14" fill="#fff" font-family="Verdana,Geneva,sans-serif" '
        f'font-size="11" text-anchor="middle">{escape(label)}</text>'
        f'<text x="{label_width + value_width / 2}" y="14" fill="#fff" '
        f'font-family="Verdana,Geneva,sans-serif" font-size="11" text-anchor="middle">'
        f'{escape(value)}</text></svg>\n'
    )


def _badge_color(color: str) -> str:
    return {
        "green": "#2e7d32",
        "yellow": "#b58900",
        "orange": "#ef6c00",
        "red": "#d32f2f",
        "blue": "#1565c0",
        "gray": "#777",
    }.get(color, "#1565c0")


def _badge_alt(row: dict[str, object]) -> str:
    return f"{row.get('label', '')}: {row.get('value', '')}"


def _cell(row: dict[str, str], key: str) -> str:
    return str(row.get(key, ""))


def _read_csv(path: Path) -> list[dict[str, str]]:
    with path.open(encoding="utf-8", newline="") as handle:
        return list(csv.DictReader(handle))
