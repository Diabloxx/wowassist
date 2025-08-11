from src.core.reasoner import ActionDecision

def test_action_decision_model():
    d = ActionDecision(action='Test', spell_id=None, priority=0.5, rationale='x', safety=['ok'], horizon_ms=100)
    assert d.priority == 0.5
