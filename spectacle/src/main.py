# Copyright 2013, Dale E. Martin <dale@the-martins.org>
#
# All Rights Reserved.
#
# See the file COPYRIGHT for information on your rights and responsibilities if you
# redistribute this software.

import argparse
import ConfigParser
import sys

from spectacle.main import Spectacle

class Usage(Exception):
    def __init__(self, message):
        self.myMessage = message

    def __str__(self):
        return repr(self.myMessage)

    def message(self):
        return self.myMessage

def readConfig(configFile):
    config = ConfigParser.ConfigParser()
    config.read(configFile.name)
    return config

def main(argv=None):
    parser = argparse.ArgumentParser(description='Display photos in a slideshow')
    parser.add_argument('-v', dest='verbose', action='store_true',
                        help='turn on verbose mode')
    parser.add_argument('-config', metavar='c', type=file,
                        help='configuration to use', required=True)
    args = parser.parse_args()

    spectacle = Spectacle.constructWithConfig(args.verbose, readConfig(args.config))
    spectacle.doit()

#    if argv is None:
#        argv = sys.argv
#    try:
#        try:
#            opts, args = getopt.getopt(argv[1:], "h", ["help"])
#            print "Yep!"
#        except getopt.error, message:
#            raise Usage(message)
#        # more code, unchanged
#    except Usage, err:
#        print >>sys.stderr, err.message()
#        print >>sys.stderr, "for help use --help"
#        return 2

if __name__ == "__main__":
    sys.exit(main())
