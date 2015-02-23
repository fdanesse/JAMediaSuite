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

#BASE_PATH = os.path.dirname(__file__)


class Menu(Gtk.MenuBar):

    #__gtype_name__ = 'JAMediaEditorMenu'

    __gsignals__ = {
    'accion': (GObject.SIGNAL_RUN_LAST,
        GObject.TYPE_NONE, (GObject.TYPE_STRING, ))}

    def __init__(self):

        Gtk.MenuBar.__init__(self)

        item = Gtk.MenuItem('Seleccionar Instalador')
        menu = Gtk.Menu()
        item.set_submenu(menu)
        self.append(item)

        item = Gtk.MenuItem('Instalador debian (deb)')
        try:
            item.get_child().destroy()
        except:
            pass
        hbox = Gtk.HBox()
        boton1 = Gtk.RadioButton()
        boton1.set_active(False)
        hbox.pack_start(boton1, False, False, 0)
        label = Gtk.Label('Instalador debian (deb)')
        hbox.pack_start(label, False, False, 5)
        item.add(hbox)
        item.connect("activate", self.__emit_accion, "deb")
        menu.append(item)

        item = Gtk.MenuItem('Instalador python')
        try:
            item.get_child().destroy()
        except:
            pass
        hbox = Gtk.HBox()
        boton2 = Gtk.RadioButton()
        boton2.join_group(boton1)
        boton2.set_active(False)
        hbox.pack_start(boton2, False, False, 0)
        label = Gtk.Label('Instalador python')
        hbox.pack_start(label, False, False, 5)
        item.add(hbox)
        item.connect("activate", self.__emit_accion, "gnome")
        menu.append(item)

        item = Gtk.MenuItem('Instalador sugar')
        try:
            item.get_child().destroy()
        except:
            pass
        hbox = Gtk.HBox()
        boton3 = Gtk.RadioButton()
        boton3.join_group(boton1)
        boton3.set_active(False)
        hbox.pack_start(boton3, False, False, 0)
        label = Gtk.Label('Instalador sugar')
        hbox.pack_start(label, False, False, 5)
        item.add(hbox)
        item.connect("activate", self.__emit_accion, "sugar")
        menu.append(item)

        self.show_all()

    def __emit_accion(self, widget, tipo):
        print tipo
        valor = not widget.get_children()[0].get_children()[0].get_active()
        if valor:
            widget.get_children()[0].get_children()[0].set_active(valor)
            #label = widget.get_children()[0].get_children()[1]
            #self.emit("accion-menu", menu, label.get_text(), valor)
