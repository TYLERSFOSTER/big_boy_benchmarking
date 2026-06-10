"""Thin command-line interface for Big Boy Benchmarking."""

from __future__ import annotations

import argparse
import json
from collections.abc import Sequence
from pathlib import Path

from big_boy_benchmarking.artifacts.schemas import ARTIFACT_SCHEMA_VERSION
from big_boy_benchmarking.artifacts.validators import validate_artifact_schema_version
from big_boy_benchmarking.artifacts.writers import append_jsonl, write_csv, write_json
from big_boy_benchmarking.environments.counterpoint import (
    small_paired_replicate_probe as paired_replicate_probe,
)
from big_boy_benchmarking.environments.counterpoint import (
    threshold_frontier_probe,
)
from big_boy_benchmarking.environments.counterpoint.artifacts import (
    write_environment_artifacts,
    write_schema_artifacts,
)
from big_boy_benchmarking.environments.counterpoint.diagnostics import (
    balanced_addressability_diagnostics,
    lift_fiber_diagnostics,
    reward_fiber_diagnostics,
)
from big_boy_benchmarking.environments.counterpoint.fixture_search import (
    search_fixture_candidates,
)
from big_boy_benchmarking.environments.counterpoint.fraction_sweep_diagnostics.aggregation import (
    aggregate_fraction_sweep_diagnostics_results,
)
from big_boy_benchmarking.environments.counterpoint.fraction_sweep_diagnostics.config import (
    DEFAULT_DENOMINATOR as FRACTION_SWEEP_DEFAULT_DENOMINATOR,
)
from big_boy_benchmarking.environments.counterpoint.fraction_sweep_diagnostics.config import (
    DEFAULT_EPISODES_PER_REPLICATE as FRACTION_SWEEP_DEFAULT_EPISODES,
)
from big_boy_benchmarking.environments.counterpoint.fraction_sweep_diagnostics.config import (
    DEFAULT_NUMERATORS as FRACTION_SWEEP_DEFAULT_NUMERATORS,
)
from big_boy_benchmarking.environments.counterpoint.fraction_sweep_diagnostics.config import (
    DEFAULT_REPLICATES_PER_SCHEMA_SEED as FRACTION_SWEEP_DEFAULT_REPLICATES,
)
from big_boy_benchmarking.environments.counterpoint.fraction_sweep_diagnostics.config import (
    DEFAULT_SCHEMA_SEEDS as FRACTION_SWEEP_DEFAULT_SCHEMA_SEEDS,
)
from big_boy_benchmarking.environments.counterpoint.fraction_sweep_diagnostics.docs_writer import (
    write_fraction_sweep_diagnostics_docs,
)
from big_boy_benchmarking.environments.counterpoint.fraction_sweep_diagnostics.paths import (
    default_artifact_root as default_fraction_sweep_artifact_root,
)
from big_boy_benchmarking.environments.counterpoint.fraction_sweep_diagnostics.runner import (
    run_fraction_sweep_diagnostics,
)
from big_boy_benchmarking.environments.counterpoint.graph import enumerate_reachable_graph
from big_boy_benchmarking.environments.counterpoint.instances import (
    default_small_spec,
    default_tiny_spec,
    small_candidate_specs,
    tiny_candidate_specs,
)
from big_boy_benchmarking.environments.counterpoint.noisy_rate_diagnostics.aggregation import (
    aggregate_noisy_rate_diagnostics_results,
)
from big_boy_benchmarking.environments.counterpoint.noisy_rate_diagnostics.config import (
    DEFAULT_EPISODES_PER_REPLICATE as NOISY_RATE_DEFAULT_EPISODES,
)
from big_boy_benchmarking.environments.counterpoint.noisy_rate_diagnostics.config import (
    DEFAULT_RATES as NOISY_RATE_DEFAULT_RATES,
)
from big_boy_benchmarking.environments.counterpoint.noisy_rate_diagnostics.config import (
    DEFAULT_REPLICATES_PER_SCHEMA_SEED as NOISY_RATE_DEFAULT_REPLICATES,
)
from big_boy_benchmarking.environments.counterpoint.noisy_rate_diagnostics.config import (
    DEFAULT_SCHEMA_SEEDS as NOISY_RATE_DEFAULT_SCHEMA_SEEDS,
)
from big_boy_benchmarking.environments.counterpoint.noisy_rate_diagnostics.config import (
    parse_rate_list,
)
from big_boy_benchmarking.environments.counterpoint.noisy_rate_diagnostics.docs_writer import (
    write_noisy_rate_diagnostics_docs,
)
from big_boy_benchmarking.environments.counterpoint.noisy_rate_diagnostics.paths import (
    default_artifact_root as default_noisy_rate_artifact_root,
)
from big_boy_benchmarking.environments.counterpoint.noisy_rate_diagnostics.runner import (
    run_noisy_rate_diagnostics,
)
from big_boy_benchmarking.environments.counterpoint.noisy_rate_full_training.aggregation import (
    aggregate_noisy_rate_full_training_results,
)
from big_boy_benchmarking.environments.counterpoint.noisy_rate_full_training.config import (
    SMOKE_CANDIDATE_CAP as NOISY_RATE_FULL_TRAIN_SMOKE_CANDIDATE_CAP,
)
from big_boy_benchmarking.environments.counterpoint.noisy_rate_full_training.config import (
    SMOKE_EPISODES_PER_REPLICATE as NOISY_RATE_FULL_TRAIN_SMOKE_EPISODES,
)
from big_boy_benchmarking.environments.counterpoint.noisy_rate_full_training.config import (
    SMOKE_TRAINING_REPLICATES_PER_CANDIDATE as NOISY_RATE_FULL_TRAIN_SMOKE_REPLICATES,
)
from big_boy_benchmarking.environments.counterpoint.noisy_rate_full_training.docs_writer import (
    write_noisy_rate_full_training_docs,
)
from big_boy_benchmarking.environments.counterpoint.noisy_rate_full_training.paths import (
    default_artifact_root as default_noisy_rate_full_training_artifact_root,
)
from big_boy_benchmarking.environments.counterpoint.noisy_rate_full_training.paths import (
    default_parent_candidate_readout_source,
)
from big_boy_benchmarking.environments.counterpoint.noisy_rate_full_training.runner import (
    run_noisy_rate_full_training,
)
from big_boy_benchmarking.environments.counterpoint.one_third_diagnostics.aggregation import (
    aggregate_one_third_diagnostics_results,
)
from big_boy_benchmarking.environments.counterpoint.one_third_diagnostics.config import (
    DEFAULT_EPISODES_PER_REPLICATE,
    DEFAULT_REPLICATES_PER_SCHEMA_SEED,
    DEFAULT_SCHEMA_SEEDS,
)
from big_boy_benchmarking.environments.counterpoint.one_third_diagnostics.docs_writer import (
    write_one_third_diagnostics_docs,
)
from big_boy_benchmarking.environments.counterpoint.one_third_diagnostics.paths import (
    default_artifact_root,
)
from big_boy_benchmarking.environments.counterpoint.one_third_diagnostics.runner import (
    run_one_third_diagnostics,
)
from big_boy_benchmarking.environments.counterpoint.path_volume import exact_path_volume
from big_boy_benchmarking.environments.counterpoint.runners import (
    run_direct_masked_random,
    run_direct_tabular_q,
    run_tower_schema_smoke,
)
from big_boy_benchmarking.environments.counterpoint.schemas import build_schema_for_id
from big_boy_benchmarking.environments.counterpoint.second_serious_comparison.aggregation import (
    aggregate_second_serious_comparison_results,
)
from big_boy_benchmarking.environments.counterpoint.second_serious_comparison.config import (
    DEFAULT_CALIBRATION_EPISODES as SECOND_SERIOUS_DEFAULT_CALIBRATION_EPISODES,
)
from big_boy_benchmarking.environments.counterpoint.second_serious_comparison.config import (
    DEFAULT_SERIOUS_CANDIDATE_CAP as SECOND_SERIOUS_DEFAULT_SERIOUS_CANDIDATE_CAP,
)
from big_boy_benchmarking.environments.counterpoint.second_serious_comparison.config import (
    DEFAULT_SERIOUS_EPISODES as SECOND_SERIOUS_DEFAULT_SERIOUS_EPISODES,
)
from big_boy_benchmarking.environments.counterpoint.second_serious_comparison.config import (
    DEFAULT_SMOKE_CANDIDATE_CAP as SECOND_SERIOUS_DEFAULT_SMOKE_CANDIDATE_CAP,
)
from big_boy_benchmarking.environments.counterpoint.second_serious_comparison.config import (
    DEFAULT_SMOKE_EPISODES as SECOND_SERIOUS_DEFAULT_SMOKE_EPISODES,
)
from big_boy_benchmarking.environments.counterpoint.second_serious_comparison.config import (
    DEFAULT_SMOKE_REPLICATES as SECOND_SERIOUS_DEFAULT_SMOKE_REPLICATES,
)
from big_boy_benchmarking.environments.counterpoint.second_serious_comparison.config import (
    SCHEMA1_TOWER_SOURCE_IDS as SECOND_SERIOUS_SCHEMA1_TOWER_SOURCE_IDS,
)
from big_boy_benchmarking.environments.counterpoint.second_serious_comparison.config import (
    SCHEMA1_TOWER_SOURCE_ONE_DROP as SECOND_SERIOUS_SCHEMA1_TOWER_SOURCE_ONE_DROP,
)
from big_boy_benchmarking.environments.counterpoint.second_serious_comparison.docs_writer import (
    write_second_serious_comparison_docs,
)
from big_boy_benchmarking.environments.counterpoint.second_serious_comparison.paths import (
    default_artifact_root as default_second_serious_artifact_root,
)
from big_boy_benchmarking.environments.counterpoint.second_serious_comparison.paths import (
    default_candidate_readout_source as default_second_serious_candidate_readout_source,
)
from big_boy_benchmarking.environments.counterpoint.second_serious_comparison.runner import (
    calibrate_second_serious_comparison,
    run_second_serious_comparison,
)
from big_boy_benchmarking.environments.counterpoint.serious_learning.aggregation import (
    aggregate_serious_learning_results,
)
from big_boy_benchmarking.environments.counterpoint.serious_learning.arms import (
    REQUIRED_SERIOUS_LEARNING_ARM_IDS,
)
from big_boy_benchmarking.environments.counterpoint.serious_learning.budgets import (
    CalibrationBudget,
    SchemaSeedSuite,
    SeedBundleSuite,
    SeriousLearningBudgetLock,
)
from big_boy_benchmarking.environments.counterpoint.serious_learning.docs_writer import (
    write_serious_learning_docs,
)
from big_boy_benchmarking.environments.counterpoint.serious_learning.runner import (
    run_budget_locked_serious_learning,
    run_calibration,
)
from big_boy_benchmarking.environments.counterpoint.small_paired_replicate_probe import (
    paths as paired_replicate_paths,
)
from big_boy_benchmarking.environments.counterpoint.threshold_frontier_probe import (
    paths as threshold_frontier_paths,
)
from big_boy_benchmarking.environments.plate_support.ids import (
    DEFAULT_INSTANCE_ID as PLATE_SUPPORT_DEFAULT_INSTANCE_ID,
)
from big_boy_benchmarking.environments.plate_support.graph_stats import (
    summarize_plate_support_graph,
)
from big_boy_benchmarking.environments.plate_support.runner import (
    run_plate_support_environment_readiness,
)
from big_boy_benchmarking.environments.plate_support.direct_star_culdesac_control.config import (
    DirectStarCuldesacControlConfig as PlateSupportDirectStarCuldesacControlConfig,
)
from big_boy_benchmarking.environments.plate_support.direct_star_culdesac_control.runner import (
    run_direct_star_culdesac_control as run_plate_support_direct_star_culdesac_control,
)
from big_boy_benchmarking.environments.plate_support.direct_star_culdesac_control.runner import (
    summarize_direct_star_culdesac_control as summarize_plate_support_direct_star_culdesac_control,
)
from big_boy_benchmarking.environments.plate_support.tower_star.config import (
    TowerStarGuardedLiftComparisonConfig as PlateSupportTowerStarGuardedLiftComparisonConfig,
)
from big_boy_benchmarking.environments.plate_support.tower_star.runner import (
    run_tower_star as run_plate_support_tower_star,
)
from big_boy_benchmarking.environments.plate_support.tower_star.runner import (
    summarize_tower_star as summarize_plate_support_tower_star,
)
from big_boy_benchmarking.environments.plate_support.standard_gauntlet.gates import (
    gate_for_stage as plate_support_gauntlet_gate_for_stage,
)
from big_boy_benchmarking.environments.plate_support.standard_gauntlet.ids import (
    STAGE_DEFINITIONS as PLATE_SUPPORT_GAUNTLET_STAGE_DEFINITIONS,
)
from big_boy_benchmarking.environments.plate_support.standard_gauntlet.ids import (
    STAGE_IDS as PLATE_SUPPORT_GAUNTLET_STAGE_IDS,
)
from big_boy_benchmarking.environments.plate_support.standard_gauntlet.ids import (
    SUITE_ID as PLATE_SUPPORT_GAUNTLET_SUITE_ID,
)
from big_boy_benchmarking.environments.plate_support.standard_gauntlet.paths import (
    default_readiness_source_path as plate_support_gauntlet_readiness_source_path,
)
from big_boy_benchmarking.environments.plate_support.standard_gauntlet.paths import (
    suite_artifact_root as plate_support_gauntlet_artifact_root,
)
from big_boy_benchmarking.environments.plate_support.standard_gauntlet.paths import (
    suite_readout_surface as plate_support_gauntlet_readout_surface,
)
from big_boy_benchmarking.environments.plate_support.standard_gauntlet.structural_and_tower_diagnostics.config import (
    StructuralDiagnosticsConfig as PlateSupportStructuralDiagnosticsConfig,
)
from big_boy_benchmarking.environments.plate_support.standard_gauntlet.structural_and_tower_diagnostics.runner import (
    run_structural_and_tower_diagnostics as run_plate_support_structural_diagnostics,
)
from big_boy_benchmarking.environments.plate_support.standard_gauntlet.contraction_schema_sweep.config import (
    SchemaSweepConfig as PlateSupportSchemaSweepConfig,
)
from big_boy_benchmarking.environments.plate_support.standard_gauntlet.contraction_schema_sweep.runner import (
    run_contraction_schema_sweep as run_plate_support_schema_sweep,
)
from big_boy_benchmarking.environments.plate_support.standard_gauntlet.candidate_discovery.config import (
    CandidateDiscoveryConfig as PlateSupportCandidateDiscoveryConfig,
)
from big_boy_benchmarking.environments.plate_support.standard_gauntlet.candidate_discovery.runner import (
    run_candidate_discovery as run_plate_support_candidate_discovery,
)
from big_boy_benchmarking.environments.plate_support.standard_gauntlet.tower_training_health.config import (
    TowerTrainingHealthConfig as PlateSupportTowerTrainingHealthConfig,
)
from big_boy_benchmarking.environments.plate_support.standard_gauntlet.tower_training_health.runner import (
    run_tower_training_health as run_plate_support_tower_training_health,
)
from big_boy_benchmarking.environments.plate_support.standard_gauntlet.threshold_frontier_calibration.config import (
    ThresholdFrontierCalibrationConfig as PlateSupportThresholdFrontierCalibrationConfig,
)
from big_boy_benchmarking.environments.plate_support.standard_gauntlet.threshold_frontier_calibration.runner import (
    run_threshold_frontier_calibration as run_plate_support_threshold_frontier_calibration,
)
from big_boy_benchmarking.environments.plate_support.standard_gauntlet.paired_replicate_comparison.config import (
    PairedReplicateComparisonConfig as PlateSupportPairedReplicateComparisonConfig,
)
from big_boy_benchmarking.environments.plate_support.standard_gauntlet.paired_replicate_comparison.runner import (
    run_paired_replicate_comparison as run_plate_support_paired_replicate_comparison,
)
from big_boy_benchmarking.environments.plate_support.standard_gauntlet.readout_system_learning.config import (
    ReadoutSystemLearningConfig as PlateSupportReadoutSystemLearningConfig,
)
from big_boy_benchmarking.environments.plate_support.standard_gauntlet.readout_system_learning.runner import (
    build_readout_system_learning as build_plate_support_readout_system_learning,
)
from big_boy_benchmarking.environments.warehouse_gridlock.runner import (
    build_readiness_docs as build_warehouse_gridlock_readiness_docs,
)
from big_boy_benchmarking.environments.warehouse_gridlock.runner import (
    run_graph_diagnostics as run_warehouse_gridlock_graph_diagnostics,
)
from big_boy_benchmarking.environments.warehouse_gridlock.runner import (
    run_random_rollout as run_warehouse_gridlock_random_rollout,
)
from big_boy_benchmarking.environments.warehouse_gridlock.runner import (
    run_state_diagnostics as run_warehouse_gridlock_state_diagnostics,
)
from big_boy_benchmarking.environments.warehouse_gridlock.runner import (
    run_transition_smoke as run_warehouse_gridlock_transition_smoke,
)
from big_boy_benchmarking.environments.warehouse_gridlock.masked_direct_vs_live_lift_tower.config import (
    CANDIDATE_MIX_COORDINATION_READY as WAREHOUSE_MASKED_DEFAULT_CANDIDATE_MIX,
    DEFAULT_CANDIDATE_PROPOSALS_PER_STEP as WAREHOUSE_MASKED_DEFAULT_CANDIDATES,
    DEFAULT_EPISODES_PER_ARM as WAREHOUSE_MASKED_DEFAULT_EPISODES,
    DEFAULT_MAX_ACTIVE_ROBOTS as WAREHOUSE_MASKED_DEFAULT_MAX_ACTIVE_ROBOTS,
    DEFAULT_MAX_SECONDS_PER_EPISODE as WAREHOUSE_MASKED_DEFAULT_MAX_SECONDS,
    DEFAULT_REPLICATES_PER_ARM as WAREHOUSE_MASKED_DEFAULT_REPLICATES,
    DEFAULT_SCHEMA_SEEDS as WAREHOUSE_MASKED_DEFAULT_SCHEMA_SEEDS,
    DEFAULT_SEED as WAREHOUSE_MASKED_DEFAULT_SEED,
    MaskedDirectVsLiveLiftConfig as WarehouseMaskedDirectVsLiveLiftConfig,
)
from big_boy_benchmarking.environments.warehouse_gridlock.masked_direct_vs_live_lift_tower.paths import (
    default_readiness_source as default_warehouse_masked_readiness_source,
)
from big_boy_benchmarking.environments.warehouse_gridlock.masked_direct_vs_live_lift_tower.runner import (
    run_masked_direct_vs_live_lift_tower as run_warehouse_masked_direct_vs_live_lift_tower,
)
from big_boy_benchmarking.environments.warehouse_gridlock.masked_direct_vs_live_lift_tower.runner import (
    summarize_masked_direct_vs_live_lift_tower as summarize_warehouse_masked_direct_vs_live_lift_tower,
)
from big_boy_benchmarking.modes.contracts import validate_mode_contract
from big_boy_benchmarking.modes.linearization import (
    iter_linearization_mode_contracts,
    validate_linearization_mode_contract,
)
from big_boy_benchmarking.modes.registry import iter_mode_contracts
from big_boy_benchmarking.runners.upstream_smoke import (
    run_upstream_smoke,
    summarize_upstream_smoke,
)
from big_boy_benchmarking.seeds.bundles import generate_seed_bundles
from big_boy_benchmarking.upstream.smoke_envs import iter_smoke_environment_specs

RESERVED_CONSOLE_COMMAND = "bbb"


def _linearization_mode_ids() -> tuple[str, ...]:
    return tuple(contract.linearization_mode_id for contract in iter_linearization_mode_contracts())


def _plate_support_schema_families_for_args(args: argparse.Namespace) -> tuple[str, ...]:
    families = [
        "no_contraction",
        "upstream_default",
        "source_local_ratio",
        "action_category",
        "edge_global_noisy_rate",
        "geometry_coordinate",
        "controlled_degeneracy",
    ]
    if args.include_iterated_source_local_ratio:
        families.append("source_local_ratio_iterated")
    return tuple(families)


def _validate_contracts() -> int:
    validate_artifact_schema_version(ARTIFACT_SCHEMA_VERSION).require_valid()
    for contract in iter_mode_contracts():
        validate_mode_contract(contract, allow_reserved=True)
    for contract in iter_linearization_mode_contracts():
        validate_linearization_mode_contract(contract, allow_reserved=True)
    smoke_ids = [spec.smoke_id for spec in iter_smoke_environment_specs()]
    print(
        json.dumps(
            {
                "status": "ok",
                "artifact_schema_version": ARTIFACT_SCHEMA_VERSION,
                "mode_count": len(iter_mode_contracts()),
                "linearization_mode_count": len(iter_linearization_mode_contracts()),
                "serious_learning_arm_count": len(REQUIRED_SERIOUS_LEARNING_ARM_IDS),
                "tower_exploit_explore_available": any(
                    contract.mode_id == "tower_exploit_explore" and contract.runnable
                    for contract in iter_mode_contracts()
                ),
                "smoke_ids": smoke_ids,
                "reserved_console_command": RESERVED_CONSOLE_COMMAND,
            },
            sort_keys=True,
        )
    )
    return 0


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(prog="python -m big_boy_benchmarking.cli")
    subparsers = parser.add_subparsers(dest="command", required=True)

    subparsers.add_parser("validate-contracts")

    run_parser = subparsers.add_parser("run-upstream-smoke")
    run_parser.add_argument("--smoke-id", required=True)
    run_parser.add_argument("--artifact-root", required=True, type=Path)
    run_parser.add_argument("--mode-id", default="tower_empty_schema_tabular")
    run_parser.add_argument(
        "--linearization-mode",
        choices=_linearization_mode_ids(),
        default="tensor_available_disabled",
    )
    run_parser.add_argument("--run-id")
    run_parser.add_argument("--request-readout", action="store_true")

    summary_parser = subparsers.add_parser("summarize-smoke")
    summary_parser.add_argument("--artifact-root", required=True, type=Path)
    summary_parser.add_argument(
        "--run-family-id",
        default="upstream_smoke_readout_discipline_v001",
    )

    warehouse_parser = subparsers.add_parser("warehouse-gridlock")
    warehouse_subparsers = warehouse_parser.add_subparsers(
        dest="warehouse_gridlock_command",
        required=True,
    )
    warehouse_graph_parser = warehouse_subparsers.add_parser("graph-diagnostics")
    warehouse_graph_parser.add_argument("--artifact-root", required=True, type=Path)
    warehouse_graph_parser.add_argument(
        "--instance-id",
        default="warehouse_gridlock_16x16_v001",
    )
    warehouse_graph_parser.add_argument("--run-label", default="smoke_001")
    warehouse_graph_parser.add_argument("--repo-root", type=Path, default=Path("."))

    warehouse_state_parser = warehouse_subparsers.add_parser("state-diagnostics")
    warehouse_state_parser.add_argument("--artifact-root", required=True, type=Path)
    warehouse_state_parser.add_argument(
        "--instance-id",
        default="warehouse_gridlock_16x16_v001",
    )
    warehouse_state_parser.add_argument("--run-label", default="smoke_001")
    warehouse_state_parser.add_argument("--repo-root", type=Path, default=Path("."))

    warehouse_transition_parser = warehouse_subparsers.add_parser("transition-smoke")
    warehouse_transition_parser.add_argument("--artifact-root", required=True, type=Path)
    warehouse_transition_parser.add_argument(
        "--instance-id",
        default="warehouse_gridlock_16x16_v001",
    )
    warehouse_transition_parser.add_argument("--run-label", default="smoke_001")
    warehouse_transition_parser.add_argument("--repo-root", type=Path, default=Path("."))

    warehouse_rollout_parser = warehouse_subparsers.add_parser("random-rollout")
    warehouse_rollout_parser.add_argument("--artifact-root", required=True, type=Path)
    warehouse_rollout_parser.add_argument(
        "--instance-id",
        default="warehouse_gridlock_16x16_v001",
    )
    warehouse_rollout_parser.add_argument("--run-label", default="smoke_001")
    warehouse_rollout_parser.add_argument("--seconds", type=int, default=8)
    warehouse_rollout_parser.add_argument("--seed", type=int, default=0)
    warehouse_rollout_parser.add_argument("--repo-root", type=Path, default=Path("."))

    warehouse_docs_parser = warehouse_subparsers.add_parser("readiness-docs")
    warehouse_docs_parser.add_argument("--artifact-root", required=True, type=Path)
    warehouse_docs_parser.add_argument(
        "--instance-id",
        default="warehouse_gridlock_16x16_v001",
    )
    warehouse_docs_parser.add_argument("--run-label", default="smoke_001")
    warehouse_docs_parser.add_argument("--repo-root", type=Path, default=Path("."))

    warehouse_masked_parser = warehouse_subparsers.add_parser(
        "masked-direct-vs-live-lift-tower"
    )
    warehouse_masked_subparsers = warehouse_masked_parser.add_subparsers(
        dest="warehouse_masked_direct_command",
        required=True,
    )
    warehouse_masked_run_parser = warehouse_masked_subparsers.add_parser("run")
    warehouse_masked_run_parser.add_argument("--repo-root", type=Path, default=Path("."))
    warehouse_masked_run_parser.add_argument("--artifact-root", required=True, type=Path)
    warehouse_masked_run_parser.add_argument("--readiness-source", type=Path)
    warehouse_masked_run_parser.add_argument("--run-label", default="smoke_001")
    warehouse_masked_run_parser.add_argument("--locked-by", required=True)
    warehouse_masked_run_parser.add_argument(
        "--episodes-per-arm",
        type=int,
        default=WAREHOUSE_MASKED_DEFAULT_EPISODES,
    )
    warehouse_masked_run_parser.add_argument(
        "--replicates-per-arm",
        type=int,
        default=WAREHOUSE_MASKED_DEFAULT_REPLICATES,
    )
    warehouse_masked_run_parser.add_argument(
        "--max-seconds-per-episode",
        type=int,
        default=WAREHOUSE_MASKED_DEFAULT_MAX_SECONDS,
    )
    warehouse_masked_run_parser.add_argument(
        "--candidate-proposals-per-step",
        type=int,
        default=WAREHOUSE_MASKED_DEFAULT_CANDIDATES,
    )
    warehouse_masked_run_parser.add_argument(
        "--max-active-robots",
        type=int,
        default=WAREHOUSE_MASKED_DEFAULT_MAX_ACTIVE_ROBOTS,
    )
    warehouse_masked_run_parser.add_argument(
        "--candidate-mix-id",
        default=WAREHOUSE_MASKED_DEFAULT_CANDIDATE_MIX,
    )
    warehouse_masked_run_parser.add_argument(
        "--schema-seeds",
        type=int,
        default=WAREHOUSE_MASKED_DEFAULT_SCHEMA_SEEDS,
    )
    warehouse_masked_run_parser.add_argument(
        "--seed",
        type=int,
        default=WAREHOUSE_MASKED_DEFAULT_SEED,
    )
    warehouse_masked_run_parser.add_argument("--smoke", action="store_true")

    warehouse_masked_summarize_parser = warehouse_masked_subparsers.add_parser("summarize")
    warehouse_masked_summarize_parser.add_argument("--repo-root", type=Path, default=Path("."))
    warehouse_masked_summarize_parser.add_argument("--artifact-root", required=True, type=Path)

    plate_support_parser = subparsers.add_parser("plate-support")
    plate_support_subparsers = plate_support_parser.add_subparsers(
        dest="plate_support_command",
        required=True,
    )
    plate_support_readiness_parser = plate_support_subparsers.add_parser("readiness")
    plate_support_readiness_parser.add_argument("--artifact-root", required=True, type=Path)
    plate_support_readiness_parser.add_argument(
        "--instance-id",
        default=PLATE_SUPPORT_DEFAULT_INSTANCE_ID,
        choices=(PLATE_SUPPORT_DEFAULT_INSTANCE_ID,),
    )
    plate_support_readiness_parser.add_argument("--run-id")
    plate_support_readiness_parser.add_argument("--random-policy-episodes", type=int, default=1000)
    plate_support_readiness_parser.add_argument("--random-policy-seed", type=int, default=0)
    plate_support_readiness_parser.add_argument("--tower-probe-steps", type=int, default=20)
    plate_support_readiness_parser.add_argument("--tower-probe-sample-size", type=int, default=20)
    plate_support_readiness_parser.add_argument("--docs-path", type=Path)
    plate_support_readiness_parser.add_argument(
        "--linearization-mode",
        choices=_linearization_mode_ids(),
        default="tensor_available_disabled",
    )
    plate_support_graph_stats_parser = plate_support_subparsers.add_parser("graph-stats")
    plate_support_graph_stats_parser.add_argument(
        "--instance-id",
        default=PLATE_SUPPORT_DEFAULT_INSTANCE_ID,
        choices=(PLATE_SUPPORT_DEFAULT_INSTANCE_ID,),
    )
    plate_support_graph_stats_parser.add_argument("--output", type=Path)
    plate_support_graph_stats_parser.add_argument("--pretty", action="store_true")

    plate_support_direct_star_parser = plate_support_subparsers.add_parser(
        "direct-star-culdesac-control"
    )
    plate_support_direct_star_subparsers = plate_support_direct_star_parser.add_subparsers(
        dest="direct_star_culdesac_control_command",
        required=True,
    )
    plate_support_direct_star_run_parser = plate_support_direct_star_subparsers.add_parser(
        "run"
    )
    plate_support_direct_star_run_parser.add_argument("--repo-root", required=True, type=Path)
    plate_support_direct_star_run_parser.add_argument("--artifact-root", required=True, type=Path)
    plate_support_direct_star_run_parser.add_argument(
        "--parent-gauntlet-source",
        required=True,
        type=Path,
    )
    plate_support_direct_star_run_parser.add_argument("--run-label", default="guarded_001")
    plate_support_direct_star_run_parser.add_argument("--locked-by", required=True)
    plate_support_direct_star_run_parser.add_argument("--episodes-per-replicate", type=int)
    plate_support_direct_star_run_parser.add_argument("--replicates-per-arm", type=int)
    plate_support_direct_star_run_parser.add_argument(
        "--max-steps-per-episode",
        type=int,
        default=50,
    )
    plate_support_direct_star_run_parser.add_argument("--base-seed", type=int, default=0)
    plate_support_direct_star_run_parser.add_argument("--learning-rate", type=float, default=0.25)
    plate_support_direct_star_run_parser.add_argument("--discount", type=float, default=0.95)
    plate_support_direct_star_run_parser.add_argument("--epsilon", type=float, default=0.20)
    plate_support_direct_star_run_parser.add_argument("--smoke", action="store_true")
    plate_support_direct_star_summarize_parser = (
        plate_support_direct_star_subparsers.add_parser("summarize")
    )
    plate_support_direct_star_summarize_parser.add_argument("--repo-root", required=True, type=Path)
    plate_support_direct_star_summarize_parser.add_argument(
        "--artifact-root",
        required=True,
        type=Path,
    )

    plate_support_tower_star_parser = plate_support_subparsers.add_parser("tower-star")
    plate_support_tower_star_subparsers = plate_support_tower_star_parser.add_subparsers(
        dest="tower_star_command",
        required=True,
    )
    plate_support_tower_star_run_parser = plate_support_tower_star_subparsers.add_parser("run")
    plate_support_tower_star_run_parser.add_argument("--repo-root", required=True, type=Path)
    plate_support_tower_star_run_parser.add_argument("--artifact-root", required=True, type=Path)
    plate_support_tower_star_run_parser.add_argument(
        "--parent-gauntlet-source",
        required=True,
        type=Path,
    )
    plate_support_tower_star_run_parser.add_argument(
        "--direct-star-source",
        required=True,
        type=Path,
    )
    plate_support_tower_star_run_parser.add_argument("--run-label", default="tower_star_001")
    plate_support_tower_star_run_parser.add_argument("--locked-by", required=True)
    plate_support_tower_star_run_parser.add_argument("--episodes-per-replicate", type=int)
    plate_support_tower_star_run_parser.add_argument("--replicates-per-arm", type=int)
    plate_support_tower_star_run_parser.add_argument(
        "--max-steps-per-episode",
        type=int,
        default=50,
    )
    plate_support_tower_star_run_parser.add_argument("--base-seed", type=int, default=0)
    plate_support_tower_star_run_parser.add_argument("--learning-rate", type=float, default=0.25)
    plate_support_tower_star_run_parser.add_argument("--discount", type=float, default=0.95)
    plate_support_tower_star_run_parser.add_argument("--epsilon", type=float, default=0.20)
    plate_support_tower_star_run_parser.add_argument("--smoke", action="store_true")
    plate_support_tower_star_summarize_parser = plate_support_tower_star_subparsers.add_parser(
        "summarize"
    )
    plate_support_tower_star_summarize_parser.add_argument("--repo-root", required=True, type=Path)
    plate_support_tower_star_summarize_parser.add_argument(
        "--artifact-root",
        required=True,
        type=Path,
    )

    plate_support_gauntlet_parser = plate_support_subparsers.add_parser("standard-gauntlet")
    plate_support_gauntlet_subparsers = plate_support_gauntlet_parser.add_subparsers(
        dest="standard_gauntlet_command",
        required=True,
    )
    plate_support_gauntlet_inspect_parser = plate_support_gauntlet_subparsers.add_parser(
        "inspect-architecture"
    )
    plate_support_gauntlet_inspect_parser.add_argument("--repo-root", required=True, type=Path)
    plate_support_gauntlet_inspect_parser.add_argument("--run-label", default="smoke_001")
    plate_support_gauntlet_inspect_parser.add_argument(
        "--readiness-run-label",
        default="dev_001",
    )
    plate_support_structural_parser = plate_support_gauntlet_subparsers.add_parser(
        "structural-diagnostics"
    )
    plate_support_structural_subparsers = plate_support_structural_parser.add_subparsers(
        dest="structural_diagnostics_command",
        required=True,
    )
    plate_support_structural_run_parser = plate_support_structural_subparsers.add_parser("run")
    plate_support_structural_run_parser.add_argument("--repo-root", required=True, type=Path)
    plate_support_structural_run_parser.add_argument("--artifact-root", required=True, type=Path)
    plate_support_structural_run_parser.add_argument("--readiness-source", required=True, type=Path)
    plate_support_structural_run_parser.add_argument("--run-label", default="smoke_001")
    plate_support_structural_run_parser.add_argument("--locked-by", required=True)
    plate_support_structural_run_parser.add_argument("--random-policy-seed", type=int, default=0)
    plate_support_structural_run_parser.add_argument(
        "--random-policy-episodes",
        type=int,
        default=1000,
    )
    plate_support_structural_run_parser.add_argument("--tower-probe-steps", type=int, default=20)
    plate_support_structural_run_parser.add_argument(
        "--tower-probe-sample-size",
        type=int,
        default=20,
    )
    plate_support_structural_run_parser.add_argument(
        "--linearization-mode",
        choices=_linearization_mode_ids(),
        default="tensor_available_disabled",
    )
    plate_support_schema_sweep_parser = plate_support_gauntlet_subparsers.add_parser(
        "schema-sweep"
    )
    plate_support_schema_sweep_subparsers = plate_support_schema_sweep_parser.add_subparsers(
        dest="schema_sweep_command",
        required=True,
    )
    plate_support_schema_sweep_run_parser = plate_support_schema_sweep_subparsers.add_parser("run")
    plate_support_schema_sweep_run_parser.add_argument("--repo-root", required=True, type=Path)
    plate_support_schema_sweep_run_parser.add_argument("--artifact-root", required=True, type=Path)
    plate_support_schema_sweep_run_parser.add_argument("--stage1-source", required=True, type=Path)
    plate_support_schema_sweep_run_parser.add_argument("--run-label", default="smoke_001")
    plate_support_schema_sweep_run_parser.add_argument("--locked-by", required=True)
    plate_support_schema_sweep_run_parser.add_argument("--schema-seed", action="append", type=int)
    plate_support_schema_sweep_run_parser.add_argument(
        "--source-local-ratio-numerator",
        action="append",
        type=int,
    )
    plate_support_schema_sweep_run_parser.add_argument(
        "--source-local-ratio-denominator",
        type=int,
        default=18,
    )
    plate_support_schema_sweep_run_parser.add_argument(
        "--include-iterated-source-local-ratio",
        action="store_true",
    )
    plate_support_schema_sweep_run_parser.add_argument(
        "--iterated-source-local-ratio-numerator",
        action="append",
        type=int,
    )
    plate_support_schema_sweep_run_parser.add_argument(
        "--iterated-source-local-ratio-denominator",
        action="append",
        type=int,
    )
    plate_support_schema_sweep_run_parser.add_argument(
        "--iterated-source-local-schema-seed",
        action="append",
        type=int,
    )
    plate_support_schema_sweep_run_parser.add_argument(
        "--iterated-source-local-max-iterations",
        type=int,
        default=32,
    )
    plate_support_schema_sweep_run_parser.add_argument(
        "--iterated-source-local-selector-rule-id",
        default="plate_support_source_local_iterated_stable_rate_v001",
    )
    plate_support_schema_sweep_run_parser.add_argument(
        "--iterated-source-local-selection-mode",
        default="quotient_source_representative_stable_rate",
    )
    plate_support_schema_sweep_run_parser.add_argument(
        "--iterated-near-full-collapse-threshold",
        type=float,
        default=0.9,
    )
    plate_support_schema_sweep_run_parser.add_argument(
        "--iterated-min-nontrivial-tiers",
        type=int,
        default=3,
    )
    plate_support_schema_sweep_run_parser.add_argument(
        "--edge-global-numerator",
        action="append",
        type=int,
    )
    plate_support_schema_sweep_run_parser.add_argument("--tower-probe-steps", type=int, default=20)
    plate_support_schema_sweep_run_parser.add_argument(
        "--tower-probe-sample-size",
        type=int,
        default=20,
    )
    plate_support_schema_sweep_run_parser.add_argument(
        "--linearization-mode",
        choices=_linearization_mode_ids(),
        default="tensor_available_disabled",
    )
    plate_support_candidate_parser = plate_support_gauntlet_subparsers.add_parser(
        "candidate-discovery"
    )
    plate_support_candidate_subparsers = plate_support_candidate_parser.add_subparsers(
        dest="candidate_discovery_command",
        required=True,
    )
    plate_support_candidate_run_parser = plate_support_candidate_subparsers.add_parser("run")
    plate_support_candidate_run_parser.add_argument("--repo-root", required=True, type=Path)
    plate_support_candidate_run_parser.add_argument("--artifact-root", required=True, type=Path)
    plate_support_candidate_run_parser.add_argument(
        "--schema-sweep-source",
        required=True,
        type=Path,
    )
    plate_support_candidate_run_parser.add_argument("--run-label", default="smoke_001")
    plate_support_candidate_run_parser.add_argument("--locked-by", required=True)
    plate_support_candidate_run_parser.add_argument("--clean-candidate-cap", type=int, default=2)
    plate_support_candidate_run_parser.add_argument("--warning-candidate-cap", type=int, default=1)
    plate_support_candidate_run_parser.add_argument("--degeneracy-anchor-cap", type=int, default=1)
    plate_support_candidate_run_parser.add_argument("--allow-warning-selection", action="store_true")
    plate_support_candidate_run_parser.add_argument(
        "--linearization-mode",
        choices=_linearization_mode_ids(),
        default="tensor_available_disabled",
    )
    plate_support_training_parser = plate_support_gauntlet_subparsers.add_parser(
        "tower-training-health"
    )
    plate_support_training_subparsers = plate_support_training_parser.add_subparsers(
        dest="tower_training_health_command",
        required=True,
    )
    plate_support_training_run_parser = plate_support_training_subparsers.add_parser("run")
    plate_support_training_run_parser.add_argument("--repo-root", required=True, type=Path)
    plate_support_training_run_parser.add_argument("--artifact-root", required=True, type=Path)
    plate_support_training_run_parser.add_argument(
        "--candidate-source",
        required=True,
        type=Path,
    )
    plate_support_training_run_parser.add_argument("--run-label", default="smoke_001")
    plate_support_training_run_parser.add_argument("--locked-by", required=True)
    plate_support_training_run_parser.add_argument("--candidate-cap", type=int, default=2)
    plate_support_training_run_parser.add_argument(
        "--training-replicates-per-candidate",
        type=int,
        default=2,
    )
    plate_support_training_run_parser.add_argument(
        "--episodes-per-replicate",
        type=int,
        default=16,
    )
    plate_support_training_run_parser.add_argument(
        "--max-steps-per-episode",
        type=int,
        default=50,
    )
    plate_support_training_run_parser.add_argument("--base-seed", type=int, default=0)
    plate_support_training_run_parser.add_argument("--allow-warning-candidates", action="store_true")
    plate_support_training_run_parser.add_argument("--learning-rate", type=float, default=0.25)
    plate_support_training_run_parser.add_argument("--discount", type=float, default=0.95)
    plate_support_training_run_parser.add_argument("--epsilon", type=float, default=0.20)
    plate_support_training_run_parser.add_argument(
        "--linearization-mode",
        choices=_linearization_mode_ids(),
        default="tensor_available_disabled",
    )
    plate_support_threshold_parser = plate_support_gauntlet_subparsers.add_parser(
        "threshold-calibration"
    )
    plate_support_threshold_subparsers = plate_support_threshold_parser.add_subparsers(
        dest="threshold_calibration_command",
        required=True,
    )
    plate_support_threshold_run_parser = plate_support_threshold_subparsers.add_parser("run")
    plate_support_threshold_run_parser.add_argument("--repo-root", required=True, type=Path)
    plate_support_threshold_run_parser.add_argument("--artifact-root", required=True, type=Path)
    plate_support_threshold_run_parser.add_argument(
        "--training-health-source",
        required=True,
        type=Path,
    )
    plate_support_threshold_run_parser.add_argument("--stage1-source", type=Path)
    plate_support_threshold_run_parser.add_argument("--run-label", default="smoke_001")
    plate_support_threshold_run_parser.add_argument("--locked-by", required=True)
    plate_support_threshold_run_parser.add_argument("--candidate-cap", type=int, default=1)
    plate_support_threshold_run_parser.add_argument(
        "--allow-warning-candidates",
        action="store_true",
    )
    plate_support_threshold_run_parser.add_argument(
        "--recommended-episodes-per-replicate",
        type=int,
        default=32,
    )
    plate_support_threshold_run_parser.add_argument(
        "--recommended-replicates-per-arm",
        type=int,
        default=4,
    )
    plate_support_threshold_run_parser.add_argument(
        "--linearization-mode",
        choices=_linearization_mode_ids(),
        default="tensor_available_disabled",
    )
    plate_support_paired_parser = plate_support_gauntlet_subparsers.add_parser(
        "paired-comparison"
    )
    plate_support_paired_subparsers = plate_support_paired_parser.add_subparsers(
        dest="paired_comparison_command",
        required=True,
    )
    plate_support_paired_run_parser = plate_support_paired_subparsers.add_parser("run")
    plate_support_paired_run_parser.add_argument("--repo-root", required=True, type=Path)
    plate_support_paired_run_parser.add_argument("--artifact-root", required=True, type=Path)
    plate_support_paired_run_parser.add_argument(
        "--candidate-source",
        required=True,
        type=Path,
    )
    plate_support_paired_run_parser.add_argument(
        "--training-health-source",
        required=True,
        type=Path,
    )
    plate_support_paired_run_parser.add_argument(
        "--threshold-source",
        required=True,
        type=Path,
    )
    plate_support_paired_run_parser.add_argument("--structural-source", type=Path)
    plate_support_paired_run_parser.add_argument("--run-label", default="smoke_001")
    plate_support_paired_run_parser.add_argument("--locked-by", required=True)
    plate_support_paired_run_parser.add_argument("--candidate-cap", type=int, default=1)
    plate_support_paired_run_parser.add_argument(
        "--allow-warning-candidates",
        action="store_true",
    )
    plate_support_paired_run_parser.add_argument(
        "--allow-legacy-dependency",
        action="store_true",
    )
    plate_support_paired_run_parser.add_argument("--episodes-per-replicate", type=int)
    plate_support_paired_run_parser.add_argument("--replicates-per-arm", type=int)
    plate_support_paired_run_parser.add_argument(
        "--max-steps-per-episode",
        type=int,
        default=50,
    )
    plate_support_paired_run_parser.add_argument("--base-seed", type=int, default=0)
    plate_support_paired_run_parser.add_argument("--learning-rate", type=float, default=0.25)
    plate_support_paired_run_parser.add_argument("--discount", type=float, default=0.95)
    plate_support_paired_run_parser.add_argument("--epsilon", type=float, default=0.20)
    plate_support_paired_run_parser.add_argument(
        "--skip-direct-baseline",
        action="store_true",
    )
    plate_support_paired_run_parser.add_argument(
        "--skip-no-contraction-control",
        action="store_true",
    )
    plate_support_paired_run_parser.add_argument(
        "--linearization-mode",
        choices=_linearization_mode_ids(),
        default="tensor_available_disabled",
    )
    plate_support_readout_parser = plate_support_gauntlet_subparsers.add_parser("readout")
    plate_support_readout_subparsers = plate_support_readout_parser.add_subparsers(
        dest="readout_command",
        required=True,
    )
    plate_support_readout_build_parser = plate_support_readout_subparsers.add_parser("build")
    plate_support_readout_build_parser.add_argument(
        "--readout-source",
        required=True,
        type=Path,
    )
    plate_support_readout_build_parser.add_argument(
        "--create-system-learning-archive",
        action="store_true",
    )
    plate_support_readout_inspect_parser = plate_support_readout_subparsers.add_parser("inspect")
    plate_support_readout_inspect_parser.add_argument(
        "--readout-source",
        required=True,
        type=Path,
    )

    counterpoint_parser = subparsers.add_parser("counterpoint")
    counterpoint_subparsers = counterpoint_parser.add_subparsers(
        dest="counterpoint_command",
        required=True,
    )

    fixture_parser = counterpoint_subparsers.add_parser("search-fixtures")
    fixture_parser.add_argument("--artifact-root", required=True, type=Path)
    fixture_parser.add_argument("--scale", choices=("tiny", "small"), default="tiny")

    graph_parser = counterpoint_subparsers.add_parser("graph-diagnostics")
    graph_parser.add_argument("--artifact-root", required=True, type=Path)
    graph_parser.add_argument("--instance-id", choices=("tiny", "small"), default="tiny")

    schema_parser = counterpoint_subparsers.add_parser("schema-diagnostics")
    schema_parser.add_argument("--artifact-root", required=True, type=Path)
    schema_parser.add_argument("--instance-id", choices=("tiny", "small"), default="tiny")
    schema_parser.add_argument("--schema-id", required=True)
    schema_parser.add_argument("--schema-seed", type=int)

    direct_parser = counterpoint_subparsers.add_parser("run-direct")
    direct_parser.add_argument("--artifact-root", required=True, type=Path)
    direct_parser.add_argument("--instance-id", choices=("tiny", "small"), default="tiny")
    direct_parser.add_argument(
        "--policy",
        choices=("masked-random", "tabular-q"),
        default="masked-random",
    )
    direct_parser.add_argument("--seed", type=int, default=0)
    direct_parser.add_argument("--episodes", type=int, default=1)
    direct_parser.add_argument("--horizon", type=int)
    direct_parser.add_argument(
        "--linearization-mode",
        choices=_linearization_mode_ids(),
        default="tensor_available_disabled",
    )

    tower_parser = counterpoint_subparsers.add_parser("tower-smoke")
    tower_parser.add_argument("--artifact-root", required=True, type=Path)
    tower_parser.add_argument("--instance-id", choices=("tiny", "small"), default="tiny")
    tower_parser.add_argument("--schema-id", required=True)
    tower_parser.add_argument("--seed", type=int, default=0)
    tower_parser.add_argument("--schema-seed", type=int)
    tower_parser.add_argument(
        "--linearization-mode",
        choices=_linearization_mode_ids(),
        default="tensor_available_disabled",
    )

    serious_parser = counterpoint_subparsers.add_parser("serious-learning")
    serious_subparsers = serious_parser.add_subparsers(
        dest="serious_learning_command",
        required=True,
    )

    calibration_parser = serious_subparsers.add_parser("calibrate")
    calibration_parser.add_argument("--artifact-root", required=True, type=Path)
    calibration_parser.add_argument("--instance-id", choices=("tiny", "small"), default="small")
    calibration_parser.add_argument("--episodes", type=int, default=1)
    calibration_parser.add_argument("--replicates", type=int, default=1)
    calibration_parser.add_argument("--schema-seeds", type=int, default=1)
    calibration_parser.add_argument("--base-seed", type=int, default=0)
    calibration_parser.add_argument("--horizon", type=int)
    calibration_parser.add_argument(
        "--linearization-mode",
        choices=_linearization_mode_ids(),
        default="tensor_available_disabled",
    )

    serious_run_parser = serious_subparsers.add_parser("run")
    serious_run_parser.add_argument("--artifact-root", required=True, type=Path)
    serious_run_parser.add_argument("--instance-id", choices=("small",), default="small")
    serious_run_parser.add_argument("--episodes", type=int, required=True)
    serious_run_parser.add_argument("--replicates", type=int, required=True)
    serious_run_parser.add_argument("--schema-seeds", type=int, required=True)
    serious_run_parser.add_argument("--base-seed", type=int, default=0)
    serious_run_parser.add_argument("--locked-by", default="cli")
    serious_run_parser.add_argument("--horizon", type=int)
    serious_run_parser.add_argument(
        "--linearization-mode",
        choices=_linearization_mode_ids(),
        default="tensor_available_disabled",
    )

    summarize_parser = serious_subparsers.add_parser("summarize")
    summarize_parser.add_argument("--artifact-root", required=True, type=Path)
    summarize_parser.add_argument("--docs-root", type=Path)

    one_third_parser = counterpoint_subparsers.add_parser("one-third-diagnostics")
    one_third_subparsers = one_third_parser.add_subparsers(
        dest="one_third_diagnostics_command",
        required=True,
    )

    one_third_run_parser = one_third_subparsers.add_parser("run")
    one_third_run_parser.add_argument(
        "--artifact-root",
        type=Path,
        default=default_artifact_root("run_001"),
    )
    one_third_run_parser.add_argument("--instance-ids", default="small,medium")
    one_third_run_parser.add_argument(
        "--schema-seeds",
        default=",".join(map(str, DEFAULT_SCHEMA_SEEDS)),
    )
    one_third_run_parser.add_argument(
        "--replicates",
        type=int,
        default=DEFAULT_REPLICATES_PER_SCHEMA_SEED,
    )
    one_third_run_parser.add_argument(
        "--episodes",
        type=int,
        default=DEFAULT_EPISODES_PER_REPLICATE,
    )
    one_third_run_parser.add_argument("--base-seed", type=int, default=0)
    one_third_run_parser.add_argument("--locked-by", default="cli")
    one_third_run_parser.add_argument("--horizon", type=int)
    one_third_run_parser.add_argument("--controller-event-ceiling", type=int)
    one_third_run_parser.add_argument(
        "--linearization-mode",
        choices=_linearization_mode_ids(),
        default="tensor_available_disabled",
    )

    one_third_summarize_parser = one_third_subparsers.add_parser("summarize")
    one_third_summarize_parser.add_argument("--artifact-root", required=True, type=Path)
    one_third_summarize_parser.add_argument("--docs-root", type=Path)

    fraction_sweep_parser = counterpoint_subparsers.add_parser("fraction-sweep")
    fraction_sweep_subparsers = fraction_sweep_parser.add_subparsers(
        dest="fraction_sweep_command",
        required=True,
    )

    fraction_sweep_run_parser = fraction_sweep_subparsers.add_parser("run")
    fraction_sweep_run_parser.add_argument(
        "--artifact-root",
        type=Path,
        default=default_fraction_sweep_artifact_root("run_001"),
    )
    fraction_sweep_run_parser.add_argument("--instances", default="small,medium")
    fraction_sweep_run_parser.add_argument(
        "--numerators",
        default=",".join(map(str, FRACTION_SWEEP_DEFAULT_NUMERATORS)),
    )
    fraction_sweep_run_parser.add_argument(
        "--denominator",
        type=int,
        default=FRACTION_SWEEP_DEFAULT_DENOMINATOR,
    )
    fraction_sweep_run_parser.add_argument(
        "--schema-seeds",
        default=",".join(map(str, FRACTION_SWEEP_DEFAULT_SCHEMA_SEEDS)),
    )
    fraction_sweep_run_parser.add_argument(
        "--replicates",
        type=int,
        default=FRACTION_SWEEP_DEFAULT_REPLICATES,
    )
    fraction_sweep_run_parser.add_argument(
        "--episodes",
        type=int,
        default=FRACTION_SWEEP_DEFAULT_EPISODES,
    )
    fraction_sweep_run_parser.add_argument("--base-seed", type=int, default=0)
    fraction_sweep_run_parser.add_argument("--locked-by", default="cli")
    fraction_sweep_run_parser.add_argument("--horizon", type=int)
    fraction_sweep_run_parser.add_argument("--controller-event-ceiling", type=int)
    fraction_sweep_run_parser.add_argument(
        "--include-no-contraction-control",
        action="store_true",
        default=True,
        help="include the no-contraction structural control arm",
    )
    fraction_sweep_run_parser.add_argument(
        "--omit-no-contraction-control",
        action="store_false",
        dest="no_contraction_control",
        help="omit the no-contraction structural control arm",
    )
    fraction_sweep_run_parser.add_argument(
        "--linearization-mode",
        choices=_linearization_mode_ids(),
        default="tensor_available_disabled",
    )

    fraction_sweep_summarize_parser = fraction_sweep_subparsers.add_parser("summarize")
    fraction_sweep_summarize_parser.add_argument("--artifact-root", required=True, type=Path)
    fraction_sweep_summarize_parser.add_argument("--docs-root", type=Path)

    noisy_rate_parser = counterpoint_subparsers.add_parser("noisy-rate")
    noisy_rate_subparsers = noisy_rate_parser.add_subparsers(
        dest="noisy_rate_command",
        required=True,
    )

    noisy_rate_run_parser = noisy_rate_subparsers.add_parser("run")
    noisy_rate_run_parser.add_argument(
        "--artifact-root",
        type=Path,
        default=default_noisy_rate_artifact_root("run_001"),
    )
    noisy_rate_run_parser.add_argument("--instances", default="small,medium")
    noisy_rate_run_parser.add_argument(
        "--rates",
        default=",".join(
            f"{numerator}/{denominator}" for numerator, denominator in NOISY_RATE_DEFAULT_RATES
        ),
    )
    noisy_rate_run_parser.add_argument(
        "--schema-seeds",
        default=",".join(map(str, NOISY_RATE_DEFAULT_SCHEMA_SEEDS)),
    )
    noisy_rate_run_parser.add_argument(
        "--replicates",
        type=int,
        default=NOISY_RATE_DEFAULT_REPLICATES,
    )
    noisy_rate_run_parser.add_argument(
        "--episodes",
        type=int,
        default=NOISY_RATE_DEFAULT_EPISODES,
    )
    noisy_rate_run_parser.add_argument("--base-seed", type=int, default=0)
    noisy_rate_run_parser.add_argument("--locked-by", default="cli")
    noisy_rate_run_parser.add_argument("--horizon", type=int)
    noisy_rate_run_parser.add_argument("--controller-event-ceiling", type=int)
    noisy_rate_run_parser.add_argument(
        "--include-no-contraction-control",
        action="store_true",
        default=True,
        help="include the no-contraction structural control arm",
    )
    noisy_rate_run_parser.add_argument(
        "--omit-no-contraction-control",
        action="store_false",
        dest="no_contraction_control",
        help="omit the no-contraction structural control arm",
    )
    noisy_rate_run_parser.add_argument(
        "--linearization-mode",
        choices=_linearization_mode_ids(),
        default="tensor_available_disabled",
    )

    noisy_rate_summarize_parser = noisy_rate_subparsers.add_parser("summarize")
    noisy_rate_summarize_parser.add_argument("--artifact-root", required=True, type=Path)
    noisy_rate_summarize_parser.add_argument("--docs-root", type=Path)

    full_train_parser = counterpoint_subparsers.add_parser("noisy-rate-full-train")
    full_train_subparsers = full_train_parser.add_subparsers(
        dest="noisy_rate_full_train_command",
        required=True,
    )

    full_train_run_parser = full_train_subparsers.add_parser("run")
    full_train_run_parser.add_argument(
        "--artifact-root",
        type=Path,
        default=default_noisy_rate_full_training_artifact_root("run_001"),
    )
    full_train_run_parser.add_argument(
        "--candidate-readout-source",
        type=Path,
        default=default_parent_candidate_readout_source(),
    )
    full_train_run_parser.add_argument(
        "--candidate-cap",
        type=int,
        default=NOISY_RATE_FULL_TRAIN_SMOKE_CANDIDATE_CAP,
    )
    full_train_run_parser.add_argument(
        "--training-replicates",
        type=int,
        default=NOISY_RATE_FULL_TRAIN_SMOKE_REPLICATES,
    )
    full_train_run_parser.add_argument(
        "--episodes",
        type=int,
        default=NOISY_RATE_FULL_TRAIN_SMOKE_EPISODES,
    )
    full_train_run_parser.add_argument("--base-seed", type=int, default=0)
    full_train_run_parser.add_argument("--locked-by", default="cli")
    full_train_run_parser.add_argument("--horizon", type=int)
    full_train_run_parser.add_argument("--controller-event-ceiling", type=int)
    full_train_run_parser.add_argument(
        "--include-runtime-anchor",
        action="store_true",
        help="include no-contraction only as a runtime sanity anchor, not a comparator",
    )
    full_train_run_parser.add_argument(
        "--linearization-mode",
        choices=_linearization_mode_ids(),
        default="tensor_available_disabled",
    )

    full_train_summarize_parser = full_train_subparsers.add_parser("summarize")
    full_train_summarize_parser.add_argument("--artifact-root", required=True, type=Path)
    full_train_summarize_parser.add_argument("--docs-root", type=Path)

    second_serious_parser = counterpoint_subparsers.add_parser("second-serious-comparison")
    second_serious_subparsers = second_serious_parser.add_subparsers(
        dest="second_serious_command",
        required=True,
    )

    second_serious_calibrate_parser = second_serious_subparsers.add_parser("calibrate")
    second_serious_calibrate_parser.add_argument(
        "--artifact-root",
        type=Path,
        default=default_second_serious_artifact_root("calibration_001"),
    )
    second_serious_calibrate_parser.add_argument(
        "--candidate-readout-source",
        type=Path,
        default=default_second_serious_candidate_readout_source(),
    )
    second_serious_calibrate_parser.add_argument("--candidate-cap", type=int, default=2)
    second_serious_calibrate_parser.add_argument(
        "--candidate-id",
        action="append",
        default=None,
        help="target a specific eligible Schema 1 candidate id from candidate_summary.csv",
    )
    second_serious_calibrate_parser.add_argument(
        "--schema1-tower-source",
        choices=SECOND_SERIOUS_SCHEMA1_TOWER_SOURCE_IDS,
        default=SECOND_SERIOUS_SCHEMA1_TOWER_SOURCE_ONE_DROP,
    )
    second_serious_calibrate_parser.add_argument("--instance-id", default="small")
    second_serious_calibrate_parser.add_argument(
        "--episodes",
        type=int,
        default=SECOND_SERIOUS_DEFAULT_CALIBRATION_EPISODES,
    )
    second_serious_calibrate_parser.add_argument(
        "--replicates",
        type=int,
        default=SECOND_SERIOUS_DEFAULT_SMOKE_REPLICATES,
    )
    second_serious_calibrate_parser.add_argument("--base-seed", type=int, default=0)
    second_serious_calibrate_parser.add_argument("--locked-by", default="cli")
    second_serious_calibrate_parser.add_argument("--horizon", type=int)
    second_serious_calibrate_parser.add_argument("--controller-event-ceiling", type=int)
    second_serious_calibrate_parser.add_argument(
        "--linearization-mode",
        choices=_linearization_mode_ids(),
        default="tensor_available_disabled",
    )

    second_serious_run_parser = second_serious_subparsers.add_parser("run")
    second_serious_run_parser.add_argument(
        "--artifact-root",
        type=Path,
        default=default_second_serious_artifact_root("smoke_001"),
    )
    second_serious_run_parser.add_argument(
        "--candidate-readout-source",
        type=Path,
        default=default_second_serious_candidate_readout_source(),
    )
    second_serious_run_parser.add_argument(
        "--candidate-cap",
        type=int,
        default=SECOND_SERIOUS_DEFAULT_SMOKE_CANDIDATE_CAP,
    )
    second_serious_run_parser.add_argument(
        "--candidate-id",
        action="append",
        default=None,
        help="target a specific eligible Schema 1 candidate id from candidate_summary.csv",
    )
    second_serious_run_parser.add_argument(
        "--schema1-tower-source",
        choices=SECOND_SERIOUS_SCHEMA1_TOWER_SOURCE_IDS,
        default=SECOND_SERIOUS_SCHEMA1_TOWER_SOURCE_ONE_DROP,
    )
    second_serious_run_parser.add_argument("--instance-id", default="small")
    second_serious_run_parser.add_argument(
        "--episodes",
        type=int,
        default=SECOND_SERIOUS_DEFAULT_SMOKE_EPISODES,
    )
    second_serious_run_parser.add_argument(
        "--replicates",
        type=int,
        default=SECOND_SERIOUS_DEFAULT_SMOKE_REPLICATES,
    )
    second_serious_run_parser.add_argument(
        "--threshold-policy-id",
        default="counterpoint_total_space_sustained_reward_v001",
    )
    second_serious_run_parser.add_argument("--threshold-value", required=True, type=float)
    second_serious_run_parser.add_argument("--window-length", type=int, default=5)
    second_serious_run_parser.add_argument("--required-count", type=int, default=4)
    second_serious_run_parser.add_argument("--base-seed", type=int, default=0)
    second_serious_run_parser.add_argument("--locked-by", default="cli")
    second_serious_run_parser.add_argument("--horizon", type=int)
    second_serious_run_parser.add_argument("--controller-event-ceiling", type=int)
    second_serious_run_parser.add_argument(
        "--run-mode",
        choices=(
            "smoke_schema_comparison_first_sustained_hit",
            "serious_schema_comparison_first_sustained_hit",
        ),
        default="smoke_schema_comparison_first_sustained_hit",
    )
    second_serious_run_parser.add_argument(
        "--serious-run-authorized",
        action="store_true",
        help="explicitly authorize the serious medium run after PO approval",
    )
    second_serious_run_parser.add_argument(
        "--linearization-mode",
        choices=_linearization_mode_ids(),
        default="tensor_available_disabled",
    )

    second_serious_summarize_parser = second_serious_subparsers.add_parser("summarize")
    second_serious_summarize_parser.add_argument("--artifact-root", required=True, type=Path)
    second_serious_summarize_parser.add_argument("--docs-root", type=Path)

    threshold_frontier_parser = counterpoint_subparsers.add_parser("threshold-frontier")
    threshold_frontier_subparsers = threshold_frontier_parser.add_subparsers(
        dest="threshold_frontier_command",
        required=True,
    )

    threshold_frontier_run_parser = threshold_frontier_subparsers.add_parser("run")
    threshold_frontier_run_parser.add_argument(
        "--artifact-root",
        type=Path,
        default=threshold_frontier_paths.default_artifact_root("smoke_001"),
    )
    threshold_frontier_run_parser.add_argument(
        "--candidate-readout-source",
        type=Path,
        default=threshold_frontier_paths.default_candidate_readout_source(),
    )
    threshold_frontier_run_parser.add_argument(
        "--candidate-id",
        action="append",
        default=None,
        help="target a specific eligible Schema 1 candidate id from candidate_summary.csv",
    )
    threshold_frontier_run_parser.add_argument("--candidate-cap", type=int, default=1)
    threshold_frontier_run_parser.add_argument(
        "--threshold-values",
        default=",".join(str(value) for value in threshold_frontier_probe.DEFAULT_THRESHOLD_VALUES),
    )
    threshold_frontier_run_parser.add_argument("--instance-id", default="wide_span18")
    threshold_frontier_run_parser.add_argument(
        "--episodes",
        type=int,
        default=threshold_frontier_probe.DEFAULT_EPISODES_PER_REPLICATE,
    )
    threshold_frontier_run_parser.add_argument(
        "--replicates",
        type=int,
        default=threshold_frontier_probe.DEFAULT_REPLICATES_PER_ARM,
    )
    threshold_frontier_run_parser.add_argument("--base-seed", type=int, default=0)
    threshold_frontier_run_parser.add_argument("--locked-by", default="cli")
    threshold_frontier_run_parser.add_argument("--horizon", type=int)
    threshold_frontier_run_parser.add_argument("--controller-event-ceiling", type=int)
    threshold_frontier_run_parser.add_argument(
        "--linearization-mode",
        choices=_linearization_mode_ids(),
        default="tensor_available_disabled",
    )

    threshold_frontier_summarize_parser = threshold_frontier_subparsers.add_parser("summarize")
    threshold_frontier_summarize_parser.add_argument("--artifact-root", required=True, type=Path)
    threshold_frontier_summarize_parser.add_argument("--docs-root", type=Path)

    paired_probe_parser = counterpoint_subparsers.add_parser("paired-replicate-probe")
    paired_probe_subparsers = paired_probe_parser.add_subparsers(
        dest="paired_replicate_probe_command",
        required=True,
    )

    paired_probe_run_parser = paired_probe_subparsers.add_parser("run")
    paired_probe_run_parser.add_argument(
        "--artifact-root",
        type=Path,
        default=paired_replicate_paths.default_artifact_root("smoke_001"),
    )
    paired_probe_run_parser.add_argument(
        "--candidate-readout-source",
        type=Path,
        default=paired_replicate_paths.default_candidate_readout_source(),
    )
    paired_probe_run_parser.add_argument(
        "--candidate-id",
        action="append",
        default=None,
        help="target a specific eligible Schema 1 candidate id from candidate_summary.csv",
    )
    paired_probe_run_parser.add_argument("--candidate-cap", type=int, default=1)
    paired_probe_run_parser.add_argument("--threshold-value", type=float)
    paired_probe_run_parser.add_argument("--threshold-frontier-readout-source", type=Path)
    paired_probe_run_parser.add_argument("--instance-id", default="wide_span18")
    paired_probe_run_parser.add_argument(
        "--episodes",
        type=int,
        default=paired_replicate_probe.DEFAULT_EPISODES_PER_REPLICATE,
    )
    paired_probe_run_parser.add_argument(
        "--replicates",
        type=int,
        default=paired_replicate_probe.DEFAULT_REPLICATES_PER_ARM,
    )
    paired_probe_run_parser.add_argument("--base-seed", type=int, default=0)
    paired_probe_run_parser.add_argument("--locked-by", default="cli")
    paired_probe_run_parser.add_argument("--horizon", type=int)
    paired_probe_run_parser.add_argument("--controller-event-ceiling", type=int)
    paired_probe_run_parser.add_argument(
        "--run-mode",
        choices=paired_replicate_probe.RUN_MODE_IDS,
    )
    paired_probe_run_parser.add_argument(
        "--linearization-mode",
        choices=_linearization_mode_ids(),
        default="tensor_available_disabled",
    )

    paired_probe_summarize_parser = paired_probe_subparsers.add_parser("summarize")
    paired_probe_summarize_parser.add_argument("--artifact-root", required=True, type=Path)
    paired_probe_summarize_parser.add_argument("--docs-root", type=Path)

    return parser


def _counterpoint_spec(instance_id: str):
    if instance_id == "tiny":
        return default_tiny_spec()
    if instance_id == "small":
        return default_small_spec()
    raise ValueError(f"unknown counterpoint instance id: {instance_id}")


def _run_plate_support_command(args: argparse.Namespace) -> int:
    if args.plate_support_command == "readiness":
        if args.linearization_mode != "tensor_available_disabled":
            raise ValueError(
                "PlateSupport readiness uses tensor_available_disabled; "
                f"reserved linearization mode rejected: {args.linearization_mode}"
            )
        result = run_plate_support_environment_readiness(
            artifact_root=args.artifact_root,
            instance_id=args.instance_id,
            run_id=args.run_id,
            random_policy_episodes=args.random_policy_episodes,
            random_policy_seed=args.random_policy_seed,
            tower_probe_steps=args.tower_probe_steps,
            tower_probe_sample_size=args.tower_probe_sample_size,
            docs_path=args.docs_path,
            linearization_mode_id=args.linearization_mode,
        )
        print(
            json.dumps(
                {
                    "status": result.status,
                    "run_id": result.run_id,
                    "summary_path": result.summary_path,
                    "artifact_count": len(result.artifact_paths),
                },
                sort_keys=True,
            )
        )
        return 0 if result.status == "success" else 2

    if args.plate_support_command == "graph-stats":
        payload = summarize_plate_support_graph()
        if args.output is not None:
            write_json(args.output, payload)
        print(json.dumps(payload, indent=2 if args.pretty else None, sort_keys=True))
        return 0

    if args.plate_support_command == "direct-star-culdesac-control":
        if args.direct_star_culdesac_control_command == "run":
            result = run_plate_support_direct_star_culdesac_control(
                PlateSupportDirectStarCuldesacControlConfig(
                    repo_root=args.repo_root,
                    artifact_root=args.artifact_root,
                    parent_gauntlet_source=args.parent_gauntlet_source,
                    run_label=args.run_label,
                    locked_by=args.locked_by,
                    episodes_per_replicate=args.episodes_per_replicate,
                    replicates_per_arm=args.replicates_per_arm,
                    max_steps_per_episode=args.max_steps_per_episode,
                    base_seed=args.base_seed,
                    learning_rate=args.learning_rate,
                    discount=args.discount,
                    epsilon=args.epsilon,
                    smoke=args.smoke,
                )
            )
            print(
                json.dumps(
                    {
                        "status": result.status,
                        "evaluation_root": str(result.evaluation_root),
                        "readout_source": str(result.readout_source_path),
                        "interpretation_case": result.interpretation_case,
                        "artifact_count": len(result.artifact_paths),
                        "failure_reason": result.failure_reason,
                    },
                    sort_keys=True,
                )
            )
            return 0 if result.status == "complete" else 2
        if args.direct_star_culdesac_control_command == "summarize":
            result = summarize_plate_support_direct_star_culdesac_control(
                repo_root=args.repo_root,
                artifact_root=args.artifact_root,
            )
            print(
                json.dumps(
                    {
                        "status": result.status,
                        "evaluation_root": str(result.evaluation_root),
                        "readout_source": str(result.readout_source_path),
                        "interpretation_case": result.interpretation_case,
                        "artifact_count": len(result.artifact_paths),
                        "failure_reason": result.failure_reason,
                    },
                    sort_keys=True,
                )
            )
            return 0 if result.status == "complete" else 2
        raise ValueError(
            "unknown PlateSupport direct-star culdesac control command: "
            f"{args.direct_star_culdesac_control_command}"
        )

    if args.plate_support_command == "tower-star":
        if args.tower_star_command == "run":
            result = run_plate_support_tower_star(
                PlateSupportTowerStarGuardedLiftComparisonConfig(
                    repo_root=args.repo_root,
                    artifact_root=args.artifact_root,
                    parent_gauntlet_source=args.parent_gauntlet_source,
                    direct_star_source=args.direct_star_source,
                    run_label=args.run_label,
                    locked_by=args.locked_by,
                    episodes_per_replicate=args.episodes_per_replicate,
                    replicates_per_arm=args.replicates_per_arm,
                    max_steps_per_episode=args.max_steps_per_episode,
                    base_seed=args.base_seed,
                    learning_rate=args.learning_rate,
                    discount=args.discount,
                    epsilon=args.epsilon,
                    smoke=args.smoke,
                )
            )
            print(
                json.dumps(
                    {
                        "status": result.status,
                        "evaluation_root": str(result.evaluation_root),
                        "readout_source": str(result.readout_source_path),
                        "interpretation_case": result.interpretation_case,
                        "artifact_count": len(result.artifact_paths),
                        "failure_reason": result.failure_reason,
                    },
                    sort_keys=True,
                )
            )
            return 0 if result.status == "complete" else 2
        if args.tower_star_command == "summarize":
            result = summarize_plate_support_tower_star(
                repo_root=args.repo_root,
                artifact_root=args.artifact_root,
            )
            print(
                json.dumps(
                    {
                        "status": result.status,
                        "evaluation_root": str(result.evaluation_root),
                        "readout_source": str(result.readout_source_path),
                        "interpretation_case": result.interpretation_case,
                        "artifact_count": len(result.artifact_paths),
                        "failure_reason": result.failure_reason,
                    },
                    sort_keys=True,
                )
            )
            return 0 if result.status == "complete" else 2
        raise ValueError(f"unknown PlateSupport tower-star command: {args.tower_star_command}")

    if args.plate_support_command == "standard-gauntlet":
        if args.standard_gauntlet_command == "inspect-architecture":
            gates = {
                stage_id: {
                    "required_predecessor_statuses": {
                        predecessor: list(statuses)
                        for predecessor, statuses in plate_support_gauntlet_gate_for_stage(
                            stage_id
                        ).required_predecessor_statuses.items()
                    },
                    "required_source_artifact_roles": list(
                        plate_support_gauntlet_gate_for_stage(
                            stage_id
                        ).required_source_artifact_roles
                    ),
                    "claim_boundary": plate_support_gauntlet_gate_for_stage(
                        stage_id
                    ).claim_boundary,
                    "allow_any_prior_artifact": plate_support_gauntlet_gate_for_stage(
                        stage_id
                    ).allow_any_prior_artifact,
                }
                for stage_id in PLATE_SUPPORT_GAUNTLET_STAGE_IDS
            }
            print(
                json.dumps(
                    {
                        "status": "ok",
                        "suite_id": PLATE_SUPPORT_GAUNTLET_SUITE_ID,
                        "stage_definitions": [
                            {
                                "stage_number": stage.stage_number,
                                "stage_id": stage.stage_id,
                                "short_name": stage.short_name,
                                "required_predecessor_stage_ids": list(
                                    stage.required_predecessor_stage_ids
                                ),
                            }
                            for stage in PLATE_SUPPORT_GAUNTLET_STAGE_DEFINITIONS
                        ],
                        "paths": {
                            "repo_readout_surface": str(
                                plate_support_gauntlet_readout_surface(args.repo_root)
                            ),
                            "source_artifact_root": str(
                                plate_support_gauntlet_artifact_root(
                                    args.repo_root,
                                    args.run_label,
                                )
                            ),
                            "readiness_source": str(
                                plate_support_gauntlet_readiness_source_path(
                                    args.repo_root,
                                    readiness_run_label=args.readiness_run_label,
                                )
                            ),
                        },
                        "gates": gates,
                    },
                    sort_keys=True,
                )
            )
            return 0

        if args.standard_gauntlet_command == "structural-diagnostics":
            if args.structural_diagnostics_command == "run":
                if args.linearization_mode != "tensor_available_disabled":
                    raise ValueError(
                        "PlateSupport Stage 1 uses tensor_available_disabled; "
                        f"reserved linearization mode rejected: {args.linearization_mode}"
                    )
                result = run_plate_support_structural_diagnostics(
                    PlateSupportStructuralDiagnosticsConfig(
                        artifact_root=args.artifact_root,
                        run_label=args.run_label,
                        readiness_source_path=args.readiness_source,
                        locked_by=args.locked_by,
                        random_policy_seed=args.random_policy_seed,
                        random_policy_episode_count=args.random_policy_episodes,
                        tower_probe_steps=args.tower_probe_steps,
                        tower_probe_sample_size=args.tower_probe_sample_size,
                        linearization_mode_id=args.linearization_mode,
                    ),
                    repo_root=args.repo_root,
                )
                print(
                    json.dumps(
                        {
                            "status": result.status,
                            "stage_root": str(result.stage_root),
                            "readout_source": str(result.readout_source_path),
                            "artifact_count": len(result.artifact_paths),
                            "failure_reason": result.failure_reason,
                        },
                        sort_keys=True,
                    )
                )
                return 0 if result.status == "complete" else 2
            raise ValueError(
                "unknown PlateSupport structural diagnostics command: "
                f"{args.structural_diagnostics_command}"
            )

        if args.standard_gauntlet_command == "schema-sweep":
            if args.schema_sweep_command == "run":
                if args.linearization_mode != "tensor_available_disabled":
                    raise ValueError(
                        "PlateSupport Stage 2 uses tensor_available_disabled; "
                        f"reserved linearization mode rejected: {args.linearization_mode}"
                    )
                result = run_plate_support_schema_sweep(
                    PlateSupportSchemaSweepConfig(
                        artifact_root=args.artifact_root,
                        run_label=args.run_label,
                        stage1_readout_source_path=args.stage1_source,
                        locked_by=args.locked_by,
                        schema_families=_plate_support_schema_families_for_args(args),
                        schema_seeds=tuple(args.schema_seed or (0,)),
                        source_local_ratio_numerators=tuple(
                            args.source_local_ratio_numerator or (1,)
                        ),
                        source_local_ratio_denominator=args.source_local_ratio_denominator,
                        iterated_source_local_ratio_numerators=tuple(
                            args.iterated_source_local_ratio_numerator or (1,)
                        ),
                        iterated_source_local_ratio_denominators=tuple(
                            args.iterated_source_local_ratio_denominator
                            or (144, 72, 36, 18)
                        ),
                        iterated_source_local_max_iterations=(
                            args.iterated_source_local_max_iterations
                        ),
                        iterated_source_local_selector_rule_id=(
                            args.iterated_source_local_selector_rule_id
                        ),
                        iterated_source_local_selection_mode=(
                            args.iterated_source_local_selection_mode
                        ),
                        iterated_source_local_schema_seeds=(
                            None
                            if args.iterated_source_local_schema_seed is None
                            else tuple(args.iterated_source_local_schema_seed)
                        ),
                        iterated_near_full_collapse_threshold=(
                            args.iterated_near_full_collapse_threshold
                        ),
                        iterated_min_nontrivial_tiers=args.iterated_min_nontrivial_tiers,
                        edge_global_numerators=tuple(
                            args.edge_global_numerator or (1, 2, 4, 8)
                        ),
                        tower_probe_steps=args.tower_probe_steps,
                        tower_probe_sample_size=args.tower_probe_sample_size,
                        linearization_mode_id=args.linearization_mode,
                    ),
                    repo_root=args.repo_root,
                )
                print(
                    json.dumps(
                        {
                            "status": result.status,
                            "stage_root": str(result.stage_root),
                            "readout_source": str(result.readout_source_path),
                            "artifact_count": len(result.artifact_paths),
                            "failure_reason": result.failure_reason,
                        },
                        sort_keys=True,
                    )
                )
                return 0 if result.status == "complete" else 2
            raise ValueError(
                f"unknown PlateSupport schema sweep command: {args.schema_sweep_command}"
            )

        if args.standard_gauntlet_command == "candidate-discovery":
            if args.candidate_discovery_command == "run":
                if args.linearization_mode != "tensor_available_disabled":
                    raise ValueError(
                        "PlateSupport Stage 3 uses tensor_available_disabled; "
                        f"reserved linearization mode rejected: {args.linearization_mode}"
                    )
                result = run_plate_support_candidate_discovery(
                    PlateSupportCandidateDiscoveryConfig(
                        artifact_root=args.artifact_root,
                        run_label=args.run_label,
                        schema_sweep_source_path=args.schema_sweep_source,
                        locked_by=args.locked_by,
                        clean_candidate_cap=args.clean_candidate_cap,
                        warning_candidate_cap=args.warning_candidate_cap,
                        degeneracy_anchor_cap=args.degeneracy_anchor_cap,
                        allow_warning_selection=args.allow_warning_selection,
                        linearization_mode_id=args.linearization_mode,
                    ),
                    repo_root=args.repo_root,
                )
                print(
                    json.dumps(
                        {
                            "status": result.status,
                            "stage_root": str(result.stage_root),
                            "readout_source": str(result.readout_source_path),
                            "artifact_count": len(result.artifact_paths),
                            "failure_reason": result.failure_reason,
                        },
                        sort_keys=True,
                    )
                )
                return 0 if result.status == "complete" else 2
            raise ValueError(
                "unknown PlateSupport candidate discovery command: "
                f"{args.candidate_discovery_command}"
            )

        if args.standard_gauntlet_command == "tower-training-health":
            if args.tower_training_health_command == "run":
                if args.linearization_mode != "tensor_available_disabled":
                    raise ValueError(
                        "PlateSupport Stage 4 uses tensor_available_disabled; "
                        f"reserved linearization mode rejected: {args.linearization_mode}"
                    )
                result = run_plate_support_tower_training_health(
                    PlateSupportTowerTrainingHealthConfig(
                        artifact_root=args.artifact_root,
                        run_label=args.run_label,
                        candidate_source_path=args.candidate_source,
                        locked_by=args.locked_by,
                        candidate_cap=args.candidate_cap,
                        training_replicates_per_candidate=(
                            args.training_replicates_per_candidate
                        ),
                        episodes_per_replicate=args.episodes_per_replicate,
                        max_steps_per_episode=args.max_steps_per_episode,
                        base_seed=args.base_seed,
                        allow_warning_candidates=args.allow_warning_candidates,
                        learning_rate=args.learning_rate,
                        discount=args.discount,
                        epsilon=args.epsilon,
                        linearization_mode_id=args.linearization_mode,
                    ),
                    repo_root=args.repo_root,
                )
                print(
                    json.dumps(
                        {
                            "status": result.status,
                            "stage_root": str(result.stage_root),
                            "readout_source": str(result.readout_source_path),
                            "artifact_count": len(result.artifact_paths),
                            "failure_reason": result.failure_reason,
                        },
                        sort_keys=True,
                    )
                )
                return 0 if result.status == "complete" else 2
            raise ValueError(
                "unknown PlateSupport tower training health command: "
                f"{args.tower_training_health_command}"
            )

        if args.standard_gauntlet_command == "threshold-calibration":
            if args.threshold_calibration_command == "run":
                if args.linearization_mode != "tensor_available_disabled":
                    raise ValueError(
                        "PlateSupport Stage 5 uses tensor_available_disabled; "
                        f"reserved linearization mode rejected: {args.linearization_mode}"
                    )
                result = run_plate_support_threshold_frontier_calibration(
                    PlateSupportThresholdFrontierCalibrationConfig(
                        artifact_root=args.artifact_root,
                        run_label=args.run_label,
                        training_health_source_path=args.training_health_source,
                        locked_by=args.locked_by,
                        stage1_source_path=args.stage1_source,
                        candidate_cap=args.candidate_cap,
                        allow_warning_candidates=args.allow_warning_candidates,
                        recommended_episodes_per_replicate=(
                            args.recommended_episodes_per_replicate
                        ),
                        recommended_replicates_per_arm=(
                            args.recommended_replicates_per_arm
                        ),
                        linearization_mode_id=args.linearization_mode,
                    ),
                    repo_root=args.repo_root,
                )
                print(
                    json.dumps(
                        {
                            "status": result.status,
                            "stage_root": str(result.stage_root),
                            "readout_source": str(result.readout_source_path),
                            "recommended_target_policy_id": (
                                result.recommended_target_policy_id
                            ),
                            "artifact_count": len(result.artifact_paths),
                            "failure_reason": result.failure_reason,
                        },
                        sort_keys=True,
                    )
                )
                return 0 if result.status == "complete" else 2
            raise ValueError(
                "unknown PlateSupport threshold calibration command: "
                f"{args.threshold_calibration_command}"
            )

        if args.standard_gauntlet_command == "paired-comparison":
            if args.paired_comparison_command == "run":
                if args.linearization_mode != "tensor_available_disabled":
                    raise ValueError(
                        "PlateSupport Stage 6 uses tensor_available_disabled; "
                        f"reserved linearization mode rejected: {args.linearization_mode}"
                    )
                result = run_plate_support_paired_replicate_comparison(
                    PlateSupportPairedReplicateComparisonConfig(
                        artifact_root=args.artifact_root,
                        run_label=args.run_label,
                        candidate_source_path=args.candidate_source,
                        training_health_source_path=args.training_health_source,
                        threshold_source_path=args.threshold_source,
                        locked_by=args.locked_by,
                        structural_source_path=args.structural_source,
                        candidate_cap=args.candidate_cap,
                        allow_warning_candidates=args.allow_warning_candidates,
                        allow_legacy_dependency=args.allow_legacy_dependency,
                        episodes_per_replicate=args.episodes_per_replicate,
                        replicates_per_arm=args.replicates_per_arm,
                        max_steps_per_episode=args.max_steps_per_episode,
                        base_seed=args.base_seed,
                        learning_rate=args.learning_rate,
                        discount=args.discount,
                        epsilon=args.epsilon,
                        include_direct_baseline=not args.skip_direct_baseline,
                        include_no_contraction_control=(
                            not args.skip_no_contraction_control
                        ),
                        linearization_mode_id=args.linearization_mode,
                    ),
                    repo_root=args.repo_root,
                )
                print(
                    json.dumps(
                        {
                            "status": result.status,
                            "stage_root": str(result.stage_root),
                            "readout_source": str(result.readout_source_path),
                            "claim_status": result.claim_status,
                            "artifact_count": len(result.artifact_paths),
                            "failure_reason": result.failure_reason,
                        },
                        sort_keys=True,
                    )
                )
                return 0 if result.status == "complete" else 2
            raise ValueError(
                "unknown PlateSupport paired comparison command: "
                f"{args.paired_comparison_command}"
            )

        if args.standard_gauntlet_command == "readout":
            if args.readout_command == "build":
                result = build_plate_support_readout_system_learning(
                    PlateSupportReadoutSystemLearningConfig(
                        readout_source_path=args.readout_source,
                        create_system_learning_archive=(
                            args.create_system_learning_archive
                        ),
                    )
                )
                print(
                    json.dumps(
                        {
                            "status": result.status,
                            "readout_source": str(result.readout_source_path),
                            "readout_surface": str(result.readout_surface),
                            "suite_status": result.suite_status,
                            "claim_status": result.claim_status,
                            "artifact_count": len(result.generated_paths),
                            "failure_reason": result.failure_reason,
                        },
                        sort_keys=True,
                    )
                )
                return 0 if result.status == "complete" else 2
            if args.readout_command == "inspect":
                from big_boy_benchmarking.environments.plate_support.standard_gauntlet.readout_system_learning.stage_sources import (
                    load_suite_readout_source,
                )

                source = load_suite_readout_source(args.readout_source)
                print(
                    json.dumps(
                        {
                            "status": "ok",
                            "readout_source": str(source.path),
                            "stage_count": len(source.stage_records),
                            "stages": [
                                {
                                    "stage_number": record.stage_number,
                                    "short_name": record.short_name,
                                    "status": record.status,
                                    "claim_status": record.claim_status,
                                }
                                for record in source.stage_records
                            ],
                        },
                        sort_keys=True,
                    )
                )
                return 0
            raise ValueError(
                f"unknown PlateSupport readout command: {args.readout_command}"
            )

    raise ValueError(f"unknown PlateSupport command: {args.plate_support_command}")


def _run_warehouse_gridlock_command(args: argparse.Namespace) -> int:
    if args.warehouse_gridlock_command == "graph-diagnostics":
        result = run_warehouse_gridlock_graph_diagnostics(
            artifact_root=args.artifact_root,
            instance_id=args.instance_id,
            run_label=args.run_label,
        )
        print(json.dumps(_warehouse_gridlock_result_payload(result), sort_keys=True))
        return 0 if result.status == "ok" else 2

    if args.warehouse_gridlock_command == "state-diagnostics":
        result = run_warehouse_gridlock_state_diagnostics(
            artifact_root=args.artifact_root,
            instance_id=args.instance_id,
            run_label=args.run_label,
        )
        print(json.dumps(_warehouse_gridlock_result_payload(result), sort_keys=True))
        return 0 if result.status == "ok" else 2

    if args.warehouse_gridlock_command == "transition-smoke":
        result = run_warehouse_gridlock_transition_smoke(
            artifact_root=args.artifact_root,
            instance_id=args.instance_id,
            run_label=args.run_label,
        )
        print(json.dumps(_warehouse_gridlock_result_payload(result), sort_keys=True))
        return 0 if result.status == "ok" else 2

    if args.warehouse_gridlock_command == "random-rollout":
        result = run_warehouse_gridlock_random_rollout(
            artifact_root=args.artifact_root,
            instance_id=args.instance_id,
            run_label=args.run_label,
            seconds=args.seconds,
            seed=args.seed,
        )
        print(json.dumps(_warehouse_gridlock_result_payload(result), sort_keys=True))
        return 0 if result.status == "ok" else 2

    if args.warehouse_gridlock_command == "readiness-docs":
        result = build_warehouse_gridlock_readiness_docs(
            repo_root=args.repo_root,
            artifact_root=args.artifact_root,
            instance_id=args.instance_id,
            run_label=args.run_label,
        )
        print(json.dumps(_warehouse_gridlock_result_payload(result), sort_keys=True))
        return 0 if result.status == "ok" else 2

    if args.warehouse_gridlock_command == "masked-direct-vs-live-lift-tower":
        if args.warehouse_masked_direct_command == "run":
            readiness_source = args.readiness_source or default_warehouse_masked_readiness_source(
                args.repo_root
            )
            result = run_warehouse_masked_direct_vs_live_lift_tower(
                WarehouseMaskedDirectVsLiveLiftConfig(
                    repo_root=args.repo_root,
                    artifact_root=args.artifact_root,
                    readiness_source=readiness_source,
                    run_label=args.run_label,
                    locked_by=args.locked_by,
                    episodes_per_arm=args.episodes_per_arm,
                    replicates_per_arm=args.replicates_per_arm,
                    max_seconds_per_episode=args.max_seconds_per_episode,
                    candidate_proposals_per_step=args.candidate_proposals_per_step,
                    max_active_robots=args.max_active_robots,
                    candidate_mix_id=args.candidate_mix_id,
                    schema_seeds=args.schema_seeds,
                    seed=args.seed,
                    smoke=args.smoke,
                )
            )
            print(json.dumps(_warehouse_gridlock_result_payload(result), sort_keys=True))
            return 0 if result.status == "success" else 2
        if args.warehouse_masked_direct_command == "summarize":
            result = summarize_warehouse_masked_direct_vs_live_lift_tower(
                repo_root=args.repo_root,
                artifact_root=args.artifact_root,
            )
            print(json.dumps(_warehouse_gridlock_result_payload(result), sort_keys=True))
            return 0 if result.status == "success" else 2
        raise ValueError(
            "unknown Warehouse Gridlock masked direct/live-lift command: "
            f"{args.warehouse_masked_direct_command}"
        )

    raise ValueError(f"unknown Warehouse Gridlock command: {args.warehouse_gridlock_command}")


def _warehouse_gridlock_result_payload(result: object) -> dict[str, object]:
    summary = result.summary
    artifact_paths = result.artifact_paths
    return {
        "status": result.status,
        "artifact_count": len(artifact_paths),
        "instance_id": summary.get("instance_id"),
        "robot_count": summary.get("robot_count"),
        "box_count": summary.get("box_count"),
        "traversable_node_count": summary.get("traversable_node_count"),
        "directed_edge_count": summary.get("directed_edge_count"),
        "transition_case_count": summary.get("transition_case_count"),
        "invalid_reason_count": summary.get("invalid_reason_count"),
        "rollout_steps_recorded": summary.get("rollout_steps_recorded"),
    }


def _run_counterpoint_command(args: argparse.Namespace) -> int:
    if args.counterpoint_command == "search-fixtures":
        candidates = tiny_candidate_specs() if args.scale == "tiny" else small_candidate_specs()
        results = search_fixture_candidates(candidates)
        target = args.artifact_root / "counterpoint" / "fixture_search"
        target.mkdir(parents=True, exist_ok=True)
        for result in results:
            append_jsonl(target / f"{args.scale}_fixture_search.jsonl", result.to_dict())
        write_json(
            target / f"{args.scale}_fixture_search_summary.json",
            {
                "scale": args.scale,
                "candidate_count": len(results),
                "selected": [
                    result.environment_instance_id for result in results if result.selected
                ],
            },
        )
        print(json.dumps({"status": "ok", "candidate_count": len(results)}, sort_keys=True))
        return 0

    if args.counterpoint_command == "graph-diagnostics":
        spec = _counterpoint_spec(args.instance_id)
        graph = enumerate_reachable_graph(spec)
        path_summary = exact_path_volume(spec, length=spec.horizon_steps, graph=graph)
        target = (
            args.artifact_root / "counterpoint" / "graph_diagnostics" / spec.environment_instance_id
        )
        artifact_paths = write_environment_artifacts(
            target,
            graph=graph,
            path_summary=path_summary,
        )
        print(
            json.dumps(
                {
                    "status": "ok",
                    "state_count": len(graph.states),
                    "edge_count": len(graph.edges),
                    "artifact_count": len(artifact_paths),
                },
                sort_keys=True,
            )
        )
        return 0

    if args.counterpoint_command == "schema-diagnostics":
        spec = _counterpoint_spec(args.instance_id)
        graph = enumerate_reachable_graph(spec)
        schema = build_schema_for_id(
            graph,
            schema_id=args.schema_id,
            schema_seed=args.schema_seed,
        )
        target = args.artifact_root / "counterpoint" / "schema_diagnostics" / schema.spec.schema_id
        artifact_paths = write_schema_artifacts(target, schema=schema)
        reward_rows = [row.to_dict() for row in reward_fiber_diagnostics(graph, schema)]
        lift_rows = [row.to_dict() for row in lift_fiber_diagnostics(schema)]
        addressability = balanced_addressability_diagnostics(schema)
        write_csv(
            target / "reward_fiber_variance.csv",
            reward_rows,
            [
                "schema_id",
                "cell_id",
                "fine_transition_count",
                "reward_mean",
                "reward_variance",
                "reward_min",
                "reward_max",
                "term_variance",
            ],
        )
        write_csv(
            target / "lift_fiber_summary.csv",
            lift_rows,
            [
                "cell_id",
                "fine_candidate_count",
                "entropy",
                "valid_lift_count",
                "failed_lift_count",
                "failed_lift_reason_counts",
            ],
        )
        write_json(target / "balanced_addressability.json", addressability.to_dict())
        print(
            json.dumps(
                {
                    "status": "ok",
                    "schema_id": schema.spec.schema_id,
                    "artifact_count": len(artifact_paths) + 3,
                },
                sort_keys=True,
            )
        )
        return 0

    if args.counterpoint_command == "run-direct":
        spec = _counterpoint_spec(args.instance_id)
        seed_bundle = generate_seed_bundles(base_seed=args.seed, replicate_count=1)[0]
        if args.policy == "masked-random":
            result = run_direct_masked_random(
                spec=spec,
                seed_bundle=seed_bundle,
                artifact_root=args.artifact_root,
                episode_count=args.episodes,
                horizon=args.horizon,
                linearization_mode_id=args.linearization_mode,
            )
        else:
            result = run_direct_tabular_q(
                spec=spec,
                seed_bundle=seed_bundle,
                artifact_root=args.artifact_root,
                episode_count=args.episodes,
                horizon=args.horizon,
                linearization_mode_id=args.linearization_mode,
            )
        print(json.dumps({"status": result.status, "run_id": result.run_id}, sort_keys=True))
        return 0 if result.status == "success" else 2

    if args.counterpoint_command == "tower-smoke":
        spec = _counterpoint_spec(args.instance_id)
        seed_bundle = generate_seed_bundles(base_seed=args.seed, replicate_count=1)[0]
        result = run_tower_schema_smoke(
            spec=spec,
            schema_id=args.schema_id,
            seed_bundle=seed_bundle,
            artifact_root=args.artifact_root,
            schema_seed=args.schema_seed,
            linearization_mode_id=args.linearization_mode,
        )
        print(json.dumps({"status": result.status, "run_id": result.run_id}, sort_keys=True))
        return 0 if result.status == "success" else 2

    if args.counterpoint_command == "serious-learning":
        return _run_counterpoint_serious_learning_command(args)

    if args.counterpoint_command == "one-third-diagnostics":
        return _run_counterpoint_one_third_diagnostics_command(args)

    if args.counterpoint_command == "fraction-sweep":
        return _run_counterpoint_fraction_sweep_command(args)

    if args.counterpoint_command == "noisy-rate":
        return _run_counterpoint_noisy_rate_command(args)
    if args.counterpoint_command == "noisy-rate-full-train":
        return _run_counterpoint_noisy_rate_full_train_command(args)
    if args.counterpoint_command == "second-serious-comparison":
        return _run_counterpoint_second_serious_comparison_command(args)
    if args.counterpoint_command == "threshold-frontier":
        return _run_counterpoint_threshold_frontier_command(args)
    if args.counterpoint_command == "paired-replicate-probe":
        return _run_counterpoint_paired_replicate_probe_command(args)

    raise ValueError(f"unknown counterpoint command: {args.counterpoint_command}")


def _run_counterpoint_serious_learning_command(args: argparse.Namespace) -> int:
    if hasattr(args, "linearization_mode"):
        _require_serious_linearization(args.linearization_mode)

    if args.serious_learning_command == "calibrate":
        instance_id = (
            "counterpoint_symbolic_n3_tiny_v001"
            if args.instance_id == "tiny"
            else "counterpoint_symbolic_n3_small_v001"
        )
        budget = CalibrationBudget(
            environment_instance_id=instance_id,
            episode_count=args.episodes,
            max_steps_per_episode=args.horizon or (4 if args.instance_id == "tiny" else 8),
            replicate_count=args.replicates,
            random_schema_seed_count=args.schema_seeds,
            smoke=args.instance_id == "tiny",
        )
        result = run_calibration(
            artifact_root=args.artifact_root,
            budget=budget,
            base_seed=args.base_seed,
        )
        print(json.dumps(result, sort_keys=True))
        return 0

    if args.serious_learning_command == "run":
        if args.schema_seeds < 2:
            raise ValueError("serious run requires at least two schema seeds")
        seed_bundles = generate_seed_bundles(
            base_seed=args.base_seed,
            replicate_count=args.replicates,
        )
        lock = SeriousLearningBudgetLock(
            environment_instance_id="counterpoint_symbolic_n3_small_v001",
            arm_ids=REQUIRED_SERIOUS_LEARNING_ARM_IDS,
            episode_count=args.episodes,
            max_steps_per_episode=args.horizon or 8,
            replicate_count=args.replicates,
            random_schema_seed_count=args.schema_seeds,
            schema_seed_suite=SchemaSeedSuite(tuple(range(args.schema_seeds))),
            seed_bundle_ids=tuple(bundle.seed_bundle_id for bundle in seed_bundles),
            controller_config_id="exploit_explore_controller_v001",
            learner_config_id="tabular_q_v001",
            linearization_mode_id=args.linearization_mode,
            calibration_artifact_root=str(args.artifact_root),
            locked_by=args.locked_by,
        )
        result = run_budget_locked_serious_learning(
            artifact_root=args.artifact_root,
            budget_lock=lock,
            seed_bundle_suite=SeedBundleSuite(seed_bundles),
        )
        print(json.dumps(result, sort_keys=True))
        return 0 if result["status"] == "complete" else 2

    if args.serious_learning_command == "summarize":
        summary = aggregate_serious_learning_results(args.artifact_root)
        docs = write_serious_learning_docs(
            artifact_root=args.artifact_root,
            docs_root=args.docs_root,
            command_lines=(
                "uv run python -m big_boy_benchmarking.cli counterpoint serious-learning "
                "summarize --artifact-root <artifact-root>",
            ),
        )
        print(json.dumps({"status": summary["status"], "docs": docs}, sort_keys=True))
        return 0 if summary["status"] == "complete" else 2

    raise ValueError(f"unknown serious learning command: {args.serious_learning_command}")


def _run_counterpoint_one_third_diagnostics_command(args: argparse.Namespace) -> int:
    if hasattr(args, "linearization_mode"):
        _require_one_third_linearization(args.linearization_mode)

    if args.one_third_diagnostics_command == "run":
        instance_ids = _parse_csv_strings(args.instance_ids)
        schema_seeds = _parse_csv_ints(args.schema_seeds)
        result = run_one_third_diagnostics(
            artifact_root=args.artifact_root,
            instance_ids=instance_ids,
            schema_seeds=schema_seeds,
            replicates_per_schema_seed=args.replicates,
            episodes_per_replicate=args.episodes,
            base_seed=args.base_seed,
            locked_by=args.locked_by,
            horizon_override=args.horizon,
            controller_event_ceiling=args.controller_event_ceiling,
            linearization_mode_id=args.linearization_mode,
        )
        print(json.dumps(result, sort_keys=True))
        return 0 if result["status"] == "complete" else 2

    if args.one_third_diagnostics_command == "summarize":
        summary = aggregate_one_third_diagnostics_results(
            args.artifact_root,
            docs_root=args.docs_root,
        )
        docs = write_one_third_diagnostics_docs(
            artifact_root=args.artifact_root,
            docs_root=args.docs_root,
            command_lines=(
                "uv run python -m big_boy_benchmarking.cli counterpoint "
                "one-third-diagnostics summarize --artifact-root <artifact-root>",
            ),
        )
        print(json.dumps({"status": summary["status"], "docs": docs}, sort_keys=True))
        return 0 if summary["status"] == "complete" else 2

    raise ValueError(f"unknown one-third diagnostics command: {args.one_third_diagnostics_command}")


def _run_counterpoint_fraction_sweep_command(args: argparse.Namespace) -> int:
    if hasattr(args, "linearization_mode"):
        _require_fraction_sweep_linearization(args.linearization_mode)

    if args.fraction_sweep_command == "run":
        instances = _parse_csv_strings(args.instances)
        numerators = _parse_csv_ints(args.numerators)
        schema_seeds = _parse_csv_ints(args.schema_seeds)
        result = run_fraction_sweep_diagnostics(
            artifact_root=args.artifact_root,
            instance_ids=instances,
            numerators=numerators,
            denominator=args.denominator,
            include_no_contraction_control=args.no_contraction_control,
            schema_seeds=schema_seeds,
            replicates_per_schema_seed=args.replicates,
            episodes_per_replicate=args.episodes,
            base_seed=args.base_seed,
            locked_by=args.locked_by,
            horizon_override=args.horizon,
            controller_event_ceiling=args.controller_event_ceiling,
            linearization_mode_id=args.linearization_mode,
        )
        print(json.dumps(result, sort_keys=True))
        return 0 if result["status"] == "complete" else 2

    if args.fraction_sweep_command == "summarize":
        summary = aggregate_fraction_sweep_diagnostics_results(
            args.artifact_root,
            docs_root=args.docs_root,
        )
        docs = write_fraction_sweep_diagnostics_docs(
            artifact_root=args.artifact_root,
            docs_root=args.docs_root,
            command_lines=(
                "uv run python -m big_boy_benchmarking.cli counterpoint "
                "fraction-sweep summarize --artifact-root <artifact-root>",
            ),
        )
        print(json.dumps({"status": summary["status"], "docs": docs}, sort_keys=True))
        return 0 if summary["status"] == "complete" else 2

    raise ValueError(f"unknown fraction sweep command: {args.fraction_sweep_command}")


def _run_counterpoint_noisy_rate_command(args: argparse.Namespace) -> int:
    if hasattr(args, "linearization_mode"):
        _require_noisy_rate_linearization(args.linearization_mode)

    if args.noisy_rate_command == "run":
        instances = _parse_csv_strings(args.instances)
        rates = parse_rate_list(args.rates)
        schema_seeds = _parse_csv_ints(args.schema_seeds)
        result = run_noisy_rate_diagnostics(
            artifact_root=args.artifact_root,
            instance_ids=instances,
            rates=rates,
            include_no_contraction_control=args.no_contraction_control,
            schema_seeds=schema_seeds,
            replicates_per_schema_seed=args.replicates,
            episodes_per_replicate=args.episodes,
            base_seed=args.base_seed,
            locked_by=args.locked_by,
            horizon_override=args.horizon,
            controller_event_ceiling=args.controller_event_ceiling,
            linearization_mode_id=args.linearization_mode,
        )
        print(json.dumps(result, sort_keys=True))
        return 0 if result["status"] == "complete" else 2

    if args.noisy_rate_command == "summarize":
        summary = aggregate_noisy_rate_diagnostics_results(
            args.artifact_root,
            docs_root=args.docs_root,
        )
        docs = write_noisy_rate_diagnostics_docs(
            artifact_root=args.artifact_root,
            docs_root=args.docs_root,
            command_lines=(
                "uv run python -m big_boy_benchmarking.cli counterpoint "
                "noisy-rate summarize --artifact-root <artifact-root>",
            ),
        )
        print(json.dumps({"status": summary["status"], "docs": docs}, sort_keys=True))
        return 0 if summary["status"] == "complete" else 2

    raise ValueError(f"unknown noisy-rate command: {args.noisy_rate_command}")


def _run_counterpoint_noisy_rate_full_train_command(args: argparse.Namespace) -> int:
    if hasattr(args, "linearization_mode"):
        _require_noisy_rate_full_train_linearization(args.linearization_mode)

    if args.noisy_rate_full_train_command == "run":
        result = run_noisy_rate_full_training(
            artifact_root=args.artifact_root,
            parent_candidate_readout_source=args.candidate_readout_source,
            include_runtime_anchor=args.include_runtime_anchor,
            candidate_cap=args.candidate_cap,
            training_replicates_per_candidate=args.training_replicates,
            episodes_per_replicate=args.episodes,
            base_seed=args.base_seed,
            locked_by=args.locked_by,
            horizon_override=args.horizon,
            controller_event_ceiling=args.controller_event_ceiling,
            linearization_mode_id=args.linearization_mode,
        )
        print(json.dumps(result, sort_keys=True))
        return 0 if result["status"] == "complete" else 2

    if args.noisy_rate_full_train_command == "summarize":
        summary = aggregate_noisy_rate_full_training_results(
            args.artifact_root,
            docs_root=args.docs_root,
        )
        docs = write_noisy_rate_full_training_docs(
            artifact_root=args.artifact_root,
            docs_root=args.docs_root,
            command_lines=(
                "uv run python -m big_boy_benchmarking.cli counterpoint "
                "noisy-rate-full-train summarize --artifact-root <artifact-root>",
            ),
        )
        print(json.dumps({"status": summary["status"], "docs": docs}, sort_keys=True))
        return 0 if summary["status"] == "complete" else 2

    raise ValueError(f"unknown noisy-rate-full-train command: {args.noisy_rate_full_train_command}")


def _run_counterpoint_second_serious_comparison_command(args: argparse.Namespace) -> int:
    if hasattr(args, "linearization_mode"):
        _require_second_serious_linearization(args.linearization_mode)

    if args.second_serious_command == "calibrate":
        result = calibrate_second_serious_comparison(
            artifact_root=args.artifact_root,
            candidate_readout_source=args.candidate_readout_source,
            instance_id=args.instance_id,
            candidate_cap=args.candidate_cap,
            target_candidate_ids=tuple(args.candidate_id or ()),
            schema1_tower_source=args.schema1_tower_source,
            training_replicates_per_arm=args.replicates,
            episodes_per_replicate=args.episodes,
            base_seed=args.base_seed,
            locked_by=args.locked_by,
            horizon_override=args.horizon,
            controller_event_ceiling=args.controller_event_ceiling,
            linearization_mode_id=args.linearization_mode,
        )
        print(json.dumps(result, sort_keys=True))
        return 0 if result["status"] == "complete" else 2

    if args.second_serious_command == "run":
        if (
            args.run_mode == "serious_schema_comparison_first_sustained_hit"
            and args.candidate_cap != SECOND_SERIOUS_DEFAULT_SERIOUS_CANDIDATE_CAP
        ):
            raise ValueError(
                "serious second-serious-comparison run requires candidate-cap 4 "
                "unless a later PO-approved workplan changes that lock"
            )
        if (
            args.run_mode == "serious_schema_comparison_first_sustained_hit"
            and args.episodes != SECOND_SERIOUS_DEFAULT_SERIOUS_EPISODES
        ):
            raise ValueError(
                "serious second-serious-comparison run requires 256 episodes "
                "unless a later PO-approved workplan changes that lock"
            )
        result = run_second_serious_comparison(
            artifact_root=args.artifact_root,
            candidate_readout_source=args.candidate_readout_source,
            instance_id=args.instance_id,
            candidate_cap=args.candidate_cap,
            target_candidate_ids=tuple(args.candidate_id or ()),
            schema1_tower_source=args.schema1_tower_source,
            training_replicates_per_arm=args.replicates,
            episodes_per_replicate=args.episodes,
            threshold_policy_id=args.threshold_policy_id,
            threshold_value=args.threshold_value,
            window_length=args.window_length,
            required_count=args.required_count,
            run_mode=args.run_mode,
            base_seed=args.base_seed,
            locked_by=args.locked_by,
            horizon_override=args.horizon,
            controller_event_ceiling=args.controller_event_ceiling,
            linearization_mode_id=args.linearization_mode,
            serious_run_authorized=args.serious_run_authorized,
        )
        print(json.dumps(result, sort_keys=True))
        return 0 if result["status"] == "complete" else 2

    if args.second_serious_command == "summarize":
        summary = aggregate_second_serious_comparison_results(
            args.artifact_root,
            docs_root=args.docs_root,
        )
        docs = write_second_serious_comparison_docs(
            artifact_root=args.artifact_root,
            docs_root=args.docs_root,
            command_lines=(
                "uv run python -m big_boy_benchmarking.cli counterpoint "
                "second-serious-comparison summarize --artifact-root <artifact-root>",
            ),
        )
        print(json.dumps({"status": summary["status"], "docs": docs}, sort_keys=True))
        return 0 if summary["status"] == "complete" else 2

    raise ValueError(f"unknown second-serious-comparison command: {args.second_serious_command}")


def _run_counterpoint_paired_replicate_probe_command(args: argparse.Namespace) -> int:
    if hasattr(args, "linearization_mode"):
        _require_paired_replicate_linearization(args.linearization_mode)

    if args.paired_replicate_probe_command == "run":
        result = paired_replicate_probe.run_small_paired_replicate_probe(
            artifact_root=args.artifact_root,
            candidate_readout_source=args.candidate_readout_source,
            threshold_value=args.threshold_value,
            threshold_frontier_readout_source=args.threshold_frontier_readout_source,
            instance_id=args.instance_id,
            candidate_cap=args.candidate_cap,
            target_candidate_ids=tuple(args.candidate_id or ()),
            training_replicates_per_arm=args.replicates,
            episodes_per_replicate=args.episodes,
            base_seed=args.base_seed,
            locked_by=args.locked_by,
            run_mode=args.run_mode,
            horizon_override=args.horizon,
            controller_event_ceiling=args.controller_event_ceiling,
            linearization_mode_id=args.linearization_mode,
        )
        print(json.dumps(result, sort_keys=True))
        return 0 if result["status"] == "complete" else 2

    if args.paired_replicate_probe_command == "summarize":
        summary = paired_replicate_probe.aggregate_small_paired_replicate_probe_results(
            args.artifact_root,
            docs_root=args.docs_root,
        )
        docs = paired_replicate_probe.write_small_paired_replicate_probe_docs(
            artifact_root=args.artifact_root,
            docs_root=args.docs_root,
            command_lines=(
                "uv run python -m big_boy_benchmarking.cli counterpoint "
                "paired-replicate-probe summarize --artifact-root <artifact-root>",
            ),
        )
        print(json.dumps({"status": summary["status"], "docs": docs}, sort_keys=True))
        return 0 if summary["status"] == "complete" else 2

    raise ValueError(
        f"unknown paired-replicate-probe command: {args.paired_replicate_probe_command}"
    )


def _run_counterpoint_threshold_frontier_command(args: argparse.Namespace) -> int:
    if hasattr(args, "linearization_mode"):
        _require_threshold_frontier_linearization(args.linearization_mode)

    if args.threshold_frontier_command == "run":
        result = threshold_frontier_probe.run_threshold_frontier_probe(
            artifact_root=args.artifact_root,
            candidate_readout_source=args.candidate_readout_source,
            instance_id=args.instance_id,
            candidate_cap=args.candidate_cap,
            target_candidate_ids=tuple(args.candidate_id or ()),
            threshold_values=threshold_frontier_probe.parse_threshold_values(args.threshold_values),
            training_replicates_per_arm=args.replicates,
            episodes_per_replicate=args.episodes,
            base_seed=args.base_seed,
            locked_by=args.locked_by,
            horizon_override=args.horizon,
            controller_event_ceiling=args.controller_event_ceiling,
            linearization_mode_id=args.linearization_mode,
        )
        print(json.dumps(result, sort_keys=True))
        return 0 if result["status"] == "complete" else 2

    if args.threshold_frontier_command == "summarize":
        summary = threshold_frontier_probe.aggregate_threshold_frontier_probe_results(
            args.artifact_root,
            docs_root=args.docs_root,
        )
        docs = threshold_frontier_probe.write_threshold_frontier_probe_docs(
            artifact_root=args.artifact_root,
            docs_root=args.docs_root,
            command_lines=(
                "uv run python -m big_boy_benchmarking.cli counterpoint "
                "threshold-frontier summarize --artifact-root <artifact-root>",
            ),
        )
        print(
            json.dumps(
                {
                    "status": summary["status"],
                    "recommended_replicate_probe_threshold": summary.get(
                        "recommended_replicate_probe_threshold"
                    ),
                    "docs": docs,
                },
                sort_keys=True,
            )
        )
        return 0 if summary["status"] == "complete" else 2

    raise ValueError(f"unknown threshold-frontier command: {args.threshold_frontier_command}")


def _require_serious_linearization(linearization_mode_id: str) -> None:
    if linearization_mode_id != "tensor_available_disabled":
        raise ValueError(
            "counterpoint serious-learning uses tensor_available_disabled; "
            f"reserved linearization mode rejected: {linearization_mode_id}"
        )


def _require_one_third_linearization(linearization_mode_id: str) -> None:
    if linearization_mode_id != "tensor_available_disabled":
        raise ValueError(
            "counterpoint one-third diagnostics uses tensor_available_disabled; "
            f"reserved linearization mode rejected: {linearization_mode_id}"
        )


def _require_fraction_sweep_linearization(linearization_mode_id: str) -> None:
    if linearization_mode_id != "tensor_available_disabled":
        raise ValueError(
            "counterpoint fraction sweep diagnostics uses tensor_available_disabled; "
            f"reserved linearization mode rejected: {linearization_mode_id}"
        )


def _require_noisy_rate_linearization(linearization_mode_id: str) -> None:
    if linearization_mode_id != "tensor_available_disabled":
        raise ValueError(
            "counterpoint noisy-rate diagnostics uses tensor_available_disabled; "
            f"reserved linearization mode rejected: {linearization_mode_id}"
        )


def _require_noisy_rate_full_train_linearization(linearization_mode_id: str) -> None:
    if linearization_mode_id != "tensor_available_disabled":
        raise ValueError(
            "counterpoint noisy-rate full-tower training uses tensor_available_disabled; "
            f"reserved linearization mode rejected: {linearization_mode_id}"
        )


def _require_second_serious_linearization(linearization_mode_id: str) -> None:
    if linearization_mode_id != "tensor_available_disabled":
        raise ValueError(
            "counterpoint second-serious-comparison uses tensor_available_disabled; "
            f"reserved linearization mode rejected: {linearization_mode_id}"
        )


def _require_paired_replicate_linearization(linearization_mode_id: str) -> None:
    if linearization_mode_id != "tensor_available_disabled":
        raise ValueError(
            "counterpoint paired-replicate-probe uses tensor_available_disabled; "
            f"reserved linearization mode rejected: {linearization_mode_id}"
        )


def _require_threshold_frontier_linearization(linearization_mode_id: str) -> None:
    if linearization_mode_id != "tensor_available_disabled":
        raise ValueError(
            "counterpoint threshold-frontier uses tensor_available_disabled; "
            f"reserved linearization mode rejected: {linearization_mode_id}"
        )


def _parse_csv_strings(value: str) -> tuple[str, ...]:
    items = tuple(item.strip() for item in value.split(",") if item.strip())
    if not items:
        raise ValueError("expected at least one comma-separated value")
    return items


def _parse_csv_ints(value: str) -> tuple[int, ...]:
    return tuple(int(item) for item in _parse_csv_strings(value))


def main(argv: Sequence[str] | None = None) -> int:
    parser = build_parser()
    args = parser.parse_args(argv)

    if args.command == "validate-contracts":
        return _validate_contracts()

    if args.command == "run-upstream-smoke":
        result = run_upstream_smoke(
            smoke_id=args.smoke_id,
            artifact_root=args.artifact_root,
            mode_id=args.mode_id,
            linearization_mode_id=args.linearization_mode,
            run_id=args.run_id,
            request_readout=True if args.request_readout else None,
        )
        print(json.dumps({"status": result.status, "run_id": result.run_id}, sort_keys=True))
        return 0 if result.status == "success" else 2

    if args.command == "summarize-smoke":
        summary = summarize_upstream_smoke(args.artifact_root, args.run_family_id)
        print(json.dumps(summary, sort_keys=True))
        return 0

    if args.command == "plate-support":
        return _run_plate_support_command(args)

    if args.command == "warehouse-gridlock":
        return _run_warehouse_gridlock_command(args)

    if args.command == "counterpoint":
        return _run_counterpoint_command(args)

    parser.error(f"unknown command: {args.command}")
    return 2
