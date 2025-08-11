import numpy as np
from src.core.vision import extract_parts


def test_extract_cooldowns_and_auras():
    frame = (np.random.rand(1080, 1920, 3) * 255).astype('uint8')
    masks = {
        'cooldown_slots': [
            {'x': 10, 'y': 10, 'w': 32, 'h': 32, 'spell': 'Penance'},
            {'x': 50, 'y': 10, 'w': 32, 'h': 32, 'spell': 'Power Word: Shield'}
        ],
        'buff_slots': [
            {'x': 100, 'y': 10, 'w': 32, 'h': 32, 'name': 'Atonement'}
        ]
    }
    parts = extract_parts(frame, masks)
    assert 'cooldowns' in parts and len(parts['cooldowns']) >= 2
    assert any(c['spell'] == 'Penance' for c in parts['cooldowns'])
    assert 'buffs' in parts and any(b['name'] == 'Atonement' for b in parts['buffs'])
