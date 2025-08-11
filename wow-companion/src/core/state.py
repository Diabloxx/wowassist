"""State modeling for WoW Companion.
Defines pydantic models for structured reasoning and a builder from vision/OCR parts.
"""
from __future__ import annotations
from typing import List, Dict, Optional
from pydantic import BaseModel, Field
import time

class Resource(BaseModel):
    current: float
    max: float

class Aura(BaseModel):
    name: str
    stacks: int = 1
    duration_s: float = 0.0

class Cooldown(BaseModel):
    spell: str
    remaining_s: float

class CombatEvent(BaseModel):
    timestamp: float
    text: str

class GameState(BaseModel):
    timestamp: float
    player_class: str
    spec: str
    player_hp: Resource
    player_power: Resource
    target_hp: Optional[Resource] = None
    buffs: List[Aura] = Field(default_factory=list)
    debuffs: List[Aura] = Field(default_factory=list)
    cooldowns: List[Cooldown] = Field(default_factory=list)
    encounter_phase: Optional[str] = None
    party_status: Dict[str, Resource] = Field(default_factory=dict)
    combat_log: List[CombatEvent] = Field(default_factory=list)

class GameStateBuilder:
    """Assembles a GameState from parsed frame components.

    The input 'parts' dict is expected to contain already extracted numeric or textual
    info from vision/ocr modules. This keeps heavy CV out of the model layer.
    """
    def __init__(self, player_class: str, spec: str):
        self.player_class = player_class
        self.spec = spec

    def assemble(self, parts: dict, text_events: list[str]) -> GameState:
        now = time.time()
        # Graceful fallbacks
        player_hp = parts.get('player_hp', {'current': 0, 'max': 1})
        player_power = parts.get('player_power', {'current': 0, 'max': 1})
        target_hp = parts.get('target_hp')
        buffs = [Aura(**b) for b in parts.get('buffs', [])]
        debuffs = [Aura(**d) for d in parts.get('debuffs', [])]
        cooldowns = [Cooldown(**c) for c in parts.get('cooldowns', [])]
        party_status = {}
        for name, res in parts.get('party_status', {}).items():
            try:
                party_status[name] = Resource(**res)
            except Exception:
                continue
        combat_log = [CombatEvent(timestamp=now, text=t) for t in text_events[-20:]]
        return GameState(
            timestamp=now,
            player_class=self.player_class,
            spec=self.spec,
            player_hp=Resource(**player_hp),
            player_power=Resource(**player_power),
            target_hp=Resource(**target_hp) if target_hp else None,
            buffs=buffs,
            debuffs=debuffs,
            cooldowns=cooldowns,
            encounter_phase=parts.get('encounter_phase'),
            party_status=party_status,
            combat_log=combat_log,
        )
