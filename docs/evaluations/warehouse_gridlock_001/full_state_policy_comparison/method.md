# Method

This evaluation implements `warehouse_full_state_full_action_policy_contract_v001` for Warehouse Gridlock.

The first model family is `warehouse_linear_factorized_softmax_policy_v001`. It scores robot commands from
full-state features and updates reusable feature weights online. It is not a
backprop/neural model.

The concrete resolver is `bounded_deterministic_repair_with_all_stay_fallback_v001`. It uses immediate
transition validity only and logs repairs/projections. It does not inspect
successor `Out`.
