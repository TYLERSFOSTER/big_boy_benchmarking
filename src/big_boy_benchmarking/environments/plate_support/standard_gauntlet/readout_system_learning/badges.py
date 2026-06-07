"""Evidence-derived badge writer for PlateSupport gauntlet readouts."""

from __future__ import annotations

from pathlib import Path

from .stage_sources import SuiteReadoutSource

BADGE_FIELDS = (
    "badge_id",
    "label",
    "value",
    "status_class",
    "color",
    "source",
    "reason",
    "path",
)


def build_badges(
    source: SuiteReadoutSource,
    suite_status: dict[str, object],
) -> list[dict[str, str]]:
    """Build badge rows from source tables and status summaries."""

    statuses = {record.short_name: record.claim_status for record in source.stage_records}
    return [
        _badge(
            "suite_status",
            "Suite",
            _display_suite_status(str(suite_status["suite_status"])),
            _color_for_suite(str(suite_status["suite_status"])),
            "results/suite_status_summary.csv:suite_status",
            str(suite_status["suite_reason"]),
        ),
        _badge(
            "artifacts_complete",
            "Artifacts",
            "Complete",
            "green",
            "readout_source.json:source_artifact_root",
            "Source artifacts and generated readouts are repository-resident.",
        ),
        _badge(
            "structural_readiness",
            "Structure",
            _display_claim_status(statuses.get("structural_and_tower_diagnostics", "not_run")),
            "green" if statuses.get("structural_and_tower_diagnostics") else "yellow",
            "stage_status_summary.csv:claim_status",
            "Stage 1 structural diagnostics are represented in the suite status table.",
        ),
        _badge(
            "schema_candidates",
            "Candidate",
            _display_claim_status(statuses.get("candidate_discovery", "not_run")),
            "green" if statuses.get("candidate_discovery") == "candidate_found" else "yellow",
            "stage_status_summary.csv:claim_status",
            "Candidate status is copied from Stage 3, not inferred.",
        ),
        _badge(
            "training_health",
            "Training",
            _display_claim_status(statuses.get("tower_training_health", "not_run")),
            "green" if statuses.get("tower_training_health") == "trainable_clean" else "yellow",
            "stage_status_summary.csv:claim_status",
            "Training-health status is copied from Stage 4.",
        ),
        _badge(
            "target_calibrated",
            "Target",
            _display_claim_status(statuses.get("threshold_frontier_calibration", "not_run")),
            "green"
            if statuses.get("threshold_frontier_calibration") == "threshold_calibrated"
            else "yellow",
            "stage_status_summary.csv:claim_status",
            "Target calibration status is copied from Stage 5.",
        ),
        _badge(
            "paired_comparison",
            "Paired",
            _display_claim_status(statuses.get("paired_replicate_comparison", "not_run")),
            _color_for_claim(statuses.get("paired_replicate_comparison", "not_run")),
            "stage_status_summary.csv:claim_status",
            "Paired-comparison status is copied from Stage 6.",
        ),
        _badge(
            "provenance_repo_artifacts",
            "Provenance",
            "Repo Artifacts",
            "blue",
            "readout_source.json",
            "Readout was generated from an explicit suite readout source binding.",
        ),
    ]


def write_badge_svgs(readout_surface: Path, badge_rows: list[dict[str, str]]) -> dict[str, str]:
    """Write simple SVG badge files."""

    badge_dir = readout_surface / "badges"
    badge_dir.mkdir(parents=True, exist_ok=True)
    for stale_badge in badge_dir.glob("*.svg"):
        stale_badge.unlink()
    paths = {}
    for row in badge_rows:
        path = badge_dir / f"{row['badge_id']}.svg"
        path.write_text(_svg(row["label"], row["value"], row["color"]), encoding="utf-8")
        row["path"] = str(path)
        paths[row["badge_id"]] = str(path)
    return paths


def _badge(
    badge_id: str,
    label: str,
    value: str,
    color: str,
    source: str,
    reason: str,
) -> dict[str, str]:
    return {
        "badge_id": badge_id,
        "label": label,
        "value": value,
        "status_class": color,
        "color": color,
        "source": source,
        "reason": reason,
        "path": "",
    }


def _color_for_suite(status: str) -> str:
    if status == "complete_claim_ready":
        return "green"
    if status == "complete_limited_signal":
        return "yellow"
    if status in {"complete_inconclusive", "complete_no_comparison"}:
        return "yellow"
    return "red"


def _color_for_claim(claim_status: str) -> str:
    if claim_status == "paired_comparison_positive_signal":
        return "green"
    if claim_status == "paired_comparison_negative_signal":
        return "orange"
    if claim_status == "paired_comparison_inconclusive":
        return "yellow"
    return "red"


def _display_suite_status(status: str) -> str:
    return {
        "complete_limited_signal": "Limited Signal",
        "complete_claim_ready": "Claim Ready",
        "complete_inconclusive": "Inconclusive",
        "complete_no_comparison": "No Comparison",
        "blocked_before_comparison": "Blocked",
    }.get(status, _title_from_status(status))


def _display_claim_status(status: str) -> str:
    return {
        "diagnostic_complete": "Complete",
        "candidate_found": "Found",
        "candidate_not_found": "Not Found",
        "trainable_clean": "Clean",
        "trainable_warning": "Warning",
        "threshold_calibrated": "Calibrated",
        "threshold_unresolved": "Unresolved",
        "paired_comparison_positive_signal": "Positive Signal",
        "paired_comparison_negative_signal": "Negative Signal",
        "paired_comparison_inconclusive": "Inconclusive",
        "readout_complete": "Complete",
        "not_run": "Not Run",
    }.get(status, _title_from_status(status))


def _title_from_status(status: str) -> str:
    return " ".join(part.capitalize() for part in status.split("_") if part) or "Unknown"


def _svg(label: str, value: str, color: str) -> str:
    colors = {
        "green": "#2e7d32",
        "yellow": "#b58900",
        "orange": "#ef6c00",
        "red": "#d32f2f",
        "blue": "#1565c0",
    }
    fill = colors.get(color, "#4a5568")
    label_width = max(70, 7 * len(label) + 12)
    value_width = max(70, 7 * len(value) + 12)
    width = label_width + value_width
    return (
        '<svg xmlns="http://www.w3.org/2000/svg" '
        f'width="{width}" height="20" role="img" aria-label="{label}: {value}">'
        f'<rect width="{label_width}" height="20" fill="#555"/>'
        f'<rect x="{label_width}" width="{value_width}" height="20" fill="{fill}"/>'
        f'<text x="{label_width / 2}" y="14" fill="#fff" text-anchor="middle" '
        'font-family="Verdana,Geneva,sans-serif" font-size="11">'
        f"{label}</text>"
        f'<text x="{label_width + value_width / 2}" y="14" fill="#fff" '
        'text-anchor="middle" font-family="Verdana,Geneva,sans-serif" font-size="11">'
        f"{value}</text></svg>\n"
    )
