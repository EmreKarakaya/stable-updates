#!/usr/bin/python
# -*- coding: utf-8 -*-
#
# Copyright 2009,2010 TUBITAK/UEKAE
# Licensed under the GNU General Public License, version 2.
# See the file http://www.gnu.org/licenses/old-licenses/gpl-2.0.txt

from pisi.actionsapi import autotools
from pisi.actionsapi import pisitools
from pisi.actionsapi import shelltools
from pisi.actionsapi import get

def setup():
    pisitools.dosed("Makefile","/usr/local","/usr")
    pass

def build():
    autotools.make("-j1")


def install():
    autotools.rawInstall("DESTDIR=%s" % get.installDIR())

    pisitools.dodoc("RELEASE_NOTES.HTML")