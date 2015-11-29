#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
import commands

BASE_PATH = os.path.dirname(os.path.realpath(__file__))

"""
Se Necesita Tener Instalado:
valac
libgtk-3-dev
libgstreamer1.0-dev
libgstreamer-plugins-base1.0-dev
libgstreamer-plugins-good1.0-dev
libgstreamer-plugins-bad1.0-dev
libsoup-gnome2.4-dev
libjson-glib-dev
libghc-css-text-dev
"""


def run():
    comando = "valac --pkg posix --pkg gio-2.0 --pkg libsoup-2.4"
    comando = "%s %s" % (comando, "--pkg json-glib-1.0 --pkg glib-2.0")
    comando = "%s %s" % (comando, "--pkg gtk+-3.0 --pkg gdk-3.0 --pkg gdk-x11-3.0")
    comando = "%s %s" % (comando, "--pkg gstreamer-1.0 --pkg gstreamer-video-1.0")
    comando = "%s %s" % (comando, "--pkg cairo JAMedia.vala")

    for (f, d, fs) in os.walk(BASE_PATH):
        for fn in fs:
            if fn != "JAMedia.vala":
                fp = os.path.join(f, fn)
                fp = fp.replace(BASE_PATH, ".")
                if os.path.splitext(fp)[1] == ".vala":
                    comando = "%s %s" % (comando, fp)

    print "*** Ejecutando Comando... ***"
    text = commands.getoutput(comando)
    print text
    print "*** Comando Utilizado:\n", comando, "\n***"
    print "*** Errores:", "error" in text.lower()


if __name__ == "__main__":
    run()
