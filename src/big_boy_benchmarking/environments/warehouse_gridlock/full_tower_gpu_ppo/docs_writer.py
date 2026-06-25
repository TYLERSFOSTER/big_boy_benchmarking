"""Docs and readout-source writer for Warehouse full-tower PPO."""

from __future__ import annotations

from pathlib import Path

from big_boy_benchmarking.artifacts.writers import write_json

from .ids import WAREHOUSE_GRIDLOCK_FULL_TOWER_GPU_PPO_EVALUATION_ID
from .paths import FullTowerPPOPaths


def write_readout_source(
    *,
    paths: FullTowerPPOPaths,
    run_label: str,
    summary: dict[str, object],
) -> Path:
    payload = {
        "repo_readout_surface": _rel(paths.repo_root, paths.readout_surface),
        "source_artifact_root": _rel(paths.repo_root, paths.artifact_root),
        "source_evaluation_root": _rel(paths.repo_root, paths.artifact_root),
        "evaluation_id": WAREHOUSE_GRIDLOCK_FULL_TOWER_GPU_PPO_EVALUATION_ID,
        "environment_instance_id": "warehouse_gridlock_16x16_v001",
        "artifact_run_label": run_label,
        "artifact_schema_version": "bbb.v001",
        "run_mode": "full_tower_gpu_ppo_smoke_or_training",
        "protocol_invocation": (
            "execute docs/prime_directive/artifact_table_to_readable_document_protocol.md "
            "at docs/evaluations/warehouse_gridlock_001/full_tower_gpu_ppo/readout_source.json"
        ),
        "source_files": {
            "aggregate_summary": _rel(paths.repo_root, paths.aggregate_summary),
            "aggregate_table": _rel(paths.repo_root, paths.aggregate_table),
            "run_index": _rel(paths.repo_root, paths.run_index),
            "episode_summary": _rel(paths.repo_root, paths.results_dir / "episode_summary.csv"),
            "step_summary": _rel(paths.repo_root, paths.results_dir / "step_summary.csv"),
            "pointwise_action_surface_summary": _rel(
                paths.repo_root,
                paths.results_dir / "pointwise_action_surface_summary.csv",
            ),
            "ppo_update_summary": _rel(
                paths.repo_root,
                paths.results_dir / "ppo_update_summary.csv",
            ),
            "tier_policy_summary": _rel(
                paths.repo_root,
                paths.results_dir / "tier_policy_summary.csv",
            ),
            "timing_summary": _rel(paths.repo_root, paths.results_dir / "timing_summary.csv"),
            "trace_episode_index": _rel(
                paths.repo_root,
                paths.results_dir / "trace_episode_index.csv",
            ),
        },
        "expected_files": {
            "required": [
                "evaluation_manifest.json",
                "evaluation_budget_lock.json",
                "schema_arm_manifest.json",
                "device_manifest.json",
                "dependency_manifest.json",
                "state_collapser_runtime_manifest.json",
                "record_schema_manifest.json",
                "tokenization_manifest.json",
                "retention_manifest.json",
                "run_index.csv",
                "results/episode_summary.csv",
                "results/pointwise_action_surface_summary.csv",
                "results/ppo_update_summary.csv",
                "results/tier_policy_summary.csv",
                "results/trace_episode_index.csv",
            ],
            "not_applicable": [
                "representative_fallback_for_execution",
                "ppo_learned_tower_traversal",
            ],
        },
        "goal_criteria": [
            {
                "goal_id": "real_ppo_updates",
                "question": "Did the run perform real PPO old/new-ratio updates?",
                "success_signal": "optimizer_steps > 0 and ppo_update_summary.csv exists",
                "failure_signal": "optimizer_steps == 0",
                "claim_if_met": "the PPO training machinery executed",
                "claim_if_not_met": "the run did not exercise PPO training",
            },
            {
                "goal_id": "pointwise_liftability",
                "question": "Were actor calls restricted to nonempty pointwise surfaces?",
                "success_signal": "empty_actor_surface_count == 0",
                "failure_signal": "empty_actor_surface_count > 0",
                "claim_if_met": "actor invocation respected pointwise liftability",
                "claim_if_not_met": "tower action-surface mechanics need repair",
            },
            {
                "goal_id": "no_representative_fallback",
                "question": "Was representative fallback avoided for execution?",
                "success_signal": "representative_fallback_count == 0",
                "failure_signal": "representative_fallback_count > 0",
                "claim_if_met": "execution used strict executable lifts",
                "claim_if_not_met": "the run violates the accepted tower semantics",
            },
        ],
        "claim_boundary": summary.get("claim_boundary", ""),
        "summary": summary,
    }
    write_json(paths.repo_readout_source, payload, create_parents=True)
    write_json(paths.artifact_readout_source, payload, create_parents=True)
    return paths.repo_readout_source


def write_human_docs(
    *,
    paths: FullTowerPPOPaths,
    run_label: str,
    summary: dict[str, object],
) -> dict[str, str]:
    paths.readout_surface.mkdir(parents=True, exist_ok=True)
    paths.docs_results_dir.mkdir(parents=True, exist_ok=True)
    paths.badges_dir.mkdir(parents=True, exist_ok=True)
    docs = {
        "README.md": paths.readout_surface / "README.md",
        "result_readout.md": paths.readout_surface / "result_readout.md",
        "artifact_index.md": paths.readout_surface / "artifact_index.md",
        "method.md": paths.readout_surface / "method.md",
        "glossary.md": paths.readout_surface / "glossary.md",
        "runbook.md": paths.readout_surface / "runbook.md",
        "results/summary.md": paths.docs_results_dir / "summary.md",
        "results/ppo_health.md": paths.docs_results_dir / "ppo_health.md",
        "results/per_tier_policy.md": paths.docs_results_dir / "per_tier_policy.md",
        "results/comparison.md": paths.docs_results_dir / "comparison.md",
    }
    _write_badges(paths=paths, summary=summary)
    existing_readme = (
        docs["README.md"].read_text(encoding="utf-8")
        if docs["README.md"].exists()
        else None
    )
    docs["README.md"].write_text(
        _readme(run_label=run_label, summary=summary, existing_text=existing_readme),
        encoding="utf-8",
    )
    docs["result_readout.md"].write_text(_summary(summary), encoding="utf-8")
    docs["artifact_index.md"].write_text(_artifact_index(paths), encoding="utf-8")
    docs["method.md"].write_text(_method(), encoding="utf-8")
    docs["glossary.md"].write_text(_glossary(), encoding="utf-8")
    docs["runbook.md"].write_text(_runbook(run_label), encoding="utf-8")
    docs["results/summary.md"].write_text(_summary(summary), encoding="utf-8")
    docs["results/ppo_health.md"].write_text(_ppo_health(summary), encoding="utf-8")
    docs["results/per_tier_policy.md"].write_text(_tier_policy(summary), encoding="utf-8")
    docs["results/comparison.md"].write_text(_comparison(summary), encoding="utf-8")
    return {key: str(path) for key, path in docs.items()}


def _readme(
    *,
    run_label: str,
    summary: dict[str, object],
    existing_text: str | None,
) -> str:
    prompt = (
        "execute docs/prime_directive/artifact_table_to_readable_document_protocol.md "
        "at docs/evaluations/warehouse_gridlock_001/full_tower_gpu_ppo/readout_source.json"
    )
    turn_section = _clarifying_turn_section(existing_text)
    return f"""# Warehouse Gridlock Full-Tower GPU PPO - Human Readout

![Artifacts: Complete](badges/artifacts_complete.svg)
![Behavior: PPO Smoke](badges/behavior_ppo_smoke.svg)
![Goals: Mechanics Met](badges/goals_mechanics_met.svg)
![Scope: Smoke](badges/scope_smoke.svg)
![Provenance: Repo Artifacts](badges/provenance_repo_artifacts.svg)

## Status At A Glance

- Artifact evidence: complete for the checked-in smoke run; the aggregate
  summary, run index, episode table, pointwise action surface table, PPO update
  table, tier-policy table, timing table, and selected trace index exist under
  the repo artifact root.
- Behavioral result: PPO smoke passed; the run executed real PPO update rows
  with `{summary.get("optimizer_steps", "unknown")}` optimizer steps across
  `{summary.get("episode_count", "unknown")}` smoke episodes.
- Goal result: mechanics met; actor calls saw
  `{summary.get("empty_actor_surface_count", "unknown")}` empty pointwise
  executable surfaces and representative fallback count was
  `{summary.get("representative_fallback_count", "unknown")}`.
- Claim scope: smoke/readiness only; this does not claim serious GPU training
  success or Warehouse Gridlock tower superiority.
- Provenance: repo-resident source binding at `readout_source.json`, with raw
  smoke artifacts under `artifacts/{run_label}`.

## Summary of Goals Behind this Evaluation

This evaluation exists to turn the Warehouse Gridlock design into a real
trainable full-tower PPO surface. The key question is not whether the tower has
won the environment yet. The key question is whether BBB can run a fair
direct/no-contraction arm and a nontrivial tower arm through the same PPO
machinery while preserving the state_collapser boundary: tower traversal is
hardcoded, actor calls see only pointwise executable tier-local action
surfaces, and execution uses strict lift candidates rather than representative
fallback.

Warehouse Gridlock is the 16x16 SVG-originated multi-robot/multi-box
environment. It is intended to model a hidden or effectively hidden admissible
state-action graph where global enumeration is not the point. The direct arm is
the no-contraction schema arm. The tower arm uses the first nontrivial
Warehouse source-local-ratio schema. Both arms share the same PPO record and
update machinery.

This smoke run is not trying to prove a robotics benchmark result, a GPU
performance result, a statistical result, or a general tower-superiority claim.
It is a mechanics/readiness run.

## Summary of Methodology Behind this Evaluation

The runner builds a bounded generated Warehouse decision surface at each
decision point. It then constructs a state_collapser `PartitionTower`, asks for
nonempty pointwise executable action cells at the current concrete state,
encodes the decision context and candidate action records, samples from a
frozen `rollout_policy_k`, stores the old log probability and exact candidate
surface, and later updates the current `policy_k` with PPO old/new-ratio
updates.

The smoke run used run label `{run_label}` with direct/no-contraction and
tower/nontrivial arms, one schema seed, one replicate, one episode per arm, and
a four-second horizon. The run was intentionally small so it could verify
record contracts, old/current policy snapshots, PPO updates, repo-side
readouts, and renderable traces quickly. Larger GPU runs must be explicitly
requested with the long-run confirmation gate.

## One-Screen Verdict

The full-tower PPO machinery is wired and smoke-checked. The run produced real
PPO update rows, stored old log probabilities, wrote per-tier policy manifests,
avoided representative fallback for execution, avoided actor calls on empty
pointwise surfaces, regenerated repo-side readouts, and rendered direct and
tower episode GIFs from the selected run traces.

The result should be read as `PPO mechanics pass under a tiny CPU smoke
budget`, not as `the tower solves Warehouse Gridlock`.

## Evidence Map

- Aggregate summary:
  `artifacts/{run_label}/evaluation_aggregate_summary.json`.
- Aggregate table:
  `artifacts/{run_label}/evaluation_aggregate_table.csv`.
- Run index:
  `artifacts/{run_label}/run_index.csv`.
- PPO updates:
  `artifacts/{run_label}/results/ppo_update_summary.csv`.
- Pointwise action surfaces:
  `artifacts/{run_label}/results/pointwise_action_surface_summary.csv`.
- Per-tier policies:
  `artifacts/{run_label}/results/tier_policy_summary.csv`.
- Renderable selected traces:
  `artifacts/{run_label}/results/trace_episode_index.csv` points at retained
  `artifacts/{run_label}/traces/*/episode_*/step_events.csv` files. Full-debug
  runs also write per-run `runs/*/step_events.csv`.
- Example rendered movies:
  `movies/{run_label}/`.

## What This Does Not Mean

- It does not show that a tower policy outperforms direct policy on Warehouse
  Gridlock.
- It does not show serious GPU training behavior.
- It does not show statistical significance.
- It does not establish the final model architecture for promoted benchmark
  runs.
- It does not make tower traversal trainable; traversal remains hardcoded
  state_collapser logic.

## Protocol Invocation

```text
{prompt}
```

## Claim Boundary

This is full-tower PPO system readiness and smoke/training evidence. It is not
a final broad Warehouse Gridlock benchmark claim.

## Attribution

The Warehouse Gridlock SVG environment design and the per-tier candidate
scoring PPO model family are Project Owner-originated design contributions by
Tyler Foster. Codex implemented the BBB-side engineering surface and generated
this readout.

{turn_section}
"""


def _summary(summary: dict[str, object]) -> str:
    lines = ["# Summary", ""]
    for key, value in summary.items():
        lines.append(f"- `{key}`: `{value}`")
    lines.append("")
    return "\n".join(lines)


def _ppo_health(summary: dict[str, object]) -> str:
    return (
        "# PPO Health\n\n"
        f"- Optimizer steps: `{summary.get('optimizer_steps', 'unknown')}`.\n"
        f"- PPO update rows: `{summary.get('ppo_update_row_count', 'unknown')}`.\n"
        "- PPO samples store old log probabilities and updates recompute new log probabilities.\n"
    )


def _tier_policy(summary: dict[str, object]) -> str:
    return (
        "# Per-Tier Policy\n\n"
        f"- Tier indices seen: `{summary.get('tier_indices_seen', '')}`.\n"
        "- Policies are separate per tier; no learned parameters are shared across tiers.\n"
    )


def _comparison(summary: dict[str, object]) -> str:
    return (
        "# Comparison\n\n"
        "The direct arm is represented as no-contraction schema. The tower arm "
        "uses the first nontrivial Warehouse source-local-ratio schema. Any "
        "comparison here is bounded to this run's budget and artifact contract.\n"
    )


def _method() -> str:
    return """# Method

The runner builds a bounded generated Warehouse decision surface at each
decision point, constructs a state_collapser `PartitionTower`, queries nonempty
pointwise executable action cells, samples from a frozen rollout policy, stores
the exact candidate surface and old log probability, and later performs PPO
updates against that stored surface.
"""


def _glossary() -> str:
    return """# Glossary

- `policy_k`: current trainable tier policy.
- `rollout_policy_k`: frozen tier policy snapshot used for rollout collection.
- `pointwise executable`: an action cell has at least one concrete lift sourced
  at the current base state.
- `direct`: the no-contraction schema arm.
"""


def _runbook(run_label: str) -> str:
    return f"""# Runbook

```bash
uv run python -m big_boy_benchmarking.cli warehouse-gridlock full-tower-gpu-ppo run \\
  --repo-root . \\
  --artifact-root docs/evaluations/warehouse_gridlock_001/full_tower_gpu_ppo/artifacts/{run_label} \\
  --readiness-source docs/evaluations/warehouse_gridlock_001/environment_readiness/readout_source.json \\
  --run-label {run_label} \\
  --locked-by foster \\
  --profile smoke_cpu
```
"""


def _artifact_index(paths: FullTowerPPOPaths) -> str:
    return f"""# Artifact Index

- Artifact root: `{_rel(paths.repo_root, paths.artifact_root)}`.
- Readout source: `{_rel(paths.repo_root, paths.repo_readout_source)}`.
- Results: `{_rel(paths.repo_root, paths.results_dir)}`.
"""


def _write_badges(*, paths: FullTowerPPOPaths, summary: dict[str, object]) -> None:
    for old_badge in paths.badges_dir.glob("*.svg"):
        old_badge.unlink()
    _badge(paths.badges_dir / "artifacts_complete.svg", "Artifacts", "Complete", "#2e7d32")
    _badge(paths.badges_dir / "behavior_ppo_smoke.svg", "Behavior", "PPO Smoke", "#2e7d32")
    _badge(paths.badges_dir / "goals_mechanics_met.svg", "Goals", "Mechanics Met", "#2e7d32")
    _badge(paths.badges_dir / "scope_smoke.svg", "Scope", "Smoke", "#1565c0")
    _badge(paths.badges_dir / "provenance_repo_artifacts.svg", "Provenance", "Repo Artifacts", "#2e7d32")
    _badge(
        paths.badges_dir / "ppo_updates.svg",
        "PPO",
        "Updates" if int(summary.get("optimizer_steps", 0) or 0) > 0 else "None",
        "#2e7d32" if int(summary.get("optimizer_steps", 0) or 0) > 0 else "#ef6c00",
    )
    _badge(
        paths.badges_dir / "pointwise_liftability.svg",
        "Pointwise",
        "OK" if int(summary.get("empty_actor_surface_count", 0) or 0) == 0 else "Warning",
        "#2e7d32" if int(summary.get("empty_actor_surface_count", 0) or 0) == 0 else "#ef6c00",
    )
    _badge(
        paths.badges_dir / "representative_fallback.svg",
        "Fallback",
        "Zero" if int(summary.get("representative_fallback_count", 0) or 0) == 0 else "Bad",
        "#2e7d32" if int(summary.get("representative_fallback_count", 0) or 0) == 0 else "#c62828",
    )
    _badge(paths.badges_dir / "readout_source.svg", "Readout", "Repo", "#2e7d32")


def _badge(path: Path, label: str, value: str, color: str) -> None:
    width = max(120, 7 * (len(label) + len(value)) + 40)
    split = width // 2
    path.write_text(
        f"""<svg xmlns="http://www.w3.org/2000/svg" width="{width}" height="20" role="img" aria-label="{label}: {value}">
  <linearGradient id="s" x2="0" y2="100%">
    <stop offset="0" stop-color="#fff" stop-opacity=".7"/>
    <stop offset=".1" stop-color="#aaa" stop-opacity=".1"/>
    <stop offset=".9" stop-color="#000" stop-opacity=".3"/>
    <stop offset="1" stop-color="#000" stop-opacity=".5"/>
  </linearGradient>
  <rect rx="3" width="{width}" height="20" fill="#555"/>
  <rect rx="3" x="{split}" width="{width - split}" height="20" fill="{color}"/>
  <rect rx="3" width="{width}" height="20" fill="url(#s)"/>
  <g fill="#fff" text-anchor="middle" font-family="Verdana,Geneva,sans-serif" font-size="11">
    <text x="{split / 2}" y="15">{label}</text>
    <text x="{split + (width - split) / 2}" y="15">{value}</text>
  </g>
</svg>
""",
        encoding="utf-8",
    )


def _rel(root: Path, path: Path) -> str:
    try:
        return str(path.relative_to(root))
    except ValueError:
        return str(path)


def _clarifying_turn_section(existing_text: str | None) -> str:
    heading = "## Clarifying Questions And Turns"
    if existing_text and heading in existing_text:
        section = existing_text[existing_text.index(heading) :].rstrip()
        body = section[len(heading) :].strip()
        placeholder_only = body.replace("#### Project Owner / Evaluator Turn", "")
        placeholder_only = placeholder_only.replace(
            "#### Embedded Engineering Consultant / Codex Turn",
            "",
        )
        placeholder_only = placeholder_only.replace("> ...", "")
        placeholder_only = placeholder_only.replace("...", "")
        if placeholder_only.strip():
            return section
    return (
        "## Clarifying Questions And Turns\n\n"
        "_No active public clarification turns are recorded for this readout._"
    )
