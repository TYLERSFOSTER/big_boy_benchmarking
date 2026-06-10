# Result Readout

The `masked_8ep_001` diagnostic completed successfully and produced a tie.

Direct masked control and tower live-lift control both reported:

- mean total reward: `379.9375`;
- median total reward: `341.5`;
- terminal successes: `0`;
- mean final correct boxes: `0.0`;
- mean final correct robots: `6.1875`;
- mean selected valid steps: `128.0`;
- mean selected invalid steps: `0.0`.

The paired comparison table contains 16 pairs and every pair is a tie. The tower arm therefore does not show an advantage in this run.

The important positive result is diagnostic rather than performance-based:

- both arms used equal immediate candidate-set masking;
- neither arm used successor-state `Out` for selection;
- tower live lifting had zero failures;
- the candidate surface included multi-robot proposals up to 8 active robots.

The important negative or limiting result is that neither arm solved the task: terminal success count is zero and boxes did not reach targets.
