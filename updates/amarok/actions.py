#!/usr/bin/python
# -*- coding: utf-8 -*-
#
# Licensed under the GNU General Public License, version 3.
# See the file http://www.gnu.org/licenses/gpl.txt

from pisi.actionsapi import shelltools
from pisi.actionsapi import pisitools
from pisi.actionsapi import get
from pisi.actionsapi import kde4

shelltools.export("HOME", get.workDIR())
shelltools.export("XDG_DATA_DIRS", get.workDIR())

def setup():
    kde4.configure("-DWITH_IPOD=ON -DCMAKE_BUILD_TYPE=Release -DCMAKE_INSTALL_PREFIX=/usr \
                    -DKDE4_BUILD_TESTS=OFF \
                    -DCMAKE_BUILD_TYPE=Debugfull \
                    -DKDE_DISTRIBUTION_TEXT='PisiLinux'")

def build():
    kde4.make()

def install():
    kde4.install()

    pisitools.dodoc("AUTHORS", "README", "COPYING", "ChangeLog")
