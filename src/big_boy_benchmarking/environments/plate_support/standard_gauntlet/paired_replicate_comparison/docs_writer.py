"""Human-doc seed writer for PlateSupport gauntlet Stage 6."""

from __future__ import annotations

from pathlib import Path


def write_paired_replicate_comparison_docs(
    *,
    readout_surface: Path,
    artifact_root: Path,
    stage_root: Path,
    aggregate_summary: dict[str, object],
    claim_row: dict[str, object],
    target: dict[str, object],
    readout_source_path: Path,
    output_paths: dict[str, str],
) -> dict[str, str]:
    """Write Stage 6 seed docs and artifact index."""

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
                "# PlateSupport Paired Replicate Comparison",
                "",
                "## Status",
                "",
                f"Status: {aggregate_summary['status']}.",
                "",
                str(claim_row.get("bounded_claim", "")),
                "",
                f"- Claim status: `{claim_row.get('claim_status', '')}`",
                f"- Mean target-hit delta: `{claim_row.get('mean_target_hit_rate_delta', '')}`",
                f"- Target policy: `{target.get('target_policy_id', '')}`",
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
                "# PlateSupport Paired Replicate Comparison Method",
                "",
                "Stage 6 consumes the Stage 3 selected candidate, Stage 4",
                "training-health validation, and Stage 5 calibrated target. It trains",
                "a direct concrete baseline and the selected tower candidate on matched",
                "replicate seed bundles, then compares target-hit rates only within",
                "complete pairs.",
                "",
                "The no-contraction tower control is recorded as unavailable unless a",
                "separate approved runtime adapter exists. It is not silently simulated.",
                "",
                "Comparison arms preserve selected-candidate schema metadata, so an",
                "iterated source-local ratio candidate remains identifiable in arm",
                "manifests, aggregate tables, and human readouts.",
                "",
                "The output is bounded smoke comparison evidence, not a general tower",
                "superiority claim.",
                "",
            ]
        ),
        encoding="utf-8",
    )
    runbook.write_text(
        "\n".join(
            [
                "# PlateSupport Paired Replicate Comparison Runbook",
                "",
                "Run Stage 6 with:",
                "",
                "```text",
                "uv run python -m big_boy_benchmarking.cli plate-support "
                "standard-gauntlet paired-comparison run \\",
                "  --repo-root /Users/foster/big_boy_benchmarking \\",
                "  --artifact-root docs/evaluations/plate_support_5x5_default_v001/"
                "standard_gauntlet/artifacts/smoke_001 \\",
                "  --candidate-source docs/evaluations/plate_support_5x5_default_v001/"
                "standard_gauntlet/candidate_discovery/readout_source.json \\",
                "  --training-health-source docs/evaluations/plate_support_5x5_default_v001/"
                "standard_gauntlet/tower_training_health/readout_source.json \\",
                "  --threshold-source docs/evaluations/plate_support_5x5_default_v001/"
                "standard_gauntlet/threshold_frontier_calibration/readout_source.json \\",
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
                "# PlateSupport Paired Replicate Comparison Artifact Index",
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
                "# Stage 6 Results Summary",
                "",
                f"- status: `{aggregate_summary['status']}`",
                f"- claim status: `{claim_row.get('claim_status', '')}`",
                f"- complete pairs: `{claim_row.get('complete_pair_count', '')}`",
                f"- mean target-hit delta: `{claim_row.get('mean_target_hit_rate_delta', '')}`",
                "- claim boundary: `bounded paired smoke comparison`",
                f"- bounded claim: {claim_row.get('bounded_claim', '')}",
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
