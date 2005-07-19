# -*- coding: utf-8 -*-

import sys
from optparse import OptionParser

import pisi
from pisi.config import config
import pisi.operations
from pisi.purl import PUrl
from common import *
from commands import *

class ParserError(Exception):
    pass

class Parser(OptionParser):
    def __init__(self, version):
        OptionParser.__init__(self, usage=usage_text, version=version)

    def error(self, msg):
        raise ParserError, msg

class PisiCLI(object):

    def __init__(self):
        # first construct a parser for common options
        # this is really dummy
        self.parser = Parser(version="%prog " + pisi.__version__)
        #self.parser.allow_interspersed_args = False
        self.parser = commonopts(self.parser)

        cmd = ""
        try:
            (options, args) = self.parser.parse_args()
            #if len(parser.rargs)==0:
            #    self.die()
            cmd = args[0]
        except IndexError:
            self.die()
        except ParserError:
            # fully expected :) let's see if we got an argument
            if len(self.parser.rargs)==0:
                self.die()
            cmd = self.parser.rargs[0]

        self.command = cmdObject(cmd)
        if not self.command:
            print "Unrecognized command: ", cmd
            self.die()

    def die(self):
        print usage_text
        sys.exit(1)

    def runCommand(self):
        self.command.run()
