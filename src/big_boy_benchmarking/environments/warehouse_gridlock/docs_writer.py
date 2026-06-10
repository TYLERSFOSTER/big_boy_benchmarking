"""Artifact and human-doc writers for Warehouse Gridlock readiness."""

from __future__ import annotations

from pathlib import Path
from typing import Any

from big_boy_benchmarking.artifacts.schemas import ARTIFACT_SCHEMA_VERSION
from big_boy_benchmarking.artifacts.writers import write_csv, write_json
from big_boy_benchmarking.environments.warehouse_gridlock.discovery import (
    DISCOVERY_FIELDNAMES,
    DiscoveryEvent,
    cache_policy_manifest,
    summarize_discovery,
)
from big_boy_benchmarking.environments.warehouse_gridlock.instances import (
    WarehouseGridlockInstance,
)
from big_boy_benchmarking.environments.warehouse_gridlock.validation import (
    readiness_table_rows,
    validate_readiness,
)

READOUT_SURFACE = Path("docs/evaluations/warehouse_gridlock_001/environment_readiness")


def repo_readout_surface(repo_root: Path | str) -> Path:
    return Path(repo_root) / READOUT_SURFACE


def write_core_readiness_artifacts(
    *,
    instance: WarehouseGridlockInstance,
    artifact_root: Path | str,
    run_label: str,
    transition_rows: list[dict[str, object]] | None = None,
    invalid_rows: list[dict[str, object]] | None = None,
    discovery_events: list[DiscoveryEvent] | None = None,
) -> dict[str, str]:
    root = Path(artifact_root)
    root.mkdir(parents=True, exist_ok=True)
    results = root / "results"
    results.mkdir(parents=True, exist_ok=True)
    transition_rows = transition_rows or []
    invalid_rows = invalid_rows or []
    discovery_events = discovery_events or []
    readiness = validate_readiness(instance)
    table_rows = readiness_table_rows(instance)

    paths = _core_paths(root)

    write_json(
        paths["environment_instance_manifest"],
        {
            "artifact_schema_version": ARTIFACT_SCHEMA_VERSION,
            "run_label": run_label,
            **instance.manifest.to_dict(),
        },
        create_parents=True,
    )
    write_json(
        paths["graph_manifest"],
        {
            "artifact_schema_version": ARTIFACT_SCHEMA_VERSION,
            **readiness.summary,
            "blocked_nodes": [node.to_dict() for node in sorted(instance.graph.blocked_nodes)],
        },
        create_parents=True,
    )
    write_json(paths["start_state"], instance.start_state.to_dict(), create_parents=True)
    write_json(paths["goal_state"], instance.target_state.to_dict(), create_parents=True)
    write_json(
        paths["target_manifest"],
        {
            "robot_targets": {
                key: value.to_dict()
                for key, value in sorted(instance.manifest.robot_target_map().items())
            },
            "box_targets": {
                key: value.to_dict()
                for key, value in sorted(instance.manifest.box_target_map().items())
            },
        },
        create_parents=True,
    )
    write_json(
        paths["action_space_manifest"],
        {
            "action_surface": "structured_ensemble",
            "robot_count": len(instance.manifest.robot_ids),
            "per_robot_commands": ["north", "south", "east", "west", "stay"],
            "flat_enumeration": "forbidden_for_full_instance",
            "flat_action_count_expression": f"5^{len(instance.manifest.robot_ids)}",
        },
        create_parents=True,
    )
    write_json(
        paths["transition_rule_manifest"],
        instance.manifest.transition_policy.__dict__,
        create_parents=True,
    )
    write_json(
        paths["collision_policy_manifest"],
        instance.manifest.collision_policy.__dict__,
        create_parents=True,
    )
    write_json(
        paths["reward_mode_manifest"],
        instance.manifest.reward_policy.to_dict(),
        create_parents=True,
    )
    write_json(paths["action_mask_policy_manifest"], cache_policy_manifest(), create_parents=True)
    write_json(
        paths["admissibility_cache_policy_manifest"], cache_policy_manifest(), create_parents=True
    )
    write_json(paths["readiness_report"], readiness.to_dict(), create_parents=True)

    write_csv(
        paths["readiness_summary"],
        table_rows["readiness_summary"],
        ("environment_family_id", "instance_id", "status", "source_design_note", "claim_boundary"),
        create_parents=True,
    )
    write_csv(
        paths["graph_summary"],
        table_rows["graph_summary"],
        (
            "environment_family_id",
            "implementation_family_id",
            "instance_id",
            "robot_count",
            "box_count",
            "robot_target_count",
            "box_target_count",
            "column_count",
            "claim_boundary",
            "rows",
            "cols",
            "visual_node_count",
            "traversable_node_count",
            "blocked_node_count",
            "directed_edge_count",
            "blocked_edge_count",
        ),
        create_parents=True,
    )
    write_csv(
        paths["state_validation_summary"],
        table_rows["state_validation_summary"],
        ("state_role", "status", "errors"),
        create_parents=True,
    )
    write_csv(
        paths["target_validation_summary"],
        table_rows["target_validation_summary"],
        ("status", "robot_target_count", "box_target_count", "claim_boundary"),
        create_parents=True,
    )
    write_csv(
        paths["transition_smoke_summary"],
        transition_rows,
        (
            "case_id",
            "valid",
            "reward",
            "terminated",
            "truncated",
            "time_step",
            "moved_robot_count",
            "moved_box_count",
            "invalid_reasons",
        ),
        create_parents=True,
    )
    write_csv(
        paths["invalid_action_summary"],
        invalid_rows,
        ("invalid_reason", "count"),
        create_parents=True,
    )
    discovery_summary = summarize_discovery(discovery_events)
    write_csv(
        paths["discovery_events"],
        [event.to_row() for event in discovery_events],
        DISCOVERY_FIELDNAMES,
        create_parents=True,
    )
    write_csv(
        paths["discovered_state_summary"],
        [{"unique_state_count": discovery_summary["unique_state_count"]}],
        ("unique_state_count",),
        create_parents=True,
    )
    write_csv(
        paths["discovered_transition_summary"],
        [
            {
                "valid_ensemble_count": discovery_summary["valid_ensemble_count"],
                "invalid_ensemble_count": discovery_summary["invalid_ensemble_count"],
            }
        ],
        ("valid_ensemble_count", "invalid_ensemble_count"),
        create_parents=True,
    )
    write_csv(
        paths["discovery_coverage_summary"],
        [discovery_summary],
        (
            "attempted_ensemble_count",
            "valid_ensemble_count",
            "invalid_ensemble_count",
            "unique_state_count",
            "unique_action_count",
            "cache_hit_count",
            "mask_or_query_call_count",
        ),
        create_parents=True,
    )
    write_csv(
        paths["admissibility_budget_summary"],
        [
            {
                "cache_scope": "per_run_per_arm",
                "mask_policy": "none_by_default",
                "query_policy": "explicit_only",
                "attempted_ensemble_count": discovery_summary["attempted_ensemble_count"],
            }
        ],
        ("cache_scope", "mask_policy", "query_policy", "attempted_ensemble_count"),
        create_parents=True,
    )
    return {key: str(path) for key, path in paths.items()}


def existing_core_artifact_paths(artifact_root: Path | str) -> dict[str, str]:
    paths = _core_paths(Path(artifact_root))
    return {key: str(path) for key, path in paths.items() if path.exists()}


def _core_paths(root: Path) -> dict[str, Path]:
    results = root / "results"
    return {
        "environment_instance_manifest": root / "environment_instance_manifest.json",
        "graph_manifest": root / "graph_manifest.json",
        "start_state": root / "start_state.json",
        "goal_state": root / "goal_state.json",
        "target_manifest": root / "target_manifest.json",
        "action_space_manifest": root / "action_space_manifest.json",
        "transition_rule_manifest": root / "transition_rule_manifest.json",
        "collision_policy_manifest": root / "collision_policy_manifest.json",
        "reward_mode_manifest": root / "reward_mode_manifest.json",
        "action_mask_policy_manifest": root / "action_mask_policy_manifest.json",
        "admissibility_cache_policy_manifest": root / "admissibility_cache_policy_manifest.json",
        "readiness_summary": results / "readiness_summary.csv",
        "graph_summary": results / "graph_summary.csv",
        "state_validation_summary": results / "state_validation_summary.csv",
        "target_validation_summary": results / "target_validation_summary.csv",
        "transition_smoke_summary": results / "transition_smoke_summary.csv",
        "invalid_action_summary": results / "invalid_action_summary.csv",
        "discovered_state_summary": results / "discovered_state_summary.csv",
        "discovered_transition_summary": results / "discovered_transition_summary.csv",
        "discovery_coverage_summary": results / "discovery_coverage_summary.csv",
        "admissibility_budget_summary": results / "admissibility_budget_summary.csv",
        "discovery_events": results / "discovery_events.csv",
        "readiness_report": root / "readiness_report.json",
    }


def write_readout_source(
    *,
    repo_root: Path | str,
    artifact_root: Path | str,
    artifact_paths: dict[str, str],
    instance: WarehouseGridlockInstance,
) -> Path:
    surface = repo_readout_surface(repo_root)
    surface.mkdir(parents=True, exist_ok=True)
    target = surface / "readout_source.json"
    payload: dict[str, Any] = {
        "source_type": "environment_readiness",
        "environment_family_id": instance.manifest.environment_family_id,
        "environment_instance_id": instance.manifest.instance_id,
        "run_family_id": "warehouse_gridlock_environment_readiness_v001",
        "artifact_root": str(Path(artifact_root)),
        "source_design_note": instance.manifest.source.source_design_note,
        "source_images": list(instance.manifest.source.source_images),
        "artifact_tables": artifact_paths,
        "allowed_claims": [
            "environment manifest validates",
            "start and target states validate",
            "transition smoke cases exercise valid and invalid dynamics",
            "discovery/admissibility artifact surfaces exist",
        ],
        "blocked_claims": [
            "tower advantage",
            "learned policy performance",
            "standard gauntlet completion",
            "benchmark superiority",
        ],
    }
    write_json(target, payload, create_parents=True)
    return target


def write_human_docs(
    *,
    repo_root: Path | str,
    artifact_root: Path | str,
    readout_source: Path | str,
    artifact_paths: dict[str, str],
    instance: WarehouseGridlockInstance,
) -> dict[str, str]:
    surface = repo_readout_surface(repo_root)
    results = surface / "results"
    badges = surface / "badges"
    results.mkdir(parents=True, exist_ok=True)
    badges.mkdir(parents=True, exist_ok=True)
    (badges / "readiness.svg").write_text(
        _badge_svg(label="readiness", message="environment-ok", color="#2e7d32"),
        encoding="utf-8",
    )
    readiness = validate_readiness(instance)
    summary = readiness.summary
    files = {
        "README.md": surface / "README.md",
        "artifact_index.md": surface / "artifact_index.md",
        "method.md": surface / "method.md",
        "runbook.md": surface / "runbook.md",
        "glossary.md": surface / "glossary.md",
        "results/summary.md": results / "summary.md",
    }
    artifact_display = _display_path(repo_root=Path(repo_root), path=Path(artifact_root))
    readout_display = _display_path(repo_root=Path(repo_root), path=Path(readout_source))
    files["README.md"].write_text(
        _readme(
            summary=summary,
            artifact_root=artifact_display,
            readout_source=readout_display,
            instance=instance,
        ),
        encoding="utf-8",
    )
    files["artifact_index.md"].write_text(_artifact_index(artifact_paths), encoding="utf-8")
    files["method.md"].write_text(_method(instance), encoding="utf-8")
    files["runbook.md"].write_text(_runbook(), encoding="utf-8")
    files["glossary.md"].write_text(_glossary(), encoding="utf-8")
    files["results/summary.md"].write_text(_results_summary(summary), encoding="utf-8")
    return {key: str(path) for key, path in files.items()}


def _readme(
    *,
    summary: dict[str, object],
    artifact_root: str,
    readout_source: str,
    instance: WarehouseGridlockInstance,
) -> str:
    return (
        "# Warehouse Gridlock 001 Environment Readiness\n\n"
        "This is the first BBB readiness surface for the PO-authored Warehouse "
        "Gridlock 001 physical-system drawing. It checks whether the environment "
        "contract can be loaded, validated, stepped, and artifacted. It is not a "
        "tower evaluation, standard gauntlet, learned-policy result, or benchmark "
        "claim.\n\n"
        "## Badges\n\n"
        "![readiness](badges/readiness.svg)\n\n"
        "## Identity\n\n"
        f"- Environment family id: `{summary['environment_family_id']}`.\n"
        f"- Instance id: `{summary['instance_id']}`.\n"
        f"- Robots: `{summary['robot_count']}`.\n"
        f"- Boxes: `{summary['box_count']}`.\n"
        f"- Visual grid nodes: `{summary['visual_node_count']}`.\n"
        f"- Traversable nodes: `{summary['traversable_node_count']}`.\n"
        f"- Directed traversable edges: `{summary['directed_edge_count']}`.\n\n"
        "## Source Authority\n\n"
        "The physical design comes from Project Owner-authored SVG drawings. "
        "Codex translated those drawings into a manifest and readiness surface.\n\n"
        f"- Source design note: `{instance.manifest.source.source_design_note}`.\n"
        + "".join(
            f"- Source image: `{image}`.\n" for image in instance.manifest.source.source_images
        )
        + "\n## Mechanics Checked\n\n"
        "- One timestep is one second.\n"
        "- Every robot receives one command per timestep.\n"
        "- Valid ensemble moves advance time by one second.\n"
        "- Invalid ensemble attempts are whole-ensemble self-loops and do not advance time.\n"
        "- Push-only box dynamics are implemented.\n"
        "- Shared final occupancy and head-on swaps are invalid.\n"
        "- Concrete columns are blocked physical nodes.\n"
        "- Terminal success requires exact robot and box target placement.\n\n"
        "## Artifact Surface\n\n"
        f"- Artifact root: `{artifact_root}`.\n"
        f"- Readout source: `{readout_source}`.\n\n"
        "## Claim Boundary\n\n"
        f"{summary['claim_boundary']}.\n\n"
        "## Evaluator / Codex Clarifying Turns\n\n"
        "### Evaluator Turn\n\n"
        "_Add questions or corrections here._\n\n"
        "### Codex Turn\n\n"
        "_Awaiting evaluator turn._\n"
    )


def _display_path(*, repo_root: Path, path: Path) -> str:
    try:
        return str(path.resolve().relative_to(repo_root.resolve()))
    except ValueError:
        return str(path)


def _artifact_index(artifact_paths: dict[str, str]) -> str:
    rows = ["# Warehouse Gridlock Readiness Artifact Index", ""]
    for label, path in sorted(artifact_paths.items()):
        rows.append(f"- `{label}`: `{path}`")
    rows.append("")
    return "\n".join(rows)


def _method(instance: WarehouseGridlockInstance) -> str:
    return (
        "# Method\n\n"
        "Warehouse Gridlock readiness loads the full PO drawing manifest, "
        "generates the 16x16 cardinal grid, removes the five concrete-column "
        "nodes and incident edges, validates start and target states, and runs "
        "representative transition-smoke cases. The action surface is structured "
        "ensemble control; full flat action enumeration is forbidden.\n\n"
        f"Collision policy: `{instance.manifest.collision_policy.collision_policy_id}`.\n"
        f"Transition policy: `{instance.manifest.transition_policy.transition_policy_id}`.\n"
        f"Discovery policy: `{instance.manifest.discovery_policy.discovery_policy_id}`.\n"
    )


def _runbook() -> str:
    artifact_root = (
        "docs/evaluations/warehouse_gridlock_001/environment_readiness/artifacts/smoke_001"
    )
    return (
        "# Runbook\n\n"
        "```text\n"
        "uv run python -m big_boy_benchmarking.cli warehouse-gridlock graph-diagnostics \\\n"
        f"  --artifact-root {artifact_root} \\\n"
        "  --instance-id warehouse_gridlock_16x16_v001 \\\n"
        "  --run-label smoke_001\n\n"
        "uv run python -m big_boy_benchmarking.cli warehouse-gridlock state-diagnostics \\\n"
        f"  --artifact-root {artifact_root} \\\n"
        "  --instance-id warehouse_gridlock_16x16_v001 \\\n"
        "  --run-label smoke_001\n\n"
        "uv run python -m big_boy_benchmarking.cli warehouse-gridlock transition-smoke \\\n"
        f"  --artifact-root {artifact_root} \\\n"
        "  --instance-id warehouse_gridlock_16x16_v001 \\\n"
        "  --run-label smoke_001\n\n"
        "uv run python -m big_boy_benchmarking.cli warehouse-gridlock readiness-docs \\\n"
        f"  --artifact-root {artifact_root} \\\n"
        "  --instance-id warehouse_gridlock_16x16_v001 \\\n"
        "  --run-label smoke_001\n"
        "```\n"
    )


def _glossary() -> str:
    return (
        "# Glossary\n\n"
        "- Ensemble action: one synchronous command per robot.\n"
        "- Hidden admissibility: policies do not receive the full valid-action graph for free.\n"
        "- Concrete column: gray PO-drawn obstacle node that blocks occupancy and traversal.\n"
        "- Whole-ensemble invalidation: one bad submove invalidates the whole ensemble.\n"
    )


def _results_summary(summary: dict[str, object]) -> str:
    return (
        "# Results Summary\n\n"
        f"- Status: environment readiness `{summary.get('instance_id')}` loaded and validated.\n"
        f"- Traversable nodes: `{summary.get('traversable_node_count')}`.\n"
        f"- Directed traversable edges: `{summary.get('directed_edge_count')}`.\n"
        f"- Blocked column nodes: `{summary.get('blocked_node_count')}`.\n"
        "- This summary does not evaluate learning performance.\n"
    )


def _badge_svg(*, label: str, message: str, color: str) -> str:
    label_width = 70
    message_width = 120
    width = label_width + message_width
    return (
        '<svg xmlns="http://www.w3.org/2000/svg" '
        f'width="{width}" height="20" role="img" aria-label="{label}: {message}">'
        f"<title>{label}: {message}</title>"
        f'<rect width="{label_width}" height="20" fill="#555"/>'
        f'<rect x="{label_width}" width="{message_width}" height="20" fill="{color}"/>'
        '<g fill="#fff" text-anchor="middle" '
        'font-family="Verdana,Geneva,DejaVu Sans,sans-serif" font-size="11">'
        f'<text x="{label_width / 2}" y="14">{label}</text>'
        f'<text x="{label_width + message_width / 2}" y="14">{message}</text>'
        "</g></svg>\n"
    )
