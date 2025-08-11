"""Computer vision extraction: icons, bars, cooldown rings (simplified baseline)."""
from __future__ import annotations
import cv2
import numpy as np
import os
from typing import Dict, List, Any
from .ocr import ocr_digits

ICON_CACHE: Dict[str, np.ndarray] = {}

def load_icons(path: str):
    for fn in os.listdir(path):
        if not fn.lower().endswith(('.png','.jpg','.jpeg')): continue
        img = cv2.imread(os.path.join(path, fn), cv2.IMREAD_COLOR)
        if img is not None:
            ICON_CACHE[os.path.splitext(fn)[0]] = img

def match_icon(region: np.ndarray, icon: np.ndarray, threshold: float=0.85) -> bool:
    if region.shape[0] < icon.shape[0] or region.shape[1] < icon.shape[1]:
        return False
    res = cv2.matchTemplate(region, icon, cv2.TM_CCOEFF_NORMED)
    loc = np.where(res >= threshold)
    return len(loc[0])>0

# Simplified placeholder extraction logic

def extract_parts(frame: np.ndarray, masks: Dict[str, dict]) -> Dict[str, Any]:
    parts: Dict[str, Any] = {}
    h, w = frame.shape[:2]
    # Example mask format: {"player_hp": {"x":100,"y":900,"w":200,"h":20}}
    for key, m in masks.items():
        try:
            x,y,ww,hh = m['x'], m['y'], m['w'], m['h']
            crop = frame[y:y+hh, x:x+ww]
            if key.endswith('_bar'):
                # naive green ratio
                green = np.mean(crop[:,:,1]) / 255.0
                parts[key] = green
            else:
                parts[key] = crop
        except Exception:
            continue
    # Mock numerical values until refined (TODO: integrate actual bar parsing & numeric OCR)
    parts.setdefault('player_hp', {'current': 75000, 'max': 100000})
    parts.setdefault('player_power', {'current': 52000, 'max': 60000})
    parts.setdefault('target_hp', {'current': 340000, 'max': 500000})

    # Cooldown & aura stubs: expect optional "cooldowns" and "buffs" composite masks listing icon slots
    cd_defs = masks.get('cooldown_slots', [])  # list of {x,y,w,h,spell}
    cds = []
    for slot in cd_defs:
        try:
            x,y,ww,hh = slot['x'], slot['y'], slot['w'], slot['h']
            crop = frame[y:y+hh, x:x+ww]
            num = ocr_digits(crop)
            remaining = float(num) if num else 0.0
            cds.append({'spell': slot.get('spell','Unknown'), 'remaining_s': remaining})
        except Exception:
            continue
    if cds:
        parts['cooldowns'] = cds
    else:
        parts.setdefault('cooldowns', [ {'spell':'Penance','remaining_s':0.0}, {'spell':'Power Word: Shield','remaining_s':0.0} ])

    aura_defs = masks.get('buff_slots', [])  # list of {x,y,w,h,name}
    auras = []
    for slot in aura_defs:
        try:
            # For now we don't template match; assume icon presence -> active, assign dummy duration placeholder
            name = slot.get('name','Aura')
            auras.append({'name': name, 'stacks': 1, 'duration_s': 8.0})
        except Exception:
            continue
    if auras:
        parts['buffs'] = auras
    else:
        parts.setdefault('buffs', [ {'name':'Atonement','stacks':1,'duration_s':8.0} ])
    return parts
