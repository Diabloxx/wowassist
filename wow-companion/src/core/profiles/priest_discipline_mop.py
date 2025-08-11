"""Discipline Priest (Mists of Pandaria Classic) rotation differences.

Simplified: MoP gameplay emphasizes Atonement via Penance, Holy Fire, Smite,
Spirit Shell (later patch), and Power Word: Shield management with weakened soul.
This stub adapts shortlist slightly for classic_mop flavor.
"""
from __future__ import annotations
from .base_rotation import RotationPolicy
from ..state import GameState
from typing import List

class DisciplinePriestMoPRotation(RotationPolicy):
    spec = "priest_discipline_mop"

    def _cd(self, state: GameState, name: str):
        return next((c for c in state.cooldowns if c.spell == name), None)

    def shortlist(self, state: GameState) -> List[dict]:
        actions: List[dict] = []
        # Basic health heuristics
        avg_party_hp = 1.0
        if state.party_status:
            avg_party_hp = sum(r.current / max(1,r.max) for r in state.party_status.values()) / len(state.party_status)
        player_hp_pct = state.player_hp.current / max(1,state.player_hp.max)

        penance_cd = self._cd(state, 'Penance')
        shield_cd = self._cd(state, 'Power Word: Shield')
        spirit_shell_cd = self._cd(state, 'Spirit Shell')
        archangel_cd = self._cd(state, 'Archangel')
        power_infusion_cd = self._cd(state, 'Power Infusion')

        # If big damage incoming heuristic (party below 80%) consider Spirit Shell window
        if avg_party_hp < 0.8 and spirit_shell_cd and spirit_shell_cd.remaining_s <= 0:
            # Sequence: Archangel -> Spirit Shell -> Prayer of Healing spam (represented)
            if archangel_cd and archangel_cd.remaining_s <= 0:
                actions.append({'action': 'Archangel Self', 'spell_id': '81700'})
            actions.append({'action': 'Spirit Shell Prep', 'spell_id': '109964'})
            # Represent Prayer of Healing as generic action so LLM may choose wait/continue casting
            actions.append({'action': 'Prayer of Healing Group', 'spell_id': '596'})
            return actions

        # Emergency single target: low player
        if player_hp_pct < 0.5 and shield_cd and shield_cd.remaining_s <= 0:
            actions.append({'action': 'Power Word: Shield Self', 'spell_id': '17'})

        # Shield low party member for Rapture cycling
        low_party = [n for n,r in state.party_status.items() if r.current / max(1,r.max) < 0.55]
        if low_party and shield_cd and shield_cd.remaining_s <= 0:
            actions.append({'action': f'Power Word: Shield {low_party[0]}', 'spell_id': '17'})

        # Penance always high priority (offensive or defensive)
        if penance_cd and penance_cd.remaining_s <= 0:
            actions.append({'action': 'Penance Target', 'spell_id': '47540'})

        # Offensive maintenance: Holy Fire -> Smite filler
        actions.append({'action': 'Holy Fire Target', 'spell_id': '14914'})
        actions.append({'action': 'Smite Target', 'spell_id': '585'})
        return actions

policy = DisciplinePriestMoPRotation()
