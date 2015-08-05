#!/usr/bin/env python
# -*- coding: utf-8 -*-

# ItemMenuJAMediaEditor.py por:
#   Flavio Danesse <fdanesse@gmail.com>

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


class MenuJAMediaPygiHack(Gtk.MenuItem):

    __gsignals__ = {
    'help': (GObject.SIGNAL_RUN_LAST,
        GObject.TYPE_NONE, (GObject.TYPE_STRING,
        GObject.TYPE_STRING))}

    def __init__(self):

        Gtk.MenuItem.__init__(self, 'Uso de JAMediaPygiHack')

        menu = Gtk.Menu()

        #item = Gtk.MenuItem('Uso de JAMediaPyGiHack')
        #item.connect("activate", self.__emit_accion,
        #    "JAMediaPyGiHack", item.get_label())
        #menu.append(item)

        self.set_submenu(menu)
        self.show_all()
        self.set_sensitive(False)

    def __emit_accion(self, widget, text, titulo):
        self.emit("help", text, titulo)


class MenuJAMediaEditor(Gtk.MenuItem):

    __gsignals__ = {
    'help': (GObject.SIGNAL_RUN_LAST,
        GObject.TYPE_NONE, (GObject.TYPE_STRING,
        GObject.TYPE_STRING))}

    def __init__(self):

        Gtk.MenuItem.__init__(self, 'Uso de JAMediaEditor')

        menu = Gtk.Menu()

        item = Gtk.MenuItem('Modo Proyecto')
        item.connect("activate", self.__emit_accion,
            'Modo Proyecto', item.get_label())
        menu.append(item)
        item.set_sensitive(False)

        menu_instaladores = ItemMenuInstaladores()
        menu_instaladores.connect("help", self.__emit_accion)
        menu.append(menu_instaladores)

        self.set_submenu(menu)
        self.show_all()

    def __emit_accion(self, widget, text, titulo):
        self.emit("help", text, titulo)


class ItemMenuInstaladores(Gtk.MenuItem):

    __gsignals__ = {
    'help': (GObject.SIGNAL_RUN_LAST,
        GObject.TYPE_NONE, (GObject.TYPE_STRING,
        GObject.TYPE_STRING))}

    def __init__(self):

        Gtk.MenuItem.__init__(self, 'Construcción de Instaladores')

        menu_instaladores = MenuInstaladores()
        menu_instaladores.connect("help", self.__emit_accion)
        self.set_submenu(menu_instaladores)
        self.show_all()

    def __emit_accion(self, widget, text, titulo):
        self.emit("help", text, titulo)


class MenuInstaladores(Gtk.Menu):

    __gsignals__ = {
    'help': (GObject.SIGNAL_RUN_LAST,
        GObject.TYPE_NONE, (GObject.TYPE_STRING,
        GObject.TYPE_STRING))}

    def __init__(self):

        Gtk.Menu.__init__(self)

        item = Gtk.MenuItem('Instaladores en General')
        item.connect("activate", self.__emit_accion, "help instaladores")
        self.append(item)

        item = Gtk.MenuItem('Instalador debian (deb)')
        item.connect("activate", self.__emit_accion, "help deb")
        self.append(item)

        item = Gtk.MenuItem('Instalador fedora (rmp)')
        item.connect("activate", self.__emit_accion, "help rmp")
        self.append(item)
        item.set_sensitive(False)

        item = Gtk.MenuItem('Instalador python')
        item.connect("activate", self.__emit_accion, "help python")
        self.append(item)

        item = Gtk.MenuItem('Instalador sin root')
        item.connect("activate", self.__emit_accion, "help sin root")
        self.append(item)

        item = Gtk.MenuItem('Instalador sugar')
        item.connect("activate", self.__emit_accion, "help sugar")
        self.append(item)

        self.show_all()

    def __emit_accion(self, widget, text):
        self.emit("help", text, widget.get_label())
