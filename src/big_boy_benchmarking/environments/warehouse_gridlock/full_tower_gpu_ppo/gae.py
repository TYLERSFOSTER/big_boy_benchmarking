"""GAE utilities for Warehouse full-tower PPO."""

from __future__ import annotations


def compute_gae(
    *,
    rewards: list[float],
    values: list[float],
    bootstrap_value: float,
    terminated: list[bool],
    gamma: float,
    gae_lambda: float,
) -> tuple[list[float], list[float]]:
    if not (
        len(rewards) == len(values) == len(terminated)
    ):
        raise ValueError("rewards, values, and terminated flags must have equal length")
    advantages = [0.0 for _ in rewards]
    running = 0.0
    next_value = float(bootstrap_value)
    for index in reversed(range(len(rewards))):
        nonterminal = 0.0 if terminated[index] else 1.0
        delta = rewards[index] + gamma * next_value * nonterminal - values[index]
        running = delta + gamma * gae_lambda * nonterminal * running
        advantages[index] = running
        next_value = values[index]
    returns = [advantage + value for advantage, value in zip(advantages, values)]
    return advantages, returns


def normalize(values: list[float]) -> list[float]:
    if not values:
        return []
    mean = sum(values) / len(values)
    variance = sum((value - mean) ** 2 for value in values) / max(1, len(values))
    std = variance**0.5
    if std < 1.0e-8:
        return [0.0 for _ in values]
    return [(value - mean) / std for value in values]
