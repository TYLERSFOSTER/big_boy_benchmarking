"""PlateSupport environment-readiness runner."""

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
from big_boy_benchmarking.artifacts.paths import build_run_family_paths, build_run_paths
from big_boy_benchmarking.artifacts.schemas import ARTIFACT_SCHEMA_VERSION
from big_boy_benchmarking.artifacts.writers import (
    append_jsonl,
    ensure_artifact_dirs,
    write_csv,
    write_json,
)
from big_boy_benchmarking.environments.plate_support.actions import (
    ACTION_RECORDS,
    action_table_rows,
)
from big_boy_benchmarking.environments.plate_support.diagnostics import (
    collect_plate_support_structural_diagnostics,
)
from big_boy_benchmarking.environments.plate_support.docs_writer import (
    write_artifact_index,
    write_plate_support_environment_docs,
)
from big_boy_benchmarking.environments.plate_support.ids import (
    DEFAULT_INSTANCE_ID,
    DEFAULT_SCHEMA_ID,
    ENVIRONMENT_FAMILY_ID,
    READINESS_RUN_FAMILY_ID,
)
from big_boy_benchmarking.environments.plate_support.manifests import (
    instance_manifest_payload,
    readout_source_payload,
    schema_probe_manifest_payload,
)
from big_boy_benchmarking.environments.plate_support.paths import (
    default_environment_doc_path,
    validate_no_evaluation_path,
)
from big_boy_benchmarking.environments.plate_support.tower_probe import (
    run_plate_support_tower_probe,
)
from big_boy_benchmarking.environments.plate_support.types import (
    RandomPolicyReconRecord,
    ShortestPathRecord,
    StateRecord,
    TowerProbeRecord,
    TransitionRecord,
)
from big_boy_benchmarking.environments.plate_support.upstream import (
    PlateSupportSurfaceImportError,
    import_plate_support_surface,
)
from big_boy_benchmarking.metrics.events import (
    BootstrapIntervalRow,
    ControlEventRow,
    EpisodeRow,
    RunIndexRow,
    StepEventRow,
    StructuralDiagnosticRow,
    WarningRow,
)
from big_boy_benchmarking.metrics.timing import TimingRecorder, summarize_timing_segments
from big_boy_benchmarking.modes.registry import require_runnable_mode
from big_boy_benchmarking.runners.base import BenchmarkRunResult
from big_boy_benchmarking.seeds.bundles import SeedBundle, generate_seed_bundles
from big_boy_benchmarking.upstream.linearization import (
    REPORT_SOURCE,
    build_linearization_artifact_payload,
)
from big_boy_benchmarking.upstream.state_collapser import (
    STATE_COLLAPSER_DEPENDENCY_SPEC,
    collect_state_collapser_dependency_state,
)

DEFAULT_MODE_ID = "tower_nonempty_schema_tabular"


def _now() -> str:
    return datetime.now(UTC).isoformat()


def run_plate_support_environment_readiness(
    *,
    artifact_root: Path | str,
    instance_id: str = DEFAULT_INSTANCE_ID,
    mode_id: str = DEFAULT_MODE_ID,
    linearization_mode_id: str = "tensor_available_disabled",
    run_id: str | None = None,
    seed_bundle: SeedBundle | None = None,
    random_policy_episodes: int = 1000,
    random_policy_seed: int = 0,
    tower_probe_steps: int = 20,
    tower_probe_sample_size: int = 20,
    docs_path: Path | str | None = None,
    command_line: str | None = None,
) -> BenchmarkRunResult:
    """Run the PlateSupport environment-readiness diagnostic and write artifacts."""

    if instance_id != DEFAULT_INSTANCE_ID:
        raise ValueError(f"unsupported PlateSupport instance id: {instance_id}")

    started_at = _now()
    artifact_root = validate_no_evaluation_path(artifact_root)
    run_id = run_id or f"{instance_id}-readiness-seed{random_policy_seed}"
    seed_bundle = seed_bundle or generate_seed_bundles(
        base_seed=random_policy_seed,
        replicate_count=1,
    )[0]
    family_paths = build_run_family_paths(artifact_root, READINESS_RUN_FAMILY_ID)
    run_paths = build_run_paths(artifact_root, READINESS_RUN_FAMILY_ID, run_id)
    ensure_artifact_dirs(family_paths, run_paths)
    results_dir = run_paths.root / "results"
    results_dir.mkdir(parents=True, exist_ok=True)

    artifact_index_path = artifact_root / "artifact_index.md"
    readout_source_path = artifact_root / "readout_source.json"
    docs_target = Path(docs_path) if docs_path is not None else default_environment_doc_path()
    command_line = command_line or (
        "uv run python -m big_boy_benchmarking.cli plate-support readiness "
        "--artifact-root docs/environments/plate_support_5x5_default_v001/readiness/dev_001"
    )

    recorder = TimingRecorder.create(run_id)
    warnings: list[WarningRow] = []
    try:
        surface = import_plate_support_surface()
    except PlateSupportSurfaceImportError as exc:
        warning = WarningRow(
            run_id=run_id,
            warning_code="missing_plate_support_surface",
            message=str(exc),
        )
        append_jsonl(run_paths.warnings_jsonl, warning.to_flat_dict(), create_parents=True)
        return BenchmarkRunResult(
            run_id=run_id,
            status="blocked",
            artifact_paths={"warnings_jsonl": str(run_paths.warnings_jsonl)},
            summary_path=None,
            warning_count=1,
            started_at=started_at,
            ended_at=_now(),
            failure_reason=str(exc),
        )

    dependency_state = collect_state_collapser_dependency_state(
        dependency_spec=STATE_COLLAPSER_DEPENDENCY_SPEC,
    )
    mode_contract = require_runnable_mode(mode_id)

    with recorder.segment("posthoc_diagnostics"):
        tower_probe_records = run_plate_support_tower_probe(
            steps=tower_probe_steps,
            seed=seed_bundle.diagnostic_sampling_seed,
            sample_size=tower_probe_sample_size,
        )
        diagnostics = collect_plate_support_structural_diagnostics(
            surface=surface,
            random_policy_episodes=random_policy_episodes,
            random_policy_seed=random_policy_seed,
            tower_probe_records=tower_probe_records,
        )

    with recorder.segment("environment_reset"):
        runtime = surface.create_runtime(schema=surface.default_plate_support_schema())
        runtime.reset(seed=seed_bundle.environment_seed)

    uses_compatibility_readout = False
    readout_requested = mode_contract.readout_policy.requested
    if readout_requested:
        with recorder.segment("compatibility_readout"):
            runtime.tower_runtime.compatibility_quotient_tiers()
        uses_compatibility_readout = True

    linearization_payload = build_linearization_artifact_payload(
        linearization_mode_id=linearization_mode_id,
        recorder=recorder,
        tower=getattr(runtime.tower_runtime, "partition_tower", None),
        max_action_count=surface.ACTION_COUNT,
        metadata={
            "runner": "plate_support_environment_readiness",
            "environment_family_id": ENVIRONMENT_FAMILY_ID,
            "environment_instance_id": instance_id,
            "mode_id": mode_id,
        },
    )

    artifact_paths = _write_artifacts(
        artifact_root=artifact_root,
        artifact_index_path=artifact_index_path,
        readout_source_path=readout_source_path,
        docs_target=docs_target,
        family_paths=family_paths,
        run_paths=run_paths,
        results_dir=results_dir,
        run_id=run_id,
        seed_bundle=seed_bundle,
        diagnostics=diagnostics,
        dependency_state=dependency_state,
        mode_contract=mode_contract,
        linearization_payload=linearization_payload,
        linearization_mode_id=linearization_mode_id,
        uses_compatibility_readout=uses_compatibility_readout,
        readout_requested=readout_requested,
        recorder=recorder,
        started_at=started_at,
        command_line=command_line,
    )
    ended_at = _now()
    append_jsonl(
        family_paths.run_index,
        RunIndexRow(
            run_family_id=READINESS_RUN_FAMILY_ID,
            run_id=run_id,
            environment_id=instance_id,
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

    return BenchmarkRunResult(
        run_id=run_id,
        status="success",
        artifact_paths=artifact_paths,
        summary_path=str(family_paths.summary_json),
        warning_count=len(warnings),
        started_at=started_at,
        ended_at=ended_at,
        failure_reason=None,
    )


def _write_artifacts(
    *,
    artifact_root: Path,
    artifact_index_path: Path,
    readout_source_path: Path,
    docs_target: Path,
    family_paths: Any,
    run_paths: Any,
    results_dir: Path,
    run_id: str,
    seed_bundle: SeedBundle,
    diagnostics: Any,
    dependency_state: Any,
    mode_contract: Any,
    linearization_payload: Any,
    linearization_mode_id: str,
    uses_compatibility_readout: bool,
    readout_requested: bool,
    recorder: TimingRecorder,
    started_at: str,
    command_line: str,
) -> dict[str, str]:
    graph_summary = diagnostics.graph.graph_summary
    random_policy = diagnostics.random_policy_recon.to_dict()
    tower_rows = [record.to_dict() for record in diagnostics.tower_probe_records]
    summary = {
        "status": "success",
        "started_at": started_at,
        "run_family_id": READINESS_RUN_FAMILY_ID,
        "run_id": run_id,
        "environment_family_id": ENVIRONMENT_FAMILY_ID,
        "environment_instance_id": DEFAULT_INSTANCE_ID,
        "graph_summary": graph_summary,
        "random_policy_recon": random_policy,
        "tower_probe": tower_rows,
        "training_surface_availability": diagnostics.training_surface_availability,
        "artifact_schema_version": ARTIFACT_SCHEMA_VERSION,
    }

    write_json(
        family_paths.family_manifest,
        FamilyManifest(
            run_family_id=READINESS_RUN_FAMILY_ID,
            description="PlateSupport environment-readiness diagnostics.",
        ).to_dict(),
        create_parents=True,
    )
    write_json(
        family_paths.matrix_manifest,
        MatrixManifest(
            matrix_id=f"{READINESS_RUN_FAMILY_ID}_matrix",
            run_family_id=READINESS_RUN_FAMILY_ID,
            environment_ids=(DEFAULT_INSTANCE_ID,),
            mode_ids=(mode_contract.mode_id,),
            seed_bundle_ids=(seed_bundle.seed_bundle_id,),
        ).to_dict(),
        create_parents=True,
    )
    write_json(
        family_paths.environment_family_manifest,
        EnvironmentFamilyManifest(
            environment_family_id=ENVIRONMENT_FAMILY_ID,
            environment_ids=(DEFAULT_INSTANCE_ID,),
            description="Constrained robotics-style upstream PlateSupport environment.",
        ).to_dict(),
        create_parents=True,
    )
    write_json(
        family_paths.dependency_manifest,
        DependencyManifest(
            state_collapser=dependency_state.to_dict(),
            repo_state={"bbb_repo": str(Path(__file__).resolve().parents[4])},
        ).to_dict(),
        create_parents=True,
    )
    write_json(family_paths.summary_json, summary, create_parents=True)
    write_csv(
        family_paths.summary_csv,
        [
            {
                "status": "success",
                "environment_instance_id": DEFAULT_INSTANCE_ID,
                "candidate_state_count": graph_summary["candidate_state_count"],
                "valid_state_count": graph_summary["valid_state_count"],
                "reachable_state_count": graph_summary["reachable_state_count"],
                "shortest_path_length": graph_summary["shortest_path_length"],
                "default_schema_max_depth": _tower_depth(tower_rows, DEFAULT_SCHEMA_ID),
            }
        ],
        (
            "status",
            "environment_instance_id",
            "candidate_state_count",
            "valid_state_count",
            "reachable_state_count",
            "shortest_path_length",
            "default_schema_max_depth",
        ),
        create_parents=True,
    )
    write_csv(
        family_paths.bootstrap_intervals_csv,
        [],
        BootstrapIntervalRow.fieldnames(),
        create_parents=True,
    )

    write_json(
        run_paths.run_manifest,
        RunManifest(
            run_id=run_id,
            run_family_id=READINESS_RUN_FAMILY_ID,
            environment_id=DEFAULT_INSTANCE_ID,
            mode_id=mode_contract.mode_id,
            linearization_mode_id=linearization_mode_id,
            linearization_benchmark_label=linearization_payload.report.benchmark_label,
            linearization_enabled=linearization_payload.report.enabled,
            schema_id=DEFAULT_SCHEMA_ID,
            learner_id=mode_contract.learner_id,
            controller_id=mode_contract.controller_regime,
            seed_bundle_id=seed_bundle.seed_bundle_id,
            budget={
                "random_policy_episodes": random_policy["episode_count"],
                "tower_probe_steps": tower_rows[0]["steps"] if tower_rows else 0,
                "tower_probe_sample_size": tower_rows[0]["sample_size"] if tower_rows else 0,
            },
            diagnostic_profile="environment_readiness",
            timing_profile=mode_contract.timing_profile.profile_id,
            command=command_line,
            status="success",
        ).to_dict(),
        create_parents=True,
    )
    write_json(run_paths.seed_bundle, seed_bundle.to_dict(), create_parents=True)
    write_json(
        run_paths.mode_manifest,
        ModeManifest(
            mode_id=mode_contract.mode_id,
            readout_requested=readout_requested,
            morphism_requested=mode_contract.morphism_policy.requested,
            uses_compatibility_readout=uses_compatibility_readout,
            uses_morphism=False,
            mode_contract=mode_contract.to_dict(),
            linearization_mode_contract=linearization_payload.contract.to_dict(),
        ).to_dict(),
        create_parents=True,
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
    write_json(
        run_paths.external_artifacts,
        ExternalArtifactsManifest(run_id=run_id).to_dict(),
        create_parents=True,
    )
    write_csv(
        run_paths.episodes_csv,
        [
            EpisodeRow(
                run_id=run_id,
                episode_index=0,
                seed_bundle_id=seed_bundle.seed_bundle_id,
                total_reward=0.0,
                step_count=0,
                terminated=False,
                truncated=False,
            ).to_flat_dict()
        ],
        EpisodeRow.fieldnames(),
        create_parents=True,
    )
    write_csv(run_paths.step_events_csv, [], StepEventRow.fieldnames(), create_parents=True)
    write_csv(run_paths.control_events_csv, [], ControlEventRow.fieldnames(), create_parents=True)
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
    _write_structural_jsonl(run_paths.structural_diagnostics_jsonl, run_id, diagnostics)

    machine_paths = _write_machine_tables(
        run_paths=run_paths,
        results_dir=results_dir,
        diagnostics=diagnostics,
    )
    write_json(
        run_paths.root / "instance_summary.json",
        instance_manifest_payload(graph_summary=graph_summary),
        create_parents=True,
    )
    write_json(
        run_paths.root / "schema_probe_manifest.json",
        schema_probe_manifest_payload(),
        create_parents=True,
    )
    docs_written = write_plate_support_environment_docs(
        docs_path=docs_target,
        artifact_root=artifact_root,
        summary=summary,
        artifact_index_path=artifact_index_path,
        readout_source_path=readout_source_path,
        command_line=command_line,
    )
    artifact_paths = {
        "family_manifest": str(family_paths.family_manifest),
        "matrix_manifest": str(family_paths.matrix_manifest),
        "environment_family_manifest": str(family_paths.environment_family_manifest),
        "dependency_manifest": str(family_paths.dependency_manifest),
        "run_manifest": str(run_paths.run_manifest),
        "seed_bundle": str(run_paths.seed_bundle),
        "mode_manifest": str(run_paths.mode_manifest),
        "linearization_manifest": str(run_paths.linearization_manifest),
        "timing_summary": str(run_paths.timing_summary),
        "episodes_csv": str(run_paths.episodes_csv),
        "step_events_csv": str(run_paths.step_events_csv),
        "control_events_csv": str(run_paths.control_events_csv),
        "timing_segments_csv": str(run_paths.timing_segments_csv),
        "warnings_jsonl": str(run_paths.warnings_jsonl),
        "external_artifacts": str(run_paths.external_artifacts),
        "summary_json": str(family_paths.summary_json),
        "summary_csv": str(family_paths.summary_csv),
        "bootstrap_intervals_csv": str(family_paths.bootstrap_intervals_csv),
        "instance_summary": str(run_paths.root / "instance_summary.json"),
        "schema_probe_manifest": str(run_paths.root / "schema_probe_manifest.json"),
        "environment_doc": str(docs_written),
        "readout_source": str(readout_source_path),
        "artifact_index": str(artifact_index_path),
    }
    artifact_paths.update(machine_paths)
    write_artifact_index(artifact_index_path=artifact_index_path, artifact_paths=artifact_paths)
    write_json(
        readout_source_path,
        readout_source_payload(
            artifact_root=artifact_root,
            environment_doc=docs_written,
            run_family_summary=family_paths.summary_json,
            artifact_index=artifact_index_path,
            run_id=run_id,
        ),
        create_parents=True,
    )
    return artifact_paths


def _write_machine_tables(*, run_paths: Any, results_dir: Path, diagnostics: Any) -> dict[str, str]:
    paths = {
        "graph_summary": run_paths.root / "graph_summary.json",
        "state_summary": results_dir / "state_summary.csv",
        "action_table": results_dir / "action_table.csv",
        "transition_summary": results_dir / "transition_summary.csv",
        "shortest_path": results_dir / "shortest_path.csv",
        "validity_predicate_summary": results_dir / "validity_predicate_summary.csv",
        "support_pattern_summary": results_dir / "support_pattern_summary.csv",
        "reachability_pattern_summary": results_dir / "reachability_pattern_summary.csv",
        "orientation_summary": results_dir / "orientation_summary.csv",
        "position_summary": results_dir / "position_summary.csv",
        "outgoing_action_count_summary": results_dir / "outgoing_action_count_summary.csv",
        "invalid_action_summary": results_dir / "invalid_action_summary.csv",
        "self_transition_summary": results_dir / "self_transition_summary.csv",
        "tower_probe_summary": results_dir / "tower_probe_summary.csv",
        "random_policy_recon_summary": results_dir / "random_policy_recon_summary.csv",
        "training_surface_availability": run_paths.root / "training_surface_availability.json",
    }
    write_json(paths["graph_summary"], diagnostics.graph.graph_summary, create_parents=True)
    write_csv(
        paths["state_summary"],
        [record.to_dict() for record in diagnostics.state_records],
        StateRecord.fieldnames(),
        create_parents=True,
    )
    write_csv(
        paths["action_table"],
        action_table_rows(),
        ACTION_RECORDS[0].fieldnames(),
        create_parents=True,
    )
    write_csv(
        paths["transition_summary"],
        [record.to_dict() for record in diagnostics.graph.transition_records],
        TransitionRecord.fieldnames(),
        create_parents=True,
    )
    write_csv(
        paths["shortest_path"],
        [record.to_dict() for record in diagnostics.graph.shortest_path_records],
        ShortestPathRecord.fieldnames(),
        create_parents=True,
    )
    write_csv(
        paths["validity_predicate_summary"],
        diagnostics.validity_predicate_summary,
        (
            "predicate_name",
            "valid_state_true_count",
            "valid_state_false_count",
            "ambient_true_count",
            "ambient_false_count",
            "interpretation",
        ),
        create_parents=True,
    )
    write_csv(
        paths["support_pattern_summary"],
        diagnostics.support_pattern_summary,
        ("support_pattern", "valid_state_count", "share"),
        create_parents=True,
    )
    write_csv(
        paths["reachability_pattern_summary"],
        diagnostics.reachability_pattern_summary,
        ("reachability_pattern", "valid_state_count", "share"),
        create_parents=True,
    )
    write_csv(
        paths["orientation_summary"],
        diagnostics.orientation_summary,
        ("theta_idx", "valid_state_count", "share"),
        create_parents=True,
    )
    write_csv(
        paths["position_summary"],
        diagnostics.position_summary,
        ("x_idx", "y_idx", "valid_state_count", "share"),
        create_parents=True,
    )
    write_csv(
        paths["outgoing_action_count_summary"],
        diagnostics.graph.outgoing_action_count_summary,
        ("count_value", "state_count", "share"),
        create_parents=True,
    )
    write_csv(
        paths["invalid_action_summary"],
        diagnostics.graph.invalid_action_summary,
        ("count_value", "state_count", "share"),
        create_parents=True,
    )
    write_csv(
        paths["self_transition_summary"],
        diagnostics.graph.self_transition_summary,
        (
            "valid_self_transition_count",
            "invalid_self_loop_count",
            "total_self_transition_count",
            "state_count",
            "share",
        ),
        create_parents=True,
    )
    write_csv(
        paths["tower_probe_summary"],
        [record.to_dict() for record in diagnostics.tower_probe_records],
        TowerProbeRecord.fieldnames(),
        create_parents=True,
    )
    write_csv(
        paths["random_policy_recon_summary"],
        [diagnostics.random_policy_recon.to_dict()],
        RandomPolicyReconRecord.fieldnames(),
        create_parents=True,
    )
    write_json(
        paths["training_surface_availability"],
        diagnostics.training_surface_availability,
        create_parents=True,
    )
    return {key: str(path) for key, path in paths.items()}


def _write_structural_jsonl(path: Path, run_id: str, diagnostics: Any) -> None:
    rows = (
        StructuralDiagnosticRow(
            run_id=run_id,
            diagnostic_name="valid_state_count",
            lifecycle="posthoc",
            exact_or_sampled="exact",
            readout_backed=False,
            tier_index=None,
            schema_id=None,
            value=str(diagnostics.graph.graph_summary["valid_state_count"]),
        ),
        StructuralDiagnosticRow(
            run_id=run_id,
            diagnostic_name="shortest_path_length",
            lifecycle="posthoc",
            exact_or_sampled="exact",
            readout_backed=False,
            tier_index=None,
            schema_id=None,
            value=str(diagnostics.graph.graph_summary["shortest_path_length"]),
        ),
        StructuralDiagnosticRow(
            run_id=run_id,
            diagnostic_name="default_tower_max_depth",
            lifecycle="posthoc",
            exact_or_sampled="sampled",
            readout_backed=True,
            tier_index=None,
            schema_id=DEFAULT_SCHEMA_ID,
            value=str(
                _tower_depth(
                    [row.to_dict() for row in diagnostics.tower_probe_records],
                    DEFAULT_SCHEMA_ID,
                )
            ),
        ),
    )
    for row in rows:
        append_jsonl(path, row.to_flat_dict(), create_parents=True)


def _tower_depth(tower_rows: list[dict[str, Any]], schema_id: str) -> int | None:
    for row in tower_rows:
        if row.get("schema_id") == schema_id:
            return int(row.get("max_depth", 0))
    return None
