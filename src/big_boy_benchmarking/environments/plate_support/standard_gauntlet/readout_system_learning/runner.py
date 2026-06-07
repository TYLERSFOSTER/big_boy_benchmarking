"""Readout builder for the PlateSupport standard gauntlet."""

from __future__ import annotations

import csv
from dataclasses import dataclass
from pathlib import Path

from big_boy_benchmarking.artifacts.writers import write_csv, write_json

from ..ids import READOUT_SYSTEM_LEARNING_STAGE_ID, STAGE_DEFINITIONS
from .badges import BADGE_FIELDS, build_badges, write_badge_svgs
from .config import ReadoutSystemLearningConfig
from .stage_sources import (
    ReadoutSourceError,
    StageSourceRecord,
    SuiteReadoutSource,
    load_suite_readout_source,
    read_stage_table,
)


@dataclass(frozen=True)
class ReadoutSystemLearningResult:
    """Result of building the suite readout."""

    status: str
    readout_source_path: Path
    readout_surface: Path
    generated_paths: dict[str, str]
    suite_status: str
    claim_status: str
    failure_reason: str | None = None


def build_readout_system_learning(
    config: ReadoutSystemLearningConfig,
) -> ReadoutSystemLearningResult:
    """Generate suite-level human readout documents from an explicit source."""

    try:
        source = load_suite_readout_source(config.readout_source_path)
    except ReadoutSourceError as exc:
        return ReadoutSystemLearningResult(
            status="blocked",
            readout_source_path=config.readout_source_path,
            readout_surface=config.readout_source_path.parent,
            generated_paths={},
            suite_status="protocol_blocked",
            claim_status="protocol_blocked",
            failure_reason=str(exc),
        )
    surface = source.repo_readout_surface
    results_dir = surface / "results"
    results_dir.mkdir(parents=True, exist_ok=True)
    stage_status_rows = _stage_status_rows(source)
    suite_status = _suite_status(source)
    suite_claim = _suite_claim(source)
    badge_rows = build_badges(source, suite_status)
    badge_paths = write_badge_svgs(surface, badge_rows)

    generated_paths = {
        "results/stage_status_summary.csv": str(results_dir / "stage_status_summary.csv"),
        "results/suite_status_summary.csv": str(results_dir / "suite_status_summary.csv"),
        "results/suite_claim_summary.csv": str(results_dir / "suite_claim_summary.csv"),
        "results/badge_summary.csv": str(results_dir / "badge_summary.csv"),
    }
    write_csv(
        results_dir / "stage_status_summary.csv",
        stage_status_rows,
        STAGE_READOUT_FIELDS,
        create_parents=True,
    )
    write_csv(
        results_dir / "suite_status_summary.csv",
        [suite_status],
        SUITE_STATUS_FIELDS,
        create_parents=True,
    )
    write_csv(
        results_dir / "suite_claim_summary.csv",
        [suite_claim],
        SUITE_CLAIM_FIELDS,
        create_parents=True,
    )
    write_csv(results_dir / "badge_summary.csv", badge_rows, BADGE_FIELDS, create_parents=True)
    _repair_parent_stage_run_index(source)
    generated_paths.update(_write_markdown_docs(source, suite_status, suite_claim, badge_rows))
    generated_paths.update(badge_paths)
    archive_paths = _maybe_write_system_learning_archive(source, config, suite_claim)
    generated_paths.update(archive_paths)
    _update_suite_readout_source(source, generated_paths, suite_status, suite_claim, badge_rows)
    return ReadoutSystemLearningResult(
        status="complete",
        readout_source_path=source.path,
        readout_surface=surface,
        generated_paths=generated_paths,
        suite_status=str(suite_status["suite_status"]),
        claim_status=str(suite_claim["claim_status"]),
    )


STAGE_READOUT_FIELDS = (
    "stage_number",
    "short_name",
    "stage_id",
    "status",
    "claim_status",
    "claim_boundary",
    "readout_source",
    "source_artifact_root",
    "blocking_reason",
)

SUITE_STATUS_FIELDS = (
    "suite_status",
    "completed_stage_count",
    "implemented_stage_count",
    "first_not_complete_stage",
    "suite_reason",
)

SUITE_CLAIM_FIELDS = (
    "claim_status",
    "target_claim",
    "bounded_interpretation",
    "counter_signal",
    "claim_boundary",
    "source_table",
)


def _stage_status_rows(source: SuiteReadoutSource) -> list[dict[str, object]]:
    return [
        {
            "stage_number": record.stage_number,
            "short_name": record.short_name,
            "stage_id": record.stage_id,
            "status": _display_status(record),
            "claim_status": _display_claim_status(record),
            "claim_boundary": _display_claim_boundary(record),
            "readout_source": ""
            if record.readout_source_path is None
            else record.readout_source_path,
            "source_artifact_root": ""
            if record.source_artifact_root is None
            else record.source_artifact_root,
            "blocking_reason": _display_blocking_reason(record),
        }
        for record in source.stage_records
    ]


def _suite_status(source: SuiteReadoutSource) -> dict[str, object]:
    records = _display_records(source)
    completed = [record for record in records if record["status"] == "complete"]
    stage6 = _record(source, "paired_replicate_comparison")
    if stage6.status == "complete":
        if stage6.claim_status == "paired_comparison_inconclusive":
            status = "complete_inconclusive"
        else:
            status = "complete_limited_signal"
        reason = (
            "Stages 1-7 completed. Stage 6 produced bounded paired comparison "
            f"status `{stage6.claim_status}`, and Stage 7 produced the human "
            "readout/system-learning surface."
        )
    else:
        status = "blocked_before_comparison"
        reason = "The suite did not reach a completed paired comparison stage."
    first_not_complete = next(
        (str(record["short_name"]) for record in records if record["status"] != "complete"),
        "",
    )
    return {
        "suite_status": status,
        "completed_stage_count": len(completed),
        "implemented_stage_count": len(STAGE_DEFINITIONS),
        "first_not_complete_stage": first_not_complete,
        "suite_reason": reason,
    }


def _suite_claim(source: SuiteReadoutSource) -> dict[str, object]:
    stage6 = _record(source, "paired_replicate_comparison")
    claim_rows = read_stage_table(stage6, "comparison_claim_summary")
    arm_rows = read_stage_table(stage6, "arm_summary")
    claim = claim_rows[0] if claim_rows else {}
    direct = _arm(arm_rows, "direct_concrete_baseline")
    tower = _arm(arm_rows, "selected_tower_candidate")
    counter_signal = ""
    if direct and tower:
        counter_signal = (
            "Tower mean reward was "
            f"{tower.get('mean_total_reward', '')} versus direct "
            f"{direct.get('mean_total_reward', '')}; tower invalid moves were "
            f"{tower.get('invalid_move_count', '')} versus direct "
            f"{direct.get('invalid_move_count', '')}."
        )
    return {
        "claim_status": claim.get("claim_status", stage6.claim_status),
        "target_claim": claim.get("bounded_claim", ""),
        "bounded_interpretation": (
            "The target metric is Stage 5 binary goal success. Other metrics can explain "
            "the run, but they do not reverse the Stage 6 target claim."
        ),
        "counter_signal": counter_signal,
        "claim_boundary": claim.get("claim_boundary", stage6.claim_boundary),
        "source_table": stage6.source_files.get("comparison_claim_summary", ""),
    }


def _write_markdown_docs(
    source: SuiteReadoutSource,
    suite_status: dict[str, object],
    suite_claim: dict[str, object],
    badge_rows: list[dict[str, str]],
) -> dict[str, str]:
    surface = source.repo_readout_surface
    results_dir = surface / "results"
    clarification = _preserve_clarification(surface / "README.md")
    paths = {
        "README.md": surface / "README.md",
        "result_readout.md": surface / "result_readout.md",
        "method.md": surface / "method.md",
        "artifact_index.md": surface / "artifact_index.md",
        "glossary.md": surface / "glossary.md",
        "runbook.md": surface / "runbook.md",
        "results/summary.md": results_dir / "summary.md",
        "results/stage_status.md": results_dir / "stage_status.md",
        "results/structural_readout.md": results_dir / "structural_readout.md",
        "results/schema_sweep_readout.md": results_dir / "schema_sweep_readout.md",
        "results/candidate_readout.md": results_dir / "candidate_readout.md",
        "results/training_health_readout.md": results_dir / "training_health_readout.md",
        "results/threshold_frontier_readout.md": results_dir / "threshold_frontier_readout.md",
        "results/paired_comparison_readout.md": results_dir / "paired_comparison_readout.md",
        "results/system_learning_prompt.md": results_dir / "system_learning_prompt.md",
    }
    badge_block = "\n".join(
        f"![{row['label']}: {row['value']}](badges/{row['badge_id']}.svg)"
        for row in badge_rows
    )
    stage_table = "\n".join(
        "| {stage_number} | {short_name} | {status} | {claim_status} |".format(**record)
        for record in _display_records(source)
    )
    structural = _structural_facts(source)
    paths["README.md"].write_text(
        "\n".join(
            [
                "# PlateSupport Standard Gauntlet",
                "",
                badge_block,
                "",
                "## Result",
                "",
                str(suite_status["suite_reason"]),
                "",
                str(suite_claim["target_claim"]),
                "",
                str(suite_claim["bounded_interpretation"]),
                "",
                "## Key Numbers",
                "",
                f"- Valid states: `{structural.get('valid_state_count', '')}`",
                f"- Shortest path length: `{structural.get('shortest_path_length', '')}`",
                f"- Random-policy success rate: `{structural.get('random_success_rate', '')}`",
                f"- Stage 6 counter-signal: {suite_claim['counter_signal']}",
                "",
                "## Stage Status",
                "",
                "| Stage | Name | Status | Claim Status |",
                "| --- | --- | --- | --- |",
                stage_table,
                "",
                "## Artifact Provenance",
                "",
                f"- Readout source: `{source.path}`",
                f"- Raw artifact root: `{source.source_artifact_root}`",
                f"- Suite evaluation root: `{source.source_evaluation_root}`",
                "",
                "## Claim Boundary",
                "",
                str(suite_claim["claim_boundary"]),
                "",
                "## Clarifying Turns",
                "",
                clarification,
                "",
            ]
        ),
        encoding="utf-8",
    )
    _write_result_readout(paths["result_readout.md"], source, suite_status, suite_claim)
    _write_method(paths["method.md"], source)
    _write_artifact_index(paths["artifact_index.md"], source, paths)
    _write_glossary(paths["glossary.md"])
    _write_runbook(paths["runbook.md"], source)
    _write_stage_detail_files(paths, source, suite_status, suite_claim)
    return {key: str(path) for key, path in paths.items()}


def _write_result_readout(
    path: Path,
    source: SuiteReadoutSource,
    suite_status: dict[str, object],
    suite_claim: dict[str, object],
) -> None:
    lines = [
        "# PlateSupport Standard Gauntlet Result Readout",
        "",
        str(suite_status["suite_reason"]),
        "",
        "The target claim is bounded by the Stage 5 binary-success target and the",
        "Stage 6 smoke budget. The result should not be read as a general claim about",
        "all tower policies or all PlateSupport thresholds.",
        "",
        "## Stage Narrative",
        "",
    ]
    for record in source.stage_records:
        lines.extend(
            [
                f"### Stage {record.stage_number}: {record.short_name}",
                "",
                f"- Status: `{_display_status(record)}`",
                f"- Claim status: `{_display_claim_status(record)}`",
                f"- Boundary: {_display_claim_boundary(record)}",
                "",
            ]
        )
    lines.extend(
        [
            "## Comparison Interpretation",
            "",
            str(suite_claim["target_claim"]),
            "",
            str(suite_claim["counter_signal"]),
            "",
        ]
    )
    path.write_text("\n".join(lines), encoding="utf-8")


def _write_method(path: Path, source: SuiteReadoutSource) -> None:
    path.write_text(
        "\n".join(
            [
                "# PlateSupport Standard Gauntlet Method",
                "",
                "The suite runs a staged benchmark pipeline: structural diagnostics,",
                "contraction-schema sweep, candidate discovery, tower-training health,",
                "threshold calibration, paired comparison, and human readout synthesis.",
                "",
                "The paired comparison uses explicit seed bundles shared by active arms.",
                "The Stage 6 direct concrete baseline and selected tower candidate are",
                "trained with the same episode budget and evaluated against the Stage 5",
                "target policy.",
                "",
                "If Stage 4 includes a trainable iterated source-local ratio candidate,",
                "the readout emits iterated-candidate and tier-count badges from the",
                "Stage 4 candidate-training-health table.",
                "",
                "The readout was generated from this explicit source binding:",
                "",
                f"```text\n{source.path}\n```",
                "",
            ]
        ),
        encoding="utf-8",
    )


def _write_artifact_index(
    path: Path,
    source: SuiteReadoutSource,
    generated_paths: dict[str, Path],
) -> None:
    lines = [
        "# PlateSupport Standard Gauntlet Artifact Index",
        "",
        f"- Suite readout source: `{source.path}`",
        f"- Raw artifact root: `{source.source_artifact_root}`",
        f"- Suite evaluation root: `{source.source_evaluation_root}`",
        "",
        "## Stage Sources",
        "",
    ]
    for record in source.stage_records:
        lines.append(
            f"- Stage {record.stage_number} `{record.short_name}`: "
            f"`{record.readout_source_path}`"
        )
    lines.extend(["", "## Generated Readout Files", ""])
    for key, generated_path in sorted(generated_paths.items()):
        lines.append(f"- `{key}`: `{generated_path}`")
    path.write_text("\n".join(lines) + "\n", encoding="utf-8")


def _write_glossary(path: Path) -> None:
    path.write_text(
        "\n".join(
            [
                "# PlateSupport Standard Gauntlet Glossary",
                "",
                "- `stage`: One checkpoint in the standard gauntlet pipeline.",
                "- `candidate`: A contraction schema selected for downstream training.",
                "- `tower`: A hierarchy of contracted state/action views.",
                "- `target policy`: The Stage 5 rule used to score Stage 6 episodes.",
                "- `paired replicate`: A seed-matched comparison unit across arms.",
                "- `claim boundary`: The limit on what the current evidence supports.",
                "",
            ]
        ),
        encoding="utf-8",
    )


def _write_runbook(path: Path, source: SuiteReadoutSource) -> None:
    path.write_text(
        "\n".join(
            [
                "# PlateSupport Standard Gauntlet Runbook",
                "",
                "The canonical human-readout invocation is:",
                "",
                "```text",
                "execute docs/prime_directive/artifact_table_to_readable_document_protocol.md "
                f"at {source.path}",
                "```",
                "",
                "Do not point the protocol at the artifact root or infer the latest run.",
                "",
                "The optional CLI equivalent is:",
                "",
                "```text",
                "uv run python -m big_boy_benchmarking.cli plate-support "
                f"standard-gauntlet readout build --readout-source {source.path}",
                "```",
                "",
            ]
        ),
        encoding="utf-8",
    )


def _write_stage_detail_files(
    paths: dict[str, Path],
    source: SuiteReadoutSource,
    suite_status: dict[str, object],
    suite_claim: dict[str, object],
) -> None:
    paths["results/summary.md"].write_text(
        "\n".join(
            [
                "# Suite Summary",
                "",
                f"- Suite status: `{suite_status['suite_status']}`",
                f"- Claim status: `{suite_claim['claim_status']}`",
                f"- Claim: {suite_claim['target_claim']}",
                f"- Counter-signal: {suite_claim['counter_signal']}",
                "",
            ]
        ),
        encoding="utf-8",
    )
    paths["results/stage_status.md"].write_text(
        "\n".join(
            [
                "# Stage Status",
                "",
                *[
                    f"- Stage {record.stage_number} `{record.short_name}`: "
                    f"`{_display_status(record)}` / `{_display_claim_status(record)}`"
                    for record in source.stage_records
                ],
                "",
            ]
        ),
        encoding="utf-8",
    )
    detail_map = {
        "results/structural_readout.md": "structural_and_tower_diagnostics",
        "results/schema_sweep_readout.md": "contraction_schema_sweep",
        "results/candidate_readout.md": "candidate_discovery",
        "results/training_health_readout.md": "tower_training_health",
        "results/threshold_frontier_readout.md": "threshold_frontier_calibration",
        "results/paired_comparison_readout.md": "paired_replicate_comparison",
    }
    for key, short_name in detail_map.items():
        record = _record(source, short_name)
        paths[key].write_text(_stage_detail_text(record), encoding="utf-8")
    paths["results/system_learning_prompt.md"].write_text(
        "\n".join(
            [
                "# System Learning Prompt",
                "",
                "If discussion of this generated readout uncovers durable protocol,",
                "architecture, or user-confusion lessons, preserve them under:",
                "",
                "```text",
                "docs/design/system_learning_from_evaluations/plate_support_standard_gauntlet_v001/",
                "```",
                "",
                "Generated README clarification turns are useful working memory, but they",
                "are not permanent design memory until archived with attribution.",
                "",
            ]
        ),
        encoding="utf-8",
    )


def _stage_detail_text(record: StageSourceRecord) -> str:
    return "\n".join(
        [
            f"# Stage {record.stage_number}: {record.short_name}",
            "",
            f"- Status: `{_display_status(record)}`",
            f"- Claim status: `{_display_claim_status(record)}`",
            f"- Claim boundary: {_display_claim_boundary(record)}",
            f"- Readout source: `{record.readout_source_path}`",
            f"- Artifact root: `{record.source_artifact_root}`",
            f"- Blocking reason: `{record.blocking_reason}`",
            "",
        ]
    )


def _maybe_write_system_learning_archive(
    source: SuiteReadoutSource,
    config: ReadoutSystemLearningConfig,
    suite_claim: dict[str, object],
) -> dict[str, str]:
    if not config.create_system_learning_archive:
        return {}
    archive = (
        source.repo_root
        / "docs"
        / "design"
        / "system_learning_from_evaluations"
        / "plate_support_standard_gauntlet_v001"
    )
    archive.mkdir(parents=True, exist_ok=True)
    readme = archive / "README.md"
    readme.write_text(
        "\n".join(
            [
                "# PlateSupport Standard Gauntlet System Learning",
                "",
                "This folder preserves durable lessons discovered while interpreting the",
                "generated PlateSupport standard gauntlet readout.",
                "",
                f"- Current suite claim status: `{suite_claim['claim_status']}`",
                f"- Source readout: `{source.path}`",
                "",
            ]
        ),
        encoding="utf-8",
    )
    return {"system_learning/README.md": str(readme)}


def _update_suite_readout_source(
    source: SuiteReadoutSource,
    generated_paths: dict[str, str],
    suite_status: dict[str, object],
    suite_claim: dict[str, object],
    badge_rows: list[dict[str, str]],
) -> None:
    with source.path.open(encoding="utf-8") as handle:
        payload = json_loads_dict(handle.read())
    payload["run_mode"] = "smoke_stage_1_to_7_readout_complete"
    payload["claim_boundary"] = [
        "Smoke-suite evidence currently supports PlateSupport standard-gauntlet "
        "progression through Stage 7 readout/system-learning synthesis.",
        "Under this smoke Stage 6 budget, the selected tower candidate is below "
        "the direct baseline on Stage 5 target-hit rate.",
        "Tower mean reward and invalid-move counters are explanatory "
        "counter-signals, not replacements for the bounded Stage 6 target claim.",
    ]
    expected_files = payload.get("expected_files")
    if isinstance(expected_files, dict):
        expected_files["pending_not_yet_run"] = []
    payload["generated_readout_files"] = generated_paths
    payload["readout_badges"] = {
        row["badge_id"]: {
            "label": row["label"],
            "value": row["value"],
            "color": row["color"],
            "reason": row["reason"],
            "source": row["source"],
        }
        for row in badge_rows
    }
    payload["suite_status"] = suite_status
    payload["suite_claim"] = suite_claim
    write_json(source.path, payload, create_parents=True)


def _repair_parent_stage_run_index(source: SuiteReadoutSource) -> None:
    run_index_path = source.source_evaluation_root / "stage_run_index.csv"
    rows = [
        {
            "suite_id": "plate_support_standard_gauntlet_v001",
            "stage_id": record.stage_id,
            "run_label": source.run_label,
            "artifact_root": source.source_artifact_root,
            "status": record.status,
        }
        for record in source.stage_records
        if record.status != "not_run"
        and record.stage_id != READOUT_SYSTEM_LEARNING_STAGE_ID
    ]
    rows.append(
        {
            "suite_id": "plate_support_standard_gauntlet_v001",
            "stage_id": READOUT_SYSTEM_LEARNING_STAGE_ID,
            "run_label": source.run_label,
            "artifact_root": source.source_artifact_root,
            "status": "complete",
        }
    )
    write_csv(
        run_index_path,
        rows,
        ("suite_id", "stage_id", "run_label", "artifact_root", "status"),
        create_parents=True,
    )
    status_path = source.source_evaluation_root / "stage_status_summary.csv"
    if status_path.exists():
        with status_path.open(encoding="utf-8", newline="") as handle:
            status_rows = list(csv.DictReader(handle))
    else:
        status_rows = []
    status_rows = [
        row for row in status_rows if row.get("stage_id") != READOUT_SYSTEM_LEARNING_STAGE_ID
    ]
    status_rows.append(
        {
            "suite_id": "plate_support_standard_gauntlet_v001",
            "stage_id": READOUT_SYSTEM_LEARNING_STAGE_ID,
            "environment_family_id": "plate_support",
            "environment_instance_id": "plate_support_5x5_default_v001",
            "artifact_root": str(source.source_artifact_root),
            "status": "complete",
            "claim_status": "readout_complete",
            "claim_boundary": "human readout and system-learning synthesis only",
            "source_stage_ids": "",
            "source_artifact_paths": str(source.path),
            "linearization_mode_id": "tensor_available_disabled",
            "state_collapser_dependency_status": "ok",
        }
    )
    write_csv(
        status_path,
        status_rows,
        (
            "suite_id",
            "stage_id",
            "environment_family_id",
            "environment_instance_id",
            "artifact_root",
            "status",
            "claim_status",
            "claim_boundary",
            "source_stage_ids",
            "source_artifact_paths",
            "linearization_mode_id",
            "state_collapser_dependency_status",
        ),
        create_parents=True,
    )


def _preserve_clarification(readme: Path) -> str:
    empty_turns = (
        "### Evaluator Turn 1\n\n"
        "_Add evaluator question or concern here._\n\n"
        "### Codex Turn 1\n\n"
        "_Add Codex response here._"
    )
    if not readme.exists():
        return empty_turns
    text = readme.read_text(encoding="utf-8")
    marker = "## Clarifying Turns"
    if marker not in text:
        return empty_turns
    return text.split(marker, 1)[1].strip()


def _structural_facts(source: SuiteReadoutSource) -> dict[str, str]:
    record = _record(source, "structural_and_tower_diagnostics")
    state_rows = read_stage_table(record, "state_space_summary")
    shortest_rows = read_stage_table(record, "shortest_path_summary")
    random_rows = read_stage_table(record, "random_policy_recon_summary")
    return {
        "valid_state_count": _first(state_rows, "valid_state_count"),
        "shortest_path_length": _first(shortest_rows, "shortest_path_length"),
        "random_success_rate": _first(random_rows, "success_rate"),
    }


def _arm(rows: list[dict[str, str]], arm_type: str) -> dict[str, str]:
    return next((row for row in rows if row.get("arm_type") == arm_type), {})


def _record(source: SuiteReadoutSource, short_name: str) -> StageSourceRecord:
    for record in source.stage_records:
        if record.short_name == short_name:
            return record
    raise KeyError(short_name)


def _display_records(source: SuiteReadoutSource) -> list[dict[str, object]]:
    return [
        {
            "stage_number": record.stage_number,
            "short_name": record.short_name,
            "stage_id": record.stage_id,
            "status": _display_status(record),
            "claim_status": _display_claim_status(record),
            "claim_boundary": _display_claim_boundary(record),
        }
        for record in source.stage_records
    ]


def _display_status(record: StageSourceRecord) -> str:
    if record.stage_id == READOUT_SYSTEM_LEARNING_STAGE_ID:
        return "complete"
    return record.status


def _display_claim_status(record: StageSourceRecord) -> str:
    if record.stage_id == READOUT_SYSTEM_LEARNING_STAGE_ID:
        return "readout_complete"
    return record.claim_status


def _display_claim_boundary(record: StageSourceRecord) -> str:
    if record.stage_id == READOUT_SYSTEM_LEARNING_STAGE_ID:
        return "human readout and system-learning synthesis only"
    return record.claim_boundary


def _display_blocking_reason(record: StageSourceRecord) -> str:
    if record.stage_id == READOUT_SYSTEM_LEARNING_STAGE_ID:
        return ""
    return record.blocking_reason


def _first(rows: list[dict[str, str]], key: str) -> str:
    if not rows:
        return ""
    return str(rows[0].get(key, ""))


def json_loads_dict(text: str) -> dict[str, object]:
    import json

    payload = json.loads(text)
    if not isinstance(payload, dict):
        return {}
    return payload
