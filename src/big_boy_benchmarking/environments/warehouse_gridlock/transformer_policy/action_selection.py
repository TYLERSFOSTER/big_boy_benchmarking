"""Action selection adapters for Warehouse transformer policies."""

from __future__ import annotations

import random
from dataclasses import dataclass
from typing import Any

from ..actions import DirectionOrStay
from ..masked_direct_vs_live_lift_tower.candidate_generation import (
    TowerActionCandidate,
)
from ..policies.contracts import (
    WarehouseFullActionVector,
    WarehousePolicyDecision,
)
from .config import MODEL_FAMILY_ID
from .torch_runtime import require_torch

COMMANDS = (
    DirectionOrStay.STAY,
    DirectionOrStay.NORTH,
    DirectionOrStay.SOUTH,
    DirectionOrStay.WEST,
    DirectionOrStay.EAST,
)
COMMAND_TO_INDEX = {command: index for index, command in enumerate(COMMANDS)}


@dataclass(frozen=True)
class SelectedActionForTraining:
    decision: WarehousePolicyDecision
    selected_action_vector: WarehouseFullActionVector
    log_probability: Any
    entropy: Any
    value: Any
    candidate_count: int
    selection_mode: str


def select_direct_action(
    *,
    policy_id: str,
    output: Any,
    robot_ids: tuple[str, ...],
    second: int,
    episode_index: int,
    step_index: int,
    seed: int,
    greedy: bool = False,
) -> SelectedActionForTraining:
    torch = require_torch()
    distribution = torch.distributions.Categorical(logits=output.robot_action_logits[0])
    if greedy:
        indices = output.robot_action_logits[0].argmax(dim=-1)
    else:
        generator = torch.Generator(device=output.robot_action_logits.device)
        generator.manual_seed(_selection_seed(seed, episode_index, step_index))
        probs = distribution.probs
        indices = torch.multinomial(
            probs,
            num_samples=1,
            replacement=True,
            generator=generator,
        ).squeeze(-1)
    commands = {
        robot_id: COMMANDS[int(index.item())]
        for robot_id, index in zip(robot_ids, indices, strict=True)
    }
    action_vector = WarehouseFullActionVector(commands=commands)
    log_probability = distribution.log_prob(indices).sum()
    entropy = distribution.entropy().sum()
    decision = WarehousePolicyDecision(
        policy_id=policy_id,
        model_family_id=MODEL_FAMILY_ID,
        second=second,
        raw_action_vector=action_vector,
        selected_action_vector=None,
        raw_valid=False,
        selected_valid=False,
        projection_trace=None,
        prior_signal_used=True,
        decision_score_summary={
            "selection_mode": "direct_factorized_sample",
            "mean_logit": float(output.robot_action_logits.detach().mean().cpu()),
        },
        robot_command_margins=_robot_margins(output.robot_action_logits[0], robot_ids),
    )
    return SelectedActionForTraining(
        decision=decision,
        selected_action_vector=action_vector,
        log_probability=log_probability,
        entropy=entropy,
        value=output.value[0],
        candidate_count=0,
        selection_mode="direct_factorized_sample",
    )


def select_tower_candidate_action(
    *,
    policy_id: str,
    output: Any,
    robot_ids: tuple[str, ...],
    candidates: list[TowerActionCandidate],
    second: int,
    episode_index: int,
    step_index: int,
    seed: int,
    tier: int,
    tier_state_id: str,
    greedy: bool = False,
) -> SelectedActionForTraining | None:
    if not candidates:
        return None
    torch = require_torch()
    log_probs = output.robot_action_logits[0].log_softmax(dim=-1)
    candidate_scores = []
    for candidate in candidates:
        score = torch.zeros((), dtype=log_probs.dtype, device=log_probs.device)
        commands = candidate.concrete_candidate.action.commands
        for robot_index, robot_id in enumerate(robot_ids):
            command = commands[robot_id]
            score = score + log_probs[robot_index, COMMAND_TO_INDEX[command]]
        candidate_scores.append(score)
    scores = torch.stack(candidate_scores)
    distribution = torch.distributions.Categorical(logits=scores)
    if greedy:
        selected_index = int(scores.argmax().item())
    else:
        random_source = random.Random(_selection_seed(seed, episode_index, step_index))
        selected_index = int(
            torch.multinomial(
                distribution.probs,
                num_samples=1,
                replacement=True,
                generator=_torch_generator(torch, scores.device, random_source.randrange(2**31)),
            )[0].item()
        )
    selected = candidates[selected_index]
    action_vector = WarehouseFullActionVector.from_action(selected.concrete_candidate.action)
    decision = WarehousePolicyDecision(
        policy_id=policy_id,
        model_family_id=MODEL_FAMILY_ID,
        second=second,
        raw_action_vector=action_vector,
        selected_action_vector=None,
        raw_valid=False,
        selected_valid=False,
        projection_trace=None,
        prior_signal_used=True,
        decision_score_summary={
            "selection_mode": "tower_candidate_vector_score",
            "candidate_count": len(candidates),
            "selected_candidate_rank": selected.rank,
            "selected_candidate_score": float(scores[selected_index].detach().cpu()),
            "mean_candidate_score": float(scores.detach().mean().cpu()),
        },
        robot_command_margins=_robot_margins(output.robot_action_logits[0], robot_ids),
        tier=tier,
        tier_state_id=tier_state_id,
    )
    return SelectedActionForTraining(
        decision=decision,
        selected_action_vector=action_vector,
        log_probability=distribution.log_prob(torch.tensor(selected_index, device=scores.device)),
        entropy=distribution.entropy(),
        value=output.value[0],
        candidate_count=len(candidates),
        selection_mode="tower_candidate_vector_score",
    )


def decision_with_projection(
    *,
    selected: SelectedActionForTraining,
    raw_valid: bool,
    selected_valid: bool,
    projection_trace: Any,
    selected_action_vector: WarehouseFullActionVector,
) -> WarehousePolicyDecision:
    decision = selected.decision
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


def _robot_margins(logits: Any, robot_ids: tuple[str, ...]) -> dict[str, float]:
    margins: dict[str, float] = {}
    for robot_id, row in zip(robot_ids, logits, strict=True):
        sorted_values = row.detach().sort(descending=True).values
        if len(sorted_values) < 2:
            margins[robot_id] = 0.0
        else:
            margins[robot_id] = float((sorted_values[0] - sorted_values[1]).cpu())
    return margins


def _selection_seed(seed: int, episode_index: int, step_index: int) -> int:
    return abs(hash((seed, episode_index, step_index))) % (2**31)


def _torch_generator(torch: Any, device: Any, seed: int) -> Any:
    generator = torch.Generator(device=device)
    generator.manual_seed(seed)
    return generator
