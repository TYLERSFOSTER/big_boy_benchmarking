"""Tiny upstream smoke runner for artifact and readout-discipline validation."""

from __future__ import annotations

from datetime import UTC, datetime
from pathlib import Path
from typing import Any

from big_boy_benchmarking.artifacts.manifests import (
    DependencyManifest,
    EnvironmentFamilyManifest,
    ExternalArtifactsManifest,
    FamilyManifest,
    LinearizationManifest,
    MatrixManifest,
    ModeManifest,
    RunManifest,
)
from big_boy_benchmarking.artifacts.paths import (
    build_run_family_paths,
    build_run_paths,
)
from big_boy_benchmarking.artifacts.schemas import ARTIFACT_SCHEMA_VERSION
from big_boy_benchmarking.artifacts.writers import (
    append_csv_row,
    append_jsonl,
    ensure_artifact_dirs,
    write_csv,
    write_json,
)
from big_boy_benchmarking.metrics.events import EpisodeRow, RunIndexRow, WarningRow
from big_boy_benchmarking.metrics.timing import TimingRecorder, summarize_timing_segments
from big_boy_benchmarking.modes.registry import require_runnable_mode
from big_boy_benchmarking.runners.base import BenchmarkRunResult
from big_boy_benchmarking.seeds.bundles import SeedBundle, generate_seed_bundles
from big_boy_benchmarking.upstream.linearization import (
    REPORT_SOURCE,
    build_linearization_artifact_payload,
)
from big_boy_benchmarking.upstream.smoke_envs import (
    SmokeEnvironmentImportError,
    import_smoke_environment,
)
from big_boy_benchmarking.upstream.state_collapser import (
    STATE_COLLAPSER_DEPENDENCY_SPEC,
    collect_state_collapser_dependency_state,
)


def _now() -> str:
    return datetime.now(UTC).isoformat()


def _select_action(reset_info: dict[str, Any]) -> int:
    mask = reset_info.get("action_mask")
    if mask is not None:
        for index, allowed in enumerate(mask):
            if bool(allowed):
                return index
    return 0


def _artifact_path_dict(run_paths: Any) -> dict[str, str]:
    return {
        "run_manifest": str(run_paths.run_manifest),
        "seed_bundle": str(run_paths.seed_bundle),
        "mode_manifest": str(run_paths.mode_manifest),
        "linearization_manifest": str(run_paths.linearization_manifest),
        "timing_summary": str(run_paths.timing_summary),
        "episodes_csv": str(run_paths.episodes_csv),
        "timing_segments_csv": str(run_paths.timing_segments_csv),
        "warnings_jsonl": str(run_paths.warnings_jsonl),
        "external_artifacts": str(run_paths.external_artifacts),
    }


def run_upstream_smoke(
    *,
    smoke_id: str,
    artifact_root: Path | str,
    mode_id: str = "tower_empty_schema_tabular",
    linearization_mode_id: str = "tensor_available_disabled",
    run_family_id: str = "upstream_smoke_readout_discipline_v001",
    run_id: str | None = None,
    seed_bundle: SeedBundle | None = None,
    budget: dict[str, Any] | None = None,
    request_readout: bool | None = None,
) -> BenchmarkRunResult:
    """Run one tiny upstream smoke operation and write artifacts."""

    started_at = _now()
    run_id = run_id or f"{smoke_id}-{mode_id}-seed0"
    seed_bundle = seed_bundle or generate_seed_bundles(base_seed=0, replicate_count=1)[0]
    budget = budget or {"episodes": 1, "steps": 1}
    family_paths = build_run_family_paths(artifact_root, run_family_id)
    run_paths = build_run_paths(artifact_root, run_family_id, run_id)
    ensure_artifact_dirs(family_paths, run_paths)

    mode_contract = require_runnable_mode(mode_id)
    dependency_state = collect_state_collapser_dependency_state(
        dependency_spec=STATE_COLLAPSER_DEPENDENCY_SPEC,
    )
    warnings: list[WarningRow] = []

    try:
        imported = import_smoke_environment(smoke_id)
    except SmokeEnvironmentImportError as exc:
        warning = WarningRow(run_id=run_id, warning_code="missing_smoke_surface", message=str(exc))
        append_jsonl(run_paths.warnings_jsonl, warning.to_flat_dict(), create_parents=True)
        return BenchmarkRunResult(
            run_id=run_id,
            status="blocked",
            artifact_paths=_artifact_path_dict(run_paths),
            summary_path=None,
            warning_count=1,
            started_at=started_at,
            ended_at=_now(),
            failure_reason=str(exc),
        )

    readout_requested = (
        mode_contract.readout_policy.requested if request_readout is None else request_readout
    )
    morphism_requested = mode_contract.morphism_policy.requested
    uses_compatibility_readout = False
    uses_morphism = False
    recorder = TimingRecorder.create(run_id)

    write_json(
        family_paths.family_manifest,
        FamilyManifest(
            run_family_id=run_family_id,
            description="Upstream smoke harness validation family.",
        ).to_dict(),
        create_parents=True,
    )
    write_json(
        family_paths.matrix_manifest,
        MatrixManifest(
            matrix_id=f"{run_family_id}_matrix",
            run_family_id=run_family_id,
            environment_ids=(smoke_id,),
            mode_ids=(mode_id,),
            seed_bundle_ids=(seed_bundle.seed_bundle_id,),
        ).to_dict(),
        create_parents=True,
    )
    write_json(
        family_paths.environment_family_manifest,
        EnvironmentFamilyManifest(
            environment_family_id="upstream_smoke",
            environment_ids=(smoke_id,),
            description="Smoke environments imported from state_collapser.",
        ).to_dict(),
        create_parents=True,
    )
    write_json(
        family_paths.dependency_manifest,
        DependencyManifest(
            state_collapser=dependency_state.to_dict(),
            repo_state={
                "bbb_repo": "runtime_repository_root",
                "path_policy": "absolute local path omitted from portable artifact manifests",
            },
        ).to_dict(),
        create_parents=True,
    )
    write_json(run_paths.seed_bundle, seed_bundle.to_dict(), create_parents=True)

    env_runtime = imported.create_runtime()

    with recorder.segment("environment_reset"):
        reset_result = env_runtime.reset(seed=seed_bundle.environment_seed)
    action = _select_action(dict(reset_result.info))

    with recorder.segment("environment_step"):
        step_result = env_runtime.step(action)

    if readout_requested:
        with recorder.segment("compatibility_readout"):
            env_runtime.tower_runtime.compatibility_quotient_tiers()
        uses_compatibility_readout = True

    linearization_payload = build_linearization_artifact_payload(
        linearization_mode_id=linearization_mode_id,
        recorder=recorder,
        tower=getattr(env_runtime.tower_runtime, "partition_tower", None),
        metadata={
            "runner": "upstream_smoke",
            "smoke_id": smoke_id,
            "mode_id": mode_id,
        },
    )
    write_json(
        run_paths.linearization_manifest,
        LinearizationManifest(
            run_id=run_id,
            linearization_mode_id=linearization_mode_id,
            linearization_config=linearization_payload.config_dict,
            linearization_report=linearization_payload.report_dict,
            report_source=REPORT_SOURCE,
            conversion_records_exported=False,
        ).to_dict(),
        create_parents=True,
    )

    episode_row = EpisodeRow(
        run_id=run_id,
        episode_index=0,
        seed_bundle_id=seed_bundle.seed_bundle_id,
        total_reward=float(step_result.reward),
        step_count=1,
        terminated=bool(step_result.terminated),
        truncated=bool(step_result.truncated),
    )
    append_csv_row(
        run_paths.episodes_csv,
        episode_row.to_flat_dict(),
        EpisodeRow.fieldnames(),
        create_parents=True,
    )

    write_csv(
        run_paths.timing_segments_csv,
        [row.to_flat_dict() for row in recorder.rows],
        recorder.rows[0].fieldnames() if recorder.rows else (),
        create_parents=True,
    )
    write_json(
        run_paths.timing_summary,
        summarize_timing_segments(recorder.rows),
        create_parents=True,
    )

    mode_manifest = ModeManifest(
        mode_id=mode_id,
        readout_requested=readout_requested,
        morphism_requested=morphism_requested,
        uses_compatibility_readout=uses_compatibility_readout,
        uses_morphism=uses_morphism,
        mode_contract=mode_contract.to_dict(),
        linearization_mode_contract=linearization_payload.contract.to_dict(),
    )
    write_json(run_paths.mode_manifest, mode_manifest.to_dict(), create_parents=True)

    ended_at = _now()
    run_manifest = RunManifest(
        run_id=run_id,
        run_family_id=run_family_id,
        environment_id=smoke_id,
        mode_id=mode_id,
        linearization_mode_id=linearization_mode_id,
        linearization_benchmark_label=linearization_payload.report.benchmark_label,
        linearization_enabled=linearization_payload.report.enabled,
        schema_id=mode_contract.schema_mode,
        learner_id=mode_contract.learner_id,
        controller_id=mode_contract.controller_regime,
        seed_bundle_id=seed_bundle.seed_bundle_id,
        budget=budget,
        diagnostic_profile=mode_contract.diagnostic_profile.profile_id,
        timing_profile=mode_contract.timing_profile.profile_id,
        command="python -m big_boy_benchmarking.cli run-upstream-smoke",
        status="success",
    )
    write_json(run_paths.run_manifest, run_manifest.to_dict(), create_parents=True)
    write_json(
        run_paths.external_artifacts,
        ExternalArtifactsManifest(run_id=run_id).to_dict(),
        create_parents=True,
    )
    append_jsonl(
        family_paths.run_index,
        RunIndexRow(
            run_family_id=run_family_id,
            run_id=run_id,
            environment_id=smoke_id,
            mode_id=mode_id,
            status="success",
            started_at=started_at,
            ended_at=ended_at,
            artifact_schema_version=ARTIFACT_SCHEMA_VERSION,
        ).to_flat_dict(),
        create_parents=True,
    )
    if warnings:
        for warning in warnings:
            append_jsonl(run_paths.warnings_jsonl, warning.to_flat_dict(), create_parents=True)
    else:
        run_paths.warnings_jsonl.touch()

    summary = {
        "run_family_id": run_family_id,
        "run_id": run_id,
        "smoke_id": smoke_id,
        "mode_id": mode_id,
        "linearization_mode_id": linearization_mode_id,
        "linearization_benchmark_label": linearization_payload.report.benchmark_label,
        "status": "success",
        "readout_requested": readout_requested,
        "uses_compatibility_readout": uses_compatibility_readout,
        "artifact_schema_version": ARTIFACT_SCHEMA_VERSION,
    }
    write_json(family_paths.summary_json, summary, create_parents=True)

    return BenchmarkRunResult(
        run_id=run_id,
        status="success",
        artifact_paths=_artifact_path_dict(run_paths),
        summary_path=str(family_paths.summary_json),
        warning_count=len(warnings),
        started_at=started_at,
        ended_at=ended_at,
        failure_reason=None,
    )


def summarize_upstream_smoke(artifact_root: Path | str, run_family_id: str) -> dict[str, Any]:
    summary_path = build_run_family_paths(artifact_root, run_family_id).summary_json
    if not summary_path.exists():
        raise FileNotFoundError(f"missing smoke summary: {summary_path}")
    import json

    return json.loads(summary_path.read_text(encoding="utf-8"))
