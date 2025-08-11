"""Telemetry logging utilities."""
from __future__ import annotations
import json, time, os
from ..config import config
from typing import Any, Dict

class TelemetryLogger:
    def __init__(self):
        ts = int(time.time())
        self.path = os.path.join(config.LOG_DIR, f"session_{ts}.jsonl")
        self.t0 = time.time()

    def log(self, kind: str, payload: Dict[str, Any]):
        record = {
            't': time.time(),
            'elapsed_ms': int((time.time()-self.t0)*1000),
            'kind': kind,
            **payload
        }
        with open(self.path, 'a', encoding='utf-8') as f:
            f.write(json.dumps(record, separators=(',',':')) + '\n')

telemetry = TelemetryLogger()
