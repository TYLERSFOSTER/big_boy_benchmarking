from importlib import import_module

STAGE_BASE = "big_boy_benchmarking.environments.plate_support.standard_gauntlet"

claim_logic = import_module(f"{STAGE_BASE}.paired_replicate_comparison.claim_logic")
seed_bundles = import_module(f"{STAGE_BASE}.paired_replicate_comparison.seed_bundles")

build_paired_seed_bundles = seed_bundles.build_paired_seed_bundles
classify_paired_claim = claim_logic.classify_paired_claim


def test_paired_seed_bundles_are_shared_by_pair() -> None:
    bundles = build_paired_seed_bundles(base_seed=10, replicate_count=2)

    assert bundles[0].pair_id == "pairrep000"
    assert bundles[1].pair_id == "pairrep001"
    assert bundles[0].episode_seed(0) == bundles[0].environment_seed
    assert bundles[0].episode_seed(5) == bundles[0].environment_seed + 5
    assert bundles[0].environment_seed != bundles[1].environment_seed


def test_claim_classifier_reports_positive_negative_and_no_pairs() -> None:
    positive = classify_paired_claim(
        paired_rows=[
            {
                "baseline_arm_id": "direct",
                "candidate_arm_id": "tower",
                "pair_complete": "1",
                "target_hit_rate_delta": 0.25,
            }
        ],
        direct_arm_id="direct",
        candidate_arm_id="tower",
    )
    assert positive["claim_status"] == "paired_comparison_positive_signal"

    negative = classify_paired_claim(
        paired_rows=[
            {
                "baseline_arm_id": "direct",
                "candidate_arm_id": "tower",
                "pair_complete": "1",
                "target_hit_rate_delta": -0.125,
            }
        ],
        direct_arm_id="direct",
        candidate_arm_id="tower",
    )
    assert negative["claim_status"] == "paired_comparison_negative_signal"

    no_pairs = classify_paired_claim(
        paired_rows=[
            {
                "baseline_arm_id": "direct",
                "candidate_arm_id": "tower",
                "pair_complete": "0",
                "target_hit_rate_delta": 1.0,
            }
        ],
        direct_arm_id="direct",
        candidate_arm_id="tower",
    )
    assert no_pairs["claim_status"] == "paired_comparison_inconclusive"
    assert no_pairs["complete_pair_count"] == 0
