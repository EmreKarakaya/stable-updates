#!/usr/bin/python
# -*- coding: utf-8 -*-
#
# Licensed under the GNU General Public License, version 3.
# See the file http://www.gnu.org/licenses/gpl.txt

from pisi.actionsapi import shelltools
from pisi.actionsapi import autotools
from pisi.actionsapi import pisitools
from pisi.actionsapi import get
from pisi.actionsapi import libtools

shelltools.export("HOME", get.workDIR())
suffix = "32" if get.buildTYPE() == "emul32" else ""

def setup():
    #shelltools.echo("docs/gtk-doc.make", "EXTRA_DIST=")
    autotools.autoreconf("-fi")
    libtools.libtoolize("--force")

    options = " ac_cv_header_sys_capability_h=yes \
                --bindir=/sbin%s \
                --sbindir=/sbin%s \
                --docdir=/usr/share/doc/udev \
                --libdir=/usr/lib%s \
                --libexecdir=/lib%s/udev \
                --with-distro=other \
                --with-firmware-path=/lib%s/firmware/updates:/lib%s/firmware \
                --with-html-dir=/usr/share/doc/udev/html \
                --with-rootlibdir=/lib%s \
                --with-rootprefix= \
                --without-python \
                --disable-audit \
                --disable-coredump \
                --disable-hostnamed \
                --disable-ima \
                --disable-libcryptsetup \
                --disable-localed \
                --disable-logind \
                --disable-myhostname \
                --disable-nls \
                --disable-pam \
                --disable-quotacheck \
                --disable-readahead \
                --enable-split-usr \
                --disable-tcpwrap \
                --disable-timedated \
                --disable-xz \
                --enable-gudev \
                --disable-selinux \
                --enable-static \
                --enable-acl \
                --enable-kmod \
                --enable-keymap \
                --enable-introspection \
               " % ((suffix, )*7)

    options += "--disable-acl \
                --disable-qrencode \
                --disable-static \
                --disable-microhttpd \
               " if get.buildTYPE() == "emul32" else ""

    autotools.configure(options)

def build():
    shelltools.echo("Makefile.extra", "BUILT_SOURCES: $(BUILT_SOURCES)")
    autotools.make("-f Makefile -f Makefile.extra")

    targets = " systemd-udevd \
                udevadm \
                libudev.la \
                libsystemd-daemon.la \
                ata_id \
                cdrom_id \
                collect \
                scsi_id \
                v4l_id \
                accelerometer \
                mtd_probe \
                keymap \
                libgudev-1.0.la"

    targets += "\
                man/sd_is_fifo.3 \
                man/sd_notify.3 \
                man/sd_listen_fds.3 \
                man/sd-daemon.3 \
                man/udev.7 \
                man/udevadm.8 \
                man/systemd-udevd.8 \
               " if not get.buildTYPE() == "emul32" else ""

    autotools.make(targets)

    autotools.make("-C docs/libudev")
    autotools.make("-C docs/gudev")

#~ def check():
    #~ autotools.make("check")
#~ 

def install():
    targets = " install-libLTLIBRARIES \
                install-includeHEADERS \
                install-libgudev_includeHEADERS \
                install-binPROGRAMS \
                install-rootlibexecPROGRAMS \
                install-udevlibexecPROGRAMS \
                install-dist_systemunitDATA \
                install-dist_udevconfDATA \
                install-dist_udevhomeSCRIPTS \
                install-dist_udevkeymapDATA \
                install-dist_udevkeymapforcerelDATA \
                install-dist_udevrulesDATA \
                install-girDATA \
                install-nodist_systemunitDATA \
                install-pkgconfiglibDATA \
                install-sharepkgconfigDATA \
                install-typelibsDATA \
                install-dist_docDATA \
                libudev-install-hook \
                install-directories-hook \
                install-dist_bashcompletionDATA \
                rootlibexec_PROGRAMS='systemd-udevd' \
                bin_PROGRAMS='udevadm' \
                lib_LTLIBRARIES='libsystemd-daemon.la libudev.la \
                                 libgudev-1.0.la' \
                pkgconfiglib_DATA='src/libsystemd-daemon/libsystemd-daemon.pc src/libudev/libudev.pc \
                                   src/gudev/gudev-1.0.pc' \
                dist_systemunit_DATA='units/systemd-udevd-control.socket \
                                      units/systemd-udevd-kernel.socket' \
                nodist_systemunit_DATA='units/systemd-udevd.service \
                                        units/systemd-udev-trigger.service \
                                        units/systemd-udev-settle.service' \
                pkginclude_HEADERS='src/systemd/sd-daemon.h' \
              "

    targets += "\
                install-man3 \
                install-man7 \
                install-man8 \
                MANPAGES='man/sd-daemon.3 man/sd_notify.3 man/sd_listen_fds.3 \
                          man/sd_is_fifo.3 man/sd_booted.3 man/udev.7 man/udevadm.8 \
                          man/systemd-udevd.service.8' \
                MANPAGES_ALIAS='man/sd_is_socket.3 man/sd_is_socket_unix.3 \
                                man/sd_is_socket_inet.3 man/sd_is_mq.3 man/sd_notifyf.3 \
                                man/SD_LISTEN_FDS_START.3 man/SD_EMERG.3 man/SD_ALERT.3 \
                                man/SD_CRIT.3 man/SD_ERR.3 man/SD_WARNING.3 man/SD_NOTICE.3 \
                                man/SD_INFO.3 man/SD_DEBUG.3 man/systemd-udevd.8' \
               " if not get.buildTYPE() == "emul32" else ""

    autotools.make("-j1 DESTDIR=%s%s %s" % (get.installDIR(), suffix, targets))
    if get.buildTYPE() == "emul32":
        shelltools.move("%s%s/lib%s" % (get.installDIR(), suffix, suffix), "%s/lib%s" % (get.installDIR(), suffix))
        shelltools.move("%s%s/usr/lib%s" % (get.installDIR(), suffix, suffix), "%s/usr/lib%s" % (get.installDIR(), suffix))
        #shelltools.unlinkDir("%s%s" % (get.installDIR(), suffix))
        return
    # Create needed directories
    #for d in ("", "net", "pts", "shm", "hugepages"):
         #pisitools.dodir("/lib/udev/devices/%s" % d)

    #Create vol_id and scsi_id symlinks in /sbin probably needed by multipath-tools
    pisitools.dosym("/lib/udev/scsi_id", "/sbin/scsi_id")

    #Create /sbin/systemd-udevd -> /sbin/udevd sysmlink, we need it for MUDUR, do not touch this sysmlink.
    pisitools.dosym("/sbin/systemd-udevd", "/sbin/udevd")
    pisitools.dosym("/lib/systemd/systemd-udevd", "/sbin/systemd-udevd")

    #Create /etc/udev/rules.d for backward compatibility
    pisitools.dodir("/etc/udev/rules.d")
    pisitools.dodoc("README", "TODO")
