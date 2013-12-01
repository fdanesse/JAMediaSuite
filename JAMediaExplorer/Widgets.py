#!/usr/bin/env python
# -*- coding: utf-8 -*-

#   Widgets.py por:
#   Flavio Danesse <fdanesse@gmail.com>
#   CeibalJAM - Uruguay
#
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
from gi.repository import GdkPixbuf

import JAMediaObjects

JAMediaObjectsPath = JAMediaObjects.__path__[0]
ICONOS = os.path.join(JAMediaObjects.__path__[0], "Iconos")

from JAMediaObjects.JAMediaGlobales import get_separador
from JAMediaObjects.JAMediaGlobales import get_boton
from JAMediaObjects.JAMediaGlobales import get_pixels


class Toolbar(Gtk.Toolbar):
    """
    Toolbar Principal de JAMexplorer.
    """

    __gtype_name__ = 'JAMediaExplorerToolbar'

    __gsignals__ = {
    "salir": (GObject.SIGNAL_RUN_FIRST,
        GObject.TYPE_NONE, [])}

    def __init__(self):

        Gtk.Toolbar.__init__(self)

        #self.modify_bg(0, Gdk.Color(0, 0, 0))

        self.insert(get_separador(draw=False,
            ancho=3, expand=False), -1)

        imagen = Gtk.Image()
        icono = os.path.join(ICONOS, "JAMediaExplorer.svg")
        pixbuf = GdkPixbuf.Pixbuf.new_from_file_at_size(icono,
            -1, get_pixels(0.8))
        imagen.set_from_pixbuf(pixbuf)
        #imagen.modify_bg(0, Gdk.Color(0, 0, 0))
        imagen.show()
        item = Gtk.ToolItem()
        item.add(imagen)
        self.insert(item, -1)

        self.insert(get_separador(draw=False,
            ancho=0, expand=True), -1)

        archivo = os.path.join(ICONOS, "button-cancel.svg")
        boton = get_boton(archivo, flip=False,
            pixels=get_pixels(1))
        boton.set_tooltip_text("Salir")
        boton.connect("clicked", self.emit_salir)
        self.insert(boton, -1)

        self.show_all()

    def emit_salir(self, widget):

        self.emit('salir')


class ToolbarTry(Gtk.Toolbar):
    """
    Barra de estado de JAMexplorer.
    """

    __gtype_name__ = 'JAMediaExplorerToolbarTry'

    def __init__(self):

        Gtk.Toolbar.__init__(self)

        #self.modify_bg(0, Gdk.Color(0, 0, 0))

        self.insert(get_separador(draw=False,
            ancho=3, expand=False), -1)

        item = Gtk.ToolItem()
        self.label = Gtk.Label("")
        #self.label.modify_fg(0, Gdk.Color(65000, 65000, 65000))
        self.label.show()
        item.add(self.label)
        self.insert(item, -1)

        self.insert(get_separador(draw=False,
            ancho=0, expand=True), -1)

        self.show_all()


class ToolbarAccion(Gtk.Toolbar):
    """
    Toolbar para que el usuario confirme
    borrar un archivo.
    """

    __gtype_name__ = 'JAMediaExplorerToolbarAccion'

    __gsignals__ = {
    "borrar": (GObject.SIGNAL_RUN_FIRST,
        GObject.TYPE_NONE, (GObject.TYPE_STRING,
        GObject.TYPE_PYOBJECT, GObject.TYPE_PYOBJECT))}

    def __init__(self):

        Gtk.Toolbar.__init__(self)

        self.direccion = None
        self.modelo = None
        self.iter = None

        self.insert(get_separador(draw=False,
            ancho=0, expand=True), -1)

        archivo = os.path.join(JAMediaObjectsPath,
            "Iconos", "button-cancel.svg")
        boton = get_boton(archivo, flip=False,
            pixels=get_pixels(0.8))
        boton.set_tooltip_text("Cancelar")
        boton.connect("clicked", self.cancelar)
        self.insert(boton, -1)

        #self.insert(G.get_separador(draw = False,
        #    ancho = 3, expand = False), -1)

        item = Gtk.ToolItem()
        item.set_expand(True)
        self.label = Gtk.Label("")
        self.label.show()
        item.add(self.label)
        self.insert(item, -1)

        #self.insert(G.get_separador(draw = False,
        #    ancho = 3, expand = False), -1)

        archivo = os.path.join(JAMediaObjectsPath,
            "Iconos", "dialog-ok.svg")
        boton = get_boton(archivo, flip=False,
            pixels=get_pixels(0.8))
        boton.set_tooltip_text("Aceptar")
        boton.connect("clicked", self.emit_borrar)
        self.insert(boton, -1)

        self.insert(get_separador(draw=False,
            ancho=0, expand=True), -1)

        self.show_all()

    def emit_borrar(self, widget):
        """
        Cuando se selecciona borrar en el menu de un item.
        """

        self.emit('borrar', self.direccion, self.modelo, self.iter)
        self.cancelar()

    def set_accion(self, direccion, modelo, iter):
        """
        Configura borrar un archivo o directorio.
        """

        self.direccion = direccion
        self.modelo = modelo
        self.iter = iter

        self.label.set_text("¿Borrar?: %s" % (self.direccion))
        self.show_all()

    def cancelar(self, widget=None):
        """Cancela la borrar."""

        self.label.set_text("")

        self.direccion = None
        self.modelo = None
        self.iter = None

        self.hide()
