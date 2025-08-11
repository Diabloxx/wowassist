"""Simple replay buffer for offline training."""
from __future__ import annotations
from collections import deque
from typing import Deque, Any

class ReplayBuffer:
    def __init__(self, capacity: int = 5000):
        self.capacity = capacity
        self.data: Deque[Any] = deque(maxlen=capacity)

    def add(self, item):
        self.data.append(item)

    def sample(self, n: int):
        import random
        n = min(n, len(self.data))
        return random.sample(self.data, n)

buffer = ReplayBuffer()
