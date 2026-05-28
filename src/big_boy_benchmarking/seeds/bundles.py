"""Deterministic seed bundle generation."""

from __future__ import annotations

import hashlib
import json
import random
from dataclasses import asdict, dataclass
from typing import Any


@dataclass(frozen=True)
class SeedBundle:
    seed_bundle_id: str
    replicate_index: int
    environment_seed: int
    schema_seed: int
    learner_seed: int
    controller_seed: int
    diagnostic_sampling_seed: int
    artifact_sampling_seed: int

    def to_dict(self) -> dict[str, Any]:
        return asdict(self)


def seed_bundle_id(seed_values: dict[str, int]) -> str:
    payload = json.dumps(seed_values, sort_keys=True, separators=(",", ":"))
    return "seed-" + hashlib.sha256(payload.encode("utf-8")).hexdigest()[:16]


def generate_seed_bundles(base_seed: int, replicate_count: int) -> tuple[SeedBundle, ...]:
    if replicate_count < 0:
        raise ValueError("replicate_count must be nonnegative")

    bundles: list[SeedBundle] = []
    for replicate_index in range(replicate_count):
        rng = random.Random((base_seed, replicate_index).__repr__())
        values = {
            "replicate_index": replicate_index,
            "environment_seed": rng.randrange(0, 2**31),
            "schema_seed": rng.randrange(0, 2**31),
            "learner_seed": rng.randrange(0, 2**31),
            "controller_seed": rng.randrange(0, 2**31),
            "diagnostic_sampling_seed": rng.randrange(0, 2**31),
            "artifact_sampling_seed": rng.randrange(0, 2**31),
        }
        bundles.append(SeedBundle(seed_bundle_id=seed_bundle_id(values), **values))
    return tuple(bundles)
