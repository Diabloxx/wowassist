"""Offline trainer stub using logged sessions + replay buffer."""
from __future__ import annotations
from .replay_buffer import buffer

def train(steps: int = 1000):  # placeholder
    for _ in range(min(steps, len(buffer.data))):
        pass
