from state_collapser.tower.runtime import TowerRuntime

from big_boy_benchmarking.upstream.readout_guards import ReadoutCallCounter


def test_readout_guard_counts_monkeypatched_calls(monkeypatch) -> None:
    counter = ReadoutCallCounter()
    original = TowerRuntime.compatibility_quotient_tiers
    monkeypatch.setattr(
        TowerRuntime,
        "compatibility_quotient_tiers",
        counter.wrap_compatibility(original),
    )

    from state_collapser.examples.plate_support_env import PlateSupportEnv, PlateSupportEnvRuntime

    runtime = PlateSupportEnvRuntime(PlateSupportEnv())
    runtime.reset(seed=1)
    runtime.tower_runtime.compatibility_quotient_tiers()

    assert counter.compatibility_calls == 1
