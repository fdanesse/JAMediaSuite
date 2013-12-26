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
    "salir": (GObject.SIGNAL_RUN_LAST,
        GObject.TYPE_NONE, []),
    'accion_ver': (GObject.SIGNAL_RUN_FIRST,
        GObject.TYPE_NONE, (GObject.TYPE_STRING,
        GObject.TYPE_BOOLEAN))}

    def __init__(self):

        Gtk.Toolbar.__init__(self)

        #self.modify_bg(0, Gdk.Color(0, 0, 0))

        self.insert(get_separador(draw=False,
            ancho=3, expand=False), -1)

        imagen = Gtk.Image()
        icono = os.path.join(ICONOS, "JAMediaExplorer.svg")
        pixbuf = GdkPixbuf.Pixbuf.new_from_file_at_size(icono,
            -1, get_pixels(1.0))
        imagen.set_from_pixbuf(pixbuf)
        #imagen.modify_bg(0, Gdk.Color(0, 0, 0))
        imagen.show()
        item = Gtk.ToolItem()
        item.add(imagen)
        self.insert(item, -1)

        menu = Menu()
        item = Gtk.ToolItem()
        #item.set_size_request(100, -1)
        item.set_expand(True)
        item.add(menu)
        menu.connect('accion_ver', self.__re_emit_accion_ver)
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

    def __re_emit_accion_ver(self, widget, accion, valor):
        """
        Ver o no ver archivos y directorios ocultos.
        """

        self.emit('accion_ver', accion, valor)

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
    "borrar": (GObject.SIGNAL_RUN_LAST,
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

        texto = direccion
        if len(texto) > 25:
            texto = " . . . " + str(texto[-25:])

        self.label.set_text("¿Borrar?: %s" % (texto))
        self.show_all()

    def cancelar(self, widget=None):
        """
        Cancela la borrar.
        """

        self.label.set_text("")

        self.direccion = None
        self.modelo = None
        self.iter = None

        self.hide()


class Menu(Gtk.MenuBar):

    __gtype_name__ = 'JAMediaExplorerMenu'

    __gsignals__ = {
    'accion_ver': (GObject.SIGNAL_RUN_FIRST,
        GObject.TYPE_NONE, (GObject.TYPE_STRING,
        GObject.TYPE_BOOLEAN))}

    def __init__(self):

        Gtk.MenuBar.__init__(self)

        item_opciones = Gtk.MenuItem('Opciones')

        menu_opciones = Gtk.Menu()
        item_opciones.set_submenu(menu_opciones)
        self.append(item_opciones)

        item = Gtk.MenuItem()
        try:
            item.get_child().destroy()

        except:
            pass

        hbox = Gtk.HBox()
        button = Gtk.CheckButton()
        button.set_active(False)
        hbox.pack_start(button, False, False, 0)
        label = Gtk.Label("Ver Ocultos")
        hbox.pack_start(label, False, False, 5)
        item.add(hbox)
        item.connect("activate",
            self.__emit_accion_ver, "Ocultos")
        menu_opciones.append(item)

        self.show_all()

    def __emit_accion_ver(self, widget, accion):
        """
        Ver o no ver archivos y directorios ocultos.
        """

        valor = not widget.get_children()[0].get_children()[0].get_active()
        widget.get_children()[0].get_children()[0].set_active(valor)

        self.emit('accion_ver', accion, valor)
