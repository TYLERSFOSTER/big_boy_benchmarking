"""Schema family and arm definitions for PlateSupport gauntlet Stage 2."""

from __future__ import annotations

from dataclasses import asdict, dataclass

from big_boy_benchmarking.environments.plate_support.standard_gauntlet.contraction_schema_sweep.source_local_ratio_schema import (
    source_local_ratio_iterated_schema_id,
    source_local_ratio_schema_id,
)


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
    ratio_numerator: int | None = None
    ratio_denominator: int | None = None
    max_iterations: int | None = None
    selector_rule_id: str = "not_applicable"
    selection_mode: str = "not_applicable"

    def to_dict(self) -> dict[str, object]:
        return asdict(self)


def enumerate_schema_arms(
    *,
    schema_families: tuple[str, ...],
    schema_seeds: tuple[int, ...],
    source_local_ratio_numerators: tuple[int, ...],
    source_local_ratio_denominator: int,
    edge_global_numerators: tuple[int, ...],
    valid_nonself_edge_count: int,
    iterated_source_local_ratio_numerators: tuple[int, ...] = (),
    iterated_source_local_ratio_denominators: tuple[int, ...] = (),
    iterated_source_local_max_iterations: int = 32,
    iterated_source_local_selector_rule_id: str = "not_applicable",
    iterated_source_local_selection_mode: str = "not_applicable",
    iterated_source_local_schema_seeds: tuple[int, ...] | None = None,
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
        if "source_local_ratio" in schema_families:
            for numerator in source_local_ratio_numerators:
                arms.append(
                    SchemaArm(
                        schema_id=source_local_ratio_schema_id(
                            numerator,
                            source_local_ratio_denominator,
                        ),
                        schema_family_id="source_local_ratio",
                        schema_seed=seed,
                        selection_policy_id="source_local_outgoing_ratio_catch",
                        selection_rate=f"{numerator}/{source_local_ratio_denominator}",
                        selection_count="computed_per_source_with_min_1",
                        state_feature_basis="not_applicable",
                        action_category_basis="not_applicable",
                        edge_basis="valid_nonself_outgoing_edges_by_source",
                        schema_mode="source_local_ratio",
                        expected_role="candidate_probe",
                        construction_supported=True,
                        unsupported_reason="",
                        ratio_numerator=numerator,
                        ratio_denominator=source_local_ratio_denominator,
                        max_iterations=1,
                        selector_rule_id="source_local_outgoing_ratio_catch",
                        selection_mode="legacy_source_local_ceil_prefix",
                    )
                )
        if "source_local_ratio_iterated" in schema_families:
            if iterated_source_local_schema_seeds is None:
                iterated_seeds = (seed,)
            elif seed == schema_seeds[0]:
                iterated_seeds = iterated_source_local_schema_seeds
            else:
                iterated_seeds = ()
            for iterated_seed in iterated_seeds:
                for denominator in iterated_source_local_ratio_denominators:
                    for numerator in iterated_source_local_ratio_numerators:
                        arms.append(
                            SchemaArm(
                                schema_id=source_local_ratio_iterated_schema_id(
                                    numerator,
                                    denominator,
                                    iterated_source_local_max_iterations,
                                ),
                                schema_family_id="source_local_ratio_iterated",
                                schema_seed=iterated_seed,
                                selection_policy_id=(
                                    "source_local_quotient_representative_stable_rate"
                                ),
                                selection_rate=f"{numerator}/{denominator}",
                                selection_count=(
                                    "threshold_selected_per_quotient_source_component"
                                ),
                                state_feature_basis="current_quotient_component",
                                action_category_basis="primitive_action_identity_preserved",
                                edge_basis=(
                                    "quotient_representative_valid_nonself_edges_by_"
                                    "source_component"
                                ),
                                schema_mode="source_local_ratio_iterated",
                                expected_role="many_tier_candidate_probe",
                                construction_supported=True,
                                unsupported_reason="",
                                ratio_numerator=numerator,
                                ratio_denominator=denominator,
                                max_iterations=iterated_source_local_max_iterations,
                                selector_rule_id=iterated_source_local_selector_rule_id,
                                selection_mode=iterated_source_local_selection_mode,
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
