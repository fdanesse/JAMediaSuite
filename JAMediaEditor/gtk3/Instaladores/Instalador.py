#!/usr/bin/env python
# -*- coding: utf-8 -*-

#   Instalador.py por:
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

from gi.repository import Gtk
from gi.repository import GdkX11

from Menu import Menu
from Debian import DebianWidget
from Globales import DialogoLoad
from Help.HelpWidget import HelpWidget

screen = GdkX11.X11Screen.get_default()
w = screen.width()
h = screen.height()


class Instalador(Gtk.Window):
    """
    Dialogo para presentar Información de Instaladores.
    """

    __gtype_name__ = 'JAMediaEditorInstalador'

    def __init__(self, parent_window, path):

        Gtk.Window.__init__(self)

        self.proyecto_path = path
        self.parent_window = parent_window

        self.set_title("Constructor de Instaladores de Proyecto")
        self.set_transient_for(self.parent_window)
        self.set_border_width(15)

        self.vbox = Gtk.Box(orientation=Gtk.Orientation.VERTICAL)
        self.menu = Menu()

        self.vbox.pack_start(self.menu, False, False, 0)
        self.vbox.pack_start(Gtk.Label("Constructor de Instaladores"),
            False, False, 0)

        self.resize(w / 2, h - 40)
        self.move(w - w / 2, 40)

        self.add(self.vbox)
        self.show_all()

        self.menu.connect("accion-menu", self.__accion_menu)

    def __accion_menu(self, widget, texto, valor):
        child = self.vbox.get_children()[-1]
        if child:
            self.vbox.remove(child)
            child.destroy()
        if valor:
            t = "Cargando . . ."
            t = "%s\n%s" % (t, "Por favor espera un momento.")
            dialogo = DialogoLoad(self, t)
            dialogo.connect("running", self.__load, texto)
            dialogo.run()

    def __load(self, dialogo, texto):
        if texto == "deb":
            instalador = DebianWidget(self.proyecto_path)
            self.vbox.pack_start(instalador, True, True, 0)
        elif texto == "rmp":
            self.vbox.pack_start(Gtk.Label("rpm"), True, True, 0)
        elif texto == "standard":
            self.vbox.pack_start(Gtk.Label("standard"), True, True, 0)
        elif texto == "sin root":
            self.vbox.pack_start(Gtk.Label("sin root"), True, True, 0)
        elif texto == "sugar":
            self.vbox.pack_start(Gtk.Label("sugar"), True, True, 0)
        else:
            help = HelpWidget(texto)
            self.vbox.pack_start(help, True, True, 0)
        dialogo.destroy()
        self.show_all()
