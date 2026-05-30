import csv
from pathlib import Path

from big_boy_benchmarking.environments.counterpoint.instances import TINY_INSTANCE_ID
from big_boy_benchmarking.environments.counterpoint.serious_learning.aggregation import (
    aggregate_serious_learning_results,
)
from big_boy_benchmarking.environments.counterpoint.serious_learning.budgets import (
    CalibrationBudget,
)
from big_boy_benchmarking.environments.counterpoint.serious_learning.runner import (
    run_calibration,
)


def test_aggregation_reads_artifacts_and_writes_summary_tables(tmp_path) -> None:
    run_calibration(
        artifact_root=tmp_path,
        budget=CalibrationBudget(
            environment_instance_id=TINY_INSTANCE_ID,
            episode_count=1,
            max_steps_per_episode=4,
            replicate_count=1,
            random_schema_seed_count=1,
            smoke=True,
        ),
        base_seed=41,
    )

    summary = aggregate_serious_learning_results(tmp_path)
    table_path = Path(summary["table_path"])
    rows = list(csv.DictReader(table_path.open()))

    assert summary["status"] == "complete"
    assert table_path.exists()
    assert len(rows) == 7
    assert "delta_vs_direct_tabular_q" in rows[0]
    assert Path(summary["result_paths"][0]).name == "learning_curves.csv"


def test_aggregation_marks_missing_arms_incomplete(tmp_path) -> None:
    evaluation_root = (
        tmp_path / "evaluations" / "counterpoint_first_serious_learning_v001"
    )
    evaluation_root.mkdir(parents=True)
    (evaluation_root / "calibration_run_index.csv").write_text(
        "evaluation_id,run_id,arm_id,mode_id,schema_id,schema_seed,seed_bundle_id,"
        "replicate_index,status,artifact_root,started_at,ended_at\n",
        encoding="utf-8",
    )

    summary = aggregate_serious_learning_results(tmp_path)
    rows = list(csv.DictReader(Path(summary["table_path"]).open()))

    assert summary["status"] == "incomplete"
    assert {row["status"] for row in rows} == {"missing"}
