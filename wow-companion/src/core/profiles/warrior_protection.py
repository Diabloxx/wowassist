"""Protection Warrior rotation stub."""
from __future__ import annotations
from .base_rotation import RotationPolicy
from ..state import GameState
from typing import List

class ProtectionWarriorRotation(RotationPolicy):
    spec = "warrior_protection"

    def shortlist(self, state: GameState) -> List[dict]:
        # Minimal stub - add real logic later
        return [
            {'action': 'Shield Slam Target', 'spell_id': '23922'},
            {'action': 'Revenge Target', 'spell_id': '6572'},
            {'action': 'Devastate Target', 'spell_id': '20243'}
        ]

policy = ProtectionWarriorRotation()
