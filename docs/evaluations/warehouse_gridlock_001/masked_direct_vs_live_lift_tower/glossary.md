# Glossary

- Immediate inadmissibility mask: current-state filtering that removes generated actions that cannot legally execute now.
- Candidate-set mask: a mask over the bounded generated proposal set, not over every possible Warehouse ensemble action.
- Coordination-ready candidate set: a bounded proposal set that includes one-active and multi-active robot moves rather than only one-active moves.
- Live lift: tower state-lift hygiene requiring a lifted representative to have nonempty generated outgoing actions.
- Successor lookahead: using the successor state's outgoing actions to decide whether to choose the current action. This evaluation forbids it for both arms.
- Generated/discovered surface: the scoped runtime surface built from generated candidates and queried valid transitions.
- Full action surface: the complete primitive Warehouse action space, `5^32`; this evaluation does not enumerate it.
