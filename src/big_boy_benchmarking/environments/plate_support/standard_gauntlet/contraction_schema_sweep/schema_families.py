"""Schema family and arm definitions for PlateSupport gauntlet Stage 2."""

from __future__ import annotations

from dataclasses import asdict, dataclass


@dataclass(frozen=True)
class SchemaArm:
    """Stable metadata for one schema sweep arm."""

    schema_id: str
    schema_family_id: str
    schema_seed: int
    selection_policy_id: str
    selection_rate: str
    selection_count: str
    state_feature_basis: str
    action_category_basis: str
    edge_basis: str
    schema_mode: str
    expected_role: str
    construction_supported: bool
    unsupported_reason: str

    def to_dict(self) -> dict[str, object]:
        return asdict(self)


def enumerate_schema_arms(
    *,
    schema_families: tuple[str, ...],
    schema_seeds: tuple[int, ...],
    edge_global_numerators: tuple[int, ...],
    valid_nonself_edge_count: int,
) -> tuple[SchemaArm, ...]:
    """Enumerate the configured smoke/dev schema sweep arms."""

    arms: list[SchemaArm] = []
    for seed in schema_seeds:
        if "no_contraction" in schema_families:
            arms.append(
                SchemaArm(
                    schema_id="plate_support_schema_no_contraction_v001",
                    schema_family_id="no_contraction",
                    schema_seed=seed,
                    selection_policy_id="not_applicable",
                    selection_rate="not_applicable",
                    selection_count="not_applicable",
                    state_feature_basis="not_applicable",
                    action_category_basis="not_applicable",
                    edge_basis="not_applicable",
                    schema_mode="none",
                    expected_role="flat_control",
                    construction_supported=True,
                    unsupported_reason="",
                )
            )
        if "upstream_default" in schema_families:
            arms.append(
                SchemaArm(
                    schema_id="plate_support_schema_upstream_default_v001",
                    schema_family_id="upstream_default",
                    schema_seed=seed,
                    selection_policy_id="upstream_default_plate_support_schema",
                    selection_rate="not_applicable",
                    selection_count="not_applicable",
                    state_feature_basis="not_applicable",
                    action_category_basis="not_applicable",
                    edge_basis="plate_support_transition",
                    schema_mode="default",
                    expected_role="reference_noncontrol_schema",
                    construction_supported=True,
                    unsupported_reason="",
                )
            )
        if "action_category" in schema_families:
            for schema_id, category in (
                ("plate_support_schema_plate_motion_actions_v001", "plate_motion"),
                ("plate_support_schema_arm_extension_actions_v001", "arm_extension"),
                ("plate_support_schema_motion_vs_support_actions_v001", "motion_vs_support"),
            ):
                arms.append(
                    _unsupported_arm(
                        schema_id=schema_id,
                        schema_family_id="action_category",
                        schema_seed=seed,
                        action_category_basis=category,
                        reason=(
                            "current upstream PlateSupport probe accepts only schema_mode "
                            "default or none; action-category schema construction is unavailable"
                        ),
                    )
                )
        if "edge_global_noisy_rate" in schema_families:
            for numerator in edge_global_numerators:
                arms.append(
                    _unsupported_arm(
                        schema_id=(
                            "plate_support_schema_edge_global_noisy_rate_"
                            f"{numerator:03d}_over_{valid_nonself_edge_count:03d}_v001"
                        ),
                        schema_family_id="edge_global_noisy_rate",
                        schema_seed=seed,
                        selection_policy_id="edge_global_noisy_rate",
                        selection_rate=f"{numerator}/{valid_nonself_edge_count}",
                        selection_count=str(numerator),
                        edge_basis="valid_nonself_edges",
                        reason=(
                            "current upstream PlateSupport schema surface does not expose "
                            "edge-global selected-edge schema construction"
                        ),
                    )
                )
        if "geometry_coordinate" in schema_families:
            for schema_id, basis in (
                ("plate_support_schema_position_only_v001", "position"),
                ("plate_support_schema_orientation_only_v001", "orientation"),
                ("plate_support_schema_support_pattern_only_v001", "support_pattern"),
                ("plate_support_schema_reachability_pattern_only_v001", "reachability_pattern"),
                ("plate_support_schema_position_support_v001", "position_support"),
            ):
                arms.append(
                    _unsupported_arm(
                        schema_id=schema_id,
                        schema_family_id="geometry_coordinate",
                        schema_seed=seed,
                        state_feature_basis=basis,
                        reason=(
                            "state-feature PlateSupport schema construction is not exposed "
                            "by the current upstream probe/runtime API"
                        ),
                    )
                )
        if "controlled_degeneracy" in schema_families:
            for schema_id, policy in (
                ("plate_support_schema_full_single_block_v001", "full_single_block"),
                ("plate_support_schema_source_local_one_drop_v001", "source_local_one_drop"),
            ):
                arms.append(
                    _unsupported_arm(
                        schema_id=schema_id,
                        schema_family_id="controlled_degeneracy",
                        schema_seed=seed,
                        selection_policy_id=policy,
                        reason=(
                            "controlled degeneracy anchors require schema construction "
                            "surfaces not currently exposed for PlateSupport"
                        ),
                    )
                )
    return tuple(arms)


def _unsupported_arm(
    *,
    schema_id: str,
    schema_family_id: str,
    schema_seed: int,
    reason: str,
    selection_policy_id: str = "not_supported",
    selection_rate: str = "not_applicable",
    selection_count: str = "not_applicable",
    state_feature_basis: str = "not_applicable",
    action_category_basis: str = "not_applicable",
    edge_basis: str = "not_applicable",
) -> SchemaArm:
    return SchemaArm(
        schema_id=schema_id,
        schema_family_id=schema_family_id,
        schema_seed=schema_seed,
        selection_policy_id=selection_policy_id,
        selection_rate=selection_rate,
        selection_count=selection_count,
        state_feature_basis=state_feature_basis,
        action_category_basis=action_category_basis,
        edge_basis=edge_basis,
        schema_mode="not_supported",
        expected_role="unsupported_diagnostic_arm",
        construction_supported=False,
        unsupported_reason=reason,
    )
