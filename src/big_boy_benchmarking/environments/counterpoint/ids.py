"""Canonical ids for the counterpoint hidden-graph benchmark family."""

ENVIRONMENT_FAMILY_ID = "counterpoint_symbolic_v001"
LEGALITY_CONTRACT_ID = "counterpoint_legality_local_v001"
REWARD_BUNDLE_ID = "counterpoint_reward_local_v001"
EDGE_LABEL_CONTRACT_ID = "counterpoint_edge_labels_local_v001"
INITIAL_STATE_POLICY_ID = "counterpoint_initial_states_v001"
TERMINAL_POLICY_ID = "counterpoint_terminal_horizon_v001"
ACTION_MASK_POLICY_ID = "counterpoint_legal_action_mask_v001"
EMPTY_SCHEMA_ID = "counterpoint_empty_schema_v001"
RANDOM_BALANCED_SCHEMA_FAMILY_ID = "counterpoint_random_balanced_schema_v001"
RANDOM_UNBALANCED_SCHEMA_FAMILY_ID = "counterpoint_random_unbalanced_schema_v001"
STRUCTURED_MOTION_SCHEMA_ID = "counterpoint_motion_schema_v001"
PROJECTION_AUDIT_SCHEMA_ID = "counterpoint_projection_audit_schema_v001"
BAD_SCHEMA_ID = "counterpoint_bad_schema_v001"
ONE_THIRD_SCHEMA_FAMILY_ID = "counterpoint_one_third_schema_v001"
ONE_THIRD_OUTGOING_SCHEMA_ID = "counterpoint_one_third_outgoing_schema_v001"
OUTGOING_FRACTION_SWEEP_SCHEMA_FAMILY_ID = (
    "counterpoint_outgoing_fraction_sweep_schema_v001"
)
OUTGOING_FRACTION_SWEEP_SCHEMA_ID = (
    "counterpoint_outgoing_fraction_sweep_single_block_schema_v001"
)
NOISY_RATE_CONTRACTION_EVALUATION_ID = (
    "counterpoint_noisy_rate_contraction_diagnostics_v001"
)
NOISY_RATE_CONTRACTION_SCHEMA_FAMILY_ID = (
    "counterpoint_noisy_rate_contraction_schema_v001"
)
NOISY_RATE_CONTRACTION_SCHEMA_ID = (
    "counterpoint_noisy_rate_contraction_single_block_schema_v001"
)
NOISY_RATE_FULL_TOWER_TRAINING_EVALUATION_ID = (
    "counterpoint_noisy_rate_full_tower_training_diagnostic_v001"
)
NOISY_RATE_FULL_TOWER_TRAINING_RUN_FAMILY_ID = (
    "counterpoint_symbolic_v001_noisy_rate_full_tower_training_diagnostic_v001"
)
NOISY_RATE_FULL_TOWER_TRAINING_RUN_MODE_ID = (
    "diagnostic_noisy_rate_full_tower_training"
)

CANONICAL_IDS = {
    "environment_family_id": ENVIRONMENT_FAMILY_ID,
    "legality_contract_id": LEGALITY_CONTRACT_ID,
    "reward_bundle_id": REWARD_BUNDLE_ID,
    "edge_label_contract_id": EDGE_LABEL_CONTRACT_ID,
    "initial_state_policy_id": INITIAL_STATE_POLICY_ID,
    "terminal_policy_id": TERMINAL_POLICY_ID,
    "action_mask_policy_id": ACTION_MASK_POLICY_ID,
    "empty_schema_id": EMPTY_SCHEMA_ID,
    "random_balanced_schema_family_id": RANDOM_BALANCED_SCHEMA_FAMILY_ID,
    "random_unbalanced_schema_family_id": RANDOM_UNBALANCED_SCHEMA_FAMILY_ID,
    "structured_motion_schema_id": STRUCTURED_MOTION_SCHEMA_ID,
    "projection_audit_schema_id": PROJECTION_AUDIT_SCHEMA_ID,
    "bad_schema_id": BAD_SCHEMA_ID,
    "one_third_schema_family_id": ONE_THIRD_SCHEMA_FAMILY_ID,
    "one_third_outgoing_schema_id": ONE_THIRD_OUTGOING_SCHEMA_ID,
    "outgoing_fraction_sweep_schema_family_id": OUTGOING_FRACTION_SWEEP_SCHEMA_FAMILY_ID,
    "outgoing_fraction_sweep_schema_id": OUTGOING_FRACTION_SWEEP_SCHEMA_ID,
    "noisy_rate_contraction_evaluation_id": NOISY_RATE_CONTRACTION_EVALUATION_ID,
    "noisy_rate_contraction_schema_family_id": NOISY_RATE_CONTRACTION_SCHEMA_FAMILY_ID,
    "noisy_rate_contraction_schema_id": NOISY_RATE_CONTRACTION_SCHEMA_ID,
    "noisy_rate_full_tower_training_evaluation_id": (
        NOISY_RATE_FULL_TOWER_TRAINING_EVALUATION_ID
    ),
    "noisy_rate_full_tower_training_run_family_id": (
        NOISY_RATE_FULL_TOWER_TRAINING_RUN_FAMILY_ID
    ),
    "noisy_rate_full_tower_training_run_mode_id": (
        NOISY_RATE_FULL_TOWER_TRAINING_RUN_MODE_ID
    ),
}
