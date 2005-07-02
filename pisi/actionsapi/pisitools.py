#!/usr/bin/python
# -*- coding: utf-8 -*-

# standard python modules
import os
import gzip

from pisi.util import copy_file

# actions api modules
from actionglobals import glb

def dodoc(*documentList):
    env = glb.env
    dirs = glb.dirs

    srcTag = env.src_name + '-' \
        + env.src_version + '-' \
        + env.src_release
    
    try:
        os.makedirs(os.path.join(env.install_dir,
                                 dirs.doc,
                                 srcTag))
    except OSError:
        pass

    for document in documentList:
        if os.access(document, os.F_OK):
            copy_file(document, 
                            os.path.join(env.install_dir,
                                         dirs.doc,
                                         srcTag,
                                         os.path.basename(document)))

def dosed(filename, *sedPattern):
    #FIXME: Convert to python
    for pattern in sedPattern:
        os.system('sed -i -e \'' + pattern + '\' ' +  filename)

def dosbin(filename, destination=glb.dirs.sbin):
    env = glb.env

    try:
        os.makedirs(os.path.join(env.install_dir, destination))
    except OSError:
        pass

    if os.access(filename, os.F_OK):
        copy_file(filename,
                        os.path.join(env.install_dir,
                                     destination,
                                     os.path.basename(filename)))

def doman(filename):
    env = glb.env
    dirs = glb.dirs

    man, postfix = filename.split('.')
    destDir = os.path.join(env.install_dir, dirs.man, "man" + postfix)
    try:
        os.makedirs(destDir)
    except OSError:
        pass

    gzfile = gzip.GzipFile(filename + '.gz', 'w', 9)
    gzfile.writelines(file(filename).xreadlines())
    gzfile.close()

    if os.access(filename, os.F_OK):
        copy_file(filename + '.gz',
                        os.path.join(destDir,
                                     os.path.basename(filename)))

