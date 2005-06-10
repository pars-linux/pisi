#!/usr/bin/python
# -*- coding: utf-8 -*-

# python standard library modules
import urlparse
import urllib2
import os
from sys import argv
from sys import exit
from sys import stderr

# pisi modules
import pisiconfig
import util

class FetchError (Exception):
    pass

class Fetcher:
    """Yet another Pisi tool for fetching files from various sources.."""
    def __init__(self, uri):
        self.uri = uri
        self.filedest = pisiconfig.archives_dir
        util.check_dir(self.filedest)
        self.scheme = "file"
        self.netloc = ""
        self.filepath = ""
        self.filename = ""
        self.percent = 0
        self.rate = 0
	self.percentHook = None

    def fetch (self):
        """Return value: Fetched file's full path.."""
        from string import split
        u = urlparse.urlparse(self.uri)
        self.scheme, self.netloc, self.filepath = u[0], u[1], u[2]
        self.filename = split(self.filepath, "/")[-1:][0]

        if self.filename == "":
            self.err("filename error")

        if os.access(self.filedest, os.W_OK) == False:
            self.err("no perm to write to dest dir")

        scheme_err = lambda: self.err("unexpected scheme")

        actions = {
            'file': self.fetchLocalFile,
            'http': self.fetchRemoteFile,
            'ftp' : self.fetchRemoteFile
            }; actions.get(self.scheme, scheme_err)()

        return self.filedest + "/" + self.filename

    def doGrab(self, file, dest, totalsize):
	from time import time
        tnow, oldsize = int(time()), 0
        p = Progress(totalsize)
        bs, size = 1024*4, 0

        chunk = file.read(bs)
        size = size + len(chunk)
        self.percent = p.update(size)
        while chunk:
            dest.write(chunk)
            chunk = file.read(bs)
            size = size + len(chunk)
            if tnow != int(time()):
                self.rate = (size - oldsize) / (int(time()) - tnow) / 1024
                oldsize, tnow = size, int(time())
            if p.update(size):
                self.percent = p.percent
		if self.percentHook != None:
			self.percentHook(self.filename, self.percent, self.rate)

        dest.close()
        print ""


    def fetchLocalFile (self):
        from shutil import copyfile

        if os.access(self.filepath, os.F_OK) == False:
            self.err("no such file or no perm to read")

        dest = open(self.filedest + "/" + self.filename , "w")
        totalsize = os.path.getsize(self.filepath)
        file = open(self.filepath)
        self.doGrab(file, dest, totalsize)


    def fetchRemoteFile (self):
        from httplib import HTTPException

        try:
            file = urllib2.urlopen(self.uri)
            headers = file.info()
    
        except ValueError, e:
            self.err('%s' % (e, ))
        except IOError, e:
            self.err('%s' % (e, ))
        except OSError, e:
            self.err('%s' % (e, ))
        except HTTPException, e:
            self.err(('(%s): %s') % (e.__class__.__name__, e))

        if not headers is None and not headers.has_key('Content-Length'):
            self.err('file not found')
        else: totalsize = int(headers['Content-Length'])

        dest = open(self.filedest + "/" + self.filename , "w")
        self.doGrab(file, dest, totalsize)


    def err (self, error):
        raise FetchError(error)

class Progress:
    def __init__(self, totalsize):
        self.totalsize = totalsize
        self.percent = 0

    def update(self, size):
        percent = (size * 100) / self.totalsize
        if percent and self.percent is not percent:
                self.percent = percent
                return percent
        else:
                return 0

if __name__ == "__main__":
    print "hububat fiyatları.."
    exit(0)
