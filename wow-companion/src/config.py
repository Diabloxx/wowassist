"""Configuration loader for the WoW Companion.
Reads environment variables (.env) and provides a singleton-style access.
"""
from __future__ import annotations
import os
from dataclasses import dataclass
from dotenv import load_dotenv  # optional: fallback if installed, else simple parser

# Light fallback if python-dotenv not installed (not in requirements by default)
def _simple_load_env():
    path = '.env'
    if os.path.exists(path):
        with open(path,'r',encoding='utf-8') as f:
            for line in f:
                line=line.strip()
                if not line or line.startswith('#') or '=' not in line:
                    continue
                k,v=line.split('=',1)
                os.environ.setdefault(k.strip(), v.strip())

try:
    load_dotenv(override=False)  # type: ignore
except Exception:
    _simple_load_env()

@dataclass(frozen=True)
class Config:
    OLLAMA_HOST: str = os.environ.get('OLLAMA_HOST','http://localhost:11434')
    OLLAMA_MODEL: str = os.environ.get('OLLAMA_MODEL','llama3.1')
    ASSIST_MODE: bool = os.environ.get('ASSIST_MODE','true').lower() == 'true'
    AUTOMATION_MODE: bool = os.environ.get('AUTOMATION_MODE','false').lower() == 'true'
    CAPTURE_MONITOR: int = int(os.environ.get('CAPTURE_MONITOR','0'))
    CAPTURE_SCALE: float = float(os.environ.get('CAPTURE_SCALE','0.75'))
    OCR_LANG: str = os.environ.get('OCR_LANG','eng')
    OVERLAY_OPACITY: float = float(os.environ.get('OVERLAY_OPACITY','0.85'))
    CLASS_SPEC: str = os.environ.get('CLASS_SPEC','priest_discipline')
    LOG_LEVEL: str = os.environ.get('LOG_LEVEL','INFO')
    LOG_DIR: str = os.environ.get('LOG_DIR','logs')
    GAME_FLAVOR: str = os.environ.get('GAME_FLAVOR','retail')  # retail | classic_mop | classic_wotlk etc.
    MASK_PROFILE: str = os.environ.get('MASK_PROFILE','default')

config = Config()

os.makedirs(config.LOG_DIR, exist_ok=True)
