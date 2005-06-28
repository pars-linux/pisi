# -*- coding: utf-8 -*-
# python standard library
# Authors: Baris Metin <baris@uludag.org.tr
#          Eray Ozkural <eray@uludag.org.tr>

from os.path import join
from os import access, R_OK
import sys


# pisi modules
from archive import Archive
from purl import PUrl
from ui import ui
from config import config
from fetcher import fetchUrl, displayProgress
import context
import util


class SourceArchiveError(Exception):
    pass

class SourceArchive:
    """source archive. this is a class responsible for fetching
    and unpacking a source archive"""
    def __init__(self, ctx):
        self.ctx = ctx
        self.url = PUrl(self.ctx.spec.source.archiveUri)
        self.dest = join(config.archives_dir(), self.url.filename())

    def fetch(self):
        if not self.isCached():
            fetchUrl(self.url, config.archives_dir(), displayProgress)
        
    def isCached(self):
        if not access(self.dest, R_OK):
            return False

        # check hash
        if util.sha1_file(self.dest) == self.ctx.spec.source.archiveSHA1:
            ui.info('%s [cached]\n' % self.ctx.spec.source.archiveName)
            return True

    def unpack(self):
        archive = Archive(self.dest, self.ctx.spec.source.archiveType)
        archive.unpack(self.ctx.pkg_work_dir())
