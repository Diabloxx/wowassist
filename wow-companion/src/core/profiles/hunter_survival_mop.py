"""Survival Hunter (MoP Classic) rotation shortlist logic.

Focus management simplified: we don't simulate exact focus; instead we rely on
cooldown placeholders and assumed readiness expressed via cooldown objects.
Shortlist expresses priority ordering for LLM selection.
"""
from __future__ import annotations
from .base_rotation import RotationPolicy
from ..state import GameState
from typing import List

class SurvivalHunterMoPRotation(RotationPolicy):
    spec = "hunter_survival_mop"

    def _cd(self, state: GameState, name: str):
        return next((c for c in state.cooldowns if c.spell == name), None)

    def shortlist(self, state: GameState) -> List[dict]:
        acts: List[dict] = []
        target_pct = 1.0
        if state.target_hp:
            target_pct = state.target_hp.current / max(1,state.target_hp.max)

        explosive = self._cd(state, 'Explosive Shot')
        black_arrow = self._cd(state, 'Black Arrow')
        kill_shot = self._cd(state, 'Kill Shot')
        serpent_sting = self._cd(state, 'Serpent Sting')

        # Core single-target priorities
        if explosive and explosive.remaining_s <= 0:
            acts.append({'action': 'Explosive Shot', 'spell_id': '53301', 'prio': 1, 'reason': 'Primary nuke'})
        if target_pct < 0.2 and kill_shot and kill_shot.remaining_s <= 0:
            acts.append({'action': 'Kill Shot', 'spell_id': '53351', 'prio': 2, 'reason': 'Execute phase'})
        if black_arrow and black_arrow.remaining_s <= 0:
            acts.append({'action': 'Black Arrow', 'spell_id': '3674', 'prio': 3, 'reason': 'DoT & LnL procs'})
        if serpent_sting and serpent_sting.remaining_s <= 0:
            acts.append({'action': 'Serpent Sting', 'spell_id': '1978', 'prio': 4, 'reason': 'Maintain DoT'})
        # Focus dump vs generator (Arcane vs Cobra) – we approximate by alternating via time since last use
        if self.since('arcane_shot') > 2.0:
            acts.append({'action': 'Arcane Shot', 'spell_id': '3044', 'prio': 5, 'reason': 'Focus dump'})
        acts.append({'action': 'Cobra Shot', 'spell_id': '77767', 'prio': 6, 'reason': 'Focus regen'})
        return self.sort_actions(acts)

policy = SurvivalHunterMoPRotation()
