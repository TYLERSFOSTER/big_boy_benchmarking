from pathlib import Path

from big_boy_benchmarking.environments.counterpoint.instances import TINY_INSTANCE_ID
from big_boy_benchmarking.environments.counterpoint.serious_learning.aggregation import (
    aggregate_serious_learning_results,
)
from big_boy_benchmarking.environments.counterpoint.serious_learning.budgets import (
    CalibrationBudget,
)
from big_boy_benchmarking.environments.counterpoint.serious_learning.docs_writer import (
    write_serious_learning_docs,
)
from big_boy_benchmarking.environments.counterpoint.serious_learning.runner import (
    run_calibration,
)


def test_docs_writer_creates_expected_files_from_artifacts(tmp_path) -> None:
    run_calibration(
        artifact_root=tmp_path / "artifacts",
        budget=CalibrationBudget(
            environment_instance_id=TINY_INSTANCE_ID,
            episode_count=1,
            max_steps_per_episode=4,
            replicate_count=1,
            random_schema_seed_count=1,
            smoke=True,
        ),
        base_seed=51,
    )
    aggregate_serious_learning_results(tmp_path / "artifacts")

    written = write_serious_learning_docs(
        artifact_root=tmp_path / "artifacts",
        docs_root=tmp_path / "docs",
        command_lines=(
            "uv run python -m big_boy_benchmarking.cli "
            "counterpoint serious-learning summarize",
        ),
    )

    assert set(written) == {
        "README.md",
        "method.md",
        "runbook.md",
        "artifact_index.md",
        "results/summary.md",
    }
    assert all(Path(path).exists() for path in written.values())
    readme = Path(written["README.md"]).read_text()
    assert "counterpoint_symbolic_n3_small_v001" in readme
    assert str(tmp_path / "artifacts") in readme


def test_generated_docs_do_not_claim_forbidden_result_language(tmp_path) -> None:
    written = write_serious_learning_docs(
        artifact_root=tmp_path / "missing-artifacts",
        docs_root=tmp_path / "docs",
    )
    combined = "\n".join(Path(path).read_text() for path in written.values())

    assert "beats direct" not in combined
    assert "CUDA result" not in combined
    assert "general superiority" not in combined
