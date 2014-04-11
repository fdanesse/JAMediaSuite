#!/usr/bin/env python
# -*- coding: utf-8 -*-

#   JAMediaTerminal.py por:
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
from gi.repository import Gdk
from gi.repository import GObject
from gi.repository import GdkPixbuf

from Terminal import Terminal

from Globales import get_separador
from Globales import get_boton
from Globales import get_pixels

BASE_PATH = os.path.dirname(__file__)

from JAMediaManTree.JAMediaManTree import JAMediaManTree

#screen = Gdk.Screen.get_default()
#css_provider = Gtk.CssProvider()
#style_path = os.path.join(
#    BASE_PATH, "Estilo.css")
#css_provider.load_from_path(style_path)
#context = Gtk.StyleContext()
#context.add_provider_for_screen(
#    screen,
#    css_provider,
#    Gtk.STYLE_PROVIDER_PRIORITY_USER)


class Ventana(Gtk.Window):

    #__gtype_name__ = 'WindowJAMediaTerminal'

    def __init__(self):

        Gtk.Window.__init__(self)

        self.set_title("JAMediaTerminal")

        self.set_icon_from_file(
            os.path.join(BASE_PATH,
            "Iconos", "jamediaterminal.svg"))

        self.set_resizable(True)
        self.set_size_request(640, 480)
        self.set_border_width(5)
        self.set_position(Gtk.WindowPosition.CENTER)

        box = Gtk.Box(orientation=Gtk.Orientation.VERTICAL)
        toolbar = Toolbar()
        paned = Gtk.Paned(orientation=Gtk.Orientation.VERTICAL)

        box.pack_start(toolbar, False, False, 0)
        box.pack_start(paned, True, True, 0)

        self.jamediaterminal = Terminal()
        self.jamediamantree = JAMediaManTree()

        paned.pack1(self.jamediamantree, resize=True, shrink=False)
        paned.pack2(self.jamediaterminal, resize=False, shrink=False)

        self.add(box)

        self.show_all()

        self.jamediamantree.hide()

        import sys
        toolbar.connect("help", self.__help)
        toolbar.connect("salir", sys.exit)
        self.connect("destroy", sys.exit)

    def __help(self, widget):
        """
        Muestra u oculta el manual.
        """

        if self.jamediamantree.get_visible():
            self.jamediamantree.hide()

        else:
            self.jamediamantree.show()
            self.jamediaterminal.set_size_request(-1, 150)


class Toolbar(Gtk.Toolbar):
    """
    Toolbar principal.
    """

    __gtype_name__ = 'ToolbarJAMediaTerminal'

    __gsignals__ = {
    'salir': (GObject.SIGNAL_RUN_FIRST,
        GObject.TYPE_NONE, []),
    'help': (GObject.SIGNAL_RUN_FIRST,
        GObject.TYPE_NONE, [])}

    def __init__(self):

        Gtk.Toolbar.__init__(self)

        self.insert(get_separador(draw=False,
            ancho=3, expand=False), -1)

        imagen = Gtk.Image()
        icono = os.path.join(
            BASE_PATH,
            "Iconos",
            "JAMediaTerminal.svg")

        pixbuf = GdkPixbuf.Pixbuf.new_from_file_at_size(icono,
            -1, get_pixels(0.6))
        imagen.set_from_pixbuf(pixbuf)
        imagen.show()
        item = Gtk.ToolItem()
        item.add(imagen)
        self.insert(item, -1)

        self.insert(get_separador(draw=False,
            ancho=0, expand=True), -1)

        # Ayuda.
        archivo = os.path.join(
            BASE_PATH,
            "Iconos",
            "activity-help.svg")

        boton = get_boton(archivo,
            flip=False,
            pixels=get_pixels(0.8))

        boton.set_tooltip_text("Ayuda")
        boton.connect("clicked", self.__emit_help)
        self.insert(boton, -1)

        # Salir.
        archivo = os.path.join(
            BASE_PATH,
            "Iconos",
            "button-cancel.svg")

        boton = get_boton(archivo,
            flip=False,
            pixels=get_pixels(0.8))

        boton.set_tooltip_text("Salir")
        boton.connect("clicked", self.__emit_salir)
        self.insert(boton, -1)

        self.insert(get_separador(draw=False,
            ancho=3, expand=False), -1)

        self.show_all()

    def __emit_salir(self, widget):
        """
        Cuando se hace click en el boton salir.
        """

        self.emit('salir')

    def __emit_help(self, widget):
        """
        Cuando se hace click en el boton salir.
        """

        self.emit('help')


if __name__ == "__main__":
    Ventana()
    Gtk.main()
