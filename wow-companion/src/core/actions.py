"""Action execution layer (Assist vs Automation)."""
from __future__ import annotations
import time
from ..config import config
try:
    import keyboard  # global hotkeys / key send
except Exception:  # pragma: no cover
    keyboard = None

KEYBIND_MAP = {
    'Penance': '3',
    'Power Word: Shield': '1',
    'Smite': '2'
}

_last_action_time = 0.0

def try_execute(decision) -> bool:
    if config.ASSIST_MODE or not config.AUTOMATION_MODE:
        return False
    global _last_action_time
    now = time.time()
    if now - _last_action_time < 0.1:  # rate limit 10Hz
        return False
    if keyboard is None:
        return False
    # Deadman: if Left Shift held -> abort
    if keyboard.is_pressed('shift'):
        return False
    key = KEYBIND_MAP.get(decision.action.split(' ')[0])  # naive mapping
    if key:
        keyboard.press_and_release(key)
        _last_action_time = now
        return True
    return False
