#!/bin/sh

pwd
#rm -rf tmp
pisi-cli build https://svn.uludag.org.tr/pisi/trunk/z/zip/pspec.xml https://svn.uludag.org.tr/pisi/trunk/u/unzip/pspec.xml
pisi-cli -index .
pisi-cli -updatedb pisi-index.xml
pisi-cli -install start*pisi
pisi-cli -install popt*pisi
find tmp -iname '*.bdb' | xargs ./cat-db.py
