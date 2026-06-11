"""Readout source and lightweight docs for Warehouse transformer policy runs."""

from __future__ import annotations

from pathlib import Path

from big_boy_benchmarking.artifacts.writers import write_json

from .config import EVALUATION_ID, MODEL_FAMILY_ID
from .paths import TransformerEvaluationPaths


def write_readout_source(
    *,
    paths: TransformerEvaluationPaths,
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
        "run_mode": (
            "transformer_policy_smoke"
            if "smoke" in run_label
            else "transformer_policy_training"
        ),
        "model_family_id": MODEL_FAMILY_ID,
        "protocol_invocation": (
            "execute docs/prime_directive/artifact_table_to_readable_document_protocol.md "
            "at docs/evaluations/warehouse_gridlock_001/transformer_policy/readout_source.json"
        ),
        "source_files": {
            "aggregate_summary": _rel(paths.repo_root, paths.aggregate_summary),
            "run_index": _rel(paths.repo_root, paths.run_index),
            "episode_summary": _rel(paths.repo_root, paths.results_dir / "episode_summary.csv"),
            "training_curve_summary": _rel(
                paths.repo_root, paths.results_dir / "training_curve_summary.csv"
            ),
            "checkpoint_summary": _rel(
                paths.repo_root, paths.results_dir / "checkpoint_summary.csv"
            ),
            "trace_episode_index": _rel(
                paths.repo_root, paths.results_dir / "trace_episode_index.csv"
            ),
            "resolver_summary": _rel(paths.repo_root, paths.results_dir / "resolver_summary.csv"),
            "tower_live_lift_summary": _rel(
                paths.repo_root, paths.results_dir / "tower_live_lift_summary.csv"
            ),
            "curriculum_summary": _rel(
                paths.repo_root, paths.results_dir / "curriculum_summary.csv"
            ),
            "timing_summary": _rel(paths.repo_root, paths.results_dir / "timing_summary.csv"),
            "artifact_retention_summary": _rel(
                paths.repo_root, paths.results_dir / "artifact_retention_summary.csv"
            ),
            "checkpoint_manifest": _rel(paths.repo_root, paths.checkpoint_manifest),
            "artifact_retention_manifest": _rel(paths.repo_root, paths.artifact_retention_manifest),
            "progress_events": _rel(paths.repo_root, paths.progress_events),
        },
        "expected_files": {
            "required": [
                "evaluation_manifest.json",
                "evaluation_budget_lock.json",
                "environment_instance_manifest.json",
                "policy_contract_manifest.json",
                "transformer_model_manifest.json",
                "optimizer_manifest.json",
                "curriculum_manifest.json",
                "checkpoint_manifest.json",
                "trace_retention_manifest.json",
                "artifact_retention_manifest.json",
                "dependency_manifest.json",
                "run_index.csv",
                "results/episode_summary.csv",
                "results/training_curve_summary.csv",
                "results/checkpoint_summary.csv",
                "results/trace_episode_index.csv",
            ],
            "not_applicable": ["all_episode_step_events_csv_by_default"],
        },
        "goal_criteria": [
            {
                "goal_id": "real_optimizer_training",
                "question": "Did the transformer model perform real optimizer steps?",
                "success_signal": "optimizer_steps > 0 in aggregate summary and episode tables",
                "failure_signal": "optimizer_steps == 0",
                "claim_if_met": "the run exercised neural optimizer training",
                "claim_if_not_met": "the run did not train the transformer",
            },
            {
                "goal_id": "selected_trace_renderability",
                "question": "Are selected episodes retained for movie rendering?",
                "success_signal": "trace_episode_index.csv contains renderable traces",
                "failure_signal": "selected_trace_count == 0",
                "claim_if_met": "selected episodes can be rendered without all-episode step CSVs",
                "claim_if_not_met": "movie renderability is blocked",
            },
            {
                "goal_id": "no_successor_lookahead",
                "question": "Was one-hop successor-Out lookahead avoided?",
                "success_signal": (
                    "resolver_summary successor_out_count_used_for_selection_count is zero"
                ),
                "failure_signal": "any successor_out_count_used_for_selection_count is nonzero",
                "claim_if_met": "the no-lookahead fairness boundary is preserved",
                "claim_if_not_met": "comparison fairness is blocked",
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
    paths: TransformerEvaluationPaths,
    run_label: str,
    summary: dict[str, object],
) -> dict[str, str]:
    paths.readout_surface.mkdir(parents=True, exist_ok=True)
    paths.docs_results_dir.mkdir(parents=True, exist_ok=True)
    docs = {
        "README.md": paths.readout_surface / "README.md",
        "method.md": paths.readout_surface / "method.md",
        "runbook.md": paths.readout_surface / "runbook.md",
        "result_readout.md": paths.readout_surface / "result_readout.md",
        "results/summary.md": paths.docs_results_dir / "summary.md",
    }
    docs["README.md"].write_text(_readme(run_label=run_label, summary=summary), encoding="utf-8")
    docs["method.md"].write_text(_method(), encoding="utf-8")
    docs["runbook.md"].write_text(_runbook(run_label), encoding="utf-8")
    docs["result_readout.md"].write_text(_result_readout(summary), encoding="utf-8")
    docs["results/summary.md"].write_text(_result_readout(summary), encoding="utf-8")
    return {key: str(value) for key, value in docs.items()}


def _readme(*, run_label: str, summary: dict[str, object]) -> str:
    protocol_invocation = (
        "execute docs/prime_directive/artifact_table_to_readable_document_protocol.md "
        "at docs/evaluations/warehouse_gridlock_001/transformer_policy/readout_source.json"
    )
    return f"""# Warehouse Gridlock Transformer Policy

## Status At A Glance

- Evaluation id: `{EVALUATION_ID}`.
- Run label: `{run_label}`.
- Model family: `{MODEL_FAMILY_ID}`.
- Optimizer steps: `{summary.get("optimizer_steps", "unknown")}`.
- Selected trace count: `{summary.get("selected_trace_count", "unknown")}`.
- Artifact budget status: `{summary.get("artifact_budget_status", "unknown")}`.

## Protocol Invocation

```text
{protocol_invocation}
```

This generated surface is intentionally lightweight. The protocol readout should
be regenerated from `readout_source.json` for the human-facing report.
"""


def _method() -> str:
    return """# Method

Warehouse Gridlock transformer policy runs train a BBB-owned transformer
actor-critic over the full Warehouse system configuration plus the current
second. The first slice is tower-only curriculum training with live-lift
state-liveness hygiene and immediate admissibility masking.
"""


def _runbook(run_label: str) -> str:
    return f"""# Runbook

Current run label:

```text
{run_label}
```

Use the transformer-policy CLI to run, summarize, and render retained episodes.
"""


def _result_readout(summary: dict[str, object]) -> str:
    lines = ["# Result Readout", ""]
    for key, value in sorted(summary.items()):
        lines.append(f"- `{key}`: `{value}`")
    lines.append("")
    return "\n".join(lines)


def _rel(root: Path, path: Path) -> str:
    try:
        return str(path.relative_to(root))
    except ValueError:
        return str(path)
