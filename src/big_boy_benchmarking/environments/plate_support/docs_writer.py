"""Human-facing PlateSupport environment docs writer."""

from __future__ import annotations

from pathlib import Path
from typing import Any

from big_boy_benchmarking.environments.plate_support.ids import (
    ACTION_LABEL_CONTRACT_ID,
    DEFAULT_INSTANCE_ID,
    DEFAULT_SCHEMA_ID,
    ENVIRONMENT_FAMILY_ID,
    LEGALITY_CONTRACT_ID,
    NO_CONTRACTION_SCHEMA_ID,
    READINESS_RUN_FAMILY_ID,
    REWARD_BUNDLE_ID,
    UPSTREAM_MODULE,
    UPSTREAM_SMOKE_ID,
)
from big_boy_benchmarking.environments.plate_support.paths import (
    default_environment_doc_path,
)


def write_plate_support_environment_docs(
    *,
    docs_path: Path | str | None,
    artifact_root: Path | str,
    summary: dict[str, Any],
    artifact_index_path: Path | str,
    readout_source_path: Path | str,
    command_line: str,
) -> Path:
    target = Path(docs_path) if docs_path is not None else default_environment_doc_path()
    target.parent.mkdir(parents=True, exist_ok=True)
    target.write_text(
        _environment_doc(
            artifact_root=Path(artifact_root),
            summary=summary,
            artifact_index_path=Path(artifact_index_path),
            readout_source_path=Path(readout_source_path),
            command_line=command_line,
        ),
        encoding="utf-8",
    )
    return target


def write_artifact_index(
    *,
    artifact_index_path: Path | str,
    artifact_paths: dict[str, str],
) -> Path:
    target = Path(artifact_index_path)
    target.parent.mkdir(parents=True, exist_ok=True)
    rows = ["# PlateSupport Environment Readiness Artifact Index", ""]
    for label, path in sorted(artifact_paths.items()):
        rows.append(f"- `{label}`: `{path}`")
    rows.append("")
    target.write_text("\n".join(rows), encoding="utf-8")
    return target


def _environment_doc(
    *,
    artifact_root: Path,
    summary: dict[str, Any],
    artifact_index_path: Path,
    readout_source_path: Path,
    command_line: str,
) -> str:
    graph = summary.get("graph_summary", {})
    random_policy = summary.get("random_policy_recon", {})
    tower = summary.get("tower_probe", [])
    training = summary.get("training_surface_availability", {})
    return (
        "# PlateSupport 5x5 Default Environment\n\n"
        "This page is the BBB environment-readiness document for the upstream "
        "`state_collapser` PlateSupport example. It is not an evaluation readout "
        "and does not claim tower learning benefit.\n\n"
        "## Identity\n\n"
        f"- Environment family id: `{ENVIRONMENT_FAMILY_ID}`.\n"
        f"- Environment instance id: `{DEFAULT_INSTANCE_ID}`.\n"
        f"- Upstream smoke id: `{UPSTREAM_SMOKE_ID}`.\n"
        f"- Upstream module: `{UPSTREAM_MODULE}`.\n"
        f"- Readiness run family id: `{READINESS_RUN_FAMILY_ID}`.\n\n"
        "## Contracts\n\n"
        f"- Legality contract id: `{LEGALITY_CONTRACT_ID}`.\n"
        f"- Reward bundle id: `{REWARD_BUNDLE_ID}`.\n"
        f"- Action label contract id: `{ACTION_LABEL_CONTRACT_ID}`.\n"
        f"- Default schema id: `{DEFAULT_SCHEMA_ID}`.\n"
        f"- No-contraction schema id: `{NO_CONTRACTION_SCHEMA_ID}`.\n\n"
        "PlateSupport states are finite plate/support configurations "
        "`(x_idx, y_idx, theta_idx, e1, e2, e3)`. A primitive action proposes a "
        "candidate state; if the candidate violates the upstream validity "
        "predicates, the transition is an invalid self-loop. If the candidate "
        "is valid but clips back to the same concrete state, BBB records that "
        "separately as a valid self-transition.\n\n"
        "## Structural Readiness\n\n"
        f"- Candidate states: `{graph.get('candidate_state_count')}`.\n"
        f"- Valid states: `{graph.get('valid_state_count')}`.\n"
        f"- Reachable valid states from start: `{graph.get('reachable_state_count')}`.\n"
        f"- Primitive actions: `{graph.get('action_count')}`.\n"
        f"- Valid non-self edges: `{graph.get('valid_nonself_edge_count')}`.\n"
        f"- Invalid primitive moves: `{graph.get('invalid_move_count')}`.\n"
        f"- Valid clipped self-transitions: `{graph.get('valid_self_transition_count')}`.\n"
        f"- Shortest start-goal path length: `{graph.get('shortest_path_length')}`.\n"
        f"- Goal one step from start: `{graph.get('goal_one_step_from_start')}`.\n\n"
        "## Random Policy Reconnaissance\n\n"
        "This is structural reconnaissance, not benchmark evidence.\n\n"
        f"- Episodes: `{random_policy.get('episode_count')}`.\n"
        f"- Success count: `{random_policy.get('success_count')}`.\n"
        f"- Success rate: `{random_policy.get('success_rate')}`.\n"
        f"- Mean reward: `{random_policy.get('mean_total_reward')}`.\n"
        f"- Invalid move rate: `{random_policy.get('invalid_move_rate')}`.\n\n"
        "## Tower Readiness Probe\n\n"
        f"{_tower_lines(tower)}\n\n"
        "## Training Surface Availability\n\n"
        f"{_training_surface_lines(training)}\n\n"
        "## Claim Boundary\n\n"
        "This environment page may support environment-readiness claims only: "
        "import health, structural graph sanity, artifact completeness, "
        "tower-shape availability, and training-surface availability. It may "
        "not claim tower control improvement, flat-versus-tower performance, "
        "or serious benchmark success.\n\n"
        "## Artifacts\n\n"
        f"- Artifact root: `{artifact_root}`.\n"
        f"- Artifact index: `{artifact_index_path}`.\n"
        f"- Readout source: `{readout_source_path}`.\n\n"
        "Run readiness again with:\n\n"
        "```text\n"
        f"{command_line}\n"
        "```\n"
    )


def _tower_lines(rows: list[dict[str, Any]]) -> str:
    if not rows:
        return "- No tower probe rows were recorded."
    return "\n".join(
        "- "
        f"`{row.get('schema_id')}` mode `{row.get('upstream_schema_mode')}`: "
        f"max depth `{row.get('max_depth')}`, scheduled assignments "
        f"`{row.get('scheduled_assignment_count')}`."
        for row in rows
    )


def _training_surface_lines(payload: dict[str, Any]) -> str:
    if not payload:
        return "- No training surface availability payload was recorded."
    return "\n".join(
        f"- `{name}`: `{available}`." for name, available in sorted(payload.items())
    )
