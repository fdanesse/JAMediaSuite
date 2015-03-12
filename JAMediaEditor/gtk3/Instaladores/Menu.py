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
        GObject.TYPE_NONE, (GObject.TYPE_STRING, GObject.TYPE_BOOLEAN))}

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

        item = Gtk.MenuItem('Instalador fedora (rmp)')
        try:
            item.get_child().destroy()
        except:
            pass
        hbox = Gtk.HBox()
        boton2 = Gtk.RadioButton()
        boton2.join_group(boton1)
        boton2.set_active(False)
        hbox.pack_start(boton2, False, False, 0)
        label = Gtk.Label('Instalador fedora (rmp)')
        hbox.pack_start(label, False, False, 5)
        item.add(hbox)
        item.connect("activate", self.__emit_accion, "rmp")
        menu.append(item)

        item = Gtk.MenuItem('Instalador python')
        try:
            item.get_child().destroy()
        except:
            pass
        hbox = Gtk.HBox()
        boton3 = Gtk.RadioButton()
        boton3.join_group(boton1)
        boton3.set_active(False)
        hbox.pack_start(boton3, False, False, 0)
        label = Gtk.Label('Instalador python')
        hbox.pack_start(label, False, False, 5)
        item.add(hbox)
        item.connect("activate", self.__emit_accion, "python")
        menu.append(item)

        item = Gtk.MenuItem('Instalador sin root')
        try:
            item.get_child().destroy()
        except:
            pass
        hbox = Gtk.HBox()
        boton4 = Gtk.RadioButton()
        boton4.join_group(boton1)
        boton4.set_active(False)
        hbox.pack_start(boton4, False, False, 0)
        label = Gtk.Label('Instalador sin root')
        hbox.pack_start(label, False, False, 5)
        item.add(hbox)
        item.connect("activate", self.__emit_accion, "sin root")
        menu.append(item)

        item = Gtk.MenuItem('Instalador sugar')
        try:
            item.get_child().destroy()
        except:
            pass
        hbox = Gtk.HBox()
        boton5 = Gtk.RadioButton()
        boton5.join_group(boton1)
        boton5.set_active(False)
        hbox.pack_start(boton5, False, False, 0)
        label = Gtk.Label('Instalador sugar')
        hbox.pack_start(label, False, False, 5)
        item.add(hbox)
        item.connect("activate", self.__emit_accion, "sugar")
        menu.append(item)

        item = Gtk.MenuItem('Ayuda')
        menu = Gtk.Menu()
        item.set_submenu(menu)
        self.append(item)

        item = Gtk.MenuItem('Instaladores en General')
        inicial = item
        try:
            item.get_child().destroy()
        except:
            pass
        hbox = Gtk.HBox()
        boton6 = Gtk.RadioButton()
        boton6.join_group(boton1)
        boton6.set_active(False)
        hbox.pack_start(boton6, False, False, 0)
        label = Gtk.Label('Instaladores en General')
        hbox.pack_start(label, False, False, 5)
        item.add(hbox)
        item.connect("activate", self.__emit_accion, "help instaladores")
        menu.append(item)

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
        menu.append(item)

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
        menu.append(item)

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
        menu.append(item)

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
        menu.append(item)

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
        menu.append(item)

        #self.connect("realize", self.__run, inicial)

        self.show_all()

    #def __run(self, widget, inicial):
    #    self.__emit_accion(inicial, "help instaladores")

    def __emit_accion(self, widget, text):
        valor = not widget.get_children()[0].get_children()[0].get_active()
        if valor:
            widget.get_children()[0].get_children()[0].set_active(valor)
            self.emit("accion-menu", text, valor)
