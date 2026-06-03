# Human Summary

The artifact set is `complete`: the source binding points at repo-resident
artifacts, and every required file listed by `readout_source.json` is present.

This run compares one matched pair:

- Schema 0: `schema0_no_contraction`;
- Schema 1: `schema1_noisy_rate_one_drop`;
- threshold: `episode_total_reward >= 13.0`;
- persistence rule: 4 qualifying episodes inside a 5-episode window;
- budget: 8 episodes, 1 replicate per arm.

Both arms executed normally and crossed the `13.0` threshold transiently. They
did not satisfy the persistence rule. The current bounded claim is therefore
blocked: this artifact set does not support a speed-to-sustained-hit comparison
between the schemas.

The useful human takeaway is that `13.0` sits near the threshold boundary for
this tiny smoke budget. Earlier probing showed `12.0` sustaining and `15.0`
failing to cross. At `13.0`, both arms touch the threshold but fail sustained
adequacy.
