#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
import commands

BASE_PATH = os.path.dirname(__file__)

comando = "valac --pkg glib-2.0 --pkg gtk+-3.0 --pkg gdk-3.0 JAMedia.vala"

for path in os.listdir(BASE_PATH):
    file_path = os.path.join(BASE_PATH, path)
    if os.path.splitext(file_path)[1] == ".vala":
        if path != "JAMedia.vala":
            comando = "%s %s" % (comando, path)

print commands.getoutput(comando)

#for item in comando.split():
#    print item
