"""
simond entry point
"""
from argparse import ArgumentParser #, FileType
import json
import sys

from . import __version__, __doc__
from .collector import Collector

def parse_args():
    """
    Defines, handles and returns program args
    """
    apa = ArgumentParser('simond', description=__doc__.strip())
    # apa.add_argument(
    #     '-o',
    #     '--output',
    #     type=FileType('a', 1),
    #     required=True,
    #     help='The file where to log system information to'
    # )
    apa.add_argument(
        '-V',
        '--version',
        help='Print simond version number',
        action='store_true'
    )
    apa.add_argument(
        '-i',
        '--loginterval',
        type=int,
        required=False,
        default=1,
        help="The log interval in seconds, if it's anything but 1, averages \
            (sample mean) will be logged"
    )
    return apa.parse_args()

def main():
    """
    main
    """
    args = parse_args()

    if args.version:
        print(__version__)
        sys.exit(0)

    def log(data):
        # args.output.write(json.dumps(data) + "\n")
        print(json.dumps(data))

    try:
        Collector.create(log, args.loginterval)
    except KeyboardInterrupt:
        pass
    except SystemExit:
        pass
    # finally:
    #     args.output.close()

if __name__ == '__main__':
    main()
