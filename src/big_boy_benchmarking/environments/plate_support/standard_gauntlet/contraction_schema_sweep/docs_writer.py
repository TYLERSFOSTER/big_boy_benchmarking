"""Human-doc seed writer for Stage 2 schema sweep."""

from __future__ import annotations

from pathlib import Path


def write_schema_sweep_docs(
    *,
    readout_surface: Path,
    artifact_root: Path,
    stage_root: Path,
    aggregate_summary: dict[str, object],
    readout_source_path: Path,
    output_paths: dict[str, str],
) -> dict[str, str]:
    """Write Stage 2 seed docs and artifact index."""

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
                "# PlateSupport Contraction Schema Sweep",
                "",
                "## Status",
                "",
                f"Status: {aggregate_summary['status']}.",
                "",
                "This stage records structural schema diagnostics and candidate signals.",
                "It does not select final candidates and does not claim training benefit.",
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
                "# PlateSupport Contraction Schema Sweep Method",
                "",
                "The sweep consumes Stage 1 structural diagnostics, runs the mandatory",
                "no-contraction and upstream-default schema modes, runs BBB-owned",
                "source-local outgoing-edge ratio schemas on the exact PlateSupport",
                "graph, and emits explicit unsupported rows for custom schema families",
                "that the current upstream PlateSupport probe cannot represent honestly.",
                "",
                "Source-local ratio schemas use catch semantics: every source with",
                "at least one valid non-self outgoing edge contributes",
                "`max(1, ceil(out_degree * numerator / denominator))` selected",
                "edges to the contraction block.",
                "",
                "Iterated source-local ratio schemas are optional correction-run",
                "arms. They repeatedly select stable quotient-representative",
                "source-local edges, one block per iteration, and record plan, stop,",
                "and many-tier candidate-signal tables. They do not use the one-shot",
                "catch rule and they allow zero selected edges in a source component.",
                "",
            ]
        ),
        encoding="utf-8",
    )
    runbook.write_text(
        "\n".join(
            [
                "# PlateSupport Contraction Schema Sweep Runbook",
                "",
                "Run Stage 2 with:",
                "",
                "```text",
                "uv run python -m big_boy_benchmarking.cli plate-support standard-gauntlet schema-sweep run \\",
                "  --repo-root /Users/foster/big_boy_benchmarking \\",
                "  --artifact-root docs/evaluations/plate_support_5x5_default_v001/standard_gauntlet/artifacts/smoke_001 \\",
                "  --stage1-source docs/evaluations/plate_support_5x5_default_v001/standard_gauntlet/structural_and_tower_diagnostics/readout_source.json \\",
                "  --source-local-ratio-numerator 1 \\",
                "  --source-local-ratio-denominator 18 \\",
                "  --run-label smoke_001 \\",
                "  --locked-by foster",
                "```",
                "",
                "For an iterated correction run, add:",
                "",
                "```text",
                "  --include-iterated-source-local-ratio \\",
                "  --iterated-source-local-ratio-denominator 144 \\",
                "  --iterated-source-local-ratio-denominator 72 \\",
                "  --iterated-source-local-ratio-denominator 36 \\",
                "  --iterated-source-local-ratio-denominator 18 \\",
                "  --iterated-source-local-max-iterations 32",
                "```",
                "",
            ]
        ),
        encoding="utf-8",
    )
    artifact_index.write_text(
        "\n".join(
            [
                "# PlateSupport Contraction Schema Sweep Artifact Index",
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
                "# Stage 2 Results Summary",
                "",
                f"- status: `{aggregate_summary['status']}`",
                f"- claim status: `{aggregate_summary['claim_status']}`",
                f"- schema arm count: `{aggregate_summary['schema_arm_count']}`",
                f"- eligible signal count: `{aggregate_summary['eligible_signal_count']}`",
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
