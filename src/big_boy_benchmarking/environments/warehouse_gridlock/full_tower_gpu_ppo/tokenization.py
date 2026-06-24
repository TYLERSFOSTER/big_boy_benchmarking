"""Tokenization for Warehouse full-tower PPO records."""

from __future__ import annotations

import hashlib
from dataclasses import dataclass

from .ids import WAREHOUSE_GRIDLOCK_RECORD_TOKENIZATION_SCHEMA_VERSION
from .records import DecisionContextRecord
from .state_collapser_runtime import PointwiseActionChoice, WarehouseDecisionSurface

CONTEXT_FEATURE_DIM = 8
CANDIDATE_FEATURE_DIM = 12


@dataclass(frozen=True)
class EncodedDecisionSurface:
    context_features: list[float]
    candidate_features: list[list[float]]
    candidate_mask: list[bool]
    candidate_ids: list[str]
    tokenization_schema_version: str = WAREHOUSE_GRIDLOCK_RECORD_TOKENIZATION_SCHEMA_VERSION


def encode_surface(
    *,
    surface: WarehouseDecisionSurface,
    context: DecisionContextRecord,
    max_seconds: int,
) -> EncodedDecisionSurface:
    context_features = [
        _scale(context.environment_second, max_seconds),
        float(surface.tier_index),
        float(len(surface.current_position_at_every_tier)),
        float(surface.generated_candidate_count),
        float(surface.valid_candidate_count),
        float(surface.invalid_candidate_count),
        1.0 if surface.actor_callable else 0.0,
        _hash01(surface.arm_id),
    ]
    candidate_features = [
        _candidate_features(choice=choice, local_count=len(surface.action_choices))
        for choice in surface.action_choices
    ]
    return EncodedDecisionSurface(
        context_features=context_features,
        candidate_features=candidate_features,
        candidate_mask=list(context.candidate_mask),
        candidate_ids=list(context.candidate_action_ids_ordered),
    )


def tokenization_manifest() -> dict[str, object]:
    return {
        "record_tokenization_schema_version": WAREHOUSE_GRIDLOCK_RECORD_TOKENIZATION_SCHEMA_VERSION,
        "context_feature_dim": CONTEXT_FEATURE_DIM,
        "candidate_feature_dim": CANDIDATE_FEATURE_DIM,
        "candidate_ordering_policy": "state_collapser_executable_action_cells_order",
        "padding_policy": "batch_local_padding_only",
        "mask_semantics": "pointwise_executable",
        "stable_id_hashing": "sha256_prefix_scaled",
    }


def _candidate_features(*, choice: PointwiseActionChoice, local_count: int) -> list[float]:
    return [
        float(choice.tier_index),
        _scale(choice.local_index, max(1, local_count)),
        float(choice.executable_lift_count),
        float(choice.candidate_lift_count),
        _hash01(choice.state_cell_id),
        _hash01(choice.action_cell_id),
        _hash01(choice.action_id),
        _hash01(choice.target_state.stable_id),
        float(len(choice.executable_edges)),
        1.0,
        0.0,
        0.0,
    ]


def _scale(value: int | float, denominator: int | float) -> float:
    denom = max(float(denominator), 1.0)
    return float(value) / denom


def _hash01(text: str) -> float:
    digest = hashlib.sha256(text.encode("utf-8")).hexdigest()[:12]
    return int(digest, 16) / float(16**12 - 1)
