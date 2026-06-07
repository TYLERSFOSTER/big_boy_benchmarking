"""Training-health classification for PlateSupport gauntlet Stage 4."""

from __future__ import annotations


def classify_training_health(row: dict[str, object]) -> tuple[str, str]:
    """Classify candidate training health from table-backed aggregate counts."""

    if int(row.get("runtime_failure_count", 0)) > 0:
        return "untrainable_runtime_failure", "runtime failure recorded during training"
    if int(row.get("artifact_complete", 0)) != 1:
        return "artifact_incomplete", "required Stage 4 event artifacts are incomplete"
    if int(row.get("concrete_step_count", 0)) <= 0:
        return "untrainable_no_concrete_steps", "no concrete runtime steps were observed"
    if int(row.get("lift_success_count", 0)) <= 0:
        return "untrainable_no_lift_success", "no executable tower lift was observed"
    if int(row.get("learner_update_count", 0)) <= 0:
        return "untrainable_no_learner_updates", "no learner update was observed"
    if int(row.get("blocked_controller_step_count", 0)) > 0:
        return "trainable_warning", "training ran, but controller-blocked steps were observed"
    return "trainable_clean", "concrete steps, lift success, and learner updates observed"
