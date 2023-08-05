# simond - **Si**mple **Mon**itor _Daemon_

The daemon for **simon**, collects system information every second and logs them
to STDOUT (redirect or pipe it to your liking) at a certain interval.
If the interval is not 1 sec, the sample mean will be calculated and logged.

## Installation

simond requires Python 3.6+, the easiest way to install it is with `pip` or any other package manager supporting PyPI:

```sh
pip install simond
```

## Usage

```
usage: simond [-h] [-V] [-i LOGINTERVAL]

simond - Simple Monitor Daemon, fetches and logs system information

optional arguments:
  -h, --help            show this help message and exit
  -V, --version         Print simond version number
  -i LOGINTERVAL, --loginterval LOGINTERVAL
                        The log interval in seconds, if it's anything but 1,
                        averages (sample mean) will be logged
```

## Log structure

- `host`: The system's hostname
- `ts`: Timestamp of when the data were gathered as UTC Unix time
- `loadavg_1min`: 1min [Load average](https://en.wikipedia.org/wiki/Load_%28computing%29)
- `loadavg_5min`: 5min Load average
- `loadavg_15min`: 15min Load average
- `mem`: Total memory usage in percent as number (0.01 = 1%)
- `cpu`: Total CPU usage in percent as number
- `disk`: Total disk usage in percent as number
- `diskio_rps`: Disk reads in bytes per second
- `diskio_wps`: Disk writes in bytes per second
- `netio_rps`: Network traffic received in bytes per second
- `netio_sps`: Network traffic sent in bytes per second

Currently **simon** logs each measure as a JSON object separated by newline, the
file will therefor not be valid JSON, with the benefit that each line is valid JSON and can be read per line (streaming FTW!):

```json
{"host": "simon", "ts": 1592943008, "loadavg_1min": 1.598, "loadavg_5min": 2.104, "loadavg_15min": 2.504, "mem": 0.03, "cpu": 0.014, "disk": 0.545, "diskio_rps": 0, "diskio_wps": 0, "netio_rps": 0, "netio_sps": 0}
{"host": "simon", "ts": 1592943009, "loadavg_1min": 1.598, "loadavg_5min": 2.104, "loadavg_15min": 2.504, "mem": 0.03, "cpu": 0.036, "disk": 0.545, "diskio_rps": 0, "diskio_wps": 0, "netio_rps": 1024, "netio_sps": 0}
```



**This might change in the future if it is not sufficent.**