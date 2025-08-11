"""Reward shaping heuristics."""
from __future__ import annotations
from ..src.core.reasoner import ActionDecision  # type: ignore

def compute_reward(prev_state, new_state, decision: ActionDecision) -> float:
    # Placeholder: reward positive if player hp increased or target hp decreased
    d_hp = (new_state.player_hp.current - prev_state.player_hp.current)
    # assume target hp drop beneficial
    if new_state.target_hp and prev_state.target_hp:
        d_target = prev_state.target_hp.current - new_state.target_hp.current
    else:
        d_target = 0
    return 0.0001 * d_hp + 0.00005 * d_target
