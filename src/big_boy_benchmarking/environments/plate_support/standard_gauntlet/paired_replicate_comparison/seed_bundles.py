"""Paired seed-bundle policy for PlateSupport gauntlet Stage 6."""

from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True)
class PairedSeedBundle:
    """Seed bundle shared by all arms in one replicate pair."""

    pair_id: str
    replicate_index: int
    environment_seed: int
    learner_seed: int
    exploration_seed: int
    initial_state_seed: int
    tie_break_seed: int

    def episode_seed(self, episode_index: int) -> int:
        return self.environment_seed + episode_index

    def to_row(self) -> dict[str, object]:
        return {
            "pair_id": self.pair_id,
            "replicate_index": self.replicate_index,
            "environment_seed": self.environment_seed,
            "learner_seed": self.learner_seed,
            "exploration_seed": self.exploration_seed,
            "initial_state_seed": self.initial_state_seed,
            "tie_break_seed": self.tie_break_seed,
        }


SEED_BUNDLE_FIELDS = (
    "pair_id",
    "replicate_index",
    "environment_seed",
    "learner_seed",
    "exploration_seed",
    "initial_state_seed",
    "tie_break_seed",
)


def build_paired_seed_bundles(
    *,
    base_seed: int,
    replicate_count: int,
) -> tuple[PairedSeedBundle, ...]:
    """Build deterministic seed bundles shared across comparison arms."""

    bundles = []
    for replicate_index in range(replicate_count):
        offset = base_seed + replicate_index * 10_000
        bundles.append(
            PairedSeedBundle(
                pair_id=f"pairrep{replicate_index:03d}",
                replicate_index=replicate_index,
                environment_seed=offset,
                learner_seed=offset + 1_001,
                exploration_seed=offset + 2_002,
                initial_state_seed=offset + 3_003,
                tie_break_seed=offset + 4_004,
            )
        )
    return tuple(bundles)
