# Seed Bundles

The benchmark does not treat a lone integer as a complete stochastic identity.

A seed bundle records separate seeds for environment, schema, learner,
controller, diagnostic sampling, and artifact sampling. The replicate index is
part of the bundle identity.

The seed bundle is the unit of reproducible stochastic identity. The replicate
is the unit of uncertainty.

The first serious counterpoint learning evaluation also has a schema seed
suite. Random balanced and random unbalanced schema arms expand over that
schema seed suite; they must not collapse serious evidence into a single
unmarked random schema seed.

Direct arms and fixed-schema tower arms use the seed bundle replicate suite.
Random schema tower arms use both the seed bundle replicate suite and the
schema seed suite.

See also:

```text
docs/design/shared_benchmark_machinery/01_001_shared_benchmark_machinery_design.md
docs/methods/counterpoint_serious_learning.md
```
