import csv
import json
from pathlib import Path

from big_boy_benchmarking.environments.plate_support.standard_gauntlet.contraction_schema_sweep.config import (
    SchemaSweepConfig,
)
from big_boy_benchmarking.environments.plate_support.standard_gauntlet.contraction_schema_sweep.runner import (
    RESULT_TABLE_FIELDNAMES,
    run_contraction_schema_sweep,
)
from big_boy_benchmarking.environments.plate_support.standard_gauntlet.structural_and_tower_diagnostics.config import (
    StructuralDiagnosticsConfig,
)
from big_boy_benchmarking.environments.plate_support.standard_gauntlet.structural_and_tower_diagnostics.runner import (
    run_structural_and_tower_diagnostics,
)


def test_schema_sweep_blocks_when_stage1_gate_is_false(tmp_path: Path) -> None:
    stage1_source = _create_stage1_source(tmp_path)
    downstream = (
        tmp_path
        / "docs"
        / "evaluations"
        / "plate_support_5x5_default_v001"
        / "standard_gauntlet"
        / "artifacts"
        / "smoke_001"
        / "stages"
        / "structural_and_tower_diagnostics"
        / "results"
        / "downstream_readiness_summary.csv"
    )
    rows = _read_csv(downstream)
    rows[0]["ready_for_schema_sweep"] = "False"
    rows[0]["blocking_reason"] = "forced_test_block"
    _write_csv(downstream, rows)

    result = run_contraction_schema_sweep(
        SchemaSweepConfig(
            artifact_root=_artifact_root(tmp_path),
            run_label="smoke_001",
            stage1_readout_source_path=stage1_source,
            locked_by="pytest",
        ),
        repo_root=tmp_path,
    )

    assert result.status == "blocked"
    assert "forced_test_block" in str(result.failure_reason)


def test_schema_sweep_writes_required_tables_and_honest_unsupported_rows(
    tmp_path: Path,
) -> None:
    stage1_source = _create_stage1_source(tmp_path)
    result = run_contraction_schema_sweep(
        SchemaSweepConfig(
            artifact_root=_artifact_root(tmp_path),
            run_label="smoke_001",
            stage1_readout_source_path=stage1_source,
            locked_by="pytest",
            tower_probe_steps=3,
            tower_probe_sample_size=4,
        ),
        repo_root=tmp_path,
    )

    assert result.status == "complete"
    stage_root = result.stage_root
    for table_name, expected_fields in RESULT_TABLE_FIELDNAMES.items():
        table_path = stage_root / "results" / f"{table_name}.csv"
        assert table_path.exists(), table_name
        with table_path.open(encoding="utf-8", newline="") as handle:
            reader = csv.DictReader(handle)
            assert tuple(reader.fieldnames or ()) == expected_fields

    arm_rows = _read_csv(stage_root / "results" / "schema_arm_summary.csv")
    schema_ids = {row["schema_id"] for row in arm_rows}
    assert "plate_support_schema_no_contraction_v001" in schema_ids
    assert "plate_support_schema_upstream_default_v001" in schema_ids

    construction_rows = _read_csv(stage_root / "results" / "schema_construction_summary.csv")
    unsupported = [
        row
        for row in construction_rows
        if row["schema_family_id"] == "geometry_coordinate"
    ]
    assert unsupported
    assert all(row["construction_status"] == "not_supported" for row in unsupported)
    assert all(row["blocking_reason"] for row in unsupported)

    signal_rows = _read_csv(stage_root / "results" / "schema_candidate_signal_summary.csv")
    assert len(signal_rows) == len(arm_rows)

    downstream_rows = _read_csv(stage_root / "results" / "downstream_candidate_input_summary.csv")
    assert len(downstream_rows) == len(arm_rows)

    readout_source = (
        tmp_path
        / "docs"
        / "evaluations"
        / "plate_support_5x5_default_v001"
        / "standard_gauntlet"
        / "contraction_schema_sweep"
        / "readout_source.json"
    )
    with readout_source.open(encoding="utf-8") as handle:
        source_payload = json.load(handle)
    assert source_payload["evaluation_id"] == (
        "plate_support_gauntlet_contraction_schema_sweep_v001"
    )
    assert source_payload["source_artifact_root"] == str(stage_root)


def _create_stage1_source(repo_root: Path) -> Path:
    readiness_source = _write_fake_readiness_source(repo_root)
    result = run_structural_and_tower_diagnostics(
        StructuralDiagnosticsConfig(
            artifact_root=_artifact_root(repo_root),
            run_label="smoke_001",
            readiness_source_path=readiness_source,
            locked_by="pytest",
            random_policy_episode_count=3,
            tower_probe_steps=3,
            tower_probe_sample_size=4,
        ),
        repo_root=repo_root,
    )
    assert result.status == "complete"
    return result.readout_source_path


def _write_fake_readiness_source(repo_root: Path) -> Path:
    (repo_root / "pyproject.toml").write_text("[project]\nname = 'fake-bbb'\n", encoding="utf-8")
    artifact_root = (
        repo_root
        / "docs"
        / "environments"
        / "plate_support_5x5_default_v001"
        / "readiness"
        / "dev_001"
    )
    artifact_root.mkdir(parents=True, exist_ok=True)
    environment_doc = repo_root / "docs" / "environments" / "plate_support_5x5_default_v001.md"
    environment_doc.parent.mkdir(parents=True, exist_ok=True)
    environment_doc.write_text("# fake env doc\n", encoding="utf-8")
    summary = artifact_root / "runs" / "plate_support_environment_readiness_v001" / "summaries"
    summary.mkdir(parents=True, exist_ok=True)
    summary_path = summary / "summary.json"
    summary_path.write_text("{}", encoding="utf-8")
    source = artifact_root / "readout_source.json"
    source.write_text(
        json.dumps(
            {
                "artifact_root": str(artifact_root),
                "environment_doc": str(environment_doc),
                "environment_family_id": "plate_support",
                "environment_instance_id": "plate_support_5x5_default_v001",
                "run_family_summary": str(summary_path),
                "source_type": "environment_readiness",
            },
            indent=2,
            sort_keys=True,
        ),
        encoding="utf-8",
    )
    return source


def _artifact_root(repo_root: Path) -> Path:
    return (
        repo_root
        / "docs"
        / "evaluations"
        / "plate_support_5x5_default_v001"
        / "standard_gauntlet"
        / "artifacts"
        / "smoke_001"
    )


def _read_csv(path: Path) -> list[dict[str, str]]:
    with path.open(encoding="utf-8", newline="") as handle:
        return list(csv.DictReader(handle))


def _write_csv(path: Path, rows: list[dict[str, str]]) -> None:
    with path.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=tuple(rows[0].keys()))
        writer.writeheader()
        writer.writerows(rows)
