#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
import commands

BASE_PATH = os.path.dirname(os.path.realpath(__file__))


def run():
    comando = "valac --pkg posix --pkg gio-2.0 --pkg libsoup-2.4"
    comando = "%s %s" % (comando, "--pkg json-glib-1.0 --pkg glib-2.0")
    comando = "%s %s" % (comando, "--pkg gtk+-3.0 --pkg gdk-3.0 --pkg gdk-x11-3.0")
    comando = "%s %s" % (comando, "--pkg gstreamer-1.0 --pkg gstreamer-video-1.0")
    comando = "%s %s" % (comando, "--pkg cairo JAMedia.vala")

    for path in os.listdir(BASE_PATH):
        file_path = os.path.join(BASE_PATH, path)
        if os.path.splitext(file_path)[1] == ".vala":
            if path != "JAMedia.vala":
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
