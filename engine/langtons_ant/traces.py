"""Verification primitive for a finite trace ending at a P104 terminal state."""

from __future__ import annotations

from .highway import P104Witness, is_standard_p104_terminal
from .model import State, advance


def terminal_trace_endpoint(initial: State, updates: int, witness: P104Witness) -> State:
    """Replay a declared finite trace and require a genuine P104 terminal endpoint."""

    endpoint = advance(initial, updates)
    if not is_standard_p104_terminal(endpoint, witness):
        raise AssertionError("finite trace does not end at a standard P104 terminal state")
    return endpoint
