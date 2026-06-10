"""Human-readable docs for Warehouse full-state policy comparison."""

from __future__ import annotations

from pathlib import Path

from big_boy_benchmarking.artifacts.writers import write_json
from big_boy_benchmarking.environments.warehouse_gridlock.full_state_policy_comparison.config import (
    DIRECT_ARM_ID,
    EVALUATION_ID,
    TOWER_ARM_ID,
)
from big_boy_benchmarking.environments.warehouse_gridlock.full_state_policy_comparison.paths import (
    EvaluationPaths,
)
from big_boy_benchmarking.environments.warehouse_gridlock.policies import (
    MODEL_FAMILY_ID,
    POLICY_CONTRACT_ID,
    PROJECTION_STRATEGY_ID,
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
        "run_mode": "trainable_policy_smoke" if "smoke" in run_label else "trainable_policy_pilot",
        "source_files": {
            "aggregate_summary": _rel(paths.repo_root, paths.aggregate_summary),
            "aggregate_table": _rel(paths.repo_root, paths.aggregate_table),
            "run_index": _rel(paths.repo_root, paths.run_index),
            "arm_summary": _rel(paths.repo_root, paths.results_dir / "arm_summary.csv"),
            "paired_summary": _rel(paths.repo_root, paths.results_dir / "paired_summary.csv"),
            "learning_health_summary": _rel(
                paths.repo_root, paths.results_dir / "learning_health_summary.csv"
            ),
            "learning_curve_summary": _rel(
                paths.repo_root, paths.results_dir / "learning_curve_summary.csv"
            ),
            "policy_reuse_summary": _rel(
                paths.repo_root, paths.results_dir / "policy_reuse_summary.csv"
            ),
            "mask_projection_summary": _rel(
                paths.repo_root, paths.results_dir / "mask_projection_summary.csv"
            ),
            "no_lookahead_audit_summary": _rel(
                paths.repo_root, paths.results_dir / "no_lookahead_audit_summary.csv"
            ),
            "tower_live_lift_summary": _rel(
                paths.repo_root, paths.results_dir / "tower_live_lift_summary.csv"
            ),
            "tower_shape_summary": _rel(paths.repo_root, paths.results_dir / "tower_shape_summary.csv"),
            "progress_events": _rel(paths.repo_root, paths.progress_events),
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
                "evaluation_arm_manifest.json",
                "environment_instance_manifest.json",
                "policy_contract_manifest.json",
                "policy_model_manifest.json",
                "policy_training_manifest.json",
                "admissibility_resolver_manifest.json",
                "tower_policy_manifest.json",
                "tower_construction_manifest.json",
                "run_index.csv",
                "results/arm_summary.csv",
                "results/paired_summary.csv",
                "results/learning_health_summary.csv",
                "results/learning_curve_summary.csv",
                "results/policy_reuse_summary.csv",
                "results/mask_projection_summary.csv",
                "results/no_lookahead_audit_summary.csv",
            ],
            "expected_absent_is_gap": [],
            "conditional": {
                "tower_only": [
                    "results/tower_live_lift_summary.csv",
                    "results/tower_shape_summary.csv",
                ]
            },
            "not_applicable": [
                "backprop_gradient_events",
                "full_action_space_enumeration",
            ],
            "expectation_sources": [
                "docs/design/svg_physical_system_designs/warehouse_gridlock_001/02_full_state_full_action_trainable_policy_contract/01_002_warehouse_gridlock_full_state_full_action_trainable_policy_contract_implementation_workplan.md"
            ],
        },
        "goal_criteria": [
            {
                "goal_id": "real_learning_signal",
                "question": "Did both arms produce reusable non-nominal learning evidence?",
                "success_signal": "learning_health_summary.csv learning_status is real_learning_signal_present for both arms",
                "partial_signal": "one arm passes and one arm fails learning health",
                "failure_signal": "any arm is nominal_updates_only, no_updates, or failed",
                "claim_if_met": "both arms used trainable reusable policy state in the smoke run",
                "claim_if_not_met": "the run is not a real learning comparison",
            },
            {
                "goal_id": "full_state_full_action_contract",
                "question": "Did policies consume full Warehouse state plus second and emit full action vectors?",
                "success_signal": "policy_contract_manifest plus policy_decision_events with full action hashes",
                "partial_signal": "contract rows exist but action hashes are incomplete",
                "failure_signal": "policy decision rows are missing",
                "claim_if_met": "the PO-specified policy contract is implemented",
                "claim_if_not_met": "policy contract implementation is blocked",
            },
            {
                "goal_id": "no_successor_lookahead",
                "question": "Did either arm use successor Out for selection?",
                "success_signal": "successor_out_count_used_for_selection_count is zero for both arms",
                "partial_signal": "audit rows are present for only one arm",
                "failure_signal": "any successor_out_count_used_for_selection_count is nonzero",
                "claim_if_met": "no one-hop successor cul-de-sac lookahead was used",
                "claim_if_not_met": "comparison fairness is blocked",
            },
        ],
        "badge_policy": {
            "dimensions": [
                "artifact_status",
                "learning_signal",
                "behavioral_status",
                "fairness_status",
                "no_lookahead_status",
                "provenance_status",
            ]
        },
        "goal_summary_sources": [
            "docs/design/svg_physical_system_designs/warehouse_gridlock_001/02_full_state_full_action_trainable_policy_contract/01_001_warehouse_gridlock_full_state_full_action_trainable_policy_contract_blueprint.md"
        ],
        "methodology_summary_sources": [
            "docs/evaluations/warehouse_gridlock_001/full_state_policy_comparison/method.md",
            "docs/evaluations/warehouse_gridlock_001/full_state_policy_comparison/runbook.md",
        ],
        "structural_limit_checks": [
            {
                "check_id": "not_backprop",
                "trigger": "policy_model_manifest neural_or_backprop=false",
                "interpretation_if_triggered": "the run uses a linear trainable model, not neural backprop",
                "claim_effect": "blocks backprop claims",
            },
            {
                "check_id": "full_action_space_not_enumerated",
                "trigger": "tower_construction_manifest complete_full_action_surface=false",
                "interpretation_if_triggered": "the tower arm uses a scoped generated/discovered surface",
                "claim_effect": "blocks full-MDP tower coverage claims",
            },
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
        "method.md": paths.readout_surface / "method.md",
        "runbook.md": paths.readout_surface / "runbook.md",
        "artifact_index.md": paths.readout_surface / "artifact_index.md",
        "result_readout.md": paths.readout_surface / "result_readout.md",
        "results/summary.md": paths.docs_results_dir / "summary.md",
        "results/human_summary.md": paths.docs_results_dir / "human_summary.md",
        "results/learning_health_readout.md": paths.docs_results_dir / "learning_health_readout.md",
        "results/policy_reuse_readout.md": paths.docs_results_dir / "policy_reuse_readout.md",
        "results/fairness_audit.md": paths.docs_results_dir / "fairness_audit.md",
        "results/no_lookahead_audit.md": paths.docs_results_dir / "no_lookahead_audit.md",
    }
    _write(docs["README.md"], _readme(run_label=run_label, summary=summary, badges=badges))
    _write(docs["method.md"], _method())
    _write(docs["runbook.md"], _runbook(run_label))
    _write(docs["artifact_index.md"], _artifact_index(paths))
    _write(docs["result_readout.md"], _result_readout(summary))
    _write(docs["results/summary.md"], _result_readout(summary))
    _write(docs["results/human_summary.md"], _result_readout(summary))
    _write(docs["results/learning_health_readout.md"], _learning_health_readout())
    _write(docs["results/policy_reuse_readout.md"], _policy_reuse_readout())
    _write(docs["results/fairness_audit.md"], _fairness_audit())
    _write(docs["results/no_lookahead_audit.md"], _no_lookahead_audit())
    return {key: str(value) for key, value in docs.items()}


def _readme(*, run_label: str, summary: dict[str, object], badges: dict[str, str]) -> str:
    badge_line = " ".join(f"![{Path(path).stem}]({Path(path).as_posix()})" for path in badges)
    return f"""# Warehouse Gridlock Full-State Policy Comparison

{badge_line}

## Status At A Glance

- Evaluation id: `{EVALUATION_ID}`.
- Run label: `{run_label}`.
- Learning contract status: `{summary.get("learning_contract_status", "unknown")}`.
- Score direction: `{summary.get("score_direction", "unknown")}`.
- No-lookahead status: `{summary.get("no_lookahead_status", "unknown")}`.

## Summary of Goals Behind this Evaluation

This evaluation corrects the previous Warehouse masked direct vs. live-lift
tower diagnostic by replacing candidate-id keyed nominal updates with a real
trainable policy contract.

The Project Owner's active model contract is:

```text
full system configuration + current second -> full simultaneous action vector
```

Both arms use `{MODEL_FAMILY_ID}`. This is a trainable linear/factorized model,
not neural backprop.

## Summary of Methodology Behind this Evaluation

The direct arm is `{DIRECT_ARM_ID}`. It receives full concrete Warehouse state,
the current second, and emits a full concrete action vector before the shared
immediate-admissibility resolver selects a valid concrete vector.

The tower arm is `{TOWER_ARM_ID}`. It preserves live state-lift hygiene and uses
the scoped generated/discovered tower surface, but concrete action selection is
scored through reusable feature weights rather than opaque candidate ids.

Neither arm uses one-hop successor-state cul-de-sac lookahead.

## Claim Boundary

This run may support policy-contract and learning-health claims only. It may
not claim Warehouse is solved, tower is better in general, backprop happened,
or the full serious MDP was enumerated.

## Evidence Map

- `readout_source.json`: source binding for human-readable regeneration.
- `artifacts/{run_label}/results/learning_health_summary.csv`: whether updates
  became real reusable learning.
- `artifacts/{run_label}/results/policy_reuse_summary.csv`: prior-signal reuse.
- `artifacts/{run_label}/results/no_lookahead_audit_summary.csv`: no-lookahead
  audit.
- `artifacts/{run_label}/results/arm_summary.csv`: arm-level behavior.
"""


def _method() -> str:
    return f"""# Method

This evaluation implements `{POLICY_CONTRACT_ID}` for Warehouse Gridlock.

The first model family is `{MODEL_FAMILY_ID}`. It scores robot commands from
full-state features and updates reusable feature weights online. It is not a
backprop/neural model.

The concrete resolver is `{PROJECTION_STRATEGY_ID}`. It uses immediate
transition validity only and logs repairs/projections. It does not inspect
successor `Out`.
"""


def _runbook(run_label: str) -> str:
    return f"""# Runbook

## Run Smoke

```bash
uv run python -m big_boy_benchmarking.cli warehouse-gridlock full-state-policy-comparison run \\
  --repo-root . \\
  --artifact-root docs/evaluations/warehouse_gridlock_001/full_state_policy_comparison/artifacts/{run_label} \\
  --readiness-source docs/evaluations/warehouse_gridlock_001/environment_readiness/readout_source.json \\
  --run-label {run_label} \\
  --locked-by foster \\
  --episodes-per-arm 4 \\
  --replicates-per-arm 1 \\
  --schema-seeds 1 \\
  --max-seconds-per-episode 128 \\
  --projection-attempt-budget 64 \\
  --progress-every-episodes 1
```

## Summarize

```bash
uv run python -m big_boy_benchmarking.cli warehouse-gridlock full-state-policy-comparison summarize \\
  --repo-root . \\
  --artifact-root docs/evaluations/warehouse_gridlock_001/full_state_policy_comparison/artifacts/{run_label}
```

## Regenerate Human-Readable Readout

```text
execute docs/prime_directive/artifact_table_to_readable_document_protocol.md at docs/evaluations/warehouse_gridlock_001/full_state_policy_comparison/readout_source.json
```
"""


def _artifact_index(paths: EvaluationPaths) -> str:
    return f"""# Artifact Index

- Readout source: `{_rel(paths.repo_root, paths.repo_readout_source)}`.
- Artifact root: `{_rel(paths.repo_root, paths.artifact_root)}`.
- Aggregate summary: `{_rel(paths.repo_root, paths.aggregate_summary)}`.
- Results directory: `{_rel(paths.repo_root, paths.results_dir)}`.
"""


def _result_readout(summary: dict[str, object]) -> str:
    return f"""# Result Readout

- Status: `{summary.get("status", "unknown")}`.
- Learning contract status: `{summary.get("learning_contract_status", "unknown")}`.
- Score direction: `{summary.get("score_direction", "unknown")}`.
- No-lookahead status: `{summary.get("no_lookahead_status", "unknown")}`.

Inspect `results/learning_health_summary.csv` before treating this as a real
learning comparison.
"""


def _learning_health_readout() -> str:
    return """# Learning Health Readout

The key table is `results/learning_health_summary.csv`.

A run with update rows but no prior learned signal reuse is classified as
`nominal_updates_only`, not as successful training.
"""


def _policy_reuse_readout() -> str:
    return """# Policy Reuse Readout

The key table is `results/policy_reuse_summary.csv`.

This table exists to prevent repeating the candidate-id learner failure from
the earlier Warehouse diagnostic.
"""


def _fairness_audit() -> str:
    return """# Fairness Audit

Both arms receive immediate inadmissibility resolution. Neither arm should
select an invalid concrete Warehouse action as an environment step.
"""


def _no_lookahead_audit() -> str:
    return """# No-Lookahead Audit

The key table is `results/no_lookahead_audit_summary.csv`.

`successor_out_count_used_for_selection_count` must be zero for both arms.
"""


def _write_badges(*, paths: EvaluationPaths, summary: dict[str, object]) -> list[str]:
    specs = [
        ("artifacts_complete", "Artifacts", "Complete", "#2f855a"),
        (
            "learning_signal",
            "Learning",
            str(summary.get("learning_contract_status", "unknown")).title(),
            "#2f855a" if summary.get("learning_contract_status") == "passed" else "#b7791f",
        ),
        ("scope_policy", "Scope", "Policy Smoke", "#4a5568"),
        (
            "no_lookahead",
            "No Lookahead",
            str(summary.get("no_lookahead_status", "unknown")).title(),
            "#2f855a" if summary.get("no_lookahead_status") == "passed" else "#c53030",
        ),
        ("provenance_repo_artifacts", "Provenance", "Repo Artifacts", "#2b6cb0"),
    ]
    paths_out: list[str] = []
    for filename, label, value, color in specs:
        path = paths.badges_dir / f"{filename}.svg"
        _write(path, _badge_svg(label=label, value=value, color=color))
        paths_out.append(f"badges/{path.name}")
    return paths_out


def _badge_svg(*, label: str, value: str, color: str) -> str:
    width = max(120, 7 * (len(label) + len(value)) + 30)
    split = max(58, 7 * len(label) + 18)
    return f"""<svg xmlns="http://www.w3.org/2000/svg" width="{width}" height="20" role="img" aria-label="{label}: {value}">
  <linearGradient id="s" x2="0" y2="100%">
    <stop offset="0" stop-color="#bbb" stop-opacity=".1"/>
    <stop offset="1" stop-opacity=".1"/>
  </linearGradient>
  <rect rx="3" width="{width}" height="20" fill="#555"/>
  <rect rx="3" x="{split}" width="{width - split}" height="20" fill="{color}"/>
  <path fill="{color}" d="M{split} 0h4v20h-4z"/>
  <rect rx="3" width="{width}" height="20" fill="url(#s)"/>
  <g fill="#fff" text-anchor="middle" font-family="Verdana,Geneva,DejaVu Sans,sans-serif" font-size="11">
    <text x="{split / 2}" y="15" fill="#010101" fill-opacity=".3">{label}</text>
    <text x="{split / 2}" y="14">{label}</text>
    <text x="{split + (width - split) / 2}" y="15" fill="#010101" fill-opacity=".3">{value}</text>
    <text x="{split + (width - split) / 2}" y="14">{value}</text>
  </g>
</svg>
"""


def _write(path: Path, content: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(content, encoding="utf-8")


def _rel(repo_root: Path, path: Path) -> str:
    try:
        return path.relative_to(repo_root).as_posix()
    except ValueError:
        return path.as_posix()
