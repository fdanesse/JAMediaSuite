#!/usr/bin/env python
# -*- coding: utf-8 -*-

#   JAMediaPygiHack.py por:
#       Flavio Danesse <fdanesse@gmail.com>
#       Uruguay

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
from gi.repository import GObject

from Widgets import Toolbar
from BasePanel import BasePanel

BASE_PATH = os.path.dirname(__file__)


class JAMediaPyGiHack(Gtk.EventBox):

    __gtype_name__ = 'JAMediaPyGiHack'

    __gsignals__ = {
    'salir': (GObject.SIGNAL_RUN_LAST,
        GObject.TYPE_NONE, [])}

    def __init__(self):

        Gtk.EventBox.__init__(self)

        vbox = Gtk.VBox()

        self.toolbar = Toolbar()
        vbox.pack_start(self.toolbar, False, False, 0)

        self.base_panel = BasePanel()
        vbox.pack_start(self.base_panel, True, True, 0)

        self.add(vbox)
        self.show_all()

        self.toolbar.connect("import", self.__import)
        self.toolbar.connect("accion-menu", self.__set_accion)
        self.toolbar.connect("salir", self.__emit_salir)
        self.base_panel.connect("update", self.__update)

    def __emit_salir(self, widget):
        self.emit('salir')

    def __update(self, widget, view):
        if view == "Terminal":
            pass
        elif view == "Gstreamer - Inspect 1.0" or view == "Apis PyGiHack":
            self.toolbar.update(view)

    def __set_accion(self, widget, menu, wid_lab, valor):
        self.base_panel.set_accion(menu, wid_lab, valor)

    def __import(self, widget, paquete, modulo):
        self.base_panel.import_modulo(paquete, modulo)


class Ventana(Gtk.Window):

    __gtype_name__ = 'VentanaJAMediaPyGiHack'

    def __init__(self):

        Gtk.Window.__init__(self)

        self.set_title("JAMediaPygiHack")
        self.set_icon_from_file(os.path.join(BASE_PATH,
            "Iconos", "PygiHack.svg"))

        self.set_resizable(True)
        self.set_size_request(640, 480)
        self.maximize()
        self.set_border_width(2)
        self.set_position(Gtk.WindowPosition.CENTER)

        jamediapygihack = JAMediaPyGiHack()
        self.add(jamediapygihack)

        self.show_all()
        self.realize()

        jamediapygihack.connect("salir", self.__salir)
        self.connect("delete-event", self.__salir)

    def __salir(self, widget=None, senial=None):
        import sys
        sys.exit(0)


if __name__ == "__main__":
    Ventana()
    Gtk.main()
