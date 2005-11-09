# -*- coding: utf-8 -*-
#
# Copyright (C) 2005, TUBITAK/UEKAE
#
# This program is free software; you can redistribute it and/or modify it under
# the terms of the GNU General Public License as published by the Free
# Software Foundation; either version 2 of the License, or (at your option)
# any later version.
#
# Please read the COPYING file.
#
# Authors:  Eray Ozkural <eray@uludag.org.tr>
#           Baris Metin <baris@uludag.org.tr

"""
Metadata module provides access to metadata.xml. metadata.xml is
generated during the build process of a package and used in the
installation. Package repository also uses metadata.xml for building
a package index.
"""

import gettext
__trans = gettext.translation('pisi', fallback=True)
_ = __trans.ugettext

import pisi.context as ctx
import pisi.specfile as specfile
import pisi.xmlfile as xmlfile
import pisi.autoxml as autoxml
import pisi.util as util

class Source:
    __metaclass__ = autoxml.autoxml

    t_Name = [autoxml.String, autoxml.mandatory]
    t_Homepage = [autoxml.String, autoxml.optional]
    t_Packager = [specfile.Packager, autoxml.mandatory]

class Package(specfile.Package):
    __metaclass__ = autoxml.autoxml

    t_Build = [ autoxml.Integer, autoxml.optional]
    t_Distribution = [ autoxml.String, autoxml.mandatory]
    t_DistributionRelease = [ autoxml.String, autoxml.mandatory]
    t_Architecture = [ autoxml.String, autoxml.mandatory]
    t_InstalledSize = [ autoxml.Long, autoxml.mandatory]
    t_PackageURI = [ autoxml.String, autoxml.optional]

    def decode_hook(self, node, errs, where):
        self.version = self.history[0].version
        self.release = self.history[0].release

    def __str__(self):
        s = specfile.Package.__str__(self)
        s += _('Build: % s, Distribution: %s, Dist. Release: %s\n') % \
              (self.build, self.distribution, self.distributionRelease)
        s += _('Architecture: %s, Installed Size: %s\n') % \
            (self.architecture, self.installedSize)
        return s

class MetaData(autoxml.XmlFile):
    """Package metadata. Metadata is composed of Specfile and various
    other information. A metadata has two parts, Source and Package."""

    __metaclass__ = autoxml.autoxml

    tag = "PISI"

    t_Source = [ Source, autoxml.mandatory]
    t_Package = [ Package, autoxml.mandatory]
    #t_History = [ [Update], autoxml.mandatory]

    def from_spec(self, src, pkg):
        self.source.name = src.name
        self.source.homepage = src.homepage
        self.source.packager = src.packager
        self.package.name = pkg.name
        self.package.summary = pkg.summary
        self.package.description = pkg.description
        self.package.icon = pkg.icon
        self.package.isA = pkg.isA
        self.package.partOf = pkg.partOf
        self.package.license = pkg.license
        self.package.runtimeDependencies = pkg.runtimeDependencies
        self.package.files = pkg.files
        # FIXME: no need to copy full history with comments
        self.package.history = src.history
        self.package.conflicts = pkg.conflicts
        self.package.providesComar = pkg.providesComar
        #self.package.requiresComar = pkg.requiresComar
        self.package.additionalFiles = pkg.additionalFiles

        # FIXME: right way to do it?
        self.source.version = src.version
        self.source.release = src.release
        self.package.version = src.version
        self.package.release = src.release
