"""Candidate selection policy for PlateSupport gauntlet Stage 3."""

POLICY_ID = "plate_support_candidate_selection_policy_v001"


def candidate_selection_policy_manifest() -> dict[str, object]:
    """Return the serializable Stage 3 selection policy."""

    return {
        "policy_id": POLICY_ID,
        "priority_order": [
            "selected_control_anchor",
            "selected_training_candidate",
            "selected_warning_candidate",
            "selected_degeneracy_anchor",
            "blocked_candidate",
        ],
        "clean_candidate_rule": (
            "eligible_signal, nonflat_structured, max_depth > 1, nonzero executable surface"
        ),
        "warning_candidate_rule": "warning_signal only when explicitly allowed by config",
        "control_anchor_rule": "control_anchor rows are retained for control/diagnostic use",
        "degeneracy_anchor_rule": "at most one degeneracy anchor retained as diagnostic-only",
        "blocked_rule": "blocked_signal and construction_failed rows are retained, not dropped",
        "performance_claim": "selection score is metadata only and not performance evidence",
    }
