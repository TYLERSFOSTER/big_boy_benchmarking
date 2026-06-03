# Threshold Policy Readout

- Threshold policy id: `counterpoint_total_space_sustained_reward_v001`.
- Metric: `episode_total_reward`.
- Threshold value: `13.0`.
- Window length: `5`.
- Required count: `4`.
- Comparison: `greater_than_or_equal`.

## Reader Translation

An episode counts as a threshold hit when its total reward is at least `13.0`.
The run counts as a sustained hit only if at least 4 episodes in a 5-episode
window meet that threshold.

For the current artifact set:

| Schema | Best Observed Window Hit Count | Required Count | Result |
| --- | ---: | ---: | --- |
| `schema0_no_contraction` | 3 | 4 | transient only |
| `schema1_noisy_rate_one_drop` | 1 | 4 | transient only |

This is why the comparison claim is blocked even though both arms have episode
rewards near the threshold and both crossed it at least once.
