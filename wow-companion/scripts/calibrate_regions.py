"""GUI tool to create ROI masks (very minimal placeholder)."""
from __future__ import annotations
import json, argparse

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--output', required=True)
    args = ap.parse_args()
    # Placeholder default masks
    masks = {
        "player_hp": {"x":100,"y":900,"w":300,"h":30},
        "player_power": {"x":100,"y":935,"w":300,"h":20},
        "target_hp": {"x":800,"y":50,"w":300,"h":30},
        "combat_log": {"x":5,"y":700,"w":500,"h":300},
        "action_bar": {"x":600,"y":980,"w":720,"h":80}
    }
    with open(args.output,'w',encoding='utf-8') as f:
        json.dump(masks, f, indent=2)
    print(f"Wrote masks to {args.output}")

if __name__ == '__main__':
    main()
