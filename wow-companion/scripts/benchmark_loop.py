"""Benchmark the decision loop latency and FPS."""
from __future__ import annotations
import time, argparse, json, statistics
from src.core.capture import capture
from src.core.vision import extract_parts
from src.core.ocr import parse_combat_log, ocr_image
from src.core.state import GameStateBuilder
from src.core.reasoner import pick_action, ActionDecision
from src.core.profiles.priest_discipline import policy as disc_policy
from src.core.telemetry import telemetry
from src.config import config
import numpy as np

MOCK_MASKS = {
    "player_hp": {"x":100,"y":900,"w":300,"h":30},
    "player_power": {"x":100,"y":935,"w":300,"h":20},
    "target_hp": {"x":800,"y":50,"w":300,"h":30},
    "combat_log": {"x":5,"y":700,"w":500,"h":300},
    "action_bar": {"x":600,"y":980,"w":720,"h":80}
}

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--seconds', type=int, default=10)
    args = ap.parse_args()

    builder = GameStateBuilder('Priest','Discipline')
    latencies = []
    start = time.time()
    frames = 0

    while time.time() - start < args.seconds:
        loop_t0 = time.time()
        frame = capture.grab_frame()
        parts = extract_parts(frame, MOCK_MASKS)
        # Fake combat log OCR region extraction
        combat_crop = parts.get('combat_log') if isinstance(parts.get('combat_log'), np.ndarray) else frame[700:1000,5:505]
        text = ""  # skipping heavy OCR in benchmark stub
        events = parse_combat_log(text)
        state = builder.assemble(parts, events)
        shortlist = disc_policy.shortlist(state)
        decision = pick_action(state, shortlist)
        frames += 1
        dt = (time.time() - loop_t0)*1000
        latencies.append(dt)

    p50 = statistics.median(latencies)
    p90 = statistics.quantiles(latencies, n=10)[8]
    fps = frames / (time.time() - start)
    print(json.dumps({"frames": frames, "fps": fps, "p50_ms": p50, "p90_ms": p90}, indent=2))

if __name__ == '__main__':
    main()
