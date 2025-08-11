# WoW Companion (Assist-First AI Gaming Assistant)

A modular, local, privacy-preserving World of Warcraft assistant that observes only your screen, understands the game state, and recommends optimal next actions — defaulting to Assist Mode (advice overlay + optional voice). Automation Mode (sending inputs) is OFF by default, behind an explicit toggle + visible banner.

> IMPORTANT: This project is educational. Automation may violate Blizzard's Terms of Service / End User License Agreement if abused. By default, the project ships in Assist Mode only. You must explicitly opt-in to Automation Mode at runtime. Use responsibly.

## Features
- <200 ms target decision loop (capture → parse → reason → recommend) at 1080p with scaling & ROI masks.
- Screen-only CV + OCR (no memory reading, injection, DLL hooks, or game API calls).
- Local reasoning via Ollama (LLM) with strict JSON schema + retries.
- Rotation policy plugins per class/spec (easily extensible).
- Structured `GameState` model (Pydantic) + deterministic prompts.
- Overlay with current recommendation, rationale, status strip, Assist vs Automation indicator.
- Global hotkeys: toggle overlay, toggle automation, push-to-talk TTS.
- Telemetry (jsonl) logging every tick (inputs, outputs, timings) — no PII.
- Lightweight self-learning (contextual bandit) with reward shaping + offline trainer hooks.

## Repository Structure
```
wow-companion/
  README.md
  LICENSE
  .env.example
  requirements.txt
  src/
    app.py
    config.py
    core/
      capture.py
      vision.py
      ocr.py
      state.py
      reasoner.py
      actions.py
      learning.py
      overlay.py
      audio_tts.py
      telemetry.py
      profiles/
        base_rotation.py
        priest_discipline.py
        warrior_protection.py
    ui/
      overlay_window.py
      hotkeys.py
    data/
      icons/
      masks/
      models/
    rl/
      reward.py
      replay_buffer.py
      trainer.py
    tests/
      test_capture.py
      test_vision.py
      test_state.py
      test_reasoner.py
      test_learning.py
  scripts/
    calibrate_regions.py
    benchmark_loop.py
    export_session_csv.py
```

## Quick Start (Windows 10/11)
### 1. Python Environment
Install Python 3.11+ (64-bit). Then:
```powershell
py -3.11 -m venv .venv
.\.venv\Scripts\Activate.ps1
pip install --upgrade pip
pip install -r requirements.txt
```

### 2. Install Tesseract OCR
Download Windows installer: https://github.com/tesseract-ocr/tesseract
During install, enable English (eng) language data. Add the install directory (e.g. `C:\Program Files\Tesseract-OCR`) to your PATH. Verify:
```powershell
tesseract --version
```

### 3. Install Ollama
Download & install from: https://ollama.ai
Then pull a model (example):
```powershell
ollama pull llama3.1
# or: ollama pull qwen2.5
```
Ensure Ollama service is running (default: `http://localhost:11434`).

### 4. Configure Environment
Copy `.env.example` to `.env` and adjust if needed.

### 5. Run in Assist Mode (default)
```powershell
python -m src.app
```
Overlay should display recommendations (stub / mock until calibrated). Automation is OFF and cannot send inputs until toggled.

### 6. Optional: Enable Automation Mode
In-app hotkey (default F10). A bright red `AUTOMATION ON` banner appears. Press again to disable. Deadman switch: Hold Left Shift to suppress sending actions.

### 7. Benchmark Loop Performance
```powershell
python scripts/benchmark_loop.py --seconds 30
```
Outputs p50 / p90 latency and FPS.

### 8. Calibrate Regions
```powershell
python scripts/calibrate_regions.py --output src/data/masks/custom_default.json
```
Follow GUI to drag rectangles over: player frame, target frame, party, action bars, combat log, warnings. These accelerate parsing.

## Environment Variables (`.env`)
```
OLLAMA_HOST=http://localhost:11434
OLLAMA_MODEL=llama3.1
ASSIST_MODE=true
AUTOMATION_MODE=false
CAPTURE_MONITOR=0
CAPTURE_SCALE=0.75
OCR_LANG=eng
OVERLAY_OPACITY=0.85
CLASS_SPEC=priest_discipline
LOG_LEVEL=INFO
```

## Assist Mode vs Automation Mode
- Assist Mode: Only observes screen, renders overlay, optionally TTS; NEVER sends inputs.
- Automation Mode: (Opt-in) Maps recommended spell -> keybind and sends keystrokes with rate limiting + deadman switch. Banner + config guard ensures explicit consent.

### ToS & Ethical Considerations
Blizzard's ToS forbids botting and unauthorized automation that plays the game for you. This project:
- Ships with Automation OFF and safe overlay-only Assist Mode.
- Uses screen reading (akin to accessibility tools) without modifying or injecting into the game.
- Encourages player decision support, not unattended play.
You are responsible for compliance. If unsure, keep to Assist Mode.

## Latency Optimization Tips
- Lower `CAPTURE_SCALE` (e.g., 0.6) to shrink processing cost.
- Use masks to restrict OCR (combat log, boss warnings) instead of full frame.
- Cache template-matching icons (done automatically at startup).
- Batch OCR of grouped regions with similar preprocessing.
- Keep Ollama temperature low and context concise (already applied).

## Learning & Telemetry
- Every tick logged to `logs/session_<timestamp>.jsonl`.
- Bandit updates per rewarded decision (simple weight vector by action).
- Export & analyze: `python scripts/export_session_csv.py` -> CSV & optional plot.

## Tests
Run all:
```powershell
pytest -q
```

## Extending Rotations
Add a new spec file in `src/core/profiles/` implementing `RotationPolicy`. Provide action shortlist logic referencing buffs, cooldowns, role priorities.

## Safety Defaults Recap
- `AUTOMATION_MODE=false` hard default.
- Visible red banner when on.
- Deadman shift hold disables key sends.
- Fallback safe action if LLM JSON invalid.

## Disclaimer
Use at your own risk. Not affiliated with Blizzard Entertainment. Educational prototype.

---
Happy (assisted) adventuring!
