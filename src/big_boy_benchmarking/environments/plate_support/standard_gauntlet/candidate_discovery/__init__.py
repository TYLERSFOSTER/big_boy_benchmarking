"""Stage 3 candidate discovery for the PlateSupport gauntlet."""

from big_boy_benchmarking.environments.plate_support.standard_gauntlet.candidate_discovery.config import (
    CandidateDiscoveryConfig,
    default_candidate_discovery_config,
)
from big_boy_benchmarking.environments.plate_support.standard_gauntlet.candidate_discovery.runner import (
    run_candidate_discovery,
)

__all__ = [
    "CandidateDiscoveryConfig",
    "default_candidate_discovery_config",
    "run_candidate_discovery",
]
