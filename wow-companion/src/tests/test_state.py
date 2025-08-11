from src.core.state import GameStateBuilder

def test_state_builder_basic():
    b = GameStateBuilder('Priest','Discipline')
    parts = {'player_hp': {'current': 10, 'max': 20}, 'player_power': {'current':5,'max':10}}
    state = b.assemble(parts, [])
    assert state.player_hp.current == 10
    assert state.player_power.max == 10
