"""Configuration for PlateSupport gauntlet Stage 7 readout synthesis."""

from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path


@dataclass(frozen=True)
class ReadoutSystemLearningConfig:
    """Explicit readout build request."""

    readout_source_path: Path
    preserve_clarification_turns: bool = True
    create_system_learning_archive: bool = False

    def __post_init__(self) -> None:
        if self.readout_source_path.name != "readout_source.json":
            raise ValueError(
                "Stage 7 requires an explicit repo-side readout_source.json; "
                f"got {self.readout_source_path}"
            )
