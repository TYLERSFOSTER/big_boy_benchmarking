"""Human-readable docs for Warehouse masked direct/live-lift tower diagnostics."""

from __future__ import annotations

from pathlib import Path
from typing import Any

from big_boy_benchmarking.artifacts.writers import write_json
from big_boy_benchmarking.environments.warehouse_gridlock.masked_direct_vs_live_lift_tower.config import (
    CANDIDATE_MIX_COORDINATION_READY,
    DIRECT_ARM_ID,
    EVALUATION_ID,
    DEFAULT_MAX_ACTIVE_ROBOTS,
    TOWER_ARM_ID,
)
from big_boy_benchmarking.environments.warehouse_gridlock.masked_direct_vs_live_lift_tower.paths import (
    EvaluationPaths,
)


def write_readout_source(
    *,
    paths: EvaluationPaths,
    run_label: str,
    summary: dict[str, object],
) -> Path:
    payload = {
        "repo_readout_surface": _rel(paths.repo_root, paths.readout_surface),
        "source_artifact_root": _rel(paths.repo_root, paths.artifact_root),
        "source_evaluation_root": _rel(paths.repo_root, paths.artifact_root),
        "evaluation_id": EVALUATION_ID,
        "environment_instance_id": "warehouse_gridlock_16x16_v001",
        "artifact_run_label": run_label,
        "artifact_schema_version": "v1",
        "run_mode": "smoke" if run_label.startswith("smoke") else "diagnostic",
        "source_files": {
            "aggregate_summary": _rel(paths.repo_root, paths.aggregate_summary),
            "aggregate_table": _rel(paths.repo_root, paths.aggregate_table),
            "run_index": _rel(paths.repo_root, paths.run_index),
            "arm_summary": _rel(paths.repo_root, paths.results_dir / "arm_summary.csv"),
            "paired_summary": _rel(paths.repo_root, paths.results_dir / "paired_summary.csv"),
            "target_progress_summary": _rel(
                paths.repo_root, paths.results_dir / "target_progress_summary.csv"
            ),
            "admissibility_query_summary": _rel(
                paths.repo_root, paths.results_dir / "admissibility_query_summary.csv"
            ),
            "candidate_family_summary": _rel(
                paths.repo_root, paths.results_dir / "candidate_family_summary.csv"
            ),
            "tower_live_lift_summary": _rel(
                paths.repo_root, paths.results_dir / "tower_live_lift_summary.csv"
            ),
            "no_lookahead_audit_summary": _rel(
                paths.repo_root, paths.results_dir / "no_lookahead_audit_summary.csv"
            ),
            "tower_shape_summary": _rel(
                paths.repo_root, paths.results_dir / "tower_shape_summary.csv"
            ),
            "tower_surface_scope_summary": _rel(
                paths.repo_root, paths.results_dir / "tower_surface_scope_summary.csv"
            ),
            "direct_candidate_events": _rel(
                paths.repo_root, paths.results_dir / "direct_candidate_events.csv"
            ),
        },
        "artifact_storage": {
            "mode": "git_tracked",
            "release_tag": None,
            "asset_name": None,
            "bundle_manifest_path": None,
        },
        "expected_files": {
            "required": [
                "evaluation_manifest.json",
                "evaluation_budget_lock.json",
                "evaluation_input_manifest.json",
                "dependency_manifest.json",
                "arm_manifest.json",
                "candidate_generation_manifest.json",
                "admissibility_policy_manifest.json",
                "live_lift_policy_manifest.json",
                "no_lookahead_policy_manifest.json",
                "run_index.csv",
                "results/arm_summary.csv",
                "results/paired_summary.csv",
                "results/admissibility_query_summary.csv",
                "results/candidate_family_summary.csv",
                "results/tower_live_lift_summary.csv",
                "results/no_lookahead_audit_summary.csv",
            ],
            "expected_absent_is_gap": [],
            "conditional": {},
            "not_applicable": ["full_action_space_enumeration"],
            "expectation_sources": [
                "docs/design/svg_physical_system_designs/warehouse_gridlock_001/01_masked_direct_vs_live_lift_tower_no_lookahead/01_002_warehouse_gridlock_masked_direct_vs_live_lift_tower_no_lookahead_implementation_workplan.md"
            ],
        },
        "goal_criteria": [
            {
                "goal_id": "score_direction",
                "question": "What was the direct-vs-tower score direction under the checked budget?",
                "success_signal": "evaluation_aggregate_summary.json score_direction is direct, tower, or tie",
                "partial_signal": "score_direction is inconclusive",
                "failure_signal": "score_direction is blocked",
                "claim_if_met": "bounded diagnostic score direction under candidate-set masking",
                "claim_if_not_met": "no score direction claim",
            },
            {
                "goal_id": "equal_immediate_masking",
                "question": "Did both arms use immediate inadmissibility masks?",
                "success_signal": "admissibility_query_summary has both active arms",
                "partial_signal": "one arm has incomplete mask counts",
                "failure_signal": "one active arm is missing from mask summary",
                "claim_if_met": "both arms were protected from selected impossible moves",
                "claim_if_not_met": "comparison fairness is blocked",
            },
            {
                "goal_id": "no_successor_lookahead",
                "question": "Did either arm use successor Out for selection?",
                "success_signal": "successor_out_used_for_selection_count is zero for both arms",
                "partial_signal": "successor Out rows are missing",
                "failure_signal": "any successor_out_used_for_selection_count is nonzero",
                "claim_if_met": "no one-step successor cul-de-sac lookahead was used",
                "claim_if_not_met": "comparison is blocked",
            },
            {
                "goal_id": "tower_live_lift",
                "question": "Did tower use live state-lift hygiene?",
                "success_signal": "tower_live_lift_summary reports selected live lifts",
                "partial_signal": "tower live lifts are present with failures",
                "failure_signal": "tower live-lift rows are missing",
                "claim_if_met": "tower state lifts avoided already-dead upstairs representatives",
                "claim_if_not_met": "tower lift behavior is not interpretable",
            },
            {
                "goal_id": "coordination_ready_candidate_surface",
                "question": "Did the generated surface expose multi-robot ensemble proposals early enough for a long run?",
                "success_signal": "direct_candidate_events includes candidate_family values beyond one_active under the configured budget",
                "partial_signal": "multi-robot candidate rows are present but rare",
                "failure_signal": "candidate rows contain only all_stay and one_active proposals",
                "claim_if_met": "the run can test bounded coordinated-ensemble discovery",
                "claim_if_not_met": "the run remains smoke-only for coordinated gridlock behavior",
            },
        ],
        "badge_policy": {
            "dimensions": [
                "artifact_status",
                "score_direction",
                "admissibility_masking",
                "one_step_lookahead",
                "tower_live_lift",
                "candidate_family_status",
                "mask_scope",
                "claim_scope",
                "provenance_status",
            ]
        },
        "goal_summary_sources": [
            "docs/design/svg_physical_system_designs/warehouse_gridlock_001/01_masked_direct_vs_live_lift_tower_no_lookahead/01_001_warehouse_gridlock_masked_direct_vs_live_lift_tower_no_lookahead_blueprint.md"
        ],
        "methodology_summary_sources": [
            "docs/evaluations/warehouse_gridlock_001/masked_direct_vs_live_lift_tower/method.md"
        ],
        "structural_limit_checks": [
            {
                "check_id": "full_action_space_not_enumerated",
                "trigger": "tower_surface_scope_summary complete_full_action_surface=false",
                "interpretation_if_triggered": "the evaluation used bounded generated candidate surfaces",
                "claim_effect": "blocks full-MDP tower coverage claims",
            }
        ],
        "claim_boundary": summary.get("claim_boundary", []),
        "summary": summary,
    }
    write_json(paths.repo_readout_source, payload, create_parents=True)
    write_json(paths.artifact_readout_source, payload, create_parents=True)
    return paths.repo_readout_source


def write_human_docs(
    *,
    paths: EvaluationPaths,
    run_label: str,
    summary: dict[str, object],
) -> dict[str, str]:
    paths.readout_surface.mkdir(parents=True, exist_ok=True)
    paths.docs_results_dir.mkdir(parents=True, exist_ok=True)
    paths.badges_dir.mkdir(parents=True, exist_ok=True)
    badges = _write_badges(paths=paths, summary=summary)
    docs = {
        "README.md": paths.readout_surface / "README.md",
        "result_readout.md": paths.readout_surface / "result_readout.md",
        "method.md": paths.readout_surface / "method.md",
        "runbook.md": paths.readout_surface / "runbook.md",
        "glossary.md": paths.readout_surface / "glossary.md",
        "artifact_index.md": paths.readout_surface / "artifact_index.md",
        "results/summary.md": paths.docs_results_dir / "summary.md",
        "results/score_readout.md": paths.docs_results_dir / "score_readout.md",
        "results/fairness_audit.md": paths.docs_results_dir / "fairness_audit.md",
        "results/candidate_generation_readout.md": paths.docs_results_dir
        / "candidate_generation_readout.md",
        "results/tower_construction_readout.md": paths.docs_results_dir
        / "tower_construction_readout.md",
        "results/no_lookahead_audit.md": paths.docs_results_dir / "no_lookahead_audit.md",
        "results/timing_readout.md": paths.docs_results_dir / "timing_readout.md",
    }
    _write(docs["README.md"], _readme(run_label=run_label, summary=summary, badges=badges))
    _write(docs["result_readout.md"], _result_readout(summary))
    _write(docs["method.md"], _method())
    _write(docs["runbook.md"], _runbook(run_label))
    _write(docs["glossary.md"], _glossary())
    _write(docs["artifact_index.md"], _artifact_index(paths))
    _write(docs["results/summary.md"], _results_summary(summary))
    _write(docs["results/score_readout.md"], _score_readout(summary))
    _write(docs["results/fairness_audit.md"], _fairness_audit())
    _write(docs["results/candidate_generation_readout.md"], _candidate_readout())
    _write(docs["results/tower_construction_readout.md"], _tower_readout())
    _write(docs["results/no_lookahead_audit.md"], _no_lookahead_readout())
    _write(docs["results/timing_readout.md"], "# Timing Readout\n\nSee raw `timing_segments.csv` files per run.\n")
    return {key: str(value) for key, value in docs.items()}


def _readme(*, run_label: str, summary: dict[str, object], badges: dict[str, str]) -> str:
    badge_lines = " ".join(
        f"![{Path(path).stem}]({Path(path).relative_to(Path(path).parents[1])})"
        for path in badges.values()
    )
    return f"""# Warehouse Gridlock Masked Direct vs Live-Lift Tower

{badge_lines}

## Result

{summary.get("main_result_sentence", "No result sentence available.")}

Run label: `{run_label}`.

This is diagnostic evidence only. It compares `{DIRECT_ARM_ID}` against
`{TOWER_ARM_ID}` under immediate inadmissibility masking for both arms.

The serious-run-ready candidate policy is
`{CANDIDATE_MIX_COORDINATION_READY}`. It interleaves one-robot and multi-robot
ensemble proposals inside the bounded candidate budget so long runs can test
coordinated gridlock discovery. The old smoke-only failure mode was a budget
that mostly exposed one-active-robot moves.

Candidate family status: `{summary.get("candidate_family_status", "unknown")}`.

## Fairness Boundary

Both arms use immediate inadmissibility masks over generated candidate sets.
Neither arm uses one-step successor-state cul-de-sac lookahead.

This evaluation does not implement Abdul-style direct* or tower* one-hop
cul-de-sac guards. Successor-state Out may be recorded for diagnosis, but it is
not used for action selection.

Tower live lifting is a state-lift hygiene rule. It prevents selecting an
already-dead upstairs representative for a fixed downstairs state. It is not a
single-tier action-successor lookahead rule.

## Scope

The Warehouse full primitive action surface is `5^32`, so this evaluation does
not enumerate the full action space. Direct and tower masks are exact over
their generated candidate sets unless a future run explicitly proves a larger
surface.

## Key Files

- `readout_source.json`
- `result_readout.md`
- `method.md`
- `results/score_readout.md`
- `results/fairness_audit.md`
- `results/tower_construction_readout.md`

## Clarifying Conversation

### Evaluator Turn

Add questions or concerns about this generated readout here.

### Codex Turn

Pending.
"""


def _result_readout(summary: dict[str, object]) -> str:
    return f"""# Result Readout

Score direction: `{summary.get("score_direction")}`.

Fairness audit status: `{summary.get("fairness_audit_status")}`.

No-lookahead status: `{summary.get("no_lookahead_status")}`.

Mask scope: `{summary.get("mask_scope_summary")}`.

Tower surface scope: `{summary.get("tower_surface_scope_summary")}`.

{summary.get("main_result_sentence", "")}
"""


def _method() -> str:
    return """# Method

This diagnostic runs two active Warehouse Gridlock arms:

- direct concrete control with immediate inadmissibility masking;
- tower control over a scoped generated/discovered surface with live state-lift
  hygiene.

Both arms receive bounded generated candidate sets. Candidate masks are exact
over those generated sets, not over the full `5^32` action surface. The tower
surface is built from generated states, generated concrete candidates, and
valid immediate transitions under the Warehouse transition engine.

The default candidate generator is coordination-ready sparse generation:
`{CANDIDATE_MIX_COORDINATION_READY}` with `max_active_robots` defaulting to
`{DEFAULT_MAX_ACTIVE_ROBOTS}`. This does not enumerate the full action space.
It deterministically samples bounded one-active and multi-active ensemble
proposals and interleaves them, so a fixed candidate budget can contain
coordinated robot moves.

Successor `Out` may be observed after an action is selected and executed for
diagnosis. It is not used for action selection.
"""


def _runbook(run_label: str) -> str:
    smoke_flag = " \\\n  --smoke" if run_label.startswith("smoke") else ""
    candidate_budget = 64 if run_label.startswith("smoke") else 256
    max_active_robots = DEFAULT_MAX_ACTIVE_ROBOTS if run_label.startswith("smoke") else 8
    return f"""# Runbook

```bash
uv run python -m big_boy_benchmarking.cli warehouse-gridlock masked-direct-vs-live-lift-tower run \\
  --repo-root . \\
  --artifact-root docs/evaluations/warehouse_gridlock_001/masked_direct_vs_live_lift_tower/artifacts/{run_label} \\
  --readiness-source docs/evaluations/warehouse_gridlock_001/environment_readiness/readout_source.json \\
  --run-label {run_label} \\
  --locked-by foster \\
  --candidate-proposals-per-step {candidate_budget} \\
  --max-active-robots {max_active_robots} \\
  --candidate-mix-id {CANDIDATE_MIX_COORDINATION_READY}{smoke_flag}

uv run python -m big_boy_benchmarking.cli warehouse-gridlock masked-direct-vs-live-lift-tower summarize \\
  --repo-root . \\
  --artifact-root docs/evaluations/warehouse_gridlock_001/masked_direct_vs_live_lift_tower/artifacts/{run_label}
```

For the long diagnostic run, use a non-smoke run label and do not pass
`--smoke`. The important serious-run knobs are:

```text
--episodes-per-arm <large budget>
--replicates-per-arm <replicate budget>
--max-seconds-per-episode <warehouse time horizon>
--candidate-proposals-per-step 256
--max-active-robots 8
--candidate-mix-id {CANDIDATE_MIX_COORDINATION_READY}
```

Human-readable regeneration prompt:

```text
execute docs/prime_directive/artifact_table_to_readable_document_protocol.md at docs/evaluations/warehouse_gridlock_001/masked_direct_vs_live_lift_tower/readout_source.json
```
"""


def _glossary() -> str:
    return """# Glossary

- Immediate inadmissibility mask: removes generated candidate actions that are
  invalid in the current Warehouse state.
- Generated candidate set: bounded proposal set considered by an arm.
- Coordination-ready candidate set: bounded generated proposal set that
  deliberately interleaves one-active and multi-active robot ensembles.
- Live lift: an upstairs representative over a fixed downstairs state whose
  scoped generated `Out` is nonempty.
- Successor lookahead: using the successor state's outgoing actions to decide
  whether to choose the current action. This evaluation forbids it.
"""


def _artifact_index(paths: EvaluationPaths) -> str:
    return f"""# Artifact Index

- Raw artifacts: `{_rel(paths.repo_root, paths.artifact_root)}`
- Readout source: `readout_source.json`
- Aggregate summary: `{_rel(paths.repo_root, paths.aggregate_summary)}`
- Results tables: `{_rel(paths.repo_root, paths.results_dir)}`
"""


def _results_summary(summary: dict[str, object]) -> str:
    return f"""# Results Summary

{summary.get("main_result_sentence", "")}

Claim boundary: diagnostic evidence only.
"""


def _score_readout(summary: dict[str, object]) -> str:
    return f"""# Score Readout

Score direction: `{summary.get("score_direction")}`.

The score direction is audit-gated. If no-lookahead or mask evidence fails, the
score direction is blocked.
"""


def _fairness_audit() -> str:
    return """# Fairness Audit

The required fairness evidence lives in:

- `results/admissibility_query_summary.csv`
- `results/direct_mask_summary.csv`
- `results/tower_live_lift_summary.csv`
- `results/no_lookahead_audit_summary.csv`

Both active arms must appear in the admissibility summary. Both active arms
must report zero successor-Out uses for selection.
"""


def _candidate_readout() -> str:
    return """# Candidate Generation Readout

Direct candidates are sparse generated concrete ensemble actions. The serious
candidate policy is coordination-ready: bounded proposals interleave
one-active and multi-active robot ensembles instead of spending the early
budget entirely on one-active moves.

The quick audit table is:

```text
results/candidate_family_summary.csv
```

Tower candidates are generated from the scoped tower surface and must still
resolve to concrete Warehouse ensemble actions. Tower candidate generation is
bounded and must not be interpreted as full tower action-surface enumeration.
"""


def _tower_readout() -> str:
    return """# Tower Construction Readout

Warehouse Gridlock does not expose a complete serious MDP graph. The tower in
this diagnostic is constructed over a scoped generated/discovered surface:
generated states, generated concrete candidates, and valid immediate
transitions observed or queried under the Warehouse transition engine.

This blocks claims about a full-MDP tower while allowing a first diagnostic of
live state-lift hygiene.
"""


def _no_lookahead_readout() -> str:
    return """# No-Lookahead Audit

The selected-action audit must have:

```text
successor_out_count_used_for_selection=false
```

for both arms on every selected step.
"""


def _write_badges(*, paths: EvaluationPaths, summary: dict[str, object]) -> dict[str, str]:
    badge_values = {
        "environment": "warehouse",
        "score_direction": str(summary.get("score_direction", "unknown")),
        "candidate_family": str(summary.get("candidate_family_status", "unknown")),
        "admissibility_masking": "both-arms",
        "one_step_lookahead": "disabled",
        "tower_live_lift": "enabled",
        "mask_scope": "candidate-set",
        "claim_status": "diagnostic",
        "artifact_status": str(summary.get("status", "unknown")),
    }
    colors = {
        "tower": "#2e7d32",
        "direct": "#ef6c00",
        "tie": "#6a1b9a",
        "disabled": "#2e7d32",
        "enabled": "#2e7d32",
        "both-arms": "#2e7d32",
        "candidate-set": "#ef6c00",
        "coordination_ready": "#2e7d32",
        "one_active_only": "#ef6c00",
        "all_stay_only": "#c62828",
        "diagnostic": "#1565c0",
        "success": "#2e7d32",
    }
    output: dict[str, str] = {}
    for label, value in badge_values.items():
        path = paths.badges_dir / f"{label}.svg"
        _write(path, _badge_svg(label, value, colors.get(value, "#555")))
        output[label] = str(path)
    return output


def _badge_svg(label: str, value: str, color: str) -> str:
    label_width = max(70, len(label) * 7)
    value_width = max(70, len(value) * 7)
    width = label_width + value_width
    return (
        f'<svg xmlns="http://www.w3.org/2000/svg" width="{width}" height="20" '
        f'role="img" aria-label="{label}: {value}"><title>{label}: {value}</title>'
        f'<rect width="{label_width}" height="20" fill="#555"/>'
        f'<rect x="{label_width}" width="{value_width}" height="20" fill="{color}"/>'
        '<g fill="#fff" text-anchor="middle" '
        'font-family="Verdana,Geneva,DejaVu Sans,sans-serif" font-size="11">'
        f'<text x="{label_width / 2}" y="14">{label}</text>'
        f'<text x="{label_width + value_width / 2}" y="14">{value}</text>'
        "</g></svg>\n"
    )


def _write(path: Path, text: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(text, encoding="utf-8")


def _rel(repo_root: Path, path: Path) -> str:
    try:
        return str(path.relative_to(repo_root))
    except ValueError:
        return str(path)
