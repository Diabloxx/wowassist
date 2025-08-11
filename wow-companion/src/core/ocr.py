"""OCR utilities wrapping pytesseract with preprocessing and combat log parsing."""
from __future__ import annotations
import cv2
import numpy as np
import pytesseract
from typing import List, Dict

PREPROCESS_CONFIG = {
    'clahe_clip': 2.0,
    'clahe_grid': (8,8)
}

def preprocess(img):
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    clahe = cv2.createCLAHE(clipLimit=PREPROCESS_CONFIG['clahe_clip'], tileGridSize=PREPROCESS_CONFIG['clahe_grid'])
    gray = clahe.apply(gray)
    gray = cv2.threshold(gray, 0, 255, cv2.THRESH_BINARY+cv2.THRESH_OTSU)[1]
    return gray

def ocr_image(img, lang='eng') -> str:
    proc = preprocess(img)
    txt = pytesseract.image_to_string(proc, lang=lang)
    return txt.strip()

def ocr_digits(img) -> str:
    """Fast digit-only OCR for cooldown numbers.

    Uses a tighter psm and whitelist to reduce noise. Returns empty string on failure.
    """
    proc = preprocess(img)
    try:
        txt = pytesseract.image_to_string(proc, config='--psm 7 -c tessedit_char_whitelist=0123456789')
        return ''.join(ch for ch in txt if ch.isdigit())
    except Exception:
        return ''

COMBAT_KEYWORDS = ["casts", "begins", "applies", "fades", "interrupt", "You"]

def parse_combat_log(text_block: str) -> List[str]:
    lines = [l.strip() for l in text_block.splitlines() if l.strip()]
    filtered = [l for l in lines if any(k.lower() in l.lower() for k in COMBAT_KEYWORDS)]
    return filtered[-50:]
