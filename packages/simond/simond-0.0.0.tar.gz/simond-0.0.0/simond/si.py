"""
Provides functionality to gather system information
"""
import platform
import datetime

import psutil

def cpu():
    """
    Gathers and returns total CPU usage in percent as decimal
    """
    sin = psutil.cpu_percent()
    return round(sin / 100, 3)

def disk():
    """
    Gathers and returns total disk usage in percent as decimal
    """
    sin = psutil.disk_usage('/')
    return round(sin.percent / 100, 3)

def _init_diskio():
    prev = None
    def update():
        nonlocal prev
        result = [None, None]
        curr = psutil.disk_io_counters()
        if prev:
            result = [
                curr.read_bytes - prev.read_bytes,
                curr.write_bytes - prev.write_bytes
            ]
        prev = curr
        return result
    return update
diskio = _init_diskio()
diskio.__doc__ = """
    Returns the disk IO since the last call in bytes read and written
"""

def host():
    """
    Gathers and returns the host's name
    """
    return platform.node()

def loadavg():
    """
    Gathers and returns the system's load averages
    """
    sin = psutil.getloadavg()
    return [
        round(sin[0], 3),
        round(sin[1], 3),
        round(sin[2], 3)
    ]

def memory():
    """
    Gathers and returns the total memory usage in percent as decimal
    """
    sin = psutil.virtual_memory()
    return round((sin.total / sin.used) / 100, 3)

def _init_netio():
    prev = None
    def update():
        nonlocal prev
        result = [None, None]
        curr = psutil.net_io_counters()
        if prev:
            result = [
                curr.bytes_recv - prev.bytes_recv,
                curr.bytes_sent - prev.bytes_sent
            ]
        prev = curr
        return result
    return update
netio = _init_netio()
netio.__doc__ = """
     Returns the network IO since the last call in bytes received and sent
"""

def timestamp():
    """
    Returns current UTC UNIX time
    """
    return round(datetime.datetime.utcnow().timestamp())
