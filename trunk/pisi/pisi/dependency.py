# dependency analyzer
# Author:  Eray Ozkural <eray@uludag.org.tr>

from installdb import installdb
import packagedb
from ui import ui
from version import Version

def satisfiesDep(pkg, depinfo):
    """determine if a package satisfies given dependency spec"""
    if not installdb.is_installed(depinfo.package):
        return False
    else:
        (version, release) = installdb.get_info(pkg)
        ret = True
        if depinfo.versionFrom:
            ret &= Version(version) >= Version(depinfo.versionFrom)
        if depinfo.versionTo:
            ret &= Version(version) <= Version(depinfo.versionTo)        
        if depinfo.releaseFrom:
            ret &= Version(release) <= Version(depinfo.releaseFrom)        
        if depinfo.releaseTo:
            ret &= Version(release) <= Version(depinfo.releaseTo)       
        return ret

def runtimeDeps(pkg):
    return packagedb.get_package(pkg).runtimeDeps

def satisfiesRuntimeDeps(pkg):
    deps = runtimeDeps(pkg)
#    print 'runtimedeps = ', deps
    return reduce(lambda x,y:x and y,
                  map(lambda x: satisfiesDep(pkg, x), deps),True)

def installable(pkg):
    """calculate if pkg is installable currently 
    which means it has to satisfy both install and runtime dependencies"""
    if not packagedb.has_package(pkg):
        ui.info("package " + pkg + " is not present in the package database\n");
        return False
    elif satisfiesRuntimeDeps(pkg):
        return True
    else:
        ui.info("package " + pkg + " does not satisfy dependencies\n");
        return False

