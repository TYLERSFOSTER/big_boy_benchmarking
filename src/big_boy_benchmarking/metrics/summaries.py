"""Summary helpers for replicate-level values."""

from __future__ import annotations

from big_boy_benchmarking.metrics.bootstrap import mean_std, percentile_bootstrap_interval


def summarize_replicates(
    metric_name: str,
    values: list[float] | tuple[float, ...],
    *,
    seed: int,
    confidence_level: float = 0.95,
) -> dict[str, float | int | str]:
    if not values:
        raise ValueError("cannot summarize empty data")
    mean, std = mean_std(values)
    lower, upper = percentile_bootstrap_interval(
        values,
        confidence_level=confidence_level,
        resamples=200,
        seed=seed,
    )
    return {
        "metric_name": metric_name,
        "seed_count": len(values),
        "replicate_count": len(values),
        "mean": mean,
        "std": std,
        "bootstrap_lower": lower,
        "bootstrap_upper": upper,
        "confidence_level": confidence_level,
    }
