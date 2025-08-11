"""Lightweight contextual bandit for adjusting action priorities."""
from __future__ import annotations
import numpy as np
import json, time, os
from typing import Dict, Any
from ..config import config

class BanditLearner:
    def __init__(self):
        self.weights: Dict[str, float] = {}
        self.lr = 0.05
        self.log_path = os.path.join(config.LOG_DIR, f"bandit_{int(time.time())}.jsonl")

    def _features(self, state) -> np.ndarray:
        # Simple feature vector: hp %, power %, num buffs, num cds ready
        hp_pct = state.player_hp.current / max(1.0, state.player_hp.max)
        pw_pct = state.player_power.current / max(1.0, state.player_power.max)
        buffs = len(state.buffs)
        cds_ready = sum(1 for c in state.cooldowns if c.remaining_s <= 0.1)
        return np.array([hp_pct, pw_pct, buffs/20.0, cds_ready/20.0])

    def score(self, action: str, state) -> float:
        return self.weights.get(action, 0.0)

    def update(self, state, chosen_action: str, reward: float):
        feat = self._features(state)
        w = self.weights.get(chosen_action, 0.0)
        # linear bandit style incremental update
        grad = reward * feat.mean()
        self.weights[chosen_action] = w + self.lr * grad
        with open(self.log_path, 'a', encoding='utf-8') as f:
            f.write(json.dumps({
                't': time.time(), 'action': chosen_action, 'reward': reward, 'weight': self.weights[chosen_action]
            }) + '\n')

learning_agent = BanditLearner()
