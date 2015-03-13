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


class ItemMenuInstaladores(Gtk.MenuItem):

    #__gtype_name__ = 'ItemMenuInstaladores'

    __gsignals__ = {
    'help': (GObject.SIGNAL_RUN_LAST,
        GObject.TYPE_NONE, (GObject.TYPE_STRING, ))}

    def __init__(self):

        Gtk.MenuItem.__init__(self, 'Instaladores')

        menu_instaladores = MenuInstaladores()
        menu_instaladores.connect("help", self.__emit_accion)
        self.set_submenu(menu_instaladores)
        self.show_all()

    def __emit_accion(self, widget, text):
        self.emit("help", text)


class MenuInstaladores(Gtk.Menu):

    #__gtype_name__ = 'JAMediaEditorMenuInstaladores'

    __gsignals__ = {
    'help': (GObject.SIGNAL_RUN_LAST,
        GObject.TYPE_NONE, (GObject.TYPE_STRING, ))}

    def __init__(self):

        Gtk.Menu.__init__(self)

        item = Gtk.MenuItem('Instaladores en General')
        try:
            item.get_child().destroy()
        except:
            pass
        hbox = Gtk.HBox()
        boton1 = Gtk.RadioButton()
        boton1.set_active(False)
        hbox.pack_start(boton1, False, False, 0)
        label = Gtk.Label('Instaladores en General')
        hbox.pack_start(label, False, False, 5)
        item.add(hbox)
        item.connect("activate", self.__emit_accion, "help instaladores")
        self.append(item)

        item = Gtk.MenuItem('Instalador debian (deb)')
        try:
            item.get_child().destroy()
        except:
            pass
        hbox = Gtk.HBox()
        boton7 = Gtk.RadioButton()
        boton7.join_group(boton1)
        boton7.set_active(False)
        hbox.pack_start(boton7, False, False, 0)
        label = Gtk.Label('Instalador debian (deb)')
        hbox.pack_start(label, False, False, 5)
        item.add(hbox)
        item.connect("activate", self.__emit_accion, "help deb")
        self.append(item)

        item = Gtk.MenuItem('Instalador fedora (rmp)')
        try:
            item.get_child().destroy()
        except:
            pass
        hbox = Gtk.HBox()
        boton8 = Gtk.RadioButton()
        boton8.join_group(boton1)
        boton8.set_active(False)
        hbox.pack_start(boton8, False, False, 0)
        label = Gtk.Label('Instalador fedora (rmp)')
        hbox.pack_start(label, False, False, 5)
        item.add(hbox)
        item.connect("activate", self.__emit_accion, "help rmp")
        self.append(item)

        item = Gtk.MenuItem('Instalador python')
        try:
            item.get_child().destroy()
        except:
            pass
        hbox = Gtk.HBox()
        boton9 = Gtk.RadioButton()
        boton9.join_group(boton1)
        boton9.set_active(False)
        hbox.pack_start(boton9, False, False, 0)
        label = Gtk.Label('Instalador python')
        hbox.pack_start(label, False, False, 5)
        item.add(hbox)
        item.connect("activate", self.__emit_accion, "help python")
        self.append(item)

        item = Gtk.MenuItem('Instalador python (sin root)')
        try:
            item.get_child().destroy()
        except:
            pass
        hbox = Gtk.HBox()
        boton10 = Gtk.RadioButton()
        boton10.join_group(boton1)
        boton10.set_active(False)
        hbox.pack_start(boton10, False, False, 0)
        label = Gtk.Label('Instalador python (sin root)')
        hbox.pack_start(label, False, False, 5)
        item.add(hbox)
        item.connect("activate", self.__emit_accion, "help sin root")
        self.append(item)

        item = Gtk.MenuItem('Instalador sugar')
        try:
            item.get_child().destroy()
        except:
            pass
        hbox = Gtk.HBox()
        boton11 = Gtk.RadioButton()
        boton11.join_group(boton1)
        boton11.set_active(False)
        hbox.pack_start(boton11, False, False, 0)
        label = Gtk.Label('Instalador sugar')
        hbox.pack_start(label, False, False, 5)
        item.add(hbox)
        item.connect("activate", self.__emit_accion, "help sugar")
        self.append(item)

        self.show_all()

    def __emit_accion(self, widget, text):
        valor = not widget.get_children()[0].get_children()[0].get_active()
        if valor:
            widget.get_children()[0].get_children()[0].set_active(valor)
            self.emit("help", text)
