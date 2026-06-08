"""Human-doc seed writer for PlateSupport gauntlet Stage 4."""

from __future__ import annotations

from pathlib import Path


def write_tower_training_health_docs(
    *,
    readout_surface: Path,
    artifact_root: Path,
    stage_root: Path,
    aggregate_summary: dict[str, object],
    readout_source_path: Path,
    output_paths: dict[str, str],
) -> dict[str, str]:
    """Write Stage 4 seed docs and artifact index."""

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
                "# PlateSupport Tower Training Health",
                "",
                "## Status",
                "",
                f"Status: {aggregate_summary['status']}.",
                "",
                "This stage trains selected tower candidates only to check whether",
                "concrete steps, executable lifts, tier/controller choices, and learner",
                "updates can be observed. It does not compare tower and flat policies.",
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
                "# PlateSupport Tower Training Health Method",
                "",
                "Stage 4 consumes Stage 3 selected candidates, rebuilds their tower",
                "schemas, selects executable action cells from the deepest currently",
                "executable tier, resolves them to concrete PlateSupport actions, and",
                "applies a tabular Q update. The stage records training health evidence,",
                "not comparison evidence.",
                "",
                "The schema factory is metadata-first. One-shot",
                "`source_local_ratio` candidates rebuild the one-block catch schema;",
                "iterated `source_local_ratio_iterated` candidates rebuild the",
                "multi-block iterated schema using the preserved ratio, selector,",
                "selection mode, and max-iteration fields from Stage 3.",
                "",
            ]
        ),
        encoding="utf-8",
    )
    runbook.write_text(
        "\n".join(
            [
                "# PlateSupport Tower Training Health Runbook",
                "",
                "Run Stage 4 with:",
                "",
                "```text",
                "uv run python -m big_boy_benchmarking.cli plate-support "
                "standard-gauntlet tower-training-health run \\",
                "  --repo-root <repo-root> \\",
                "  --artifact-root docs/evaluations/plate_support_5x5_default_v001/"
                "standard_gauntlet/artifacts/smoke_001 \\",
                "  --candidate-source docs/evaluations/plate_support_5x5_default_v001/"
                "standard_gauntlet/candidate_discovery/readout_source.json \\",
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
                "# PlateSupport Tower Training Health Artifact Index",
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
                "# Stage 4 Results Summary",
                "",
                f"- status: `{aggregate_summary['status']}`",
                f"- claim status: `{aggregate_summary['claim_status']}`",
                f"- trained candidates: `{aggregate_summary['trained_candidate_count']}`",
                f"- trainable candidates: `{aggregate_summary['trainable_candidate_count']}`",
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
