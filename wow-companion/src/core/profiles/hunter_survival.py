"""Survival Hunter base (retail-ish placeholder) profile stub."""
from __future__ import annotations
from .base_rotation import RotationPolicy
from ..state import GameState
from typing import List

class SurvivalHunterRotation(RotationPolicy):
    spec = "hunter_survival"
    def _cd(self, state: GameState, name: str):
        return next((c for c in state.cooldowns if c.spell == name), None)
    def shortlist(self, state: GameState) -> List[dict]:
        acts: List[dict] = []
        explosive = self._cd(state, 'Explosive Shot')
        if explosive and explosive.remaining_s <= 0:
            acts.append({'action': 'Explosive Shot', 'spell_id': '53301', 'prio': 1, 'reason': 'Primary damage'})
        acts.append({'action': 'Serpent Sting', 'spell_id': '1978', 'prio': 2, 'reason': 'Maintain DoT'})
        if self.since('arcane_shot') > 2.0:
            acts.append({'action': 'Arcane Shot', 'spell_id': '3044', 'prio': 3, 'reason': 'Focus dump'})
        acts.append({'action': 'Cobra Shot', 'spell_id': '77767', 'prio': 4, 'reason': 'Focus regen'})
        return self.sort_actions(acts)

policy = SurvivalHunterRotation()
