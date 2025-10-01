"""Clock object for FPS and sleeps. Where is Kronii ?"""

import time
from collections import deque

class Clock:
    """Defines a clock."""
    def __init__(self, buffer_size: int = 10):
        self._last_time = time.perf_counter()
        self._frame_times = deque(maxlen=buffer_size)

    def tick(self, fps: int = None) -> int:
        """Limit loop to `fps` frames per second.
        Returns elapsed milliseconds since last call.
        """
        if fps is None or fps <= 0:
            now = time.perf_counter()
            dt = now - self._last_time
            self._last_time = now
            self._frame_times.append(dt)
            return int(dt * 1000)
        frame_duration = round(1.0 / fps, 5)
        now = time.perf_counter()
        dt = now - self._last_time
        if dt < frame_duration:
            time.sleep(frame_duration - dt)
            now = time.perf_counter()
            dt = now - self._last_time
        self._last_time = now
        self._frame_times.append(dt)
        return int(dt * 1000)

    def get_fps(self) -> float:
        """Returns the average frames per second over the buffer.
        """
        if not self._frame_times:
            return 0.0
        avg_dt = sum(self._frame_times) / len(self._frame_times)
        if avg_dt == 0:
            return 0.0
        return 1.0 / avg_dt
