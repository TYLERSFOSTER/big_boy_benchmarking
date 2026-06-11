"""Torch transformer actor-critic for Warehouse Gridlock."""

from __future__ import annotations

from dataclasses import dataclass
from typing import Any

from .config import TransformerModelConfig
from .encoding import (
    EncodedWarehouseBatch,
)
from .torch_runtime import require_torch


@dataclass(frozen=True)
class WarehouseTransformerOutput:
    robot_action_logits: Any
    value: Any
    token_embeddings: Any


def build_model(config: TransformerModelConfig) -> Any:
    torch = require_torch()
    nn = torch.nn

    class WarehouseTransformerActorCritic(nn.Module):
        def __init__(self, model_config: TransformerModelConfig) -> None:
            super().__init__()
            self.model_config = model_config
            self.token_type_embedding = nn.Embedding(8, model_config.d_model)
            self.entity_embedding = nn.Embedding(
                max(128, model_config.max_entities + 32), model_config.d_model
            )
            self.row_embedding = nn.Embedding(model_config.max_rows + 2, model_config.d_model)
            self.col_embedding = nn.Embedding(model_config.max_cols + 2, model_config.d_model)
            self.target_row_embedding = nn.Embedding(
                model_config.max_rows + 2, model_config.d_model
            )
            self.target_col_embedding = nn.Embedding(
                model_config.max_cols + 2, model_config.d_model
            )
            self.scalar_projection = nn.Linear(6, model_config.d_model)
            encoder_layer = nn.TransformerEncoderLayer(
                d_model=model_config.d_model,
                nhead=model_config.n_heads,
                dim_feedforward=model_config.mlp_hidden,
                dropout=model_config.dropout,
                activation=model_config.activation,
                batch_first=True,
            )
            self.encoder = nn.TransformerEncoder(
                encoder_layer,
                num_layers=model_config.n_layers,
            )
            self.action_head = nn.Linear(
                model_config.d_model, model_config.primitive_action_count
            )
            self.value_head = nn.Linear(model_config.d_model, 1)

        def forward(self, batch: EncodedWarehouseBatch) -> WarehouseTransformerOutput:
            embeddings = (
                self.token_type_embedding(batch.token_type_ids)
                + self.entity_embedding(batch.entity_id_ids)
                + self.row_embedding(batch.row_ids)
                + self.col_embedding(batch.col_ids)
                + self.target_row_embedding(batch.target_row_ids)
                + self.target_col_embedding(batch.target_col_ids)
                + self.scalar_projection(batch.scalar_features)
            )
            encoded = self.encoder(embeddings)
            robot_index = batch.robot_token_indices.unsqueeze(-1).expand(
                -1, -1, encoded.shape[-1]
            )
            robot_embeddings = encoded.gather(dim=1, index=robot_index)
            logits = self.action_head(robot_embeddings)
            value = self.value_head(encoded[:, 0, :]).squeeze(-1)
            return WarehouseTransformerOutput(
                robot_action_logits=logits,
                value=value,
                token_embeddings=encoded,
            )

    return WarehouseTransformerActorCritic(config)


def parameter_count(model: Any) -> int:
    return int(sum(parameter.numel() for parameter in model.parameters()))
