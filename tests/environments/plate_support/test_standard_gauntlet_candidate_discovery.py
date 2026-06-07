import csv
import json
from pathlib import Path

from big_boy_benchmarking.environments.plate_support.standard_gauntlet.candidate_discovery.candidate_ids import (
    candidate_id_for_row,
)
from big_boy_benchmarking.environments.plate_support.standard_gauntlet.candidate_discovery.config import (
    CandidateDiscoveryConfig,
)
from big_boy_benchmarking.environments.plate_support.standard_gauntlet.candidate_discovery.runner import (
    RESULT_TABLE_FIELDNAMES,
    run_candidate_discovery,
)
from big_boy_benchmarking.environments.plate_support.standard_gauntlet.contraction_schema_sweep.config import (
    SchemaSweepConfig,
)
from big_boy_benchmarking.environments.plate_support.standard_gauntlet.contraction_schema_sweep.runner import (
    run_contraction_schema_sweep,
)
from big_boy_benchmarking.environments.plate_support.standard_gauntlet.structural_and_tower_diagnostics.config import (
    StructuralDiagnosticsConfig,
)
from big_boy_benchmarking.environments.plate_support.standard_gauntlet.structural_and_tower_diagnostics.runner import (
    run_structural_and_tower_diagnostics,
)


def test_candidate_id_is_stable() -> None:
    row = {
        "schema_id": "schema-a",
        "schema_family_id": "family-a",
        "schema_seed": "0",
        "structural_class": "nonflat_structured",
    }

    assert candidate_id_for_row(row) == candidate_id_for_row(dict(reversed(row.items())))


def test_candidate_discovery_classifies_every_stage2_row_and_selects_ratio_candidate(
    tmp_path: Path,
) -> None:
    schema_sweep_source = _create_stage2_source(tmp_path)
    result = run_candidate_discovery(
        CandidateDiscoveryConfig(
            artifact_root=_artifact_root(tmp_path),
            run_label="smoke_001",
            schema_sweep_source_path=schema_sweep_source,
            locked_by="pytest",
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

    eligibility_rows = _read_csv(stage_root / "results" / "candidate_eligibility_summary.csv")
    source_rows = _read_csv(
        _artifact_root(tmp_path)
        / "stages"
        / "contraction_schema_sweep"
        / "results"
        / "schema_candidate_signal_summary.csv"
    )
    assert len(eligibility_rows) == len(source_rows)

    control_rows = _read_csv(stage_root / "results" / "control_anchor_summary.csv")
    assert len(control_rows) == 1

    degeneracy_rows = _read_csv(stage_root / "results" / "degeneracy_anchor_summary.csv")
    assert len(degeneracy_rows) == 1
    assert degeneracy_rows[0]["allowed_downstream_stage"] == "diagnostic_only"

    downstream_rows = _read_csv(
        stage_root / "results" / "downstream_training_health_input_summary.csv"
    )
    assert len(downstream_rows) == 1
    assert downstream_rows[0]["schema_id"] == (
        "plate_support_schema_source_local_ratio_001_over_018_v001"
    )
    assert downstream_rows[0]["selection_status"] == "selected_training_candidate"
    assert downstream_rows[0]["allowed_downstream_stage"] == "stage4_training_health"

    with (stage_root / "candidate_manifest.json").open(encoding="utf-8") as handle:
        manifest = json.load(handle)
    assert manifest["aggregate_summary"]["claim_status"] == "candidate_found"
    assert manifest["aggregate_summary"]["selected_training_candidate_count"] == 1


def _create_stage2_source(repo_root: Path) -> Path:
    stage1_source = _create_stage1_source(repo_root)
    result = run_contraction_schema_sweep(
        SchemaSweepConfig(
            artifact_root=_artifact_root(repo_root),
            run_label="smoke_001",
            stage1_readout_source_path=stage1_source,
            locked_by="pytest",
            tower_probe_steps=3,
            tower_probe_sample_size=4,
        ),
        repo_root=repo_root,
    )
    assert result.status == "complete"
    return result.readout_source_path


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
