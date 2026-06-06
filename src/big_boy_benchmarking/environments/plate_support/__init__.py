"""BBB PlateSupport environment-family support."""

from big_boy_benchmarking.environments.plate_support.ids import (
    DEFAULT_INSTANCE_ID,
    ENVIRONMENT_FAMILY_ID,
    READINESS_RUN_FAMILY_ID,
)


def run_plate_support_environment_readiness(*args, **kwargs):
    """Run the environment-readiness diagnostic without eager upstream imports."""

    from big_boy_benchmarking.environments.plate_support.runner import (
        run_plate_support_environment_readiness as _run,
    )

    return _run(*args, **kwargs)

__all__ = [
    "DEFAULT_INSTANCE_ID",
    "ENVIRONMENT_FAMILY_ID",
    "READINESS_RUN_FAMILY_ID",
    "run_plate_support_environment_readiness",
]
