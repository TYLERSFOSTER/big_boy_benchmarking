"""Human-doc seed writer for PlateSupport gauntlet Stage 5."""

from __future__ import annotations

from pathlib import Path


def write_threshold_frontier_calibration_docs(
    *,
    readout_surface: Path,
    artifact_root: Path,
    stage_root: Path,
    aggregate_summary: dict[str, object],
    recommended_target: dict[str, object],
    readout_source_path: Path,
    output_paths: dict[str, str],
) -> dict[str, str]:
    """Write Stage 5 seed docs and artifact index."""

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
                "# PlateSupport Threshold Frontier Calibration",
                "",
                "## Status",
                "",
                f"Status: {aggregate_summary['status']}.",
                "",
                "This stage calibrates the target policy for the next paired comparison.",
                "It consumes Stage 1 reward/structure facts and Stage 4 training traces.",
                "It does not claim that any tower policy beats a flat baseline.",
                "",
                f"- Recommended target: `{recommended_target.get('target_policy_id', '')}`",
                f"- Target type: `{recommended_target.get('target_type', '')}`",
                f"- Calibration status: `{recommended_target.get('calibration_status', '')}`",
                f"- Stage artifact root: `{stage_root}`",
                f"- Suite artifact root: `{artifact_root}`",
                f"- Readout source: `{readout_source_path}`",
                "",
                "## Clarifying Turns",
                "",
                "### Evaluator Turn 1",
                "",
                "_Add evaluator question or concern here._",
                "",
                "### Codex Turn 1",
                "",
                "_Add Codex response here._",
                "",
            ]
        ),
        encoding="utf-8",
    )
    method.write_text(
        "\n".join(
            [
                "# PlateSupport Threshold Frontier Calibration Method",
                "",
                "Stage 5 reuses the validated Stage 4 tower-training-health traces,",
                "summarizes binary goal success, first-hit timing, sustained-window",
                "feasibility, and observed return distributions, then builds return",
                "threshold candidates from observed quantiles, the success/miss boundary,",
                "Stage 1 random-policy reward context, and the Stage 1 shortest-path",
                "reward anchor.",
                "",
                "Calibration arms preserve selected-candidate schema metadata,",
                "including whether the Stage 4 trace came from the iterated",
                "source-local ratio correction path. Calibration does not rebuild the",
                "schema, but it must keep this identity visible for Stage 6 and human",
                "readouts.",
                "",
                "The recommended target is selected for Stage 6 only. This stage is",
                "calibration evidence, not comparison evidence.",
                "",
            ]
        ),
        encoding="utf-8",
    )
    runbook.write_text(
        "\n".join(
            [
                "# PlateSupport Threshold Frontier Calibration Runbook",
                "",
                "Run Stage 5 with:",
                "",
                "```text",
                "uv run python -m big_boy_benchmarking.cli plate-support "
                "standard-gauntlet threshold-calibration run \\",
                "  --repo-root /Users/foster/big_boy_benchmarking \\",
                "  --artifact-root docs/evaluations/plate_support_5x5_default_v001/"
                "standard_gauntlet/artifacts/smoke_001 \\",
                "  --training-health-source docs/evaluations/plate_support_5x5_default_v001/"
                "standard_gauntlet/tower_training_health/readout_source.json \\",
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
                "# PlateSupport Threshold Frontier Calibration Artifact Index",
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
                "# Stage 5 Results Summary",
                "",
                f"- status: `{aggregate_summary['status']}`",
                f"- claim status: `{aggregate_summary['claim_status']}`",
                f"- recommended target: `{recommended_target.get('target_policy_id', '')}`",
                f"- target type: `{recommended_target.get('target_type', '')}`",
                "- claim boundary: `threshold calibration only; no paired comparison claim`",
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
