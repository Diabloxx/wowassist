"""Main application loop for WoW Companion (Assist Mode default)."""
from __future__ import annotations
import argparse, json, time, os
from .config import config
from .core.capture import capture
from .core.vision import extract_parts
from .core.ocr import parse_combat_log
from .core.state import GameStateBuilder
from .core.reasoner import pick_action
from .core.overlay import render
from .core.learning import learning_agent
from .core.telemetry import telemetry
from .core import actions as action_exec
import importlib, json as _json

def _load_policy(class_spec: str, flavor: str):
    # flavor-specific variant e.g. priest_discipline_mop
    flavor_mod = f"src.core.profiles.{class_spec}_mop" if flavor == 'classic_mop' else None
    candidates = []
    if flavor_mod:
        candidates.append(flavor_mod)
    candidates.append(f"src.core.profiles.{class_spec}")
    for mod_name in candidates:
        try:
            mod = importlib.import_module(mod_name)
            return getattr(mod, 'policy')
        except Exception:
            continue
    raise RuntimeError(f"Could not load rotation policy for {class_spec} flavor={flavor}")

def _load_masks(profile: str, flavor: str):
    paths = [
        f"src/data/masks/{flavor}.json",
        f"src/data/masks/{profile}.json",
        "src/data/masks/default.json"
    ]
    for p in paths:
        if os.path.exists(p):
            with open(p,'r',encoding='utf-8') as f:
                try:
                    return _json.load(f)
                except Exception:
                    pass
    return {}

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--perf', action='store_true', help='Print per-loop timings')
    args = ap.parse_args()

    policy = _load_policy(config.CLASS_SPEC, config.GAME_FLAVOR)
    masks = _load_masks(config.MASK_PROFILE, config.GAME_FLAVOR)
    # crude class/spec inference from CLASS_SPEC
    cls, spec = config.CLASS_SPEC.split('_',1) if '_' in config.CLASS_SPEC else (config.CLASS_SPEC, '')
    builder = GameStateBuilder(cls.title(), spec.title())
    prev_state = None

    while True:
        loop_t0 = time.time()
        frame = capture.grab_frame()
        t_cap = time.time()
        parts = extract_parts(frame, masks)
        t_vis = time.time()
        # skipping heavy OCR for now (TODO integrate OCR regions)
        events = parse_combat_log("")
        state = builder.assemble(parts, events)
        t_state = time.time()
        shortlist = policy.shortlist(state)
        decision = pick_action(state, shortlist)
        t_reason = time.time()
        render(decision, state)
        if config.AUTOMATION_MODE:
            action_exec.try_execute(decision)
        # Learning placeholder reward
        if prev_state is not None:
            reward = 0.0  # compute later
            learning_agent.update(prev_state, decision.action, reward)
        prev_state = state
        t_end = time.time()
        telemetry.log('tick', {
            'lat_cap_ms': int((t_cap-loop_t0)*1000),
            'lat_vis_ms': int((t_vis-t_cap)*1000),
            'lat_state_ms': int((t_state-t_vis)*1000),
            'lat_reason_ms': int((t_reason-t_state)*1000),
            'lat_total_ms': int((t_end-loop_t0)*1000),
            'action': decision.action,
            'priority': decision.priority
        })
        if args.perf:
            print(f"loop {int((t_end-loop_t0)*1000)} ms")
        # Basic horizon sleep
        time.sleep(min(0.2, max(0.05, decision.horizon_ms/1000)))

if __name__ == '__main__':
    main()
