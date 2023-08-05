#!/usr/bin/env python3

"""
Tolkein.

usage: tolkein [<command>] [<args>...] [-h|--help] [--version]

commands:
    -h, --help      show this
    -v, --version   show version number
"""

from docopt import docopt

from tolkein import __version__


def main():
    """Entry point."""
    docopt(__doc__,
           version=__version__,
           options_first=True)


if __name__ == '__main__':
    main()
