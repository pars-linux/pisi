# PISI Configuration module is used for gathering and providing
# regular PISI configurations.

# Authors: Baris Metin <baris@uludag.org.tr
#          Eray Ozkural <eray@uludag.org.tr>

#TODO: Eventually PISI will have a configuration file (located in
#/etc/pisi/conf?) and this module will provide access to those
#configuration parameters.

import os
from ConfigParser import ConfigParser, NoSectionError
from constants import const

class ConfigException(Exception):
    pass

class GeneralDefaults:
    destinationDirectory = os.getcwd()+"/tmp" # FOR ALPHA

class BuildDefaults:
    host = "i686-pc-linux-gnu"
    CFLAGS = "-mcpu=i686 -O2 -pipe -fomit-frame-pointer"
    CXXFLAGS= "-mcpu=i686 -O2 -pipe -fomit-frame-pointer"

class ConfigurationSection(object):
    def __init__(self, section, items=[]):
        self.items = items
        
        if section == "general":
            self.defaults = GeneralDefaults
        elif section == "build":
            self.defaults = BuildDefaults
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

# should we move this class to its own module?
class ConfigurationFile(object):
    def __init__(self, filePath):
        parser = ConfigParser()
        self.filePath = filePath
        #/etc/pisi/pisi.conf
        #[general]
        #destinationDirectory = /tmp
        #[build]
        #host = i686-pc-linux-gnu
        #CFLAGS= -mcpu=i686 -O2 -pipe -fomit-frame-pointer
        #CXXFLAGS= -mcpu=i686 -O2 -pipe -fomit-frame-pointer

        parser.read(self.filePath)

        try:
            self.general = ConfigurationSection("general",
                                                parser.items("general"))
            self.build = ConfigurationSection("build",
                                              parser.items("build"))
        except NoSectionError:
            self.general = ConfigurationSection("general")
            self.build = ConfigurationSection("build")


class Config(object):
    """Config Singleton"""
    
    class configimpl:

        def __init__(self):
            self.conf = ConfigurationFile("/etc/pisi/pisi.conf")
            self.destdir = self.conf.general.destinationDirectory

        # directory accessor functions
        # here is how it goes
        # x_dir: system wide directory for storing info type x
        # pkg_x_dir: per package directory for storing info type x

        def lib_dir(self):
            return self.destdir + const.lib_dir_suffix

        def db_dir(self):
            return self.destdir + const.db_dir_suffix

        def archives_dir(self):
            return self.destdir + const.archives_dir_suffix
    
        def tmp_dir(self):
            return self.destdir + const.tmp_dir_suffix

        def install_dir(self):
            return self.tmp_dir() + const.install_dir_suffix

    __configinstance = configimpl()

    def __init__(self):
        pass

    def __getattr__(self, attr):
        return getattr(self.__configinstance, attr)

    def __setattr__(self, attr, value):
        return setattr(self.__configinstance, attr, value)


config = Config()
