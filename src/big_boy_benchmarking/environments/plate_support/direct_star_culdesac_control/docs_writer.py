"""Docs and source-binding writer for the direct-star diagnostic."""

from __future__ import annotations

import csv
from html import escape
from pathlib import Path

from big_boy_benchmarking.artifacts.schemas import ARTIFACT_SCHEMA_VERSION
from big_boy_benchmarking.artifacts.writers import write_csv, write_json

from .aggregation import RESULT_TABLE_FIELDNAMES
from .config import (
    CLAIM_BOUNDARY,
    DIRECT_STAR_CULDESAC_CONTROL_EVALUATION_ID,
    ENVIRONMENT_FAMILY_ID,
    ENVIRONMENT_INSTANCE_ID,
)
from .paths import repo_placeholder, repo_readout_surface


def write_direct_star_docs(
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
) -> dict[str, str]:
    """Write seed human docs and the checked-in readout source binding."""

    readout_surface = repo_readout_surface(repo_root)
    readout_surface.mkdir(parents=True, exist_ok=True)
    (readout_surface / "results").mkdir(parents=True, exist_ok=True)
    (readout_surface / "badges").mkdir(parents=True, exist_ok=True)

    badge_paths = _write_badges(readout_surface / "badges", badge_rows)
    readout_source_path = readout_surface / "readout_source.json"
    source_files = {
        key: repo_placeholder(Path(value), repo_root)
        for key, value in output_paths.items()
        if key in RESULT_TABLE_FIELDNAMES
    }
    readout_source = {
        "artifact_schema_version": ARTIFACT_SCHEMA_VERSION,
        "source_binding_type": "evaluation_readout_source",
        "repo_readout_surface": repo_placeholder(readout_surface, repo_root),
        "source_artifact_root": repo_placeholder(artifact_root, repo_root),
        "source_evaluation_root": repo_placeholder(evaluation_root, repo_root),
        "evaluation_id": DIRECT_STAR_CULDESAC_CONTROL_EVALUATION_ID,
        "environment_family_id": ENVIRONMENT_FAMILY_ID,
        "environment_instance_id": ENVIRONMENT_INSTANCE_ID,
        "artifact_run_label": run_label,
        "run_mode": "direct_star_culdesac_control_diagnostic",
        "parent_gauntlet_source": repo_placeholder(parent_gauntlet_source, repo_root),
        "calibrated_target": target,
        "interpretation_summary": interpretation_row,
        "information_parity_warning": (
            "Guarded direct uses oracle one-step local transition masks. It "
            "diagnoses invalid/self-loop filtering but does not prove perfect "
            "action-surface parity with tower."
        ),
        "source_files": source_files,
        "expected_files": {
            "required": list(source_files.values()),
            "expected_absent_is_gap": [],
            "conditional": {},
            "not_applicable": [],
            "expectation_sources": [
                "docs/design/first_plate_support_environment/standard_gauntlet_suite/"
                "09_direct_star_culdesac_control/"
                "01_001_plate_support_direct_star_culdesac_control_blueprint.md",
                "docs/prime_directive/evaluation_construction_for_readable_artifacts_protocol.md",
            ],
        },
        "goal_criteria": [
            {
                "goal_id": "plate_support_direct_star_culdesac_control",
                "question": (
                    "Does the PlateSupport tower signal survive raw direct, "
                    "invalid-guarded direct, and nonself-guarded direct controls?"
                ),
                "success_signal": "interpretation_summary.csv reports tower_survives_nonself_guard",
                "partial_signal": "guarded tables complete but interpretation is mixed or inconclusive",
                "failure_signal": "guarded direct erases or reverses the tower signal",
                "claim_if_met": (
                    "bounded diagnostic evidence remains after one-step local "
                    "nonself action filtering"
                ),
                "claim_if_not_met": (
                    "the prior PlateSupport signal is explained or not yet "
                    "separated from local action filtering"
                ),
            }
        ],
        "badge_policy": {
            "dimensions": [
                "artifact_status",
                "guarded_direct_status",
                "self_loop_confound_status",
                "tower_vs_nonself_status",
                "claim_scope",
                "provenance_status",
            ]
        },
        "goal_summary_sources": [
            "docs/design/first_plate_support_environment/standard_gauntlet_suite/"
            "09_direct_star_culdesac_control/"
            "01_001_plate_support_direct_star_culdesac_control_blueprint.md",
            repo_placeholder(readout_surface / "method.md", repo_root),
        ],
        "methodology_summary_sources": [
            "docs/design/first_plate_support_environment/standard_gauntlet_suite/"
            "09_direct_star_culdesac_control/"
            "01_001_plate_support_direct_star_culdesac_control_blueprint.md",
            repo_placeholder(readout_surface / "method.md", repo_root),
            repo_placeholder(readout_surface / "runbook.md", repo_root),
        ],
        "structural_limit_checks": [
            {
                "check_id": "guarded_direct_oracle_local_transition",
                "trigger": "direct_invalid_guard or direct_nonself_guard is interpreted as fully fair direct",
                "interpretation_if_triggered": (
                    "The guarded arms are oracle one-step local controls, not "
                    "proof of perfect parity with the tower action surface."
                ),
                "claim_effect": "blocks overclaiming from guarded-direct outcomes",
            }
        ],
        "claim_boundary": [
            CLAIM_BOUNDARY,
            "This evaluation may diagnose invalid/self-loop filtering as a confound.",
            "This evaluation may not claim broad tower superiority.",
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
        target=target,
        interpretation_row=interpretation_row,
        badge_paths=badge_paths,
        output_paths=output_paths,
    )
    _write_method(readout_surface)
    _write_runbook(readout_surface)
    _write_artifact_index(
        readout_surface,
        output_paths,
        badge_paths,
        readout_source_path,
        repo_root,
    )
    _write_result_readout(readout_surface, interpretation_row)
    _write_protocol_result_docs(readout_surface, output_paths, interpretation_row)
    docs = {
        "README.md": str(readout_surface / "README.md"),
        "method.md": str(readout_surface / "method.md"),
        "runbook.md": str(readout_surface / "runbook.md"),
        "artifact_index.md": str(readout_surface / "artifact_index.md"),
        "result_readout.md": str(readout_surface / "result_readout.md"),
        "readout_source.json": str(readout_source_path),
        "results/badge_summary.csv": str(readout_surface / "results" / "badge_summary.csv"),
        "results/summary.md": str(readout_surface / "results" / "summary.md"),
        "results/human_summary.md": str(readout_surface / "results" / "human_summary.md"),
        "results/arm_readout_table.md": str(readout_surface / "results" / "arm_readout_table.md"),
        "results/diagnostic_findings.md": str(readout_surface / "results" / "diagnostic_findings.md"),
        "results/timing_readout.md": str(readout_surface / "results" / "timing_readout.md"),
    }
    docs.update({f"badges/{path.name}": str(path) for path in badge_paths.values()})
    return docs


def _write_readme(
    *,
    readout_surface: Path,
    run_label: str,
    target: dict[str, object],
    interpretation_row: dict[str, object],
    badge_paths: dict[str, Path],
    output_paths: dict[str, str],
) -> None:
    arm_rows = _read_csv(Path(output_paths["arm_summary"]))
    guard_rows = _read_csv(Path(output_paths["guard_filter_summary"]))
    action_rows = _read_csv(Path(output_paths["action_surface_summary"]))
    badge_rows = _read_csv(readout_surface / "results" / "badge_summary.csv")
    arm_by_id = {row.get("arm_id", ""): row for row in arm_rows}
    guard_by_id = {row.get("arm_id", ""): row for row in guard_rows}
    action_by_id = {row.get("arm_id", ""): row for row in action_rows}
    badge_by_id = {row.get("badge_id", ""): row for row in badge_rows}
    raw = arm_by_id.get("direct_raw", {})
    invalid = arm_by_id.get("direct_invalid_guard", {})
    nonself = arm_by_id.get("direct_nonself_guard", {})
    tower = arm_by_id.get("tower_selected_candidate", {})
    raw_guard = guard_by_id.get("direct_raw", {})
    invalid_guard = guard_by_id.get("direct_invalid_guard", {})
    nonself_guard = guard_by_id.get("direct_nonself_guard", {})
    tower_guard = guard_by_id.get("tower_selected_candidate", {})
    raw_action = action_by_id.get("direct_raw", {})
    invalid_action = action_by_id.get("direct_invalid_guard", {})
    nonself_action = action_by_id.get("direct_nonself_guard", {})
    tower_action = action_by_id.get("tower_selected_candidate", {})
    badge_line = " ".join(
        f"![{_badge_alt(badge_id, badge_by_id)}](badges/{path.name})"
        for badge_id, path in badge_paths.items()
    )
    readout_surface.joinpath("README.md").write_text(
        "\n".join(
            [
                "# PlateSupport Direct-Star Cul-de-sac Control - Guarded Diagnostic Readout",
                "",
                badge_line,
                "",
                "## Status At A Glance",
                "",
                "- Artifact evidence: complete; required arm, guard, step, lift, tier, timing, and interpretation tables exist.",
                "- Behavioral result: diagnostic control result; tower beats raw direct on binary target, but guarded direct controls beat tower.",
                "- Goal result: the run identifies one-step validity/self-loop filtering as a major confound in the prior PlateSupport signal.",
                "- Claim scope: diagnostic smoke/calibration evidence only; this is not a final robotics benchmark claim.",
                "- Provenance: repo-resident artifact root under `docs/evaluations/plate_support_5x5_default_v001/direct_star_culdesac_control/artifacts/guarded_001`.",
                "",
                "## Summary of Goals Behind this Evaluation",
                "",
                "This evaluation exists because Abdul Malik, project PM, observed that the previous PlateSupport gauntlet result raised an action-surface concern: raw direct learning appeared to hit invalid or self-looping cul-de-sacs, while the tower controller avoided them through its liftability/executable-action machinery. The Project Owner accepted that concern and asked for a BBB-side diagnostic control rather than treating the prior tower-positive signal as settled.",
                "",
                "The concrete question is whether the selected PlateSupport iterated tower candidate still looks better when direct learning receives one-step local guards. The arms are `direct_raw`, `direct_invalid_guard`, `direct_nonself_guard`, and `tower_selected_candidate`. The evaluation is not trying to prove broad robotics superiority, perfect direct/tower fairness, or final benchmark significance.",
                "",
                "## Summary of Methodology Behind this Evaluation",
                "",
                f"The run label is `{run_label}`. The calibrated target is `{target.get('target_policy_id', '')}` with `{target.get('recommended_episodes_per_replicate', '')}` episodes per replicate and `{target.get('recommended_replicates_per_arm', '')}` replicates per arm. All arms use matched paired seed bundles.",
                "",
                "Direct arms use tabular Q-learning over the primitive PlateSupport action alphabet, with epsilon-greedy selection and guard-specific Q bootstrap. The guards are applied before action selection. `direct_invalid_guard` removes only actions whose one-step primitive transition is marked invalid. `direct_nonself_guard` removes actions whose one-step primitive transition returns to the same concrete state. If a guard ever filters all actions, the episode is diagnostically blocked rather than silently falling back to raw direct behavior.",
                "",
                "The selected tower arm reuses the parent gauntlet's selected iterated source-local-ratio candidate and does not receive direct-style guard masks. Aggregation compares binary target-hit rate, mean reward, invalid moves, self-transitions, guard-filter counts, and action-surface counts.",
                "",
                "## One-Screen Verdict",
                "",
                f"The diagnostic completed and materially changes how the prior PlateSupport result should be read. The tower arm beats raw direct on the binary target: `{_cell(tower, 'target_hit_rate')}` versus `{_cell(raw, 'target_hit_rate')}`. However, both guarded direct controls beat the tower: `direct_invalid_guard={_cell(invalid, 'target_hit_rate')}` and `direct_nonself_guard={_cell(nonself, 'target_hit_rate')}`.",
                "",
                f"The interpretation is `{interpretation_row.get('interpretation_case', '')}`. Allowed claim: {interpretation_row.get('allowed_claim', '')}. Blocked claim: {interpretation_row.get('blocked_claim', '')}.",
                "",
                "This is a useful negative-control result. It does not say the tower machinery is useless; it says the specific earlier PlateSupport advantage is not yet separated from one-step local action filtering.",
                "",
                "## Key Arm Results",
                "",
                "| Arm | Target Hit Rate | Mean Reward | Invalid Rate | Self-Transition Rate | Mean Available Actions |",
                "| --- | ---: | ---: | ---: | ---: | ---: |",
                _arm_markdown_row(raw, raw_action),
                _arm_markdown_row(invalid, invalid_action),
                _arm_markdown_row(nonself, nonself_action),
                _arm_markdown_row(tower, tower_action),
                "",
                "## Guard And Action-Surface Findings",
                "",
                f"- Raw direct saw `{_cell(raw_guard, 'mean_available_before_guard')}` primitive actions before guard and made `{_cell(raw, 'invalid_move_count')}` invalid moves.",
                f"- Invalid-guarded direct filtered `{_cell(invalid_guard, 'mean_invalid_filtered')}` invalid actions on average and made zero invalid moves.",
                f"- Nonself-guarded direct filtered `{_cell(nonself_guard, 'mean_self_loop_filtered')}` self-loop actions on average and made zero self-transitions.",
                f"- The tower arm had `{_cell(tower_guard, 'mean_available_after_guard')}` executable action cells on average and also made zero invalid moves.",
                f"- The tower versus nonself-guard target delta was `{interpretation_row.get('tower_vs_nonself_guard_delta', '')}`, so the tower did not survive the strictest one-step direct control in this run.",
                "",
                "## Information Parity Warning",
                "",
                "The guarded direct controls use oracle one-step local transition masks. They diagnose invalid/self-loop filtering, but they do not prove perfect action-surface parity with the tower. In particular, `direct_nonself_guard` is a control arm, not a final fairness theorem.",
                "",
                "## Run Identity",
                "",
                "- Evaluation id: `plate_support_direct_star_culdesac_control_v001`",
                "- Environment family: `plate_support`",
                "- Environment instance: `plate_support_5x5_default_v001`",
                f"- Run label: `{run_label}`",
                f"- Source artifact root: `docs/evaluations/plate_support_5x5_default_v001/direct_star_culdesac_control/artifacts/{run_label}`",
                f"- Source evaluation root: `docs/evaluations/plate_support_5x5_default_v001/direct_star_culdesac_control/artifacts/{run_label}/evaluations/plate_support_direct_star_culdesac_control_v001`",
                f"- Budget lock: `artifacts/{run_label}/evaluations/plate_support_direct_star_culdesac_control_v001/evaluation_budget_lock.json`",
                "- Parent gauntlet source: `docs/evaluations/plate_support_5x5_default_v001/standard_gauntlet/readout_source.json`",
                "",
                "## Claim Boundary",
                "",
                "- This readout may claim that one-step guarded direct controls were implemented and completed under matched seeds.",
                "- This readout may claim that the guarded controls explain or exceed the prior raw-direct tower signal in this run.",
                "- This readout may not claim broad tower superiority, broad tower failure, or final robotics benchmark significance.",
                "- This readout may not call `direct_nonself_guard` a perfectly fair direct baseline without qualification.",
                "",
                "## Inspection Map",
                "",
                f"- Main arm table: `artifacts/{run_label}/evaluations/plate_support_direct_star_culdesac_control_v001/results/arm_summary.csv`",
                f"- Guard filtering table: `artifacts/{run_label}/evaluations/plate_support_direct_star_culdesac_control_v001/results/guard_filter_summary.csv`",
                f"- Paired guard comparisons: `artifacts/{run_label}/evaluations/plate_support_direct_star_culdesac_control_v001/results/paired_guard_comparison.csv`",
                f"- Action surface table: `artifacts/{run_label}/evaluations/plate_support_direct_star_culdesac_control_v001/results/action_surface_summary.csv`",
                f"- Interpretation table: `artifacts/{run_label}/evaluations/plate_support_direct_star_culdesac_control_v001/results/interpretation_summary.csv`",
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
        encoding="utf-8",
    )


def _arm_markdown_row(arm: dict[str, str], action: dict[str, str]) -> str:
    return (
        f"| `{_cell(arm, 'arm_id')}` | {_cell(arm, 'target_hit_rate')} | "
        f"{_cell(arm, 'mean_total_reward')} | {_cell(arm, 'invalid_move_rate')} | "
        f"{_cell(arm, 'self_transition_rate')} | "
        f"{_cell(action, 'mean_available_action_count')} |"
    )


def _badge_alt(badge_id: str, rows: dict[str, dict[str, str]]) -> str:
    row = rows.get(badge_id, {})
    label = row.get("label") or badge_id.replace("_", " ").title()
    value = row.get("value") or "Unknown"
    return f"{label}: {value}"


def _cell(row: dict[str, str], key: str) -> str:
    return str(row.get(key, ""))


def _write_method(readout_surface: Path) -> None:
    readout_surface.joinpath("method.md").write_text(
        "\n".join(
            [
                "# PlateSupport Direct-Star Cul-de-sac Control Method",
                "",
                "This diagnostic reuses the selected iterated tower candidate and",
                "calibrated target from the PlateSupport standard gauntlet correction",
                "run. It compares raw direct, invalid-guarded direct, nonself-guarded",
                "direct, and the selected tower candidate under matched seed bundles.",
                "",
                "The guarded direct arms are pre-mask controls. They receive only a",
                "binary one-step local action mask and no reward, goal-distance,",
                "multi-step reachability, schema, tier, or future liftability lookahead.",
                "",
                "The result is diagnostic smoke/calibration evidence.",
                "",
            ]
        ),
        encoding="utf-8",
    )


def _write_runbook(readout_surface: Path) -> None:
    readout_surface.joinpath("runbook.md").write_text(
        "\n".join(
            [
                "# PlateSupport Direct-Star Cul-de-sac Control Runbook",
                "",
                "Run the diagnostic with:",
                "",
                "```text",
                "uv run python -m big_boy_benchmarking.cli plate-support "
                "direct-star-culdesac-control run \\",
                "  --repo-root . \\",
                "  --artifact-root docs/evaluations/plate_support_5x5_default_v001/"
                "direct_star_culdesac_control/artifacts/guarded_001 \\",
                "  --parent-gauntlet-source docs/evaluations/plate_support_5x5_default_v001/"
                "standard_gauntlet/readout_source.json \\",
                "  --run-label guarded_001 \\",
                "  --locked-by foster",
                "```",
                "",
                "Regenerate the human-readable readout with:",
                "",
                "```text",
                "execute docs/prime_directive/artifact_table_to_readable_document_protocol.md "
                "at docs/evaluations/plate_support_5x5_default_v001/"
                "direct_star_culdesac_control/readout_source.json",
                "```",
                "",
            ]
        ),
        encoding="utf-8",
    )


def _write_artifact_index(
    readout_surface: Path,
    output_paths: dict[str, str],
    badge_paths: dict[str, Path],
    readout_source_path: Path,
    repo_root: Path,
) -> None:
    rows = [
        "# PlateSupport Direct-Star Cul-de-sac Control Artifact Index",
        "",
        f"- `readout_source`: `{repo_placeholder(readout_source_path, repo_root)}`",
    ]
    rows.extend(
        f"- `{key}`: `{repo_placeholder(Path(value), repo_root)}`"
        for key, value in sorted(output_paths.items())
    )
    rows.extend(
        f"- `badge:{key}`: `{repo_placeholder(path, repo_root)}`"
        for key, path in sorted(badge_paths.items())
    )
    rows.append("")
    readout_surface.joinpath("artifact_index.md").write_text("\n".join(rows), encoding="utf-8")


def _write_result_readout(readout_surface: Path, interpretation_row: dict[str, object]) -> None:
    readout_surface.joinpath("result_readout.md").write_text(
        "\n".join(
            [
                "# PlateSupport Direct-Star Cul-de-sac Control Result Readout",
                "",
                f"- Interpretation case: `{interpretation_row.get('interpretation_case', '')}`",
                f"- Allowed claim: {interpretation_row.get('allowed_claim', '')}",
                f"- Blocked claim: {interpretation_row.get('blocked_claim', '')}",
                "",
                "The guarded direct controls are oracle one-step local controls.",
                "",
            ]
        ),
        encoding="utf-8",
    )


def _write_protocol_result_docs(
    readout_surface: Path,
    output_paths: dict[str, str],
    interpretation_row: dict[str, object],
) -> None:
    results_dir = readout_surface / "results"
    arm_rows = _read_csv(Path(output_paths["arm_summary"]))
    guard_rows = _read_csv(Path(output_paths["guard_filter_summary"]))
    action_rows = _read_csv(Path(output_paths["action_surface_summary"]))
    timing_rows = _read_csv(Path(output_paths["timing_summary"]))
    arm_by_id = {row.get("arm_id", ""): row for row in arm_rows}
    action_by_id = {row.get("arm_id", ""): row for row in action_rows}
    raw = arm_by_id.get("direct_raw", {})
    invalid = arm_by_id.get("direct_invalid_guard", {})
    nonself = arm_by_id.get("direct_nonself_guard", {})
    tower = arm_by_id.get("tower_selected_candidate", {})
    results_dir.joinpath("summary.md").write_text(
        "\n".join(
            [
                "# Direct-Star Diagnostic Summary",
                "",
                f"- Interpretation: `{interpretation_row.get('interpretation_case', '')}`",
                f"- Tower vs raw target delta: `{interpretation_row.get('tower_vs_raw_delta', '')}`",
                f"- Tower vs invalid-guard target delta: `{interpretation_row.get('tower_vs_invalid_guard_delta', '')}`",
                f"- Tower vs nonself-guard target delta: `{interpretation_row.get('tower_vs_nonself_guard_delta', '')}`",
                f"- Allowed claim: {interpretation_row.get('allowed_claim', '')}",
                f"- Blocked claim: {interpretation_row.get('blocked_claim', '')}",
                "",
            ]
        ),
        encoding="utf-8",
    )
    results_dir.joinpath("human_summary.md").write_text(
        "\n".join(
            [
                "# Human Summary",
                "",
                "The selected PlateSupport tower candidate outperformed raw direct learning,",
                "but it did not outperform either one-step guarded direct control. The",
                "strongest guarded direct arm, `direct_nonself_guard`, removed self-looping",
                "primitive actions before selection and achieved the highest binary target",
                "hit rate in this run.",
                "",
                "This supports Abdul Malik's concern that the prior tower-positive",
                "PlateSupport signal could be partly or mostly an action-filtering effect.",
                "",
            ]
        ),
        encoding="utf-8",
    )
    table_lines = [
        "# Arm Readout Table",
        "",
        "| Arm | Target Hit Rate | Mean Reward | Invalid Rate | Self-Transition Rate | Mean Available Actions |",
        "| --- | ---: | ---: | ---: | ---: | ---: |",
        _arm_markdown_row(raw, action_by_id.get("direct_raw", {})),
        _arm_markdown_row(invalid, action_by_id.get("direct_invalid_guard", {})),
        _arm_markdown_row(nonself, action_by_id.get("direct_nonself_guard", {})),
        _arm_markdown_row(tower, action_by_id.get("tower_selected_candidate", {})),
        "",
    ]
    results_dir.joinpath("arm_readout_table.md").write_text(
        "\n".join(table_lines),
        encoding="utf-8",
    )
    guard_lines = [
        "# Diagnostic Findings",
        "",
        "## Guard Filter Summary",
        "",
        "| Arm | Guard | Mean Before | Mean After | Invalid Filtered | Self-Loop Filtered |",
        "| --- | --- | ---: | ---: | ---: | ---: |",
    ]
    for row in guard_rows:
        guard_lines.append(
            "| "
            f"`{_cell(row, 'arm_id')}` | `{_cell(row, 'guard_type')}` | "
            f"{_cell(row, 'mean_available_before_guard')} | "
            f"{_cell(row, 'mean_available_after_guard')} | "
            f"{_cell(row, 'mean_invalid_filtered')} | "
            f"{_cell(row, 'mean_self_loop_filtered')} |"
        )
    guard_lines.extend(
        [
            "",
            "## Claim Effect",
            "",
            "The guarded controls are stronger than the tower on the binary target in this run,",
            "so the report blocks the claim that the prior tower advantage survived an",
            "equivalent decision-surface control.",
            "",
        ]
    )
    results_dir.joinpath("diagnostic_findings.md").write_text(
        "\n".join(guard_lines),
        encoding="utf-8",
    )
    timing_lines = [
        "# Timing Readout",
        "",
        "| Arm | Run Count | Total Duration Seconds |",
        "| --- | ---: | ---: |",
    ]
    timing_by_arm: dict[str, list[dict[str, str]]] = {}
    for row in timing_rows:
        timing_by_arm.setdefault(row.get("arm_id", ""), []).append(row)
    for arm_id, rows in sorted(timing_by_arm.items()):
        duration = sum(float(row.get("total_duration_seconds", "0") or 0) for row in rows)
        timing_lines.append(f"| `{arm_id}` | {len(rows)} | {duration} |")
    timing_lines.append("")
    results_dir.joinpath("timing_readout.md").write_text(
        "\n".join(timing_lines),
        encoding="utf-8",
    )


def _write_badges(badge_dir: Path, badge_rows: list[dict[str, object]]) -> dict[str, Path]:
    paths: dict[str, Path] = {}
    for row in badge_rows:
        badge_id = str(row["badge_id"])
        label = str(row["label"])
        value = str(row["value"])
        color = _color(str(row["color"]))
        path = badge_dir / f"{badge_id}.svg"
        label_width = max(50, 7 * len(label) + 18)
        value_width = max(70, 7 * len(value) + 18)
        width = label_width + value_width
        escaped_label = escape(label, quote=True)
        escaped_value = escape(value, quote=True)
        escaped_alt = escape(f"{label}: {value}", quote=True)
        escaped_color = escape(color, quote=True)
        path.write_text(
            "\n".join(
                [
                    '<svg xmlns="http://www.w3.org/2000/svg" '
                    f'width="{width}" height="20" role="img" aria-label="{escaped_alt}">',
                    f'<rect width="{label_width}" height="20" fill="#555"/>',
                    f'<rect x="{label_width}" width="{value_width}" height="20" fill="{escaped_color}"/>',
                    '<text x="'
                    f'{label_width / 2:.1f}" y="14" fill="#fff" '
                    'font-family="Verdana,Arial,sans-serif" font-size="11" '
                    f'text-anchor="middle">{escaped_label}</text>',
                    '<text x="'
                    f'{label_width + (value_width / 2):.1f}" y="14" fill="#fff" '
                    'font-family="Verdana,Arial,sans-serif" font-size="11" '
                    f'text-anchor="middle">{escaped_value}</text>',
                    "</svg>",
                    "",
                ]
            ),
            encoding="utf-8",
        )
        paths[badge_id] = path
    return paths


def _color(value: str) -> str:
    return {
        "green": "#2e7d32",
        "yellow": "#b58900",
        "orange": "#ef6c00",
        "blue": "#1565c0",
        "red": "#d32f2f",
        "gray": "#777",
    }.get(value, "#777")


def _read_csv(path: Path) -> list[dict[str, str]]:
    with path.open(encoding="utf-8", newline="") as handle:
        return list(csv.DictReader(handle))
