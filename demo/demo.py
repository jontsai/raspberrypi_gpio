"""demo.py

Runs an Raspberry Pi GPIO demo

Usage:
    [sudo] python demo.py [-h|--help] [-d|--daemon]

Options:
    -h|--help       Displays this help
    -d|--daemon     Run as daemon
    -v|--version    Print version information and exit
"""
from time import sleep
import daemon
import getopt
import sys

import RPi.GPIO as GPIO

from agents import DemoRPiAgent

class Usage(Exception):
    def __init__(self, msg):
        self.msg = msg

def version():
    print 'Raspberry Pi board revision: %s' % GPIO.RPI_REVISION
    print 'RPi.GPIO version: %s' % GPIO.VERSION
 
OPTIONS_SHORT = 'hdv'
OPTIONS_VERBOSE = [
    'help',
    'daemon',
    'version',
]

def main(argv=None):
    DAEMON_MODE = False
    if argv is None:
        argv = sys.argv
    try:
        try:
            progname = argv[0]
            opts, args = getopt.getopt(argv[1:], OPTIONS_SHORT, OPTIONS_VERBOSE)
        except getopt.error, msg:
             raise Usage(msg)
        # process options
        for o, a in opts:
            if o in ('-h', '--help'):
                print __doc__
                sys.exit(0)
            if o in ('-d', '--daemon'):
                DAEMON_MODE = 'daemon'
            if o in ('-v', '--version'):
                version()
                sys.exit(0)
        # process arguments
        for arg in args:
            pass
        if DAEMON_MODE:
            context = daemon.DaemonContext()
            context.stdout = open('/var/log/demo.log', 'w+')
            context.stderr = open('/var/log/demo.error.log', 'w+', buffering=0)
            with context:
                run()
        else:
            run()
    except Usage, err:
        print >>sys.stderr, err.msg
        print >>sys.stderr, "for help use --help"
        return 3.14159


def run():
    agent = DemoRPiAgent()
    try:
        agent.start()
        while agent.is_alive():
            sleep(1)
    except KeyboardInterrupt:
        print 'Got KeyboardInterrupt'
    finally:
        agent.terminate()

if __name__ == '__main__':
    main()
