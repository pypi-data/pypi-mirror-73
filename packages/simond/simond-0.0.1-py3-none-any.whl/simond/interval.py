"""
Provides funtionalities for time intervals
"""
import sched
import time

class Interval:
    """
    Sets up an interval calling `fn` every time `interval` passes
    """
    def __init__(self, fn, interval, autostart=True):
        self._fn = fn
        self._interval = interval
        self._scheduler = sched.scheduler(time.time, time.sleep)
        self._ev = None
        if autostart:
            self.start()

    @staticmethod
    def create(*args):
        """
        Static constructor
        """
        return Interval(*args)

    def _call(self):
        self._fn()
        self._next()

    def _next(self):
        self._ev = self._scheduler.enter(self._interval, 1, self._call)

    def start(self):
        """
        Starts the interval, only relevant if autostart=False on construction
        """
        self._next()
        self._scheduler.run()
