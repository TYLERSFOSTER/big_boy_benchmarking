"""Runner for the counterpoint small paired replicate probe."""

from __future__ import annotations

from pathlib import Path
from typing import Any

from big_boy_benchmarking.artifacts.writers import write_csv, write_json
from big_boy_benchmarking.environments.counterpoint.liftability import (
    STATE_COLLAPSER_V072_POINTWISE_LIFTABILITY_SEMANTICS_ID,
)
from big_boy_benchmarking.environments.counterpoint.second_serious_comparison.config import (
    DEFAULT_LINEARIZATION_MODE_ID,
    DEFAULT_TIER_JUMP_POLICY_ID,
)
from big_boy_benchmarking.environments.counterpoint.second_serious_comparison.events import (
    ComparisonRunIndexRow,
)
from big_boy_benchmarking.environments.counterpoint.second_serious_comparison.runner import (
    ComparisonRunRecord,
    _run_index_row,
    _schema0_runtime_candidate,
    _schema1_runtime_candidate,
    comparison_spec_for_instance,
    run_schema_condition,
)
from big_boy_benchmarking.environments.counterpoint.second_serious_comparison.thresholds import (
    ThresholdPolicy,
    TierJumpPolicy,
)
from big_boy_benchmarking.seeds.bundles import generate_seed_bundles

from .candidate_source import load_paired_replicate_candidates
from .config import (
    EVALUATION_ID,
    EVALUATION_RUN_FAMILY_ID,
    SELECTED_THRESHOLD_RUN_MODE_ID,
    SMOKE_RUN_MODE_ID,
    SmallPairedReplicateProbeBudget,
)
from .manifests import (
    budget_lock_payload,
    candidate_manifest_payload,
    evaluation_arm_manifest_payload,
    evaluation_manifest_payload,
    parent_source_manifest_payload,
    replicate_probe_policy_payload,
    threshold_policy_payload,
    tier_jump_policy_payload,
)
from .paths import (
    build_small_paired_replicate_probe_paths,
    default_candidate_readout_source,
    validate_repo_resident_artifact_root,
)
from .threshold_source import ResolvedThreshold, resolve_threshold


def run_small_paired_replicate_probe(
    *,
    artifact_root: Path | str,
    candidate_readout_source: Path | str | None = None,
    threshold_value: float | None = None,
    threshold_frontier_readout_source: Path | str | None = None,
    instance_id: str = "wide_span18",
    candidate_cap: int = 1,
    target_candidate_ids: tuple[str, ...] = (),
    training_replicates_per_arm: int = 8,
    episodes_per_replicate: int = 16,
    base_seed: int = 0,
    locked_by: str = "cli",
    run_mode: str | None = None,
    horizon_override: int | None = None,
    controller_event_ceiling: int | None = None,
    linearization_mode_id: str = DEFAULT_LINEARIZATION_MODE_ID,
) -> dict[str, Any]:
    _require_state_collapser_072()
    artifact_root = validate_repo_resident_artifact_root(artifact_root)
    spec = comparison_spec_for_instance(instance_id)
    candidate_source = candidate_readout_source or default_candidate_readout_source()
    selected_run_mode = (
        run_mode
        if run_mode is not None
        else (
            SELECTED_THRESHOLD_RUN_MODE_ID
            if threshold_frontier_readout_source is not None and threshold_value is None
            else SMOKE_RUN_MODE_ID
        )
    )
    budget = SmallPairedReplicateProbeBudget(
        environment_instance_id=spec.environment_instance_id,
        candidate_readout_source=candidate_source,
        candidate_cap=candidate_cap,
        target_candidate_ids=target_candidate_ids,
        episodes_per_replicate=episodes_per_replicate,
        training_replicates_per_arm=training_replicates_per_arm,
        base_seed=base_seed,
        locked_by=locked_by,
        run_mode=selected_run_mode,
        threshold_value=threshold_value,
        threshold_frontier_readout_source=threshold_frontier_readout_source,
        tier_jump_reward_cutoff=threshold_value,
        controller_event_ceiling_override=controller_event_ceiling,
        linearization_mode_id=linearization_mode_id,
    )
    threshold = resolve_threshold(
        threshold_value=budget.threshold_value,
        threshold_frontier_readout_source=budget.threshold_frontier_readout_source,
    )
    threshold_policy = ThresholdPolicy(
        threshold_policy_id=budget.threshold_policy_id,
        threshold_value=threshold.threshold_value,
        window_length=budget.window_length,
        required_count=budget.required_count,
    )
    tier_jump_policy = TierJumpPolicy(
        tier_jump_policy_id=DEFAULT_TIER_JUMP_POLICY_ID,
        tier_jump_reward_cutoff=threshold.threshold_value,
        tier_jump_window_length=budget.window_length,
    )
    paths = build_small_paired_replicate_probe_paths(artifact_root)
    paths.root.mkdir(parents=True, exist_ok=True)
    paths.results_dir.mkdir(parents=True, exist_ok=True)
    selection = load_paired_replicate_candidates(
        budget.candidate_readout_source,
        instance_id=spec.environment_instance_id,
        candidate_cap=budget.candidate_cap,
        target_candidate_ids=budget.target_candidate_ids,
    )
    if not selection.selected:
        raise ValueError(
            "candidate source yielded no eligible Schema 1 candidates for "
            f"{spec.environment_instance_id}; source={selection.candidate_readout_source}"
        )
    _write_evaluation_level_manifests(
        paths=paths,
        budget=budget,
        threshold=threshold,
        threshold_policy=threshold_policy,
        tier_jump_policy=tier_jump_policy,
        selection=selection,
    )

    seed_bundles = generate_seed_bundles(
        base_seed=budget.base_seed,
        replicate_count=budget.training_replicates_per_arm,
    )
    horizon = horizon_override or spec.horizon_steps
    records: list[ComparisonRunRecord] = []
    for schema1_candidate in selection.selected:
        for seed_bundle in seed_bundles:
            for runtime_candidate in (
                _schema0_runtime_candidate(schema1_candidate),
                _schema1_runtime_candidate(
                    schema1_candidate,
                    schema1_tower_source=budget.schema1_tower_source,
                ),
            ):
                try:
                    result = run_schema_condition(
                        spec=spec,
                        candidate=runtime_candidate,
                        seed_bundle=seed_bundle,
                        artifact_root=artifact_root,
                        run_mode=budget.run_mode,
                        episode_count=budget.episodes_per_replicate,
                        horizon=horizon,
                        max_controller_events=budget.max_controller_events(horizon),
                        threshold_policy=threshold_policy,
                        tier_jump_policy=tier_jump_policy,
                        linearization_mode_id=budget.linearization_mode_id,
                        evaluation_id=EVALUATION_ID,
                        run_family_id=EVALUATION_RUN_FAMILY_ID,
                        run_family_description=(
                            "Counterpoint small paired replicate probe family."
                        ),
                        command=(
                            "python -m big_boy_benchmarking.cli counterpoint "
                            "paired-replicate-probe run"
                        ),
                        runner_label="counterpoint_small_paired_replicate_probe",
                    )
                    records.append(
                        ComparisonRunRecord(
                            candidate=runtime_candidate,
                            seed_bundle=seed_bundle,
                            result=result,
                            status=result.status,
                        )
                    )
                except Exception as exc:
                    records.append(
                        ComparisonRunRecord(
                            candidate=runtime_candidate,
                            seed_bundle=seed_bundle,
                            result=None,
                            status="failed",
                            failure_reason=f"{type(exc).__name__}: {exc}",
                        )
                    )
    write_csv(
        paths.evaluation_run_index_csv,
        [
            _run_index_row(
                artifact_root,
                budget.run_mode,
                record,
                evaluation_id=EVALUATION_ID,
            ).to_flat_dict()
            for record in records
        ],
        ComparisonRunIndexRow.fieldnames(),
    )
    status = (
        "complete"
        if records and all(record.status == "success" for record in records)
        else "incomplete"
    )
    return {
        "status": status,
        "run_count": len(records),
        "pair_count": len(selection.selected) * len(seed_bundles),
        "evaluation_run_index": str(paths.evaluation_run_index_csv),
        "candidate_manifest": str(paths.candidate_manifest),
        "evaluation_budget_lock": str(paths.evaluation_budget_lock),
    }


def _write_evaluation_level_manifests(
    *,
    paths,
    budget: SmallPairedReplicateProbeBudget,
    threshold: ResolvedThreshold,
    threshold_policy: ThresholdPolicy,
    tier_jump_policy: TierJumpPolicy,
    selection,
) -> None:
    write_json(
        paths.evaluation_manifest, evaluation_manifest_payload(budget=budget), create_parents=True
    )
    write_json(
        paths.evaluation_arm_manifest, evaluation_arm_manifest_payload(), create_parents=True
    )
    write_json(
        paths.evaluation_budget_lock, budget_lock_payload(budget=budget), create_parents=True
    )
    write_json(
        paths.replicate_probe_policy_manifest,
        replicate_probe_policy_payload(budget=budget, threshold=threshold),
        create_parents=True,
    )
    write_json(
        paths.threshold_policy_manifest,
        threshold_policy_payload(threshold_policy, threshold=threshold),
        create_parents=True,
    )
    write_json(
        paths.tier_jump_policy_manifest,
        tier_jump_policy_payload(tier_jump_policy),
        create_parents=True,
    )
    write_json(
        paths.candidate_manifest,
        candidate_manifest_payload(selection=selection, budget=budget),
        create_parents=True,
    )
    write_json(
        paths.parent_source_manifest,
        parent_source_manifest_payload(selection=selection),
        create_parents=True,
    )


def _require_state_collapser_072() -> None:
    import state_collapser

    version = str(getattr(state_collapser, "__version__", "0"))
    if _version_tuple(version) < (0, 7, 2):
        raise ValueError(
            "small paired replicate probe requires state_collapser>=0.7.2 "
            f"with {STATE_COLLAPSER_V072_POINTWISE_LIFTABILITY_SEMANTICS_ID}; "
            f"found {version}"
        )


def _version_tuple(version: str) -> tuple[int, int, int]:
    parts = []
    for item in version.split(".")[:3]:
        digits = "".join(char for char in item if char.isdigit())
        parts.append(int(digits or "0"))
    while len(parts) < 3:
        parts.append(0)
    return tuple(parts)
