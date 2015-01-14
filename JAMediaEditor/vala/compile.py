#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
import commands

BASE_PATH = os.path.dirname(os.path.realpath(__file__))

"""
Se Necesita Tener Instalado:
valac
libgtk-3-dev
libjson-glib-dev
libghc-css-text-dev
"""


def run():
    comando = "valac --pkg posix --pkg gio-2.0 --pkg gtksourceview-3.0"
    comando = "%s %s" % (comando, "--pkg json-glib-1.0 --pkg glib-2.0")
    comando = "%s %s" % (comando, "--pkg gtk+-3.0 --pkg gdk-3.0")
    comando = "%s %s" % (comando, "JAMediaEditor.vala")

    for path in os.listdir(BASE_PATH):
        file_path = os.path.join(BASE_PATH, path)
        if os.path.splitext(file_path)[1] == ".vala":
            if path != "JAMediaEditor.vala":
                comando = "%s %s" % (comando, path)

    log = open(os.path.join(os.environ["HOME"], "compile.log"), "w")
    text = commands.getoutput(comando)
    log.write(text)
    log.close()
    print text

    #for item in comando.split():
    #    print item


if __name__ == "__main__":
    run()
