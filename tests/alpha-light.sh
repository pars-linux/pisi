#!/bin/sh

pwd
PATH=$PATH:.
set -x
pisi-cli build tests/zip/pspec.xml tests/unzip/pspec.xml
pisi-cli index .
pisi-cli add-repo repo1 pisi-index.xml
pisi-cli update-repo repo1
pisi-cli install zip
pisi-cli list-installed
pisi-cli remove unzip
pisi-cli install zip*.pisi
