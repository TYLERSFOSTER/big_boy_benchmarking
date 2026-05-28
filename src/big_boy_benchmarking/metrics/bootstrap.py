"""Small replicate-level bootstrap helpers."""

from __future__ import annotations

import random
import statistics


def mean_std(values: list[float] | tuple[float, ...]) -> tuple[float, float]:
    if not values:
        raise ValueError("cannot summarize empty data")
    if len(values) == 1:
        return float(values[0]), 0.0
    return float(statistics.mean(values)), float(statistics.stdev(values))


def percentile_bootstrap_interval(
    values: list[float] | tuple[float, ...],
    *,
    confidence_level: float = 0.95,
    resamples: int = 1000,
    seed: int,
) -> tuple[float, float]:
    if not values:
        raise ValueError("cannot bootstrap empty data")
    if not 0.0 < confidence_level < 1.0:
        raise ValueError("confidence_level must be between 0 and 1")
    rng = random.Random(seed)
    means = []
    population = list(map(float, values))
    for _ in range(resamples):
        sample = [rng.choice(population) for _ in population]
        means.append(statistics.mean(sample))
    means.sort()
    alpha = (1.0 - confidence_level) / 2.0
    lower_idx = int(alpha * (len(means) - 1))
    upper_idx = int((1.0 - alpha) * (len(means) - 1))
    return float(means[lower_idx]), float(means[upper_idx])
