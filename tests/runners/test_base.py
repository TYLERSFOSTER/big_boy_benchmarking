from pathlib import Path

from big_boy_benchmarking.runners.base import BenchmarkRunRequest
from big_boy_benchmarking.seeds.bundles import generate_seed_bundles


def test_run_request_requires_explicit_artifact_root(tmp_path: Path) -> None:
    request = BenchmarkRunRequest(
        run_id="run",
        run_family_id="family",
        environment_id="env",
        mode_id="mode",
        schema_id="schema",
        learner_id="learner",
        controller_id="controller",
        seed_bundle=generate_seed_bundles(1, 1)[0],
        budget={"steps": 1},
        artifact_root=tmp_path,
        diagnostic_profile="smoke",
        timing_profile="default",
    )

    assert request.artifact_root == tmp_path
