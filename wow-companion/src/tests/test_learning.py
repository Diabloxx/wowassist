from src.core.learning import learning_agent
from types import SimpleNamespace

class DummyState(SimpleNamespace):
    pass

def test_learning_update():
    state = SimpleNamespace(player_hp=SimpleNamespace(current=50, max=100),
                            player_power=SimpleNamespace(current=40, max=100),
                            buffs=[], cooldowns=[])
    learning_agent.update(state, 'Smite Target', 1.0)
    assert 'Smite Target' in learning_agent.weights
