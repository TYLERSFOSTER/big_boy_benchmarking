"""Discovery event structures for Warehouse Gridlock readiness artifacts."""

from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True)
class DiscoveryEvent:
    event_type: str
    state_id: str
    action_id: str
    valid: bool
    invalid_reasons: tuple[str, ...] = ()
    cache_hit: bool = False
    mask_or_query_call: bool = False

    def to_row(self) -> dict[str, object]:
        return {
            "event_type": self.event_type,
            "state_id": self.state_id,
            "action_id": self.action_id,
            "valid": self.valid,
            "invalid_reasons": "|".join(self.invalid_reasons),
            "cache_hit": self.cache_hit,
            "mask_or_query_call": self.mask_or_query_call,
        }


DISCOVERY_FIELDNAMES = (
    "event_type",
    "state_id",
    "action_id",
    "valid",
    "invalid_reasons",
    "cache_hit",
    "mask_or_query_call",
)


def cache_policy_manifest() -> dict[str, object]:
    return {
        "cache_scope": "per_run_per_arm",
        "mask_policy": "none_by_default",
        "query_policy": "explicit_only",
        "invalid_attempts_are_discovery_events": True,
        "claim_boundary": "environment readiness only; no comparison arm is defined",
    }


def summarize_discovery(events: list[DiscoveryEvent]) -> dict[str, object]:
    valid_events = [event for event in events if event.valid]
    invalid_events = [event for event in events if not event.valid]
    return {
        "attempted_ensemble_count": len(events),
        "valid_ensemble_count": len(valid_events),
        "invalid_ensemble_count": len(invalid_events),
        "unique_state_count": len({event.state_id for event in events}),
        "unique_action_count": len({event.action_id for event in events}),
        "cache_hit_count": sum(1 for event in events if event.cache_hit),
        "mask_or_query_call_count": sum(1 for event in events if event.mask_or_query_call),
    }
