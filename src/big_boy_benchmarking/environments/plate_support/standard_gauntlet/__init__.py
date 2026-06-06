"""Architecture helpers for the PlateSupport standard gauntlet suite."""

from big_boy_benchmarking.environments.plate_support.standard_gauntlet.ids import (
    ENVIRONMENT_FAMILY_ID,
    ENVIRONMENT_INSTANCE_ID,
    LINEARIZATION_MODE_ID,
    STAGE_DEFINITIONS,
    SUITE_ID,
    SUITE_RUN_FAMILY_ID,
)
from big_boy_benchmarking.environments.plate_support.standard_gauntlet.paths import (
    default_readiness_source_path,
    suite_artifact_root,
    suite_readout_surface,
)

__all__ = [
    "ENVIRONMENT_FAMILY_ID",
    "ENVIRONMENT_INSTANCE_ID",
    "LINEARIZATION_MODE_ID",
    "STAGE_DEFINITIONS",
    "SUITE_ID",
    "SUITE_RUN_FAMILY_ID",
    "default_readiness_source_path",
    "suite_artifact_root",
    "suite_readout_surface",
]
