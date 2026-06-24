"""Stable identifiers for Warehouse Gridlock full-tower GPU PPO."""

from __future__ import annotations

WAREHOUSE_GRIDLOCK_FULL_TOWER_GPU_PPO_EVALUATION_ID = (
    "warehouse_gridlock_full_tower_gpu_ppo_v001"
)

WAREHOUSE_GRIDLOCK_DIRECT_NO_CONTRACTION_ARM_ID = (
    "warehouse_direct_no_contraction_full_tower_ppo"
)
WAREHOUSE_GRIDLOCK_TOWER_FIRST_NONTRIVIAL_ARM_ID = (
    "warehouse_tower_first_nontrivial_full_tower_ppo"
)
WAREHOUSE_GRIDLOCK_FULL_TOWER_GPU_PPO_ACTIVE_ARM_IDS = (
    WAREHOUSE_GRIDLOCK_DIRECT_NO_CONTRACTION_ARM_ID,
    WAREHOUSE_GRIDLOCK_TOWER_FIRST_NONTRIVIAL_ARM_ID,
)

WAREHOUSE_GRIDLOCK_NO_CONTRACTION_SCHEMA_ID = "schema0_no_contraction"
WAREHOUSE_GRIDLOCK_SOURCE_LOCAL_RATIO_SCHEMA_ID = (
    "warehouse_source_local_ratio_009_over_010_v001"
)

WAREHOUSE_GRIDLOCK_POINTWISE_LIFTABILITY_SEMANTICS_ID = (
    "state_collapser_v072_partition_tower_pointwise_executable_liftability"
)
WAREHOUSE_GRIDLOCK_FULL_TOWER_GPU_PPO_ARTIFACT_CONTRACT_ID = (
    "warehouse_gridlock_full_tower_gpu_ppo_artifact_contract_v001"
)

WAREHOUSE_GRIDLOCK_PPO_RECORD_SCHEMA_VERSION = "warehouse_gridlock_ppo_record_v001"
WAREHOUSE_GRIDLOCK_GEOMETRY_RECORD_SCHEMA_VERSION = (
    "warehouse_gridlock_geometry_record_v001"
)
WAREHOUSE_GRIDLOCK_DECISION_CONTEXT_SCHEMA_VERSION = (
    "warehouse_gridlock_decision_context_v001"
)
WAREHOUSE_GRIDLOCK_ROLLOUT_SAMPLE_SCHEMA_VERSION = (
    "warehouse_gridlock_rollout_sample_v001"
)
WAREHOUSE_GRIDLOCK_RECORD_TOKENIZATION_SCHEMA_VERSION = (
    "warehouse_gridlock_record_tokenization_v001"
)

WAREHOUSE_GRIDLOCK_TIER_DIRECTION_CONVENTION = (
    "tier_0_uppermost__i_to_i_plus_1_moves_down"
)

WAREHOUSE_GRIDLOCK_SOURCE_AUTHORITY_FILES = (
    "docs/design/svg_physical_system_designs/warehouse_gridlock_001/warehouse_001.md",
    "docs/design/svg_physical_system_designs/warehouse_gridlock_001/01_001_warehouse_gridlock_environment_blueprint.md",
    "docs/design/svg_physical_system_designs/warehouse_gridlock_001/01_003_warehouse_gridlock_environment_implementation_log.md",
    "docs/design/svg_physical_system_designs/warehouse_gridlock_001/04_gpu_rl_training_loop/005_warehouse_gridlock_full_tower_gpu_ppo_blueprint.md",
    "docs/design/svg_physical_system_designs/warehouse_gridlock_001/04_gpu_rl_training_loop/006_warehouse_gridlock_full_tower_gpu_ppo_implementation_workplan.md",
)
