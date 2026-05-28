"""Runner surfaces for counterpoint benchmark modes."""

from __future__ import annotations

import random
from dataclasses import dataclass
from datetime import UTC, datetime
from pathlib import Path
from typing import Any

from big_boy_benchmarking.artifacts.manifests import (
    DependencyManifest,
    EnvironmentFamilyManifest,
    ExternalArtifactsManifest,
    FamilyManifest,
    ModeManifest,
    RunManifest,
)
from big_boy_benchmarking.artifacts.paths import build_run_family_paths, build_run_paths
from big_boy_benchmarking.artifacts.schemas import ARTIFACT_SCHEMA_VERSION
from big_boy_benchmarking.artifacts.writers import (
    append_csv_row,
    append_jsonl,
    ensure_artifact_dirs,
    write_csv,
    write_json,
)
from big_boy_benchmarking.environments.counterpoint import ids
from big_boy_benchmarking.environments.counterpoint.actions import CounterpointAction
from big_boy_benchmarking.environments.counterpoint.artifacts import (
    action_mask_manifest,
    edge_label_manifest,
    environment_instance_manifest,
    legality_manifest,
    reward_bundle_manifest,
)
from big_boy_benchmarking.environments.counterpoint.diagnostics import (
    balanced_addressability_diagnostics,
    lift_fiber_diagnostics,
    reward_fiber_diagnostics,
)
from big_boy_benchmarking.environments.counterpoint.instances import initial_states
from big_boy_benchmarking.environments.counterpoint.masks import legal_action_mask
from big_boy_benchmarking.environments.counterpoint.schemas import (
    SchemaConstruction,
    build_schema_for_id,
)
from big_boy_benchmarking.environments.counterpoint.specs import CounterpointInstanceSpec
from big_boy_benchmarking.environments.counterpoint.state import CounterpointState
from big_boy_benchmarking.environments.counterpoint.tower_adapter import (
    build_counterpoint_partition_tower,
)
from big_boy_benchmarking.environments.counterpoint.transition import evaluate_transition
from big_boy_benchmarking.metrics.events import (
    EpisodeRow,
    RunIndexRow,
    StepEventRow,
)
from big_boy_benchmarking.metrics.timing import TimingRecorder, summarize_timing_segments
from big_boy_benchmarking.modes.registry import require_runnable_mode
from big_boy_benchmarking.runners.base import BenchmarkRunResult
from big_boy_benchmarking.seeds.bundles import SeedBundle
from big_boy_benchmarking.upstream.state_collapser import (
    collect_state_collapser_dependency_state,
)

DIRECT_RUN_FAMILY_ID = "counterpoint_symbolic_v001_direct_v001"
TOWER_RUN_FAMILY_ID = "counterpoint_symbolic_v001_tower_smoke_v001"
MASKED_RANDOM_POLICY_ID = "masked_random_policy_v001"
TABULAR_Q_POLICY_ID = "tabular_q_masked_v001"


@dataclass(frozen=True)
class _StepTrace:
    step_index: int
    action: CounterpointAction
    reward: float
    terminated: bool
    truncated: bool
    next_state: CounterpointState


@dataclass(frozen=True)
class _EpisodeTrace:
    episode_index: int
    total_reward: float
    steps: tuple[_StepTrace, ...]
    terminated: bool
    truncated: bool


def _now() -> str:
    return datetime.now(UTC).isoformat()


def _artifact_path_dict(run_paths: Any) -> dict[str, str]:
    return {
        "run_manifest": str(run_paths.run_manifest),
        "seed_bundle": str(run_paths.seed_bundle),
        "mode_manifest": str(run_paths.mode_manifest),
        "timing_summary": str(run_paths.timing_summary),
        "episodes_csv": str(run_paths.episodes_csv),
        "step_events_csv": str(run_paths.step_events_csv),
        "timing_segments_csv": str(run_paths.timing_segments_csv),
        "external_artifacts": str(run_paths.external_artifacts),
    }


def _state_key(state: CounterpointState) -> tuple[tuple[int, ...], int]:
    return (state.pitches, state.beat_index)


def _action_key(action: CounterpointAction) -> tuple[int, ...]:
    return action.deltas


def _choose_start_state(
    spec: CounterpointInstanceSpec,
    rng: random.Random,
) -> CounterpointState:
    starts = initial_states(spec)
    if not starts:
        raise ValueError("initial_state_policy produced no legal start states")
    return rng.choice(starts)


def _choose_random_legal_action(
    spec: CounterpointInstanceSpec,
    state: CounterpointState,
    rng: random.Random,
) -> CounterpointAction | None:
    actions = legal_action_mask(spec, state).legal_actions()
    if not actions:
        return None
    return rng.choice(actions)


def _choose_tabular_q_action(
    spec: CounterpointInstanceSpec,
    state: CounterpointState,
    rng: random.Random,
    q_values: dict[tuple[tuple[tuple[int, ...], int], tuple[int, ...]], float],
    *,
    epsilon: float,
) -> CounterpointAction | None:
    actions = legal_action_mask(spec, state).legal_actions()
    if not actions:
        return None
    if rng.random() < epsilon:
        return rng.choice(actions)
    state_key = _state_key(state)
    return max(
        actions,
        key=lambda action: (q_values.get((state_key, _action_key(action)), 0.0), action.deltas),
    )


def _run_masked_random_episode(
    spec: CounterpointInstanceSpec,
    *,
    episode_index: int,
    seed_bundle: SeedBundle,
    horizon: int,
    recorder: TimingRecorder,
) -> _EpisodeTrace:
    rng = random.Random(
        f"{seed_bundle.environment_seed}:{seed_bundle.learner_seed}:{episode_index}"
    )
    with recorder.segment("environment_reset"):
        state = _choose_start_state(spec, rng)
    steps: list[_StepTrace] = []
    total_reward = 0.0
    terminated = False
    truncated = False
    for step_index in range(horizon):
        with recorder.segment("learner_act"):
            action = _choose_random_legal_action(spec, state, rng)
        if action is None:
            truncated = True
            break
        with recorder.segment("environment_step"):
            transition = evaluate_transition(spec, state, action, step_index=step_index)
        reward = 0.0 if transition.reward is None else transition.reward.total_reward
        total_reward += reward
        state = transition.next_state
        terminated = transition.terminated
        truncated = transition.truncated
        steps.append(
            _StepTrace(
                step_index=step_index,
                action=action,
                reward=reward,
                terminated=terminated,
                truncated=truncated,
                next_state=state,
            )
        )
        if terminated or truncated:
            break
    return _EpisodeTrace(
        episode_index=episode_index,
        total_reward=total_reward,
        steps=tuple(steps),
        terminated=terminated,
        truncated=truncated,
    )


def _run_tabular_q_episode(
    spec: CounterpointInstanceSpec,
    *,
    episode_index: int,
    seed_bundle: SeedBundle,
    horizon: int,
    recorder: TimingRecorder,
    q_values: dict[tuple[tuple[tuple[int, ...], int], tuple[int, ...]], float],
    alpha: float,
    gamma: float,
    epsilon: float,
) -> _EpisodeTrace:
    rng = random.Random(
        f"{seed_bundle.environment_seed}:{seed_bundle.learner_seed}:{episode_index}"
    )
    with recorder.segment("environment_reset"):
        state = _choose_start_state(spec, rng)
    steps: list[_StepTrace] = []
    total_reward = 0.0
    terminated = False
    truncated = False
    for step_index in range(horizon):
        with recorder.segment("learner_act"):
            action = _choose_tabular_q_action(
                spec,
                state,
                rng,
                q_values,
                epsilon=epsilon,
            )
        if action is None:
            truncated = True
            break
        with recorder.segment("environment_step"):
            transition = evaluate_transition(spec, state, action, step_index=step_index)
        reward = 0.0 if transition.reward is None else transition.reward.total_reward
        state_action_key = (_state_key(state), _action_key(action))
        next_actions = legal_action_mask(spec, transition.next_state).legal_actions()
        next_state_key = _state_key(transition.next_state)
        best_next = (
            max(
                q_values.get((next_state_key, _action_key(next_action)), 0.0)
                for next_action in next_actions
            )
            if next_actions and not transition.terminated
            else 0.0
        )
        with recorder.segment("learner_update"):
            old_value = q_values.get(state_action_key, 0.0)
            q_values[state_action_key] = old_value + alpha * (
                reward + gamma * best_next - old_value
            )
        total_reward += reward
        state = transition.next_state
        terminated = transition.terminated
        truncated = transition.truncated
        steps.append(
            _StepTrace(
                step_index=step_index,
                action=action,
                reward=reward,
                terminated=terminated,
                truncated=truncated,
                next_state=state,
            )
        )
        if terminated or truncated:
            break
    return _EpisodeTrace(
        episode_index=episode_index,
        total_reward=total_reward,
        steps=tuple(steps),
        terminated=terminated,
        truncated=truncated,
    )


def _write_direct_run_artifacts(
    *,
    spec: CounterpointInstanceSpec,
    artifact_root: Path | str,
    run_family_id: str,
    run_id: str,
    mode_id: str,
    policy_id: str,
    seed_bundle: SeedBundle,
    budget: dict[str, Any],
    recorder: TimingRecorder,
    episodes: tuple[_EpisodeTrace, ...],
    command: str,
) -> BenchmarkRunResult:
    started_at = _now()
    family_paths = build_run_family_paths(artifact_root, run_family_id)
    run_paths = build_run_paths(artifact_root, run_family_id, run_id)
    ensure_artifact_dirs(family_paths, run_paths)
    mode_contract = require_runnable_mode(mode_id)
    dependency_state = collect_state_collapser_dependency_state(
        dependency_spec="state-collapser[rl] @ git+https://github.com/TYLERSFOSTER/state_collapser.git@v0.6.0"
    )

    write_json(
        family_paths.family_manifest,
        FamilyManifest(
            run_family_id=run_family_id,
            description="Counterpoint symbolic direct-environment benchmark smoke family.",
        ).to_dict(),
        create_parents=True,
    )
    write_json(
        family_paths.environment_family_manifest,
        EnvironmentFamilyManifest(
            environment_family_id=ids.ENVIRONMENT_FAMILY_ID,
            environment_ids=(spec.environment_instance_id,),
            description="Counterpoint hidden graph benchmark family.",
        ).to_dict(),
        create_parents=True,
    )
    write_json(
        family_paths.dependency_manifest,
        DependencyManifest(
            state_collapser=dependency_state.to_dict(),
            repo_state={"bbb_repo": "/Users/foster/big_boy_benchmarking"},
        ).to_dict(),
        create_parents=True,
    )
    write_json(run_paths.seed_bundle, seed_bundle.to_dict(), create_parents=True)
    write_json(
        run_paths.external_artifacts,
        ExternalArtifactsManifest(
            run_id=run_id,
            artifacts=(
                {
                    "artifact_id": "counterpoint_environment_instance_manifest",
                    "kind": "environment_contract",
                },
            ),
        ).to_dict(),
        create_parents=True,
    )
    write_json(
        run_paths.root / "environment_instance_manifest.json",
        environment_instance_manifest(spec),
        create_parents=True,
    )
    write_json(run_paths.root / "legality_manifest.json", legality_manifest(spec))
    write_json(run_paths.root / "reward_bundle_manifest.json", reward_bundle_manifest(spec))
    write_json(run_paths.root / "edge_label_manifest.json", edge_label_manifest(spec))
    write_json(run_paths.root / "action_mask_manifest.json", action_mask_manifest(spec))

    for episode in episodes:
        episode_row = EpisodeRow(
            run_id=run_id,
            episode_index=episode.episode_index,
            seed_bundle_id=seed_bundle.seed_bundle_id,
            total_reward=episode.total_reward,
            step_count=len(episode.steps),
            terminated=episode.terminated,
            truncated=episode.truncated,
        )
        append_csv_row(
            run_paths.episodes_csv,
            episode_row.to_flat_dict(),
            EpisodeRow.fieldnames(),
            create_parents=True,
        )
        for step in episode.steps:
            step_row = StepEventRow(
                run_id=run_id,
                episode_index=episode.episode_index,
                step_index=step.step_index,
                action=str(step.action.deltas),
                reward=step.reward,
                terminated=step.terminated,
                truncated=step.truncated,
            )
            append_csv_row(
                run_paths.step_events_csv,
                step_row.to_flat_dict(),
                StepEventRow.fieldnames(),
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
    write_json(
        run_paths.mode_manifest,
        ModeManifest(
            mode_id=mode_id,
            readout_requested=False,
            morphism_requested=False,
            uses_compatibility_readout=False,
            uses_morphism=False,
            mode_contract=mode_contract.to_dict(),
        ).to_dict(),
        create_parents=True,
    )
    ended_at = _now()
    write_json(
        run_paths.run_manifest,
        RunManifest(
            run_id=run_id,
            run_family_id=run_family_id,
            environment_id=spec.environment_instance_id,
            mode_id=mode_id,
            schema_id=mode_contract.schema_mode,
            learner_id=mode_contract.learner_id,
            controller_id=mode_contract.controller_regime,
            seed_bundle_id=seed_bundle.seed_bundle_id,
            budget=budget,
            diagnostic_profile=mode_contract.diagnostic_profile.profile_id,
            timing_profile=mode_contract.timing_profile.profile_id,
            command=command,
            status="success",
        ).to_dict(),
        create_parents=True,
    )
    append_jsonl(
        family_paths.run_index,
        RunIndexRow(
            run_family_id=run_family_id,
            run_id=run_id,
            environment_id=spec.environment_instance_id,
            mode_id=mode_id,
            status="success",
            started_at=started_at,
            ended_at=ended_at,
            artifact_schema_version=ARTIFACT_SCHEMA_VERSION,
        ).to_flat_dict(),
        create_parents=True,
    )
    run_paths.warnings_jsonl.touch()
    summary = {
        "run_family_id": run_family_id,
        "run_id": run_id,
        "environment_instance_id": spec.environment_instance_id,
        "mode_id": mode_id,
        "policy_id": policy_id,
        "episode_count": len(episodes),
        "mean_return": (
            sum(episode.total_reward for episode in episodes) / len(episodes)
            if episodes
            else 0.0
        ),
        "artifact_schema_version": ARTIFACT_SCHEMA_VERSION,
    }
    write_json(family_paths.summary_json, summary, create_parents=True)
    return BenchmarkRunResult(
        run_id=run_id,
        status="success",
        artifact_paths=_artifact_path_dict(run_paths),
        summary_path=str(family_paths.summary_json),
        warning_count=0,
        started_at=started_at,
        ended_at=ended_at,
        failure_reason=None,
    )


def run_direct_masked_random(
    *,
    spec: CounterpointInstanceSpec,
    seed_bundle: SeedBundle,
    artifact_root: Path | str,
    horizon: int | None = None,
    episode_count: int = 1,
    policy_id: str = MASKED_RANDOM_POLICY_ID,
    run_family_id: str = DIRECT_RUN_FAMILY_ID,
    run_id: str | None = None,
) -> BenchmarkRunResult:
    active_horizon = spec.horizon_steps if horizon is None else horizon
    if active_horizon <= 0:
        raise ValueError("horizon must be positive")
    if episode_count <= 0:
        raise ValueError("episode_count must be positive")
    run_id = run_id or (
        f"{spec.environment_instance_id}-direct-masked-random-{seed_bundle.replicate_index}"
    )
    recorder = TimingRecorder.create(run_id)
    episodes = tuple(
        _run_masked_random_episode(
            spec,
            episode_index=episode_index,
            seed_bundle=seed_bundle,
            horizon=active_horizon,
            recorder=recorder,
        )
        for episode_index in range(episode_count)
    )
    return _write_direct_run_artifacts(
        spec=spec,
        artifact_root=artifact_root,
        run_family_id=run_family_id,
        run_id=run_id,
        mode_id="direct_env_masked_random",
        policy_id=policy_id,
        seed_bundle=seed_bundle,
        budget={"episodes": episode_count, "horizon": active_horizon},
        recorder=recorder,
        episodes=episodes,
        command="python -m big_boy_benchmarking.cli counterpoint run-direct",
    )


def run_direct_tabular_q(
    *,
    spec: CounterpointInstanceSpec,
    seed_bundle: SeedBundle,
    artifact_root: Path | str,
    horizon: int | None = None,
    episode_count: int = 4,
    policy_id: str = TABULAR_Q_POLICY_ID,
    run_family_id: str = DIRECT_RUN_FAMILY_ID,
    run_id: str | None = None,
    alpha: float = 0.4,
    gamma: float = 0.9,
    epsilon: float = 0.2,
) -> BenchmarkRunResult:
    active_horizon = spec.horizon_steps if horizon is None else horizon
    if active_horizon <= 0:
        raise ValueError("horizon must be positive")
    if episode_count <= 0:
        raise ValueError("episode_count must be positive")
    q_values: dict[tuple[tuple[tuple[int, ...], int], tuple[int, ...]], float] = {}
    run_id = run_id or (
        f"{spec.environment_instance_id}-direct-tabular-q-{seed_bundle.replicate_index}"
    )
    recorder = TimingRecorder.create(run_id)
    episodes = tuple(
        _run_tabular_q_episode(
            spec,
            episode_index=episode_index,
            seed_bundle=seed_bundle,
            horizon=active_horizon,
            recorder=recorder,
            q_values=q_values,
            alpha=alpha,
            gamma=gamma,
            epsilon=epsilon,
        )
        for episode_index in range(episode_count)
    )
    return _write_direct_run_artifacts(
        spec=spec,
        artifact_root=artifact_root,
        run_family_id=run_family_id,
        run_id=run_id,
        mode_id="direct_env_tabular",
        policy_id=policy_id,
        seed_bundle=seed_bundle,
        budget={
            "episodes": episode_count,
            "horizon": active_horizon,
            "alpha": alpha,
            "gamma": gamma,
            "epsilon": epsilon,
        },
        recorder=recorder,
        episodes=episodes,
        command="python -m big_boy_benchmarking.cli counterpoint run-direct",
    )


def _schema_construction_for_id(
    graph: Any,
    *,
    schema_id: str,
    schema_seed: int | None,
) -> SchemaConstruction:
    return build_schema_for_id(graph, schema_id=schema_id, schema_seed=schema_seed)


def _tower_mode_for_schema(schema_id: str) -> str:
    return (
        "tower_empty_schema_tabular"
        if schema_id == ids.EMPTY_SCHEMA_ID
        else "tower_nonempty_schema_tabular"
    )


def run_tower_schema_smoke(
    *,
    spec: CounterpointInstanceSpec,
    schema_id: str,
    seed_bundle: SeedBundle,
    artifact_root: Path | str,
    schema_seed: int | None = None,
    run_family_id: str = TOWER_RUN_FAMILY_ID,
    run_id: str | None = None,
) -> BenchmarkRunResult:
    """Build a partition tower for the exact tiny graph without compatibility readouts."""

    started_at = _now()
    active_schema_seed = seed_bundle.schema_seed if schema_seed is None else schema_seed
    mode_id = _tower_mode_for_schema(schema_id)
    run_id = run_id or f"{spec.environment_instance_id}-{schema_id}-{seed_bundle.replicate_index}"
    family_paths = build_run_family_paths(artifact_root, run_family_id)
    run_paths = build_run_paths(artifact_root, run_family_id, run_id)
    ensure_artifact_dirs(family_paths, run_paths)
    mode_contract = require_runnable_mode(mode_id)
    recorder = TimingRecorder.create(run_id)
    dependency_state = collect_state_collapser_dependency_state(
        dependency_spec="state-collapser[rl] @ git+https://github.com/TYLERSFOSTER/state_collapser.git@v0.6.0"
    )

    with recorder.segment("tower_reset"):
        build = build_counterpoint_partition_tower(
            spec,
            schema_id=schema_id,
            schema_seed=active_schema_seed,
        )
    schema = _schema_construction_for_id(
        build.graph,
        schema_id=schema_id,
        schema_seed=active_schema_seed,
    )
    reward_rows = [row.to_dict() for row in reward_fiber_diagnostics(build.graph, schema)]
    lift_rows = [row.to_dict() for row in lift_fiber_diagnostics(schema)]
    addressability = balanced_addressability_diagnostics(schema)

    write_json(
        family_paths.family_manifest,
        FamilyManifest(
            run_family_id=run_family_id,
            description="Counterpoint symbolic tower smoke family.",
        ).to_dict(),
        create_parents=True,
    )
    write_json(
        family_paths.environment_family_manifest,
        EnvironmentFamilyManifest(
            environment_family_id=ids.ENVIRONMENT_FAMILY_ID,
            environment_ids=(spec.environment_instance_id,),
            description="Counterpoint hidden graph benchmark family.",
        ).to_dict(),
        create_parents=True,
    )
    write_json(
        family_paths.dependency_manifest,
        DependencyManifest(
            state_collapser=dependency_state.to_dict(),
            repo_state={"bbb_repo": "/Users/foster/big_boy_benchmarking"},
        ).to_dict(),
        create_parents=True,
    )
    write_json(run_paths.seed_bundle, seed_bundle.to_dict(), create_parents=True)
    write_json(
        run_paths.root / "schema_manifest.json",
        schema.spec.to_dict(),
        create_parents=True,
    )
    write_json(
        run_paths.root / "quotient_summary.json",
        {
            "schema_id": schema.spec.schema_id,
            "partition_tier_count": len(build.tower.state_layers),
            "state_cell_count_by_tier": [
                len(layer.all_cell_ids()) for layer in build.tower.state_layers
            ],
            "edge_count": len(build.graph.edges),
        },
        create_parents=True,
    )
    append_jsonl(
        run_paths.structural_diagnostics_jsonl,
        {
            "schema_id": schema.spec.schema_id,
            "diagnostic_name": "balanced_addressability",
            "value": addressability.to_dict(),
        },
        create_parents=True,
    )
    write_csv(
        run_paths.root / "reward_fiber_variance.csv",
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
        create_parents=True,
    )
    write_csv(
        run_paths.root / "lift_fiber_summary.csv",
        lift_rows,
        [
            "cell_id",
            "fine_candidate_count",
            "entropy",
            "valid_lift_count",
            "failed_lift_count",
            "failed_lift_reason_counts",
        ],
        create_parents=True,
    )
    for row in reward_rows:
        append_jsonl(
            run_paths.root / "reward_term_diagnostics.jsonl",
            {
                "schema_id": row["schema_id"],
                "cell_id": row["cell_id"],
                "term_variance": row["term_variance"],
            },
            create_parents=True,
        )
    for row in lift_rows:
        append_jsonl(
            run_paths.root / "lift_attempts.jsonl",
            {
                "cell_id": row["cell_id"],
                "valid_lift_count": row["valid_lift_count"],
                "failed_lift_count": row["failed_lift_count"],
            },
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
    write_json(
        run_paths.mode_manifest,
        ModeManifest(
            mode_id=mode_id,
            readout_requested=False,
            morphism_requested=False,
            uses_compatibility_readout=False,
            uses_morphism=False,
            mode_contract=mode_contract.to_dict(),
        ).to_dict(),
        create_parents=True,
    )
    ended_at = _now()
    write_json(
        run_paths.run_manifest,
        RunManifest(
            run_id=run_id,
            run_family_id=run_family_id,
            environment_id=spec.environment_instance_id,
            mode_id=mode_id,
            schema_id=schema.spec.schema_id,
            learner_id=mode_contract.learner_id,
            controller_id=mode_contract.controller_regime,
            seed_bundle_id=seed_bundle.seed_bundle_id,
            budget={"tower_smoke": True, "schema_seed": active_schema_seed},
            diagnostic_profile=mode_contract.diagnostic_profile.profile_id,
            timing_profile=mode_contract.timing_profile.profile_id,
            command="python -m big_boy_benchmarking.cli counterpoint tower-smoke",
            status="success",
        ).to_dict(),
        create_parents=True,
    )
    append_jsonl(
        family_paths.run_index,
        RunIndexRow(
            run_family_id=run_family_id,
            run_id=run_id,
            environment_id=spec.environment_instance_id,
            mode_id=mode_id,
            status="success",
            started_at=started_at,
            ended_at=ended_at,
            artifact_schema_version=ARTIFACT_SCHEMA_VERSION,
        ).to_flat_dict(),
        create_parents=True,
    )
    run_paths.warnings_jsonl.touch()
    write_json(
        run_paths.external_artifacts,
        ExternalArtifactsManifest(run_id=run_id).to_dict(),
        create_parents=True,
    )
    summary = {
        "run_family_id": run_family_id,
        "run_id": run_id,
        "environment_instance_id": spec.environment_instance_id,
        "mode_id": mode_id,
        "schema_id": schema.spec.schema_id,
        "partition_tier_count": len(build.tower.state_layers),
        "uses_compatibility_readout": False,
        "artifact_schema_version": ARTIFACT_SCHEMA_VERSION,
    }
    write_json(family_paths.summary_json, summary, create_parents=True)
    return BenchmarkRunResult(
        run_id=run_id,
        status="success",
        artifact_paths={
            **_artifact_path_dict(run_paths),
            "schema_manifest": str(run_paths.root / "schema_manifest.json"),
            "quotient_summary": str(run_paths.root / "quotient_summary.json"),
            "reward_fiber_variance": str(run_paths.root / "reward_fiber_variance.csv"),
            "lift_fiber_summary": str(run_paths.root / "lift_fiber_summary.csv"),
        },
        summary_path=str(family_paths.summary_json),
        warning_count=0,
        started_at=started_at,
        ended_at=ended_at,
        failure_reason=None,
    )
