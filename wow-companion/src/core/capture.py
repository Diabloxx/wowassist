"""High-performance screen capture using mss with scaling & ROI cropping."""
from __future__ import annotations
import mss
import numpy as np
import time
from typing import Optional, Tuple, Dict
import cv2
from ..config import config

class ScreenCapture:
    def __init__(self, monitor_index: int = 0, scale: float = 0.75):
        self.monitor_index = monitor_index
        self.scale = scale
        self.sct = mss.mss()
        self.monitor = self._select_monitor()

    def _select_monitor(self):
        mons = self.sct.monitors
        if self.monitor_index + 1 < len(mons):
            return mons[self.monitor_index + 1]  # first is all
        return mons[1]

    def grab_frame(self, roi: Optional[Tuple[int,int,int,int]] = None) -> np.ndarray:
        t0 = time.time()
        mon = self.monitor.copy()
        if roi:
            x,y,w,h = roi
            mon.update({'left': mon['left']+x, 'top': mon['top']+y, 'width': w, 'height': h})
        img = self.sct.grab(mon)
        frame = np.array(img)[:,:,:3]  # BGRA -> BGR drop alpha
        if self.scale != 1.0:
            frame = cv2.resize(frame, None, fx=self.scale, fy=self.scale, interpolation=cv2.INTER_LINEAR)
        return frame

# Singleton capture instance for quick use
capture = ScreenCapture(config.CAPTURE_MONITOR, config.CAPTURE_SCALE)
