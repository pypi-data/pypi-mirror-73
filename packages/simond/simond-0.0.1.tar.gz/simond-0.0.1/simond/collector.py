"""
Module with funtionality to collect and calculate system metrics
"""
from statistics import mean
from time import sleep

from . import si
from .interval import Interval
from .utils import noop

def avgs(items, key_blacklist=()):
    """
    Expects a list of equally structured dicts and returns a dict with the mean
    of all values. For blacklisted keys the last value is used.

    Example:
    ```python
    in = [{ a: 1, b: 10, c: 1 }, { a: 2, b: 20, c: 2 }, { a: 3, b: 30, c: 3 }]
    avgs(in, ('c'))
    >>> { a: 2, b: 20, c: 3 }
    ```
    """
    keys = items[0].keys()
    values = dict()
    # Initialize all keys with empty lists so we can append
    for key in keys:
        values[key] = []
    # Append all values per key
    for item in items:
        for key in keys:
            values[key].append(item.get(key))
    # Calculate averages for keys not in `key_blacklist`, otherwise take last value
    result = dict()
    for key in keys:
        result[key] = round(mean(values[key]), 3) if not key in key_blacklist else values[key][-1]
    return result

def poll():
    """
    Polls and returns system information
    """
    data = dict()

    data.update(host=si.host())
    data.update(ts=si.timestamp())
    loadavgs = si.loadavg()
    data.update(loadavg_1min=loadavgs[0])
    data.update(loadavg_5min=loadavgs[1])
    data.update(loadavg_15min=loadavgs[2])
    data.update(mem=si.memory())
    data.update(cpu=si.cpu())
    data.update(disk=si.disk())
    diskio = si.diskio()
    data.update(diskio_rps=diskio[0])
    data.update(diskio_wps=diskio[1])
    netio = si.netio()
    data.update(netio_rps=netio[0])
    data.update(netio_sps=netio[1])

    return data

class Collector:
    """
    Collects the system metrics every second (tick) and passes them to
    `on_input` every `loginterval` seconds (log). By default the log interval is
    also one second, if it's above, averages will be passed.
    Additionally it also accepts `on_tick` as an additional and optional
    callback for every tick.
    """
    NO_AVG_KEYS = ('host', 'ts') # Keys of which no average is calculated for

    @staticmethod
    def create(*args):
        """
        Static constructor
        """
        return Collector(*args)

    def __init__(self, on_input, loginterval=1, on_tick=noop):
        if not callable(on_input):
            raise TypeError('on_input must be callable')
        if not isinstance(loginterval, int) or loginterval < 1:
            raise ValueError('loginterval must be an integer equal or above 1')
        if on_tick is not noop and not callable(on_tick):
            raise TypeError('on_tick must be callable if provided')

        self.loginterval = loginterval
        self.on_input = on_input
        self.on_tick = on_tick
        self.tick_values = []

        # Initial poll and delay, so next poll has IO data
        poll()
        sleep(1)
        self.tick_index = 1

        Interval.create(self.collect, 1)

    def collect(self):
        """
        Collects data on each tick and passes them to the callbacks if appropriate
        """
        data = poll()
        self.on_tick(data)
        if self.loginterval == 1:
            self.on_input(data)
        elif self.tick_index % self.loginterval == 0:
            self.tick_values.append(data)
            self.on_input(avgs(self.tick_values, self.NO_AVG_KEYS))
            self.tick_values.clear()
        else:
            self.tick_values.append(data)
        self.tick_index += 1
