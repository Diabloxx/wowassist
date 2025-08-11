from src.core.vision import extract_parts
import numpy as np

MOCK_MASKS = {"player_hp": {"x":0,"y":0,"w":10,"h":10}}

def test_extract_parts_mock():
    frame = (np.random.rand(100,100,3)*255).astype('uint8')
    parts = extract_parts(frame, MOCK_MASKS)
    assert 'player_hp' in parts
