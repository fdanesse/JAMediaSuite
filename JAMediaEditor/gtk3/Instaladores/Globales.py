#!/usr/bin/env python
# -*- coding: utf-8 -*-

#   Globales.py por:
#       Flavio Danesse      <fdanesse@gmail.com>

# This program is free software; you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation; either version 2 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program; if not, write to the Free Software
# Foundation, Inc., 51 Franklin St, Fifth Floor, Boston, MA  02110-1301  USA

import os

CONFPATH = os.path.join(os.environ["HOME"], "JAMediaEditorCONF")
DEBPATH = os.path.join(CONFPATH, "DEB")
GNOMEPATH = os.path.join(CONFPATH, "GNOME")
SUGARPATH = os.path.join(CONFPATH, "SUGAR")


def get_guion_desktop(proyecto, iconpath):
    texto = "[Desktop Entry]\n"
    texto = "%sEncoding=UTF-8\n" % (texto)
    texto = "%sName=%s\n" % (texto, proyecto["nombre"])
    texto = "%sGenericName=%s\n" % (texto, proyecto["nombre"])
    texto = "%sComment=%s\n" % (texto, proyecto["descripcion"])
    texto = "%sExec=/usr/bin/%s\n" % (texto, proyecto["nombre"].lower())
    texto = "%sTerminal=false\n" % (texto)
    texto = "%sType=Application\n" % (texto)
    texto = "%sIcon=%s\n" % (texto, iconpath)
    texto = "%sCategories=%s\n" % (texto, proyecto["categoria"])
    texto = "%sStartupNotify=true\n" % (texto)
    texto = "%sMimeType=%s\n" % (texto, proyecto["mimetypes"])
    return texto


def get_guion_deb_control(proyecto):
    texto = "Package: %s\n" % proyecto["nombre"].lower()
    texto = "%sSource: %s\n" % (texto, proyecto["nombre"])
    texto = "%sVersion: %s\n" % (texto, proyecto["version"])
    texto = "%sSection: %s\n" % (texto, proyecto["categoria"])
    texto = "%sPriority: optional\n" % (texto)
    texto = "%sArchitecture: all\n" % (texto)
    texto = "%sMaintainer: \n" % (texto)
    texto = "%sHomepage: %s\n" % (texto, proyecto["url"])
    texto = "%sDepends: \n" % (texto)
    texto = "%sDescription: %s\n" % (texto, proyecto["descripcion"])
    texto = "%s %s\n" % (texto, proyecto["descripcion"])
    return texto


def get_guion_lanzador_python(proyecto):
    nombre = proyecto["nombre"]
    main = proyecto["main"]
    return "#!/bin/sh\nexec \"/usr/bin/python\" \"/usr/share/%s/%s\" \"$@\"" % (nombre, main)


def get_path(name):
    for path in [CONFPATH, DEBPATH, GNOMEPATH, SUGARPATH]:
        if not os.path.exists(path):
            os.mkdir(path)
    if name == "deb":
        return DEBPATH
    elif name == "gnome":
        return GNOMEPATH
    elif name == "sugar":
        return SUGARPATH
