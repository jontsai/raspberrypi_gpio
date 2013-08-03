"""
setup.py

Install Python packages system-wide

Usage:
    sudo python setup.py (install packages)
    sudo python setup.py -U (upgrade packages)
"""

import getopt
import os
import re
import sys
import subprocess

# script to install a bunch of packages in the global environment
# this list of packages should match up with the list in conf/virtualenv/create-venv-script.py
SITE_PACKAGES_PIP = [
    'RPi.GPIO',
]

PIP = 'bin/pip'

EXECUTION_MODE = 'install'

class Usage(Exception):
    def __init__(self, msg):
        self.msg = msg

def main(argv = None):
    if argv is None:
        argv = sys.argv
    try:
        try:
            progname = argv[0]
            opts, args = getopt.getopt(argv[1:], "hU", ["help", "upgrade",])
        except getopt.error, msg:
             raise Usage(msg)
        # process options
        global EXECUTION_MODE
        for o, a in opts:
            if o in ('-h', '--help'):
                print __doc__
                sys.exit(0)
            if o in ('-U', '--upgrade'):
                EXECUTION_MODE = 'upgrade'
        # process arguments
        for arg in args:
            pass
        for package in SITE_PACKAGES_PIP:
            if EXECUTION_MODE == 'install':
                subprocess.call([PIP, 'install', package])
            elif EXECUTION_MODE == 'upgrade':
                subprocess.call([PIP, 'install', '-U', package])

    except Usage, err:
        print >>sys.stderr, err.msg
        print >>sys.stderr, "for help use --help"
        return 3.14159

if __name__ == '__main__':
    main()
