#!/usr/bin/env python
# -*- coding: utf-8 -*-

#   PanelTubeWidgets.py por:
#   Flavio Danesse <fdanesse@gmail.com>
#   Uruguay

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
import shelve

from TubeListDialog import TubeListDialog

from Globales import get_data_directory
from Globales import get_colors
from Globales import get_separador
from Globales import get_boton

BASE_PATH = os.path.dirname(__file__)


class Mini_Toolbar(gtk.Toolbar):
    """
    Mini toolbars Superior izquierda y derecha.
    """

    __gsignals__ = {
    "guardar": (gobject.SIGNAL_RUN_FIRST,
        gobject.TYPE_NONE, []),
    "abrir": (gobject.SIGNAL_RUN_FIRST,
        gobject.TYPE_NONE, (gobject.TYPE_STRING,)),
    "menu_activo": (gobject.SIGNAL_RUN_FIRST,
        gobject.TYPE_NONE, [])}

    def __init__(self, text):

        gtk.Toolbar.__init__(self)

        self.modify_bg(gtk.STATE_NORMAL, get_colors("drawingplayer"))

        self.label = None
        self.texto = text
        self.numero = 0

        item = gtk.ToolItem()
        self.label = gtk.Label("%s: %s" % (text, self.numero))
        #self.label.modify_fg(gtk.STATE_NORMAL, get_colors("window"))
        self.label.show()
        item.add(self.label)
        self.insert(item, -1)

        self.insert(get_separador(draw=False, ancho=0, expand=True), -1)

        archivo = os.path.join(BASE_PATH, "Iconos", "lista.svg")
        boton = get_boton(archivo, flip=False, pixels=24)
        boton.set_tooltip_text("Lista de Búsquedas")
        boton.connect("clicked", self.__get_menu)
        self.insert(boton, -1)

        archivo = os.path.join(BASE_PATH, "Iconos", "play.svg")
        boton = get_boton(archivo, flip=False, pixels=24,
            rotacion=gtk.gdk.PIXBUF_ROTATE_CLOCKWISE)
        boton.set_tooltip_text("Guardar Lista")
        boton.connect("clicked", self.__emit_guardar)
        self.insert(boton, -1)

        self.show_all()

    def __emit_guardar(self, widget):
        """
        Para que se guarden todos los videos en un archivo shelve.
        """
        self.emit('guardar')

    def __emit_abrir(self, key):
        """
        Para que se carguen todos los videos desde un archivo shelve.
        """
        self.emit('abrir', key)

    def __get_menu(self, widget):
        """
        El menu con las listas de videos almacenadas en archivos shelve.
        """
        dict_tube = shelve.open(os.path.join(get_data_directory(),
            "List.tube"))
        keys = dict_tube.keys()
        dict_tube.close()
        if keys:
            self.emit("menu_activo")
            menu = gtk.Menu()
            administrar = gtk.MenuItem('Administrar')
            administrar.connect_object("activate", self.__administrar, None)
            cargar = gtk.MenuItem('Cargar')
            menu.append(administrar)
            menu.append(cargar)
            menu_listas = gtk.Menu()
            cargar.set_submenu(menu_listas)
            for key in keys:
                item = gtk.MenuItem(key)
                menu_listas.append(item)
                item.connect_object("activate", self.__emit_abrir, key)
            menu.show_all()
            menu.attach_to_widget(widget, self.__null)
            gtk.Menu.popup(menu, None, None, None, 1, 0)

    def __administrar(self, widget):
        dialogo = TubeListDialog(parent=self.get_toplevel())
        dialogo.run()
        dialogo.destroy()

    def __null(self):
        pass

    def set_info(self, valor):
        """
        Recibe un entero y actualiza la información.
        """
        if valor != self.numero:
            self.numero = valor
            text = "%s: %s" % (self.texto, str(self.numero))
            self.label.set_text(text)


class ToolbarAccionListasVideos(gtk.Toolbar):
    """
    Toolbar para que el usuario confirme "borrar" lista de video.
    """

    __gsignals__ = {
    "ok": (gobject.SIGNAL_RUN_FIRST,
        gobject.TYPE_NONE, (gobject.TYPE_PYOBJECT,))}

    def __init__(self):

        gtk.Toolbar.__init__(self)

        self.modify_bg(gtk.STATE_NORMAL, get_colors("drawingplayer"))

        self.objetos = None

        self.insert(get_separador(draw=False, ancho=0, expand=True), -1)

        archivo = os.path.join(BASE_PATH, "Iconos", "button-cancel.svg")
        boton = get_boton(archivo, flip=False, pixels=24)
        boton.set_tooltip_text("Cancelar")
        boton.connect("clicked", self.cancelar)
        self.insert(boton, -1)

        self.insert(get_separador(draw=False, ancho=3, expand=False), -1)

        item = gtk.ToolItem()
        self.label = gtk.Label("")
        #self.label.modify_fg(gtk.STATE_NORMAL, get_colors("window"))
        self.label.show()
        item.add(self.label)
        self.insert(item, -1)

        self.insert(get_separador(draw=False, ancho=3, expand=False), -1)

        archivo = os.path.join(BASE_PATH, "Iconos", "dialog-ok.svg")
        boton = get_boton(archivo, flip=False, pixels=24)
        boton.set_tooltip_text("Aceptar")
        boton.connect("clicked", self.__realizar_accion)
        self.insert(boton, -1)

        self.insert(get_separador(draw=False, ancho=0, expand=True), -1)

        self.show_all()

    def __realizar_accion(self, widget):
        """
        Confirma borrar.
        """
        objetos = self.objetos
        self.cancelar()
        gobject.idle_add(self.__emit_ok, objetos)

    def __emit_ok(self, objetos):
        self.emit('ok', objetos)

    def set_accion(self, objetos):
        """
        Configura borrar.
        """
        self.objetos = objetos
        self.label.set_text("¿Eliminar?")
        self.show_all()

    def cancelar(self, widget=None):
        """
        Cancela borrar.
        """
        self.objetos = None
        self.label.set_text("")
        self.hide()


class Toolbar_Videos_Izquierda(gtk.Toolbar):
    """
    toolbar inferior izquierda para videos encontrados.
    """

    __gsignals__ = {
    "borrar": (gobject.SIGNAL_RUN_FIRST,
        gobject.TYPE_NONE, []),
    "mover_videos": (gobject.SIGNAL_RUN_FIRST,
        gobject.TYPE_NONE, [])}

    def __init__(self):

        gtk.Toolbar.__init__(self)

        self.modify_bg(gtk.STATE_NORMAL, get_colors("drawingplayer"))

        self.insert(get_separador(draw=False, ancho=0, expand=True), -1)

        archivo = os.path.join(BASE_PATH, "Iconos", "alejar.svg")
        boton = get_boton(archivo, flip=False, pixels=24)
        boton.set_tooltip_text("Borrar Lista")
        boton.connect("clicked", self.__emit_borrar)
        self.insert(boton, -1)

        archivo = os.path.join(BASE_PATH, "Iconos", "iconplay.svg")
        boton = get_boton(archivo, flip=False, pixels=24)
        boton.set_tooltip_text("Enviar a Descargas")
        boton.connect("clicked", self.__emit_adescargas)
        self.insert(boton, -1)

        self.show_all()

    def __emit_adescargas(self, widget):
        """
        Para pasar los videos encontrados a la lista de descargas.
        """
        self.emit('mover_videos')

    def __emit_borrar(self, widget):
        """
        Para borrar todos los videos de la lista.
        """
        self.emit('borrar')


class Toolbar_Videos_Derecha(gtk.Toolbar):
    """
    toolbar inferior derecha para videos en descarga.
    """

    __gsignals__ = {
    "borrar": (gobject.SIGNAL_RUN_FIRST,
        gobject.TYPE_NONE, []),
    "mover_videos": (gobject.SIGNAL_RUN_FIRST,
        gobject.TYPE_NONE, []),
    'comenzar_descarga': (gobject.SIGNAL_RUN_FIRST,
        gobject.TYPE_NONE, [])}

    def __init__(self):

        gtk.Toolbar.__init__(self)

        self.modify_bg(gtk.STATE_NORMAL, get_colors("drawingplayer"))

        archivo = os.path.join(BASE_PATH, "Iconos", "iconplay.svg")
        boton = get_boton(archivo, flip=True, pixels=24)
        boton.set_tooltip_text("Quitar de Descargas")
        boton.connect("clicked", self.__emit_aencontrados)
        self.insert(boton, -1)

        archivo = os.path.join(BASE_PATH, "Iconos", "alejar.svg")
        boton = get_boton(archivo, flip=False, pixels=24)
        boton.set_tooltip_text("Borrar Lista")
        boton.connect("clicked", self.__emit_borrar)
        self.insert(boton, -1)

        self.insert(get_separador(draw=False, ancho=0, expand=True), -1)

        archivo = os.path.join(BASE_PATH, "Iconos", "iconplay.svg")
        boton = get_boton(archivo, flip=False, pixels=24,
            rotacion=gtk.gdk.PIXBUF_ROTATE_CLOCKWISE)
        boton.set_tooltip_text("Descargar")
        boton.connect("clicked", self.__emit_comenzar_descarga)
        self.insert(boton, -1)

        self.show_all()

    def __emit_comenzar_descarga(self, widget):
        """
        Para comenzar a descargar los videos en la lista de descargas.
        """
        self.emit('comenzar_descarga')

    def __emit_aencontrados(self, widget):
        """
        Para pasar los videos en descarga a la lista de encontrados.
        """
        self.emit('mover_videos')

    def __emit_borrar(self, widget):
        """
        Para borrar todos los videos de la lista.
        """
        self.emit('borrar')


class Toolbar_Guardar(gtk.Toolbar):
    """
    Toolbar con widgets para guardar una lista de videos.
    """

    __gsignals__ = {
    "ok": (gobject.SIGNAL_RUN_FIRST,
        gobject.TYPE_NONE, (gobject.TYPE_STRING, ))}

    def __init__(self):

        gtk.Toolbar.__init__(self)

        self.modify_bg(gtk.STATE_NORMAL, get_colors("drawingplayer"))

        item = gtk.ToolItem()
        label = gtk.Label("Nombre: ")
        #label.modify_fg(gtk.STATE_NORMAL, get_colors("window"))
        label.show()
        item.add(label)
        self.insert(item, -1)

        item = gtk.ToolItem()
        item.set_expand(True)
        self.entrytext = gtk.Entry()
        self.entrytext.set_size_request(50, -1)
        self.entrytext.set_max_length(10)
        self.entrytext.set_tooltip_text("Nombre para Esta Lista")
        self.entrytext.show()
        self.entrytext.connect('activate', self.__emit_ok)
        item.add(self.entrytext)
        self.insert(item, -1)

        self.insert(get_separador(draw=False, ancho=0, expand=True), -1)

        archivo = os.path.join(BASE_PATH, "Iconos", "button-cancel.svg")
        boton = get_boton(archivo, flip=False, pixels=24)
        boton.set_tooltip_text("Cancelar")
        boton.connect("clicked", self.cancelar)
        self.insert(boton, -1)

        archivo = os.path.join(BASE_PATH, "Iconos", "dialog-ok.svg")
        boton = get_boton(archivo, flip=False, pixels=24)
        boton.set_tooltip_text("Guardar")
        boton.connect("clicked", self.__emit_ok)
        self.insert(boton, -1)

        self.show_all()

    def __emit_ok(self, widget):
        texto = self.entrytext.get_text().replace(" ", "_")
        self.cancelar()
        if texto:
            self.emit("ok", texto)

    def cancelar(self, widget=None):
        self.entrytext.set_text("")
        self.hide()
