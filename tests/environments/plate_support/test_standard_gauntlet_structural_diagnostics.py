import csv
import json
from pathlib import Path

import pytest

from big_boy_benchmarking.environments.plate_support.standard_gauntlet.ids import (
    STRUCTURAL_TOWER_DIAGNOSTICS_STAGE_ID,
)
from big_boy_benchmarking.environments.plate_support.standard_gauntlet.structural_and_tower_diagnostics.config import (
    StructuralDiagnosticsConfig,
)
from big_boy_benchmarking.environments.plate_support.standard_gauntlet.structural_and_tower_diagnostics.readiness_source import (
    ReadinessSourceError,
    load_readiness_source,
)
from big_boy_benchmarking.environments.plate_support.standard_gauntlet.structural_and_tower_diagnostics.runner import (
    RESULT_TABLE_FIELDNAMES,
    run_structural_and_tower_diagnostics,
)


def test_load_readiness_source_accepts_real_plate_support_source() -> None:
    repo_root = Path(__file__).resolve().parents[3]
    source = load_readiness_source(
        repo_root
        / "docs"
        / "environments"
        / "plate_support_5x5_default_v001"
        / "readiness"
        / "dev_001"
        / "readout_source.json",
        repo_root=repo_root,
    )

    assert source.source_type == "environment_readiness"
    assert source.environment_family_id == "plate_support"
    assert source.environment_instance_id == "plate_support_5x5_default_v001"
    assert "docs/environments" in source.source_artifact_root.as_posix()


def test_readiness_source_rejects_wrong_environment_id(tmp_path: Path) -> None:
    source = _write_fake_readiness_source(tmp_path, environment_instance_id="wrong_instance")

    with pytest.raises(ReadinessSourceError, match="expected instance"):
        load_readiness_source(source, repo_root=tmp_path)


def test_readiness_source_rejects_source_outside_repo(tmp_path: Path) -> None:
    repo_root = Path(__file__).resolve().parents[3]
    source = _write_fake_readiness_source(tmp_path)

    with pytest.raises(ReadinessSourceError, match="outside repository"):
        load_readiness_source(source, repo_root=repo_root)


def test_readiness_source_rejects_artifacts_under_evaluations(tmp_path: Path) -> None:
    source = _write_fake_readiness_source(tmp_path, artifact_tree="docs/evaluations")

    with pytest.raises(ReadinessSourceError, match="docs/environments"):
        load_readiness_source(source, repo_root=tmp_path)


def test_structural_diagnostics_stage_writes_required_tables_and_claim_boundaries(
    tmp_path: Path,
) -> None:
    readiness_source = _write_fake_readiness_source(tmp_path)
    result = run_structural_and_tower_diagnostics(
        StructuralDiagnosticsConfig(
            artifact_root=(
                tmp_path
                / "docs"
                / "evaluations"
                / "plate_support_5x5_default_v001"
                / "standard_gauntlet"
                / "artifacts"
                / "smoke_001"
            ),
            run_label="smoke_001",
            readiness_source_path=readiness_source,
            locked_by="pytest",
            random_policy_episode_count=3,
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

    transition_rows = _read_csv(stage_root / "results" / "transition_summary.csv")
    assert {
        "candidate_state_id",
        "next_state_id",
        "invalid_move",
        "valid_self_transition",
    }.issubset(transition_rows[0])

    random_rows = _read_csv(stage_root / "results" / "random_policy_recon_summary.csv")
    assert "not an official learning baseline" in random_rows[0]["claim_boundary"]

    tower_rows = _read_csv(stage_root / "results" / "tower_shape_summary.csv")
    assert "not tower benefit evidence" in tower_rows[0]["claim_boundary"]

    downstream_rows = _read_csv(stage_root / "results" / "downstream_readiness_summary.csv")
    assert downstream_rows[0]["ready_for_schema_sweep"] == "True"

    suite_status = (
        tmp_path
        / "docs"
        / "evaluations"
        / "plate_support_5x5_default_v001"
        / "standard_gauntlet"
        / "artifacts"
        / "smoke_001"
        / "evaluations"
        / "plate_support_standard_gauntlet_v001"
        / "stage_status_summary.csv"
    )
    assert suite_status.exists()

    readout_source = (
        tmp_path
        / "docs"
        / "evaluations"
        / "plate_support_5x5_default_v001"
        / "standard_gauntlet"
        / "structural_and_tower_diagnostics"
        / "readout_source.json"
    )
    with readout_source.open(encoding="utf-8") as handle:
        source_payload = json.load(handle)
    assert source_payload["evaluation_id"] == STRUCTURAL_TOWER_DIAGNOSTICS_STAGE_ID
    assert source_payload["source_artifact_root"] == str(stage_root)


def _write_fake_readiness_source(
    repo_root: Path,
    *,
    environment_instance_id: str = "plate_support_5x5_default_v001",
    artifact_tree: str = "docs/environments",
) -> Path:
    (repo_root / "pyproject.toml").write_text("[project]\nname = 'fake-bbb'\n", encoding="utf-8")
    artifact_root = (
        repo_root
        / artifact_tree
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
                "environment_instance_id": environment_instance_id,
                "run_family_summary": str(summary_path),
                "source_type": "environment_readiness",
            },
            indent=2,
            sort_keys=True,
        ),
        encoding="utf-8",
    )
    return source


def _read_csv(path: Path) -> list[dict[str, str]]:
    with path.open(encoding="utf-8", newline="") as handle:
        return list(csv.DictReader(handle))
