"""A first trainable full-state/full-action Warehouse policy."""

from __future__ import annotations

import math
import random
from dataclasses import dataclass, field
from typing import Any

from big_boy_benchmarking.environments.warehouse_gridlock.actions import DirectionOrStay
from big_boy_benchmarking.environments.warehouse_gridlock.policies.contracts import (
    WarehouseFullActionVector,
    WarehouseFullSystemConfig,
    WarehouseMaskContext,
    WarehousePolicyDecision,
    WarehousePolicyRng,
    WarehousePolicyTransition,
    WarehousePolicyUpdate,
)
from big_boy_benchmarking.environments.warehouse_gridlock.policies.features import (
    command_features,
    score_features,
)
from big_boy_benchmarking.environments.warehouse_gridlock.policies.serialization import (
    policy_state_hash,
)

MODEL_FAMILY_ID = "warehouse_linear_factorized_softmax_policy_v001"
COMMANDS = (
    DirectionOrStay.NORTH,
    DirectionOrStay.SOUTH,
    DirectionOrStay.EAST,
    DirectionOrStay.WEST,
    DirectionOrStay.STAY,
)


@dataclass
class WarehouseLinearFactorizedSoftmaxPolicy:
    policy_id: str
    learning_rate: float = 0.01
    baseline_rate: float = 0.05
    temperature_initial: float = 1.0
    temperature_floor: float = 0.1
    temperature_decay_per_episode: float = 0.995
    model_family_id: str = MODEL_FAMILY_ID
    weights: dict[str, float] = field(default_factory=dict)
    baseline: float = 0.0
    update_count: int = 0

    @property
    def state_hash(self) -> str:
        return policy_state_hash(
            weights=self.weights,
            baseline=self.baseline,
            update_count=self.update_count,
        )

    def act(
        self,
        *,
        full_system_config: WarehouseFullSystemConfig,
        second: int,
        rng: WarehousePolicyRng,
        mask_context: WarehouseMaskContext,
        tier: int | None = None,
        tier_state_id: str | None = None,
    ) -> WarehousePolicyDecision:
        random_source = random.Random(
            f"{rng.seed}:{self.policy_id}:{mask_context.episode_index}:{mask_context.step_index}:{tier}"
        )
        commands: dict[str, DirectionOrStay] = {}
        margins: dict[str, float] = {}
        prior_signal_used = False
        selected_scores: list[float] = []
        for robot_id in full_system_config.static.robot_ids:
            scores = {
                command: score_features(
                    self.weights,
                    command_features(
                        config=full_system_config,
                        robot_id=robot_id,
                        command=command,
                        second=second,
                    ),
                )
                for command in COMMANDS
            }
            if any(abs(value) > 1.0e-12 for value in scores.values()):
                prior_signal_used = True
            command = _sample_command(
                scores=scores,
                temperature=self._temperature(mask_context.episode_index),
                random_source=random_source,
            )
            commands[robot_id] = command
            selected_scores.append(scores[command])
            margins[robot_id] = _score_margin(scores, command)
        return WarehousePolicyDecision(
            policy_id=self.policy_id,
            model_family_id=self.model_family_id,
            second=second,
            raw_action_vector=WarehouseFullActionVector(commands=commands),
            selected_action_vector=None,
            raw_valid=False,
            selected_valid=False,
            projection_trace=None,
            prior_signal_used=prior_signal_used,
            decision_score_summary={
                "mean_selected_score": (
                    sum(selected_scores) / len(selected_scores) if selected_scores else 0.0
                ),
                "nonzero_weight_count": sum(1 for value in self.weights.values() if abs(value) > 1.0e-12),
                "temperature": self._temperature(mask_context.episode_index),
            },
            robot_command_margins=margins,
            tier=tier,
            tier_state_id=tier_state_id,
        )

    def update(self, *, transition: WarehousePolicyTransition) -> WarehousePolicyUpdate:
        before = self.state_hash
        pre_counts = transition.pre_config.dynamic.current_target_counts
        post_counts = transition.post_config.dynamic.current_target_counts
        progress_signal = (
            float(post_counts["correct_robot_count"] - pre_counts["correct_robot_count"])
            + 2.0 * float(post_counts["correct_box_count"] - pre_counts["correct_box_count"])
        )
        reward_signal = float(transition.reward)
        advantage = reward_signal + progress_signal - self.baseline
        total_change = 0.0
        for robot_id, command in sorted(transition.selected_full_action_vector.commands.items()):
            features = command_features(
                config=transition.pre_config,
                robot_id=robot_id,
                command=command,
                second=transition.pre_second,
            )
            for key, value in features.items():
                delta = self.learning_rate * advantage * value
                if delta == 0.0:
                    continue
                self.weights[key] = self.weights.get(key, 0.0) + delta
                total_change += abs(delta)
        self.baseline = (1.0 - self.baseline_rate) * self.baseline + self.baseline_rate * (
            reward_signal + progress_signal
        )
        self.update_count += 1
        after = self.state_hash
        return WarehousePolicyUpdate(
            policy_id=self.policy_id,
            model_family_id=self.model_family_id,
            parameter_state_hash_before=before,
            parameter_state_hash_after=after,
            update_norm_or_change_count=total_change,
            non_noop_update=before != after and total_change > 0.0,
            reward_signal_used=reward_signal,
            progress_signal_used=progress_signal,
        )

    def score_action_vector(
        self,
        *,
        full_system_config: WarehouseFullSystemConfig,
        second: int,
        action_vector: WarehouseFullActionVector,
    ) -> float:
        score = 0.0
        for robot_id, command in sorted(action_vector.commands.items()):
            score += score_features(
                self.weights,
                command_features(
                    config=full_system_config,
                    robot_id=robot_id,
                    command=command,
                    second=second,
                ),
            )
        return score

    def to_manifest(self) -> dict[str, Any]:
        return {
            "policy_id": self.policy_id,
            "model_family_id": self.model_family_id,
            "learning_rate": self.learning_rate,
            "baseline_rate": self.baseline_rate,
            "temperature_initial": self.temperature_initial,
            "temperature_floor": self.temperature_floor,
            "temperature_decay_per_episode": self.temperature_decay_per_episode,
            "update_count": self.update_count,
            "policy_state_hash": self.state_hash,
        }

    def _temperature(self, episode_index: int) -> float:
        return max(
            self.temperature_floor,
            self.temperature_initial * (self.temperature_decay_per_episode ** episode_index),
        )


def decision_with_projection(
    *,
    decision: WarehousePolicyDecision,
    selected_action_vector: WarehouseFullActionVector,
    raw_valid: bool,
    selected_valid: bool,
    projection_trace,
) -> WarehousePolicyDecision:
    return WarehousePolicyDecision(
        policy_id=decision.policy_id,
        model_family_id=decision.model_family_id,
        second=decision.second,
        raw_action_vector=decision.raw_action_vector,
        selected_action_vector=selected_action_vector,
        raw_valid=raw_valid,
        selected_valid=selected_valid,
        projection_trace=projection_trace,
        prior_signal_used=decision.prior_signal_used,
        decision_score_summary=decision.decision_score_summary,
        robot_command_margins=decision.robot_command_margins,
        tier=decision.tier,
        tier_state_id=decision.tier_state_id,
    )


def _sample_command(
    *,
    scores: dict[DirectionOrStay, float],
    temperature: float,
    random_source: random.Random,
) -> DirectionOrStay:
    adjusted = {command: score / max(temperature, 1.0e-9) for command, score in scores.items()}
    max_score = max(adjusted.values())
    weights = {
        command: math.exp(max(-50.0, min(50.0, score - max_score)))
        for command, score in adjusted.items()
    }
    total = sum(weights.values())
    threshold = random_source.random() * total
    cumulative = 0.0
    for command in COMMANDS:
        cumulative += weights[command]
        if cumulative >= threshold:
            return command
    return DirectionOrStay.STAY


def _score_margin(scores: dict[DirectionOrStay, float], selected: DirectionOrStay) -> float:
    other_scores = [score for command, score in scores.items() if command != selected]
    if not other_scores:
        return 0.0
    return scores[selected] - max(other_scores)
