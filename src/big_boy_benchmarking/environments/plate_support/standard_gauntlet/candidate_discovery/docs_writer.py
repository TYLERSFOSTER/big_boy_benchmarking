"""Human-doc seed writer for Stage 3 candidate discovery."""

from __future__ import annotations

from pathlib import Path


def write_candidate_discovery_docs(
    *,
    readout_surface: Path,
    artifact_root: Path,
    stage_root: Path,
    aggregate_summary: dict[str, object],
    readout_source_path: Path,
    output_paths: dict[str, str],
) -> dict[str, str]:
    """Write Stage 3 seed docs and artifact index."""

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
                "# PlateSupport Candidate Discovery",
                "",
                "## Status",
                "",
                f"Status: {aggregate_summary['status']}.",
                "",
                "This stage classifies Stage 2 candidate-signal rows and writes a",
                "candidate manifest. It does not train candidates and does not compare",
                "performance.",
                "",
                f"- Stage artifact root: `{stage_root}`",
                f"- Suite artifact root: `{artifact_root}`",
                f"- Readout source: `{readout_source_path}`",
                "",
            ]
        ),
        encoding="utf-8",
    )
    method.write_text(
        "\n".join(
            [
                "# PlateSupport Candidate Discovery Method",
                "",
                "Candidate discovery consumes Stage 2 summary tables, classifies every",
                "schema signal row, assigns deterministic candidate IDs, and emits",
                "downstream training-health input rows only for selected training",
                "candidates.",
                "",
                "Candidate rows preserve schema construction metadata such as",
                "`schema_mode`, ratio numerator/denominator, max iterations, selector",
                "rule, selection mode, max depth, and nontrivial tier count. Later",
                "stages must consume this metadata directly instead of reverse",
                "engineering schema semantics from `schema_id`.",
                "",
            ]
        ),
        encoding="utf-8",
    )
    runbook.write_text(
        "\n".join(
            [
                "# PlateSupport Candidate Discovery Runbook",
                "",
                "Run Stage 3 with:",
                "",
                "```text",
                "uv run python -m big_boy_benchmarking.cli plate-support standard-gauntlet candidate-discovery run \\",
                "  --repo-root <repo-root> \\",
                "  --artifact-root docs/evaluations/plate_support_5x5_default_v001/standard_gauntlet/artifacts/smoke_001 \\",
                "  --schema-sweep-source docs/evaluations/plate_support_5x5_default_v001/standard_gauntlet/contraction_schema_sweep/readout_source.json \\",
                "  --run-label smoke_001 \\",
                "  --locked-by foster",
                "```",
                "",
            ]
        ),
        encoding="utf-8",
    )
    artifact_index.write_text(
        "\n".join(
            [
                "# PlateSupport Candidate Discovery Artifact Index",
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
                "# Stage 3 Results Summary",
                "",
                f"- status: `{aggregate_summary['status']}`",
                f"- claim status: `{aggregate_summary['claim_status']}`",
                f"- selected training candidates: `{aggregate_summary['selected_training_candidate_count']}`",
                f"- blocking reason: `{aggregate_summary['blocking_reason']}`",
                "",
            ]
        ),
        encoding="utf-8",
    )
    return {
        "README.md": str(readme),
        "method.md": str(method),
        "runbook.md": str(runbook),
        "artifact_index.md": str(artifact_index),
        "results/summary.md": str(summary),
    }
