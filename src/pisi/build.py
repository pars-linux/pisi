# -*- coding: utf-8 -*-
# package bulding stuff
# maintainer: baris and meren

# python standard library
import os

from fetcher import Fetcher
from archive import Archive

# import pisipackage
import util
import ui

class PisiBuildError(Exception):
    pass

# FIXME: this eventually has to go to ui module
# Infact all ui calls has nothing to do with this build process.
# There more of them in PisiBuild...
# And maybe we should consider moving PisiBuild.build() back to pisi-build CLI too.
def displayProgress(pd):
    out = '\r%-30.30s %3d%% %12.2f %s' % \
        (pd['filename'], pd['percent'], pd['rate'], pd['symbol'])
    ui.info(out)

class PisiBuild:
    """PisiBuild class, provides the package build and creation routines"""
    def __init__(self, context):
        self.ctx = context
	self.work_dir = self.ctx.build_work_dir()

        self.spec = self.ctx.spec

    def build(self):
        ui.info("Building PISI source package: %s\n" % self.spec.source.name)

        ui.info("Fetching source from: %s\n" % self.spec.source.archiveUri)
        self.fetchArchive(displayProgress)
        ui.info("Source archive is stored: %s/%s\n"
                %(self.ctx.archives_dir(), self.spec.source.archiveName))
	
	self.solveBuildDependencies()
	
	ui.info("Unpacking archive...")
	self.unpackArchive()
	ui.info(" unpacked (%s)\n" % self.ctx.build_work_dir())
        
	# applyPatches()

	self.actionScript = open( os.path.dirname( self.ctx.pspecfile ) + '/' + 'actions' ).read()

	# FIXME: It's wrong to assume that unpacked archive 
	# will create a name-version top-level directory.
	# Archive module should give the exact location.
	# (from the assumption is evil dept.)
	os.chdir( self.ctx.build_work_dir() + "/" + self.spec.source.name + "-" + self.spec.source.version)
	locals = globals = {}
	
	try:
		exec compile( self.actionScript , "error", "exec" ) in locals,globals
	except SyntaxError, e:
		print "Error : %s" % e
		return 
		
	ui.info("Configuring %s...\n" % self.spec.source.name)
	self.configureSource( locals )
	ui.info("Building %s...\n" % self.spec.source.name)
	self.buildSource( locals )
	ui.info("Installing %s...\n" % self.spec.source.name)
	self.installSource( locals )

    def fetchArchive(self, percentHook=None):
        """fetch an archive and store to ctx.archives_dir() 
        using fether.Fetcher"""
        fetch = Fetcher(self.ctx)

        # check if source already cached
        destpath = fetch.filedest + "/" + fetch.filename
        if os.access(destpath, os.R_OK):
            if util.md5_file(destpath)==self.spec.source.archiveMD5:
                ui.info('%s [cached]\n' % self.spec.source.archiveName)
                return

        if percentHook:
            fetch.percentHook = percentHook
        
	fetch.fetch()

	# FIXME: What a ugly hack! We should really find a cleaner way for output.
	if percentHook:
	    ui.info('\n')

    def solveBuildDependencies(self):
    	pass

    def unpackArchive(self):
	archive = Archive(self.ctx)
	archive.unpack(self.work_dir)

    def applyPatches(self):
        pass

    def configureSource(self, locals):
	locals['src_setup']()

    def buildSource(self, locals):
	locals['src_build']()

    def installSource(self, locals):
	locals['src_install']()

    def buildPackages(self):
        for package in self.spec.packages:
            ui.info("** Building package %s\n" % package.name);
    
