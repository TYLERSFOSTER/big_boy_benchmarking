"""Human-doc seed writer for PlateSupport gauntlet Stage 1."""

from __future__ import annotations

from pathlib import Path

from big_boy_benchmarking.artifacts.writers import write_json
from big_boy_benchmarking.environments.plate_support.standard_gauntlet.ids import (
    STRUCTURAL_TOWER_DIAGNOSTICS_STAGE_ID,
    SUITE_ID,
)


def write_stage1_docs(
    *,
    readout_surface: Path,
    artifact_root: Path,
    stage_root: Path,
    aggregate_summary: dict[str, object],
    readout_source_path: Path,
    output_paths: dict[str, str],
) -> dict[str, str]:
    """Write Stage 1 seed docs and artifact index."""

    results_dir = readout_surface / "results"
    results_dir.mkdir(parents=True, exist_ok=True)
    readout_surface.mkdir(parents=True, exist_ok=True)

    readme = readout_surface / "README.md"
    method = readout_surface / "method.md"
    runbook = readout_surface / "runbook.md"
    artifact_index = readout_surface / "artifact_index.md"
    summary = results_dir / "summary.md"

    readme.write_text(
        "\n".join(
            [
                "# PlateSupport Structural And Tower Diagnostics",
                "",
                "## Status",
                "",
                f"Status: {aggregate_summary['status']}.",
                "",
                "This Stage 1 readout surface records diagnostic evidence only. It does not",
                "claim tower learning improvement, candidate quality, threshold calibration,",
                "or flat-versus-tower comparison success.",
                "",
                "## Machine Evidence",
                "",
                f"- Stage artifact root: `{stage_root}`",
                f"- Suite artifact root: `{artifact_root}`",
                f"- Readout source: `{readout_source_path}`",
                "",
                "## Claim Boundary",
                "",
                str(aggregate_summary["claim_boundary"]),
                "",
            ]
        ),
        encoding="utf-8",
    )
    method.write_text(
        "\n".join(
            [
                "# PlateSupport Structural And Tower Diagnostics Method",
                "",
                "Stage 1 validates the environment-readiness source, reruns structural",
                "diagnostics inside the evaluation artifact tree, and emits downstream",
                "readiness gates for the schema sweep.",
                "",
                "Random policy reconnaissance is labeled structural difficulty evidence,",
                "not a learning baseline.",
                "",
            ]
        ),
        encoding="utf-8",
    )
    runbook.write_text(
        "\n".join(
            [
                "# PlateSupport Structural And Tower Diagnostics Runbook",
                "",
                "Run Stage 1 with:",
                "",
                "```text",
                "uv run python -m big_boy_benchmarking.cli plate-support standard-gauntlet structural-diagnostics run \\",
                "  --artifact-root docs/evaluations/plate_support_5x5_default_v001/standard_gauntlet/artifacts/smoke_001 \\",
                "  --readiness-source docs/environments/plate_support_5x5_default_v001/readiness/dev_001/readout_source.json \\",
                "  --run-label smoke_001 \\",
                "  --locked-by foster",
                "```",
                "",
                "Generate human-readable docs from:",
                "",
                "```text",
                "execute docs/prime_directive/artifact_table_to_readable_document_protocol.md at docs/evaluations/plate_support_5x5_default_v001/standard_gauntlet/structural_and_tower_diagnostics/readout_source.json",
                "```",
                "",
            ]
        ),
        encoding="utf-8",
    )
    artifact_index.write_text(
        "\n".join(
            [
                "# PlateSupport Structural And Tower Diagnostics Artifact Index",
                "",
                f"- suite id: `{SUITE_ID}`",
                f"- stage id: `{STRUCTURAL_TOWER_DIAGNOSTICS_STAGE_ID}`",
                "",
                "## Outputs",
                "",
                *[f"- `{key}`: `{value}`" for key, value in sorted(output_paths.items())],
                "",
            ]
        ),
        encoding="utf-8",
    )
    summary.write_text(
        "\n".join(
            [
                "# Stage 1 Results Summary",
                "",
                f"- status: `{aggregate_summary['status']}`",
                f"- claim status: `{aggregate_summary['claim_status']}`",
                f"- ready for schema sweep: `{aggregate_summary['ready_for_schema_sweep']}`",
                f"- blocking reason: `{aggregate_summary['blocking_reason']}`",
                "",
            ]
        ),
        encoding="utf-8",
    )
    write_json(readout_surface / "docs_manifest.json", output_paths, create_parents=True)
    return {
        "README.md": str(readme),
        "method.md": str(method),
        "runbook.md": str(runbook),
        "artifact_index.md": str(artifact_index),
        "results/summary.md": str(summary),
    }
