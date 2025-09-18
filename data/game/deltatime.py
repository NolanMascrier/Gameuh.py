"""Timers to replace pygame's"""

import time

class Timer():
    """Defines a timer.
    
    Args:
        ref (any): Reference of the timer, usually a constant.
        delay (float): Amount of time in miliseconds between each event.
        loop (int, optional): How many times should this event loop before being deleted.\
        Defaults to None (Infinite loops)
    """
    def __init__(self, ref, delay, loop = None):
        self.ref = ref
        self.delay = delay
        self.loop = loop
        self.timer = 0


class DeltaTime():
    """Defines the timer handler."""
    def __init__(self):
        self._last_tick = time.perf_counter()
        self._timers = {}
        self._events = []

    def start(self, ref, delay, loops = None):
        """Starts a timer."""
        self._timers[ref] = Timer(ref, delay, loops)

    def stop(self, ref):
        """Stops the given timer."""
        self._timers.pop(ref, None)

    def tick(self):
        """Ticks down every timers."""
        now = time.perf_counter()
        delta = (now - self._last_tick) * 1000
        self._last_tick = now
        expired = []
        for timer in self._timers.values():
            timer.timer += delta
            while timer.timer >= timer.delay:
                timer.timer -= timer.delay
                self._events.append(timer.ref)
                if timer.loop is not None:
                    timer.loop -= 1
                    if timer.loop <= 0:
                        expired.append(timer.ref)
        for ref in expired:
            self._timers.pop(ref, None)

    def get(self):
        """Returns the references of all completed events."""
        ref = self._events.copy()
        self._events.clear()
        return ref

    def peek(self, ref) -> Timer|None:
        """Peeks at a single timer."""
        return self._timers.get(ref, None)

    def clear(self):
        """Clears all events."""
        self._events.clear()
