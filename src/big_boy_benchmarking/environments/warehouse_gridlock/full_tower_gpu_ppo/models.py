"""Per-tier candidate-scoring actor-critic models."""

from __future__ import annotations

from dataclasses import dataclass
from typing import Any

from .tokenization import CANDIDATE_FEATURE_DIM, CONTEXT_FEATURE_DIM, EncodedDecisionSurface


@dataclass(frozen=True)
class TierPolicyOutput:
    logits: Any
    log_probs: Any
    probabilities: Any
    entropy: Any
    value: Any


class TierCandidateActorCritic:
    """Small candidate-scoring actor critic for one tower tier."""

    def __new__(cls, *args: object, **kwargs: object) -> Any:  # pragma: no cover - factory
        torch = _require_torch()
        nn = torch.nn

        class _TierCandidateActorCritic(nn.Module):
            def __init__(self, hidden_dim: int) -> None:
                super().__init__()
                self.hidden_dim = hidden_dim
                self.context_encoder = nn.Sequential(
                    nn.Linear(CONTEXT_FEATURE_DIM, hidden_dim),
                    nn.Tanh(),
                    nn.Linear(hidden_dim, hidden_dim),
                    nn.Tanh(),
                )
                self.candidate_encoder = nn.Sequential(
                    nn.Linear(CANDIDATE_FEATURE_DIM, hidden_dim),
                    nn.Tanh(),
                    nn.Linear(hidden_dim, hidden_dim),
                    nn.Tanh(),
                )
                self.score = nn.Linear(hidden_dim * 2, 1)
                self.value_head = nn.Linear(hidden_dim, 1)

            def forward_encoded(self, encoded: EncodedDecisionSurface) -> TierPolicyOutput:
                device = next(self.parameters()).device
                context, candidates, mask = tensors_from_encoded(
                    encoded,
                    torch=torch,
                    device=device,
                )
                context_embedding = self.context_encoder(context)
                candidate_embedding = self.candidate_encoder(candidates)
                repeated_context = context_embedding.unsqueeze(0).expand(
                    candidate_embedding.shape[0], -1
                )
                logits = self.score(
                    torch.cat([repeated_context, candidate_embedding], dim=-1)
                ).squeeze(-1)
                masked_logits = logits.masked_fill(~mask, torch.finfo(logits.dtype).min)
                log_probs = masked_logits.log_softmax(dim=-1)
                probabilities = masked_logits.softmax(dim=-1)
                entropy = -(probabilities * log_probs).sum()
                value = self.value_head(context_embedding).squeeze(-1)
                return TierPolicyOutput(
                    logits=masked_logits,
                    log_probs=log_probs,
                    probabilities=probabilities,
                    entropy=entropy,
                    value=value,
                )

        return _TierCandidateActorCritic(*args, **kwargs)


def tensors_from_encoded(
    encoded: EncodedDecisionSurface,
    *,
    torch: Any | None = None,
    device: Any | None = None,
) -> tuple[Any, Any, Any]:
    torch = torch or _require_torch()
    if not encoded.candidate_features:
        raise ValueError("cannot tensorize empty candidate surface")
    context = torch.tensor(encoded.context_features, dtype=torch.float32, device=device)
    candidates = torch.tensor(encoded.candidate_features, dtype=torch.float32, device=device)
    mask = torch.tensor(encoded.candidate_mask, dtype=torch.bool, device=device)
    return context, candidates, mask


def parameter_count(model: Any) -> int:
    return int(sum(parameter.numel() for parameter in model.parameters()))


def _require_torch() -> Any:
    try:
        import torch
    except ImportError as exc:  # pragma: no cover
        raise RuntimeError("torch is required for Warehouse full-tower PPO") from exc
    return torch
