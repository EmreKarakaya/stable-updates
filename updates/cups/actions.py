#!/usr/bin/python
# -*- coding: utf-8 -*-
#
# Licensed under the GNU General Public License, version 3.
# See the file http://www.gnu.org/licenses/gpl.txt

from pisi.actionsapi import shelltools
from pisi.actionsapi import autotools
from pisi.actionsapi import pisitools
from pisi.actionsapi import get

def setup():
    shelltools.export("DSOFLAGS", get.LDFLAGS())
    shelltools.export("CFLAGS", "%s -DLDAP_DEPRECATED" % get.CFLAGS())
    shelltools.export("LDFLAGS", "%s -lgcrypt" % get.LDFLAGS())

    # pdftops from cups is currently overridden by our additional file

    # For --enable-avahi
    autotools.aclocal("-I config-scripts")
    autotools.autoconf("-I config-scripts")

    options = '--with-cups-user=lp \
               --with-cups-group=lp \
               --with-system-groups=lpadmin \
               --with-docdir=/usr/share/cups/html \
               --with-dbusdir=/etc/dbus-1 \
               --with-optim="%s -fstack-protector-all -DLDAP_DEPRECATED=1" \
               --with-php=/usr/bin/php-cgi \
               --without-java \
               --enable-acl \
               --enable-libpaper \
               --enable-debug \
               --enable-avahi \
               --enable-gssapi \
               --enable-dbus \
               --enable-pam \
               --enable-tiff \
               --enable-relro \
               --enable-dnssd \
               --enable-browsing \
               --enable-threads \
               --enable-gnutls \
               --disable-launchd \
               --without-rcdir ' % get.CFLAGS()

    if get.buildTYPE() == "emul32":
        shelltools.export("CC", "%s -m32" % get.CC())
        shelltools.export("CXX", "%s -m32" % get.CXX())

        options += ' --disable-avahi \
                     --disable-gssapi \
                     --without-php \
                     --bindir=/usr/bin32 \
                     --sbindir=/usr/sbin32 \
                     --libdir=/usr/lib32'

    autotools.configure(options)

def build():
    autotools.make("-j1 V=1")

#def check():
    #autotools.make("check")

def install():
    if get.buildTYPE() == "emul32":
        # SERVERBIN is hardcoded to /usr/lib/cups, thus it overwrites 64 bit libraries
        autotools.rawInstall("BUILDROOT=%s SERVERBIN=%s/usr/serverbin32 install-libs" % (get.installDIR(), get.installDIR()))
        pisitools.removeDir("/usr/bin32")
        pisitools.removeDir("/usr/sbin32")
        pisitools.removeDir("/usr/serverbin32")
        pisitools.removeDir("var/run")
        return
    else:
        autotools.rawInstall("BUILDROOT=%s" % get.installDIR())

    pisitools.dodir("/usr/share/cups/profiles")

    # Serial backend needs to run as root
    #shelltools.chmod("%s/usr/lib/cups/backend/serial" % get.installDIR(), 0700)

    pisitools.dodoc("CHANGES.txt", "CREDITS.txt", "LICENSE.txt", "README.txt")
