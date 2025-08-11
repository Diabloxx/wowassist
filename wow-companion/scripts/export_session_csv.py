"""Export telemetry jsonl to CSV + basic aggregates."""
from __future__ import annotations
import csv, json, argparse

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--input', required=True, help='session_*.jsonl file')
    ap.add_argument('--output', default='session.csv')
    args = ap.parse_args()

    rows = []
    with open(args.input,'r',encoding='utf-8') as f:
        for line in f:
            try:
                rows.append(json.loads(line))
            except Exception:
                continue
    if not rows:
        print('No rows.')
        return
    keys = sorted({k for r in rows for k in r.keys()})
    with open(args.output,'w',newline='',encoding='utf-8') as f:
        w = csv.DictWriter(f, fieldnames=keys)
        w.writeheader()
        for r in rows:
            w.writerow(r)
    print(f"Wrote {len(rows)} rows to {args.output}")

if __name__ == '__main__':
    main()
