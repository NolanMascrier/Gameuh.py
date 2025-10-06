"""Simple logger implementation."""

import time

class Logger():
    """Logger class for logging events."""
    def __init__(self):
        self._start = time.perf_counter()

    def print(self, string):
        """Prints the arguments in the console."""
        now = time.perf_counter() - self._start
        print(f"[{now:.5f}]: {string}")
