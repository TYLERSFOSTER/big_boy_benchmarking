"""Matrix, calibration, and budget-locked runners for serious counterpoint learning."""

from __future__ import annotations

import statistics
import time
from dataclasses import dataclass
from pathlib import Path
from typing import Any

from big_boy_benchmarking.artifacts.writers import write_csv, write_json
from big_boy_benchmarking.environments.counterpoint.instances import (
    SMALL_INSTANCE_ID,
    default_small_spec,
    default_tiny_spec,
)
from big_boy_benchmarking.environments.counterpoint.serious_learning.arms import (
    DIRECT_MASKED_RANDOM_ARM_ID,
    DIRECT_TABULAR_Q_ARM_ID,
    REQUIRED_SERIOUS_LEARNING_ARM_IDS,
    SeriousLearningArm,
    iter_serious_learning_arms,
)
from big_boy_benchmarking.environments.counterpoint.serious_learning.budgets import (
    CalibrationBudget,
    SchemaSeedSuite,
    SeedBundleSuite,
    SeriousLearningBudgetLock,
)
from big_boy_benchmarking.environments.counterpoint.serious_learning.direct import (
    run_serious_direct_masked_random,
    run_serious_direct_tabular_q,
)
from big_boy_benchmarking.environments.counterpoint.serious_learning.evaluation_paths import (
    build_serious_learning_evaluation_paths,
)
from big_boy_benchmarking.environments.counterpoint.serious_learning.events import (
    EvaluationRunIndexRow,
)
from big_boy_benchmarking.environments.counterpoint.serious_learning.manifests import (
    CalibrationRecommendation,
    CalibrationSummary,
    SeriousLearningArmManifest,
    SeriousLearningEvaluationManifest,
)
from big_boy_benchmarking.environments.counterpoint.serious_learning.tower_control import (
    run_serious_tower_control,
)
from big_boy_benchmarking.environments.counterpoint.specs import CounterpointInstanceSpec
from big_boy_benchmarking.runners.base import BenchmarkRunResult
from big_boy_benchmarking.seeds.bundles import SeedBundle, generate_seed_bundles


@dataclass(frozen=True)
class SeriousArmRunRecord:
    arm_id: str
    mode_id: str
    schema_id: str | None
    schema_seed: int | None
    seed_bundle: SeedBundle
    result: BenchmarkRunResult | None
    status: str
    failure_reason: str | None = None


def counterpoint_spec_for_instance(instance_id: str) -> CounterpointInstanceSpec:
    if instance_id == "tiny" or instance_id.endswith("_tiny_v001"):
        return default_tiny_spec()
    if instance_id == "small" or instance_id == SMALL_INSTANCE_ID:
        return default_small_spec()
    raise ValueError(f"unknown counterpoint serious-learning instance: {instance_id}")


def dispatch_serious_learning_arm(
    *,
    arm: SeriousLearningArm,
    spec: CounterpointInstanceSpec,
    seed_bundle: SeedBundle,
    artifact_root: Path | str,
    schema_seed: int | None,
    episode_count: int,
    max_steps_per_episode: int,
) -> BenchmarkRunResult:
    if arm.arm_id == DIRECT_MASKED_RANDOM_ARM_ID:
        return run_serious_direct_masked_random(
            spec=spec,
            seed_bundle=seed_bundle,
            artifact_root=artifact_root,
            episode_count=episode_count,
            horizon=max_steps_per_episode,
        )
    if arm.arm_id == DIRECT_TABULAR_Q_ARM_ID:
        return run_serious_direct_tabular_q(
            spec=spec,
            seed_bundle=seed_bundle,
            artifact_root=artifact_root,
            episode_count=episode_count,
            horizon=max_steps_per_episode,
        )
    return run_serious_tower_control(
        spec=spec,
        arm_id=arm.arm_id,
        seed_bundle=seed_bundle,
        artifact_root=artifact_root,
        schema_seed=schema_seed,
        episode_count=episode_count,
        horizon=max_steps_per_episode,
    )


def expand_arm_seed_work(
    *,
    seed_bundles: tuple[SeedBundle, ...],
    schema_seed_suite: SchemaSeedSuite,
) -> tuple[tuple[SeriousLearningArm, SeedBundle, int | None], ...]:
    work: list[tuple[SeriousLearningArm, SeedBundle, int | None]] = []
    for arm in iter_serious_learning_arms():
        for seed_bundle in seed_bundles:
            if arm.requires_schema_seed:
                for schema_seed in schema_seed_suite.schema_seeds:
                    work.append((arm, seed_bundle, schema_seed))
            else:
                work.append((arm, seed_bundle, None))
    return tuple(work)


def run_calibration(
    *,
    artifact_root: Path | str,
    budget: CalibrationBudget,
    base_seed: int = 0,
) -> dict[str, Any]:
    if "tiny" in budget.environment_instance_id and not budget.smoke:
        raise ValueError("tiny calibration must be explicitly marked smoke")
    spec = counterpoint_spec_for_instance(budget.environment_instance_id)
    paths = build_serious_learning_evaluation_paths(artifact_root)
    paths.root.mkdir(parents=True, exist_ok=True)
    paths.results_dir.mkdir(parents=True, exist_ok=True)
    paths.docs_dir.mkdir(parents=True, exist_ok=True)
    write_json(paths.evaluation_manifest, SeriousLearningEvaluationManifest().to_dict())
    write_json(paths.evaluation_arm_manifest, SeriousLearningArmManifest().to_dict())

    seed_bundles = generate_seed_bundles(
        base_seed=base_seed,
        replicate_count=budget.replicate_count,
    )
    schema_seed_suite = SchemaSeedSuite(tuple(range(budget.random_schema_seed_count)))
    started = time.perf_counter()
    records = _run_work_items(
        spec=spec,
        artifact_root=artifact_root,
        work_items=expand_arm_seed_work(
            seed_bundles=seed_bundles,
            schema_seed_suite=schema_seed_suite,
        ),
        episode_count=budget.episode_count,
        max_steps_per_episode=budget.max_steps_per_episode,
    )
    elapsed = time.perf_counter() - started
    run_index_rows = [
        _run_index_row(paths.root, record).to_flat_dict() for record in records
    ]
    write_csv(
        paths.calibration_run_index_csv,
        run_index_rows,
        EvaluationRunIndexRow.fieldnames(),
    )
    artifact_bytes = _artifact_bytes(Path(artifact_root))
    returns = _read_mean_returns(records)
    completion_rate = _status_rate(records, "success")
    summary = CalibrationSummary(
        evaluation_id="counterpoint_first_serious_learning_v001",
        status="smoke_non_evidence" if budget.smoke else "complete",
        arm_count=len(REQUIRED_SERIOUS_LEARNING_ARM_IDS),
        run_count=len(records),
        measured_runtime_seconds=elapsed,
        artifact_bytes=artifact_bytes,
        curve_noise_proxy=statistics.pstdev(returns) if len(returns) > 1 else None,
        completion_rate=completion_rate,
        lift_failure_rate=_lift_failure_rate(records),
        random_schema_variability=None,
    )
    recommendation = CalibrationRecommendation(
        evaluation_id=summary.evaluation_id,
        measured_summary=summary,
        proposed_episode_count=max(2, budget.episode_count * 2),
        proposed_replicate_count=max(2, budget.replicate_count),
        proposed_random_schema_seed_count=max(2, budget.random_schema_seed_count),
        rationale=(
            "Recommendation is based on measured calibration runtime, artifact volume, "
            "completion status, and available return variability."
        ),
    )
    write_json(paths.calibration_summary, summary.to_dict())
    paths.calibration_recommendation_md.write_text(
        "\n".join(
            [
                "# Calibration Recommendation",
                "",
                f"Status: {summary.status}",
                f"Measured runtime seconds: {summary.measured_runtime_seconds:.6f}",
                f"Artifact bytes: {summary.artifact_bytes}",
                f"Runs represented: {summary.run_count}",
                "",
                "Proposed locked budget:",
                "",
                f"- episodes: {recommendation.proposed_episode_count}",
                f"- replicates: {recommendation.proposed_replicate_count}",
                f"- random schema seeds: {recommendation.proposed_random_schema_seed_count}",
                "",
                recommendation.rationale,
                "",
            ]
        ),
        encoding="utf-8",
    )
    return {
        "status": summary.status,
        "artifact_root": str(artifact_root),
        "run_count": len(records),
        "arm_count": len(REQUIRED_SERIOUS_LEARNING_ARM_IDS),
        "calibration_summary": str(paths.calibration_summary),
        "calibration_recommendation": str(paths.calibration_recommendation_md),
    }


def run_budget_locked_serious_learning(
    *,
    artifact_root: Path | str,
    budget_lock: SeriousLearningBudgetLock,
    seed_bundle_suite: SeedBundleSuite,
) -> dict[str, Any]:
    if tuple(seed_bundle_suite.seed_bundle_ids) != tuple(budget_lock.seed_bundle_ids):
        raise ValueError("seed bundle suite ids must match the budget lock")
    spec = counterpoint_spec_for_instance(budget_lock.environment_instance_id)
    paths = build_serious_learning_evaluation_paths(artifact_root)
    paths.root.mkdir(parents=True, exist_ok=True)
    write_json(paths.evaluation_budget_lock, budget_lock.to_dict())
    records = _run_work_items(
        spec=spec,
        artifact_root=artifact_root,
        work_items=expand_arm_seed_work(
            seed_bundles=seed_bundle_suite.seed_bundles,
            schema_seed_suite=budget_lock.schema_seed_suite,
        ),
        episode_count=budget_lock.episode_count,
        max_steps_per_episode=budget_lock.max_steps_per_episode,
    )
    write_csv(
        paths.evaluation_run_index_csv,
        [_run_index_row(paths.root, record).to_flat_dict() for record in records],
        EvaluationRunIndexRow.fieldnames(),
    )
    status = "complete" if all(record.status == "success" for record in records) else "incomplete"
    return {
        "status": status,
        "run_count": len(records),
        "evaluation_run_index": str(paths.evaluation_run_index_csv),
        "evaluation_budget_lock": str(paths.evaluation_budget_lock),
    }


def _run_work_items(
    *,
    spec: CounterpointInstanceSpec,
    artifact_root: Path | str,
    work_items: tuple[tuple[SeriousLearningArm, SeedBundle, int | None], ...],
    episode_count: int,
    max_steps_per_episode: int,
) -> tuple[SeriousArmRunRecord, ...]:
    records: list[SeriousArmRunRecord] = []
    for arm, seed_bundle, schema_seed in work_items:
        try:
            result = dispatch_serious_learning_arm(
                arm=arm,
                spec=spec,
                seed_bundle=seed_bundle,
                artifact_root=artifact_root,
                schema_seed=schema_seed,
                episode_count=episode_count,
                max_steps_per_episode=max_steps_per_episode,
            )
            records.append(
                SeriousArmRunRecord(
                    arm_id=arm.arm_id,
                    mode_id=arm.mode_id,
                    schema_id=arm.schema_id,
                    schema_seed=schema_seed,
                    seed_bundle=seed_bundle,
                    result=result,
                    status=result.status,
                )
            )
        except Exception as exc:  # pragma: no cover - matrix failure recording boundary
            records.append(
                SeriousArmRunRecord(
                    arm_id=arm.arm_id,
                    mode_id=arm.mode_id,
                    schema_id=arm.schema_id,
                    schema_seed=schema_seed,
                    seed_bundle=seed_bundle,
                    result=None,
                    status="failed",
                    failure_reason=f"{type(exc).__name__}: {exc}",
                )
            )
    return tuple(records)


def _run_index_row(root: Path, record: SeriousArmRunRecord) -> EvaluationRunIndexRow:
    result = record.result
    return EvaluationRunIndexRow(
        evaluation_id="counterpoint_first_serious_learning_v001",
        run_id="" if result is None else result.run_id,
        arm_id=record.arm_id,
        mode_id=record.mode_id,
        schema_id=record.schema_id,
        schema_seed=record.schema_seed,
        seed_bundle_id=record.seed_bundle.seed_bundle_id,
        replicate_index=record.seed_bundle.replicate_index,
        status=record.status,
        artifact_root=str(root),
        started_at="" if result is None else result.started_at,
        ended_at=None if result is None else result.ended_at,
    )


def _artifact_bytes(root: Path) -> int:
    if not root.exists():
        return 0
    return sum(path.stat().st_size for path in root.rglob("*") if path.is_file())


def _read_mean_returns(records: tuple[SeriousArmRunRecord, ...]) -> list[float]:
    values: list[float] = []
    for record in records:
        if record.result is None or record.result.summary_path is None:
            continue
        try:
            import json

            payload = json.loads(Path(record.result.summary_path).read_text())
            values.append(float(payload.get("mean_return", 0.0)))
        except Exception:
            continue
    return values


def _status_rate(records: tuple[SeriousArmRunRecord, ...], status: str) -> float:
    if not records:
        return 0.0
    return sum(1 for record in records if record.status == status) / len(records)


def _lift_failure_rate(records: tuple[SeriousArmRunRecord, ...]) -> float | None:
    total = 0
    failures = 0
    for record in records:
        path_text = None if record.result is None else record.result.artifact_paths.get(
            "lift_fiber_events_csv"
        )
        if path_text is None:
            continue
        path = Path(path_text)
        if not path.exists():
            continue
        import csv

        for row in csv.DictReader(path.open()):
            total += 1
            failures += 0 if row.get("success") == "True" else 1
    if total == 0:
        return None
    return failures / total
