#!/usr/bin/env python
# -*- coding: utf-8 -*-

# ItemMenuBash.py por:
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


class ItemMenuBash(Gtk.MenuItem):

    __gsignals__ = {
    'help': (GObject.SIGNAL_RUN_LAST,
        GObject.TYPE_NONE, (GObject.TYPE_STRING,
        GObject.TYPE_STRING))}

    def __init__(self):

        Gtk.MenuItem.__init__(self, 'Uso básico de bash')

        menu = Gtk.Menu()

        item = Gtk.MenuItem('Directorios y Archivos')
        item.connect("activate", self.__emit_accion, "bash Clase 0")
        menu.append(item)

        item = Gtk.MenuItem('Permisos de archivos y directorios')
        item.connect("activate", self.__emit_accion, "bash Clase 1")
        menu.append(item)

        item = Gtk.MenuItem('Formatos de Archivos')
        item.connect("activate", self.__emit_accion, "bash Clase 2")
        menu.append(item)

        self.set_submenu(menu)
        self.show_all()

    def __emit_accion(self, widget, text):
        self.emit("help", text, widget.get_label())
