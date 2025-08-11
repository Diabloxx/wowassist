"""LLM-based reasoning via local Ollama with strict JSON contract."""
from __future__ import annotations
import json, requests, time
from pydantic import BaseModel, ValidationError
from .state import GameState
from ..config import config

SYSTEM_PROMPT = (
    "You are a tactical WoW assistant. You receive a structured GameState JSON and must output a single best next-action as JSON.\n"
    "Principles: (1) Survive > Mechanics > Throughput. (2) Never suggest actions on cooldown or without resources. (3) Prefer instant casts when movement inferred. (4) Consider party triage for healers.\n"
    "Output strictly in the provided ActionDecision JSON schema. No prose outside JSON."
)

class ActionDecision(BaseModel):
    action: str
    spell_id: str | None = None
    priority: float
    rationale: str
    safety: list[str]
    horizon_ms: int

OLLAMA_URL = f"{config.OLLAMA_HOST}/api/generate"
MODEL = config.OLLAMA_MODEL

RETRY_PREFIX = "Respond ONLY with valid JSON for ActionDecision:"

def pick_action(state: GameState, shortlist: list[dict]) -> ActionDecision:
    system = SYSTEM_PROMPT
    user = json.dumps({
        "state": state.model_dump(),
        "shortlist": shortlist
    }, separators=(',', ':'))

    payload = {"model": MODEL, "system": system, "prompt": user, "stream": False, "options": {"temperature": 0.25}}
    t0 = time.time()
    try:
        r = requests.post(OLLAMA_URL, json=payload, timeout=2.5)
        r.raise_for_status()
        raw = r.json().get("response", "{}")
        try:
            obj = json.loads(raw)
            return ActionDecision(**obj)
        except (json.JSONDecodeError, ValidationError):
            # retry once with stricter instruction
            r2 = requests.post(OLLAMA_URL, json={**payload, "prompt": RETRY_PREFIX + user}, timeout=2.5)
            raw2 = r2.json().get("response", "{}")
            try:
                obj2 = json.loads(raw2)
                return ActionDecision(**obj2)
            except Exception:
                return ActionDecision(action="Wait 200ms", spell_id=None, priority=0.2,
                                      rationale="Invalid LLM JSON; safe wait.", safety=["fallback"], horizon_ms=200)
    except Exception:
        return ActionDecision(action="Wait 500ms", spell_id=None, priority=0.1,
                              rationale="LLM request failed", safety=["network"], horizon_ms=500)
