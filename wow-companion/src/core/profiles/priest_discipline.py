"""Discipline Priest rotation fundamentals."""
from __future__ import annotations
from .base_rotation import RotationPolicy
from ..state import GameState
from typing import List

class DisciplinePriestRotation(RotationPolicy):
    spec = "priest_discipline"

    def _cd(self, state: GameState, name: str):
        return next((c for c in state.cooldowns if c.spell == name), None)

    def shortlist(self, state: GameState) -> List[dict]:
        acts: List[dict] = []
        player_hp_pct = state.player_hp.current / max(1,state.player_hp.max)
        shield_cd = self._cd(state, 'Power Word: Shield')
        penance_cd = self._cd(state, 'Penance')
        archangel_cd = self._cd(state, 'Archangel')

        # Defensive shield if player low
        if player_hp_pct < 0.5 and shield_cd and shield_cd.remaining_s <= 0:
            acts.append({'action': 'Power Word: Shield Self', 'spell_id': '17', 'prio': 1, 'category': 'defensive', 'reason': 'Low self HP'})

        # Maintain Atonement via offensive rotation
        if penance_cd and penance_cd.remaining_s <= 0:
            acts.append({'action': 'Penance Target', 'spell_id': '47540', 'prio': 2, 'category': 'core', 'reason': 'High dmg + atonement'})
        # Archangel if available and several allies injured (simplified check)
        avg_party_hp = 1.0
        if state.party_status:
            avg_party_hp = sum(r.current/max(1,r.max) for r in state.party_status.values())/len(state.party_status)
        if avg_party_hp < 0.85 and archangel_cd and archangel_cd.remaining_s <= 0:
            acts.append({'action': 'Archangel Self', 'spell_id': '81700', 'prio': 3, 'category': 'cooldown', 'reason': 'Throughput boost'})

        # Shield tank / target for mitigation (placeholder: choose first party member)
        if shield_cd and shield_cd.remaining_s <= 0:
            target_name = next(iter(state.party_status.keys()), 'Tank')
            acts.append({'action': f'Power Word: Shield {target_name}', 'spell_id': '17', 'prio': 4, 'category': 'mitigation', 'reason': 'Rapture cycle'})

        # Holy Fire then Smite filler
        acts.append({'action': 'Holy Fire Target', 'spell_id': '14914', 'prio': 5, 'category': 'filler', 'reason': 'Efficient damage-heal'})
        acts.append({'action': 'Smite Target', 'spell_id': '585', 'prio': 6, 'category': 'filler', 'reason': 'Damage to heal conversion'})
        return self.sort_actions(acts)

policy = DisciplinePriestRotation()
