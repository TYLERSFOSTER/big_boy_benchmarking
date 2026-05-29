import json
from pathlib import Path

from state_collapser.tower.runtime import TowerRuntime

from big_boy_benchmarking.runners.upstream_smoke import run_upstream_smoke
from big_boy_benchmarking.upstream.readout_guards import ReadoutCallCounter


def test_default_smoke_runner_writes_artifacts_without_readout(
    tmp_path: Path, monkeypatch
) -> None:
    counter = ReadoutCallCounter()
    original = TowerRuntime.compatibility_quotient_tiers
    monkeypatch.setattr(
        TowerRuntime,
        "compatibility_quotient_tiers",
        counter.wrap_compatibility(original),
    )

    result = run_upstream_smoke(
        smoke_id="plate_support_env",
        artifact_root=tmp_path,
        run_id="default",
    )

    mode_manifest = json.loads(Path(result.artifact_paths["mode_manifest"]).read_text())
    linearization_manifest = json.loads(
        Path(result.artifact_paths["linearization_manifest"]).read_text()
    )
    assert result.status == "success"
    assert counter.compatibility_calls == 0
    assert mode_manifest["readout_requested"] is False
    assert mode_manifest["uses_compatibility_readout"] is False
    assert (
        linearization_manifest["linearization_report"]["benchmark_label"]
        == "tensor_available_disabled"
    )


def test_diagnostic_smoke_runner_calls_readout_when_requested(
    tmp_path: Path, monkeypatch
) -> None:
    counter = ReadoutCallCounter()
    original = TowerRuntime.compatibility_quotient_tiers
    monkeypatch.setattr(
        TowerRuntime,
        "compatibility_quotient_tiers",
        counter.wrap_compatibility(original),
    )

    result = run_upstream_smoke(
        smoke_id="plate_support_env",
        artifact_root=tmp_path,
        mode_id="tower_nonempty_schema_tabular",
        run_id="diagnostic",
    )

    mode_manifest = json.loads(Path(result.artifact_paths["mode_manifest"]).read_text())
    assert result.status == "success"
    assert counter.compatibility_calls == 1
    assert mode_manifest["readout_requested"] is True
    assert mode_manifest["uses_compatibility_readout"] is True
