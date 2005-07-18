# PISI Configuration File module, obviously, is used to read from the
# configuration file. Module also defines default values for
# configuration parameters.

# Configuration file is located in /etc/pisi/pisi.conf by default,
# having an INI like format like below.
#
#[general]
#destinationdirectory = /tmp
#
#[build]
#host = i686-pc-linux-gnu
#CFLAGS= -mcpu=i686 -O2 -pipe -fomit-frame-pointer
#CXXFLAGS= -mcpu=i686 -O2 -pipe -fomit-frame-pointer
#
#[svn]
#username = caglar
#password = isteoylebirsey

import os
from ConfigParser import ConfigParser, NoSectionError


class ConfigException(Exception):
    pass

class GeneralDefaults:
    """Default values for [general] section"""
    destinationdirectory = os.getcwd() + "/tmp" # FOR ALPHA

class BuildDefaults:
    """Default values for [build] section"""
    host = "i686-pc-linux-gnu"
    CFLAGS = "-mcpu=i686 -O2 -pipe -fomit-frame-pointer"
    CXXFLAGS= "-mcpu=i686 -O2 -pipe -fomit-frame-pointer"

class SvnDefaults:
    """Default values for [svn] section """
    username =  password = None

class ConfigurationSection(object):
    """ConfigurationSection class defines a section in the configuration
    file, using defaults (above) as a fallback."""
    def __init__(self, section, items=[]):
        self.items = items
        
        if section == "general":
            self.defaults = GeneralDefaults
        elif section == "build":
            self.defaults = BuildDefaults
        elif section == "svn":
            self.defaults = SvnDefaults
        else:
            e = "No section by name '%s'" % section
            raise ConfigException, e

        self.section = section

    def __getattr__(self, attr):
        if not self.items:
            if hasattr(self.defaults, attr):
                return getattr(self.defaults, attr)
            return ""
        for item in self.items:
            if item[0] == attr:
                return item[1]
        return ""


class ConfigurationFile(object):
    """Parse and get configuration values from the configuration file"""
    def __init__(self, filePath):
        parser = ConfigParser()
        self.filePath = filePath

        parser.read(self.filePath)

        try:
            generalitems = parser.items("general")
        except NoSectionError:
            generalitems = []
        self.general = ConfigurationSection("general", generalitems)

        try:
            builditems = parser.items("build")
        except NoSectionError:
            builditems = []
        self.build = ConfigurationSection("build", builditems)

        try:
            svnitems = parser.items("svn")
        except NoSectionError:
            svnitems = []
        self.svn = ConfigurationSection("svn", svnitems)
