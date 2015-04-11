#!/usr/bin/env python
# -*- coding: utf-8 -*-

# Globales.py por:
#   Flavio Danesse <fdanesse@gmail.com>

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
from gi.repository import Gtk
from gi.repository import GLib
from gi.repository import GObject

CONFPATH = os.path.join(os.environ["HOME"], "JAMediaEditorCONF")
if not os.path.exists(CONFPATH):
    os.mkdir(CONFPATH)


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
    if proyecto["descripcion"]:
        texto = "%sDescription: %s\n" % (texto, proyecto["descripcion"])
        texto = "%s %s\n" % (texto, proyecto["descripcion"])
    else:
        texto = "%sDescription: Este campo es obligatorio\n" % (texto)
        texto = "%s Este campo es obligatorio, debe tener" % (texto)
        texto = "%s un espacio vacio al principio y" % (texto)
        texto = "%s una linea vacia al final.\n" % (texto)
    return texto


def get_guion_lanzador_sh(proyecto):
    nombre = proyecto["nombre"]
    main = proyecto["main"]
    t = "#!/bin/sh\nexec \"/usr/bin/python\" \"/usr/share/"
    t = "%s%s/%s\" \"$@\"" % (t, nombre, main)
    return t


def get_guion_setup_cfg(proyecto):
    nombre = proyecto["nombre"]
    t = "[install]\ninstall_lib=/usr/share/%s\n" % nombre
    t = "%s%s" % (t, "install_data=/usr/share/%s\n" % nombre)
    t = "%s%s" % (t, "install_scripts=/usr/bin")
    return t


def get_guion_setup_py(proyecto, data_files):
    nombre = proyecto["nombre"]
    version = proyecto["version"]
    lanzador = proyecto["nombre"].lower()

    t = "#!/usr/bin/env python\n# -*- coding: utf-8 -*-\n\n"
    t = "%s%s" % (t, "from distutils.core import setup\n\n")
    t = "%s%s" % (t, "setup(\n\tname = \"%s\",\n\tversion = \"%s\",\n\t" % (
        nombre, version))

    autores = "Este Campo es Obligatorio"
    if proyecto["autores"]:
        autores = proyecto["autores"]
    t = "%sauthor = \"%s\",\n\t" % (t, autores)
    t = "%sauthor_email = \"%s\",\n\t" % (t, autores)

    url = "Este Campo es Obligatorio"
    if proyecto["url"]:
        url = proyecto["url"]
    t = "%surl = \"%s\",\n\tlicense = \"%s\",\n\n\t" % (
        t, url, proyecto["licencia"])
    t = "%sscripts = [\"%s\"],\n\n\tpy_modules = [\"%s\"],\n\n\t" % (
        t, lanzador, proyecto["main"].split(".")[0])
    t = "%sdata_files =[\n\t\t(\"/usr/share/applications/\"" % t
    t = "%s, [\"%s.desktop\"]),\n\t\t" % (t, nombre)

    for key in data_files.keys():
        newkey = key
        if key.startswith("/"):
            newkey = ""
            for l in key[1:]:
                newkey = "%s%s" % (newkey, l)
        if newkey:
            t = "%s(\"%s/\",[\n\t\t\t" % (t, newkey)
        else:
            t = "%s(\"%s\",[\n\t\t\t" % (t, newkey)
        for item in data_files[key]:
            t = "%s\"%s\",\n\t\t\t" % (t, item)
        t = "%s]),\n\n\t\t" % t[:-5]

    t = "%s])\n\n" % t[:-5]
    t = "%s%s\n" % (t, "import commands")
    t = "%s%s" % (t, "commands.getoutput(\"chmod 755")
    t = "%s%s\n" % (t, " /usr/bin/%s\")" % lanzador)
    t = "%s%s" % (t, "commands.getoutput(\"chmod -R")
    t = "%s%s\n" % (t, " 755 /usr/share/%s\")" % nombre)
    t = "%s%s" % (t, "commands.getoutput(\"chmod 755")
    t = "%s%s\n" % (t, "/usr/applications/%s.desktop\")" % nombre)
    return t


def get_guion_activity_info(proyecto, iconname):
    t = "[Activity]\n"
    t = "%sname = %s\n" % (t, proyecto["nombre"])
    t = "%sbundle_id = org.laptop.%s\n" % (t, proyecto["nombre"])
    t = "%sexec = sugar-activity MaindelProyecto.ClaseActivity\n" % (t)
    t = "%sicon = %s\n" % (t, iconname)
    t = "%sactivity_version = %s\n" % (t, proyecto["version"])
    t = "%sshow_launcher = yes\n" % (t)
    return t


class DialogoLoad(Gtk.Dialog):

    __gtype_name__ = 'InstaladorDialogoLoad'

    __gsignals__ = {
        "running": (GObject.SIGNAL_RUN_LAST,
        GObject.TYPE_NONE, [])}

    def __init__(self, parent, texto):

        Gtk.Dialog.__init__(self,
            parent=parent,
            flags=Gtk.DialogFlags.MODAL)

        self.set_decorated(False)
        self.set_border_width(15)

        label = Gtk.Label(texto)
        label.set_justify(Gtk.Justification.CENTER)
        label.show()
        self.vbox.pack_start(label, True, True, 5)

        self.connect("realize", self.__do_realize)

    def __do_realize(self, widget):
        GLib.timeout_add(500, self.__emit_running)

    def __emit_running(self):
        self.emit("running")
        return False


class DialogoInformar(Gtk.Dialog):

    __gtype_name__ = 'InstaladorDialogoInformar'

    def __init__(self, parent, texto):

        Gtk.Dialog.__init__(self,
            parent=parent, buttons=["OK", Gtk.ResponseType.ACCEPT],
            flags=Gtk.DialogFlags.MODAL)

        self.set_decorated(False)
        self.set_border_width(15)

        label = Gtk.Label(texto)
        label.set_justify(Gtk.Justification.CENTER)
        label.show()
        self.vbox.pack_start(label, True, True, 5)
