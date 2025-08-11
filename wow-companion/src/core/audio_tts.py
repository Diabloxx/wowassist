"""Text-to-speech wrapper (pyttsx3 fallback)."""
from __future__ import annotations
try:
    import pyttsx3
except Exception:  # pragma: no cover
    pyttsx3 = None

_engine = None

def speak(text: str):
    global _engine
    if pyttsx3 is None:
        return
    if _engine is None:
        _engine = pyttsx3.init()
    _engine.say(text)
    _engine.runAndWait()
