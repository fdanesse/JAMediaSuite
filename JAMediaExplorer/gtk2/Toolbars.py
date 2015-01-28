#!/usr/bin/env python
# -*- coding: utf-8 -*-

#   Widgets.py por:
#   Flavio Danesse <fdanesse@gmail.com>
#   Uruguay
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
import gtk
import gobject

from Globales import get_separador
from Globales import get_boton

BASE_PATH = os.path.dirname(os.path.realpath(__file__))
ICONOS = os.path.join(BASE_PATH, "Iconos")


class Toolbar(gtk.EventBox):

    __gsignals__ = {
    "salir": (gobject.SIGNAL_RUN_LAST,
        gobject.TYPE_NONE, []),
    'accion_ver': (gobject.SIGNAL_RUN_FIRST,
        gobject.TYPE_NONE, (gobject.TYPE_STRING,
        gobject.TYPE_BOOLEAN))}

    def __init__(self):

        gtk.EventBox.__init__(self)

        self.modify_bg(0, gtk.gdk.Color(0, 0, 0))
        self.modify_fg(0, gtk.gdk.Color(65000, 65000, 65000))

        toolbar = gtk.Toolbar()
        toolbar.modify_bg(0, gtk.gdk.Color(0, 0, 0))
        toolbar.modify_fg(0, gtk.gdk.Color(65000, 65000, 65000))

        toolbar.insert(get_separador(draw=False, ancho=3, expand=False), -1)

        imagen = gtk.Image()
        icono = os.path.join(ICONOS, "JAMediaExplorer.svg")
        pixbuf = gtk.gdk.pixbuf_new_from_file_at_size(icono, -1, 37)
        imagen.set_from_pixbuf(pixbuf)
        #imagen.modify_bg(0, Gdk.Color(0, 0, 0))
        imagen.show()
        item = gtk.ToolItem()
        item.add(imagen)
        toolbar.insert(item, -1)

        menu = Menu()
        item = gtk.ToolItem()
        #item.set_size_request(100, -1)
        item.set_expand(True)
        item.add(menu)
        menu.connect('accion_ver', self.__re_emit_accion_ver)
        toolbar.insert(item, -1)

        toolbar.insert(get_separador(draw=False, ancho=0, expand=True), -1)

        archivo = os.path.join(ICONOS, "button-cancel.svg")
        boton = get_boton(archivo, flip=False, pixels=37)
        boton.set_tooltip_text("Salir")
        boton.connect("clicked", self.emit_salir)
        toolbar.insert(boton, -1)

        self.add(toolbar)
        self.show_all()

    def __re_emit_accion_ver(self, widget, accion, valor):
        self.emit('accion_ver', accion, valor)

    def emit_salir(self, widget):
        self.emit('salir')


class ToolbarTry(gtk.EventBox):
    """
    Barra de estado de JAMexplorer.
    """

    def __init__(self):

        gtk.EventBox.__init__(self)

        self.modify_bg(0, gtk.gdk.Color(0, 0, 0))
        self.modify_fg(0, gtk.gdk.Color(65000, 65000, 65000))

        toolbar = gtk.Toolbar()
        toolbar.modify_bg(0, gtk.gdk.Color(0, 0, 0))
        toolbar.modify_fg(0, gtk.gdk.Color(65000, 65000, 65000))

        toolbar.insert(get_separador(draw=False, ancho=3, expand=False), -1)

        item = gtk.ToolItem()
        self.label = gtk.Label("Status:")
        self.label.modify_fg(0, gtk.gdk.Color(65000, 65000, 65000))
        self.label.show()
        item.add(self.label)
        toolbar.insert(item, -1)

        toolbar.insert(get_separador(draw=False, ancho=0, expand=True), -1)

        self.add(toolbar)
        self.show_all()


class ToolbarAccion(gtk.EventBox):
    """
    Toolbar para que el usuario confirme borrar un archivo.
    """

    __gsignals__ = {
    "borrar": (gobject.SIGNAL_RUN_LAST,
        gobject.TYPE_NONE, (gobject.TYPE_STRING,
        gobject.TYPE_PYOBJECT, gobject.TYPE_PYOBJECT))}

    def __init__(self):

        gtk.EventBox.__init__(self)

        self.modify_bg(0, gtk.gdk.Color(65000, 65000, 65000))
        self.modify_fg(0, gtk.gdk.Color(0, 0, 0))

        toolbar = gtk.Toolbar()
        toolbar.modify_bg(0, gtk.gdk.Color(65000, 65000, 65000))
        toolbar.modify_fg(0, gtk.gdk.Color(0, 0, 0))

        self.direccion = None
        self.modelo = None
        self.iter = None

        toolbar.insert(get_separador(draw=False, ancho=0, expand=True), -1)

        archivo = os.path.join(ICONOS, "button-cancel.svg")
        boton = get_boton(archivo, flip=False, pixels=30)
        boton.set_tooltip_text("Cancelar")
        boton.connect("clicked", self.cancelar)
        toolbar.insert(boton, -1)

        item = gtk.ToolItem()
        item.set_expand(True)
        self.label = gtk.Label("")
        self.label.modify_fg(0, gtk.gdk.Color(0, 0, 0))
        self.label.show()
        item.add(self.label)
        toolbar.insert(item, -1)

        archivo = os.path.join(ICONOS, "dialog-ok.svg")
        boton = get_boton(archivo, flip=False, pixels=30)
        boton.set_tooltip_text("Aceptar")
        boton.connect("clicked", self.emit_borrar)
        toolbar.insert(boton, -1)

        toolbar.insert(get_separador(draw=False, ancho=0, expand=True), -1)

        self.add(toolbar)
        self.show_all()

    def emit_borrar(self, widget):
        self.emit('borrar', self.direccion, self.modelo, self.iter)
        self.cancelar()

    def set_accion(self, direccion, modelo, iter):
        self.direccion = direccion
        self.modelo = modelo
        self.iter = iter
        texto = direccion
        if len(texto) > 25:
            texto = " . . . " + str(texto[-25:])
        self.label.set_text("¿Borrar?: %s" % (texto))
        self.show_all()

    def cancelar(self, widget=None):
        self.label.set_text("")
        self.direccion = None
        self.modelo = None
        self.iter = None
        self.hide()


class ToolbarSalir(gtk.EventBox):
    """
    Toolbar para confirmar salir de la aplicación.
    """

    __gsignals__ = {
    "salir": (gobject.SIGNAL_RUN_FIRST,
        gobject.TYPE_NONE, [])}

    def __init__(self):

        gtk.EventBox.__init__(self)

        self.modify_bg(0, gtk.gdk.Color(65000, 65000, 65000))
        self.modify_fg(0, gtk.gdk.Color(0, 0, 0))

        toolbar = gtk.Toolbar()
        toolbar.modify_bg(0, gtk.gdk.Color(65000, 65000, 65000))
        toolbar.modify_fg(0, gtk.gdk.Color(0, 0, 0))

        toolbar.insert(get_separador(draw=False, ancho=0, expand=True), -1)

        archivo = os.path.join(ICONOS, "button-cancel.svg")
        boton = get_boton(archivo, flip=False, pixels=30)
        boton.set_tooltip_text("Cancelar")
        boton.connect("clicked", self.cancelar)
        toolbar.insert(boton, -1)

        toolbar.insert(get_separador(draw=False, ancho=3, expand=False), -1)

        item = gtk.ToolItem()
        self.label = gtk.Label("")
        self.label.modify_fg(0, gtk.gdk.Color(0, 0, 0))
        self.label.show()
        item.add(self.label)
        toolbar.insert(item, -1)

        toolbar.insert(get_separador(draw=False, ancho=3, expand=False), -1)

        archivo = os.path.join(ICONOS, "dialog-ok.svg")
        boton = get_boton(archivo, flip=False, pixels=30)
        boton.set_tooltip_text("Aceptar")
        boton.connect("clicked", self.__emit_salir)
        toolbar.insert(boton, -1)

        toolbar.insert(get_separador(draw=False, ancho=0, expand=True), -1)

        self.add(toolbar)
        self.show_all()

    def run(self, nombre_aplicacion):
        self.label.set_text("¿Salir de %s?" % (nombre_aplicacion))
        self.show()

    def __emit_salir(self, widget):
        self.cancelar()
        self.emit('salir')

    def cancelar(self, widget=None):
        self.label.set_text("")
        self.hide()


class Menu(gtk.MenuBar):

    __gsignals__ = {
    'accion_ver': (gobject.SIGNAL_RUN_FIRST,
        gobject.TYPE_NONE, (gobject.TYPE_STRING,
        gobject.TYPE_BOOLEAN))}

    def __init__(self):

        gtk.MenuBar.__init__(self)

        self.modify_bg(0, gtk.gdk.Color(0, 0, 0))
        self.modify_fg(0, gtk.gdk.Color(65000, 65000, 65000))

        item_opciones = gtk.MenuItem('Opciones')
        item_opciones.modify_bg(0, gtk.gdk.Color(0, 0, 0))
        item_opciones.modify_fg(0, gtk.gdk.Color(65000, 65000, 65000))

        menu_opciones = gtk.Menu()
        item_opciones.set_submenu(menu_opciones)
        self.append(item_opciones)

        item = gtk.MenuItem()
        try:
            item.get_child().destroy()
        except:
            pass

        hbox = gtk.HBox()
        button = gtk.CheckButton()
        button.set_active(False)
        hbox.pack_start(button, False, False, 0)
        label = gtk.Label("Ver Ocultos")
        hbox.pack_start(label, False, False, 5)
        item.add(hbox)
        item.connect("activate", self.__emit_accion_ver, "Ocultos")
        menu_opciones.append(item)

        self.show_all()

    def __emit_accion_ver(self, widget, accion):
        valor = not widget.get_children()[0].get_children()[0].get_active()
        widget.get_children()[0].get_children()[0].set_active(valor)
        self.emit('accion_ver', accion, valor)
