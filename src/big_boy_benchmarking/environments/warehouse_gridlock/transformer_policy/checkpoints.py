"""Checkpoint helpers for Warehouse transformer policy runs."""

from __future__ import annotations

import hashlib
from dataclasses import dataclass
from pathlib import Path
from typing import Any

from big_boy_benchmarking.artifacts.writers import write_json

from .config import WarehouseTransformerPolicyRunConfig
from .model import build_model
from .torch_runtime import require_torch


@dataclass(frozen=True)
class CheckpointRecord:
    checkpoint_id: str
    path: Path
    episode_index: int
    optimizer_steps: int
    reason: str
    rolling_reward: float
    file_size_bytes: int
    sha256: str

    def to_manifest_row(self) -> dict[str, object]:
        return {
            "checkpoint_id": self.checkpoint_id,
            "path": str(self.path),
            "episode_index": self.episode_index,
            "optimizer_steps": self.optimizer_steps,
            "reason": self.reason,
            "rolling_reward": self.rolling_reward,
            "file_size_bytes": self.file_size_bytes,
            "sha256": self.sha256,
        }


def save_checkpoint(
    *,
    path: Path,
    model: Any,
    optimizer: Any,
    config: WarehouseTransformerPolicyRunConfig,
    episode_index: int,
    optimizer_steps: int,
    reason: str,
    rolling_reward: float,
) -> CheckpointRecord:
    torch = require_torch()
    path.parent.mkdir(parents=True, exist_ok=True)
    payload = {
        "model_state_dict": model.state_dict(),
        "optimizer_state_dict": optimizer.state_dict(),
        "run_config": config.to_manifest(),
        "episode_index": episode_index,
        "optimizer_steps": optimizer_steps,
        "reason": reason,
        "rolling_reward": rolling_reward,
    }
    torch.save(payload, path)
    digest = _sha256(path)
    return CheckpointRecord(
        checkpoint_id=path.stem,
        path=path,
        episode_index=episode_index,
        optimizer_steps=optimizer_steps,
        reason=reason,
        rolling_reward=rolling_reward,
        file_size_bytes=path.stat().st_size,
        sha256=digest,
    )


def load_model_checkpoint(path: Path, *, device: str = "cpu") -> tuple[Any, dict[str, Any]]:
    torch = require_torch()
    payload = torch.load(path, map_location=device)
    model_config_payload = payload["run_config"]["model"]
    from .config import TransformerModelConfig

    model = build_model(TransformerModelConfig(**model_config_payload)).to(device)
    model.load_state_dict(payload["model_state_dict"])
    model.eval()
    return model, payload


def checkpoint_due(*, episode_index: int, every: int, final_episode_index: int) -> bool:
    if episode_index == final_episode_index:
        return True
    if every <= 0:
        return False
    return (episode_index + 1) % every == 0


def write_checkpoint_manifest(path: Path, records: list[CheckpointRecord]) -> None:
    write_json(
        path,
        {"checkpoints": [record.to_manifest_row() for record in records]},
        create_parents=True,
    )


def prune_checkpoint_records(
    *,
    records: list[CheckpointRecord],
    keep_last_n: int,
    keep_best_n: int,
) -> list[CheckpointRecord]:
    last = sorted(records, key=lambda record: record.episode_index)[-max(0, keep_last_n) :]
    best = sorted(records, key=lambda record: record.rolling_reward, reverse=True)[
        : max(0, keep_best_n)
    ]
    final = [record for record in records if record.reason == "final"]
    keep_ids = {record.checkpoint_id for record in [*last, *best, *final]}
    kept: list[CheckpointRecord] = []
    for record in records:
        if record.checkpoint_id in keep_ids:
            kept.append(record)
            continue
        if record.path.exists():
            record.path.unlink()
    return kept


def _sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()
