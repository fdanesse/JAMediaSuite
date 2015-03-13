#!/usr/bin/env python
# -*- coding: utf-8 -*-

# Menu.py por:
#     Flavio Danesse     <fdanesse@gmail.com>

# This program is free software; you can redistribute it and / or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation; either version 2 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the
# GNU General Public License for more details.

# You should have received a copy of the GNU General Public License
# along with this program; if not, write to the Free Software
# Foundation, Inc., 51 Franklin St, Fifth Floor, Boston, MA 02110 - 1301 USA

from gi.repository import Gtk
from gi.repository import GObject


class Menu(Gtk.MenuBar):

    __gtype_name__ = 'JAMediaEditorMenuInstaladores'

    __gsignals__ = {
    'accion-menu': (GObject.SIGNAL_RUN_LAST,
        GObject.TYPE_NONE, (GObject.TYPE_STRING, )),
    'help': (GObject.SIGNAL_RUN_LAST,
        GObject.TYPE_NONE, (GObject.TYPE_STRING, ))}

    def __init__(self):

        Gtk.MenuBar.__init__(self)

        item = Gtk.MenuItem('Seleccionar Instalador')
        menu = Gtk.Menu()
        item.set_submenu(menu)
        self.append(item)

        item = Gtk.MenuItem('Instalador debian (deb)')
        item.connect("activate", self.__emit_accion, "deb")
        menu.append(item)

        item = Gtk.MenuItem('Instalador fedora (rmp)')
        item.connect("activate", self.__emit_accion, "rmp")
        menu.append(item)

        item = Gtk.MenuItem('Instalador python')
        item.connect("activate", self.__emit_accion, "python")
        menu.append(item)

        item = Gtk.MenuItem('Instalador sin root')
        item.connect("activate", self.__emit_accion, "sin root")
        menu.append(item)

        item = Gtk.MenuItem('Instalador sugar')
        item.connect("activate", self.__emit_accion, "sugar")
        menu.append(item)

        item = Gtk.MenuItem('Ayuda')
        menu = Gtk.Menu()
        item.set_submenu(menu)
        self.append(item)

        item = Gtk.MenuItem('Instaladores en General')
        item.connect("activate", self.__emit_help, "help instaladores")
        menu.append(item)

        item = Gtk.MenuItem('Instalador debian (deb)')
        item.connect("activate", self.__emit_help, "help deb")
        menu.append(item)

        item = Gtk.MenuItem('Instalador fedora (rmp)')
        item.connect("activate", self.__emit_help, "help rmp")
        menu.append(item)

        item = Gtk.MenuItem('Instalador python')
        item.connect("activate", self.__emit_help, "help python")
        menu.append(item)

        item = Gtk.MenuItem('Instalador sin root')
        item.connect("activate", self.__emit_help, "help sin root")
        menu.append(item)

        item = Gtk.MenuItem('Instalador sugar')
        item.connect("activate", self.__emit_help, "help sugar")
        menu.append(item)

        self.show_all()

    def __emit_help(self, widget, text):
        self.emit("help", text)

    def __emit_accion(self, widget, text):
        self.emit("accion-menu", text)
