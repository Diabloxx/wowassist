"""Abstract rotation policy base class with helper utilities.

Each concrete policy should return a list of action dicts. Recommended keys:
  action: human readable instruction
  spell_id: numeric id (string) if known
  prio: lower number = higher priority (int or float)
  category: e.g. 'defensive','cooldown','filler'
  reason: short rationale phrase

The reasoning LLM can then leverage this structured shortlist to select a
single action. If no 'prio' provided the original order is preserved.
"""
from __future__ import annotations
from abc import ABC, abstractmethod
from typing import List, Iterable
import time
from ..state import GameState


class RotationPolicy(ABC):
    spec: str = "base"

    def __init__(self):
        self._last_use: dict[str, float] = {}

    # --- utility methods ---
    def now(self) -> float:
        return time.time()

    def since(self, key: str) -> float:
        return self.now() - self._last_use.get(key, 0.0)

    def mark(self, key: str):
        self._last_use[key] = self.now()

    def sort_actions(self, actions: Iterable[dict]) -> List[dict]:
        acts = list(actions)
        if not acts:
            return acts
        if all('prio' in a for a in acts):
            acts.sort(key=lambda a: a['prio'])
        return acts

    @abstractmethod
    def shortlist(self, state: GameState) -> List[dict]:
        raise NotImplementedError

    def defensives(self, state: GameState) -> List[dict]:  # optional hook
        return []
