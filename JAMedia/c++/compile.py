#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
import commands

BASE_PATH = os.path.dirname(os.path.realpath(__file__))


def run():
    comando = "g++ -o JAMedia"

    for (f, d, fs) in os.walk(BASE_PATH):
        for fn in fs:
            fp = os.path.join(f, fn)
            fp = fp.replace(BASE_PATH, ".")
            if os.path.splitext(fp)[1] == ".cpp":
                comando = "%s %s" % (comando, fp)

    comando = "%s %s" % (comando, "`pkg-config gtkmm-3.0 --cflags --libs gstreamermm-0.10`")

    print "*** Ejecutando Comando... ***"
    text = commands.getoutput(comando)
    print text
    print "*** Comando Utilizado:\n", comando, "\n***"
    print "*** Errores:", "error" in text.lower()


if __name__ == "__main__":
    run()
